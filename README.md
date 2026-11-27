driver: gpui-agent-cli 0.5.0

# Lock pages proof

Proof for hexuria/buwiz-forms#488 at `12a4edf83f44844acee63139d3c2fcac5ddff42d`.

- Recipe: `proof/lockpages/recipes/lockpages.wants`
- Runner: `proof/lockpages/run-one.sh`
- Machine report: `proof/lockpages/report.json`
- Human report: `proof/lockpages/report.md`
- Desktop evidence: `proof/lockpages/evidence/macos-light/` and `proof/lockpages/evidence/macos-dark/`

The recipe drives the debug-only `lockdebug` route with gpui-agent input only. OTP inputs are found dynamically with `scroll_until` (zero scrolling) and then used through the returned `.node` reference; generated node names are not hard-coded. No simctl input, osascript, CGEvent, or coordinate fallback is used.

The iPhone and iPad simulator proof is not in this branch: the Mac had only 6 GB free after cleaning session-created folders, below the orchestrator's 25 GB simulator-build target. The desktop proof is complete in light and dark.
