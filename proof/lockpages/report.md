# Lock pages proof report

Head: `12a4edf83f44844acee63139d3c2fcac5ddff42d`  
Driver: `gpui-agent-cli 0.5.0`

| run | result | steps | screenshots | recording |
|---|---:|---:|---:|---|
| macOS light | passed | 25/25 | 7 | `proof/lockpages/evidence/macos-light/recording.mp4` |
| macOS dark | passed | 25/25 | 7 | `proof/lockpages/evidence/macos-dark/recording.mp4` |

Every recipe step passed. The run covers the empty lock page, masked account, wrong PIN, store wait, lost store, Set PIN, mismatch, successful set, and the final stub call sequence `calls: verify,set`. Each marked state has a PNG in the run's `shots/` folder.

The temporary proof entry mounts the real Shell with `view=lockdebug`; this is necessary because NSH does not expose `BIR_SHELL_START` to the shipping `App.tsx` without a capability declaration. The tested route, components, debug interface, themes, and input path are the exact PR-head code. Input is only gpui-agent recipe input.

iPhone and iPad simulator proof: not run on this Mac. Only 6 GB was free after cleaning session-created folders, while the orchestrator required about 25 GB for simulator builds. No gpui-agent capability gap was hit on the desktop proof.

Safety: `BUWIZ_NO_KEYCHAIN=1`, `EBIR_TEST_ENV=1`, `BIR_AUTH_BYPASS=1`, `BIR_SFTP_DRY_RUN=1`; `BIR_SFTP_LIVE` was never set; scratch databases were deleted after each run.
