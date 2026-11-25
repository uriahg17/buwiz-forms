# 1701 recheck — additional-sheet TIN

What this proves: the same first-check 1701 return was reprinted at `05b9c989` and compared with the already proven clean `3e8b1212` print.

Key files:
- `old.pdf`, `new.pdf`: same return at old/new commits.
- `crop-additional-tin-old.png`, `crop-additional-tin-new.png`: additional-sheet header before/after.
- `crop-taxpayer-type-old.png`, `crop-taxpayer-type-new.png`: a newly observed checkbox regression.
- `recheck-1701.mp4`: 18-second print-preview/PDF recording.
- `preview-old/new-p*.png` and `old/new-p*.png`: preview captures and rendered page images.
- `old/new-text.txt`, `old/new-raw.txt`, bbox/font outputs: extraction evidence.

Result: the claimed additional-sheet TIN fix is present (`000-123-453-00000` replaces `TIN: —`). However the new print incorrectly marks both `Single Proprietor` and `Compensation Earner` in Part I item 6 even though the seeded return sets taxpayer type to `SingleProprietor`; the old print marks only Single Proprietor. This is a wrong-box/value regression beyond the five claimed fault fixes.

What this does not prove: the large page-4 picture difference was not box-by-box fully adjudicated; extracted text shows it is chiefly spacing/alignment and the intended specify placement, with no filled value disappearance identified.
