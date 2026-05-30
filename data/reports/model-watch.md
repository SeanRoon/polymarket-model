# Model watch log

Running, dated memo from the **model-watch** agent (`/model-watch`). The agent reads the
deterministic `diagnostics.md`, root-causes regressions against git history, and appends one
dated section per run **below this header, newest first**. Read-mostly — it commits only this
memo to `main` and may open *draft* PRs for `signal_excluded_stations` edits, but never merges,
never touches `execution/`, and never trades. Findings land here for a human to act on.

See `docs/model-watch-agent.md` for how this is scheduled and how to run it by hand.

---

<!-- The agent appends dated sections (## YYYY-MM-DD) below this line, newest first. -->

## 2026-05-30

_Diagnostics source: `data/reports/diagnostics.md` generated 2026-05-29 16:42 UTC (`ba03155`). Today's resolve.yml (13:00 UTC) has not yet committed; no new resolutions or code changes since this file landed. This is the first analysis of the canonical 16:42 UTC output — the 2026-05-29 memo used an earlier pre-resolve diagnostics run and showed different numbers (Chicago +0.048/+0.051, ×5 nbm_beats_ecmwf)._

- **WARN `regression_wow` — Chicago/high (+0.073) and Chicago/low (+0.063)**: Numbers are worse than the prior memo's (+0.048/+0.051 — those came from pre-16:42 diagnostics). No model code in the 7-day window; only `559e4ed` (KNYC exclusion, config-only) and `be4b664` (diagnostics tooling). Attribution unchanged: late-May frontal variability, genuine forecast miss, not a code regression. Chicago/high cumulative PnL is −3.75 across all lead buckets; paper trades −3.28% ROI (n=115). Still below the exclude threshold (KLAX/KMIA-level gap), but if Chicago/high remains warn next week, flag as exclude_candidate for human review.
- **First `exclusion_holds` for KNYC (gap +0.065)**: Expected post-exclusion appearance (PR #1 merged 2026-05-29). Brier gap +0.065 is the smallest of the three excluded stations (vs KLAX +0.159, KMIA +0.167). Phase 3 priority note: re-evaluate KNYC first when isotonic calibration lands — it has the best chance of becoming viable.
- **`nbm_beats_ecmwf` reduced to ×2 cells** (Chicago/high/0-6h gap 0.040; NYC/high/0-6h gap 0.053): Denver/high and Chicago/low/24-72h cells dropped from the flag as the rolling window shifted — a positive signal. Two persistent cells remain; note for Phase 3 ECMWF/NBM blend design. NYC/high tracking is still useful for calibration even while KNYC is excluded from live signals.
- **Chronic, no change**: KLAX `exclusion_holds` (gap +0.159), KMIA `exclusion_holds` (gap +0.167) — correctly excluded; await Phase 3.
- **No critical flags → no GitHub issues; no exclude_candidate/reenable_candidate → no draft PR.**

## 2026-05-29

- **NEW critical `exclude_candidate` — KNYC (New York City)**: Model Brier 0.139 vs market 0.068 (gap +0.071), PnL −1.51 over n=2064. Paper trades confirm: NYC/high win rate 45.3%, weighted ROI −1.73% (n=106 settled). Signal is strong and consistent across metrics — not noise. → Draft PR #1 opened; human merged at 00:21 UTC. KNYC now in `DEFAULT_SIGNAL_EXCLUDED_STATIONS` (config.py:14). No GitHub issue opened — fix already applied before second invocation; flag will clear on next diagnostics regeneration. _(Correction from earlier log: "issue #1 filed" was wrong — that was the PR number; no GitHub issue was created.)_
- **WARN `regression_wow` — Chicago/high (+0.048) and Chicago/low (+0.051); NYC/high (+0.033)**: No forecast-model code changed in the 7-day window. Only commit landing in the window is `be4b664` (2026-05-28), which adds diagnostics tooling only — no changes to model, calibration, or bias logic. Attribution: likely a genuine hard weather week (late-May frontal variability over the Midwest/Northeast). Watch next week for reversion; escalate to investigation if Chicago regressions persist another 7d.
- **Chronic, no change**: KLAX `exclusion_holds` (gap +0.166), KMIA `exclusion_holds` (gap +0.176) — both correctly excluded; await Phase 3 calibration before re-evaluating.
- **INFO `nbm_beats_ecmwf` ×5 cells** (Chicago/high/0-6h, Chicago/low/24-72h, Denver/high/24-72h, Denver/high/6-24h, NYC/high/0-6h): NBM consistently beats ECMWF in these short-lead cells. Suitable input for Phase 3 ECMWF/NBM blend design — not a config change.
