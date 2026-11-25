# Recheck-2 item c: 0605 long name/address/line-of-business

Runtime print verification at a067f980 using exact-length values at 60, 100, 137 and 200 chars; every value includes the required 40-character unbreakable word. `before05b-len*.pdf` files are reused recheck-1 evidence at 05b9c989, not reprinted.

All a067f980 outputs are A4, two pages when an additional sheet is needed. The measured field text on page 1 and the additional-entry text are fontspec 11, approximately 8.25pt under the established poppler conversion; no tested field measured below the 7.5pt A4 floor. Header label text can measure 7.5pt but is not the shrunken field value. No case uses a third line. Exact additional-entry occurrence counts are in `analysis.json` and summarized in `results.tsv`.

Interpretation of exact-fit cases: len60/100 name and len60/100/137 address occupy two lines without ellipsis, so no additional-sheet entry is required. The narrow line-of-business box ellipsizes at all tested lengths because of the 40-character unbreakable word; its full value appears exactly once in the additional sheet.
