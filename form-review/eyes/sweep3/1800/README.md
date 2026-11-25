# Sweep 3 — BIR Form 1800

- **Target audited**: `hexuria/buwiz-forms`, branch `try/forms-band-flow` at **`b9552e27`**
- **Comparison baseline**: `origin/main` at **`00a20033`**
- **Verdict**: **BROKEN**

## Summary
Two band-flow faults on plus3-p2.png & plus3-p3.png: (1) Extra rows in Sched A (GIFT_PERS_R06..R08) and Sched B (OCT-006..OCT-010) are inserted AFTER 5 blank rows (6-10) and misnumbered 11-13 / 11-15 instead of directly under row 5; (2) Sched B Continuation breaks to Page 2 (continued) (plus3-p3.png) with NO repeated table head and NO section title (starts directly at row 2). Total 839,999,996.36 matches sum of 8 rows.

## Files
- `1800-flow.mp4`
- `cap-p1.png`
- `cap-p2.png`
- `cap-p3.png`
- `data-excerpt.txt`
- `main-00a20033-plus3-p1.png`
- `main-00a20033-plus3-p2.png`
- `maxui-p1.png`
- `maxui-p2.png`
- `maxui-p3.png`
- `plus3-p1.png`
- `plus3-p2.png`
- `plus3-p3.png`
- `results.tsv`

## What this folder does not show
- Cases beyond the UI's maximum row count (e.g., `+40` where the form page caps rows lower) are not fabricated outside the UI.
