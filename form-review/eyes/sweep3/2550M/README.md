# Sweep 3 Evidence — BIR Form 2550M (`try/forms-band-flow` @ `b9552e27` vs `origin/main` @ `3aceafe8`)

## Files
- `cap-p1.png`, `cap-p2.png`: Part II filled return printed at `b9552e27` (Schedules 1–8 blank due to UI blocker).
- `main-cap-p1.png`, `main-cap-p2.png`: exact same return printed at `origin/main` (`3aceafe8`).
- `2550M-flow.mp4`: captures the blank Schedule 2 Row 1 drawer on the form page, Saved state, and printed pages.
- `data-excerpt.txt`: persisted SQLite draft values from `sweep3-p1.db`.
- `results.tsv`: per-case audit table.

## What this folder does not show
- Schedule 1–8 rows (`cap`, `+3`, `+40`) could **not** be entered through the running form page at `b9552e27`: clicking `Add row` in Schedules 1, 2, or 3 opens an empty `Row 1` dialog with zero input controls, and `form.fill` refuses all schedule keys (`"written through the form's own editors"`).
