# Form 1800 — Round 2 Part A Evidence (`WRONG ON PAPER ONLY`)

- `1800-flow.mp4`: App-window flow opening Form 1800, entering Schedule A personal property gift `1,250,000.00` (less `250,000.00` exemption = `1,000,000.00` net gifts subject to tax, 6% tax due = `60,000.00`), verifying Part II on screen, clicking Print preview, and showing Page 1 Part II with Item 14 (`Total Net Gifts Subject to Tax`) completely blank while Item 16 prints `60,000.00`.
  - **Does not show**: Live OS desktop outside the app window, or live BIR submission. Captured via `gpui-agent screenshot` frames + the exact `sheet.html` emitted by Print preview.
- `screen-crop.png`: 1400 px crop of the app form page showing Part II Item 14 = `1,000,000.00` and Item 16 = `60,000.00`.
- `print-crop.png`: 1400 px crop of printed Page 1 Part II showing Item 14 blank beside Item 15 `6.0%` and Item 16 `60,000.00`.
