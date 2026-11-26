Free disk at report: 30 GB.

# iOS money-box proof at 7d491c57

- App commit: `7d491c57dd073a86d933361088500ab03bc74837`
- NSH pin: `8c78cfd6d8ffcef260728ad2503d43c3bc9e86bf`; CLI `nsh 0.6.1 (8c78cfd)`
- Build folder: `~/BuwizNsh/target-7d491c57`; proof path: `proof/ios-money-box-7d491c57/`
- Devices: iPhone 17 Pro `405F45A9-B471-47B7-A5D9-E545EA624713`; iPad Pro 13-inch `41A2AFE3-9E35-4EE8-BEF0-21AA02B68BC3`
- No Queue press; no tracked-file edits; no commit/push. Tested digit input used real mouse clicks into simulator keypad keys, except planned hardware-key tests (which did not complete).

Required summary sentence: **every amount saved as typed: NO; any sentence wrong or missing: YES**. The first NO is conservative because the full matrix was not finished; completed amount cases saved as typed. The YES is because exact sentence capture exists only for the iPhone comma case, not both devices/all required cases.

## Completed strong evidence

1. Case 1 slow values, both devices: `0.50`, `1234.56`, `99999.99`, `100000`, `1000000.01`, `12345678.90`, `99999999.99` all saved and reopened correctly.
2. Case 1 fast `15000.50`, ten runs per device: every run showed `15000.50` and saved `15000.5`; no misplaced decimal point. Mean spacing about 54 ms on iPhone; iPad timing is in observations.
3. iPhone case 3 German comma: real-tapped `1500,50` was visible as `1500,50`; it was not persisted. Exact captured sentence: `Taxable Amount: 1500,50 is not an amount. The box kept 1,000.00.` SQLite remained held amount `1000.0`.
4. iPhone case 2 filled `1,234.56`: tap then `7` produced `71,234.56`; Delete returned `1,234.56`; saved/reopened `1234.56` / `1,234.56`.
5. Sheet count case: iPhone exact zero precondition reproduced the anomaly (`4` showed `04`, `2` did not visibly append, saved `4`). iPad normal input `4`,`2` showed/saved/reopened `42`.
6. iPhone home/resume: `123` survived Home/5s/return, `4` appended to `1234`, saved/reopened correctly.
7. Case 8 partial: iPhone row buttons are 44 pt high and decimal pad has no minus. iPad centered row-sheet buttons/field measure about 30/28.6 pt high, below 44 pt; iPad full software numeric keyboard includes a minus key.

## Incomplete/invalid coverage

- Case 4 2550M scripts failed to locate item `13A` on both devices; computed-field behavior unproven.
- iPhone case6 script did not open the intended second row: digits appended into existing row one (`1,000.007777`), so the row-deletion/overwrite scenario is invalid. Empty-row deletion part did leave amount `0.0` in a blank row.
- iPad case2/case4home/case6 automation failed with `row not open`.
- German expanded matrix (`1500`, lone comma, `1.234,56`) incomplete; iPad exact comma sentence missing.
- Case7 iPad hardware Tab/Shift+Tab/selection replacement not tested.
- Addition A iPad reselect experiment not started.
- Addition B expanded comma-region matrix not completed.
- Percent box not reached.

## Key artifacts

- Machine observations: `hunt/observations.jsonl`
- iPhone case1 video: `hunt/iphone-case1.mp4`
- iPad fast ten-run video: `hunt/ipad/case1-fast-ten.mp4`
- iPhone comma sentence video: `hunt/iphone-case3-sentence.mp4`
- Exact sentence screenshot: `hunt/iphone/case3/comma-sentence/024-reopened-row-same-session.jpg`
- Per-key screenshots: `hunt/iphone/case1/`, `hunt/ipad/case1/`, `hunt/iphone/case2/`, `hunt/iphone/case5/`, `hunt/ipad/case5/`
