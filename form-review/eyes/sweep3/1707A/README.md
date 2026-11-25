# Sweep 3 — BIR Form 1707A

- **Target audited**: `hexuria/buwiz-forms`, branch `try/forms-band-flow` at **`b9552e27`**
- **Comparison baseline**: `origin/main` at **`00a20033`**
- **Verdict**: **TWEAK**

## Summary
Does not use in-page band-flow: falls back to legacy ADDITIONAL SHEET (plus3-p3.png) with blank Taxpayer's Name: — and Return Period: —. All 6 rows present (rows 1-2 on p2, row 3 blank, row 4 OTHERS 419,999,998.18, rows 5-8 CORP_A_R03..R06 summing to 419,999,998.18 on p3).

## Files
- `1707A-flow.mp4`
- `cap-p1.png`
- `cap-p2.png`
- `data-excerpt.txt`
- `main-00a20033-plus3-p1.png`
- `main-00a20033-plus3-p2.png`
- `maxui-p1.png`
- `maxui-p2.png`
- `maxui-p3.png`
- `maxui-p4.png`
- `plus3-p1.png`
- `plus3-p2.png`
- `plus3-p3.png`
- `plus3-p4.png`
- `results.tsv`

## What this folder does not show
- Cases beyond the UI's maximum row count (e.g., `+40` where the form page caps rows lower) are not fabricated outside the UI.
