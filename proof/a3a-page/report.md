# A3a account-open page proof report

Head: `4f66556faea083acd962c76ab3e0f670d7cafdb6`  
Driver: `gpui-agent-cli 0.5.0`

| run | result | steps | screenshots | recording |
|---|---:|---:|---:|---|
| macOS desktop relaunch light | passed | 4/4 | 2 | `proof/a3a-page/evidence/macos-relaunch/recording.mp4` |
| macOS desktop signin light | passed | 27/27 | 2 | `proof/a3a-page/evidence/macos-signin/recording.mp4` |
| iPhone 17 Pro simulator relaunch light | passed | 4/4 | 2 | `proof/a3a-page/evidence/iphone-relaunch/recording.mov` |
| iPhone 17 Pro simulator signin light | passed | 27/27 | 2 | `proof/a3a-page/evidence/iphone-signin/recording.mov` |

The recipes drive the real Shell with deterministic account-open host fakes: a relaunch with a stored sign-in reaches "Opening your account…" and then Home without the sign-in page; a sign-in reaches "Moving your returns…" and then Home. Input is gpui-agent recipe input only. The OTP textbox is found dynamically with `scroll_until` and used through its returned `.node` reference. `simctl recordVideo` only observes iOS runs; no simctl input, osascript, CGEvent, coordinates, or other OS-input fallback is used.

Safety: `BUWIZ_NO_KEYCHAIN=1`, `EBIR_TEST_ENV=1`, `BIR_AUTH_BYPASS=1`, `BIR_SFTP_DRY_RUN=1`; `BIR_SFTP_LIVE` was never set; scratch databases were deleted after each run.

## Final-head applicability

Final implementation head: `dc87e13ec840c42243900a0ca1875b91e77c191a`. No proof re-run was required: the recipes exercise the host-driven opening/moving screens, whose recipe-visible wording and outcome are unchanged at the final head. The review fixes concerned the permanent note, non-recipe blocked pages, sign-out errors, and the no-state fallback.
