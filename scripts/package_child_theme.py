#!/usr/bin/env python3
"""Package a validated WordPress child-theme directory as an installable ZIP."""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path


EXCLUDED_DIRS = {".git", ".github", "node_modules", "vendor", "tests", "__pycache__", ".pytest_cache"}
EXCLUDED_NAMES = {".DS_Store", "Thumbs.db", ".env", ".env.local", "credentials.json", "service-account.json"}
REQUIRED_HEADER = re.compile(r"^\s*Template:\s*\S+\s*$", re.MULTILINE)


def include(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    if any(part in EXCLUDED_DIRS for part in relative.parts):
        return False
    if path.name in EXCLUDED_NAMES or path.name.startswith(".env."):
        return False
    if path.suffix.lower() in {".log", ".sql", ".sqlite", ".pyc", ".map"}:
        return False
    return path.is_file()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("theme", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.theme.resolve()
    output = args.output.resolve()
    if not root.is_dir():
        raise SystemExit(f"Error: child theme directory does not exist: {root}")
    style = root / "style.css"
    functions = root / "functions.php"
    if not style.is_file() or not functions.is_file():
        raise SystemExit("Error: style.css and functions.php are required")
    if not REQUIRED_HEADER.search(style.read_text(encoding="utf-8", errors="ignore")):
        raise SystemExit("Error: style.css does not contain a valid Template header")
    if output.exists():
        raise SystemExit(f"Error: output already exists; refusing to overwrite: {output}")
    if output.suffix.lower() != ".zip":
        raise SystemExit("Error: output filename must end in .zip")

    selected = sorted(path for path in root.rglob("*") if include(path, root))
    if not selected:
        raise SystemExit("Error: no packageable files found")

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in selected:
            archive.write(path, (Path(root.name) / path.relative_to(root)).as_posix())

    print(f"Created {output} with {len(selected)} file(s) under {root.name}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
