driver: gpui-agent-cli 0.5.0

# Lock pages proof

Proof for hexuria/buwiz-forms#488 at `12a4edf83f44844acee63139d3c2fcac5ddff42d`.

- Recipe: `proof/lockpages/recipes/lockpages.wants`
- Runner: `proof/lockpages/run-one.sh`
- Machine report: `proof/lockpages/report.json`
- Human report: `proof/lockpages/report.md`
- Evidence: `proof/lockpages/evidence/`

The recipe drives the debug-only `lockdebug` route with gpui-agent input only on macOS desktop, iPhone 17 Pro simulator, and iPad Pro 13-inch simulator, each in light and dark. OTP inputs are found dynamically with `scroll_until` (zero scrolling) and then used through the returned `.node` reference; generated node names are not hard-coded. No simctl input, osascript, CGEvent, or coordinate fallback is used. `simctl recordVideo` only observes iOS runs.
