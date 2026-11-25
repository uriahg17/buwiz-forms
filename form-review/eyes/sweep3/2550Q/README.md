# Sweep 3 Evidence — BIR Form 2550Q (`try/forms-band-flow` @ `b9552e27` vs `origin/main` @ `3aceafe8`)

## Files
- `cap-p1.png`, `cap-p2.png`: Schedule 1 at paper capacity (2 rows) at `b9552e27`.
- `cap-plus1-p1.png`, `cap-plus1-p2.png`: edge case capacity + 1 (3 rows) at `b9552e27`.
- `plus3-p1.png`, `plus3-p2.png`: `+3` (5 Schedule 1 rows) at `b9552e27` — grows cleanly on p2; shows Col B/F/G alignment and `60.00` vs `60` formatting differences.
- `maxui-p1.png`, `maxui-p2.png`: UI maximum (12 Schedule 1 rows saved in DB) at `b9552e27` — **shows rows 11–12 (`CAPGOOD_R11`, `CAPGOOD_R12`) silently dropped with no page 3 while Total prints the 12-row sum (`128,666,658.78`)**.
- `r6-fit-p1.png`, `r6-fit-p2.png`, `r6-over-p1.png`, `r6-over-p2.png`: Rule 6 Item 19 specify fit vs overflow at `b9552e27` (clean).
- `main-plus3-p1.png`, `main-plus3-p2.png`, `main-r6-over-p1.png`, `main-r6-over-p2.png`: exact same `+3` and `r6-over` returns printed at `origin/main` (`3aceafe8`).
- `2550Q-flow.mp4`: UI flow adding Schedule 1 rows + `+3` printed pages.
- `data-excerpt.txt`: persisted SQLite draft values from `sweep3-p1.db`.
- `results.tsv`: per-case audit table.

## What this folder does not show
- `+40` (42 rows) could **not** be entered through the running form page at `b9552e27`: Schedule 1 caps at 12 rows in the UI.
