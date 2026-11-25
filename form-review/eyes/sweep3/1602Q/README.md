# Sweep 3 — BIR Form 1602Q

- **Target audited**: `hexuria/buwiz-forms`, branch `try/forms-band-flow` at **`b9552e27`**
- **Comparison baseline**: `origin/main` at **`00a20033`**
- **Verdict**: **TWEAK**

## Summary
Schedule 1 has 14 fixed rows on p2 (filled rows 1-6 print cleanly: 124,666,666.24 matches sum of 6 rows). Schedules 2 & 3 (cap=3) are the growables; p3 prints header-only page.

## Files
- `1602Q-flow.mp4`
- `cap-p1.png`
- `cap-p2.png`
- `cap-p3.png`
- `data-excerpt.txt`
- `main-00a20033-plus3-p1.png`
- `main-00a20033-plus3-p2.png`
- `main-00a20033-plus3-p3.png`
- `maxui-p1.png`
- `maxui-p2.png`
- `maxui-p3.png`
- `plus3-p1.png`
- `plus3-p2.png`
- `plus3-p3.png`
- `results.tsv`

## What this folder does not show
- Cases beyond the UI's maximum row count (e.g., `+40` where the form page caps rows lower) are not fabricated outside the UI.
