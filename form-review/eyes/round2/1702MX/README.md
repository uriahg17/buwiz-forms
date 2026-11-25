# Form 1702MX — Round 2 Part A Evidence (`WRONG ON PAPER ONLY`)

- `1702MX-flow.mp4`: App-window flow opening Form 1702MX, choosing Item 13 Method of Deduction = Itemized, viewing Part II totals (`Item 14`, `Item 15`, `Item 16`, `Item 21`) on screen, clicking Print preview, and showing Page 1 Part II printing Items 14, 15, and 16 completely blank while Item 21 prints `-79,000`.
  - **Does not show**: Live OS desktop outside the app window, or live BIR submission. Captured via `gpui-agent screenshot` frames + the exact `sheet.html` emitted by Print preview.
- `screen-crop.png`: 1400 px crop of the app form page showing Part II Items 14–16 and Item 21 populated.
- `print-crop.png`: 1400 px crop of printed Page 1 Part II showing Items 14, 15, and 16 blank above Item 21 `-79,000`.
