# Final consolidated report — iOS money box at 7d491c57

Free disk at final cleanup/report: see session report; this file was written before final build-folder deletion.

- App commit: `7d491c57dd073a86d933361088500ab03bc74837`
- NSH pin: `8c78cfd6d8ffcef260728ad2503d43c3bc9e86bf`; CLI `nsh 0.6.1 (8c78cfd)`
- Build folder used: `~/BuwizNsh/target-7d491c57`
- Devices: iPhone 17 Pro `405F45A9-B471-47B7-A5D9-E545EA624713`; iPad Pro 13-inch `41A2AFE3-9E35-4EE8-BEF0-21AA02B68BC3`
- Safety: dry-run/test environment only, no Queue press, invented scratch taxpayer/data only.
- Input: real simulator-window clicks on on-screen keypad keys; hardware cases used real key events.

Required summary: **every amount saved as typed: NO; any sentence wrong or missing: YES**.

Why NO: normal slow on-screen amount entry generally saved correctly, but early iPad input before/around keyboard presentation was lost in lifecycle tests and hardware-keyboard input about 125 ms after focus saved zero in all ten runs. Why YES: exact comma sentences were correct where capture succeeded, but the German hardware-comma sentence path remained automation-blocked, so sentence coverage is incomplete.

## Condensed result table

| case | device | typed/action | shown while typing | after leaving | saved | after reopening | result |
|---|---|---|---|---|---|---|---|
| 1 slow values | both | `0.50`, `1234.56`, `99999.99`, `100000`, `1000000.01`, `12345678.90`, `99999999.99` | correct per key | correctly grouped/rounded | correct | correct | PASS |
| 1 fast `15000.50` x10 | both | `15000.50` | correct final text every run | `15,000.50` | `15000.5` | correct | PASS; no misplaced point. iPhone mean spacing about 54 ms |
| 2 filled box | both | tap `1,234.56`, type `7`, Delete | `7` inserted at start: `71,234.56`; Delete restored `1,234.56` | `1,234.56` | `1234.56` | `1,234.56` / `1234.56` | PASS with documented caret behavior |
| 3 German `1500,50` | both | real comma keypad | `1500,50` visible | box returned to held amount with sentence | held `1000.0`, new value not saved | held amount | PASS. Exact sentence both devices: `Taxable Amount: 1500,50 is not an amount. The box kept 1,000.00.` |
| 3 lone comma | iPhone; iPad partial | `,` | `,` | held amount with sentence | held amount | held amount | PASS where completed. iPhone exact: `Taxable Amount: , is not an amount. The box kept 1,000.00.` |
| 3 German valid integer | both | `1500` | `1500` | `1,500.00` | `1500.0` | `1500.0` | PASS |
| 3 decimal keys | both | inspect/switch pad | German decimal pad offers comma, no dot | — | — | — | `1.234,56` impossible on software pad; no globe/layout exposed a dot |
| 4 tap zero then digit | both | zero box then immediate digit | completed cases correct when keyboard ready | correct | correct | correct | PASS in normal matrix; see lifecycle timing fault below |
| 4 2550M 13A→13B | both | `100`, hardware Tab, `5` | FKA on: Tab blurred 13A but did not focus/edit 13B; FKA off iPad: `5` stayed in 13A | FKA on `100`/`12`; FKA off `1005`/`120.6` | same | same | FAIL/blocked as a focus path; no valid Next control on decimal pad |
| 4 leave app focused | both | `123`, Home 5s, return, `4` | `123` survived; then `1234` | `1,234.00` | `1234.0` | correct | PASS |
| 5 Number of Sheet/s | iPhone | zero, type `42` | `4` showed `04`; `2` did not visibly append | — | `4` | `4` | FAIL product anomaly |
| 5 Number of Sheet/s | iPad | zero, type `42` | `42` | `42` | `42` | `42` | PASS |
| 5 1601FQ Tax Rate | both | zero percent, type `42` | `42` | `42.00` | `42.0` | `42.0` | PASS both devices |
| 6 empty amount | both | delete to empty and leave | empty while focused | `0.00`, no sentence | `0.0` | `0.00` | PASS |
| 6 row delete | both | rows `1000`/`3000`; row2 `7777`; delete row1 sequentially | row2 visible `7777`; row1 deletion did not overwrite row2 | see note | see note | row2 remained | Exact simultaneous race impossible in modal UI. Initial iPhone `777` mismatch was traced as harness Done/keypad-Delete artifact, not row deletion |
| 7 hardware Tab/Shift+Tab | iPad | filled amount, `15000.50` | Tab/Shift+Tab did not reach amount; focus landed on row-sheet Close | amount stayed `1,234.56` | unchanged | unchanged | FAIL/blocked hardware focus path |
| 7 hardware comma | iPad | German `1500,50` then Tab | hardware typing never entered field in automation | `0.00` | `0.0` | `0.00` | INCONCLUSIVE input-path blocker, not product sentence evidence |
| 8 visual/touch | both | inspect sentence box and keypad | sentence wraps/readable | — | — | — | iPhone row buttons 44pt; iPad centered row-sheet amount inner height about 28.6pt and buttons about 30pt, below 44pt. Decimal pad has no minus; full numeric keyboard does |

