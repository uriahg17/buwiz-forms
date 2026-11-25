# Recheck-2 item b: 1701 item 6

Runtime print verification of the same seeded 1701 return at a067f980 (`new`) and main db022086 (`main`). `before05b.pdf` is the reused recheck-1 output, not reprinted.

The data excerpts in both runtime logs show `taxpayer_type="SingleProprietor"` and `taxpayer_also_compensation_earner=true`; the latter is inherited from the repository sample because the harness only explicitly overrides taxpayer type and spouse compensation status. `sample-and-seed-evidence.txt` records the official payload/steps evidence: the official sample sets both taxpayer-type S and C true, and the actual steps filename is `1701-122025.steps.json` (there is no `1701-122025.official.steps.json`).

The exact extracted taxpayer-type lines and page counts are in `results.tsv`. Page count differs between main and a067f980 (4 vs 5), but the item-6 marking line is identical; page-count movement is separately covered by the nothing-moved comparison against 05b9c989.
