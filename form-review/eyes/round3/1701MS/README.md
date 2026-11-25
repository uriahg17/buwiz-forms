# Round 3 Redo Evidence — Form 1701MS (Class F = 0, Withdrawn)

- **Class counts on `origin/main` (`93820d0f`)**: `F=0`, `R=0`, `D=0`, `N=5`
- **Class counts on `rules` (`8c3a7b53`)**: `F=0`, `R=0`, `D=0`, `N=5`

## Verdict
Every value persisted in the saved draft prints cleanly in its drawn sheet box on both commits. Any remaining entries in `mismatches.tsv` are Class `R` (extra rows beyond the printed sheet) or Class `N` (internal/helper/derived/signatory keys not meant to print).

## Files
- `mismatches.tsv` — exact per-box classification.
- `data-excerpt.txt` — saved draft values read back from SQLite (`r3-redo-g1.db`).
