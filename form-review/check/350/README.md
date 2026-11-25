# Independent check of PR #350 — form-picker row selection

## Commits and harness

- **MAIN**: `00a2003351ea56e7f7b585e1485ba31adf24514c` (`origin/main`; verified with `git rev-parse HEAD` after checkout).
- **HEAD**: `b1db7157193e80066a635bfc7b9164b22c40a76d` (`fix/form-picker-row-select`; verified with `git rev-parse HEAD` after checkout).
- The application ran inside `buwiz-nsh-2404` through `~/BuwizNsh/nsh2404.sh`, under `dbus-run-session -- xvfb-run --server-num=99 -s '-screen 0 1920x1080x24'`.
- Each run used `BUWIZ_NO_KEYCHAIN=1 EBIR_TEST_ENV=1 BIR_AUTH_BYPASS=1 BIR_SFTP_DRY_RUN=1`; `BIR_SFTP_LIVE` and `BIR_DATABASE_PATH` were unset. Nothing named **Queue** was pressed. The only taxpayer was the demo taxpayer Juana Santos.
- The app was started with `nsh test ./check350-hold.test.tsx --target linux` (never `just run`). The untracked fixture files in the repo worktree are:
  - `nsh/Check350Demo.tsx` — real `Shell`, demo taxpayer, 2026 forms 1601C/2551Q, seeded January/February 1601C drafts;
  - `nsh/check350-hold.test.tsx` — holds that real window open;
  - `nsh/check350-checkrow-hold.test.tsx` — holds the branch's `ui/checkrow.fixture.tsx` open for the disabled-row check.
- Input was physical/window-plane input through `gpui-agent press --x --y` at coordinates read from the live semantic tree, except the keyboard probes, which used real `xdotool key` events. Screenshots are exact app-surface PNGs from `gpui-agent screenshot`.
- Videos were made with host `ffmpeg -f x11grab` against Xvfb `:99`, cropping the real window at `0,0`; they are not semantic replays.

## Primary result matrix

`checked` below is the state of 1601C after the first/second press. The initial state was checked, count `2 selected`. Desktop was unfiltered; tablet and phone used search text `1601C` so the same row was visible.

### MAIN `00a20033`

| width (actual) | row bounds | text | code | empty end | right chip | leading box |
|---|---:|---|---|---|---|---|
| desktop 1440×900 | 814×59 | checked→checked, count stayed 2; hit target not pressable | same | same | same | unchecked→checked, count 1→2 |
| tablet 834×1070 (requested 834×1112) | 750×58 | checked→checked; not pressable | same | same | same | unchecked→checked |
| phone 420×844 (requested 390×844; Linux minimum width) | 386×58 | checked→checked; not pressable | same | same | same | unchecked→checked |

### HEAD `b1db7157`

| width (actual) | row bounds | text | code | empty end | right chip | leading box |
|---|---:|---|---|---|---|---|
| desktop 1440×900 | 814×59 | unchecked→checked, count 1→2 | unchecked→checked, count 1→2 | unchecked→checked, count 1→2 | unchecked→checked, count 1→2 | unchecked→checked, count 1→2 |
| tablet 834×1070 | 750×58 | unchecked→checked, count 1→2 | same | same | same | same |
| phone 420×844 | 386×58 | unchecked→checked, count 1→2 | same | same | same | same |

Rows are therefore 58–59 pt high in production at both commits, above the claimed 52 pt minimum. The CheckRow fixture rows measured exactly 52 pt.

## File inventory

### Result data and drivers

- `results-main.json`, `results-head.json` — machine-readable matrix, gestures, save/cancel, search/filter/setup, accessibility and existing-dialog results. These are the authoritative precise values.
- `accessibility-main-row-before.json`, `accessibility-main-row-after.json` — MAIN semantic row: generic row plus a separate 16×16 checkbox child.
- `accessibility-head-row-before.json`, `accessibility-head-row-after.json` — HEAD semantic row: the row itself is the only checkbox, row-sized, named `File 1601C in 2026`, with checked state.
- `snapshot-{main,head}-{desktop,tablet,phone}-edit-start.json` — full semantic trees at each width in edit mode.
- `existing-dialog-{main,head}-snapshot.json` — full semantic trees with the draft-existing dialog open.
- `keyboard-{main,head}-physical.json` — physical xdotool Space/Return outcomes.
- `checkrow-fixture-results.json` — disabled-row and fixture toggle-count outcomes.
- `check350_driver.py` — repeatable systematic driver used for both commits.
- `video350_driver.py` — repeatable video-flow driver.
- `launch-check350.sh`, `launch-check350-checkrow.sh` — exact container/Xvfb launch wrappers.
- `video-head-{desktop,phone}-log.json` — action/count log for the two recordings.

