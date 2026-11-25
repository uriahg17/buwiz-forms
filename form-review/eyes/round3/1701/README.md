# Round 3 Evidence — BIR Form 1701

1701: 13 ten-digit/10-char boxes blank on main (fixed on rules); Spouse TIN branch 00001 prints 00000 on both.

## What each file shows
- `main/p1-compare.png`: 1400 px side-by-side of the live form page (left) and `origin/main` (`93820d0f`) printed PDF crop (right) for 1701 Page 1 Part II Items 23A-32 (10-char blank on main).
- `rules/p1-compare.png`: Same-named 1400 px side-by-side for `origin/feat/store-launch-field-rules` (`8c3a7b53`).
- `main/p2-compare.png`: 1400 px side-by-side of the live form page (left) and `origin/main` (`93820d0f`) printed PDF crop (right) for 1701 Page 2 Part IV Item 1 (branch prints 00000).
- `rules/p2-compare.png`: Same-named 1400 px side-by-side for `origin/feat/store-launch-field-rules` (`8c3a7b53`).
- `main/p2-sched3-compare.png`: 1400 px side-by-side of the live form page (left) and `origin/main` (`93820d0f`) printed PDF crop (right) for 1701 Page 2 Sched 3.A Items 8A/10A/12A/18A/23A/24A.
- `rules/p2-sched3-compare.png`: Same-named 1400 px side-by-side for `origin/feat/store-launch-field-rules` (`8c3a7b53`).
- `main/p4-compare.png`: 1400 px side-by-side of the live form page (left) and `origin/main` (`93820d0f`) printed PDF crop (right) for 1701 Page 4 Part VII Items 8A/10A.
- `rules/p4-compare.png`: Same-named 1400 px side-by-side for `origin/feat/store-launch-field-rules` (`8c3a7b53`).
- `1701-flow.mp4`: Under-2-minute sequence showing the live form page (`gpui-agent screenshot`) followed by the `origin/main` (`93820d0f`) and `origin/feat/store-launch-field-rules` (`8c3a7b53`) printed PDF comparisons.

## What these files do not show
- Live BIR transmission or Queue submission (run exclusively with `BUWIZ_NO_KEYCHAIN=1 EBIR_TEST_ENV=1 BIR_AUTH_BYPASS=1 BIR_SFTP_DRY_RUN=1` and demo taxpayer Juana Santos `000-123-453`).
- Real OS desktop chrome outside the app window (headless Linux/Xvfb uses `gpui-agent screenshot` frames plus the rendered `sheet.html`/PDF emitted by clicking Print preview).
