# Agent trading journal

Dated reasoning log from the `/self-trader` agent — one section per session, newest
first. Each entry records: settlements reviewed, what they said about the current
strategy version, any strategy changes (with the why), and every trade opened this
session with its thesis. PAPER ONLY.

---

<!-- The agent appends dated sections (## YYYY-MM-DD HH:MM UTC) below this line, newest first. -->

## 2026-07-16 09:16 UTC — nothing settled, no qualifying edge, holding 8

`agent-settle` → `settled=0 still_open=8`; JUL15 book + ATL JUL16 still open, no CLI yet, **no
grading, v3 stands.** Same board as 08:16 (snapshot 134 min stale): SATX T83 (0.95/0.16/0.04)
and AUS T84 (0.95/0.15/0.08) remain the R7/R8 artifact columns; weak-cell edges (CHI low B74.5,
NOLA high B91.5, DC low B77.5, OKC low B66.5) all have model_p and nbm_p on opposite sides of
the mid → fail R2's dual-agreement bar; Denver edges → R9. The one real dual-source edge, ATL
low B72.5, is already held → duplicate guard. Nothing new clears the bar. **Next:** watching for
the JUL15 book + ATL JUL16 (R2 decider) to post CLI — that settlement is the learning event.

## 2026-07-16 08:16 UTC — nothing settled, no qualifying edge, holding 8

`agent-settle` → `settled=0 still_open=8`. The six JUL15 markets + NY JUL15 haven't posted CLI
resolutions yet and remain open on Kalshi; no grading, **no strategy change; v3 stands.** Scan
re-derives the same board: SATX T83 (0.95/0.16/0.04) and AUS T84 (0.95/0.15/0.06) are R8/R7
artifact columns; the only genuine dual-source edge is ATL low B72.5 (model 0.84 / NBM 0.61 /
mid 0.18), which I already hold — duplicate guard. Nothing new clears the bar. **Next:** the
JUL15 book + ATL JUL16 (R2 decider, lead 9h) should settle in the next session or two — that's
the real learning event.

## 2026-07-16 07:16 UTC — nothing settled, no qualifying edge; fresh snapshot vindicates last hour's live-book read; holding 8

`agent-settle` → `settled=0 still_open=8`. No settlements → no grading, **no strategy change; v3
stands unedited.** First non-stale board in four sessions (07:01 snapshot, 14 min old).

Strong cells re-derive identically to the last three sessions: SATX T83 (model 0.95 / NBM 0.16 /
mid 0.04) and AUS T84 (0.95 / 0.15 / 0.06) are R8 artifact columns, R7 on price, R10 on their NO
bins. DEN — R9. ATL low B72.5 is the board's only dual-source R2 shape and I already hold it (it
is the R2 decider; duplicate guard would reject anyway).

**Worth recording:** last hour I priced DAL/HOU/MIN low at the *live* book and called their large
snapshot edges "two-thirds staleness, one-third model outlier." The snapshot has now caught up,
and the edges vanished on their own — HOU B77.5 is model 0.10 / NBM 0.42 / mid 0.43, i.e. NBM
sitting exactly on the market; DAL B74.5 has dropped off the board entirely; MIN B74.5 still fails
R2 (NBM 0.46 only 0.08 from mid 0.54) and is the modal bin besides. This is a small but real
confirmation of **R6**: the live book was right about the fresh snapshot an hour before the fresh
snapshot existed. R6 keeps earning its keep as a process rule, not just a haircut.

**Next session:** ATL B72.5 (lead 9h) settles today — it is the R2 decider, and R2 dies by its own
clause at three more net losses. That grading is the next real learning event; everything else is
holding.

## 2026-07-16 06:16 UTC — nothing settled, no qualifying edge; the stale-snapshot edges are a measurement artifact, confirmed at the live book; holding 8

`agent-settle` returned `settled=0 still_open=8`. No settlements → no grading, **no strategy
change; v3 stands unedited.** Third session on the same 04:16 snapshot (now 119 min stale —
the snapshot cron has not committed since). Strong cells re-derive identically: SATX T83
(model 0.95 / NBM 0.16 / mid 0.04) and AUS T84 (0.95 / 0.15 / 0.07) are **R8** artifact
columns, **R7** on price, **R10** on the column's NO bins. DEN — **R9**.

**What this hour actually added (worth more than the vetoes):** I priced the three R2-shaped
weak-cell candidates at the *live* book instead of trusting the snapshot, and all three
collapsed for the same reason:

| bin | snapshot mid | live mid | model_p | nbm_p | verdict |
|:----|-------------:|---------:|--------:|------:|:--------|
| DAL low B74.5 | 0.65 | **0.42** | 0.12 | 0.42 | R2 fails: NBM sits *on* the live market |
| HOU low B77.5 | 0.54 | **0.425** | 0.10 | 0.42 | R2 fails: same, plus modal bin (R5a) |
| MIN low B74.5 | 0.57 | 0.55 | 0.08 | 0.46 | modal bin, 0.55 vs 0.32 next (R5a) |

The DAL/HOU "−0.52 / −0.43 edges" were **two-thirds staleness and one-third model outlier**.
Once repriced, NBM agrees with the market to within 0.00–0.01 and the only dissenter is
model_p — which is exactly the **R8** single-source shape, arriving in a form I hadn't seen
before: not an overnight 0.95/0.01 blowup, but a quiet mid-range disagreement that *looks*
like dual-source support until you refresh the book. **R6 earned its keep this hour**: it is
what turned three "qualifying" R2 trades into three passes. Worth noting these would have
been ~$50 fades of modal bins at ~$0.58 NO — the precise shape of my 1W/4L NO-entry record.

No rule change: R6 and R8 already cover this, and one session is not evidence for a new rule.
But if stale-snapshot edges keep manufacturing R2 candidates that die at the live book, v4
should consider requiring NBM to clear its ≥0.10 bar **against the live mid** explicitly,
rather than leaving that implicit in R6.

Veto counters: R10 at 4 logged, R8 at 15+, R7 at 4, R5a at 3 more this session. Next session:
the Jul-15 cohort (7 positions) is overdue for CLI and the ATL B72.5 R2 decider is live —
that is the hour that earns the deep review.


## 2026-07-16 05:16 UTC — nothing settled, no qualifying edge (same 04:16 board re-adjudicates to the same vetoes); holding 8

`agent-settle` returned `settled=0 still_open=8`. No settlements, so no grading and **no
strategy change; v3 stands unedited.** The snapshot is the same 04:16 board the prior
session already worked, and it re-derives identically: SATX T83 (model 0.95 / NBM 0.16 /
mid 0.04) and AUS T84 (0.95 / 0.15 / 0.07) are single-source artifact columns — **R8** on
the YES side, **R10** on every NO bin in the column (SATX B85.5/B87.5, AUS B86.5/B88.5,
all aimed at the market's modal bin at ~$0.60). Weak-cell shapes (MIN low B74.5, HOU low
B77.5, ATL high B90.5) are all modal-bin fades on settlement day — **R5a**. DAL low B74.5
blends to a 0.08 edge, under R2's 0.15 live bar. DEN — **R9**.

Veto counters (for the kill clauses): R10 now at 4 logged vetoes (needs ≥10 to test),
R8 at 12+, R7 at 4. Next session: the ATL B72.5 R2 decider and the Jul-15 cohort should
start settling — that is the hour that earns the deep review.


## 2026-07-16 04:16 UTC — nothing settled; first v3 trade (ATL B72.5, the R2 decider); holding 8

**Settlements: none.** The seven Jul-15 positions are all still pending CLI
finalization — `agent-settle` returned `settled=0 still_open=7`. No settlements means no
grading and **no strategy change; v3 stands unedited**, per the session procedure.

**The board mostly vetoed itself, and that is v3 working as designed.** The 07-16 board
is the same artifact shape I have been rejecting since Jul-13 — the corrected ensemble
putting 0.88–0.95 on cold-side T-strikes the market prices at $0.04–0.08:

- **DEN T89** (model 0.95, mid 0.04, edge +0.91) — vetoed by **R9** (Denver blacklist).
  Worth noting how badly I would have wanted this without the rule: it is the single
  biggest number on the board, and DEN/high is a 91% / +24.9% cell. That is exactly the
  siren R9 was written for after DEN went 0W/4L, −$82.47.
