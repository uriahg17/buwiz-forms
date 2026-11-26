# Addition A progress

- Separate experiment copy exists at `/Users/devin/exp-7d491c57`.
- Instrumentation was added to `nsh/ui/fields.tsx`; patch saved as `instrumentation.patch`.
- `/Users/devin/nsh` had to be a real copy of the pinned sibling NSH checkout, not a symlink. A symlink caused Cargo package collision between `/Users/devin/nsh/...` and `/Users/devin/moneybox-7d491c57/nsh/...`.
- Experiment `nsh run` was started for iPad after copying NSH; build was still in progress when this run ended. Log: `exp-run.log`.
- No unmodified ordering trace, no iOS-guard patch measurement, and no 5x4 scenario matrix completed yet.
