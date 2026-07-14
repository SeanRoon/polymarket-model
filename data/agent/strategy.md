# Agent strategy playbook

**Version: v2** (2026-07-14 — first settlement cohort graded: 2W/7L, −$121.17)

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

- **R1 (model piggyback, tightened in v2):** Trade weather bins where
  `agent-model-view` shows |model edge| ≥ 0.08 at lead ≤ 72h AND the cell's per-bin
  track record is ≥ 70% win rate with positive ROI on n ≥ 50 — **subject to all of
  R5 and R6 below** (no modal-bin fades, no entries against sharp adverse drift,
  live-book verification, one city per air mass per direction per day). The cell
  track record is the production model's record at ITS entry shapes, not a promise
  about mine — weight it as a prior, not a guarantee. *Kill if: R1 trades run below
  the entry price's implied win rate over the next 10 settlements (v1 R1 went 1–5,
  −$107; v2 restarts the count under the tighter filters).*
- **R2 (weak cells, bar raised in v2):** Cells with a weak, thin, or negative
  record get at most 1 small trade per session, and only when BOTH sources agree
  against the market (model_p and nbm_p on the same side of the midpoint, each by
  ≥ 0.10), the edge is ≥ 0.15 **at the live book**, and the position is not
  correlated with anything already open. Dual-model agreement alone is NOT a
  rescue — it went 1W/4L on Jul-13. *Kill if: cumulative R2 record reaches 5
  settled losses more than wins (currently 1W–2L).*
- **R3 (own judgment, unchanged — untested):** Outside weather, trade only markets
  closing within 7 days, 24h volume ≥ 1,000, spread ≤ $0.10, where my own
  world-knowledge estimate differs from the midpoint by ≥ 0.10. State the estimate
  in the thesis. *Kill if: realized win rate on these is below what entry prices
  imply.* (Note: weather-only mandate means these are scan-context only for now.)
- **R4 (exploration budget, unchanged):** At most 1 trade per session may test a
  brand-new hypothesis outside the active rules; tag its thesis `[explore]`.
  *Permanent.*
- **R5 (market respect — NEW in v2):** The settlement-day market is the sharpest
  signal available; it holds real-time observations the model snapshot doesn't.
  Concretely: **(a)** never fade the market's modal bin on settlement day (Jul-13:
  modal-bin NO fades went 1W/3L, −$65, and the market's modal bin hit *exactly* in
  DEN, AUS, and SEA); **(b)** sharp adverse repricing against the model side since
  the prior session is information, not an entry discount — do not open or add to
  the model's side after the market has moved ≥ 0.10 away from it (Jul-13: the
  overnight collapse of DEN T93 / AUS T89 / SATX T90 predicted all three losses);
  **(c)** market drift TOWARD the model after entry is confirmation, not a missed
  add. *Kill if: over ≥10 settlements, trades this rule vetoed would have won at a
  rate exceeding their entry-implied probability (track vetoes in the journal).*
- **R6 (live-book discipline — NEW in v2):** Always verify the live book before
  entry; the edge must clear the governing rule's bar at the actual fillable price,
  not the snapshot price (Jul-13 BOS B94.5: snapshot edge 0.28 became 0.06 at the
  live fill — would have been a pass). *Permanent (process rule).*

## Open hypotheses (not yet rules)

- **NBM-confirmation on strong cells:** Jul-13's DEN T93 loss had NBM against;
  today's open DEN T93 has NBM 0.70+ agreeing. If tonight's Jul-14 cohort (all six
  positions carry some NBM support) wins where Jul-13 lost, v3 should make NBM
  agreement a hard R1 requirement rather than part of R2 only.
- Is the model's edge on production-excluded cities real money, or is the exclusion
  wisdom? R2's results will say. (Early read: MIA dual-agreement won, SEA lost twice
  — inconclusive.)
- The single-source artifact shape (extreme model_p with NBM ≈ 0.01, usually
  overnight, usually negative-ROI cells) has been passed ~10 times and never
  regretted. Candidate v3 rule: formalize as a hard veto. Tracking via journal.
- Longshot bias by category; time-to-close effects (is the last-day book sharper? —
  Jul-13 says yes, strongly).

## Changelog

- **v2** (2026-07-14): First cohort settled: 9 trades, 2W/7L, −$121.17 (−58.8% ROI).
  Evidence and changes: (1) The market's Jul-13 modal bins hit exactly in Denver
  (97–98), Austin (93–94), and Seattle (80–81) — every one a bin the corrected
  ensemble priced at 0.01 and I faded; added R5a banning settlement-day modal-bin
  fades. (2) The overnight market collapse of my three cheap T-strikes was
  information — all three lost; added R5b (adverse-drift veto). (3) Dual-model
  agreement failed to rescue weak cells (AUS T89 NBM 0.64 lost, SATX T90 NBM 0.54
  lost, SEA B76.5 NBM 0.49 lost; only MIA B92.5 won) — raised R2's bar (both
  sources ≥0.10 vs market, edge ≥0.15 live, uncorrelated). (4) AUS+SATX T-strikes
  lost together to the same warm air mass as foreseen at open — R1 now caps one
  city per air mass per direction per day. (5) BOS B94.5 filled at 0.34 vs snapshot
  0.20 — added R6 live-book discipline. R1's cell-record prior is demoted from
  guarantee to prior: the production record (91–96% cells) did not transfer to my
  fills (realized 22%).
- **v1** (2026-07-12): Seeded by the build. Model-piggyback rules R1/R2, own-judgment
  rule R3, exploration budget R4.