- **AUS T84** (+0.89 @ $0.07) and **SATX T83** (+0.88 @ $0.08) — vetoed by **R7**. These
  are the 97% and 90% cells, so R1's prior screams yes; the price floor says no, and the
  sub-$0.30 band is 0W/5L. Note the contrast with the Jul-14 *winners* (AUS/SATX T85 @
  $0.55/$0.57): there the market half-agreed at 0.53. Here it disagrees totally at 0.07.
  Same cells, same model conviction, opposite market posture — that is the split R7 encodes.
- **SATX B85.5 @0.40 and AUS B86.5 @0.39** (the NO sides of those same columns) — vetoed
  by **R5a + R10**. Both are the market's modal bin, and both derive from the claim I just
  rejected on the YES side. R10's first live outing; it worked.
- **AUS B88.5 NO @$0.71** — considered seriously and passed. R10 lets me trade an artifact
  column on an independent source, and NBM (0.15 vs mid 0.29) formally clears 0.08 alone.
  But no active rule covers a *single-source NBM* entry, so it would be an R4 explore — and
  spending my one explore on a modal-adjacent NO fade at $0.71 is the exact shape of my
  worst losses (NO ≥$0.50 is 1W/4L, −$58.54; Jul-13 AUS B93.5 NO @0.66 lost −$33.79). Bad
  explore. Declined.
- **NOLA H B91.5** (model 0.79, NBM 0.40, ask $0.21) — a clean R2 shape on both sources,
  killed by **R7**'s floor at $0.21. R7 is earning its keep.

**R6 caught a live one.** My only R1-qualifying candidate was **NOLA L B75.5** (74% / +6.0%
cell, model 0.68 vs snapshot mid 0.58). The live book had gutted it: **bid 0.57 → 0.28**,
ask 0.55, a 27-cent spread on 100 contracts, with **B77.5 (0.38/0.39) taking over as the
modal bin**. The market moved ≥0.10 away from the model's side overnight — textbook
**R5b**, the same collapse that predicted all three Jul-13 losses. Vetoed. The snapshot was
198 min stale and would have walked me straight into it.

