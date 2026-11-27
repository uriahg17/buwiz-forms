# iOS money-box proof at 542e4844

Exact app commit: `542e484401494623a7ccbae9e25832985739a3a8`  
NSH pin verified: `8c78cfd6d8ffcef260728ad2503d43c3bc9e86bf`  
Devices: iPhone 17 Pro (`405F45A9-B471-47B7-A5D9-E545EA624713`), iPad Pro 13-inch (`41A2AFE3-9E35-4EE8-BEF0-21AA02B68BC3`)

Safety: all app launches used `SIMCTL_CHILD_BUWIZ_NO_KEYCHAIN=1`, `SIMCTL_CHILD_EBIR_TEST_ENV=1`, `SIMCTL_CHILD_BIR_AUTH_BYPASS=1`, `SIMCTL_CHILD_BIR_SFTP_DRY_RUN=1`. Queue was never pressed. Values are invented. Input under test was real Simulator input.

## Required result lines

```text
7777 at 542e4844: right in 10 of 10
B1 at 542e4844: real on iPhone yes, iPad yes
Sheets at 542e4844 iPhone: 42 in 0/10 tap-and-type, 10/10 kb-shown
(b) 542e4844: iPhone lost 0/0/0; iPad lost 10/10/10; iPad kb-shown 0/0/0
row sheet points: iPad amount 42, Delete 44, Done 44; iPhone amount 42, Delete 44, Done 44
blocked by the Simulator: hardware input does not reach the field
```

For `(b)`, each `N/N/N` is losses out of 10 at 120/200/400 ms. Expanded form: iPhone `0/10, 0/10, 0/10`; iPad tap-delay `10/10, 10/10, 10/10`; iPad keyboard-shown `0/10, 0/10, 0/10`.

## Result table

| item | iPhone | iPad | notes |
|---|---|---|---|
| B1(a), row2 focused delete | 3/3 reproduced | 3/3 reproduced | focused typed `500` survives in blank deleted row; other rows correct |
| B1(b), last-row focused delete | 3/3 reproduced | 3/3 reproduced | same focused-delete retention |
| B1(c), leave-first control | 1/1 correct | 1/1 correct | blank deleted row amount `0` |
| 7777 | 10/10 right | not requested | row2 `7777` survived Done, row1 delete and reopen |
| Sheets 0→42 | tap-and-type 0/10; kb-shown 10/10 | not requested | immediate tap-and-type runs ended as `2` |
| lifecycle(a), focus across Home/app switch | 20/20 unchanged | 20/20 unchanged | 10 Home/back +10 app-switch per device |
| lifecycle(b), first digit tap-delay | 0 lost in 30 | 30/30 incorrect/lost | see exact saved-value table below |
| lifecycle(b), iPad kb-shown | n/a | 0 lost in 30 | all saved `1234.56` |
| lifecycle(c), left tap then `8` | `81,234.56` saved | `81,234.56` saved | caret before leading `1` |
| lifecycle(c), middle tap then `8` | `81,234.56` saved | `81,234.56` saved | caret before leading `1` |
| lifecycle(c), right tap then `8` | `1,234.568` then saved/reopened `1,234.57` | `1,234.568`; validation blocked close and draft remained `1234.56` | device difference |
| zero placeholder | grey `0.00` → typed black `0` → grey `0.00` | same visually | iPad proof is screenshot-based because AX values were null with floating keypad |
| German pad `1500,50` then Done | pass, saved `1500.5`, reopened `1,500.50` | pass, saved `1500.5`, reopened `1,500.50` | comma accepted by ownership |
| hardware keyboard 13B | skipped | skipped | blocked by the Simulator: hardware input does not reach the field |

## B1 focused row-delete detail

Setup rows: `(PT010,1000,30)`, `(PT040,2000,60)`, `(PT010,3000,90)`.

At 542e4844 the old suspected overwrite of the following row did **not** occur. Former row3 stayed `3000`. The real fault was narrower: when Delete row was tapped while the amount box still had focus, the deleted row became blank-ATC but retained the still-focused typed `500`. Leaving the amount before Delete correctly made the blank deleted row amount `0`.

iPad required the stable docked full-width software keyboard. With the default floating keyboard, visually exposed Delete was not reliably hittable and taps could dismiss the keyboard instead; those taps were not counted.

Evidence: `b1-fast/iphone/`, `b1-ipad-docked/`; one video per device at `b1-fast/iphone/row2-r1/b1.mp4` and `b1-ipad-docked/row2-r1/b1.mp4`.

## 7777 detail

iPhone, 10/10 valid real-input runs: row2 PT040 cleared and typed `7777`; visible/hittable Done was tapped; row1 was deleted. Every delete+reopen result was row1 blank-ATC/`0`, row2 PT040/`7777`, row3 PT010/`3000`.

Evidence: `case7777/iphone/`, summary log `case7777-iphone.log`.

## Sheets detail

The box started at zero. Tap-and-type used a first key effectively immediately after the focus tap (about `0.02 ms` in the harness), before the software keypad key existed/hittable. Every such run lost the first `4` and ended as `2`: `0/10` correct. With the accessibility-detected keyboard-fully-shown wait, every run showed/saved/reopened `42`: `10/10` correct.

