# Sweep 3 Evidence — BIR Form 1601C (`try/forms-band-flow` @ `b9552e27` vs `origin/main` @ `3aceafe8`)

## Files
- `cap-p1.png`, `cap-p2.png`: 3-row Schedule I return (paper capacity = UI max) at `b9552e27`.
- `r6-fit-p1.png`, `r6-fit-p2.png`: Rule 6 Item 20 specify text that fits inline (`HAZARD ALLOWANCE`) at `b9552e27`.
- `r6-over-p1.png`, `r6-over-p2.png`, `r6-over-p3.png`: Rule 6 Item 20 long specify text at `b9552e27` — **shows (1) 2nd line `REGULATIONS` struck through by Item 21's top border on p1, and (2) empty stamp box kicked onto Page 1 (continued) p2 with a cut-off continuation header missing TIN and Taxpayer's Name**.
- `main-cap-p1.png`, `main-cap-p2.png`, `main-r6-over-p1.png`, `main-r6-over-p2.png`: exact same returns printed at `origin/main` (`3aceafe8`).
- `1601C-flow.mp4`: UI flow + printed pages.
- `data-excerpt.txt`: persisted SQLite draft values from `sweep3-p1.db`.
- `results.tsv`: per-case audit table.

## What this folder does not show
- `+3` (6 rows) and `+40` (43 rows) could **not** be entered through the running form page at `b9552e27`: Schedule I caps at 3 rows (`Add row` disappears after row 3).
