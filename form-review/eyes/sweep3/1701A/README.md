# Sweep 3 Evidence — BIR Form 1701A (`try/forms-band-flow` @ `b9552e27` vs `origin/main` @ `3aceafe8`)

## Files
- `cap-p1.png`, `cap-p2.png`: paper capacity (2 rows) at `b9552e27`.
- `cap-plus1-p1.png`, `cap-plus1-p2.png`: edge case capacity + 1 (1 extra modal row) at `b9552e27`.
- `plus3-p1.png`, `plus3-p2.png`: `+3` (3 extra modal rows `42a..42c`) at `b9552e27` — **shows Item 42 `OTHERS` double-counting `42a..42c` on paper**.
- `maxui-p1.png`, `maxui-p2.png`, `maxui-p3.png`: UI maximum (12 extra modal rows `42a..42l`) at `b9552e27` — shows clean `Page 2 (continued)` header on p3 (Part V) and the same Item 42 `OTHERS` double-count on p2.
- `r6-fit-p1.png`, `r6-fit-p2.png`, `r6-over-p1.png`, `r6-over-p2.png`: Rule 6 Item 63 specify fit vs overflow at `b9552e27` (clean).
- `main-plus3-p1.png`, `main-plus3-p2.png`, `main-r6-over-p1.png`, `main-r6-over-p2.png`: exact same `+3` and `r6-over` returns printed at `origin/main` (`3aceafe8`).
- `1701A-flow.mp4`: UI flow + `+3` printed pages.
- `data-excerpt.txt`: persisted SQLite draft values from `sweep3-p1.db`.
- `results.tsv`: per-case audit table.

## What this folder does not show
- `+40` (42 rows) could **not** be entered through the running form page at `b9552e27`: Part IV.A modal rows cap at 12 (`txtmodalPartIVA_0..11`).

## Follow-up comparison at `origin/main` (`00a20033`)
- `main-00a20033-plus3-p1.png`, `main-00a20033-plus3-p2.png`, `main-00a20033-maxui-p1.png`, `main-00a20033-maxui-p2.png`: the same `+3` and `maxui` returns printed at `origin/main` `00a20033`. Main prints only 2 pages with Item 42 `OTHERS` as a single summary line (no `42a..42l` inline), confirming the official sheet treats Item 42 as a summary line whose details belong on an attached sheet — so `b9552e27` expanding `42a..42l` inline under Item 42 while keeping Item 42's sum double-counts them on paper.