**Trade opened (1): KXLOWTATL-26JUL16-B72.5 YES ×25 @ $0.37 (cost $9.66), R2.**
My p ~0.45 vs implied 0.37. This is the only spot on the board where a source *independent
of the model* disagrees with the market: NBM 0.56 and model 0.75, both ≥0.10 over the live
ask, book verified unmoved from the snapshot (no R5b drift), price clear of R7, uncorrelated
with my 7 open, and I am **buying** the #2 bin rather than fading the leader (T73 @ ~0.55),
so R5a is untouched. I discount the model's 0.75 hard — ATL/low is 46% / −4.0% — so my 0.45
is really NBM plus climatology (Atlanta's July mean min ~71–72°F makes 72–73 plausible; the
market's 0.55 on ≥74°F is warm-leaning). Small size on purpose: an 8-point edge is thin.

**Why take it at all, given R2 is 1W–4L and I think it is probably dead?** Because I
pre-registered the kill clause (net −5) and this setup meets every condition R2 states.
Refusing a qualifying trade because I have pre-judged the rule makes the rule unfalsifiable
— if I believe R2 is dead I should kill it on evidence, not quietly starve it. This is the
trade that decides it: one more net loss beyond this and R2 dies by its own clause.

**What I want to learn by next session:** whether the Jul-15 cohort (7 positions, $113.83 at
risk) finally settles — it is the first real test of the *pre*-R7 book, and four of those
seven would not have been opened under v3 (SFO B59.5 NO @0.30 and PHX B106.5 NO @0.55 are
modal-ish NO fades; NYC B101.5 @0.02 and DC B72.5 @0.17 are sub-$0.30 longshots, with
NYC B101.5 explicitly logged as R7's free test). If R7's vetoed shapes lose again, the floor
is confirmed on live evidence rather than back-fitted.

---

## 2026-07-16 03:19 UTC — Jul-14 cohort graded (2W/4L), v3 finished and shipped, zero trades, holding 7

**Housekeeping first: recovering an interrupted session.** Found the working tree dirty
on arrival — an 11:15 UTC session had run `agent-settle` (settling the Jul-14 cohort) and
drafted strategy v3, then died before journaling or committing. ~16h of sessions are
missing from the log because of it. I re-derived the grading from the ledger rather than
trusting the draft, and it was worth doing: v3's R7 claimed "entries ≥$0.50 are 2W/0L,"
which is true only for YES entries (n=2); **NO** entries ≥$0.50 are 1W/4L, −$58.54. The
draft had quietly picked the flattering half of the split. Fixed the wording and scoped
R7 to the model's YES side, where the real evidence (0W/5L, −$67.94 under $0.30) lives.

**Settlements reviewed — Jul-14 cohort, 6 trades, 2W/4L, −$23.19** (cumulative: 15
settled, 4W/11L, −$144.36). Better than Jul-13's −$121 on 9, and the shape is informative:

- **AUS T85 YES @0.55 → WON +$25.96** and **SATX T85 YES @0.57 → WON +$20.64.** Right for
  the right reason: strong cells (90%/97%), cool regime held, market half-agreed at 0.53.
- **DEN T93 YES @0.10 → LOST −$15.95.** This was the pre-registered NBM-confirmation test
  (NBM 0.70 agreeing where Jul-13's loss had NBM against). It failed. Wrong.
- **DEN B95.5 NO @0.59 → LOST −$24.28.** Second expression of the same DEN view. Wrong,
  and correlated — one bad column cost me twice.
- **BOS B94.5 YES @0.34 → LOST −$17.79** and **DAL T88 YES @0.28 → LOST −$11.77.** Both R2
  dual-source-on-weak-cell. Wrong. R2 is now 1W–4L.

**The hypothesis died the informative way.** All three NBM-*confirmed* trades lost; both
winners had NBM *against* the model (0.45/0.38 vs a 0.53 market). NBM agreement was
anti-predictive in this cohort. I am explicitly **not** inverting it into "require NBM
disagreement" — n=5, that's fitting noise. The rule that actually separated winners from
losers was price: ≥$0.50 went 2W/0L, sub-$0.30 went 0W/5L. That's R7, not NBM.

**Strategy changes (v2 → v3, now complete and shipped):** R7 longshot price floor ($0.30,
model-side YES only, with the evidence scoped honestly); R8 artifact veto promoted from
hypothesis (10+ passes, no regrets); R9 Denver blacklist (0W/4L, −$82.47 — the +11°F bias
correction on DEN highs looks broken, not unlucky); R2 count updated to 1W–4L (three more
net losses and it dies by its own clause); NBM hypothesis marked rejected; logged that the
air-mass correlation cap is symmetric — it would have halved Jul-14's only profit, so it's
variance control, not an edge rule.

**R10 (new, from tonight's board — the most valuable thing this session produced).** The
07-16 board is one giant artifact column across the Texas cities: model 0.95 that the SATX
high is ≤82 and the AUS high is ≤83, against markets at 0.05/0.07 and NBM at 0.23/0.25.
R7 correctly vetoes the YES longshots. But then **SATX B85.5 NO @$0.60 and AUS B86.5 NO
@$0.61 screened as clean R1 trades** — 97% and 90% cells, edge ≥0.08, lead 17h, price far
clear of R7's floor. I nearly took one. They are the *same broken column*: the model prices
the 85–86 bin at 0.01 **because** it believes the ≤82 claim I just rejected. Selling that
bin is laundering a vetoed view onto the other side of the book — and it aims at the
market's modal bin (SATX B85.5 is the column's high mark at 0.40, with mass at 85–88) at
$0.60, which is precisely my 1W/4L, −$58.54 NO-entry pattern. R10 now forbids it: to trade
against a bin in an artifact column, the case must stand on a source independent of the
broken claim. My rule set had a hole that let a rejected view back in through the exit.

**Trades: zero.** Every candidate vetoed, and I'm logging them for the kill-clause counts:
DEN T89 (R9+R7), LAX T86 (R8+R7), **AUS T84 @0.08 and SATX T83 @0.06 (R7 — strong cells,
exactly the 0W/5L shape)**, SATX B85.5 NO / AUS B86.5 NO (**R10**, first two vetoes logged),
NYC T96 (R8+R7), NOLA B91.5 @0.21 (R7), LV low T87 and SFO B56.5 (modal-fades in the
model's two worst cells — LV/low 32%, and a market at 0.84–0.89 at 19h lead knows more than
I do), CHI T92 (sources contradict, 51% cell). The one genuine non-artifact candidate was
**ATL B72.5 YES**: model 0.75 *and* NBM 0.56 vs a 0.32 mid, and it clears R7 at a 0.35 ask.
Vetoed on R2's live-book bar — the book is 0.28/0.35 on OI of *16*, the market drifted
~0.06 against me since the snapshot, and in a 46%-win cell the model's 0.75 earns no
weight; honest p ≈0.45 off NBM → edge ≈0.10 < 0.15. Not worth my one R2 slot when R2 is
three net losses from death.

**What I want to learn by next session:** whether the Jul-15 cohort (7 open, all v2, incl.
the NYC B101.5 @0.02 longshot that R7 would now ban) settles in a way that confirms the
price floor — that trade is a free live test of R7, and I want it to lose. Also whether the
Texas artifact column verifies: if the SATX/AUS highs land at 85–88 as the market says, R10
just saved me ~$100 on night one and DEN/R9 gets more support.

## 2026-07-15 10:16 UTC — nothing settled, no qualifying edge, holding 13

Same 08:30 snapshot the 09:17 session already adjudicated (all vetoes stand); no new
board, no CLIs yet. Jul-14 cohort grades after the ~13:00 UTC resolutions.

## 2026-07-15 09:17 UTC — nothing settled, no qualifying edge, holding 13

Fast session on a fresh 08:31 snapshot; re-adjudicates to the 07:16 result. Only new
consideration: DEN JUL15 B95.5 NO (model 0.01/NBM 0.01 vs mid 0.26) — passed because
the model's whole DEN column is artifact-flagged today (0.95 on "88° or below" vs NBM
0.08), so it's effectively single-source NBM. All other candidates are the standing
vetoes: dups (SATX T81, NOLA B74.5, PHX B106.5), AUS T82 air-mass cap, MIN B98.5 /
NY T97 correlated with open NYC B101.5, SFO B57.5 same-event as SFO B59.5, and the
07:16 R5a modal-fade trio unchanged. Jul-14 cohort grades after the ~13:00 UTC CLIs.

## 2026-07-15 08:16 UTC — nothing settled, no qualifying edge, holding 13

Fast session. Same 06:00 UTC snapshot as the prior two sessions (now 136 min stale) —
board already adjudicated at 06:20 (opened NYC B101.5) and 07:16 (all R2 candidates
R5a-vetoed); nothing new to trade. Jul-14 cohort settles after the ~13:00 UTC CLIs —
next session gets the full grading pass and the NBM-confirmation hypothesis test.

## 2026-07-15 07:16 UTC — nothing settled, no qualifying edge, holding 13

Fast session. Jul-14 cohort still awaits ~13:00 UTC CLIs; v2 unchanged. Board check
against the 06:00 snapshot: the only R1-cell edges (SATX T81, NOLA B74.5) are already
held; no AUS/DEN high edges. R2 candidates all blocked — **R5a vetoes logged for
kill-clause tracking:** BOS low B77.5 NO (model 0.19 / NBM 0.22 vs mid 0.46), NOLA
high B90.5 NO (0.38/0.31 vs 0.54), MIA high B94.5 NO (0.42/0.17 vs 0.57) — all
settlement-day modal-bin fades. SFO low B57.5 YES passed on correlation with open
SFO B59.5. Next session: Jul-14 settlements should land — full grading pass due.

## 2026-07-15 06:20 UTC — nothing settled; NBM is back in the snapshot (R2 alive again), one R2 trade opened (NYC high B101.5 YES); holding 13

Nothing settled (Jul-14 cohort still grades after the ~13:00 UTC CLIs); version stays
v2. Fresh 06:00 snapshot ends the NBM outage flagged at 04:20 — nbm_p is populated
across the board, so no operator flag needed and R2 is functional again.

**Opened:**

- **NYC JUL15 high B101.5 YES x200 @0.02, cost $4.28** (R2 weak-cell slot, v2) —
  thesis p≈0.12 vs market 0.02: NBM puts 0.25 on 101–102° and only 0.16 on ≤96°,
  vs a thin 2am-ET book pricing ≤96° at 0.51 — NBM sits ~3°F hotter than the
  market; the corrected ensemble agrees hotter (0.53). Full R2 checklist passed:
  dual-source ≥0.10 each side of mid, edge ≥0.15 at the live ask (verified 0.02),
  R5b clean (book identical to 03:35 — no adverse drift), uncorrelated (no NYC
  exposure). First trade guard lesson: count is capped at 1..200 (tried 400).

**Adjudicated and passed:**

- MIN high B98.5 YES also cleared R2's letter (model 0.58 / NBM 0.19 vs mid 0.055,
  live ask 0.06 verified) but it is the same hypothesis as the NYC trade — "NBM
  reads the overnight book too cold on mid-July heat" — and R2 allows one small
  trade per session; two correlated fills teach less per dollar than one. If the
  NYC ticket wins/loses, it grades the hypothesis either way.
- SATX high B81.5 / B83.5 NO (edges −0.20/−0.17, 96% cell): complement of my open
  SATX T81 YES — R1 one-city-per-direction cap.
- NOLA low B74.5 YES (+0.21, 73% cell, R1-qualifying) — already held, duplicate guard.
- Standing artifact vetoes hold: LAX T85 (model 0.95 / NBM 0.01), LV low T86
  (model 0.01 / NBM 0.69 vs mid 0.89 — model broken cold there, 32% cell), ATL low
  B69.5 (NBM 0.12). NBM's return makes the single-source shape visible again —
  every one of today's top-10 "edges" fails dual-source. More v3-veto evidence.

**Open-position notes:** NY T97 mid 0.465→0.51 (market drifting cooler, against the
NBM/model hot read — under R5b's 0.10 bar but worth watching against the new NYC
ticket); MIN B94.5 0.465→0.395 drifted toward the models.

**Want to learn by next session:** the 13:00 UTC CLIs settle the six Jul-14
positions — the first real grade of v2's R1 and the NBM-confirmation hypothesis.
Secondarily: does the NYC book reprice toward NBM as US morning liquidity arrives?

## 2026-07-15 05:15 UTC — nothing settled; same 03:37 board the 04:20 session adjudicated (no newer snapshot, NBM still absent so R2 stays dead), no qualifying edge, holding 12; Jul-14 cohort grades after ~13:00 UTC CLIs

## 2026-07-15 04:20 UTC — nothing settled; snapshot cron back (fresh 03:35 board after ~3.5h gap), adjudicated to zero trades; holding 12

Nothing settled (Jul-14 cohort grades after the ~13:00 UTC CLIs); version stays v2.
The board is finally fresh, but **nbm_p is absent from the entire 03:35 snapshot**
(every row "-"), which decides the session by itself: R2 requires dual-source
agreement so it cannot fire, and every large edge on the board is single-source —
the exact overnight artifact shape (extreme model_p, no NBM, negative-ROI or
artifact-flagged cells) that's been passed ~10 times without regret. More support
for formalizing the single-source veto in v3.

**Adjudication:**

- Standing vetoes all hold: AUS T82 YES (R1 air-mass cap vs open SATX JUL15 T81,
  now the only R1-qualifying edge on the board — market drifted toward the model,
  0.57 vs 0.53 prior, which is R5c confirmation, not a missed add); DEN T89 YES
  (artifact, edge now +0.94 with the whole DEN distribution still flagged); NYC
  T97 NO (R5b); LV pair (R5b).
- NOLA low B76.5 NO (edge −0.15) is just the complement of my open NOLA B74.5 YES —
  correlated, skip.
- Open-position notes: DC low B72.5 YES — the model has shifted DC's low mass down
  to B70.5 (model 0.69 there vs 0.05 mid), away from my bin; adverse model drift,
  no action (R5c symmetry: drift after entry is not an exit signal either, and
  there's no NBM to confirm). PHX B106.5 NO — mid 0.47→0.41, drifting toward me.

**Want to learn by next session:** the 13:00 UTC CLIs settle the six-position Jul-14
cohort — the first real grade of v2's R1 and the NBM-confirmation hypothesis; also
whether NBM reappears in the next snapshot (if its absence persists, flag it for the
operator as a data problem, since R2 is dead while it lasts).

## 2026-07-15 03:15 UTC — nothing settled; fourth session on the stale 00:05 board (snapshot cron ~3h quiet), no qualifying edge, holding 12; if the cron is still silent at the next daytime session, flag it for the operator

## 2026-07-15 02:16 UTC — nothing settled; still no snapshot newer than 00:05 (third session on the same board — 00:25 adjudicated it, 01:15 confirmed), no qualifying edge, holding 12; snapshot cron now ~2h quiet, worth noting if it persists into the morning

## 2026-07-15 01:15 UTC — nothing settled; no new snapshot since 00:12 (same board the 00:25 session adjudicated: PHX B106.5 opened, LV/NYC/DEN/AUS vetoes stand), no qualifying edge, holding 12

## 2026-07-15 00:25 UTC — nothing settled; one R2 trade opened (PHX high B106.5 NO); holding 12

Nothing settled (Jul-14 cohort grades overnight); version stays v2. Fresh 00:05 UTC
snapshot re-adjudicated.

**Opened:**

- **PHX JUL15 high B106.5 NO x25 @0.55** (R2 weak-cell slot) — thesis p(106–107)≈0.15:
  NBM 0.19 + model 0.08 vs market mid 0.47, both ≥0.10 below. Key drift distinction vs
  the LV veto below: the market repriced away in the morning (0.385→0.51 by 15:47 UTC)
  but has sat flat ~0.49 for 8 hours (last tick 0.505→0.485, toward the models), while
  BOTH models moved away from the bin on evening runs (NBM 0.28→0.19, model 0.19→0.08)
  and shifted mass to 108–109 — the widening gap came from model updates, not market
  drift, so R5b does not trigger since the prior session. Live book verified 0.45/0.49
  one minute before entry; NO filled exactly at 0.55 vs NBM-fair 0.81 → live edge 0.26
  ≥ R2's 0.15 floor (R6 clean). Yes it fades the modal bin, but not on settlement day
  (17h lead, evening before) — R5a doesn't apply; if this loses to the modal hitting,
  it's evidence for extending R5a to evening-before fades. Small size (weak-ish cell,
  55%/+2.1%), uncorrelated with open book. R2 count entering: 1W–2L.

**Vetoes (kill-rule tracking):**

- **LV JUL15 high B107.5 NO / B105.5 YES (NEW, R5b)** — model 0.42 + NBM 0.44 tightly
  agree vs mid 0.65 (live NO edge ~0.19), but the market ground 0.545→0.65 over the
  day (+0.105 away from the model side) and accelerated in the last hour (0.575→0.65)
  while the models themselves drifted TOWARD the bin (NBM 0.39→0.44). Evening-market
  grind toward a modal bin is the exact NYC/ATL shape; both LV tickets are the same
  ≤106 bet so both vetoed as one. Track: if LV high lands outside 107–108, R5b takes
  damage.
- DEN JUL15 B93.5 NO (model 0.01, NBM 0.24 vs mid 0.46) — the Denver distribution is
  artifact-flagged this cycle (T89 model 0.95 vs NBM 0.15 vs market 0.01); if model_p
  is corrupted on one tail it's untrusted on both, leaving a single-source (NBM) modal
  fade. Passed.
- Standing: AUS T82 YES (R1 air-mass cap vs open SATX T81, sixth session); DEN T89 YES
  (artifact, edge now +0.94); NYC T97 NO (R5b, drift widened again 0.495→0.60).
- Note: yesterday's PHX low B89.5 R5b veto — the market has since come back toward the
  model (mid 0.45→0.20). Entry would have been profitable mark-to-market; settlement
  still decides the kill-rule tally.
- Open-position note: NOLA B74.5 YES (filled 0.38) marked adverse, mid 0.325→0.21.
  R5c: drift after entry is not an add signal either way; holding.

**Want to learn by next session:** the Jul-14 cohort (6 positions) finally grades v2's
R1 and the NBM-confirmation hypothesis; plus whether PHX B106.5 (model-update
divergence, no market drift) behaves differently from the drift-veto class (LV, NYC).

## 2026-07-14 23:17 UTC — nothing settled; fresh 22:13 snapshot re-adjudicated to zero trades: all standing vetoes hold (ATL T72 drift now 0.235→0.64 — R5b looking stronger), new candidates fail (ATL B71.5 YES is the anti-drift side of the same R5b veto; LAX B68.5 NO would double coastal-low exposure vs open SFO B59.5; OKC B69.5 edge still <0.15 floor), holding 11

## 2026-07-14 22:20 UTC — nothing settled; no new snapshot since 21:08 (same board as last session, all vetoes stand), no qualifying edge, holding 11

## 2026-07-14 21:20 UTC — nothing settled, no qualifying edge (all candidates are standing vetoes, disagreement shapes, or miss the R2 live-book floor — OKC low B69.5 closest at ~0.11 < 0.15), holding 11

## 2026-07-14 20:20 UTC — nothing settled; no qualifying edge (three R2 candidates killed by R5b drift); holding 11

Nothing settled; version stays v2. Three fresh R2 dual-agreement candidates all
surfaced with big snapshot edges — and all three failed the R5b intraday-drift check.
Snapshot history shows the market repriced warm-overnight-lows/hot-highs sharply
against the model side all afternoon while model_p/nbm_p sat static:

**Vetoes (kill-rule tracking, all R5b — track outcomes):**

- NYC JUL15 high T97 NO (model 0.01/NBM 0.20 vs mid 0.495) — mid drifted
  0.355→0.495 today, +0.14 away from the model side.
- ATL JUL15 low T72 NO (model 0.01/NBM 0.22 vs mid 0.51, NBM edge 0.27) — mid
  drifted 0.235→0.51, +0.27 away. Volume 254 and climbing; the market is actively
  buying ≥73.
- PHX JUL15 low B89.5 NO (model 0.01/NBM 0.24 vs mid 0.45) — mid drifted
  0.19→0.45, +0.26 away.
- Standing R1 vetoes unchanged: AUS JUL15 T82 YES (air-mass cap vs open SATX T81,
  fifth session), DEN JUL15 T89 YES (single-source artifact shape, still +0.92 on
  the board).

If these three R5b vetoes settle on the model/NBM side anyway, R5b starts taking
damage (its kill clause needs ≥10 tracked vetoes). If they settle with the market,
it's the strongest confirmation yet that stale-snapshot edges against same-day
repricing are traps.

**Want to learn by next session:** tonight's Jul-14 settlements (6 positions) grade
v2's R1 and the NBM-confirmation hypothesis; plus the three R5b vetoes above and
DEN T89 as the artifact test.

## 2026-07-14 19:20 UTC — nothing settled; one R1 trade opened (NOLA low B74.5); holding 11

Nothing settled (Jul-14 cohort still grades tonight); version stays v2. Fresh 18:41
snapshot surfaced one candidate that cleared the R1 bar — the first v2 R1 trade on a
non-TX cell.

**Opened:**

- **NOLA JUL15 low B74.5 YES x60 @0.38** (R1) — thesis p≈0.55: model+biascorr 0.68
  on an R1-qualifying cell (NOLA/low: 73% win, +5.9% ROI, n=145 — one of only four
  positive-ROI cells on the board), shaded toward NBM 0.41 which is on the same
  side. Live book verified 0.29/0.38 one minute before entry, filled exactly at the
  verified ask (R6 clean). Buying the market's modal bin, not fading it; no drift
  vs the prior snapshot; Gulf-humid-night bet, uncorrelated with the TX-cool /
  DC / MIA / SFO book. Thin book (24h vol 27) → modest size. R1-v2 count entering:
  0W–0L (v2 restart).

**Vetoes (kill-rule tracking):**

- AUS JUL15 T82 YES (model 0.95, edge +0.33) — R1 air-mass cap, fourth straight
  session: same Texas cool-side bet, same day, same direction as open SATX T81.
- DEN JUL15 T89 YES (model 0.95 vs mid 0.03, edge +0.92!) — artifact shape despite
  the cell's elite record: NBM 0.18 and the market 0.03 both far from model, and
  the whole model Denver distribution sits ~5°F cool of NBM+market (B93.5 model
  0.01 vs mid 0.45). Plausible bias-correction overshoot; the biggest edge on the
  board is exactly the kind I no longer buy. Track it — if ≤88 actually hits, the
  artifact hypothesis takes real damage.
- DEN JUL15 low B61.5 YES (model 0.68, NBM 0.01) — single-source artifact,
  negative cell; passed again.
- SFO JUL15 low B57.5 YES (model 0.71, NBM 0.43, mid 0.22) — attractive dual
  agreement but near-duplicate of my open SFO B59.5 NO (both win on a ≤58 low);
  not doubling the same coastal-marine-layer exposure.
- SEA JUL15 low B55.5 YES (model 0.66, NBM 0.10) — single-source shape on a
  −5.8% cell; passed.

**Want to learn by next session:** tonight's Jul-14 settlements (6 positions) grade
v2's tightened R1 and the NBM-confirmation hypothesis. Also DEN JUL15 T89 as a
tracked veto — the cleanest test yet of the single-source-artifact hard-veto
candidate, on the model's best cell.

## 2026-07-14 18:17 UTC — nothing settled; one R2 trade opened (SFO low B59.5 NO); holding 10

Nothing settled (still 9 open pre-trade; Jul-14 cohort grades tonight). Version
stays v2. Fresh 17:20 snapshot surfaced one candidate that cleared the R2 bar.

**Opened:**

- **SFO JUL15 low B59.5 NO x40 @0.30** (R2 weak-cell slot) — thesis p(59–60)≈0.41
  by NBM / 0.01 by model, vs live mid 0.735: both sources ≥0.10 below market. Live
  book verified at 0.70/0.77 one minute before entry, filled exactly at the
  verified NO price (R6 clean). NBM fair NO 0.59 → edge +0.29 at fill. Weak cell
  (57%/−3.3%) so small size; uncorrelated with the TX/DEN/BOS/MIA/DC book. NO wins
  on ≤58 or ≥61 — the model's own modal bin is 57–58 at 0.71, and NBM thinks
  57–58 vs 59–60 is a coin flip (0.43/0.41) while the market pays 0.74 on 59–60.
  Not a settlement-day modal fade (38h to close); price drifted 0.01 TOWARD the
  model since the prior snapshot. R2 count entering: 1W–2L.

**Vetoes (kill-rule tracking):**

- AUS JUL15 T82 YES (model 0.95, edge +0.36) — R1 air-mass cap, third straight
  session: same Texas cool-side bet as open SATX T81. Cost of the cap keeps
  accruing if both would have won; grade after tomorrow's settlement.
- DAL JUL15 low (T73 NO / B72.5 YES, dual agreement intact) — same Texas cool/wet
  air mass as SATX T81; R2 slot spent on SFO anyway.
- SEA JUL15 low B59.5 NO (dual 0.01/0.26 vs mid 0.52) — same shape as the SFO
  trade but weaker NBM edge (0.26) and it would double coastal-marine-layer
  exposure in one night; one coastal low is enough.
- LV JUL15 low T86 NO (dual, NBM edge 0.18) — worst cell on the board
  (32%/−14.2%); still not paying for it.
- LAX T85 / DC T105 / CHI B102.5 / PHX low B83.5 single-source artifacts (model
  0.58–0.95, NBM ≈0.01) — passed again; v3 hard-veto evidence keeps growing.

**Want to learn by next session:** tonight's Jul-14 settlements (6 positions) are
the v2 / NBM-confirmation test — that's the session that decides whether v2's
tightened R1 actually transfers. Also whether NBM-vs-market disagreement on
coastal lows (SFO tonight) is as tradable as it looks.

## 2026-07-14 17:20 UTC — nothing settled, no new snapshot (still 15:47), holding 9

Nothing settled; snapshot unchanged since the 16:20 session, so every candidate and
veto from that session stands as-is (AUS T82 / DAL B72.5 still blocked by the R1/R2
Texas air-mass cap while SATX T81 is open). No new data → no trade. Next session:
Jul-14 cohort should start settling this evening — that's the first real grade for v2.

## 2026-07-14 16:20 UTC — nothing settled; one R2 trade opened (MIA B92.5); holding 9

Nothing settled; version stays v2 until tonight's Jul-14 cohort grades it. Fresh
15:47 snapshot (first new data since 14:04) surfaced one candidate that cleared the
bar.

**Opened:**

- **MIA JUL15 B92.5 YES x45 @0.33** (R2 weak-cell slot) — thesis p≈0.50: model 0.56
  + NBM 0.44, both ≥0.10 over live mid 0.325; live book verified at 0.32/0.33 one
  minute before entry and filled exactly at the verified ask (R6 clean, unlike
  SATX). Weak cell (47%/−5.1%) so small size, uncorrelated with the TX/DEN/BOS
  book. This is the exact shape of the Jul-13 clean R2 win (same bin, same
  dual-agreement, modal-adjacent, +19.94). Not a modal fade — modal bin is B94.5
  and I'm buying, not shorting. R2 count entering: 1W–2L.

**Vetoes (kill-rule tracking):**

- AUS JUL15 T82 YES (model 0.95, edge +0.41, book now healthy 0.54/0.55) — R1
  air-mass cap: same Texas cool-side bet, same direction, same day as open SATX
  T81. Second consecutive session vetoed; if SATX T81 wins big tonight+tomorrow,
  note the cap's cost, but the Jul-13 AUS+SATX double-loss is why it exists.
- DAL JUL15 low B72.5 (dual 0.44/0.39 vs mid 0.15 — strongest dual agreement on
  the board) — R2 correlation veto: same Texas cool/wet air mass as SATX T81, and
  only one R2 slot per session anyway (went to MIA).
- SEA JUL15 T83 (dual 0.44/0.40 vs mid 0.22) — R2 slot taken; also the model's
  Seattle cool bias burned two Jul-13 trades, so demanding more than one session
  of agreement before paying for that cell again.
- CHI low B75.5 (model 0.60 vs mid 0.33) — KMDW artifact persists per diagnostics;
  Chicago model_p untrusted, and NBM (0.29) is below mid anyway.
- LAX T85 / SFO T78 / LV low B83.5 single-source artifacts (model 0.5–0.95, NBM
  0.01–0.02) — passed again; candidate v3 hard-veto evidence keeps growing.

**Want to learn by next session:** tonight's Jul-14 settlements (6 positions) are
the v2 / NBM-confirmation test. Also whether MIA B92.5's Jul-13 win was signal
(sea-breeze regime the ensemble reads well) or luck — same bin, two days running.

Same 14:04 snapshot as the 14:20 session — no new information. Two additional candidates checked and passed: CHI low B77.5 dual-agreement (0.62/0.31 vs mid 0.17) vetoed because diagnostics report the KMDW artifact persisting, so Chicago model_p isn't trustworthy; DEN low B63.5 NO-fade (both models under 0.05 vs mid 0.31) vetoed because model (≤62) and NBM (65–68) straddle the faded bin from opposite sides — the Jul-13 modal-hit failure shape. Tonight's Jul-14 settlements remain the v2 test.

## 2026-07-14 14:20 UTC — nothing settled; first v2 trades opened (2); one R6 process violation to own

Nothing settled (6 open, all Jul-14, graded tonight). Fresh 14:00 snapshot finally
landed with the Jul-15 boards, so the wide look was warranted. No strategy change —
version stays v2 until tonight's cohort grades it.

**Opened (both Jul-15, first trades citing v2):**

- **SATX T81 YES x50 @0.71** (R1) — thesis p≈0.70: model+biascorr 0.95 on the
  system's best cell (96%/+30.8%/n=132), NBM 0.43 against so I shaded hard; market
  itself near a coin flip on the Texas rain regime, so this buys the modal side
  rather than fading it. **Process violation:** I sent the order off the 11-min-old
  snapshot book (0.54/0.55) and got filled at 0.71 — the market had moved +0.16
  toward the model within the hour. That drift is R5c confirmation of direction,
  but at 0.71 my own stated p leaves ~zero ex-ante edge. This is the BOS B94.5
  mistake repeated, one day after writing R6 to prevent it. Grade this trade as a
  process error regardless of outcome; the fix is procedural: **always pull the
  live book (agent-scan --event) immediately before agent-trade, never rely on the
  snapshot price** — which I then did for the second trade.
- **DC low B72.5 YES x40 @0.17** (R2 weak-cell slot) — thesis p≈0.45: model 0.62 +
  NBM 0.35 both ≥0.10 over mid; live book verified at 0.11/0.17 one minute before
  entry (R6 done right). Weak cell (51%/−3.4%), so small and uncorrelated with the
  open Texas/DEN/BOS highs. R2 running count: 1W–2L.

**Vetoes (kill-rule tracking):**

- DEN T89 YES (model 0.95, NBM 0.11, mid 0.06) — single-source artifact shape,
  ~11th consecutive pass; identical to the Jul-13 DEN T93 loser. The candidate v3
  hard-veto rule keeps accumulating evidence.
- AUS T82 YES — broken book (0.06/0.54, R6) and the Jul-15 Texas cool-side slot
  went to SATX (air-mass cap).

**Want to learn by next session:** tonight's Jul-14 cohort is the big one — it
tests NBM-confirmation (all six carry some NBM support) and v2's market-respect
rules. Also whether SATX T81's 0.55→0.71 repricing was smart money.

## 2026-07-14 13:20 UTC — nothing settled, no qualifying edge, holding 6 positions

Same 11:56 UTC snapshot as the 12:15 session — no new information; all candidates remain vetoed as logged there. Tonight's Jul-14 settlements are the v2 / NBM-confirmation test.

## 2026-07-14 12:15 UTC — nothing settled, no qualifying edge, holding 6 positions

Fast session. Vetoes logged for R5/R6 kill-tracking:

- NOLA low B70.5 YES — qualifying R1 cell (73%/+5.7%, n=139) but live edge 0.23−0.17 = 0.06 < 0.08 (R6 pass-on-live-book).
- OKC high T88 YES — dual agreement (0.25/0.58 vs mid 0.10) but same southern-plains cool-air-mass bet as open DAL T88 (R2 correlation veto).
- SEA high B80.5 YES — dual agreement (0.81/0.29 vs mid 0.03) but buying it fades the settlement-day modal bin B84.5 @0.51 (R5a veto; exact Jul-13 SEA failure shape).
- MIN/DAL/PHX low mega-"edges" (+0.4 to +0.9) — 12Z means today's lows are already largely observed; the 0.8–0.99 market bins KNOW. Stale-model artifact, not edge (R5 spirit). LAX/SFO/CHI high single-source artifacts (model 0.7–0.94, NBM 0.01) passed again — veto count for the candidate v3 rule keeps growing.

Watch: open DEN T93 YES (92° or below) now prices 0.16 vs model 0.95 / NBM 0.76 — market strongly disagrees; R5c says hold, don't add. Tonight's settlement is the NBM-confirmation hypothesis test.

## 2026-07-14 11:15 UTC — the Jul-13 cohort settled: 2W/7L, −$121.17; strategy → v2; no new trades

**Settlements (all nine Jul-13 positions; the first real learning event):**

| trade | result | grading |
|:------|:-------|:--------|
| DEN T93 YES @0.07 | −11.19 | Wrong. NBM (0.11, against) was right; the 91%-win cell record didn't save a trade NBM rejected. Denver hit 97–98. |
| AUS T89 YES @0.17 | −17.99 | Wrong. Dual agreement (NBM 0.64) didn't save it. Austin hit 93–94. |
| SATX T90 YES @0.34 | −35.58 | Wrong. Same: NBM 0.54 agreed and lost. |
| MIA B92.5 YES @0.32 | **+19.94** | Right, possibly for the right reason: dual agreement on the modal-adjacent bin, and Miami hit 92–93. The one clean R2 win. |
| DEN B97.5 NO @0.50 | −31.05 | Wrong for the worst reason: the market's modal bin hit EXACTLY. Ensemble 0.01 on the true outcome. |
| AUS B93.5 NO @0.66 | −33.79 | Same failure: modal-adjacent bin hit exactly; both models priced it 0.01–0.05. |
| SATX B92.5 NO @0.58 | **+22.16** | Right, but for a lucky reason: won because SATX overshot the bin — the underlying "high ≤89" view was still wrong (T90 YES lost). |
| SEA B76.5 YES @0.13 | −11.04 | Wrong. Dual agreement (0.77/0.49) on a weak cell; Seattle hit 80–81. |
| SEA B80.5 NO @0.63 | −22.63 | Wrong. Market's modal bin hit exactly, third time in one night. |

**What the cohort taught (all three open questions from 07-13 answered):**
1. *Was the overnight market move information or noise?* **Information.** All three
   T-strikes the market repudiated overnight lost, and doubling into the same view via
   modal-bin NOs added −$42.68 more. The settlement-day book holds real-time obs the
   stale ensemble doesn't.
2. *T-strike YES vs modal-bin NO — which expression paid?* **Neither**, but modal-bin
   NO was categorically worse: the market's modal bin hit exactly in DEN, AUS, and SEA
   (1W/3L, −$65 on fades).
3. *Does dual-model agreement rescue weak cells?* **Mostly no** — 1W/4L across the
   dual-agreement tests. MIA's win is the only survivor.

**Strategy → v2:** R5 (market respect: no settlement-day modal-bin fades; adverse
drift ≥0.10 against the model is a veto, not a discount; drift toward = confirmation),
R6 (live-book verification, from the BOS fill miss), R1 tightened (subject to R5/R6,
one city per air mass per direction, cell record demoted to a prior — the production
model's 91–96% cells delivered me 22%), R2 bar raised (both sources ≥0.10 vs market,
edge ≥0.15 live, uncorrelated). Full evidence in the changelog.

**Trades opened: none.** Board check against v2: MIA B92.5 YES fails R2 (NBM 0.43 is
below the 0.52 mid — no dual agreement); NY B96.5 YES is dual-agreed but correlated
with held BOS B94.5 (same Northeast heat, and NYC/high is the model's worst cell at
42%/−6.2%); DEN B93.5 NO is exactly the modal-bin fade R5a now bans; LAX/SFO/CHI
mega-edges are the single-source artifact shape (NBM 0.01). The six open Jul-14
positions already hold the board's real dual-source edges, and the market has drifted
TOWARD every one of them since entry (DEN T93 0.10→0.12, AUS T85 0.55→0.71, SATX T85
0.57→0.70, DAL T88 0.28→0.36) — R5c says that's confirmation, not a missed add. Wide
venue scan skipped: weather-only mandate makes it context-only and model-view covers
all weather events.

**Want to learn by next session:** tonight's Jul-14 cohort is a direct test of the
NBM-confirmation hypothesis — all six open positions carry NBM support, unlike the
Jul-13 losers. If they win where Jul-13 lost, v3 makes NBM agreement a hard R1
requirement. Also start tracking R5 vetoes (today: DEN B93.5 NO) to test whether the
veto rule itself pays.

## 2026-07-14 10:16 UTC — nothing settled, no qualifying edge, holding 15 positions

Same 08:23 snapshot the 09:16 session traded on (now 112 min stale) — no new
information. Same artifact-shaped edges (extreme model_p, NBM 0.01) and same passed
correlated fades (DEN B93.5 NO, AUS/SATX B85.5). The 15 Jul-13/Jul-14 positions
remain open; the nine Jul-13 CLI settlements are still the next learning event.

## 2026-07-14 09:16 UTC — nothing settled; opened 1 R2 trade (Dallas T88 YES), holding 15

**Settlements:** none — nine Jul-13 positions still await CLI settlement (next learning
event). **Strategy:** unchanged (v1); nothing settled to grade against.

**Trade opened:** KXHIGHTDAL-26JUL14-T88 YES x40 @ $0.28 (fee $0.57, cost $11.77), R2.
Fresh 08:23 snapshot finally showed a candidate with a different shape from the
overnight artifacts: model_p 0.68 AND nbm_p 0.90 both far above the market's 0.28 —
dual-source agreement, verified live (bid 0.27/ask 0.28, vol24h 3,055). My p~0.75.
Dallas/high cell record is weak (54% win, −0.6% ROI, n=134), hence R2 small size.
This is a direct test of the hypothesis I've been building all night: the artifact
shape (extreme model_p, NBM 0.01) is fake, but dual-source divergence from the market
may be real. Passed again on DEN B93.5 NO (NBM 0.20 against) and the AUS/SATX bin
fades (correlated with held views).

**Want to learn next session:** do the Jul-13 settlements land, and does the
dual-source-agreement filter (this trade) beat the single-source artifact shape I've
been passing on?

Third session on the 05:58 snapshot (138 min stale) — same artifact-shaped edges
(extreme model_p, NBM 0.01) in negative-ROI cells, same passed correlated fades
(DEN B93.5 NO with NBM 0.20 against; AUS/SATX B85.5). Nine Jul-13 positions still
await CLI settlement — the next learning event.

## 2026-07-14 07:17 UTC — nothing settled, no qualifying edge, holding 14 positions

Same 05:58 snapshot the 06:16 session already reviewed (now 78 min stale) — no new
information; same artifact-shaped edges and same passed correlated fades. Nine Jul-13
positions still await CLI settlement.

## 2026-07-14 06:16 UTC — nothing settled, no qualifying edge, holding 14 positions

Fresh 05:58 snapshot, same overnight board: artifact-shaped edges (extreme model_p,
NBM 0.01 — LAX T81 +0.90, SFO T81 +0.78, CHI T101 +0.69) in negative-ROI cells, and
the same passed correlated fades (DEN B93.5 NO — NBM 0.20 against; AUS/SATX B85.5).
Nine Jul-13 positions still await CLI settlement — the next learning event.

## 2026-07-14 05:15 UTC — nothing settled, no qualifying edge, holding 14 positions

Same 03:38 snapshot the 04:16 session reviewed (now 97 min stale) — same
artifact-shaped overnight edges (extreme model_p with NBM at 0.01), same passed
SATX B85.5 correlated fade. Nine Jul-13 positions still await CLI settlement.

## 2026-07-14 04:16 UTC — nothing settled, no qualifying edge, holding 14 positions

Fresh 03:38 snapshot at last, but the overnight board is full of artifact-shaped
"edges" (model_p extreme with NBM at 0.01: LAX T81 +0.91, CHI T101 +0.79, DEN low
T62 +0.71) — no NBM confirmation anywhere, all in negative-ROI cells. Only R1-cell
candidate is SATX B85.5 NO, a correlated add-on to my held SATX T85 YES with NBM
neutral (0.22 vs mid 0.24); passed. Nine Jul-13 positions still await CLI settlement.

## 2026-07-14 03:16 UTC — nothing settled, no qualifying edge, holding 14 positions

Snapshot still 00:10 (185 min stale) — fourth session on this exact board. Same
passed candidates (correlated Jul-14 bin-fades; DEN B93.5 NO with NBM 0.23 against).
Nine Jul-13 positions await tonight's CLI settlements — next learning event.

## 2026-07-14 02:15 UTC — nothing settled, no qualifying edge, holding 14 positions

Still the same 00:10 snapshot (125 min stale) reviewed at 00:15 and 01:15 — no new
data, same passed candidates (correlated Jul-14 bin-fades; DEN B93.5 NO with NBM
0.23 against). Nine Jul-13 positions await tonight's CLI settlements — next learning
event.

## 2026-07-14 01:15 UTC — nothing settled, no qualifying edge, holding 14 positions

Same 00:10 snapshot the 00:15 session already reviewed (now 65 min stale) — no new
data, same unheld candidates (correlated Jul-14 bin-fades, still passing). Nine
Jul-13 positions await tonight's CLI settlements; that's the next learning event.

## 2026-07-14 00:15 UTC — nothing settled, no qualifying edge, holding 14 positions

Fresh 23:15 snapshot, same board as the last four sessions: unheld candidates remain
the correlated Jul-14 bin-fades (DEN B93.5 NO — NBM 0.23 says pass; AUS/SATX fades =
3rd expressions of held views). Tonight's 9 Jul-13 settlements remain the next
learning event.

## 2026-07-13 23:20 UTC — nothing settled, no qualifying edge, holding 14 positions

Fresh 22:11 snapshot (the prior session's "23:16" entry actually ran at 22:16 UTC —
timestamp was mislabeled; this is the real 23-hour run). Same board: unheld
candidates are still the correlated Jul-14 bin-fades (DEN B93.5 NO — NBM 0.23 says
pass, as at 18:16/20:16/22:10; AUS/SATX bin fades = 3rd expressions of held views).
Tonight's 9 Jul-13 settlements remain the next learning event.

## 2026-07-13 23:16 UTC (mislabeled — actually ran 22:16 UTC) — nothing settled, no qualifying edge, holding 14 positions

Snapshot still 21:03 (no fresh data since the 22:10 session reviewed this exact
board). Tonight's 9 settlements remain the next learning event.

## 2026-07-13 22:10 UTC — nothing settled, no qualifying edge, holding 14 positions

Same board as 20:16 (21:03 snapshot): only unheld candidates are still correlated
bin-fades of held Jul-14 views; DEN B93.5 NO still passed (NBM 0.23). Tonight's 9
settlements remain the next learning event.

## 2026-07-13 20:16 UTC — nothing settled, no qualifying edge, holding 14 positions

Fresh 19:51 snapshot but same board. Only unheld candidates (DEN Jul14 B93.5 NO,
AUS/SATX bin fades) are 3rd/4th correlated expressions of the Jul-14 views already
held — and B93.5 was already passed at 18:16 in favor of B95.5 (NBM gives B93.5 a
real 0.24). Tonight's 9 settlements remain the next learning event.

## 2026-07-13 19:16 UTC — nothing settled, no qualifying edge, holding 14 positions

Same 18:02 snapshot as last session — board unchanged, nothing new clears the bar
(NOLA/low B72.5 edge +0.10 noted but passed: NBM 0.14 disagrees with ECMWF 0.49,
prices 73 min stale). Tonight's 9 settlements are the next real learning event.

## 2026-07-13 18:16 UTC — nothing settled; reconciled the 16:17 orphan session; opened 2 (DEN R1, BOS R2)

**Housekeeping first:** the 16:17 session opened 3 trades but was interrupted before
journaling/committing — the ledger changes were sitting uncommitted in the working
tree. Reconciled here; those trades are recorded retroactively below. Strategy stays
**v1** (nothing settled since 15:20; all 14 positions still open — 9 on today's
markets settling tonight, 5 on Jul 14).

**Retroactive record of 16:17 UTC (3 opened, $79.35):** the model's Jul-14 board
lit up with the same cool-TX/CO regime as Jul 13, and this time NBM agrees:

1. **KXHIGHDEN-26JUL14-T93 YES ×150 @ $0.10** (R1) — model 0.95, NBM 0.70, market
   0.10. Denver/high 91%/+24.5%/n=362. Same setup as the Jul-13 DEN T93 but with NBM
   on side this time.
2. **KXHIGHAUS-26JUL14-T85 YES ×60 @ $0.55** (R1) — model 0.95, NBM 0.45, market
   0.53. Austin/high 89%/+27.1%/n=331.
3. **KXHIGHTSATX-26JUL14-T85 YES ×50 @ $0.57** (R1) — model 0.95, NBM 0.38, market
   0.53. San Antonio/high 96%/+30.8%/n=132. Correlated with the AUS leg (same air
   mass), sized smaller.

**This session — read of the board (18:02 snapshot, 14 min old):** no R3 candidates
in the wide scan (WTI/BTC/gold books closing today are efficient; no informational
edge). The giant single-model edges (LAX T81 +0.90, SFO T81 +0.78, CHI T101 +0.77)
all have NBM at 0.01 flatly contradicting — the disagreement pattern, skipped again.

**Opened 2 ($42.07; ~$327 at risk, ~$673 cash):**

1. **KXHIGHDEN-26JUL14-B95.5 NO ×40 @ $0.59** (R1) — my est P(95-96°) ~0.10 vs market
   0.41. Strongest dual-model bin rejection on the board (ECMWF 0.01, NBM 0.05); both
   models put the high ≤92. Second expression of the DEN T93 view — knowingly
   correlated, combined DEN Jul-14 risk ~$40.
2. **KXHIGHTBOS-26JUL14-B94.5 YES ×50 @ $0.34** (R2, small) — **process miss, logged
   honestly:** snapshot showed 0.19/0.20 with dual-model agreement (ECMWF 0.47, NBM
   0.36) = edge 0.28. Live fill came at 0.34 — the book had repriced toward the models
   in the 14 min since the snapshot. At the fill my edge is ~0.06, BELOW R2's 0.15
   bar; I'd have passed had I checked the live book first. Still marginally +EV under
   my estimate, but the lesson is the rule the model-view header already states:
   re-check live prices before pulling the trigger on any bin whose snapshot edge
   looks like free money. Fourth dual-agreement-on-weak-cell test either way.

**Want to learn by next session:** tonight's settlements (9 positions) — the T-strike
YES vs modal-bin NO comparison, three dual-agreement tests, and whether the market's
overnight repricing of my cheap T-strikes was information. If several R2 tests fail
together, v2 should raise R2's bar or kill it early. Also: adopt "verify live book
before entry" as an explicit rule candidate for v2.

## 2026-07-13 15:20 UTC — nothing settled, no qualifying edge, holding 9 positions

Nothing settled; no qualifying edge (only candidates: a third correlated Seattle leg
— skipped for concentration — and an SFO fade where NBM's edge 0.11 < R2's 0.15 bar).
Holding 9 positions (~$206 at risk); everything settles tonight.

## 2026-07-13 14:20 UTC — nothing settled; added 1 small R2 (Seattle B80.5 NO)

**Settled:** nothing — all 8 positions are today's markets, ~15-18h to close. Strategy
stays **v1**.

**Read of the board (snapshot 67min stale, verified live via agent-scan):** the model
view is dominated by 6h-lead lows (SEA/LAX/LV) where the low is already observed at
7am local — all skipped per the staleness trap. LAX high T76 skipped again (ECMWF 0.95
vs NBM 0.01, the disagreement pattern). Wider venue scan (WTI, BTC, CPI, Netflix,
cricket): nothing where I have an R3-grade estimate that beats the market's.

**Opened 1 ($22.63; ~$206 at risk, ~$794 cash):**

1. **KXHIGHTSEA-26JUL13-B80.5 NO ×35 @ $0.63** (R2, small) — my est P(80-81°) ~0.05
   vs market 0.37. Both models reject the bin outright (ECMWF+biascorr 0.01, NBM 0.01)
   and put the high at 76-79. Live book confirmed 0.36/0.38 before entry. Knowingly
   correlated with my B76.5 YES — both lose if Seattle runs hot; sized small for that
   reason. Third dual-model-agreement data point on a weak cell.

**Want to learn by next session:** tonight settles everything — the whole v2 dataset
arrives at once (T-strike YES vs modal-bin NO, three dual-agreement tests on weak
cells, whether the market's overnight moves were information).

## 2026-07-13 13:20 UTC — nothing settled; opened 1 small R2 (Seattle dual-model)

**Settled:** nothing — all 7 positions are today's highs, still open. Strategy stays
**v1** (no settled evidence).

**Read of the board (13:08 snapshot, fresh):** no R1 candidates — the proven cells
(AUS/DEN/SATX high) show no new edges beyond the positions I already hold. The big
rows are all 6h-lead lows (LV/LAX/SEA), where the low is already largely observed at
6am local and the model is stale — skipped per the lead-floor warning. Skipped LAX
T76 YES (model 0.95) because NBM at 0.01 flatly contradicts — the Chicago-artifact
pattern.

**Opened 1 ($11.04; ~$183 at risk, $816 cash):**

1. **KXHIGHTSEA-26JUL13-B76.5 YES ×80 @ $0.13** (R2, small) — my est ~0.50 vs 0.13.
   Corrected ECMWF (0.77) AND NBM (0.49) both put Seattle's high at 76-77°; the market
   modal is 78-81, which both models price 0.01-0.20. High not yet observed at 6am
   local, so the 6h-lead staleness trap doesn't apply. Second data point (with MIA
   B92.5) on whether dual-model agreement rescues weak cells (Seattle/high: 55%,
   -1.2%, n=128). Also the only position not riding today's TX/CO/FL air mass.

**Want to learn by next session:** everything settles tonight — the T-strike-YES vs
modal-bin-NO comparison, the MIA and SEA dual-agreement tests, and whether the
overnight market move against my T-strikes was information. That's the v2 material.

**Settled:** nothing (all 4 positions are on today's highs, ~17-18h to close).
Strategy stays **v1** — no settled evidence to act on yet.

**Read of the board:** overnight the market moved hard against my three cheap-YES
T-strikes (DEN T93 7¢→1.5¢, AUS T89 17¢→2¢, SATX T90 34¢→3¢) — the books now think
all three cities blow past the strikes. The ensemble hasn't budged (still 0.94-0.95),
so either the bias correction is having an artifact day across TX/CO or the model is
about to look brilliant. Rather than average down on the same strikes (duplicates are
blocked anyway), I took the OTHER expression of the model's view that stays +EV even
if the ensemble is ~half wrong: NO on each event's market-modal bin, where NBM ALSO
prices the bin well below the market. Verified live books first (snapshot was 140 min
stale).

**Opened 3 (total new cost $97.68; ~$172 now at risk, $827 cash):**

1. **KXHIGHDEN-26JUL13-B97.5 NO ×60 @ $0.50** (R1) — market P(97-98)=0.50 vs ensemble
   0.01 / NBM 0.22; my estimate ~0.15. Cell: 91% win, +24.5%, n=356. Also hedges shape:
   pays on 93-96, where my T93 YES loses.
2. **KXHIGHAUS-26JUL13-B93.5 NO ×50 @ $0.66** (R1) — market P(93-94)=0.345 vs ensemble
   0.01 / NBM 0.05; my estimate ~0.08. Strongest dual-model agreement on the board.
3. **KXHIGHTSATX-26JUL13-B92.5 NO ×55 @ $0.58** (R1) — market P(92-93)=0.44 vs ensemble
   0.01 / NBM 0.21; my estimate ~0.15. Best cell (96%, +31%, n=126).

**Known concentration:** all 7 open positions are same-day TX/CO/FL heat. The modal-bin
NOs lose only if the exact modal bin hits, so they're anti-correlated with each other
across most outcomes, but a "market was exactly right" day hits all three at once.
Tomorrow's settlements are one big lesson on ensemble-vs-market day-of trust.

**Want to learn by next session:** today everything settles — (a) T-strike YES vs
modal-bin NO: which expression of the same model view actually paid; (b) whether the
overnight market move was information or noise; (c) v2 likely needs a rule about how
to size when ensemble and NBM disagree by >0.5.

## 2026-07-13 00:16 UTC — nothing settled, no qualifying edge (same 23:10 snapshot; remaining R1 rows are complements of held positions), holding 4 positions.

## 2026-07-12 23:45 UTC — first session

**Settled:** nothing (empty book — this is session one). Strategy stays **v1**.

**Read of the board:** model-view (snapshot 23:10 UTC, 33 min old) shows a cluster of
cheap-YES T-strikes on tomorrow's highs where the corrected ECMWF is emphatic. The
production trader's recent run of winning cheap-YES SATX T-strikes says this shape is
where the model's edge currently lives. Deliberately skipped the single biggest "edge"
on the board — Chicago T94 (+0.81) — because Chicago/high is the model's worst cell
(51% win, −2.0% ROI, n=362) and NBM at 0.01 flatly contradicts the 0.95; that row is
almost certainly a bias-correction artifact, exactly what R2's skepticism is for.

**Opened 4 (all fills better than or near snapshot; $74.82 at risk, $925.18 cash):**

1. **KXHIGHDEN-26JUL13-T93 YES ×150 @ $0.07** (R1) — model 0.95 vs mid 0.05 that Denver
   stays ≤92°. NBM disagrees (0.11); trusting the cell record (91% win, +24%, n=356)
   and the 13:1 payout asymmetry. This is also a clean NBM-vs-ECMWF experiment.
2. **KXHIGHAUS-26JUL13-T89 YES ×100 @ $0.17** (R1) — model 0.95 AND NBM 0.64 vs mid
   0.21 that Austin stays ≤88°. Dual-model agreement on an 89%-win cell.
3. **KXHIGHTSATX-26JUL13-T90 YES ×100 @ $0.34** (R1) — model 0.95 + NBM 0.54 vs mid
   0.30. Best cell in the book (96%, +31%, n=126); prod holds this same market @30¢.
   **Known correlation:** Austin+SAT share tomorrow's air mass — trades 2 and 3 are
   ~one bet sized twice. Accepted; if both lose to the same warm surprise I will add
   a correlation rule to v2.
4. **KXHIGHMIA-26JUL13-B92.5 YES ×30 @ $0.32** (R2, small) — the only board row where
   BOTH models sit above market (0.66 / 0.45 vs 0.27) on a bad-record cell (47%,
   −5.5%). Testing whether dual-model agreement rescues weak cells.

**R3 (non-weather):** nothing cleared the 0.10 own-estimate bar this hour — CPI-core
>0.1% at 89¢ is only ~5¢ cheap by my estimate; passed. No [explore] this session.

**Want to learn by tomorrow:** (a) does the Denver ECMWF-vs-NBM split resolve for the
cell record or for NBM — that decides whether v2 adds an NBM-agreement filter to R1;
(b) does the Miami dual-agreement test land; (c) first data point on AUS/SAT correlation.
