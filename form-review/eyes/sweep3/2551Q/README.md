# Sweep 3 Evidence — BIR Form 2551Q (`try/forms-band-flow` @ `b9552e27` vs `origin/main` @ `3aceafe8`)

## Files
- `cap-p1.png`, `cap-p2.png`: 6-row Schedule 1 return (paper capacity) printed at `b9552e27`.
- `r6-fit-p1.png`, `r6-fit-p2.png`: Rule 6 Item 17 specify text that fits inline (`PRIOR EXCESS CREDIT`) at `b9552e27`.
- `r6-over-p1.png`, `r6-over-p2.png`: Rule 6 Item 17 long specify text at `b9552e27` — **shows 2nd wrapped line (`OVER`) struck through by Item 18's top border**.
- `main-cap-p1.png`, `main-cap-p2.png`, `main-r6-over-p1.png`, `main-r6-over-p2.png`: exact same returns printed at `origin/main` (`3aceafe8`).
- `2551Q-flow.mp4`: UI flow + print pages for 2551Q.
- `data-excerpt.txt`: persisted SQLite draft values from `sweep3-p1.db`.
- `results.tsv`: per-case audit table.

## What this folder does not show
- `+3` (9 rows) and `+40` (46 rows) could **not** be entered through the running form page at `b9552e27`: Schedule 1 caps at 6 rows (no `Add row` past 6), and rows 2–6 ATC drawers display `"Can't be filled on this page yet."` (so rows 2–6 ATC remain blank in the saved draft).
