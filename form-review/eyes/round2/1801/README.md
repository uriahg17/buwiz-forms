# Form 1801 — Round 2 Part A Evidence (`WRONG ON PAPER ONLY`)

- `1801-flow.mp4`: App-window flow opening Form 1801, entering Schedule 1 real property `15,000,000.00` and Standard Deduction `5,000,000.00` (`Net Taxable Estate = 10,000,000.00`, 6% `Estate Tax Due = 600,000.00`), viewing Part II on screen, clicking Print preview, and showing Page 1 printing Item 5 TIN (first 9 digits), Item 16 (`NET TAXABLE ESTATE`), and Item 24 (`TOTAL AMOUNT PAYABLE`) blank while Item 18 prints `600,000.00`.
  - **Does not show**: Live OS desktop outside the app window, or live BIR submission. Captured via `gpui-agent screenshot` frames + the exact `sheet.html` emitted by Print preview.
- `screen-crop.png`: 1400 px crop of the app form page showing Part II Item 16 = `10,000,000.00` and Item 18 = `600,000.00`.
- `print-crop.png`: 1400 px crop of printed Page 1 showing Item 5 TIN digits 1–9 blank, Item 16 blank, Item 18 `600,000.00`, and Item 24 blank.
