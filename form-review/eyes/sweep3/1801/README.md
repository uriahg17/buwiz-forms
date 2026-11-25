# Sweep 3 — BIR Form 1801

- **Target audited**: `hexuria/buwiz-forms`, branch `try/forms-band-flow` at **`b9552e27`**
- **Comparison baseline**: `origin/main` at **`00a20033`**
- **Verdict**: **CLEAN**

## Summary
Edge case (two tables on same page both growing): Sched 1 (2->5 in plus3, 2->25 in maxui) and Sched 1A (2->5 in plus3, 2->17 in maxui) both grow cleanly inline! Totals match arithmetic (plus3: 516,666,665.15 each -> 1,033,333,330.30; maxui: 2,861,111,078.25 + 1,869,999,984.53 = 4,731,111,062.78). Page 2 (continued) has TIN, Name, repeated section title, and repeated table head.

## Files
- `1801-flow.mp4`
- `cap-p1.png`
- `cap-p2.png`
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
