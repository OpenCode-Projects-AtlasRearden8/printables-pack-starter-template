# Printables Pack Starter Template (free-*-pack pattern)

A copy-and-go starter template for Asdale Dynamics, LLC's **free printable
packs** — the open-book pattern: every sheet, its HTML/CSS source, its build
script, and its friendly usage guide are all public and MIT licensed. Nothing
is gated, no accounts, no email collection, ever.

Copies cleanly into new `free-*-pack` repositories: rename the folder, edit
`pack.ini`, and you have a working, tested printable pack.

## What's in the box

| Path | What it is |
| --- | --- |
| `sheets/` | Two starter printable sheets (HTML + shared print CSS): **Weekly Reset** and **Money at a Glance** |
| `scripts/build.py` | One-command build: stamps each sheet's **recheck-date header block** and renders print-ready PDFs into `output/` |
| `guide/usage-guide-page.html` | The friendly "How to Use This Pack" page pattern (see `guide/USAGE-GUIDE-PATTERN.md`) |
| `output/` | Brand-free generated PDFs. Regenerable; safe to delete |
| `pack.ini` | Pack name, version, and recheck window — the *only* file most copy-packs need to edit |
| `tests/test_build.py` | Offline test suite: PDFs must be real, Letter-sized, header-stamped, and brand-free |
| `.github/workflows/validate.yml` | GitHub Actions: validates **every sheet builds** on every push and PR |

## Getting started (3 steps)

```bash
# 1. Build every sheet into a print-ready PDF
python3 scripts/build.py

# 2. Open a PDF (or just print it — set printer scale to 100%)
open output/starter-sheet-1-weekly-reset.pdf     # macOS
xdg-open output/starter-sheet-1-weekly-reset.pdf # Linux

# 3. Run the offline tests any time you touch a sheet
python3 tests/test_build.py
```

Requirements: Python 3.10+ and two pip packages, no network needed to build
or test once installed:

```bash
pip install weasyprint pypdf
```

## The recheck-date header block

Every printed sheet starts with the same header pattern:

```
Last rebuilt: <today>   Recheck after: <build + pack.ini window>   Version: <semver>
```

`scripts/build.py` stamps these from `pack.ini` at build time, so a rebuilt
pack always tells readers when to grab a fresh copy — without anyone hand-
editing dates. The test suite verifies no unstamped `{{...}}` placeholders
reach the PDF, and the CI workflow re-checks that on every push.

## Brand-free output rule

Printed sheets never carry a company name, logo, personal name, or URL.
Branding lives in this README and LICENSE only. The offline tests assert
brand terms never appear in generated PDF text or filenames.

## Copying into a new free-*-pack repo

1. Copy this whole folder (or the repo) to `free-whatever-pack/`.
2. Edit `pack.ini`: pack name, version, recheck window.
3. Delete the starter sheets in `sheets/`, add your own `.html` files there
   (one file = one printable PDF; reuse `assets/print.css` and copy the
   recheck-date header block markup — it is required on every sheet).
4. Update `guide/usage-guide-page.html`'s sheet table for your sheets.
5. Run `python3 tests/test_build.py`. Green means your pack ships.

## Credits & license

Maintained as part of Asdale Dynamics, LLC's beginner-friendly AI education
and small-business tools. The idea behind the open-book printable pattern:
free, practical paper helpers, published in the open.

Code, sheets, and guides are MIT licensed — see [LICENSE](LICENSE):
Copyright (c) 2026 Asdale Dynamics, LLC

Printed sheets are paper tools for personal use, not professional advice.
