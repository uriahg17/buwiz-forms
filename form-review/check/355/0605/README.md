# 0605 clean verification

Build provenance: before.pdf/main results from CARGO_TARGET_DIR=$HOME/BuwizNsh/target-355main at 92b3e2013f7a60a86dda120dd93e5473cb4b0c16; after.pdf/head results and head-run.mp4 from CARGO_TARGET_DIR=$HOME/BuwizNsh/target-355head at 3e8b12125f08a37e832ba0477db51b8da2d0d1b7. PDFs were saved through the app's test-only savePath hook after opening the real print preview. Direct draft seeding was used rather than manual typing; data-excerpt.txt records saved values.

Files: before/after PDFs, before/after page PNGs at about 1400px wide, preview-before/after captures, bbox/pdffonts/pdfinfo/text outputs, crop-* close crops, head-run.mp4. Preview-vs-PDF was visually compared at head: page count and sampled values/placements match; the preview is a rendered-window capture, not a pixel-identical PDF export.

Overall verdict: tweak. See results.tsv. Tainted shared-target artifacts were superseded by these clean per-commit outputs.