Important placeholder mismatch: the untouched initial display in this count box is a grey single `0`, not grey `0.00`, in screenshot and accessibility evidence.

Evidence: `sheets/iphone/summary.json`, `sheets/iphone/tap-01-before.jpg`, `sheets/iphone/shown-01-after-typing.jpg`, compressed `sheets/iphone/sheets-matrix.mp4`.

## Lifecycle (a)

Filled `1,234.56`, kept focused:

| device | Home/back unchanged before key | app-switch unchanged before key | saved/reopened correctly |
|---|---:|---:|---:|
| iPhone | 10/10 | 10/10 | 20/20 |
| iPad | 10/10 | 10/10 | 20/20 |

Evidence: `lifecycle/observations.jsonl`, `lifecycle/ipad/case-a/ipad-a.mp4` (compressed), screenshots in `lifecycle/*/case-a/`.

## Lifecycle (b) timing detail

| device/mode | nominal timing | measured first-key gaps | incorrect/lost | saved values |
|---|---:|---:|---:|---|
| iPhone tap-delay | 120 ms | about 115.5–118.8 ms | 0/10 | all `1234.56` |
| iPhone tap-delay | 200 ms | about 194.6–198.9 ms | 0/10 | all `1234.56` |
| iPhone tap-delay | 400 ms | about 396.1–397.5 ms | 0/10 | all `1234.56` |
| iPad tap-delay | 120 ms | about 113.7–119.2 ms | 10/10 | only `0.0` or `4.56` |
| iPad tap-delay | 200 ms | about 192.8–198.3 ms | 10/10 | only `4.56` or `34.56` |
| iPad tap-delay | 400 ms | about 396.2–398.0 ms | 10/10 | nine `34.56`, one `234.56` |
| iPad kb-shown | +0 | about 29–53 ms after stable detection | 0/10 | all `1234.56` |
| iPad kb-shown | +200 | about 233–246 ms | 0/10 | all `1234.56` |
| iPad kb-shown | +400 | about 431–438 ms | 0/10 | all `1234.56` |

iPad keyboard stabilization took about 1.36–2.18 s after focus. In six iPad 120 ms runs the early key-position taps happened while the floating keypad was not yet usable and the sheet was already closed before a fresh Done could be pressed; those runs still saved incorrect `0.0`. At 200/400 ms Done was fresh/hittable in 10/10 runs.

Evidence: `lifecycle-b-timing/`.

## Row-sheet point measurement

Accessibility frames are macOS Simulator-window coordinates. The iPad Simulator window is scaled down: its content width was 703 window points for a device logical width of 1032 points, ratio `1.467994`. The raw and converted heights are:

| device | amount raw | amount device pt | Delete raw | Delete device pt | Done raw | Done device pt |
|---|---:|---:|---:|---:|---:|---:|
| iPad | 28.600 | 41.985 | 29.962 | 43.984 | 29.962 | 43.984 |
| iPhone | 42 | 42.000 | 44 | 44.000 | 44 | 44.000 |

Thus the required device-point result is `row sheet points: iPad amount 42, Delete 44, Done 44; iPhone amount 42, Delete 44, Done 44`.

Annotated screenshots: `row-sheet-points/ipad/annotated-device-points.png`, `row-sheet-points/iphone/annotated-device-points.png`.

## Lifecycle (c) and placeholder detail

| device | left tap then `8` | middle tap then `8` | right tap then `8` |
|---|---|---|---|
| iPhone | caret before leading `1`; saved/reopened `81,234.56` | same | immediate `1,234.568`; rounded/saved/reopened `1,234.57` |
| iPad | caret before leading `1`; saved/reopened `81,234.56` | same | immediate/visible `1,234.568`; validation blocked sheet close/Done; saved draft remained `1234.56` |

Placeholder: both devices visually show grey `0.00` under the caret before the first key. Typing `0` replaces it with black typed `0`; deleting that typed zero restores grey `0.00`. iPhone accessibility confirms `0.00 → 0 → 0.00`; iPad accessibility values were null while the floating keypad was visible, so iPad proof is screenshot-based.

Evidence: `lifecycle/*/case-c/`, `lifecycle-c-placeholder/`.

## German-region software comma pad

| device | typed | after Done | saved | after reopen | result |
|---|---|---|---:|---|---|
| iPhone | `1500,50` | `1,500.50` | `1500.5` | `1,500.50` | pass |
| iPad | `1500,50` | `1,500.50` | `1500.5` | `1,500.50` | pass |

Evidence: `german-comma/`.

## Evidence limitations

- Later `xcrun simctl io ... recordVideo` attempts failed with `Resource busy` / `Host recording is already in progress`. Valid mp4 evidence exists for Sheets, iPad lifecycle(a), and the earlier B1 runs, but not every later timing/lifecycle(c)/German run. Those later items have screenshots and machine-readable JSON/JSONL.
- Stale harness-contaminated lifecycle(c) rows were not counted and are not included in this pushed proof copy.
- `sheets/iphone/sheets-matrix.mp4` and `lifecycle/ipad/case-a/ipad-a.mp4` are compressed copies of the original Simulator recordings.

Machine-readable aggregate: `final-542-results.json`. Harness scripts used for the proof are under `bin/`.
