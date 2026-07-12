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

- **R1 (seed):** Trade only markets closing within 7 days, with 24h volume ≥ 1,000
  and spread ≤ $0.10 — liquid books with fast feedback, so the learning loop turns
  over quickly. *Kill if: fills at these filters systematically lose to fees.*
- **R2 (seed):** Prefer positions where your own world-knowledge estimate of the
  probability differs from the midpoint by ≥ 0.10. State the estimate in the thesis.
  *Kill if: realized win rate on these is below the entry price implies.*
- **R3 (seed, exploration budget):** At most 1 trade per session may test a brand-new
  hypothesis outside the active rules; tag its thesis `[explore]`. *Permanent.*

## Open hypotheses (not yet rules)

- None yet — seeded fresh. Candidates to investigate once data accrues: longshot
  bias by category (do <10¢ YES books lose?), category-level edge (sports vs econ vs
  politics), time-to-close effects (is the last-day book sharper?).

## Changelog

- **v1** (2026-07-12): Seeded by the build. Three starter rules, no trade history.
