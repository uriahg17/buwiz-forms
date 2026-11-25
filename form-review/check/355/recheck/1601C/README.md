# 1601C recheck — item 20 specify / Rule 6

What this proves: the same first-check 1601C return was reprinted at new commit `05b9c989` in the isolated fake-home build (`/home/ubuntu/rchome-new/BuwizNsh/target-nsh`, plus this worktree's own cargo `target/`). The old side is the already proven clean `3e8b1212` PDF from the first check.

Key files:
- `old.pdf`, `new.pdf`: same return at old/new commits.
- `crop-item20-old.png`, `crop-item20-new-fullwidth.png`: the original clipped inline text versus the fixed full-width Rule 6 line.
- `crop-spec30/60/120/250-new.png`: harder exact-length cases. 30 stays inline; 60/120 use one full-width line; 250 uses two clean full-width lines.
- `hard-metrics.json`, `metrics-new.json`, `metrics-old.json`: exact-text counts, page locations, and fontspec measurements.
- `preview-new-*.png`, `preview-new-spec*-p*.png`: live preview captures corresponding to the saved-PDF runs.
- `recheck-1601c.mp4`: 48-second recording of the harder-case preview/PDF run.
- `old/new-p-*.png`: rendered PDF pages at about 1400px high-quality raster scale.

Font measurement caveat: poppler `pdftohtml` reports integer fontspec units; the table uses the established 0.75 pt/unit conversion. The Rule 6 text measured fontspec 11 (~8.25 pt), above the 7.5 pt floor. The 30-char case never overflows and therefore remains at the original inline comb font (fontspec 9, ~6.75 pt), which is not shrink-engine output.

What this does not prove: it does not audit every specify box in every form; that is covered separately. Exact additional-sheet counts are zero for 60/120/250 because the complete value fit on the form and was never truncated.
