#!/usr/bin/env python3
"""
build.py — build print-ready PDFs for every sheet in this pack.

Usage:
    python3 scripts/build.py              # build every sheet -> PDFs in output/
    python3 scripts/build.py --check      # validate-only, no files written

How it works (fully offline):
    1. Reads every .html file in sheets/ (top level only).
    2. Stamps the recheck-date header tokens ({{BUILD_DATE}},
       {{RECHECK_DATE}}, {{VERSION}}) — these live in each sheet's
       recheck-date header block, so a rebuilt PDF always shows when
       it was made and when it should be re-checked.
    3. Renders HTML + CSS to a Letter-size PDF with WeasyPrint.
    4. Writes PDFs to output/ with the same base name as the sheet.

The pack name, recheck date, and version come from pack.ini at the repo
root so a copied repo only ever edits one small config file.
"""

import configparser
import datetime
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHEETS_DIR = ROOT / "sheets"
OUTPUT_DIR = ROOT / "output"
PACK_INI = ROOT / "pack.ini"


def load_pack_settings() -> dict:
    """Read pack.ini. Falls back to starter defaults if anything is missing."""
    settings = {
        "pack_name": "Free Printables Pack",
        "recheck_after_weeks": 12,
        "version": "0.1.0",
    }
    parser = configparser.ConfigParser()
    if PACK_INI.exists():
        parser.read(PACK_INI, encoding="utf-8")
        if parser.has_section("pack"):
            settings.update(dict(parser.items("pack")))
    recheck_weeks = int(settings["recheck_after_weeks"])
    build_date = datetime.date.today()
    recheck_date = build_date + datetime.timedelta(weeks=recheck_weeks)
    stamped = {
        "{{BUILD_DATE}}": build_date.isoformat(),
        "{{RECHECK_DATE}}": recheck_date.isoformat(),
        "{{VERSION}}": settings["version"],
    }
    return settings | stamped


def stamp_html(html: str, tokens: dict) -> str:
    """Replace every known header token in a sheet's HTML source."""
    for token, value in tokens.items():
        html = html.replace(token, value)
    leftover = '{{' in html and '}}' in html
    if leftover:
        start = html.index('{{')
        raise ValueError(
            "Sheet still has an un-stamped token near: "
            + html[start:start + 40]
        )
    return html


def collect_sheets() -> list[pathlib.Path]:
    """All top-level .html sheets. Sorted so builds are reproducible."""
    if not SHEETS_DIR.is_dir():
        raise SystemExit(f"Missing sheets/ directory: {SHEETS_DIR}")
    sheets = sorted(SHEETS_DIR.glob("*.html"))
    if not sheets:
        raise SystemExit(
            "No sheets found in sheets/. Every readme-pattern sheet lives "
            "there as a single top-level .html file."
        )
    return sheets


def build_pdf(sheet_html: str, css_files: list[pathlib.Path]):
    """Render stamped HTML to a WeasyPrint document (in memory)."""
    from weasyprint import HTML, CSS

    stylesheets = [CSS(filename=str(p)) for p in css_files]
    return HTML(string=sheet_html, base_url=str(SHEETS_DIR)).render(
        stylesheets=stylesheets
    )


def main(argv: list[str]) -> int:
    check_only = "--check" in argv
    only = [a for a in argv if a.endswith(".html")]
    all_sheets = collect_sheets()
    sheets = [s for s in all_sheets if s.name in only] if only else all_sheets

    tokens = load_pack_settings()

    css_files = sorted((ROOT / "assets").glob("*.css"))

    if not sheets:
        print("BUILD FAILED: no matching sheet in sheets/", file=sys.stderr)
        return 1
    results = []
    try:
        for sheet in sheets:
            stamped = stamp_html(sheet.read_text(encoding="utf-8"), tokens)
            document = build_pdf(stamped, css_files)
            pages = len(document.pages)
            result = {"sheet": sheet, "pages": pages, "bytes": None,
                      "document": document}
            if check_only:
                results.append(result)
                print(f"check ok   {sheet.name}  ({pages} page(s))")
            else:
                OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
                out = OUTPUT_DIR / (sheet.stem + ".pdf")
                document.write_pdf(str(out))
                result.update(bytes=out.stat().st_size, path=out)
                results.append(result)
                print(f"built      {sheet.name} -> output/{out.name}  "
                      f"({pages} page(s), {out.stat().st_size} bytes)")
    except Exception as exc:  # noqa: BLE001 — report any failure clearly
        print(f"BUILD FAILED: {exc}", file=sys.stderr)
        return 1

    if not results:
        print("BUILD FAILED: nothing to build", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
