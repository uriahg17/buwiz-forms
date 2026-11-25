# Sweep 3 Evidence — BIR Form 1601EQ (`try/forms-band-flow` @ `b9552e27` vs `origin/main` @ `3aceafe8`)

## Files
- `cap-p1.png`, `cap-p2.png`: 6-row Part II ATC return (paper capacity = UI max) at `b9552e27`.
- `plus3-p1.png`, `plus3-p2.png`: return after attempting to add Row 7 in `Additional ATC rows (rows 7 to 30)` at `b9552e27` (blocked by blank Row 7 drawer).
- `main-cap-p1.png`, `main-cap-p2.png`: exact same 6-row return printed at `origin/main` (`3aceafe8`).
- `1601EQ-flow.mp4`: UI flow adding 6 Part II rows, opening the blank Row 7 drawer in `Additional ATC rows`, Saved state, and printed pages.
- `data-excerpt.txt`: persisted SQLite draft values from `sweep3-p1.db`.
- `results.tsv`: per-case audit table.

## What this folder does not show
- `+3` (9 rows) and `+40` (46 rows) could **not** be entered through the running form page at `b9552e27`: `Additional ATC rows (rows 7 to 30)` opens a completely blank Row 7 dialog with zero input controls, and `form.fill` refuses `txtAtcCd*` / `txtTaxBase*`.
