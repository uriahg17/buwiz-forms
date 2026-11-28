# Lock pages proof report

Head: `12a4edf83f44844acee63139d3c2fcac5ddff42d`  
Driver: `gpui-agent-cli 0.5.0`

| run | result | steps | screenshots | recording |
|---|---:|---:|---:|---|
| macOS desktop light | passed | 25/25 | 7 | `proof/lockpages/evidence/macos-light/recording.mp4` |
| macOS desktop dark | passed | 25/25 | 7 | `proof/lockpages/evidence/macos-dark/recording.mp4` |
| iPhone 17 Pro simulator light | passed | 25/25 | 7 | `proof/lockpages/evidence/iphone-light/recording.mov` |
| iPhone 17 Pro simulator dark | passed | 25/25 | 7 | `proof/lockpages/evidence/iphone-dark/recording.mov` |
| iPad Pro 13-inch simulator light | passed | 25/25 | 7 | `proof/lockpages/evidence/ipad-light/recording.mov` |
| iPad Pro 13-inch simulator dark | passed | 25/25 | 7 | `proof/lockpages/evidence/ipad-dark/recording.mov` |

Every recipe step passed on macOS desktop, iPhone simulator, and iPad simulator, in light and dark. The run covers the empty lock page, masked account, wrong PIN, store wait, lost store, Set PIN, mismatch, successful set, and the final stub call sequence `calls: verify,set`. Each marked state has a PNG in the run's `shots/` folder.

The temporary proof entry mounts the real Shell with `view=lockdebug`; this is necessary because NSH does not expose `BIR_SHELL_START` to the shipping `App.tsx` without a capability declaration. The tested route, components, debug interface, themes, and input path are the exact PR-head code. iOS runs use the NSH development host through `just nsh-run-agent`, as ordered.

Input is only gpui-agent recipe input. OTP inputs are found dynamically with `scroll_until` (zero scrolling) and then used through returned `.node` references; generated node names are not hard-coded. No simctl input, osascript, CGEvent, or coordinate fallback is used. `simctl recordVideo` only observes iOS runs.

No gpui-agent capability gap was hit.

Safety: `BUWIZ_NO_KEYCHAIN=1`, `EBIR_TEST_ENV=1`, `BIR_AUTH_BYPASS=1`, `BIR_SFTP_DRY_RUN=1`; `BIR_SFTP_LIVE` was never set; scratch databases were deleted after each run.
