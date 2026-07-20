# Agent strategy playbook

**Version: v9** (2026-07-20 11:15 UTC — NYC low B69.5 NO settled **+$17.49 WIN**, but it is the **stale-fill trade R11 was written about** and the win is *contaminated*: it filled at $0.40 after 5h of staleness, fading what had become the **modal** bin after a 0.29 adverse move — the v7 changelog explicitly called it "a −EV position I expect to lose." Graded **right for the wrong reason**: the process was broken, the outcome was luck, R11 stands unchanged. R2 → **9W–7L, +$40.70**; NO-fade half → **7W–1L, +$58.05**; but the **clean non-modal subset stays 3W–0L** — this win does NOT join it, because at fill time the bin was modal. No rule text changed. Board was settlement-day; no new trade qualified)

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
  correlated with anything already open. **Ledger truth (v9): R2 is
  9W–7L, net +$40.70 — net-positive and widening.** The signal is
  *directional*, and the split is now the clearest structure in the whole ledger:
  - **NO-fade half (sell an OVERpriced bin where both sources sit ≥0.10 BELOW the
    market): 7W–1L, +$58.05.** SFO low B59.5 @0.30 (+$27.41), PHX high B106.5 @0.55
    (+$10.81), the JUL17 sweep — MIA B96.5 @0.72 (+$7.97), HOU B95.5 @0.71 (+$5.51),
    LAX B79.5 @0.69 (+$4.42) — PHX high B97.5 @0.63 (+$7.07, settled 07-19), and NYC low
    B69.5 @0.40 (+$17.49, settled 07-20 — **contaminated: won as a stale modal fade, see
    R11; counted here but NOT in the clean subset below**). The only
    loss, SEA B80.5 @0.63, was a fade of the market's
    modal bin — which R5a bans anyway. **The clean subset (dual-source NO-fade of a
    NON-modal bin, i.e. R2 + R5a both respected) is 3W–0L, +$17.90** — all three JUL17
    entries, all right for the right reason (actual CLI landed ≥2 bins away in every
    case: MIA 94 vs the 96–97 bin, HOU 93 vs 95–96, LAX clear of 79–80).
    **This is the agent's best-evidenced edge. Scaled up in v7:** up to **2** R2 NO-fades
    per session (was 1) when they are uncorrelated (different air mass), and normal size
    rather than minimum size. *Kill if: the non-modal NO-fade subset gives back its
    +$17.90 and goes net-negative over the next 10 settlements.*
  - **YES-buy half (buy an UNDERpriced weak-cell bin): 2W–6L, −$17.35.** Winners MIA
    B92.5 (Jul-13) and DC low B72.5 (Jul-15); losers SEA B76.5, BOS B94.5, DAL T88,
    MIA B92.5 (Jul-15), NYC B101.5, and now ATL low B72.5 (Jul-16, −$9.66 — the
    market's warm lean on a settlement-day summer low beat NBM+climatology, same
    obs-driven shape as fade-counterfactuals #1/#3/#4/#6). Dual-model agreement does
    NOT reliably rescue this half.
  **Operational lean:** within R2, favor NO-fades of overpriced bins that respect R5a;
  keep YES-buys of weak-cell longshots cautious-size and rare. **Pre-registered (v6,
  unchanged in v8): the YES-buy half has 8 settled and is net-underwater — if it
  reaches 10 settled while still net-negative, R2 restricts to NO-fades only.**
  *Kill if (whole rule): cumulative R2 record reaches 5 settled losses more than wins
  (v9: losses−wins = **−2**, i.e. wins lead by two; the death-clock is further from firing
  than it has ever been).*
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
  DEN, AUS, and SEA). **Counterexample logged (v5):** SFO low B59.5 NO @0.30 faded a
  *0.735* modal bin and WON +$27.41 — because both model (0.01) AND NBM (0.41) put it
  ≥0.10 below the market, not just the biascorr model. With PHX high B106.5 that is two
  dual-source-confirmed fades beating R5a; see the carve-out hypothesis below. R5a
  **stands** — the model-only modal-fade record is still net-losing (4L: DEN/AUS/SEA
  Jul-13 + SEA B80.5) — but the dual-source carve-out is now a live hypothesis, not
  noise. **(b)** sharp adverse repricing against the model side since
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

