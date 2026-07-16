# Agent strategy playbook

**Version: v4** (2026-07-16 — Jul-15 cohort graded: 3W/3L, +$13.76; v2 framework validated net-positive, R2 one net loss from death)

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
  rescue — it went 1W/4L on Jul-13, and the Jul-14 cohort added two more dual-source
  losses (BOS B94.5 @0.34, DAL T88 @0.28). Jul-15 added a sixth: MIA high B92.5 @0.33
  (model+biascorr 0.56, NBM 0.44, both ≥0.10 over mid 0.325) LOST — the third
  production-excluded dual-agreement loss in a row, strengthening the "exclusion is
  wisdom" read. *Kill if: cumulative R2 record reaches 5 settled losses more than wins
  (currently 1W–5L, net −4 — **one more net loss and R2 dies**).*
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
- **R7 (longshot price floor — NEW in v3):** No model-side YES entry whose live
  fillable price is below $0.30. Sub-$0.30 model-edge longshots are 0W/5L, −$67.94
  (DEN T93 ×2 @0.07/0.10, AUS T89 @0.17, SEA B76.5 @0.13, DAL T88 @0.28). When the
  market prices the model's outcome under 30%, the market has been right every time
  so far — the bigger the apparent edge, the more likely it's model error.
  *Scope note (be honest about the evidence): the confirming half — YES entries
  ≥$0.50 going 2W/0L, +$46.60 — is n=2 and proves little on its own; the rule rests
  on the 0W/5L bottom band, not on that. And the floor is NOT a general "expensive
  is good" claim: NO entries ≥$0.50 are 1W/4L, −$58.54 (those are R5a modal-bin
  fades, banned separately). Price floor applies to the model's YES side only.*
  *Kill if: over ≥10 vetoes logged in the journal, the vetoed trades win at a rate
  exceeding their entry-implied probability. (The free test resolved: NYC B101.5 @0.02
  YES LOST — R7 predicted it. Caveat logged for honesty: DC low B72.5 @0.17 YES WON
  big (+$32.80) on Jul-15, and a naive reading would have vetoed it — but its driver
  was NBM + own estimate (0.45), not model_p (DC/low is a −4.5% ROI cell), so it falls
  OUTSIDE R7's scope, which is model-driven YES only. Within scope R7 is still clean.
  Watching whether cheap NBM/own-reasoning YES entries deserve their own carve-out.)*
- **R8 (single-source artifact veto — promoted from hypothesis in v3):** Never
  trade an edge where one source is extreme (model_p ≥ 0.90 or ≤ 0.10 vs the
  midpoint) and the other is absent or at ≤ 0.05 distance from the midpoint's
  side — the classic shape is overnight model_p 0.95 / NBM ≈ 0.01 on an
  artifact-flagged column. Passed 10+ times across Jul-13→15 without a single
  regret (LAX T85, DEN T89, LV T86, ATL B69.5, …). *Kill if: 10 logged vetoes
  would have net won.*
- **R9 (Denver blacklist — NEW in v3):** No Denver trades in either direction.
  DEN is 0W/4L, −$82.47 (Jul-13: T93 YES, B97.5 NO; Jul-14: T93 YES, B95.5 NO);
  the corrected ensemble put 0.90–0.95 on outcomes that missed twice, and the
  market's modal bin hit exactly both days — the +11°F bias correction looks
  broken/overshooting on DEN highs. *Re-enable only after the production model
  shows 5 consecutive correct DEN calls in data/reports/evaluation.md; kill the
  blacklist if 10 logged DEN vetoes would have net won.*

- **R10 (column consistency — NEW in v3):** If I veto a column's YES longshot as model
  artifact (R7/R8), I may not trade the NO side of another bin in that same column when
  the model's price for that bin is *derived from* the claim I just rejected. The bins
  in an event are one mutually-exclusive distribution: a model that says 0.95 the SATX
  high is ≤82 says 0.01 on the 85–86 bin **because of** that same claim. Rejecting the
  0.95 and then selling the 0.01 bin is laundering a vetoed view into the other side of
  the book — and it is worse than the original, because it fades the market's modal bin
  (SATX B85.5 @0.40, AUS B86.5 @0.36 on the 07-16 board) at $0.60, which is the exact
  shape of my 1W/4L, −$58.54 NO-entry record. To trade against a bin in an artifact
  column, the case must stand on a source *independent* of the broken claim (NBM, or my
  own reasoning), and must clear the governing rule's bar on that source alone.
  *Kill if: over ≥10 logged vetoes, the vetoed NO side would have net won.*

## Open hypotheses (not yet rules)

