# Ten-form nothing-else-moved comparison

Scope: all ten first-check forms (`0605`, `1701`, `1600WP`, `1702Q`, `2550Q`, `2551Q`, `1601C`, `1702MX`, `2000OT`, `0619E`) were compared at `3e8b1212` versus `05b9c989` using the same seeded returns. The old sides are the clean per-commit PDFs from the first check; the new sides were reprinted in this recheck. Every form has matching preview-capture count and PDF page count at the new commit.

Files:
- `comparison.tsv` / `comparison.json`: machine-generated per-page image-difference percentages plus token/numeric extraction differences.
- `results.tsv`: human adjudication of whether each changed box is intended, correct, questionable, or a regression.
- `crop-taxpayer-type-old/new.png`: 1701 wrong-checkbox regression.
- `1600wp-crop-additional-header-old/new.png`: 1600WP wrong-TIN regression.
- `crop-other-credits-old/new.png`: 1702Q specify behavior change.
- Per-form directories beside this one contain the underlying PDFs, every rendered page, preview captures, extraction text/bbox/font files, crops, results and recordings.

Important extraction caveat: `pdftotext` concatenates adjacent cells differently when layout/alignment changes, and comb digits may be separate digits in one print but comma-grouped strings in another. Therefore raw token counts in `comparison.tsv` are investigative signals, not automatic proof of value loss. The verdicts in `results.tsv` are based on targeted raw-text inspection and visual crops.

Detected regressions beyond the five faults:
1. 1701 Part I item 6 marks both Single Proprietor and Compensation Earner at new, although the seeded taxpayer type is explicitly `SingleProprietor` and old marks only Single Proprietor.
2. 1600WP additional-sheet taxpayer TIN is severe wrong output: `12345678900001-12345678900002-453-00000`, apparently concatenating schedule/payee TINs, instead of `000-123-453-00000`.
3. 1702Q Schedule 4 item 6a specify is less readable: old fit the full text in two lines in the row; new truncates it to one line and moves the full value to the additional sheet. The value is preserved, so this is not a value loss, but it is questionable/rule-quality regression.
4. 1702MX and 1702EX additional sheets still omit period/date identity even when their drafts contain period data. This is not proven as a new regression, but it means the complete header claim is not fully satisfied.

No semantic amount loss was identified in targeted review of the ten comparisons. Positional/alignment differences are widespread and intentional; they are not listed as faults unless content or box meaning changed.
