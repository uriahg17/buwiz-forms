# Recheck-2 item a: additional-sheet TIN

Runtime print verification at a067f980 using the isolated `/home/ubuntu/rchome2-new` build. Each return contains long values forcing an additional sheet. `1600WP` contains three payee rows with distinct decoy TINs `12345678900001..3`; the header must remain the filer TIN `000-123-453-00000`.

Files per form: saved PDF, extracted layout/raw text, pdftohtml XML, 120dpi page images, preview captures, data excerpt in `/tmp/r2-tin-final.log` copied here as `run.log`, and `crop-additional-header-r2.png`.

`before05b.pdf` and `crop-header-before05b.png` for 1600WP are reused recheck-1 evidence at 05b9c989, as instructed; they were not reprinted.

The recording `recheck2-tin.mp4` shows the final successful four-form runtime print batch. An earlier harness-only 1604E tuple mutation error was fixed before this final recording; it was not an application finding.