### Recordings (both HEAD `b1db7157`)

- `picker-head-desktop.mp4` — 15.8 s, desktop width: open Edit forms, tap 1601C by its text off/on, tap 0619E on by text, watch the count, Save forms, leave to Templates, return to Forms.
- `picker-head-phone.mp4` — 16.3 s, phone width (actual logical 420×844): open Edit forms, use the search-results row for 1601C, tap it by text off/on, Save, leave/reopen.
- `video-head-desktop-frame.png`, `video-head-phone-frame.png` — representative frames proving what the videos captured; they are not substitutes for the videos.

### Picker screenshots, same scene names at both commits

- `picker-{main,head}-desktop-not-editing.png` — saved-forms rows outside editing.
- `picker-{main,head}-desktop.png` — edit mode, desktop, several rows.
- `picker-{main,head}-tablet.png` — edit mode, tablet width, filtered to 1601C.
- `picker-{main,head}-phone.png` — edit mode, phone width, filtered to 1601C.
- `rowtext-{main,head}-{desktop,tablet,phone}-click1.png` — after the first physical press on the title text. MAIN is unchanged; HEAD is toggled.
- `rowtext-{main,head}-{desktop,tablet,phone}-click2.png` — after the second press on the same text point.
- `saved-{main,head}-desktop.png` — immediately after Save forms.
- `templates-{main,head}-desktop.png` — after leaving to Templates.
- `reopened-{main,head}-desktop.png` — after returning to Forms.
- `cancelled-{main,head}-desktop.png` — after the Cancel test.
- `search-vat-{main,head}-desktop.png` — `vat` search results.
- `filter-quarterly-{main,head}-desktop.png` — search plus Quarterly frequency.
- `setup-{main,head}-desktop.png` — after applying the Non-VAT professional setup.

### Comparison composites and keyboard images

- `compare-rowtext-desktop-click1.png` — strongest side-by-side: MAIN text press leaves 1601C checked; HEAD text press unchecks it.
- `compare-rowtext-phone-click1.png` — same comparison at phone width.
- `compare-picker-desktop.png` — desktop edit scenes side by side.
- `compare-existing-dialog.png` — visually identical dialog layout at the two commits; the behavioral difference is hit-target size, visible in the JSON.
- `keyboard-focus-main-head.png` — side-by-side keyboard focus: MAIN focus ring is only around the 16×16 box; HEAD focus ring surrounds the whole row.
- `keyboard-{main,head}-focus-1601C.png` — full focus-ring screenshots after ten Tab presses.
- `keyboard-{main,head}-{space,Return}-{once,twice}.png` — screens after physical key presses.
- `keyboard-head-clean-strip.png` — HEAD Tab-order strip showing focus moving through rows.

### Open-existing and fixture images

- `existing-{main,head}-desktop.png` — draft-existing dialog before choosing.
- `existing-second-{main,head}-desktop.png` — after saving as February with fast lane on; no second dialog and the auto-load toast is visible.
- `checkrow-fixture-before.png`, `checkrow-fixture-after.png` — enabled Alpha/Beta rows and dimmed disabled Gamma row in the branch fixture.

## What the artifacts do **not** show

- They do not prove a true operating-system double-click. `xdotool` mouse clicks did not reach this Xvfb/GTK window at all in the fixture (even a single click produced no event), so a true double-click could not be delivered. Two back-to-back `gpui-agent press` injections were used in the production matrix; in the fixture, each individual press incremented the toggle counter exactly once.
- They do not prove touch scrolling on Android/iOS. On this Linux desktop, press-and-drag with the window-plane driver did not scroll at either commit; it also did not toggle the row.
- They do not prove disabled rows in the production taxpayer picker, because `FormsTab.tsx` never creates a disabled picker row. Disabled behavior was checked in the branch's own `checkrow.fixture.tsx` instead.
- They do not runtime-prove the desktop close dialog. The fixture mounts `Shell`, not the outer desktop close host; closing the fixture window closed it directly. The missed close-dialog label finding is source-verified, not runtime-verified.
