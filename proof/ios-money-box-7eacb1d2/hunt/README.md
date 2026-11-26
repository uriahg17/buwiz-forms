# iOS money-box fault hunt

Commit under test: `7eacb1d2195b8dc1e1a1b65ad97728c15b50bc2f`  
`nsh --version`: `nsh 0.6.1 (8c78cfd)`  
`../nsh` commit: `8c78cfd6d8ffcef260728ad2503d43c3bc9e86bf`  
`cargo --version`: `cargo 1.99.0 (5f94df478 2026-08-27)`  
Build folder: `~/BuwizNsh/target-7eacb1d2`

Devices: iPhone 17 Pro and iPad Pro 13-inch (M5), iOS 26.5 Simulator. Input was real mouse taps in Simulator windows for on-screen keypad keys and real hardware key events where a row says hardware. No Queue button was pressed. Saved values were read from the scratch/test SQLite database and again after reopening the return. Per-key screenshots are in each case folder. `observations.jsonl` is the machine-readable log; it also contains superseded noisy H3 keypad-discovery entries, whose final authoritative entry is `h3-keypad-floating-decimal-pad`.

`iphone-h1-h2.mov` is the continuous iPhone H1/H2 recording. Its extracted frame assignment is unreliable and those redundant frame folders were removed; use the video plus the named key screenshots as evidence.

## Result rows

| case/device | typed | shown after each key | shown after leaving | saved | saved after reopening |
|---|---|---|---|---|---|
| H1 iPhone | `15000.50`, mean tap interval 185.96 ms (min 180.87) | per-key capture unreliable: screenshots lagged behind the burst; final typing screenshot and video show `15000.50`; no leading `0.00` in final state | row `15,000.50`; tax `450.02` | `15000.5` | `15,000.50`; `15000.5` |
| H1 iPad | `15000.50`, slow because per-key capture (~2 s/key) | `1`→`15`→`150`→`1500`→`15000`→`15000.`→`15000.5`→`15000.50` | row `15,000.50`; tax `450.02` | `15000.5` | `15,000.50`; `15000.5` |
| H2 iPhone | `15000..50`, mean tap interval 182.42 ms (min 175.81) | per-key capture unreliable: screenshots lagged; final/video show `15000.50`; no evidence digits were lost | row `15,000.50`; tax `450.02` | `15000.5` | `15,000.50`; `15000.5` |
| H2 iPad | `15000..50`, slow because per-key capture | `15000`→first `.` `15000.`→second `.` stayed `15000.`→`5` `15000.5`→`0` `15000.50` | row `15,000.50`; tax `450.02` | `15000.5` | `15,000.50`; `15000.5` |
| H3 iPhone (German region) | `1500,50`; then lone `,`; dot+comma case impossible | decimal pad offered `,`, no `.`: `1`→`15`→`150`→`1500`→`1500,`→`1500,5`→`1500,50`; lone comma showed `,` | `1500,50` left as `150,050.00`; lone comma left as `0.00` | `150050.0`; lone comma `0.0` | `150,050.00` / `150050.0`; lone comma `0.00` / `0.0` |
| H3 iPad (German region) | `1500,50`; then lone `,`; dot+comma case impossible | floating decimal pad offered `,`, no `.`; pad occluded AX, so per-key evidence is screenshots only; final typed text `1500,50` | `150,050.00`; lone comma `0.00` | `150050.0`; lone comma `0.0` | `150,050.00` / `150050.0`; lone comma `0.00` / `0.0` |
| H4 iPhone | 2550M item 13A `100` using hardware digits; hardware Tab into computed 13B; typed `5` | base `1`→`10`→`100`, computed `0.12`→`1.20`→`12.00`; Tab focused `12.00`; `5` showed `12.005` (appended, not replaced) | `12.01` | 13A `100.0`, 13B `12.01` | base `100.00`, computed `12.01`; same saved values |
| H4 iPad | same as iPhone | base `1`→`10`→`100`, computed `0.12`→`1.20`→`12.00`; Tab focused `12.00`; `5` showed `12.005` (appended) | `12.01` | 13A `100.0`, 13B `12.01` | base `100.00`, computed `12.01`; same saved values |
| H5 iPhone | `123`, Home 5 s, return, `4` | `1`→`12`→`123`; after resume still `123`; `4`→`1234` | row `1,234.00`; tax `37.02` | `1234.0` | `1,234.00`; `1234.0` |
| H5 iPad | `123`, Home 5 s, return, `4` | same sequence; after resume still `123`; `4`→`1234` | row `1,234.00`; tax `37.02` | `1234.0` | `1,234.00`; `1234.0` |
| H6 iPhone | `42` in 2551Q Return details item 5 `Number of Sheet/s`, holding `0` | `4` showed `04`; `2` still showed `04` (reproduced once) | not separately shown | `4` | `4` |
| H6 iPad | `42` in same box; exact zero precondition not preserved because copied draft already held `4`, so it was cleared first | `4`→`4`; `2`→`42` | `42` | `42` | `42`; `42` |
| H7 iPhone | looked for minus on decimal pad | no minus key on software decimal pad | n/a | no negative can be typed through pad | n/a |
| H7 iPad | hardware numpad `-`/`5`, then main hardware `-`/`5`; software pad checked | numpad minus/5 entered nothing; main `-` showed `-`; following `5` left `-`; software decimal pad has no minus | empty/`0.00` | `0.0`; no negative persisted | `0.00`; `0.0` |

## Findings

1. H3 is a reproducible fault on both devices: a comma decimal separator is accepted visually (`1500,50`) but saved as `150050.0`, reopening as `150,050.00`. The review prediction was correct.
2. H4 appends into a computed amount on both devices: computed `12.00` plus typed `5` became `12.005`, then settled/saved as `12.01`; it was not replaced.
3. H6 iPhone is a reproduced anomaly: a count box holding `0` showed `04` after `4`, did not visibly append `2`, and saved `4`.
4. H7: no negative can be typed from either software decimal pad. On iPad hardware main minus can transiently show `-`, but no negative persists.
5. H1/H2 slow-entry behavior is correct on iPad and persisted correctly on both devices, but the requested sub-150 ms burst behavior remains unproven: iPhone averaged about 182-186 ms and iPad capture forced seconds per key.
6. The exact message “the box shows ..., but the draft stored ...” was not observed in any completed case. H3 nevertheless has that semantic mismatch without the message.

## Caveats

- H4 used hardware digits and hardware Tab because the decimal pad exposes no Next/Done action.
- H4 evidence includes unrelated `zero_rated_sales=1.00` in item 14 from an initial misclick. It does not affect tested 13A/13B.
- iPad H3 floating decimal pad occludes the form from Simulator accessibility; its per-key evidence is screenshots rather than AX values.
- H1/H2 iPhone named key screenshots lagged the burst; the continuous video is retained, but frame-to-key assignment is unreliable. Thus those screenshots are evidence of the run, not reliable per-key transcription.
- Region was reset after H3.