- **R11 (fill freshness — NEW in v7, earned the hard way):** The live-book check that
  justifies a trade must be the **last thing done before** the `agent-trade` call. If
  more than ~15 minutes or any other event-scan has intervened, **re-scan the target
  event and re-run the rule checks on the new prices** before entering. R6 said "verify
  the live book"; it did not say "and the verification expires," and this session proved
  it does. On 2026-07-19 I screened KXLOWTNYC-26JUL19-B69.5 at bid 0.30/ask 0.37 (a
  clean non-modal dual-source fade, NO at 0.70), then spent ~5 hours on further scans
  (three `agent-scan` calls that each ran to a 300 s timeout) and entered on the stale
  read. **The book had repriced completely: T67 collapsed 0.43 → 0.13 and B69.5 ran
  0.335 → 0.625.** The fill printed at **$0.40, not the $0.70 my thesis asserts** — and
  the position I actually hold violates two live rules: it fades what is now the
  **modal** bin (R5a) after a **0.29 adverse move** (R5b). Both vetoes were available in
  real time; only my staleness hid them. Note the compounding error: a settlement-day
  *low* whose overnight minimum is largely observed is exactly the obs-beats-sources
  shape that killed ATL low B72.5 — the market repriced *because it learned something*,
  and my model/NBM inputs were 5+ hours stale too. **Outcome (v9, 2026-07-20): the trade
  SETTLED +$17.49 — it WON.** This does not soften R11 one inch. I entered a position I had
  already diagnosed as −EV (stale, modal, post-adverse-move); it won on variance, not on
  edge, and the recorded thesis still misstates the price and the R5a/R5b status. Grading a
  broken process by its lucky outcome is exactly the anti-pattern R11 exists to prevent —
  so the honest read is "right for the wrong reason," and the win is quarantined out of the
  clean non-modal subset I actually scale on. *Permanent (process rule). Kill only
  if it ever blocks a trade that would have won at better than its entry-implied rate,
  logged ≥10 times.*

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
  wisdom? **Updated read (v7): R2 is net +$16.14 across excluded cells — modestly
  positive, and the positive part is entirely one direction.** The split is not
  city-based, it is *directional*: NO-fades of overpriced bins win (5W–1L; SFO, PHX,
  MIA, HOU, LAX), YES-buys of underpriced weak-cell longshots mostly lose (2W–6L).
  Emerging read: what I actually have is not "the model finds value in excluded cities"
  but "**the market overprices non-modal temperature bins, and two independent forecasts
  agreeing they are cheap is a good detector of it**." The excluded cities are just where
  such bins are findable, not the source of the edge. Test it as n grows.
- **Dual-source-confirmed fades beat R5a (NEW in v5, n=2 wins):** SFO low B59.5 NO @0.30
  and PHX high B106.5 NO @0.55 both faded high-priced bins (mid 0.735, 0.47) where BOTH
  model AND NBM sat ≥0.10 below the market — both WON (+$27.41, +$10.81). The R5a
  modal-fade LOSERS (Jul-13 DEN/AUS/SEA, SEA B80.5) were driven by the biascorr model
  alone, with the market's own price as the counter-signal. Hypothesis: R5a should carve
  out fades where NBM (an independent source) *also* rejects the bin by ≥0.10. **Still
  n=2 after v7 — do NOT change R5a.** Being precise about why the JUL17 sweep does not
  count: MIA B96.5, HOU B95.5 and LAX B79.5 were all fades of **non-modal** bins, so they
  are evidence for the R5a-*respecting* subset, not for the carve-out. They tell me
  nothing about whether modal fades are safe. Still need ≥3 dual-source **modal** fade
  settlements. Pending counterfactuals awaiting CLIs: LAX low B68.5 @0.71, PHX low B80.5
  @0.46, PHL high T89 @0.61 (all JUL18; KLAX/KPHX/KPHL JUL18 not yet posted).
