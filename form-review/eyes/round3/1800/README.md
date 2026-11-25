# Round 3 Evidence — BIR Form 1800

1800: Page 1 Item 14 Net Gifts blank on both main and rules; 135 Sched A/B overflow rows absent on main (2p), printed on rules (6p).

## What each file shows
- `main/compare.png`: 1400 px side-by-side of the live form page (left) and `origin/main` (`93820d0f`) printed PDF crop (right).
- `rules/compare.png`: Same-named 1400 px side-by-side for `origin/feat/store-launch-field-rules` (`8c3a7b53`).
- `1800-flow.mp4`: Under-2-minute sequence showing the live form page (`gpui-agent screenshot`) followed by the `origin/main` (`93820d0f`) and `origin/feat/store-launch-field-rules` (`8c3a7b53`) printed PDF comparisons.

## What these files do not show
- Live BIR transmission or Queue submission (run exclusively with `BUWIZ_NO_KEYCHAIN=1 EBIR_TEST_ENV=1 BIR_AUTH_BYPASS=1 BIR_SFTP_DRY_RUN=1` and demo taxpayer Juana Santos `000-123-453`).
- Real OS desktop chrome outside the app window (headless Linux/Xvfb uses `gpui-agent screenshot` frames plus the rendered `sheet.html`/PDF emitted by clicking Print preview).
