# output/ — built PDFs land here

Running `python3 scripts/build.py` writes one print-ready PDF per sheet into
this folder, named after the sheet it came from.

Two house rules:

1. **Everything here is brand-free.** Generated PDFs and their filenames never
   contain company names, logos, personal names, or URLs. Branding lives in
   README.md and LICENSE at the repo root — it never reaches the printed page.
   A test (`tests/test_build.py`) enforces this.
2. **Files here are generated.** They can be deleted and rebuilt any time
   with one command, so they are safe to gitignore — keeping only this README
   and .gitkeep in the repo.
