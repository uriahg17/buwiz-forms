# 0605 recheck — taxpayer name / identity overflow

What this proves: the same first-check 0605 return was reprinted at `05b9c989` and compared with the already proven clean `3e8b1212` print. The harder cases use exact-length 60/100/137/200-character values, each containing the continuous 40-character word, applied together to taxpayer name, registered address, and line of business.

Key files:
- `old.pdf`, `new.pdf`: same first-check return at old/new commits.
- `crop-name-address-old.png`, `crop-name-address-new.png`: the old three-line clipped name versus the fixed two-line base print.
- `crop-len60/100/137/200-identity-new.png`: harder-case page-1 identity rows.
- `crop-len100/137/200-additional-new.png`: additional-sheet headers and continuation entries.
- `hard-metrics.json`: exact whitespace-insensitive text counts and fontspec measurements.
- `recheck-0605.mp4`: 51-second recording covering the base and harder-case print-preview/PDF runs.
- `preview-new-*.png` and rendered `*-p-*.png`: preview captures and page pictures.

Important distinction: at lengths 100 and 137 the taxpayer name and address are NOT truncated; they fit in two clean page-1 lines. The additional sheet exists because line of business ellipsizes. At length 200 all three fields ellipsize and each appears exactly once as an entry in the continuation table; the taxpayer name also appears in the additional-sheet header as required.

Font measurement caveat: poppler `pdftohtml` reports integer fontspec units; this proof uses the established 0.75 pt/unit conversion. Under that measurement the harder truncated outputs are fontspec 9 (~6.75 pt), below the 7.5 pt floor even though continuation is correct. This is the remaining fault.

What this does not prove: the three harder fields were varied together, so the proof does not isolate whether one field's overflow changes another field's wrapping decision.
