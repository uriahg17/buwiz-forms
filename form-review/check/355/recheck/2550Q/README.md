# 2550Q recheck — Rule 6 specify + additional-sheet TIN branch

What this proves: the same first-check 2550Q return was reprinted at `05b9c989` and compared with the already proven clean `3e8b1212` print.

Key files:
- `old.pdf`, `new.pdf`: same return at old/new commits.
- `crop-item19-full-old.png`, `crop-item19-full-new.png`: item 19 specify before/after.
- `recheck-2550Q.mp4`: print-preview/PDF recording.
- `preview-old/new-p*.png` and `old/new-p*.png`: preview captures and rendered page images.
- extraction outputs (`*-text.txt`, `*-raw.txt`, bbox/fonts).

Result: item 19 is fixed in the claimed Rule-6 shape: the original inline box is followed by a full-width line containing the complete specify text, while the amount remains level with item 19. The additional-sheet TIN now includes branch code `000-123-453-00000` rather than `000-123-453`. No numeric-token loss was detected in a same-page token comparison; reduced additional-sheet text is expected because full specify text now fits on the form.

What this does not prove: page-image differences are large because the alignment/specify layout intentionally changed; they were adjudicated by extracted text and targeted crops, not every static pixel.
