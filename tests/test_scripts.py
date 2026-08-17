from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD = ROOT / "scripts" / "scaffold_child_theme.py"
VALIDATE = ROOT / "scripts" / "validate_child_theme.py"
PACKAGE = ROOT / "scripts" / "package_child_theme.py"


def run(*arguments: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *(str(value) for value in arguments)],
        check=False,
        capture_output=True,
        text=True,
    )


class ChildThemeScriptsTest(unittest.TestCase):
    def test_skill_includes_admin_and_email_modules(self) -> None:
        required = (
            "references/admin-content-control-center.md",
            "references/forms-and-email-routing.md",
            "references/production-upgrade-catalog.md",
            "assets/content-control-schema-template.php",
            "assets/branded-email-template.php",
        )
        for relative_path in required:
            with self.subTest(relative_path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file())

        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Build Friendly Editing Surfaces", skill_text)
        self.assertIn("Route Forms and Email Safely", skill_text)

    def scaffold(self, root: Path, mode: str, parent: str = "Divi") -> Path:
        child_slug = f"{mode}-child"
        result = run(
            SCAFFOLD,
            "--parent-name",
            parent,
            "--parent-slug",
            parent,
            "--child-name",
            f"{mode.title()} Child",
            "--child-slug",
            child_slug,
            "--mode",
            mode,
            "--output",
            root,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["mode"], mode)
        return root / child_slug

    def test_all_modes_validate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for mode in ("builder", "hybrid", "classic"):
                with self.subTest(mode=mode):
                    theme = self.scaffold(root / mode, mode)
                    result = run(VALIDATE, theme, "--format", "json", "--fail-on", "warning")
                    payload = json.loads(result.stdout)
                    self.assertEqual(result.returncode, 0, result.stdout)
                    self.assertEqual(payload["counts"]["error"], 0)
                    self.assertEqual(payload["counts"]["warning"], 0)

    def test_package_has_single_theme_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            theme = self.scaffold(root / "source", "classic", "astra")
            output = root / "classic-child-v1.0.0.zip"
            result = run(PACKAGE, theme, "--output", output)
            self.assertEqual(result.returncode, 0, result.stderr)

            with zipfile.ZipFile(output) as archive:
                names = archive.namelist()
            self.assertIn("classic-child/style.css", names)
            self.assertIn("classic-child/functions.php", names)
            self.assertTrue(all(name.startswith("classic-child/") for name in names))

    def test_generator_refuses_unsafe_or_existing_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            unsafe = run(
                SCAFFOLD,
                "--parent-name",
                "Bad",
                "--parent-slug",
                "bad/slug",
                "--child-name",
                "Bad Child",
                "--child-slug",
                "bad-child",
                "--output",
                root,
            )
            self.assertNotEqual(unsafe.returncode, 0)

            self.scaffold(root, "builder")
            existing = run(
                SCAFFOLD,
                "--parent-name",
                "Divi",
                "--parent-slug",
                "Divi",
                "--child-name",
                "Builder Child",
                "--child-slug",
                "builder-child",
                "--output",
                root,
            )
            self.assertNotEqual(existing.returncode, 0)


if __name__ == "__main__":
    unittest.main()
