29 GB free
(a) changed in 0 of 17 runs; (b) first digit lost at 100 / 200 / 400 ms: iPhone 0/10, 0/10, 0/10; iPad partial 6/7 clear, 1/1, 1/1 (filled box: typed digits visually appended, then blur/reopen kept 1,234.56); (c) where the 8 lands: left start, middle start, right end

# Lifecycle proof at 7d491c57

This file is the urgent lifecycle report. Input used real mouse-generated taps on the onscreen keyboard; no Queue button was pressed.

## (a) Focus lifecycle

Both devices completed the full 17-run matrix: 10 Home/5-second/resume runs at 1,234.56, 5 app-switcher/other-app/back runs at 1,234.56, and 2 Home runs at 12,345,678.90. No run showed a changed amount before any key. SQLite after tapping another box, after leaving, and after close/reopen remained the original amount in every completed run.

| device | runs | changed before key | saved/reopened |
|---|---:|---:|---|
| iPhone 17 Pro | 17/17 | 0/17 | correct 17/17 |
| iPad Pro 13-inch | 17/17 | 0/17 | correct 17/17 |

Videos: `iphone/case-a/iphone-a.mp4`, `ipad/case-a/ipad-a.mp4`.

## (b) First digit after focus tap

iPhone completed 10 zero-box runs at each timing. Real measured gaps were about 116-122 ms for target 100 ms, 213-223 ms for target 200 ms, and 414-421 ms for target 400 ms. The first digit was never lost; every zero-box run saved 1234.56.

iPad evidence is partial because the floating decimal keyboard repeatedly occluded the form from accessibility and automation navigation eventually failed. After correcting the script so the second digit waited for keyboard settle, six clear 100-ms runs showed/saved `234.56` rather than `1234.56`; one additional run saved zero. Single sample runs at 200 ms and 400 ms also saved `234.56`. Thus the first digit was lost in every successful iPad sample, but the required 10-run counts are incomplete.

Filled-box single runs at all three timings on both devices visually appended the new digits to the existing amount (for example iPhone `1,234.561234.5`), but after leaving/reopen the draft remained `1234.56`.

Videos: `iphone/case-b/iphone-b.mp4`, `ipad/case-b/ipad-b.mp4`. Key visual: `ipad/case-b/001-zero-100ms-after-typing.jpg` visibly shows `234.56`.

## (c) Caret position then type a digit

iPhone:
- left tap + `8`: `81,234.56`, saved/reopened `81234.56` (digit landed at start)
- middle-of-field tap + `8`: `81,234.56`, saved/reopened `81234.56` (digit landed at start; note the amount text is right-aligned, so the middle of the field is still before the visible text)
- right tap + `8`: `1,234.568` while typing; leaving initially read `1234.56`, but after close/reopen it became/displayed `1,234.57` and SQLite `1234.57`

iPad automation used the floating keypad. The intended key was `8`, but the saved digit was `9` in the left/middle runs, so treat exact key identity cautiously:
- left and middle taps inserted at the start: saved/reopened `91234.56`
- right tap displayed `1,234.568` after reopen while SQLite reads were inconsistent (`1234.56` after leaving/reopen in the automated read)

Videos: `iphone/case-c/iphone-c.mp4`, `ipad/case-c/ipad-c.mp4`.

## Gaps and cautions

- iPad (b) is partial, not 10 runs per timing.
- iPad floating decimal pad occludes the form from Simulator accessibility, so several iPad `shown` fields are null; screenshots/video and SQLite are the evidence.
- An early iPhone app-switcher false positive was caused by clicking the wrong switcher card, not by an amount change. It was excluded and the full corrected 17-run pass was rerun.
- Full case-close/reopen display capture was reduced to SQLite reads in the optimized (a)/(b) pass; the videos show the transitions.