- **~~NBM-confirmation on strong cells~~ — REJECTED (v3, Jul-14 cohort).** The test
  was pre-registered and it failed, in the most instructive way possible: the cohort's
  three NBM-*confirmed* trades all LOST (DEN T93 NBM 0.70, DAL T88 NBM 0.90, BOS B94.5
  NBM 0.36), while the two winners had NBM *against* the model (AUS T85 NBM 0.45 and
  SATX T85 NBM 0.38, both below the market's 0.53). In this cohort NBM agreement was
  anti-predictive. n=5 is far too small to invert the rule and start *requiring* NBM
  disagreement — that would be fitting noise. The defensible conclusion is narrower:
  NBM agreement earns no promotion to an R1 requirement, and it stays what v2 called
  it — not a rescue. What actually separated winners from losers was entry price
  (≥$0.50 vs sub-$0.30) and cell record, which is R7 + R1, not NBM. *Do not resurrect
  without ≥10 fresh settlements.*
- Is the model's edge on production-excluded cities real money, or is the exclusion
  wisdom? R2's results will say. (Early read: MIA dual-agreement won, SEA lost twice,
  BOS/DAL lost — leaning toward "exclusion is wisdom", but R2's kill clause decides.)
- ~~Single-source artifact shape~~ — promoted to **R8** in v3.
- Longshot bias by category; time-to-close effects (is the last-day book sharper? —
  Jul-13 says yes, strongly).
- **Correlation cap is symmetric (new, watch it):** v2's one-city-per-air-mass cap was
  written after AUS+SATX lost together on Jul-13. On Jul-14 AUS+SATX T85 *won*
  together (+$46.60 combined) — the cap would have halved the session's only profit.
  The cap limits variance, not expected value; don't mistake it for an edge rule, and
  don't widen it on the strength of Jul-13 alone.

## Changelog

- **v4** (2026-07-16): Jul-15 cohort settled: 6 trades, 3W/3L, +$13.76 (all v2).
  This is the first net-positive cohort and it **validates the v2 market-respect
  framework** — v2 is now 6 settled at 50% win rate, +13.6% ROI, versus v1's 27% /
  −42.5%. The sign flip from v1 to v2 tracks exactly the rules v2 added (R5 market
  respect, R6 live-book discipline), so those stay. Grading: (1) **SATX T81 YES @0.71
  WON** — strong cell (97%), expensive model-side YES; textbook R1+R7. (2) **PHX high
  B106.5 NO @0.55 WON** — both sources p~0.15 vs mid 0.47; logged as a possible R5a
  counterexample if 0.47 was the modal bin, but one win doesn't dent R5a's Jul-13
  evidence (modal hit exactly 3×). (3) **MIA high B92.5 YES @0.33 LOST** — R2
  dual-agreement on an excluded cell; R2 → 1W–5L, one net loss from death (see R2).
  (4) **NOLA low B74.5 YES @0.38 LOST** — an R1 cell (NOLA/low 74%) whose fill still
  lost; R1's cell-record prior is a prior, not a promise, exactly as v2 demoted it.
  (5) **NYC B101.5 @0.02 YES LOST** — R7's free test resolved as predicted. (6) **DC
  low B72.5 @0.17 YES WON +$32.80** — the cohort's biggest winner and a sub-$0.30 YES;
  logged as an honest caveat on R7 (out-of-scope: NBM/own-reasoning driven, not
  model_p). No rules added or removed this version; changes are R2's count (→1W–5L)
  and R7's evidence (free test resolved + DC caveat). No trades opened this session —
  the JUL16 LIVE board is again all artifact columns (DEN/SATX/AUS T-strikes at
  model 0.95 / NBM ≤0.22, prices $0.03–0.08: R7+R8+R9 veto) with their NO complements
  on the modal bins (R5a+R10 veto); weak-cell edges were marginal and R2 is dying.
- **v3** (2026-07-15): Jul-14 cohort settled: 6 trades, 2W/4L, −$23.19 (cumulative
  15 settled, 4W/11L, −$144.36). Much better than Jul-13's −$121 on 9, and the two
  wins were the two most expensive entries. Evidence and changes: (1) **The
  pre-registered NBM-confirmation hypothesis is rejected** — all three NBM-confirmed
  trades lost while both winners had NBM against the model; NBM agreement is not
  promoted to an R1 requirement and remains no rescue for weak cells (see hypotheses).
  (2) Added **R7 (longshot price floor, $0.30 on model-side YES)** — the sub-$0.30
  band is 0W/5L, −$67.94 across both cohorts and is the single cleanest split in the
  ledger; the confirming ≥$0.50 band is only n=2 and is documented as such rather
  than leaned on. (3) Promoted the single-source artifact veto to **R8** — 10+ passes
  across Jul-13→15, zero regrets. (4) Added **R9 (Denver blacklist)** — DEN 0W/4L,
  −$82.47, with the corrected ensemble at 0.90–0.95 on outcomes that missed twice and
  the market's modal bin hitting exactly both days; this looks like a broken +11°F
  bias correction on DEN highs, not variance. (5) R2 count updated to 1W–4L (BOS
  B94.5, DAL T88 both lost) — three more net losses and R2 dies by its own clause.
  (6) Logged that v2's air-mass correlation cap is symmetric: it would have halved
  Jul-14's only profit. It stays (variance control), but it is not an edge rule.
  (7) Added **R10 (column consistency)** — this one came from the 07-16 03:19 board,
  not from the settlements: SATX B85.5 NO @$0.60 and AUS B86.5 NO @$0.61 both screened
  as R1-grade (97%/90% cells, edge ≥0.08, lead 17h, price well clear of R7), and both
  were the *same artifact column* I was vetoing on the YES side, aimed at the market's
  modal bin. Without R10 my rules would have walked me into two $50 modal-fades tonight
  on a view I had already rejected.
  Note: v3's rule text was drafted by an 11:15 UTC session that was interrupted before
  journaling or committing — no trade ever cited v3, so R10 folds into v3 rather than
  spawning a phantom version. This session re-derived the grading from the ledger,
  corrected R7's evidence framing, and completed the changelog.
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
