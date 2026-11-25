# Form 2200T — Round 2 Part A Evidence (`WRONG ON PAPER ONLY`)

- `2200T-flow.mp4`: App-window flow showing the open 2200T v2020 return with Schedule 1 rows summing to `60,413.47` (including `txtSched1_5_2020` `250.00` under `Effective January 1, 2020`), clicking Print preview, and Page 2 of the printed August 2022 sheet omitting the 2020/2021 rows while `TOTAL TAX DUE` on Page 3 still includes them (`60,413.47` vs `60,163.47` visible).
  - **Does not show**: Live OS desktop outside the app window, or live BIR submission. Captured via `gpui-agent screenshot` frames + the exact `sheet.html` emitted by Print preview.
- `screen-crop.png`: 1400 px crop of the app form page showing Part III Item 16 Excise Tax Due = `60,413.47`.
- `print-crop.png`: 1400 px crop of printed Page 2 Schedule 1 showing `XT160` Heated Tobacco Products with only 2022/2023/2024 rows (no 2020 row for the `250.00` tax due).
