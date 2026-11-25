# All-43 sample-print comparison

Method: one repository sample-payload draft per form, printed through the real Linux print pipeline. Main PDFs are `main/*-main.pdf` from commit 92b3e201 using `target-355main`; head PDFs are `head/*-head.pdf` from commit 3e8b1212 using `target-355head`. `comparison.tsv` and `comparison.json` compare extracted `pdftotext` output.

Important interpretation: this is a text-content comparison, not a visual diff. Many differences are intentional claim behavior: comma formatting, whole-peso removal of `.00`, blank unused amount boxes, wrapped/clipped long text, continuation or additional-sheet pages. Extracted text also concatenates adjacent cells differently when layout changes, so counter samples in `comparison.json` must be read with the PDFs.

Summary:
- 43/43 forms printed at both commits; none was impossible to tool-fill because repository sample payloads exist for all 43.
- 42/43 raw extracted texts differ; only 1702EX is byte-identical after `pdftotext` extraction.
- Token sequence differs in 39 forms. Token sequence does not differ in 0619E, 1700, 1701A, 1702EX.
- Page count differs in 23 forms: 1600PT, 1600VT, 1600WP, 1601C, 1601EQ, 1601FQ, 1606, 1701, 1701MS, 1702Q, 1706, 1707, 1800, 2000, 2000OT, 2200A, 2200AN, 2200C, 2200M, 2200P, 2200S, 2200T, 2550M.
- The page-count differences are consistent with the continuation/additional-sheet claims. No all-43 form failed to produce a PDF.
- No clear evidence of a filled value completely disappearing at head was found in the automated comparison. The visible differences are mostly claimed formatting/continuation behavior plus extraction concatenation. This does not prove visual correctness; seven forms were checked in detail separately.
