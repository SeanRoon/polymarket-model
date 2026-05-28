# Model-watch: the model-improvement monitor

A two-layer loop that watches the model daily and surfaces where it can improve. It sits on
top of the existing scoring pipeline (`resolve.yml` → `evaluation.md` / `paper-trades.md`).

## Layer 1 — deterministic (`polymarket diagnose`)

`src/polymarket_model/diagnostics.py` reads the scored rows from
`evaluation.score_resolutions` and emits thresholded **flags**, rendered to
`data/reports/diagnostics.md`. Flag families:

| code | severity | what it catches |
|------|----------|-----------------|
| `exclude_candidate` | critical | An *included* station whose model Brier is worse than the market AND whose simulated PnL is negative — a candidate for `config.signal_excluded_stations`. |
| `reenable_candidate` | good | An *excluded* station whose model Brier now matches/beats the market — safe to re-enable. |
| `exclusion_holds` | info | An excluded station that's still miscalibrated; the exclusion stays. |
| `regression_wow` | warn | A (city, kind) whose Brier worsened over the last 7d vs the prior 7d. |
| `nbm_beats_ecmwf` | info | A (city, kind, lead) cell where NBM has materially lower Brier than the ECMWF ensemble — consider a blend. |
| `calibration_bias` | warn | A (city, kind) where mean(model_p) diverges from the realized YES rate — coarse miscalibration screen. |

Thresholds live in `DiagnosticsConfig`. It's pure, offline, and unit-tested
(`tests/unit/test_diagnostics.py`). It runs daily inside `.github/workflows/resolve.yml`
right after scoring, and the bot commits `diagnostics.md` back to `main`.

Run it by hand:

```
uv run polymarket diagnose --days-back 60 --markdown data/reports/diagnostics.md
```

## Layer 2 — the agent (`/model-watch`)

`.claude/commands/model-watch.md` is the standing prompt. Each run the agent:

1. reads `diagnostics.md` (+ the eval tables and its own prior log),
2. triages each flag as signal vs. noise,
3. root-causes `regression_wow` flags against `git log` (the main thing it adds over Layer 1),
4. ties findings to the Phase 3 roadmap in `CLAUDE.md`,
5. appends a dated memo to `data/reports/model-watch.md`.

**Read-mostly.** On `main` it edits and commits **only** the memo
(`data/reports/model-watch.md`, so its findings persist). For one specific, mechanical change —
adding/removing a station in `signal_excluded_stations` when a `critical`/`good` flag justifies
it — it opens a **draft** PR on a `model-watch/<slug>` branch (after `pytest` passes) for you to
review and merge. It never merges, never edits code on `main`, never touches `execution/`, and
never trades. Every other suggested change stays a memo recommendation.

Run it by hand in this repo:

```
/model-watch            # write the memo only
/model-watch issues     # also open a GitHub issue for each NEW critical flag
```

## Scheduling it (you do this once — not done automatically)

The deterministic layer already runs daily via GitHub Actions. The agent layer is **not**
scheduled yet, because a recurring remote routine is a standing commitment (and billable). To
turn it on, run the `/schedule` skill and ask for:

> Run `/model-watch` daily at 13:30 UTC (20 min after resolve.yml at 13:00 UTC), in this repo.

Add `issues` to the scheduled command if you want it to file GitHub issues for new criticals.
13:30 UTC ensures the fresh `diagnostics.md` commit from `resolve.yml` is already on `main`
when the agent reads it.

## Knobs (current defaults)

- **Leash:** read-mostly — commits only the memo to `main`; opens **draft** PRs for
  `signal_excluded_stations` edits only; optional GitHub issues (`/model-watch issues`). Never
  merges, never edits other code on `main`, never trades.
- **Memory:** keeps the running `model-watch.md` log so it doesn't repeat findings.

**Prerequisites for the PR path:** the runtime needs `gh` authenticated with push + PR-create
rights on the repo. If `main` has branch protection, draft PRs from the agent still require a
human approve+merge — which is the intended safety boundary.

To widen or narrow the leash, edit `allowed-tools` and the Leash section in
`.claude/commands/model-watch.md`. To go back to advisory-only, remove the `gh pr *` and
`git switch/branch` entries and restore the "do not edit code" rule.
