# STATUS.md — Printables Pack Starter Template

Last verified: 2026-10-30

## What was built

An open-book starter template for free printable packs (`free-*-pack` repos),
for Asdale Dynamics, LLC's beginner-friendly, warm, local-first publishing
style. Everything is MIT licensed and copy-ready.

- **Two starter printable sheets** (HTML/CSS, Letter-size, black-and-white
  friendly, brand-free output):
  - `sheets/starter-sheet-1-weekly-reset.html` — ADHD-friendly weekly brain
    dump (three buckets) + pick-3 weekly grid.
  - `sheets/starter-sheet-2-money-glance.html` — one-page monthly bill
    tracker: money in / out / left over, 14-row due table, ruled notes area.
- **Shared print stylesheet**: `assets/print.css` (page setup, recheck-date
  header block styling, print hints; every sheet is meant to print at 100%).
- **Build script**: `scripts/build.py` — stamps the recheck-date header
  block (`Last rebuilt` / `Recheck after` / `Version` from `pack.ini`) into
  every sheet and renders print-ready PDFs into `output/` with WeasyPrint.
  Supports `--check` (validate only, writes nothing).
- **Friendly usage-guide page pattern**: `guide/usage-guide-page.html`
  ("How to Use This Pack" web page) plus doc `guide/USAGE-GUIDE-PATTERN.md`
  describing the pattern's five non-negotiables.
- **Brand-free output folder**: `output/` holds generated PDFs; the repo
  keeps only its README/.gitkeep/.gitignore. A test enforces that brand
  terms never appear in generated PDF text or sheet filenames.
- **Offline test suite**: `tests/test_build.py` — 9 tests covering: every
  sheet builds, PDF magic bytes, exactly one Letter-sized page per sheet
  (catches layout overflow), header-stamp tokens land in output, no
  brand terms in output, required files present, exact LICENSE copyright
  line, CI workflow runs the tests.
- **GitHub Actions workflow**: `.github/workflows/validate.yml` — on every
  push/PR to main: install `weasyprint` + `pypdf`, run `scripts/build.py
  --check`, run the test suite, and upload built PDFs as artifacts.
- **README.md** with getting-started copy and Asdale Dynamics, LLC credit;
  **LICENSE** (MIT) with exact line `Copyright (c) 2026 Asdale Dynamics, LLC`.

## How to run it

```bash
pip install weasyprint pypdf      # one-time, offline afterwards
python3 scripts/build.py          # build PDFs -> output/
python3 scripts/build.py --check  # validate without writing
python3 tests/test_build.py       # run the offline test suite
```

Building one sheet: `python3 scripts/build.py sheets/starter-sheet-1-weekly-reset.html`

## Verification results (2026-10-30)

- `python3 scripts/build.py` — built both PDFs, each exactly 1 Letter page
  (verified by tests and by visual render inspection via `pdftoppm`).
- `python3 tests/test_build.py` — **9/9 tests pass** (`Ran 9 tests ... OK`),
  including offline subprocess-based rebuilds of every sheet.
- `python3 scripts/build.py --check` — both sheets validate.
- Workflow YAML parses (`yaml.safe_load`); both Python files compile.
- Brand-scan: no brand/personal terms in `sheets/`, `assets/`, `guide/`,
  or generated PDFs; `LICENSE` copyright line verified exact by test.
- HTML of all three pages verified well-formed (tag-stack check).

## Known gaps / honest notes

- Sheets are *starter patterns*, not a finished pack — copy the repo, swap
  sheets, and the tests + workflow carry over unchanged.
- No dedicated visual-regression test; layout is validated by page-count,
  page-size, and manual screenshot inspection rather than pixel diffing.
- The usage-guide page is a browser page, not print-tested (by design).
- CI uses pinned-by-major GitHub actions (`@v4`/`@v5`), unpinned by SHA —
  acceptable starter-level risk, easy to tighten later.
- Git history starts at this single initialization commit; no remote, no
  pushes, per instructions.
