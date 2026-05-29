# Model watch log

Running, dated memo from the **model-watch** agent (`/model-watch`). The agent reads the
deterministic `diagnostics.md`, root-causes regressions against git history, and appends one
dated section per run **below this header, newest first**. Read-mostly — it commits only this
memo to `main` and may open *draft* PRs for `signal_excluded_stations` edits, but never merges,
never touches `execution/`, and never trades. Findings land here for a human to act on.

See `docs/model-watch-agent.md` for how this is scheduled and how to run it by hand.

---

<!-- The agent appends dated sections (## YYYY-MM-DD) below this line, newest first. -->

## 2026-05-29

- **NEW critical `exclude_candidate` — KNYC (New York City)**: Model Brier 0.139 vs market 0.068 (gap +0.071), PnL −1.51 over n=2064. Paper trades confirm: NYC/high win rate 45.3%, weighted ROI −1.73% (n=106 settled). Signal is strong and consistent across metrics — not noise. → Draft PR #1 opened; human merged at 00:21 UTC. KNYC now in `DEFAULT_SIGNAL_EXCLUDED_STATIONS` (config.py:14). No GitHub issue opened — fix already applied before second invocation; flag will clear on next diagnostics regeneration. _(Correction from earlier log: "issue #1 filed" was wrong — that was the PR number; no GitHub issue was created.)_
- **WARN `regression_wow` — Chicago/high (+0.048) and Chicago/low (+0.051); NYC/high (+0.033)**: No forecast-model code changed in the 7-day window. Only commit landing in the window is `be4b664` (2026-05-28), which adds diagnostics tooling only — no changes to model, calibration, or bias logic. Attribution: likely a genuine hard weather week (late-May frontal variability over the Midwest/Northeast). Watch next week for reversion; escalate to investigation if Chicago regressions persist another 7d.
- **Chronic, no change**: KLAX `exclusion_holds` (gap +0.166), KMIA `exclusion_holds` (gap +0.176) — both correctly excluded; await Phase 3 calibration before re-evaluating.
- **INFO `nbm_beats_ecmwf` ×5 cells** (Chicago/high/0-6h, Chicago/low/24-72h, Denver/high/24-72h, Denver/high/6-24h, NYC/high/0-6h): NBM consistently beats ECMWF in these short-lead cells. Suitable input for Phase 3 ECMWF/NBM blend design — not a config change.