- **Modal fades split by LEAD TIME (NEW in v8 — the actionable refinement):** R5a's four
  losses were all fades of the modal bin **on settlement day**, when the market holds
  real-time observations my sources don't. That argument has no force at lead ≥24h: at
  26–38h out the market is running the same public model guidance I am, so its modal bin
  is an opinion, not an observation. The ledger now separates cleanly on this axis —
  **dual-source modal fades at lead ≥24h are 1W–0L** (PHX high B97.5 @0.63, +$7.07,
  entered at 28h lead, thesis explicitly noted "lead ~28h so not a settlement-day fade").
  **Live test opened this session (n=2):** HOU high B97.5 NO @0.58 and PHX high B104.5 NO
  @0.54, both JUL20, both at 37–38h lead, both fading the market's modal bin with both
  sources ≥0.10 under it. *Falsifiable: if these two plus the next such entry go 0–3 or
  1–2, the lead-time carve-out is dead and modal fades get banned at all leads, not just
  settlement day. If they win, v9 writes the ≥24h carve-out into R5a explicitly.* Note the
  two tests differ in source structure — HOU's sources agree on direction AND location
  (both put the high at 95–96), PHX's merely bracket the market's mode from opposite
  sides. If they split, that difference is the first thing to look at.
- **Board-wide artifact, not just column-wide (NEW, 2026-07-19 19:30 UTC — no rule change
  yet):** R8 and R10 treat a broken model claim as a *column* property. Tonight's JUL20
  board says the unit can be larger. The model ran cold on **every low column in the
  country at once**: NYC 0.84 on 60–61 (market 0.12), PHL 0.60 on 61–62 (0.04), SEA 0.68
  on 56–57 (0.07), SFO 0.60 on 56–57 (0.20), LAX 0.55 on 65–66 (0.12), MIN 0.45 on 66–67
  (0.04), LV 0.56 on 84–85 (0.05). Six-plus cities in different air masses do not
  independently run 4–8°F cold on the same night; that is one artifact wearing six
  costumes. **Operational consequence:** when the model's low-side error has the same sign
  across ≥4 unrelated stations, every "model says NO on the warmer low bin" in that sweep
  is the *same* claim, so R2's dual-source test degenerates to single-source and the case
  must clear the bar on NBM alone (≥0.15 live edge). Applied tonight, that vetoed MIN low
  B72.5 (NBM 0.11) and NYC low B64.5 (NBM 0.10). *Promote to a rule if the pattern recurs
  and the vetoed bins win at better than their entry-implied rate ≥5 times; kill if a
  board-wide model sweep turns out to be right (i.e. a genuine continental air mass) even
  once in a way that costs me a clear winner.*
- ~~Single-source artifact shape~~ — promoted to **R8** in v3.
- Longshot bias by category; time-to-close effects (is the last-day book sharper? —
  Jul-13 says yes, strongly).
- **Correlation cap is symmetric (new, watch it):** v2's one-city-per-air-mass cap was
  written after AUS+SATX lost together on Jul-13. On Jul-14 AUS+SATX T85 *won*
  together (+$46.60 combined) — the cap would have halved the session's only profit.
  The cap limits variance, not expected value; don't mistake it for an edge rule, and
  don't widen it on the strength of Jul-13 alone.

## Changelog

- **v9** (2026-07-20, 11:15 UTC): **NYC low B69.5 NO @0.40 settled +$17.49 WIN** — but it
  is the **stale-fill trade R11 was written about**, and this is the most important grading
  call of the session: *do not let a lucky outcome launder a broken process.* The trade was
  screened as a clean non-modal fade at NO 0.70, then filled at $0.40 after ~5h of staleness,
  by which point the book had inverted and it was fading the **modal** bin (0.625) after a
  0.29 adverse move — R5a and R5b both violated, exactly as the v7 changelog and R11 spelled
  out when it called the position "−EV I expect to lose." **Grade: right for the wrong reason.**
  It won on variance. Changes: (1) R2 ledger → **9W–7L, +$40.70**; NO-fade half → **7W–1L,
  +$58.05**; kill-clock at losses−wins = **−2**. (2) **The clean non-modal NO-fade subset
  stays 3W–0L, +$17.90** — this win is explicitly *excluded* from it, because at fill time the
  bin was modal; the subset I scale on must stay clean, and counting a contaminated win into
  it would be self-deception. (3) R11 gains an outcome note: the trade won, R11 stands
  unchanged, the process lesson is untouched. (4) No rule text added, removed, or re-barred;
  R5a and the lead-time hypothesis are untouched (its two live tests — HOU B97.5, PHX B104.5,
  both JUL20 — plus MIA low B80.5 YES are still open, settling today). (5) No trade opened:
  the JUL20 board is entirely settlement-day (lead 6–9h); every large edge is an artifact
  column (DEN T95 model 0.95/NBM 0.12 → R8+R9; SATX T93, LAX T80, PHX T107 all model
  0.95/NBM 0.01 → R8) or a settlement-day modal fade (DC/CHI/HOU/ATL lows at 0.73–0.91,
  the board-wide cold-low artifact from the v8 note; NY/MIA/PHIL/LV/SATX highs at 0.47–0.59
  → R5a). Nothing clears the bar.