## Lifecycle results

Required line:

`(a) changed in 0 of 17 runs; (b) first digit lost at 100 / 200 / 400 ms: iPhone 0/10, 0/10, 0/10; iPad partial 6/7 clear, 1/1, 1/1 (filled box: typed digits visually appended, then blur/reopen kept 1,234.56); (c) where the 8 lands: left start, middle start, right end`

- (a) both devices completed 17/17 runs (10 Home, 5 app-switcher, 2 large amount); no filled amount changed before any key.
- (b) iPhone: 10/10 valid runs at each nominal timing, no first digit loss; measured gaps about 116–122, 213–223, 414–421 ms.
- (b) iPad partial fast-tap samples repeatedly saved `234.56` instead of `1234.56`; this motivated the keyboard-shown matrix below.
- (c) iPhone validated: left/middle insertion at start produced `81,234.56`; right end produced `1,234.568` while typing and reopen/save `1,234.57` after invalid-sheet close. iPad manually validated the same left/middle/right behavior; right end triggered the 12-character validation and rounded/reopened as `1,234.57`.

## Main-vs-PR bisect and keyboard-shown matrix

Main zero-box timing at exact main `642bfc78221c0a87b318c7c3378c3f5b0b2c9359`:

`main 642bfc78 iPad: lost 10/10 at 120, 10/10 at 200, 10/10 at 400 ms`

Keyboard fully shown matrix:

`main 642bfc78 iPad kb-shown: lost 10/10 at 0, 10/10 at +200, 10/10 at +400; hardware: lost 10/10`

`7d491c57 iPad kb-shown: lost 0/10 at 0, 0/10 at +200, 0/10 at +400; hardware: lost 10/10`

Interpretation: the zero-retention/malformed-input fault predates #403 on main. At 7d, software-keyboard input succeeds once the keyboard is fully shown, even when the first key is sent at detection +0. Hardware input about 125 ms after focus still fails on both builds.

## Row-delete trace conclusion

`reproduced at 7d491c57: yes; main: yes` for the visible `7777` → saved `777` harness mismatch, but the 7d MaskedField/session trace proves the mechanism in the harness was an extra Backspace-like edit before blur, not row deletion. The first cached Done tap very likely landed on the software keypad Delete key. Row1 deletion happened seconds later with `pending={}` and did not overwrite or move row2.

## Addition A: iPad reselect experiment

Unmodified trace established:

- recomputed 13B text is written before focus: `writeText caller=outside-effect value="12.00" ... focused=false`;
- with Full Keyboard Access ON, first hardware Tab never focuses 13B and `5` does not edit it;
- with Full Keyboard Access OFF, `5` remains in 13A (`100` → `1005`) rather than entering 13B;
- in a later computed-field focus, iOS did not select all; selection was already collapsed at end (`start=6 end=6` for `120.60`) in the same ms as focus.

Because neither FKA state produces the required first-Tab-into-13B prerequisite, the local `windows||ios` guard 5x4 matrix was not run. See `ipad-reselect/BLOCKER-SUMMARY.txt` and traces.

## Legacy sentence

The exact legacy sentence pattern `the box shows ..., but the draft stored ...` was not observed anywhere.

## Evidence map

- Lifecycle: `lifecycle/`
- First-digit trace: `lifecycle/trace/`
- Row-delete trace: `lifecycle/trace-rowdelete/`
- Main bisect: `main-bisect/`
- Keyboard-shown matrix: `ipad-keyboard-shown/`, `main-ipad-keyboard-shown/`
- Reselect blocker: `ipad-reselect/`
- Percent evidence: `hunt/percent/`
- Main matrix evidence: `hunt/`, `logs/`, `RESUME-ADDENDUM.md`
