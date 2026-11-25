# Sweep 3 — BIR Form 1600PT

- **Target audited**: `hexuria/buwiz-forms`, branch `try/forms-band-flow` at **`b9552e27`**
- **Comparison baseline**: `origin/main` at **`00a20033`**
- **Verdict**: **BROKEN**

## Summary
Part II (Page 1, cap=5) silently drops rows 6-8 in plus3 (WB016..WB018, 323,333,331.21 missing) and rows 6-31 in maxui (26 rows dropped) with no band-flow growth and no continuation page. Also Tax Base centavos spill into Tax Rate column (01 3%..05 3%). Page 2 Sched 1 grows cleanly from 4 to 5 rows (7,999,999.95, total left-aligned).

## Files
- `1600PT-flow.mp4`
- `cap-p1.png`
- `cap-p2.png`
- `data-excerpt.txt`
- `main-00a20033-plus3-p1.png`
- `main-00a20033-plus3-p2.png`
- `maxui-p1.png`
- `maxui-p2.png`
- `plus3-p1.png`
- `plus3-p2.png`
- `results.tsv`

## What this folder does not show
- Cases beyond the UI's maximum row count (e.g., `+40` where the form page caps rows lower) are not fabricated outside the UI.
