# Agent strategy playbook

**Version: v1** (seeded 2026-07-12 — no trades yet)

This file is owned by the `/self-trader` agent. The agent rewrites it after every
session based on what its settled trades actually did. Humans read it; only the
agent edits it. Every trade in the ledger cites the version that motivated it, so
`performance.md` scores versions against each other.

## Rules for editing this file (fixed — do not change these)

1. Bump the version (v1 → v2 → …) whenever a rule is added, removed, or changed.
2. Keep every hypothesis falsifiable and attributable: state what you expect to
   happen and what evidence would kill the rule.
3. Kill a rule after it is ≥10 settled trades underwater; scale up what wins.
4. Log every change in the changelog with the evidence that drove it.
5. Never risk-manage by editing this file — the CLI guards (bankroll, per-trade
   cap, position cap) are hard-coded and not yours to tune.

## Active rules

- **R1 (seed, model piggyback):** Trade weather bins where `agent-model-view` shows
  |model edge| ≥ 0.08 at lead ≤ 72h AND the cell's per-bin track record is ≥ 70% win
  rate with positive ROI on n ≥ 50 (today: Austin/high, Denver/high, San Antonio/high).
  Take the model's side. *Kill if: these trades run below the entry price's implied
  win rate over ≥10 settlements.*
- **R2 (seed, model with caution):** Cells where the model shows an edge but has a
  weak, thin, or negative record (most data-collection cities; anything Chicago) get
  at most 1 small trade per session, and only when the edge is ≥ 0.15 and I can
  articulate why the model might be right THIS time. *Kill if: 0-for-5 or worse.*
- **R3 (seed, own judgment):** Outside weather, trade only markets closing within
  7 days, 24h volume ≥ 1,000, spread ≤ $0.10, where my own world-knowledge estimate
  differs from the midpoint by ≥ 0.10. State the estimate in the thesis. *Kill if:
  realized win rate on these is below what entry prices imply.*
- **R4 (seed, exploration budget):** At most 1 trade per session may test a brand-new
  hypothesis outside the active rules; tag its thesis `[explore]`. *Permanent.*

## Open hypotheses (not yet rules)

- Is the model's edge on production-excluded cities real money the production trader
  is leaving on the table, or is the exclusion wisdom? R2's results will say.
- Longshot bias by category (do <10¢ YES books lose?); category-level edge (sports vs
  econ vs politics); time-to-close effects (is the last-day book sharper?).

## Changelog

- **v1** (2026-07-12): Seeded by the build. Model-piggyback rules R1/R2 (leverage the
  weather model's live edges + per-cell track record, all cities allowed including
  production-excluded ones), own-judgment rule R3, exploration budget R4.
