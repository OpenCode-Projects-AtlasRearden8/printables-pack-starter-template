# Usage Guide Page Pattern

`usage-guide-page.html` is the copy pattern every free-*-pack repo ships with.
It is the friendly "how to use this pack" page users land on first.

## The pattern's five non-negotiables

1. **Open-book promise near the top** — say in plain words what is free and
   what will never be required (sign-ups, emails, accounts: none).
2. **Recheck-date block in the header** — `Last updated` / `Version` /
   `Recheck URL` always visible, same pattern as printed sheets.
3. **"You will need" section** — set expectations low. A printer, any paper,
   any pen. Maybe a friend's printer.
4. **Numbered print steps with the 100% scale tip** — the single most common
   print question, answered before it is asked.
5. **Honest Q&A at the bottom** — including "is this advice?" answered with a
   clear no for any pack that touches money, health, or work decisions.

## Copying it into a new pack

```bash
cp guide/usage-guide-page.html ../free-my-pack/guide/usage-guide-page.html
```

Then edit:

- The `<title>` and `<h1>` to the pack's real name.
- The sheet table rows to describe the pack's actual sheets.
- The `REPLACE-WITH-DATE` / `REPLACE-WITH-VERSION` placeholders.
- The footer credit line to point at the new repo's README.

Keep the tone: warm, short sentences, zero jargon, no condescension.