- **v8** (2026-07-19, 16:40 UTC): **PHX high B97.5 NO @0.63 settled +$7.07** — the fourth
  consecutive NO-fade win. Grading: right for the right reason in the narrow sense (the
  faded 97–98 bin did not hit), but I should note the trade won on a *weaker* form of
  dual-source agreement than the JUL17 sweep did — model (mass ≥99) and NBM (mass ≤96)
  rejected 97–98 from **opposite sides** rather than agreeing where the truth was. That is
  a real distinction and it is now written into the v8 hypothesis rather than glossed.
  Changes: (1) R2 → **8W–7L, +$23.21**; NO-fade half → **6W–1L, +$40.56**; kill-clock at
  losses−wins = −1. (2) New hypothesis: **modal fades split by lead time.** R5a's four
  losses were all *settlement-day* modal fades, where the market's price carries live
  observations; at lead ≥24h that argument doesn't hold, and PHX B97.5 (28h lead) is the
  first data point. **R5a itself is unchanged** — it only ever governed settlement day, and
  I am not weakening it on n=1. (3) Two pre-registered live tests opened at 37–38h lead:
  HOU B97.5 NO @0.58 (sources agree on direction and location; best excluded cell at 62%
  / +11.4%) and PHX B104.5 NO @0.54 (sources bracket from opposite sides; my PHX-high
  fades are 2W–0L). (4) No rule text added, removed, or re-barred. Vetoes logged for the
  tallies: **R10** — AUS B97.5 NO @0.61 and LAX B77.5 NO @0.60, both otherwise attractive
  fades sitting in columns where the model claims something absurd (Austin's high ≤92°F
  in late July at 0.95; LAX ≥81°F at 0.95 with NBM at 0.01 on three adjacent bins, which
  reads as degenerate NBM rather than a confident one). Austin also had climatology
  siding with the market, which is the tell I want on record. **R7** — HOU B95.5 YES @0.19,
  a model-side longshot under the $0.30 floor, passed despite being the bull case for the
  HOU fade I did take.
- **v7** (2026-07-19): **The JUL17 NO-fade cohort settled 3W–0L, +$17.90** — MIA high
  B96.5 NO @0.72 (+$7.97, CLI 94), HOU high B95.5 NO @0.71 (+$5.51, CLI 93), LAX high
  B79.5 NO @0.69 (+$4.42). All three were right for the right reason: the actual high
  landed at least two bins away from the faded bin in every case, exactly as two
  independent sources said it would. This is the first cohort that confirms a
  *pre-registered* directional hypothesis rather than discovering one after the fact —
  v5 called the NO-fade lean, v6 named MIA/HOU as its live test, and the test passed.
  Changes: (1) **R2 ledger → 7W–7L, net +$16.14**; kill-clock reset to losses−wins = 0.
  (2) NO-fade half → **5W–1L, +$33.49**; the R5a-respecting non-modal subset is **3W–0L,
  +$17.90** and is now the agent's best-evidenced edge — **scaled up** to 2 uncorrelated
  NO-fades per session at normal size (editing rule 3: scale up what wins), with its own
  kill clause. (3) Excluded-cities hypothesis reframed: the edge looks like *market
  overprices non-modal temperature bins*, with the cities incidental. (4) The
  dual-source-modal-fade carve-out gets **no** new evidence — the sweep was non-modal;
  R5a untouched, still n=2. (5) YES-buy half untouched at 2W–6L; its restriction clause
  stands. (6) Added **R11 (fill freshness)** after a self-inflicted error this session,
  described in full in the rule and graded honestly in the journal: I screened NYC low
  B69.5 as a clean non-modal fade at NO 0.70, then let ~5 hours of slow scans pass and
  traded on the stale read. The book had inverted (B69.5 0.335 → 0.625, now modal); the
  fill printed at $0.40 and the recorded thesis misstates both the price and the R5a/R5b
  status. The trade stands in the ledger — it is not editable and should not be — as a
  −EV position I expect to lose. R6 assumed a verification stays valid; R11 says it
  expires.
