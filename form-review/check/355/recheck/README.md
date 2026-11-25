# PR #355 print-rules recheck at 05b9c989

Independent runtime recheck comparing the author's fixed head `05b9c9893c47dfbf530c5b0135090c0b703d7d88` against the previously checked head `3e8b12125f08a37e832ba0477db51b8da2d0d1b7`.

Runtime provenance:
- New-side prints: worktree `/home/ubuntu/repos/buwiz-forms-355r-new`, fake HOME `/home/ubuntu/rchome-new`, build output `/home/ubuntu/rchome-new/BuwizNsh/target-nsh` (about 14 GB after cold build).
- Old-side prints: clean first-check PDFs produced at `3e8b1212` in the prior per-commit build folder `target-355head`, reused only where the seeded data excerpts match; no old-side reprint was needed.
- Container CLI verified inside the Ubuntu 24.04 container: `nsh 0.6.1 (8c78cfd)`.
- `/home/ubuntu/BuwizNsh/target-nsh` does not exist at final verification, so the real shared target was never written.

Per-area directories:
- `1601C/`: Rule-6 item 20 base and exact-length hard cases.
- `0605/`: base long-name repair and exact-length 60/100/137/200 identity hard cases.
- `1701/`, `2550Q/`, `2551Q/`, `2000OT/`: same-return fault rechecks.
- `tin/`: six additional-sheet TIN/header forms.
- `1600WP/`, `1702Q/`, `1702MX/`, `0619E/`: remaining first-check forms reprinted for nothing-moved comparison.
- `nothing-moved/`: consolidated ten-form extracted-text and picture comparison.

Font measurement caveat: poppler `pdftohtml` reports integer fontspec units; this proof uses the established approximate conversion of 0.75 pt per unit. Under that measurement, fontspec 10 is ~7.5 pt and fontspec 9 is ~6.75 pt.
