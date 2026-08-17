#!/usr/bin/env python3
"""Validate high-signal structural properties of a WordPress child theme."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


HEADER = re.compile(r"^\s*([A-Za-z ]+):\s*(.+?)\s*$", re.MULTILINE)
REQUIRED_HEADERS = ("Theme Name", "Template", "Version", "Text Domain")
SECRET_NAMES = {".env", ".env.local", "credentials.json", "service-account.json", "id_rsa", "id_ed25519"}
IGNORED_DIRS = {".git", "node_modules", "vendor", "__pycache__", ".pytest_cache"}
LOCAL_URL = re.compile(r"https?://(?:localhost|127\.0\.0\.1|[^/\s'\"]+\.local)(?=[/:\s'\"])", re.I)
ASSET_REFERENCE = re.compile(r"get_stylesheet_directory_uri\(\)\s*\.\s*['\"](/[^'\"]+)['\"]")


@dataclass(frozen=True)
class Finding:
    severity: str
    check: str
    message: str
    evidence: list[str]


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def files(root: Path) -> list[Path]:
    result: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or any(part in IGNORED_DIRS for part in path.parts):
            continue
        result.append(path)
    return result


def relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def validate(root: Path) -> tuple[list[Finding], dict[str, str]]:
    findings: list[Finding] = []
    headers: dict[str, str] = {}
    style = root / "style.css"
    functions = root / "functions.php"

    if not style.is_file():
        findings.append(Finding("error", "missing-style-css", "style.css is required.", ["style.css"]))
    else:
        headers = {key.strip(): value.strip() for key, value in HEADER.findall(read(style))}
        missing = [key for key in REQUIRED_HEADERS if not headers.get(key)]
        if missing:
            findings.append(
                Finding("error", "missing-theme-headers", f"Missing required style.css headers: {', '.join(missing)}.", ["style.css"])
            )

    if not functions.is_file():
        findings.append(Finding("error", "missing-functions-php", "functions.php is required.", ["functions.php"]))
    else:
        content = read(functions)
        if "ABSPATH" not in content:
            findings.append(Finding("warning", "missing-direct-access-guard", "functions.php does not visibly guard direct access.", ["functions.php"]))
        for reference in ASSET_REFERENCE.findall(content):
            asset = root / reference.lstrip("/")
            if not asset.exists():
                findings.append(
                    Finding("error", "missing-enqueued-asset", f"Enqueued child asset is missing: {reference}.", ["functions.php"])
                )

    theme_files = files(root)
    for path in theme_files:
        name = path.name
        rel = relative(root, path)
        if name in SECRET_NAMES or (name.startswith(".env") and name not in {".env.example", ".env.sample"}):
            findings.append(Finding("error", "secret-bearing-file", "Secret-bearing file must not be packaged.", [rel]))
        if path.suffix.lower() in {".php", ".css", ".js", ".html", ".json"}:
            content = read(path)
            if LOCAL_URL.search(content):
                findings.append(Finding("warning", "local-url", "Local development URL is embedded in theme source.", [rel]))
            if path.suffix.lower() == ".php" and path.name not in {"header.php", "footer.php"}:
                wrappers = [tag for tag in ("<html", "<head", "<body") if tag in content.lower()]
                if wrappers:
                    findings.append(
                        Finding("warning", "document-wrapper-in-template", f"Template includes document wrappers: {', '.join(wrappers)}.", [rel])
                    )

    header = root / "header.php"
    footer = root / "footer.php"
    if header.exists() or footer.exists():
        required = {
            "header.php": ("wp_head()", "body_class()", "wp_body_open()"),
            "footer.php": ("wp_footer()",),
        }
        for filename, tokens in required.items():
            path = root / filename
            if not path.exists():
                findings.append(Finding("error", "incomplete-classic-shell", f"Classic shell is missing {filename}.", [filename]))
                continue
            absent = [token for token in tokens if token not in read(path)]
            if absent:
                findings.append(
                    Finding("error", "missing-wordpress-hook", f"{filename} is missing: {', '.join(absent)}.", [filename])
                )

    return findings, headers


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("theme", type=Path)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--fail-on", choices=("never", "error", "warning"), default="error")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.theme.resolve()
    if not root.is_dir():
        raise SystemExit(f"Error: child theme directory does not exist: {root}")
    findings, headers = validate(root)
    order = {"error": 0, "warning": 1, "info": 2}
    findings.sort(key=lambda item: (order[item.severity], item.check, item.evidence))
    counts = {level: sum(item.severity == level for item in findings) for level in ("error", "warning", "info")}

    if args.format == "json":
        print(json.dumps({"theme": str(root), "headers": headers, "counts": counts, "findings": [asdict(item) for item in findings]}, indent=2))
    else:
        print("# Child Theme Validation\n")
        print(f"- Theme: `{root}`")
        print(f"- Parent slug: `{headers.get('Template', 'unknown')}`")
        print(f"- Version: `{headers.get('Version', 'unknown')}`")
        print(f"- Findings: **{counts['error']} error(s)**, **{counts['warning']} warning(s)**")
        if findings:
            print("\n## Findings")
            for index, item in enumerate(findings, 1):
                print(f"\n### {index}. {item.severity.upper()} — {item.check}\n")
                print(item.message)
                print("\nEvidence: " + ", ".join(f"`{value}`" for value in item.evidence))
        else:
            print("\nNo structural problems detected.")

    if args.fail_on == "warning" and (counts["error"] or counts["warning"]):
        return 1
    if args.fail_on == "error" and counts["error"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
