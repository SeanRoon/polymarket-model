# Model watch log

Running, dated memo from the **model-watch** agent (`/model-watch`). The agent reads the
deterministic `diagnostics.md`, root-causes regressions against git history, and appends one
dated section per run **below this header, newest first**. Read-mostly — it commits only this
memo to `main` and may open *draft* PRs for `signal_excluded_stations` edits, but never merges,
never touches `execution/`, and never trades. Findings land here for a human to act on.

See `docs/model-watch-agent.md` for how this is scheduled and how to run it by hand.

---

<!-- The agent appends dated sections (## YYYY-MM-DD) below this line, newest first. -->

## 2026-06-03

_Diagnostics source: `data/reports/diagnostics.md` generated 2026-06-02 17:24 UTC (`61963b6`). 8-day git log: only `Snapshot:`, `Resolutions + biases`, and `model-watch` commits — no model or config code changes._

- **WARN `regression_wow` — Chicago/high (+0.034)**: DOWN from +0.050 (06-02), now below the escalation threshold. Rolling 7d Brier 0.165 → 0.200. Watch condition progressing: today is run 1 of 2 required consecutive sub-+0.050 readings to close the watch (per 06-01 memo). Close watch if Chicago/high stays below +0.050 at next run (~06-05).
- **WARN `regression_wow` — Chicago/low (+0.025)**: DOWN from +0.036 (06-02). Healthy improvement; frontal variability rolling off the 7d window.
- **NEW WARN `regression_wow` — Los Angeles/high (+0.048)**: First appearance for KLAX. Brier worsened 0.190 → 0.238. **No impact on live signals** — KLAX is excluded. Consistent with the pre-existing `exclusion_holds` gap +0.173 (n=2766). No action; does not change the exclusion recommendation.
- **`nbm_beats_ecmwf` — Chicago/high (all 3 buckets)**: Essentially stable — 0-6h 0.051 (±0.001 vs 06-02), 6-24h 0.027, 24-72h 0.033. Persistent; Phase 3 ECMWF/NBM blend recommendation unchanged.
- **`nbm_beats_ecmwf` — NYC/high/0-6h (gap 0.029)**: Narrowed from 0.034 (06-02) — continuing downward. NYC/high/24-72h (gap 0.027, n=108) is NEW this cycle. Both are Phase 3 calibration context for KNYC re-evaluation; KNYC remains correctly excluded.
- **Chronic, no change**: KLAX `exclusion_holds` +0.173 (was +0.171), KMIA +0.158 (stable), KNYC +0.072 (was +0.071) — all within noise. Exclusion list correct; await Phase 3.
- **Paper trades (906 settled, +33 since 06-02)**: Win rate 62.0% (stable), weighted ROI 3.57% (up from 3.34%). Austin/high 19.6% ROI (n=121), Denver/high 15.8% ROI (n=133) driving gains. Chicago/high −2.7% ROI (n=139, 55.4% win rate) — marginal change from 06-02. Excluded-station shadow trades: KLAX −2.0%, KMIA −7.8%, KNYC −3.2% — all negative, validating exclusions.
- **No critical flags → no GitHub issues. No exclude_candidate or reenable_candidate → no draft PR.** Watch: Chicago/high (+0.034) and Chicago/low (+0.025) both below +0.050 today (run 1 of 2 to close). Close watch at ~06-05 if both remain below threshold.

## 2026-06-02

_Diagnostics source: `data/reports/diagnostics.md` generated 2026-06-01 18:39 UTC (`999015c`). 8-day git log: only `Snapshot:` and `Resolutions + biases` commits — no model or config code changes._

- **WARN `regression_wow` — Chicago/high (+0.050): escalation threshold met, but station exclusion is too blunt.** The ≥+0.050 trigger set in the 06-01 memo is hit exactly (rolling 7d Brier 0.158 → 0.208). This is now the 5th+ consecutive diagnostic cycle with a Chicago/high regression flag. Aggregate model-vs-market Brier gap for Chicago/high is ~+0.075 across all lead buckets (weighted by n: 1236/1062/300), slightly exceeding KNYC's +0.071 gap at time of exclusion on 2026-05-29. Paper trades: 55.6% win rate, −2.42% ROI (n=133). **However**, excluding KMDW at the station level would also remove Chicago/low signals, which are profitable (69.75% win rate, +1.84% ROI, n=119). Combined KMDW paper ROI is marginal −0.3%, and historically Chicago/low adds ~+9.0 cumulative evaluation PnL vs Chicago/high's −5.0 — net positive. Station exclusion is the wrong lever here. **No draft PR** (leash: only mechanical exclusion-list edits qualify; cell-level exclusion requires new config infrastructure). → Phase 3 engineering task: add `signal_excluded_cells: frozenset[tuple[str,str]]` (station, kind) to `config.py`. If Chicago/high regression holds ≥+0.050 for two more consecutive runs (~06-04, ~06-06), escalate priority.
- **`nbm_beats_ecmwf` now spans all 3 lead buckets for Chicago/high** — 0-6h gap 0.050 (up from 0.046), 6-24h gap 0.022 (new), 24-72h gap 0.023 (new). Prior cycle had only 0-6h flagged; this is the first time all three buckets appear simultaneously for any single city/kind. Combined with regression_wow, this confirms ECMWF is the wrong primary source for Chicago/high across all lead horizons. → Strengthens the Phase 3 case for an ECMWF/NBM blend weighted heavily toward NBM on this cell. NYC/high/0-6h gap 0.034 — persistent but narrowing; deprioritize unless it rewidens.
- **WARN `regression_wow` — Chicago/low (+0.036)**: Below escalation threshold. Paper trades healthy (69.75% win rate, +1.84% ROI). No action; likely residual frontal variability still in the 7d rolling window.
- **Paper trades (873 settled, +32 since 06-01)**: Win rate 61.7% (stable), weighted ROI 3.34% (vs 3.40% on 06-01 — slight dip as more Chicago/high trades settle). Austin/high (19.2% ROI, n=116) and Denver/high (15.6% ROI, n=128) drive gains. Miami/high worst at −7.81% (n=116), consistent with KMIA exclusion. Excluded-station paper trades (KLAX −1.74%, KMIA −7.81%, KNYC −2.61%) all negative, validating those exclusions.
- **Chronic, no change**: KLAX `exclusion_holds` gap +0.171 (n=2676), KMIA +0.158 (n=2220), KNYC +0.071 (n=2562) — stable within ±0.002 of prior run. KNYC remains smallest gap and first Phase 3 re-evaluation candidate.
- **No critical flags → no GitHub issues. No mechanical exclusion-list change applicable → no draft PR.** Phase 3 action items: (1) add per-(station,kind) exclusion config support, (2) NBM/ECMWF blend weighted toward NBM for Chicago/high across all lead buckets.

## 2026-06-01

_Diagnostics source: `data/reports/diagnostics.md` generated 2026-05-31 14:46 UTC (`676a664`). No code changes in 8-day window — only automated snapshot and resolve commits._

- **WARN `regression_wow` — Chicago/high (+0.034)**: Improved from +0.074 (05-31 memo). Now **below** the +0.050 escalation threshold set on 2026-05-29; escalation condition not met. Day 4 of the 7-day watch window. Trend is positive — no action. Escalation still triggers if any future run shows ≥+0.050 before the watch closes.
- **WARN `regression_wow` — Chicago/low (+0.049)**: Slightly worsened from +0.039 (05-31). Nudging the +0.050 escalation threshold but not over it. The 7d rolling Brier is 0.128 vs prior week's 0.079 — recent forecast period has been rough for Chicago lows. No code change to blame; attributed to late-May/early-June frontal variability continuing to roll through the 7d window.
- **`nbm_beats_ecmwf` — Chicago/high/0-6h (gap 0.046)**: Chronic; essentially unchanged (0.047 → 0.046). Still a Phase 3 ECMWF/NBM blend candidate. **NYC/high/0-6h (gap 0.024)**: Gap narrowed significantly from 0.053 (05-31) — approaching noise level; drop this cell from the high-priority Phase 3 NBM-blend list if it continues tightening.
- **Paper trades improving**: 841 settled, 61.7% win rate, 3.40% weighted ROI (up from 804 / 61.1% / 2.57% on 05-31). Austin/high (18.5% ROI, n=112) and Denver/high (14.6% ROI, n=122) driving gains. Chicago/high book improved to −1.7% ROI (from ~−2.5% on 05-31). Miami/high worst at −7.8% ROI (n=116) — consistent with KMIA exclusion being correct.
- **Chronic, no change**: KLAX `exclusion_holds` (gap +0.166), KMIA `exclusion_holds` (gap +0.158), KNYC `exclusion_holds` (gap +0.068) — all correctly excluded; await Phase 3 isotonic calibration. KNYC remains the most likely first re-enable candidate.
- **No critical flags → no GitHub issues; no exclude_candidate/reenable_candidate → no draft PR.**
- **Watch condition**: Chicago/high at day 4, below +0.050 — continuing to improve. Chicago/low now co-watches at +0.049, just under threshold. If both are below +0.050 at the next two consecutive runs (~2026-06-03, ~2026-06-05), close the watch. Escalation threshold for either: ≥+0.050 → flag as exclude_candidate, open draft PR.

## 2026-05-31

_Diagnostics source: `data/reports/diagnostics.md` generated 2026-05-30 14:41 UTC (`a78c093`). This is the first analysis of those diagnostics — the 05-30 memo used the prior 05-29 16:42 UTC run. Today's resolve.yml (13:00 UTC) had not yet committed new data at time of writing (latest commit is `5051f57`, a snapshot at 13:00:05 UTC). No code changes in 8-day window — only automated snapshot and resolve commits._

- **WARN `regression_wow` — Chicago/high (+0.074)**: Essentially flat vs +0.073 in the 05-30 memo (rolling 7d window shifted by one day, numbers have converged). This is the 3rd consecutive diagnostics cycle flagging Chicago/high. Per the 05-29 escalation condition, the 7-day watch clock started ~2026-05-29; we are at day 2 of 7 — still in watch mode. Chicago/high cumulative PnL is −3.4 across all lead buckets; paper trades ROI −2.5% (n=121 settled). The 0-6h bucket has the sharpest gap vs market (model 0.161 vs market 0.047) and is where NBM also underperforms the market (NBM 0.139 < ECMWF 0.185 but both lose badly to market 0.047) — Phase 3 calibration is the right lever here, not an exclusion.
- **`regression_wow` — Chicago/low improving to +0.039** (from +0.063 in 05-30 memo): Positive signal that the Midwest hard-weather week is rolling off the 7-day window. Consistent with genuine forecast miss attribution, not a systematic model failure. Likely clears next week barring another difficult forecast period.
- **No code changes in window**: 8-day `git log` contains only `Snapshot:` and `Resolutions + biases` commits. Chicago regressions remain attributed to late-May frontal variability — no code commit to blame.
- **`exclusion_holds` — KLAX (+0.160), KMIA (+0.165), KNYC (+0.067)**: All noise-level shifts (≤0.002 vs 05-30). Correctly excluded; KNYC has the smallest gap and remains Phase 3 re-evaluation priority. KLAX/KMIA still structurally miscalibrated.
- **`nbm_beats_ecmwf` — Chicago/high/0-6h (gap 0.047)**: Gap widened slightly from 0.040 last run; NYC/high/0-6h unchanged at 0.053. Still ×2 persistent cells; input for Phase 3 ECMWF/NBM blend. Note: even NBM (0.139) loses badly to the market (0.047) on Chicago/high/0-6h — this is a calibration problem, not solely a source-model selection problem.
- **Overall model healthy**: 804 settled paper trades, 61.1% win rate, 2.57% weighted ROI; Austin and Denver driving positive PnL. Chicago/high is the only book-level drag.
- **No critical flags → no GitHub issues; no exclude_candidate/reenable_candidate → no draft PR.**
- **Watch condition**: If Chicago/high `regression_wow` persists at next run (≥+0.050, ~2026-06-05), flag as exclude_candidate and open draft PR.

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
