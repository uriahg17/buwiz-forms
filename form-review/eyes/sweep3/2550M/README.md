# Sweep 3 — BIR Form 2550M

- **Target audited**: `hexuria/buwiz-forms`, branch `try/forms-band-flow` at **`b9552e27`**
- **Comparison baseline**: `origin/main` at **`00a20033`**
- **Verdict**: **TWEAK**

## Summary
Drawer fields visibly present on both b9552e27 and 00a20033 (gpui-agent lookup fault, not app). Real X11 input on Sched 2 (cap=4, plus3=7, maxui=10): plus3 grows cleanly inline on p2 (731,111,108.28 / 87,733,324.28); maxui prints all 10 rows on p2 (1,061,111,105.55) with a trailing sparse continuation p3.

## Files
- `2550M-flow.mp4`
- `cap-p1.png`
- `cap-p2.png`
- `data-excerpt.txt`
- `drawer-sched1-00a20033.png`
- `drawer-sched1-b9552e27.png`
- `drawer-sched2-00a20033.png`
- `drawer-sched2-b9552e27.png`
- `drawer-sched3-00a20033.png`
- `drawer-sched3-b9552e27.png`
- `main-00a20033-plus3-p1.png`
- `main-00a20033-plus3-p2.png`
- `main-cap-p1.png`
- `main-cap-p2.png`
- `maxui-p1.png`
- `maxui-p2.png`
- `maxui-p3.png`
- `plus3-p1.png`
- `plus3-p2.png`
- `results.tsv`

## What this folder does not show
- Cases beyond the UI's maximum row count (e.g., `+40` where the form page caps rows lower) are not fabricated outside the UI.
