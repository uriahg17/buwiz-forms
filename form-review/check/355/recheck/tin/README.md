# Additional-sheet TIN recheck — six forms

What this proves: six forms not printed in the first detailed check were filled with long/truncating text at `05b9c989`, printed through preview and saved PDF, and their additional-sheet headers were extracted and cropped.

Forms: `1801`, `1702MX`, `2200T`, `2552` (required), plus `1600PT` and `1702EX` (additional author-affected forms chosen because their sample payloads contain long specify/description fields that can force continuation entries).

Key files:
- `recheck-tin.mp4`: 79-second recording covering all six print-preview/PDF runs.
- `tin-header-results.tsv`: machine-extracted header verdicts.
- `crop-<FORM>-additional-header.png`: top of each additional sheet.
- `<FORM>/<FORM>-new.pdf`: saved PDF per form.
- `<FORM>/new-p-*.png`, `preview-new-p*.png`, raw/layout/bbox/font outputs.

Results: all six additional sheets show the TIN with branch code `000-123-453-00000` and a taxpayer name. Period/date evidence is present in form-appropriate labels on 1801 (`Date of Death`), 2200T (`Date`), 2552 (`Date of Transaction`), and 1600PT (`Return Period`). It is absent on 1702MX and 1702EX even though their drafts contain taxable-year/period data; those two are partial failures of the claimed complete header identity.

What this does not prove: these runs target the additional-sheet identity claim. They are not full box-by-box audits of the six forms.