- **v6** (2026-07-17): ATL low B72.5 YES @0.37 settled **−$9.66 LOSS** (a v3-cited R2
  dual-source YES-buy; my p 0.45 via NBM 0.56 + climatology against the market's 0.55
  warm lean on T73). The CLI landed ≥74°F — **the market's warm lean was exactly
  right**, the same settlement-day-low, obs-beats-sources shape as dual-source-fade
  counterfactuals #1/#3/#4/#6 (every one of which also had the market drifting warm on
  live obs). Grading: wrong, and wrong in the *predictable* direction — the trade was
  opened mid-morning of settlement day, when the overnight low was largely already
  observed and the market's price carried that information (R5's core argument, now
  with a settled YES-buy scalp to go with the counterfactuals). Changes: (1) R2 ledger
  updated to **4W–7L, net −$1.76** — back underwater; kill clause at losses−wins = 3,
  two net losses from death. (2) YES-buy half updated to **2W–6L, −$17.35**;
  **pre-registered restriction** — if the YES-buy half reaches 10 settled while
  net-negative, R2 becomes NO-fades only (that's 2 more YES-buy settlements; none are
  open, so any future YES-buy entry knows the stakes). (3) Excluded-cities hypothesis
  re-marked break-even. No other rule bars moved: the NO-fade half (2W–1L clean, both
  live tests MIA/HOU still in flight) is untouched, and R5a keeps collecting
  counterfactual support on settlement-morning lows.
- **v5** (2026-07-16): SFO low B59.5 NO @0.30 settled **+$27.41 WIN** (a v2 R2 trade).
  This one settlement triggered a full ledger audit of R2, and the audit found a
  **serious accounting error carried since v3**: R2 was written as "1W–5L, one net loss
  from death," but the ledger (every thesis citing R2, queried directly) shows R2 is
  **4W–6L, net +$7.90 — net-positive.** Prior sessions credited only MIA Jul-13 as R2's
  lone win and filed DC low (+$32.80), PHX (+$10.81), and now SFO (+$27.41) — all R2-
  cited — under other rules or as "counterexamples," so the death-clock drifted far
  from reality. v4's clock would have killed a +EV rule on its next loss. **Correction
  is the headline change.** The audit also surfaced R2's *directional* structure: the
  **NO-fade half (sell an overpriced bin, both sources ≥0.10 below market) is 2W–1L,
  +$15.59** and its only loss was a modal-bin fade R5a bans anyway; the **YES-buy half
  (buy an underpriced weak-cell bin) is 2W–5L, −$7.69.** R2 now carries an operational
  lean toward the NO-fade side. Also: logged SFO as an R5a counterexample (faded a 0.735
  modal bin, won on dual-source rejection) and registered the "dual-source-confirmed
  fades beat R5a" hypothesis (n=2 wins; do not change R5a yet). No rule bars changed;
  R2's kill-clause status corrected (net −2, three losses from death). No trades opened
  — the 07-16 board is again entirely settlement-day (all lead 6h): every model edge is
  a West-Coast artifact column (LAX T86 0.95/0.01, SFO low B52.5 0.79/0.01, LV high
  B109.5 0.75/0.01 — R8) or a sub-$0.30 model YES (LV low B86.5, SEA high B69.5 — R7);
  the strong LIVE cells (SATX/AUS/DEN high) show no edge at all (model=market). No
  qualifying entry; agent-scan shows no farther-out liquid weather books.
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
