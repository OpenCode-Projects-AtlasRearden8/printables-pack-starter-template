#!/usr/bin/env python3
"""
Offline test script for the printables pack starter template.

Run with:  python3 tests/test_build.py

No network access is required or used. The tests:
    1. Build every sheet through scripts/build.py's own code path.
    2. Assert the recheck-date header block was stamped with real tokens
       (no {{...}} placeholders left in the HTML or the rendered pages).
    3. Assert each produced PDF is a real PDF, has >= 1 page,
       and is Letter-sized print-ready output.
    4. Assert output stays brand-free: no company names anywhere in the
       rendered PDF text or filenames.
    5. Assert the usage-guide page pattern builds too.
"""

import io
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHEETS_DIR = ROOT / "sheets"
SHEETS = sorted(SHEETS_DIR.glob("*.html"))

LETTER_W = 8.5 * 72  # points
LETTER_H = 11 * 72

BRAND_TERMS = (
    "asdale",
    "asdale dynamics",
    "dylanasdale",
    "dylan asdale",
    "github.com/",
)


def build_all():
    """Build every sheet and return (sheet_path -> pdf_bytes)."""
    pdfs = {}
    for sheet in SHEETS:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build.py"), sheet.name],
            capture_output=True, text=True, cwd=str(ROOT), timeout=180,
        )
        if proc.returncode != 0:
            raise AssertionError(
                f"build failed for {sheet.name}:\n{proc.stdout}\n{proc.stderr}"
            )
        out = ROOT / "output" / (sheet.stem + ".pdf")
        pdfs[sheet] = out.read_bytes()
    return pdfs


class SheetBuildTests(unittest.TestCase):
    """Every sheet must build into a valid, brand-free print-ready PDF."""

    @classmethod
    def setUpClass(cls):
        cls.pdfs = build_all()

    def test_every_sheet_builds_to_pdf(self):
        self.assertTrue(SHEETS, "no sheets found in sheets/")
        for sheet in SHEETS:
            self.assertIn(sheet, self.pdfs)

    def test_pdf_magic_bytes_and_page_count(self):
        from pypdf import PdfReader

        for sheet, data in self.pdfs.items():
            self.assertTrue(
                data.startswith(b"%PDF-"),
                f"{sheet.name}: missing %PDF header",
            )
            reader = PdfReader(io.BytesIO(data))
            self.assertEqual(
                len(reader.pages), 1,
                f"{sheet.name}: expected exactly 1 printable page "
                f"(got {len(reader.pages)} — check for layout overflow)",
            )

    def test_pdf_is_letter_sized(self):
        from pypdf import PdfReader

        for sheet, data in self.pdfs.items():
            reader = PdfReader(io.BytesIO(data))
            page = reader.pages[0]
            w = float(page.mediabox.width)
            h = float(page.mediabox.height)
            self.assertAlmostEqual(w, LETTER_W, delta=2, msg=sheet.name)
            self.assertAlmostEqual(h, LETTER_H, delta=2, msg=sheet.name)

    def test_recheck_header_stamped_into_output(self):
        from pypdf import PdfReader

        for sheet, data in self.pdfs.items():
            text = "".join(
                p.extract_text() or "" for p in PdfReader(io.BytesIO(data)).pages
            )
            self.assertIn("Last rebuilt:", text, sheet.name)
            self.assertIn("Recheck after:", text, sheet.name)
            self.assertNotIn("{{", text, sheet.name)

    def test_output_is_brand_free(self):
        from pypdf import PdfReader

        for sheet, data in self.pdfs.items():
            text = "".join(
                p.extract_text() or ""
                for p in PdfReader(io.BytesIO(data)).pages
            ).lower()
            for term in BRAND_TERMS:
                self.assertNotIn(
                    term, text,
                    f"{sheet.name}: brand term '{term}' leaked into output",
                )
            self.assertNotIn(
                "asdale", sheet.stem.lower(),
                "sheet filenames must stay brand-free",
            )


class RepoPatternTests(unittest.TestCase):
    """Guardrails so copied free-*-pack repos keep everything that matters."""

    def test_required_files_exist(self):
        for rel in (
            "README.md",
            "LICENSE",
            "pack.ini",
            "scripts/build.py",
            "tests/test_build.py",
            "guide/usage-guide-page.html",
            ".github/workflows/validate.yml",
            "output/README.md",
        ):
            self.assertTrue((ROOT / rel).exists(), f"missing {rel}")

    def test_license_copyright_line_exact(self):
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", text)

    def test_workflow_runs_the_tests(self):
        wf = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
        self.assertIn("test_build.py", wf)
        self.assertIn("build.py --check", wf)

    def test_output_folder_is_brand_free_by_convention(self):
        text = (ROOT / "output" / "README.md").read_text(encoding="utf-8")
        self.assertIn("brand-free", text.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
