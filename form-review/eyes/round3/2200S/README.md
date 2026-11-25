# Round 3 Redo Evidence — Form 2200S

- **Class counts on `origin/main` (`93820d0f`)**: `F=98`, `R=0`, `D=0`, `N=1`
- **Class counts on `rules` (`8c3a7b53`)**: `F=98`, `R=0`, `D=0`, `N=1`

## Files
- `mismatches.tsv` — box-by-box list with key, printed item/label, page, saved value, paper output on main & rules, and class (`F`/`R`/`D`/`N`).
- `data-excerpt.txt` — saved draft values read back from SQLite (`r3-redo-g1.db`) for the cited boxes.
- `main/compare.png` — 1400 px crop of the actual form-page boxes beside `origin/main` (`93820d0f`) printed Page 2.
- `rules/compare.png` — 1400 px crop of the actual form-page boxes beside `origin/feat/store-launch-field-rules` (`8c3a7b53`) printed Page 2.
- `2200S-flow.mp4` — short recording showing the filled form boxes and the resulting printed boxes on both commits.

## What these files do not show
- Only the primary Class F boxes are cropped in `compare.png`; every other box and continuation row is itemized in `mismatches.tsv`.
- Demo taxpayer Juana Santos (`000-123-453`) and invented values only; dry-run environment; Queue was never pressed.
