# 2000OT recheck — continuation-page taxpayer-name header

What this proves: the same first-check 2000OT return was reprinted at `05b9c989` and compared with the already proven clean `3e8b1212` print.

Key files:
- `old.pdf`, `new.pdf`: same return at old/new commits.
- `crop-header-p2-old/new.png`: page-2 TIN/taxpayer-name continuation header.
- `crop-header-p3-old/new.png`: continuation Schedule 1.A header.
- `crop-header-zoom-old/new.png`: enlarged proof that the two-line name is now inside the box rather than struck/cramped by the border.
- `recheck-2000OT.mp4`: 15-second print-preview/PDF recording.
- page pictures, preview captures, text/bbox/font outputs.

Result: fault 5 is fixed. On both page 2 and the continuation Schedule 1.A page, the long taxpayer name prints in two clean lines inside the taxpayer-name box with the TIN. The `Others (Specify)` continuation entry disappears because the full specify text now fits on page 1; this is correct, not a lost value. No numeric-token loss was detected.

What this does not prove: extracted-token comparison is not a complete visual audit of every static label because layout spacing changed intentionally.
