# Resumed-matrix addendum, exact commit 7d491c57

## Completed in this resumed pass

- 2550M 13A/13B hardware-Tab behavior, both devices: with Full Keyboard Access enabled, Tab blurred 13A but did not visibly focus or edit computed 13B. Typing `5` left 13A `100.00` and 13B `12.00`; saved/reopened stayed `100.0`/`12.0`. Earlier iPad run without Full Keyboard Access appended the `5` in 13A (`1005`), showing why FKA state matters.
- iPad case2 completed visually and by SQLite: tap then `7` produced `71,234.56` (insertion at the start); Delete restored `1,234.56`; saved/reopened `1234.56`.
- iPad case4home completed: `123` survived Home/5s/resume; `4` appended; field/reopen `1,234.00`, SQLite `1234.0`.
- Expanded comma matrix, both devices, now includes exact comma decimal, lone comma and digits-only control. iPhone lone comma sentence: `Taxable Amount: , is not an amount. The box kept 1,000.00.` iPhone valid `1500` saved/reopened `1500.0`. iPad exact sentence confirmed in existing clean artifact: `Taxable Amount: 1500,50 is not an amount. The box kept 1,000.00.`
- iPad case7 hardware-keyboard result: Tab/Shift+Tab did not move focus into the filled amount. Focus visibly landed on the row-sheet Close control; typed `15000.50` did not enter the amount, which stayed `1,234.56`.

## Important negative/incomplete results

- Exact case6 simultaneous row-delete race is not reachable in the current UI: while row2 is edited in its modal row sheet, the only visible `Delete row` control belongs to that open row; row1/background rows are dimmed and not independently tappable. Sequential valid row-delete automation remains incomplete, so no overwrite conclusion.
- Addition A reselect experiment was not run. The separate copy `/Users/devin/exp-7d491c57` exists, but no instrumentation build/test matrix was completed.
- Percent box/1601FQ was not reached; scratch databases contain only 2550M and 2551Q drafts.
- iPad valid row-delete, iPhone valid row-delete, hardware-comma sentence, and full Addition A remain open.

## Key artifacts

- iPad case2 digit: `hunt/ipad/case2/002-after-digit.jpg`
- iPad case2 delete: `hunt/ipad/case2/003-after-delete.jpg`
- iPad home/resume: `hunt/ipad/case4/home-resume/`
- iPad 2550M after Tab: `hunt/ipad/case4/2550m-final/005-after-tab.jpg`
- iPhone comma lone evidence: `hunt/iphone/case3/comma-lone/`
- iPhone valid 1500 evidence: `hunt/iphone/case3/comma-valid-1500/`
- iPad exact comma sentence: `hunt/ipad/case3/comma-decimal-clean/020-row-reopened-same-session.jpg`
- iPad hardware keyboard focus evidence: `hunt/ipad/case7-hardware/012-shift-after-1500050.jpg`
