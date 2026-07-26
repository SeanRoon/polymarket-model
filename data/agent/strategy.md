# Agent strategy playbook

**Version: v21** (2026-07-26 23:15 UTC — **nothing settled. Two changes, and the first is a partial RETRACTION of my own v19 evidence: R15 → R15′ (robustness), and new R17 (operational definition of R2's 19-version-old correlation clause).** The 22:40 snapshot produced **6** mechanical candidates and exactly one survived every geometry/price/liquidity gate: **`KXHIGHTPHX-26JUL27-B113.5`** (PHX high 113–114°F) — non-modal (market mode B111.5 @0.485), both sources at their floors vs mid 0.205, **AGREEMENT** with model mode *and* NBM mode both on B109.5 ⇒ d=2 from both (i″ ✓), bias only **−2.22°F** (ii′ ✓), live book **bid 0.21 / ask 0.23, vol24h 803, OI 557** — the deepest book in the event, so R14 ✓ and the bid moved *up* 0.19→0.21 rather than decaying — NO entry **0.79** ≤ (iii′)'s 0.85 ✓, live edge **0.17** ≥ 0.15 ✓. **I did not trade it, and auditing why produced the session's real finding.** Before entering I re-ran R15 across *every* snapshot cycle of the day instead of the one my session happened to load, and **R15's reconstruction is not stable within a day — it swings 2–4× as NBM cycles update.** Per-market (min / median / max / fraction of cycles above the 0.05 bar): **MIA B96.5 W → 0.0000 / 0.0006 / 0.0009 / 0.00; HOU B95.5 W → 0.0172 / 0.0342 / 0.0409 / 0.00; LAX B79.5 W → 0.0206 / 0.0364 / 0.0532 / 0.27; DEN T101 W → 0.0423 / 0.0732 / 0.0849 / 0.83; MIA B93.5 L → 0.0090 / 0.0104 / 0.0165 / 0.00; open LV B111.5 → 0.0215 / 0.0715 / 0.0804 / 0.86; PHX B113.5 cand → 0.0337 / 0.0608 / 0.0608 / 0.62; DC T70 → 0.0839 / 0.0975 / 0.1542 / 1.00.** **Two defects follow. (1) v19's validation table is partly WRONG:** it reported one cycle per trade and gave DEN as **0.0232**, a value that appears *nowhere* in that day's actual range (0.0423–0.0849), and my open LV position as **0.0216** when the day's median is **0.0715** — I entered LV on the single lowest cycle of the day and recorded that lucky draw as if it characterized the market. **(2) A hard 0.05 line read off one arbitrary snapshot is therefore part coin-flip** for any candidate sitting in the 0.03–0.08 band. **What I am NOT claiming:** R15 never promised to separate wins from losses — v19 said so in bold — so "it admits the loss (0.0104, never above the bar) and would veto the DEN win (0.83 above)" is not a refutation of its stated purpose, and I am not repeating (i)'s overreach in reverse. Its founding case is **robust**: DC T70 is above 0.05 on **100%** of cycles and has been for three straight sessions. **Fix: R15′ requires the exceedance to be CONSISTENT (>0.05 on ≥80% of the day's cycles), not merely present on the cycle I happened to read.** R15′ admits all three clean wins and the loss, still rejects DC, and **admits today's PHX candidate at 0.62** — so it is *not* what blocked the trade. **What blocked it was R17.** My one open position is **LV high B111.5 NO**, and PHX B113.5 is its structural twin: same kind (high), same settlement date, same desert-southwest ridge, and — the tight part — **each fades the bin exactly ONE ABOVE its own market's mode** (LV mode 109–110, faded 111–112; PHX mode 111–112, faded 113–114), so **a single shared +2°F regional warm bust breaks both positions simultaneously and exactly.** That is ~2× the dollar variance for ~1 independent observation, which is strictly bad for a subset (4W–1L, +$0.36, n=5) whose entire present job is accumulating *independent* settlements against a kill clock. And the R15′ audit makes it worse: fresh NBM has quietly moved my LV position from a 0.02 tail to a **0.07** tail, so I would be stacking a correlated bet on top of a position that today's guidance has *weakened*. **R17 states the mechanism, not a fitted gate** — I have only n=2 same-session pairs (JUL22 AUS+TLV, correlated, both LOST together; JUL23/24 AUS+PHIL, explicitly different air masses, split 1W–1L) and I am explicitly NOT claiming that discriminates. **R16 self-check applied to R17:** the clause is 19 versions old, its definition references only date/kind/air-mass/side-of-mode (nothing specific to this candidate's geometry), it is a *deferral* that expires when LV settles tomorrow, and it ships with a tripwire — if R17 is the sole blocker on ≥3 consecutive sessions, my correlation classes are too wide and must narrow. **Full adjudication of all 6: PHX B113.5 → R17 (correlated with open LV); DC low T70 → R15′, 100% of cycles above bar, third straight session; LAX high B81.5 → BRACKET** (model mode T86 @0.935 *hot* vs NBM mode T79 @0.995 *cold*, faded bin the shoulder — sixth refusal) + bias +3.48; **SFO low T59 → (iii′)**, nbm 0.0608 > 0.05 and reconstruction **0.1425**; **AUS high B100.5 → quadruple veto** (bias **+12.26**, model at the 0.0093 floor, R15′ 0.0743, and vol24h **16.9 < 25** = R14); **LV B111.5 → my own open position**, duplicate guard. **No trade opened.** Holding 1. --- prior v20 note: (2026-07-26 22:15 UTC — **nothing settled. One change, and it is a rule that FORBIDS a rule: R16. The fresh 21:41 snapshot re-ran the full v19 chain and produced 7 candidates, of which exactly one was live — `KXLOWTOKC-26JUL27-B73.5` (OKC low 73–74°F), which cleared every gate I have: non-modal, both sources ≥0.10 below the mid, R15-verified (NBM's own quantiles put q10 at 77.14, so the reconstruction is 0.0022 — the bin is genuinely empty under NBM, not a discretization artifact), (i″) 2 bins from both source modes, spread 0.03, vol 277, snapshot bid 0.17 ⇒ NO entry 0.83 ≤ (iii′)'s 0.85 cap.** What made me hesitate was geometry my qualifiers have never measured: the sources put the low at 77–78 while the *market's* mode is 75–76, so the faded bin sits **immediately adjacent to the market's own center** even though it is far from both forecasts'. I started writing a qualifier for it — and then measured it, which is the whole lesson of v18. **Distance to the market's modal bin across every settled AGREEMENT trade plus my open position: MIA B96.5 W → 1, HOU B95.5 W → 1, LAX B79.5 W → 1, DEN T101 W → 1, MIA B93.5 L → 1, open LV B111.5 → 1. Constant at 1. Zero variance, zero discriminating power, and a ≥2 gate would have vetoed 4W–1L — the entire subset.** So **R16 records the hypothesis as tested and REJECTED**, permanently, so that a future session tempted by the same optics does not re-derive it: adjacency to the market's mode is the *normal shape* of my winning fades, not a defect. R16 also logs the one metric that *did* separate the loss from the wins — source-vs-market displacement (3W at 0, 1L at 1, 1W at 4) — explicitly as an unpromoted hypothesis, because n=5 with that split is precisely what (i) was built from. **Then the market settled the question anyway: R14's live check killed OKC B73.5 on its own.** Live book at 22:18 quoted **0.13 / 0.19** against the snapshot's 0.17 bid — so the real NO entry is **0.87, above (iii′)'s 0.85 cap**, and R2's ≥0.15 edge bar is *mechanically unreachable* since a NO-fade's maximum edge is the bin's own price (0.13). It independently fails **(ii′)'s surviving bias half** at `model_bias_applied_f` **+4.96°F** — larger than the −3.93 Miami bias I have refused five times. Second live firing for R14 and it fired the same way as the first: the snapshot's price side decayed and manufactured a phantom edge. **Full adjudication of all 7: OKC low B73.5 → R14 live decay + (iii′) + (ii′) bias; DC low T70 → R15 again** (fresh quantiles q50 68.52 / q90 70.36 ⇒ 0.0839 > 0.05, vs 0.098 last session — same verdict, and the second consecutive session this candidate is the funnel's best-looking and the input check's only casualty); **AUS high B100.5 → triple veto** (bias +12.26, degenerate model column at the 0.0093 floor under a 0.95 mode = R8/R10, and R15 0.0789); **DC high B89.5 → BRACKET** (model mode b4 warm vs NBM mode b0 cool, faded bin the shoulder) + bias −3.41; **NYC high B83.5 → (iii′)** (mid 0.295 < 0.30 so the emptiness test applies and NBM is 0.153, R15 0.177) + adjacent to the model's mode; **AUS high B98.5 (JUL26) → R5a settlement-day, lead 0**; **MIA high B93.5 → disqualified cell**, sixth refusal. **What binds now: R14 1, R15 1, BRACKET 1, (iii′) 1, degenerate 1, disqualified 1, R5a 1 — seven candidates, seven different reasons, no single gate starving the funnel.** **No trade opened.** Holding 1. --- prior v19 note: (2026-07-26 21:15 UTC — **nothing settled, but a fresh 20:30 snapshot produced two candidates I had never seen, and chasing the better of them turned up a genuine defect in one of my INPUTS. Two changes: new R15 (validate `nbm_p` against NBM's own quantiles) and (ii) → (ii′) (demote the cell-record veto to a tiebreaker). Neither produces a trade today — which is the reason I trust them.** The 10-candidate mechanical sweep (non-modal ∧ both sources ≥0.10 below mid ∧ `yes_bid` ≥0.15 ∧ spread ≤0.10) surfaced **KXLOWTDC-26JUL27-T70** (DC low ≥71°F, mid 0.320, bid 0.30, spread 0.04, **vol 613**, bias +1.04°F): model 0.028, NBM **0.0056**, gap 0.292, clean **AGREEMENT** geometry (model mode B65.5 → d=3, NBM mode B67.5 → d=2, faded bin above *both*, neither column degenerate), mid ≥0.30 so (iii′) needs no emptiness test and the NO entry is 0.70 ≤ 0.85. On paper it was the best candidate to clear the funnel in nine sessions, and under (ii) alone it died only because DC/low is a −2.1% cell — a number I had already measured as non-discriminating. **So I checked the input instead of the gate, and the input is broken.** NBM's quantiles for that market are q50 **68.70**, q90 **70.48** ⇒ σ = (q90−q50)/1.2816 = **1.39**, so NBM's own distribution implies P(low ≥ 70.5) = **0.098** — but the binned `nbm_p` the screen reads is **0.0056**, an understatement of **17×**. The discretization is clipping a tail that NBM plainly puts ~10% on, and R2's "both sources ≥0.10 below the mid" test was being satisfied by a number that is simply wrong. Read correctly the market's 0.32 vs NBM's ~0.10 is a **0.22** gap, not 0.31, and it is the market pricing overnight-low risk (urban heat island / dewpoint floor at KDCA) that gridded guidance chronically under-does, with **q90 sitting 0.5°F under the threshold** — i.e. the faded bin is one ordinary error away, which is the MIA B93.5 structure verbatim. **Change (a): R15 (NBM binned-probability validity check)** — before counting `nbm_p ≤ 0.05` as a vote, reconstruct P from q50/q90 and require the reconstructed value ≤0.05 too. **I validated it against every settled AGREEMENT trade plus my open position before adopting it, which is the step v17 skipped for (i): MIA B96.5 W → 0.0045; HOU B95.5 W → 0.0347; LAX B79.5 W → 0.0410; DEN T101 W → 0.0232; MIA B93.5 L → 0.0194; open LV B111.5 → 0.0216.** R15 admits **all six** and rejects **exactly one** thing — today's DC candidate. **I am explicit that R15 is an INPUT-VALIDITY check, not a win/loss discriminator: it admits the loss too, and I have not shown it separates winners from losers.** That is precisely the claim v17 overreached on, and I am not repeating it. What R15 does is stop a specific class of *false positive* from entering the funnel, without narrowing the funnel's price band the way (i) did. **Change (b): (ii) → (ii′).** I finally measured (ii)'s cell-record half against my own ledger instead of re-asserting it: **all 39 settled — negative-ROI cells 8W–9L, −$7.71; positive-ROI cells 10W–12L, −$135.78. NO-fades only (the half (ii) governs) — negative-ROI cells 6W–3L, 67%, +$5.02; positive-ROI cells 7W–6L, 54%, −$73.86.** The cells (ii) bans have been my *best* book and the cells it blesses hold essentially all of my −$143. **Confound stated honestly:** much of the positive-ROI damage is the retired ≥24h modal-fade carve-out (AUS ×2, TLV — all in positive cells) and v1 model-piggyback YES longshots, both already banned by R5a/R7, and n=9 on the NO-fade split is small. So this is a demotion, not a deletion: **the bias half of (ii) STANDS** (mechanistic, and it is what actually explains the MIA loss and R9's Denver diagnosis), **the cell-record half becomes a tiebreaker rather than a veto**, and **Miami/high stays disqualified outright** (direct settled loss at this exact bin, and its −4 to −7°F bias disqualifies it under the surviving half anyway). Structural reason to act now: **(ii) has vetoed ~50 candidates and admitted about one**, which is the learning-blocker pattern v18 retired (i) for — except this time I have a measurement pointing against the gate, where v17 had none for (i). *Kill clause: if the next ≥6 AGREEMENT settlements admitted in negative-record cells run below their entry-implied win rate, the record veto comes back as a hard gate.* **Sweep for the record, all 10 candidates: LV B111.5** = my own open position (duplicate guard); **DC low T70** → **R15** (nbm_p 0.0056 vs quantile-implied 0.098) — the first R15 veto and the reason it exists; **NYC high B83.5** (mid 0.255, vol 5022, the board's deepest book) → **BRACKET** — model mode B85.5 @0.398 *warm*, NBM mode T81 @0.665 *cool*, faded bin 83–84 is the shoulder between them, the SFO B61.5 shape that lost −$28.59; **DC high B89.5** → **BRACKET** (model mode B93.5 @0.343 vs NBM T87 @0.860, faded bin the shoulder) + bias −3.41; **MIN high B95.5** → the model column is **flat** (0.083–0.232 across all six bins) and B95.5 is its *second-highest* bin, so the model is agnostic, not rejecting — its 0.102 gap is diffuseness, not a vote (**R8/R10 in spirit**); **MIA high B93.5** → disqualified cell + bias −3.93, fifth session refusing the bin that settled −$23.77; **DEN B97.5 / B93.5** → **R9**, bias +13.39, model at the 0.0093 floor; **LAX high B81.5** → **BRACKET** (model ≥87°F vs NBM ≤78°F), fourth refusal; **SFO low T59** → **(iii′)**, NBM 0.0648 > 0.05 at mid 0.195. **Note the shift in what binds: BRACKET geometry now vetoes 3 and R15 vetoes 1, while (ii)-as-record vetoes 0 — demoting it did NOT open the floodgates, exactly as retiring (i) did not.** Position health: LV B111.5 NO @0.70 drifted 0.30 → 0.32 yes (0.02 adverse, *improved* from 0.025 last session), thesis and AGREEMENT geometry intact, and it now clears R15 as well. **No trade opened.** (ii) tally frozen at 44; new R15 tally 1. Holding 1. --- prior v18 note: (2026-07-26 15:15 UTC) **nothing settled, and I have to retract last session's headline. v17 declared qualifier (i) "OUT-OF-SAMPLE CONFIRMED." It is not. I tested it against the one AGREEMENT loss and never against the four AGREEMENT wins, and when I measure the wins today (i) would have VETOED THREE OF THE FOUR.** I pulled every settled AGREEMENT trade and measured the faded bin's bin-distance to both sources' modes in the snapshot nearest its entry: **MIA B96.5 W +$7.97 → d_model=1, d_nbm=4; HOU B95.5 W +$5.51 → d_model=1, d_nbm=2; LAX B79.5 W +$4.42 → d_model=1, d_nbm=4; DEN T101 W +$6.23 → d_model=5, d_nbm=5; MIA B93.5 L −$23.77 → d_model=2, d_nbm=2.** (i) requires ≥3 from **both**, so it admits exactly **one** of the five — DEN — and blocks 3W–1L. Worse, `min(d_model, d_nbm)` is if anything **anti**-correlated with winning in my ledger: the three trades with the *smallest* separation all won. **So (i) does not discriminate wins from losses; it is the same failure (iii) was retired for in v15, and I made it by fitting a gate to a single loss and then "confirming" it against that same loss.** The MIA B93.5 veto v17 celebrated is real but it is one true positive alongside three false ones. **Second finding, structural: (i) and R2's ≥0.15 live-edge bar are very nearly DISJOINT.** For a NO-fade the maximum possible edge is the bin's own price, so R2 needs mid ≳0.15; but ≥3 bins from both modes on a 6-bin board *is* the outer tail, and I queried every such bin on the JUL27 board — **all 27 of them are priced ≤0.075**, top of range PHIL low T61 at 0.075. Not one can ever clear 0.15. **That, not the clock and not the market, is why my funnel ends at 0: (i) forces me into a price band where R2 forbids me to trade.** R12 explained *when* to look; this explains why looking could not have helped. **Changes (v18): (a) RETIRE (i), replace with (i″)** — the faded bin must be ≥2 bins from **at least one** non-degenerate source's mode, and must not be adjacent to **both** modes. I am explicit that (i″) admits all five settled trades including the loss: it is not pretending to discriminate, because **at n=5 nothing in my ledger discriminates**, and the honest read is that (i) was not a safety rule but a *learning blocker* — it made collecting the settlements I need to evaluate this subset impossible. Protection comes from what actually bounds loss: (iii′)'s ≤0.85 entry cap, de-scaled 1-per-session size, the $50/trade guard, and the subset's live kill clock (kill at losses−wins=+2 or net −$40; currently −3 and +$0.36). **(b) New R14 (fade the BID, not the mid; require a real book)** — earned today. Three candidates cleared everything except price on the 14:10 snapshot; all three evaporated at the live book: **DAL high B105.5 bid 0.14 → 0.04, NOLA high B99.5 0.13 → 0.01, LV high B113.5 0.08 → 0.04**, and all three had **vol24h ≤ 6, OI ≤ 7**. Snapshot `mid` on a wide tail book (NOLA B99.5 quoted 0.01/0.08 live but carried mid 0.165) systematically inflates the apparent edge on exactly the illiquid bins a tail-seeking qualifier steers me into. **(c) No trading bar was loosened except (i)→(i″); (ii), (iii′), R5a, R8, R9, R10, R12, R13 all stand.** **No trade opened.** Re-running the full v18 chain over all 17 non-modal both-sources-≥0.10-below candidates yields **zero**: the binding constraints are now (iii′)'s entry cap and R2's edge bar — i.e. price and spread, not geometry. Vetoes: MIA high B93.5 → (iii′) model 0.083 > 0.05 + (ii) Miami/high 47%/−5.1%; PHX high B113.5 → (iii′) model 0.102 > 0.05; BOS high B78.5 and MIN high B93.5 → (i″) adjacent to both modes (1/1); AUS high B100.5 → (ii) bias +11.39 + R8/R10 degenerate; LAX high B81.5 → BRACKET + (ii); OKC low B75.5 → edge 0.077 < 0.15; HOU low T79/B72.5, SFO low T59/B54.5/B52.5, LV low B82.5, OKC high T99, LV high B113.5, DAL high B105.5, NOLA high B99.5 → **R14** (NO entry 0.86–0.99 on a wide/dead book). **Relaxing the overfitted gate did NOT open the floodgates — which is the most reassuring thing I learned today.** (ii) tally 23. Holding 0. --- prior v17 note: (2026-07-26 14:15 UTC) **nothing settled, but R12 paid off on its first firing and the sweep it unlocked answered the question I pre-registered last session — decisively, and in favor of my rules.** This is the first session in a week to run inside the R12 window, and the JUL27 board was live (26–29h lead, 36 events) exactly as R12 predicted. **R12 CONFIRMED, with one operational amendment (see R12): the BOARD opens at ~14:00 but the MODELED SNAPSHOT lags it by one cron cycle.** At 14:16 the JUL27 book was quoting on Kalshi while the newest committed snapshot (1215.parquet) contained **zero** JUL27 rows; I only got `model_p` because a second `git pull` mid-session brought down 1410.parquet (216 JUL27 rows, 36 events). Without that re-pull this session would have falsely reported "board open but no model coverage" and become a seventh empty session for a purely mechanical reason. **The pre-registered question was: does a ≥24h board produce a candidate clearing (i)/(ii)/(iii′), or are my qualifiers now so tight that even a good board yields nothing?** I answered it by encoding the entire v16 chain as one query over the 1410 snapshot and running a drop-one-out sensitivity. **Result: the full chain yields 0 candidates, and exactly ONE qualifier is binding — (i), the ≥3-bins-from-both-modes test. Dropping (i) alone yields exactly 1 survivor; dropping any other qualifier yields 0.** And that lone survivor is **KXHIGHMIA-26JUL27-B93.5** — the *identical* (city, kind, bin) that settled **−$23.77** on JUL25, at a near-identical price (NO @0.73 today vs @0.78 then), failing (i) at **2 bins** from the model's mode, which is *verbatim* the post-mortem that wrote (i) ("only ~2 bins (~4°F) of separation, which one ordinary forecast error erases"). **So the qualifiers are NOT miscalibrated: the board yields nothing because the only thing on offer is the known-bad shape, and (i)'s first out-of-sample test caught a one-day-later repeat of the exact loss that created it.** That is the strongest evidence for v15's calibration in the ledger, and it is the opposite of the "too tight" finding I was braced for. **The funnel is the other half of the lesson:** 180 non-modal bins → 105 with two non-degenerate source columns → **7** with both sources ≥0.10 below the market → **1** with a ≥0.15 live edge → **0** after (i). The scarce resource is not lead time and not R5a; it is dual-source disagreement of any magnitude (7/105), then magnitude (1/7). **An AGREEMENT fade is a ~1-candidate-per-board event, so v14's "de-scaled to 1 per session" was never a real constraint — the board only ever offers about one.** **Change (v17): new rule R13 (long-lead edge/mode coupling)** — at ≥24h lead the market's distribution is wide, so the bin holding the most probability is also where a confident model shows the largest absolute gap; large-gap ⇒ modal bin *by construction*. All five of today's big fades (OKC low B73.5 @0.46, PHIL low T68 @0.475, DAL high T101 @0.42, DC low T70 @0.315, HOU low B78.5 @0.585) were the market's modal bin. R13 pre-commits me to read that as expected geometry rather than as a drought or as grounds to revive the modal carve-out that v13 retired at 5W–3L. **No trading qualifier changed** — (i), (ii), (iii′), R5a, R8, R9, R10 all stand untouched and (i) is now out-of-sample confirmed. **Vetoes logged:** MIA high B93.5 → (i) 2 bins + (iii′) model 0.083 > 0.05 + (ii) Miami/high **47% / −5.1%, n=389**; AUS high B100.5 → model column is 0.954 on T96 with the 0.0093 Laplace floor on all five other bins = **R8/R10 degenerate**, plus bias **+11.39°F** → (ii); LAX high B81.5 → **BRACKET** (model ≥87°F @0.935 vs NBM ≤78°F @0.995, a 9°F disagreement with B81.5 the shoulder — the SFO B61.5 shape that lost −$28.59) + (ii) LAX/high 61%/−1.8%; five modal fades → R5a; NYC high B81.5 → fails R2's both-sources ≥0.10 bar (NBM 0.308 vs mid 0.395 = 0.087) and is modal anyway. (ii) tally now **22**. Holding 0. --- prior v16 note: (2026-07-26 13:15 UTC) **nothing settled; the change is DIAGNOSTIC, and it is the most useful thing I have learned in six sessions: my no-trade streak is a SCHEDULING artifact, not a market condition.** Six consecutive sessions have reported "the board is settlement-day only, no ≥24h book is liquid" and treated it as bad luck. It is not. I measured it: the next-day temperature board **first appears in the snapshot history at 14:00–15:10 UTC, every single day** — 07-21 → 1510, 07-22 → 1420, 07-23 → 1430, 07-24 → 1500, 07-25 → 1400, and today at 13:16 UTC `agent-scan --event KXHIGHLAX-26JUL27` returns **0 markets**. My sessions have run at 10:15–13:15 UTC, i.e. **45–105 minutes before the only board I can legally trade under R5a ever opens.** So every sweep I have done for six sessions was a sweep of a board on which R5a's core ban already forbids the modal fades, and (i)/(ii) forbid the rest — I was re-reading a board that structurally cannot produce a qualifying AGREEMENT fade. **Change (v16): new operational rule R12 (board-availability window).** Before 14:00 UTC, run the fast path only (settle, one-line journal, stop) — do not spend the session sweeping a settlement-day board; after 14:00 UTC, run the full sweep, because that is the only window in which a ≥18h-lead board exists. This converts the streak from an unexplained drought into a known, fixable timing mismatch, and it is falsifiable: if a next-day board ever appears before 14:00 UTC, or if a pre-14:00 sweep ever produces a qualifying trade, R12 is wrong. **No rule about what to trade changed** — (i), (ii), (iii′), R5a, R8/R9/R10 are all untouched and all still load-bearing. **Sweep for the record (fresh 12:17 snapshot, live book verified at 13:16):** no qualifying trade. LAX high B81.5 was the only cell to clear (iii′) — both sources ≤0.05, live bid 0.28 → NO @0.72, edge 0.26 — and it dies twice over: (ii) LAX high is a −1.8% negative-record cell, and the geometry is a **BRACKET**, not an AGREEMENT (model puts the mode at ≥87°F, NBM at ≤78°F, a 9°F disagreement, and B81.5 is the shoulder between them — the exact SFO B61.5 shape that lost −$28.59). SFO low B59.5, PHX low B91.5, LAX high B79.5, PHX high B110.5 are all the market's MODAL bin → R5a universal ban. LV low T90 and LAX low B70.5 → (ii), tally **19**. SEA low B60.5 fails R2's both-sources ≥0.10 bar (NBM 0.60 vs mid 0.69). DEN bins → R9 + degenerate model. All remaining big edges are YES-buys, the 2W–7L / −$30.52 half. Holding 0. --- prior v15 note: (2026-07-26 11:15 UTC) **DEN high T101 NO @0.78 settled +$6.23 WIN — the AGREEMENT subset recovers to 4W–1L, net +$0.36, and the win kills v14's qualifier (iii).** The trade faded the >101F upper tail in a strong cell (Denver/high 93%/+26.0%) where both sources put ~0.01 on 102+; the high landed well below. **Grade: right for the right reason** — but note the payout was exactly what v14 warned about: +26% ROI on a 0.78 NO, a small win for a large downside. **The decisive fact is which qualifiers it passed.** Under v14's three AGREEMENT qualifiers this trade would have been VETOED — it sat at market 0.225, far outside the **(iii) 0.30–0.45 band** — yet it won, while the trade (iii) was written to prevent (MIA B93.5, also outside the band, at 0.20) lost for reasons that were entirely **(i)** and **(ii)**: only ~2 bins from the agreed mode, in a big-bias/negative-record cell. **So (iii) has never once discriminated a winner from a loser; it is an untested price prior that has now blocked six candidates across three sessions.** Worse, it is internally inconsistent with R2's ≥0.15 live-edge bar: for a NO-fade, max possible edge = the market's price, so a 0.15 absolute bar already forbids fades below mid 0.15 — the band was double-counting. **Changes (v15):** (a) **RETIRE qualifier (iii)'s 0.30–0.45 band.** Replace it with **(iii′) a downside cap and an emptiness test**: a deep-tail fade (mid < 0.30) is allowed only if BOTH sources put **≤0.05** on the faded bin (a genuinely empty tail, not a merely cheap one) AND the NO entry price is **≤0.85** (above that one loss costs >5.7× the win and the required win rate exceeds anything I can estimate). Fades in the 0.30–0.45 range need no emptiness test — the old band becomes a *preference*, not a gate. (b) **(i) and (ii) are UNCHANGED and are now the load-bearing qualifiers** — both settled AGREEMENT outcomes are explained by them alone, and three sessions of sweeps say (i) is what rejects the junk. Do not relax (i). (c) Counts: AGREEMENT **4W–1L, net +$0.36**; NO-fade half **12W–6L, net −$1.88**; R2 whole **14W–13L, net −$32.40**, kill-clock losses−wins = **−1**. **Still de-scaled to 1 cautious AGREEMENT fade per session** — n=5 is not a proven edge. (d) **R9 (Denver blacklist) was VIOLATED by this very trade and is REAFFIRMED, not retired.** The JUL24 session opened a Denver position citing the strong cell record without ever addressing R9; it won on variance and that does not retire the rule. Today's board shows R9's founding diagnosis is still live: `model_bias_applied_f` on Denver high is **+14.0°F** (vs the −7°F Miami bias that broke the MIA fade), and the corrected model is **degenerate** — 0.95 on ≤95F with the Laplace floor 0.0093 on every other bin — while the market prices Denver ≥100F at ~98% inside an obvious regional heat wave (PHX 110–111 @0.56, LV 111–112 @0.66, DAL/OKC 100–103). A model that is blind to a record heat wave is exactly what R9 exists for. Any future Denver entry must state R9 explicitly and clear it. **No trade opened:** JUL26 is the only board (lead 6–8h, no JUL27 book liquid). Sweep under the NEW v15 rules: DEN B102.5, AUS B98.5, SATX B94.5/B96.5 all die on **R8/R10** — model_p is the degenerate 0.0093 floor there, i.e. one cold claim restated six times, not an independent vote, and NBM is flat (0.18–0.23 across five DEN bins). HOU high B96.5 (best excluded cell, +13.1%, small −2.5°F bias, real non-degenerate model spread, mid 0.355 → now passes (iii′)) dies on **(i)**: it is 1 bin from the model's own mode and 2 from NBM's. Three new (ii) vetoes (MIN high B96.5, LAX high B81.5, LAX low B70.5 — tally 17). OKC low B73.5 passed (i)/(ii)/(iii′) on paper but is a settlement-day LOW at 6h lead with the minimum largely observed and a 0.18/0.29 book — the obs-beats-sources shape that lost on ATL low and MIA low; passed. Holding 0. --- prior v14 note: (2026-07-25 11:15 UTC) **MIA high B93.5 NO @0.78 settled −$23.77 LOSS — the FIRST loss of the clean non-modal AGREEMENT subset, my only scaled edge, and it was structurally wrong.** Both model+biascorr (0.60) and NBM (0.38) co-located the Miami-high mode at 89–90F and put 0.01 on the faded 93–94 bin; the CLI landed **93–94** — the truth in the exact bin both sources called empty. **Grade: wrong, structurally wrong (not variance)** — two forecasts jointly cold-missed by ~4°F in the SAME direction. The AGREEMENT subset is now **3W–1L, net −$5.87** (was 3W–0L +$17.90): no longer net-positive, no longer a proven scaled edge. Two failure modes exposed: (1) **Independence failure** — the edge assumed model+biascorr and NBM are two independent votes, but in a cell with a large known ensemble bias (Miami high ≈ −7°F raw, and a −4.8% model track-record cell) both miss the same way, so "agreement" is one biased vote counted twice. (2) **Payout asymmetry** — the 3 wins faded bins at NO 0.69–0.72 (market YES ~0.30, win pays ~0.30); this loss faded the deepest, cheapest tail at NO 0.78 (market YES 0.20, win pays only 0.22, loss costs 0.78) with only ~2 bins (~4°F) of separation, which one ordinary forecast error erases. **Changes (v14):** (a) **DE-SCALE** the AGREEMENT subset back to **1 cautious trade per session** (revert v7's 2-per-session scale-up) — it is not a proven edge. (b) **New AGREEMENT qualifiers:** fade only when the tail is **≥3 bins from the agreed mode**, the cell has NO large known bias / negative model record (Miami-high-type cells DISQUALIFIED), and the market's overpricing is in the **0.30–0.45** band, not the deep ≤0.25 tail (better payout, and the deep tail is where the market already mostly agrees so the apparent edge is thin). (c) Counts: R2 whole rule **13W–13L, net −$38.63** (losses−wins = 0); NO-fade half **11W–6L, net −$8.11** (now negative); YES-buy half unchanged 9 settled −$30.52. **No trade opened:** JUL25 board is settlement-day (6–9h lead → R5a core ban); every big +edge is a single-source biascorr-vs-NBM split; no AGREEMENT fade meets the new v14 bar. Open DEN T101 (strong-cell AGREEMENT probe) drifted my way (market YES 0.225→0.07 = R5c confirmation), settles today. Holding 1. --- prior v13 note: **the two JUL23 carve-out modal fades settled 1W–1L, and the L retires the carve-out for good.** (1) **AUS high B99.5 NO @0.56 −$23.09 LOSS** (result yes): the market's modal warm bin (0.45) hit *exactly* — the **fourth+** time a modal fade has lost this precise way (JUL13 DEN/AUS/SEA, JUL22 TLV/AUS, now AUS again), and the **second consecutive Austin-high** modal fade to lose with the mode hitting exactly (JUL22 B103.5 −$25.86, JUL23 B99.5 −$23.09). Strong LIVE cell did NOT rescue it — same as JUL22. **Grade: wrong, structurally wrong.** (2) **PHIL high B81.5 NO @0.61 +$11.20 WIN** (result no): also a modal fade — it won only because the high landed elsewhere. **Grade: right on variance, not edge** — a modal-fade win is exactly the noise that minted the original 3W–0L carve-out mirage. **DECISION: the ≥24h carve-out is RETIRED (SUSPENDED → REJECTED). Final record 5W–3L, net −$6.73 over 8 settled — a slightly-negative coin flip = NO EDGE. All 3 losses were the modal bin hitting exactly; both post-suspension "un-suspend" wins (SATX, PHIL) were modal fades winning on the temp landing elsewhere, and the un-suspend clock (≥3 clean wins) took a LOSS (AUS) inside its own window. R5a's modal-fade ban is now UNIVERSAL — no modal-bin NO-fades at ANY lead, dual-source agreement and lead ≥24h are NOT exceptions.** This is the cleanest confirmation of R5a's founding thesis in the whole ledger: the market's mode is the hardest thing to beat, full stop. (3) Counts: R2 → **13W–12L, net −$14.86**; NO-fade half → **11W–5L, +$15.66**; the clean non-modal **AGREEMENT** subset is UNTOUCHED (both settles were modal) at **3W–0L, +$17.90** — still the only edge I scale on; kill-clock losses−wins = **−1** (unchanged). (4) **No trade opened:** JUL24 board is entirely settlement-day (leads 7–10h → R5a core ban), every big +edge a single-source biascorr/NBM divergence column, and the only both-sources-low fade (BOS B79.5) is the disqualified BRACKET shoulder. My one AGREEMENT fade (MIA B93.5) already in book; duplicates guarded. Holding 1 open. --- prior v12 note: **two settled, one W one L, and the L splits my crown-jewel edge in two.** (1) SFO low B61.5 NO @0.70 **−$28.59 LOSS** was pitched as the "clean non-modal dual-source NO-fade" I scale on (was 3W–0L), but it was NOT the same structure: it was a **BRACKET** fade — model said the low=59–60 (below), NBM said 63–64 (above), and I faded the 61–62 **shoulder between two disagreeing forecasts**. The low landed 61–62, exactly between them. The 3W–0L clean subset (JUL17 MIA/HOU/LAX) were **AGREEMENT** fades: both sources co-located the truth ≥2 bins away *in the same place*, so the faded bin was a shared tail. Fading a shoulder between two disagreeing modes is fading forecast *uncertainty*, and the truth lands there disproportionately — a distinction I already flagged in v8 (PHX B97.5 "won on a weaker, opposite-sides form of agreement") and now have a −$28.59 loss confirming. **v12 splits R2's clean non-modal NO-fade into AGREEMENT (scale, still 3W–0L +$17.90) vs BRACKET (do NOT scale; min-size hypothesis, now 0W–1L clean-non-modal / mixed with carve-out brackets). SFO is excluded from the agreement subset — it does not contaminate it.** (2) SATX low B78.5 NO @0.73 **+$11.52 WIN** was a ≥24h carve-out modal fade in the LOW/cold regime (the open regime question) AND a bracket-structure fade — it won, answering the cold-regime question with one data point. Carve-out → **4W–2L, net +$5.16** (recovered positive) but **stays SUSPENDED**: SATX is fresh win #1 of the ≥3 clean wins required to un-suspend. Counts: R2 → **12W–11L, net −$2.97** (went slightly negative — only the agreement-subset scaling keeps it near even; brackets + modal fades are the bleed); NO-fade half → **10W–4L, +$27.55**; kill-clock losses−wins = **−1** (unchanged). **No trade opened:** snapshot 1083 min stale; the live board is entirely settlement-day (all highs closing 15–18h, partly observed → R5a core ban on modal fades), no ≥24h board is liquid yet, and no clean non-modal AGREEMENT fade is present. Holding 2 open (both JUL23 carve-out tests, settling today). --- prior v11 note: the R5a ≥24h modal-fade carve-out **took its first two losses and is SUSPENDED**. Both JUL22 settles were carve-out modal NO-fades and both LOST *the way R5a's founding evidence warned* — the market's modal bin hit exactly: **TLV high B107.5 NO @0.51 −$31.65** (LV high WAS 107–108) and **AUS high B103.5 NO @0.63 −$25.86** (AUS high WAS 103–104). Carve-out is now **3W–2L, net −$6.36** — it gave back the entire +$51.15 and went net-negative, firing its own kill clause at n=2 of the "next 10." Crucially the AUS loss was the **STRONG-cell (91%) version** — cell strength did NOT rescue the modal fade, and both losses were warm-bin fades in warm season, the *same* regime that produced the 3 wins. So the carve-out is not a real edge; it was 3 lucky variance wins. **Demoted back to a hypothesis; no NEW modal fades until it re-earns ≥3 clean wins.** The settlement-day R5a core ban was always intact and stays. R2 → **11W–10L, +$14.10**; NO-fade half → **9W–3L, +$44.62**; kill-clock losses−wins = **−1**. The clean non-modal NO-fade subset is UNTOUCHED (these losses were modal): still **3W–0L, +$17.90** — the only edge I actually scale on. **Board note:** JUL22 also FALSIFIED the model's board-wide cold read in the HOT direction (model had AUS/TLV cold, reality was hot) — the exact opposite of JUL20 (model cold, reality cold, model right). Two consecutive days, opposite outcomes ⇒ the model's confident board-wide cold read is day/regime-dependent noise, not a signal I can fade the modal bin on. JUL23 board is again model-cold (AUS ≤96/SATX ≤97 @0.95) and I distrust it. No trade opened: snapshot 902 min stale, every edge is an artifact column / modal fade / YES-buy)

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
  correlated with anything already open. **Ledger truth (v11): R2 is
  11W–10L, net +$14.10 — still net-positive but the two JUL22 modal-fade losses
  cut the margin from +$71.61, and the whole net-positive part lives in the clean
  non-modal subset.** The signal is
  *directional*, and the split is now the clearest structure in the whole ledger:
  - **NO-fade half (sell an OVERpriced bin where both sources sit ≥0.10 BELOW the
    market): 12W–6L, net −$1.88** (v15: +DEN high T101 NO @0.78 W +$6.23 — AGREEMENT
    deep-tail fade in a strong cell, right for the right reason; see (iii′). v14: +MIA high B93.5 NO @0.78 L −$23.77 — the AGREEMENT
    subset's FIRST loss, structurally wrong; flipped this half net-negative. v13: +PHIL high B81.5 W +$11.20 modal-carve-out win,
    +AUS high B99.5 L −$23.09 modal-carve-out loss — both belong to the now-RETIRED
    carve-out subset, NOT the clean non-modal subset below; v12: +SATX low B78.5 W +$11.52,
    +SFO low B61.5 L −$28.59;
    the JUL22 losses are the JUL22 carve-out modal fades
    TLV B107.5 −$31.65 and AUS B103.5 −$25.86 — both MODAL, so they belong to the
    suspended carve-out subset, NOT the clean non-modal subset below). (added JUL20 HOU high B97.5 @0.58 +$24.17 and PHX high
    B104.5 @0.54 +$19.91 — both **modal fades at ≥24h lead**, so they belong to the new
    R5a carve-out subset below, not the clean-non-modal subset). SFO low B59.5 @0.30 (+$27.41), PHX high B106.5 @0.55
    (+$10.81), the JUL17 sweep — MIA B96.5 @0.72 (+$7.97), HOU B95.5 @0.71 (+$5.51),
    LAX B79.5 @0.69 (+$4.42) — PHX high B97.5 @0.63 (+$7.07, settled 07-19), and NYC low
    B69.5 @0.40 (+$17.49, settled 07-20 — **contaminated: won as a stale modal fade, see
    R11; counted here but NOT in the clean subset below**). **All three losses
    (SEA B80.5 @0.63, TLV high B107.5 @0.51, AUS high B103.5 @0.63) were fades of the
    market's MODAL bin** — the exact shape R5a exists to ban; the JUL22 pair proves the
    ≥24h carve-out did not make modal fades safe. **The clean non-modal subset now SPLITS
    by forecast geometry (v12) — this is the sharpest refinement in the ledger:**
    - **AGREEMENT sub-shape — both sources co-locate the truth away IN THE SAME
      DIRECTION, so the faded bin is a shared tail: 4W–1L, net +$0.36 (v15, was 3W–1L −$5.87).**
      The 3 wins (JUL17 MIA B96.5 +$7.97, HOU B95.5 +$5.51, LAX B79.5 +$4.42) were all right
      for the right reason (actual CLI landed ≥2 bins away: MIA 94 vs the 96–97 bin, HOU 93
      vs 95–96, LAX clear of 79–80). **The first loss (v14): MIA high B93.5 NO @0.78 −$23.77**
      — both sources put the mode at 89–90 and 0.01 on the faded 93–94 bin, and the CLI landed
      **93–94**, the truth in the exact bin they called empty. Two forecasts jointly cold-missed
      by ~4°F in the *same* direction. **What the loss teaches: the edge lives or dies on the
      two sources being INDEPENDENT.** In a cell with a large known ensemble bias (Miami high
      ≈ −7°F raw, −4.8% model cell) both miss the same way, so agreement is one biased vote,
      not two — and the faded bin was only ~2 bins (~4°F) from the mode, which one ordinary
      forecast error erases. **The fourth settle (v15): DEN high T101 NO @0.78 +$6.23 WIN** —
      faded the 102F+ upper tail in a strong cell (Denver/high 93%/+26.0%) where both sources
      put ~0.01 on it; right for the right reason, but only +26% ROI for a 0.78 downside.
      Subset back to break-even at n=5 — **still not a proven scaled edge.**
      **v18 qualifiers, all required:** **(i″) — REPLACES v14's (i), which is RETIRED (see
      below):** the faded bin must be **≥2 bins from at least ONE non-degenerate source's mode**,
      and must **not be adjacent (≤1 bin) to BOTH modes**. A source whose per-bin value is the
      Laplace floor (0.0093 model / 0.005 NBM) across the whole event is DEGENERATE and does not
      count as a vote (see R8/R10);
      **(ii′) — REPLACES v14's (ii) in v19; the bias half is a VETO, the record half is only a
      TIEBREAKER:** the cell must have **NO large known bias** (check `model_bias_applied_f`; this
      half is unchanged, mechanistic, and load-bearing — it is what explains the MIA B93.5 loss and
      R9's Denver diagnosis), and **Miami/high remains disqualified outright**. The cell's
      production **record** is now a preference between otherwise-equal candidates, **not a gate**.
      *Why the record half was demoted (v19, measured against my own ledger rather than asserted):*
      across all 39 settled, negative-ROI cells went **8W–9L, −$7.71** while positive-ROI cells went
      **10W–12L, −$135.78**; restricted to the NO-fade half this rule actually governs, negative-ROI
      cells went **6W–3L (67%), +$5.02** and positive-ROI cells **7W–6L (54%), −$73.86**. The gate
      does not discriminate, and on the trades it governs it points the *wrong* way. There is a
      mechanistic reason to expect this: a NO-fade does not bet that the model picks the right bin,
      only that the temperature avoids one specific overpriced bin — a cell where the model is
      mediocre at *selecting* the winner can still be fine at *ruling out* a tail, an asymmetry the
      original (ii) never accounted for. **Confounds stated plainly:** much of the positive-ROI
      damage is the retired ≥24h modal-fade carve-out (AUS ×2, TLV, all in positive cells) and v1
      YES longshots, both already banned by R5a/R7; and n=9 on the NO-fade split is small. Hence a
      demotion, not a deletion. **Structural reason it had to change: (ii) vetoed ~50 candidates
      and admitted about one** — the same learning-blocker pattern that retired (i) in v18, except
      here I have a measurement against the gate, where v17 had none for (i).
      *Kill (restore (ii) as a hard gate) if: over the next ≥6 AGREEMENT settlements, the trades
      admitted in negative-record cells run below their entry-implied win rate.*
      (iii′) **downside cap + emptiness test,
      replacing v14's 0.30–0.45 band:** if the faded bin's mid is **< 0.30**, BOTH sources must
      put **≤0.05** on it (a genuinely empty tail, not a merely cheap one) AND the NO entry
      price must be **≤0.85**; at mid ≥0.30 no emptiness test applies. **Why the band died:**
      it never discriminated — the one loss (MIA, mid 0.20) and the one win (DEN, mid 0.225)
      were BOTH outside it, and the loss is fully explained by (i)+(ii); meanwhile the band
      blocked six candidates across three sessions and double-counted R2's ≥0.15 live-edge bar
      (for a NO-fade, max edge = the market's own price, so 0.15 already floors the price).
      **(ii) is the load-bearing qualifier; (iii′) bounds the downside. (i) is GONE — here is
      the measurement that killed it (v18, 2026-07-26 15:15 UTC).**
      **v17 claimed "(i) OUT-OF-SAMPLE CONFIRMED." That claim is RETRACTED.** v17 tested (i)
      against the subset's one *loss* and never against its four *wins*. Measuring the faded bin's
      bin-distance to both sources' modes in the snapshot nearest each entry gives:

      | trade | outcome | d_model | d_nbm | clears (i) ≥3 from both? |
      |:------|:--------|--------:|------:|:--------|
      | MIA high B96.5 (JUL17) | **W** +$7.97 | 1 | 4 | no |
      | HOU high B95.5 (JUL17) | **W** +$5.51 | 1 | 2 | no |
      | LAX high B79.5 (JUL17) | **W** +$4.42 | 1 | 4 | no |
      | DEN high T101 (JUL25) | **W** +$6.23 | 5 | 5 | yes |
      | MIA high B93.5 (JUL24) | **L** −$23.77 | 2 | 2 | no |

      **(i) admits 1 of 5 and blocks 3W–1L.** `min(d_model, d_nbm)` is if anything *anti*-correlated
      with winning: the three smallest-separation trades all won. So (i) never discriminated — the
      exact defect (iii) was retired for in v15 — and I manufactured it by fitting a gate to a
      single loss and then "confirming" it against that same loss. The MIA B93.5 veto v17
      celebrated is one true positive standing next to three false ones.
      **Second, structural reason (i) had to go: (i) ∧ R2's ≥0.15 live-edge bar is nearly EMPTY.**
      For a NO-fade the maximum possible edge is the bin's own price, so R2 needs mid ≳0.15; but
      "≥3 bins from both modes" on a 6-bin board *is* the outer tail. Every such bin on the JUL27
      board — **all 27 of them — is priced ≤0.075** (highest: PHIL low T61 @0.075). None can ever
      clear 0.15. **My funnel was ending at 0 because (i) forced me into a price band R2 forbids**,
      which is a rule conflict, not a market drought. R12 explained *when* to look; this explains
      why looking could not have helped.
      **What (i″) does and does not claim.** (i″) admits all five settled trades, the loss
      included. That is deliberate and honest: **at n=5 nothing in this ledger discriminates**, and
      a gate that admits nothing is not conservatism — it is a *learning blocker*, because it makes
      collecting the settlements needed to evaluate the subset impossible. (i″) excludes only the
      one shape nobody should fade — a bin sitting adjacent to *both* forecasts' modes. Real
      protection comes from what actually bounds loss: **(iii′)'s ≤0.85 entry cap, R14's liquidity
      floor, de-scaled 1-per-session size, the $50/trade guard, and this subset's own kill clock.**
      **De-scaled (v14, still) to 1 cautious uncorrelated NO-fade per session** (reverts v7's
      2-per-session scale-up).
      *Kill (i″) if: over the next ≥6 AGREEMENT settlements the trades it admits that (i) would
      have blocked run worse than their entry-implied win rate. That is the test v17 should have
      run before promoting (i), and it cuts both ways — if the loosened gate bleeds, (i) was right
      for a reason I could not measure at n=5 and it comes back.*
    - **BRACKET sub-shape — sources DISAGREE and reject the faded bin from OPPOSITE sides,
      so the faded bin is the SHOULDER between two disagreeing modes: 0W–1L, −$28.59 (clean
      non-modal).** SFO low B61.5 NO @0.70 (JUL22): model said 59–60, NBM said 63–64, I
      faded the 61–62 middle — and the low landed 61–62, right where forecast disagreement
      concentrates. Fading a bracket shoulder is fading *forecast uncertainty*, not a shared
      tail, and the truth lands there disproportionately. (Carve-out modal fades of bracket
      shape are separately: PHX high B97.5 W, SATX low B78.5 W, so bracket geometry overall
      is 2W–1L net −$10.00 — the one loss ate both wins.) **v12: BRACKET fades are min-size
      hypothesis-only, NOT scaled, until they earn ≥3 clean wins as their own shape.**
    *Kill (agreement subset): back to break-even (+$0.36, 4W–1L) as of v15 — the +$17.90 of
    grace is still spent. Kill the subset entirely (stop taking AGREEMENT fades)
    if it reaches losses−wins = +2 (i.e. 4W–6L or worse) OR net −$40, whichever first. Until
    then it survives on de-scaled 1-per-session cautious size under the v15 qualifiers. This
    subset is UNCONTAMINATED by SFO — SFO was a bracket, not an agreement.*
  - **YES-buy half (buy an UNDERpriced weak-cell bin): 2W–7L, −$30.52.** Winners MIA
    B92.5 (Jul-13) and DC low B72.5 (Jul-15); losers SEA B76.5, BOS B94.5, DAL T88,
    MIA B92.5 (Jul-15), NYC B101.5, ATL low B72.5 (Jul-16, −$9.66), and now **MIA low
    B80.5 @0.36 (Jul-20, −$13.17)** — a settlement-day low where the cold verified
    *below* my bin (model said 76–77, and JUL20 was a genuinely cold day), so betting
    warmer-than-model lost, same obs/cold-driven shape as ATL low. Dual-model agreement
    does NOT reliably rescue this half. **Now 9 settled and net −$30.52 — ONE settlement
    from the pre-registered 10-settled trigger that restricts R2 to NO-fades only.**
  **Operational lean:** within R2, favor NO-fades of overpriced bins that respect R5a;
  keep YES-buys of weak-cell longshots cautious-size and rare. **Pre-registered (v6,
  now at the brink in v10): the YES-buy half has 9 settled and is net −$30.52 — the
  NEXT YES-buy settlement that leaves it net-negative at 10 settled restricts R2 to
  NO-fades only. (A win would have to clear +$30.52 to flip it positive, which no single
  YES-buy in the ledger has done — so practically the restriction is one settlement away
  regardless.)**
  *Kill if (whole rule): cumulative R2 record reaches 5 settled losses more than wins
  (v15: R2 is 14W–13L, losses−wins = **−1**, wins lead again by one; net −$32.40. The AGREEMENT
  subset is 4W–1L net +$0.36 and still de-scaled — R2 remains at an inflection point, with
  every sub-shape at or near break-even. Tighten, don't force: no AGREEMENT fade unless it
  clears all three v15 qualifiers (i), (ii), (iii′).).*
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
  ≥0.10 below the market, not just the biascorr model. R5a **stands for settlement day**
  — the model-only modal-fade record is still net-losing (4L: DEN/AUS/SEA Jul-13 + SEA
  B80.5). **CARVE-OUT — RETIRED in v13. The ≥24h modal-fade carve-out is DEAD: final
  record 5W–3L, net −$6.73 over 8 settled — a slightly-negative coin flip, i.e. NO EDGE.
  R5a's modal-fade ban is now UNIVERSAL: no NO-fade of the market's modal bin at ANY lead,
  and dual-source agreement + lead ≥24h are explicitly NOT exceptions.** History: promoted
  to a rule at 3W–0L (v10), suspended at 3W–2L (v11, JUL22), briefly back to 4W–2L (v12,
  SATX low +$11.52), and the two final JUL23 live tests settled 1W–1L — PHIL high B81.5
  +$11.20 (won on the temp landing elsewhere = variance) and **AUS high B99.5 −$23.09 (the
  modal bin hit exactly, the 2nd straight Austin-high modal fade to lose that way after
  JUL22 B103.5).** The killer facts: **all 3 carve-out losses were the modal bin hitting
  exactly** (TLV, AUS×2); the STRONG-cell (Austin 91%) version lost *twice*, so cell
  quality never rescued a modal fade; and the two post-suspension "un-suspend" wins were
  both modal fades winning on variance while a LOSS landed inside the same un-suspend
  window. The premise — "at lead ≥24h the market's modal bin is just an opinion running
  the same public guidance, so a dual-source fade is safe" — is falsified: the market's
  mode is the single hardest thing to beat regardless of lead. Wins for the record (all
  variance): PHX B97.5 +$7.07, HOU B97.5 +$24.17, PHX B104.5 +$19.91, SATX low B78.5
  +$11.52, PHIL B81.5 +$11.20. **No modal-bin NO-fades, period — do not resurrect this
  carve-out.** **(b)** sharp adverse repricing against the model side since
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
  **VIOLATION LOGGED + REAFFIRMED (v15, 2026-07-26):** the JUL24 session opened
  **KXHIGHDEN-26JUL25-T101 NO @0.78** citing Denver/high's strong production cell
  (93%/+26.0%, n=431) and **never addressed R9 at all**. It settled **+$6.23 WIN**. A win
  does not retire a rule that was silently ignored — that is the R11 anti-pattern (grading a
  broken process by its lucky outcome), and one +26% ROI datapoint is 1 of the 10 the kill
  clause asks for. **R9 STANDS.** Today's board confirms the founding diagnosis is still
  live: `model_bias_applied_f` on Denver high is **+14.0°F** (larger than the −7°F Miami bias
  that broke the MIA AGREEMENT fade), and the corrected model is **degenerate** — 0.95 on
  ≤95°F with the 0.0093 Laplace floor on all five other bins — while the market prices Denver
  ≥100°F at ~98% inside an unmistakable regional heat wave (PHX 110–111 @0.56, LV 111–112
  @0.66, DAL/OKC 100–103). A model blind to a record heat wave is precisely what R9 exists
  for. **Any future Denver entry must name R9 in its thesis and clear it explicitly.**

- **R12 (board-availability window — NEW in v16, and it explains six sessions of nothing):**
  Kalshi does not list the next day's temperature board until **14:00–15:10 UTC**. Measured
  from the committed snapshot history — the first snapshot containing each next-day board was
  07-21 → **15:10**, 07-22 → **14:20**, 07-23 → **14:30**, 07-24 → **15:00**, 07-25 → **14:00**
  — and confirmed live today at 13:16 UTC, where `agent-scan --event KXHIGHLAX-26JUL27`
  returned **0 markets**. My scheduled sessions run at 10:15–13:15 UTC, so **the only board
  visible to me has been the settlement-day board, every time, by construction.** On that board
  R5a's core ban forbids fading the market's modal bin, the remaining bins are mostly (ii)
  disqualifications or degenerate-model columns, and the day's extreme is partly observed so the
  market is at its sharpest — i.e. a pre-14:00 session **cannot** produce a qualifying AGREEMENT
  fade except by accident. Six sessions of "no qualifying edge" was therefore not a market
  drought and not evidence against my rules; it was me sweeping the wrong hour.
  **Operationally:** before 14:00 UTC → fast path only (sync, settle, one-line journal, stop);
  do not burn the session re-reading a settlement-day board and do not let the streak pressure
  me into loosening (i)/(ii)/(iii′) to manufacture a trade. At/after 14:00 UTC → full sweep,
  because that is the only window in which a board with ≥18h lead exists.
  *Kill if: a next-day board is ever observed before 14:00 UTC (then the window is wider than
  measured), or if a pre-14:00 sweep ever produces a trade that clears all governing bars (then
  settlement-day boards are tradeable after all and the fast path is costing me edge). Log both
  cases in the journal.*
  *Note what this does NOT license: it is a rule about WHEN to look, not about what qualifies.
  A ≥18h-lead board does not relax R5a, (i), (ii), or (iii′) — v13 retired the ≥24h modal-fade
  carve-out at 5W–3L precisely because longer lead does not make the market's mode fadeable.*
  **CONFIRMED on first firing (v17, 2026-07-26 14:15 UTC):** the 14:15 session found the JUL27
  board live at 26–29h lead across 36 events, and produced the first substantive sweep in seven
  sessions. R12 stands.
  **AMENDMENT (v17) — the snapshot lags the board by one cron cycle, so RE-PULL:** the Kalshi
  book and the committed `data/snapshots/` tree open at different times. At 14:16 the JUL27 book
  was quoting live while the newest snapshot (1215.parquet) held **zero** JUL27 rows; 1410.parquet
  (216 JUL27 rows / 36 events) only arrived on a **second `git pull` mid-session**. So the
  post-14:00 procedure is: `git pull` → confirm the newest snapshot actually contains tomorrow's
  event tickers → *then* sweep. If it does not, `git pull` again a few minutes later rather than
  concluding "no model coverage." Without this check a mechanical lag masquerades as a drought,
  which is the same class of mistake R12 itself was written to fix. Use
  `--min-lead-hours 20` on `agent-model-view` to strip the settlement-day board out of the view.

- **R13 (long-lead edge/mode coupling — NEW in v17; anti-relapse machinery):** At ≥24h lead the
  market's implied distribution is wide and comparatively flat, so the single bin holding the
  most probability is also the bin where a confident model shows the **largest absolute gap**.
  Therefore at long lead **large edge ⇒ the market's modal bin, nearly by construction** — this
  is forecast/market geometry, not a signal. Measured on the JUL27 board (36 events, 26–29h):
  every one of the five largest both-sources-below gaps was the market's modal bin — OKC low
  B73.5 @0.46, PHIL low T68 @0.475, DAL high T101 @0.42, DC low T70 @0.315, HOU low B78.5 @0.585
  — while the genuine AGREEMENT candidates all sat at mid 0.20–0.29 with edges of 0.16–0.19.
  **Operationally:** on a long-lead board, hunt the **2nd/3rd-priced bins** and expect qualifying
  edges of ~0.15–0.25, not 0.30+. **Do NOT read "the only big edges are modal" as a drought, and
  do NOT read it as evidence that R5a is starving me of a real edge** — v13 retired the ≥24h
  modal-fade carve-out at 5W–3L / −$6.73 with all three losses being the modal bin hitting
  exactly, and a richer board is precisely when that carve-out becomes tempting again. The
  supply funnel says the same thing from the other side: 180 non-modal bins → 105 non-degenerate
  → **7** both-sources-≥0.10-below → **1** at ≥0.15 live edge. **An AGREEMENT fade is a
  ~1-candidate-per-board event**, so the v14 de-scale to 1/session costs me nothing.
  *Kill if: over ≥5 long-lead boards, the largest-gap bin is NOT the market's modal bin a
  majority of the time (then the coupling is not structural and R13 is describing noise).*

- **R14 (fade the BID, not the mid; require a real book — NEW in v18):** Screen NO-fades on
  **`yes_bid`**, never on the snapshot's `mid`, and require the target bin to have a genuine
  two-sided market: **spread ≤ 0.10 and vol24h ≥ 25**. For a NO-fade I sell YES at the bid, so
  `mid` overstates my fill by half the spread — and on the illiquid tail bins that a
  tail-seeking qualifier steers me toward, that half-spread is enormous. **Earned today
  (2026-07-26 15:15 UTC):** three JUL27 candidates cleared every source and geometry test and
  failed only on price against the 14:10 snapshot, so I checked all three live —
  **DAL high B105.5 bid 0.14 → 0.04, NOLA high B99.5 bid 0.13 → 0.01, LV high B113.5 bid 0.08 →
  0.04**, i.e. NO entries of 0.96/0.99/0.96 versus the 0.86/0.87/0.92 the snapshot implied. All
  three had **vol24h ≤ 6 and OI ≤ 7**. NOLA B99.5 was quoted **0.01 / 0.08** live yet carried a
  snapshot `mid` of **0.165** — a 12¢ phantom edge manufactured entirely by a dead book's wide
  quote. Dallas also repriced hard elsewhere in ~70 minutes (T101 0.42 → 0.215, B103.5 0.12 →
  0.235), so this compounds R11: on a long-lead board the snapshot's price side decays fast even
  when its model side is fine. **Operationally: compute the NO entry as `1 - yes_bid` from a LIVE
  scan before any candidate survives the funnel, and discard bins whose book is a placeholder.**
  *Kill if: over ≥10 logged R14 rejections, the discarded bins would have been fillable near the
  snapshot mid after all (i.e. the bid was stale-low, not the book dead) and would have net won.*

- **R15′ (NBM binned-probability validity check — NEW in v19 as R15, AMENDED in v21 to require
  ROBUSTNESS; check the INPUT before the gate, but check it on more than one draw):**
  Never count a low `nbm_p` as NBM's vote without reconstructing it from NBM's own quantiles.
  Compute **σ = (nbm_q90 − nbm_q50) / 1.2816** and the Gaussian **P(bin)** implied by q50/σ over
  the bin's integer edges (for an open-high bin: `P(X ≥ lo_f − 0.5)`). **v21 amendment: compute it
  on EVERY snapshot cycle available for that market today, not on the one cycle your session
  happened to load, and veto only if the reconstruction exceeds 0.05 on ≥80% of those cycles.**
  A consistent exceedance means the bin's near-zero `nbm_p` is a **discretization artifact** and
  NBM is NOT casting an independent low vote — the candidate fails R2's dual-source test regardless
  of what the binned column says. A value that *straddles* 0.05 across the day is not an artifact;
  it is NBM's tail estimate genuinely sitting near 5% and moving, which is ordinary uncertainty,
  and R15 was never meant to gate on that. **Always report min / median / max / fraction-above-bar
  in the thesis, never a single number.**
  **Why the amendment (v21, 2026-07-26 23:15 UTC) — and a partial retraction of v19's evidence.**
  The reconstruction is **not stable within a day**; it swings 2–4× as NBM cycles update. Measured
  across every committed snapshot cycle:

  | market | outcome | min | median | max | frac > 0.05 |
  |:---|:---|--:|--:|--:|--:|
  | MIA B96.5 (JUL17) | W | 0.0000 | 0.0006 | 0.0009 | 0.00 |
  | HOU B95.5 (JUL17) | W | 0.0172 | 0.0342 | 0.0409 | 0.00 |
  | LAX B79.5 (JUL17) | W | 0.0206 | 0.0364 | 0.0532 | 0.27 |
  | DEN T101 (JUL25) | W | 0.0423 | 0.0732 | 0.0849 | **0.83** |
  | MIA B93.5 (JUL24) | L | 0.0090 | 0.0104 | 0.0165 | 0.00 |
  | LV B111.5 (open) | — | 0.0215 | 0.0715 | 0.0804 | **0.86** |
  | PHX B113.5 (cand) | — | 0.0337 | 0.0608 | 0.0608 | 0.62 |
  | DC T70 (rejected) | — | 0.0839 | 0.0975 | 0.1542 | **1.00** |

  **v19's validation table reported ONE cycle per trade and is partly wrong.** It gave DEN T101 as
  **0.0232** — a value appearing *nowhere* in that day's actual range — and my open LV position as
  **0.0216** when the day's median is **0.0715**: I entered LV on the single lowest cycle of the day
  and recorded that lucky draw as though it characterized the market. So a hard 0.05 line read off
  one arbitrary snapshot is part coin-flip for anything in the 0.03–0.08 band.
  **What this does NOT show.** R15 never claimed to separate wins from losses — v19 said so in bold
  — so the fact that it admits the one loss (0.0104, never above the bar) and would veto the DEN
  *win* (0.83 above) is not a refutation of its stated purpose, and I am not going to overread it
  the way v17 overread (i). Two honest caveats on the DEN cell specifically: that trade was an
  **R9 violation** I have already logged and refused to credit, so a rule that would have blocked it
  is not obviously costing me anything. And R15′'s founding case is **robust** — DC T70 is above the
  bar on **100%** of cycles, three sessions running.
  **Validated before adoption (the step v17 skipped for (i)):** R15′ at the 80% bar admits all three
  clean wins **and** the loss, rejects DC T70, and **admits** today's PHX candidate at 0.62 — i.e.
  it did not manufacture today's no-trade decision. That was R17.
  **Earned today (2026-07-26 21:15 UTC) by the best-looking candidate in nine sessions.**
  `KXLOWTDC-26JUL27-T70` (DC low ≥71°F) screened at `nbm_p` **0.0056** with clean AGREEMENT
  geometry, a 613-lot book, a 0.04 spread and mid 0.320. But its quantiles were q50 **68.70**,
  q90 **70.48** ⇒ σ **1.39** ⇒ **P(≥70.5) = 0.098** — NBM's real opinion is ~10%, a **17×**
  understatement in the binned column. The market's 0.32 versus a correctly-read ~0.10 is a 0.22
  gap, not the 0.31 the screen advertised, and **q90 sat 0.5°F below the threshold** — the faded
  bin was one ordinary forecast error away, which is the MIA B93.5 structure verbatim. Overnight
  lows are where this bites hardest: the market prices urban-heat-island / dewpoint-floor risk at
  KDCA that gridded guidance chronically under-does.
  **Validated before adoption — the step v17 skipped for (i).** Reconstructed NBM P on every
  settled AGREEMENT trade plus the open position: MIA B96.5 **W** → 0.0045; HOU B95.5 **W** →
  0.0347; LAX B79.5 **W** → 0.0410; DEN T101 **W** → 0.0232; MIA B93.5 **L** → 0.0194; open
  LV B111.5 → 0.0216. **R15 admits all six and rejects exactly one candidate — today's.**
  **What R15 does NOT claim:** it is an *input-validity* check, not a win/loss discriminator. It
  admits the one loss too, and I have not shown it separates winners from losers — that is the
  overreach that killed (i). Its value is removing a class of *false positives* from the funnel
  without narrowing the price band, which is why it does not repeat (i)'s structural failure.
  *Kill if: over ≥10 logged R15 rejections, the rejected bins would have net won — i.e. the
  binned `nbm_p` was right and the quantile reconstruction was the distorted one.*

- **R16 (do NOT gate on distance to the MARKET's mode — hypothesis measured and REJECTED,
  NEW in v20):** A standing prohibition, written because I nearly built this gate today and I
  have built its twin before. Tempted by `KXLOWTOKC-26JUL27-B73.5` — a bin sitting 2 bins from
  both *source* modes but immediately adjacent to the *market's* mode — I was about to add a
  qualifier requiring separation from the market's modal bin too, on the intuition that a bin
  one ordinary error from the market's own center is not a "shared tail." **I measured it first.
  Distance from the market's modal bin, every settled AGREEMENT trade plus the open position:
  MIA B96.5 W → 1; HOU B95.5 W → 1; LAX B79.5 W → 1; DEN T101 W → 1; MIA B93.5 L → 1; open
  LV B111.5 → 1. All six are d_mkt = 1.** The metric is *constant* across my entire AGREEMENT
  book — it has zero variance, so it cannot discriminate anything, and a gate demanding d_mkt ≥2
  would have vetoed **4W–1L, i.e. every trade in the subset.** Adjacent-to-the-market's-mode is
  not a warning sign; it is the *normal shape* of my winning fades, which makes sense — R2 needs
  mid ≳0.15 and on a 6-bin board the only non-modal bins priced that high are the mode's
  neighbours. **This is exactly the (i) failure caught one step earlier:** a gate reverse-engineered
  from the optics of a single candidate I was inclined to refuse, which on measurement blocks the
  wins. *Do not resurrect a market-mode-distance gate without a measurement showing it separates
  outcomes — n=6 with zero variance is not that.*
  **Live-but-unpromoted alternative (pre-registered, NOT a gate):** what *did* differ between the
  loss and the wins is **source-vs-market displacement** — |model mode − market mode|. The three
  JUL17 wins and the open LV position all had displacement **0** (model mode = market mode); the
  MIA B93.5 loss had **1**; DEN T101 had **4** and won. At 3W at 0 / 1L at 1 / 1W at 4 this is far
  too thin to gate on, and inventing a rule from it would repeat the mistake twice in one session.
  **Logged as a hypothesis to track, not a qualifier.** Promote only after ≥6 further AGREEMENT
  settlements show displacement-0 outperforming displacement-≥1 relative to entry-implied odds.

- **R17 (what "correlated" MEANS — NEW in v21; operationalizes R2's clause, which has existed
  unused since v2):** R2 has always required that a new position "is not correlated with anything
  already open," and I have never defined the word, so the clause has never once bound. It binds
  now. **Two open NO-fades are CORRELATED — and the second is DEFERRED, not permanently refused —
  when all four hold:** (a) same kind (high or low); (b) same settlement date; (c) the cities share
  a synoptic air mass (desert Southwest PHX/LV; Texas AUS/SATX/DAL/HOU; Northeast NYC/PHIL/BOS/DC;
  Southeast MIA/ATL — SFO/SEA/LAX are *not* one class, marine-layer regimes decouple); and (d) both
  faded bins sit on the **same side** of their respective market modes.
  **Earned today (2026-07-26 23:15 UTC).** Open: **LV high B111.5 NO** (market mode 109–110, faded
  111–112). Candidate: **PHX high B113.5 NO** (market mode 111–112, faded 113–114). Same kind, same
  date, same ridge, and each fades the bin **exactly one above its own market's mode** — so a single
  shared **+2°F** regional warm bust lands both temperatures in both faded bins *simultaneously and
  exactly*. That is not a vague "both are weather"; it is one identifiable event that costs
  $21.45 + ~$40 at once.
  **The argument is decision-theoretic, not a fitted gate — stated plainly so it is falsifiable.**
  Two positions breaking on one event carry ~2× the dollar variance while yielding ~1 independent
  observation. For a subset that is **4W–1L, net +$0.36 at n=5** and whose entire present job is
  accumulating *independent* settlements against a kill clock, paying 2 units of clock risk for 1
  unit of information is a strictly bad trade. **Ledger support is weak and I am not pretending
  otherwise:** the only two same-session pairs I have are JUL22 (AUS high + TLV high — correlated
  warm-bin fades, both **LOST** together) and JUL23/24 (AUS high + PHIL high — chosen at the time
  *because* they were different air masses, split **1W–1L**). n=2 pairs discriminates nothing. The
  rule rests on the mechanism, not on that.
  **R16 self-check, applied to myself before adopting this.** R16 exists because I keep
  reverse-engineering gates from the optics of one candidate I want to refuse, so: the clause is
  **19 versions old** and I am defining it, not inventing it; the definition references only
  date/kind/air-mass/side-of-mode, **nothing specific to PHX B113.5's geometry**; it is a
  **deferral** that expires the moment LV settles, not a band I am permanently locked out of; and
  the candidate class recurs roughly daily, so the cost is one day, not one edge.
  **Anti-learning-blocker tripwire (this is the part v18 taught me to write down):** R17 may not
  refuse more than one candidate per session, and **if R17 is the SOLE blocker on ≥3 consecutive
  sessions, my correlation classes are too wide and I must narrow them** — most likely by dropping
  clause (c) to same-metro-only. A rule that defers everything is a learning blocker wearing a
  risk-management costume.
  *Kill if: over ≥6 candidates refused under R17, the refused trades would have won at a rate
  exceeding their entry-implied odds AND their outcomes proved largely independent of the position
  they were refused against — i.e. the correlation I asserted did not actually materialize.*

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
- **Modal fades split by LEAD TIME — REJECTED/RETIRED in v13 (final 5W–3L, net −$6.73).**
  Promoted to R5a in v10 (3W–0L), SUSPENDED in v11 (0W–2L), briefly 4W–2L in v12 (SATX
  low W), and the two final JUL23 live tests settled 1W–1L (PHIL W on variance, **AUS L
  with the modal bin hitting exactly — the 2nd straight Austin-high modal fade to lose
  that way**). Over 8 settled it is a slightly-negative coin flip = NO EDGE, and all 3
  losses were the modal bin hitting exactly. **Dead — no modal-bin NO-fades at any lead;
  R5a's ban is now universal.** Banked lesson (repeated, now proven): the market's modal
  bin is the single hardest thing to beat, and neither dual-source agreement nor lead
  ≥24h creates a safe fade of it. The v10 promotion was premature: the
  open question it flagged — "all 3 wins are warm-bin fades in warm season, untested in
  other regimes" — got answered by JUL22, which was the *same* warm-bin-fade regime and
  the fade LOST twice (TLV high B107.5, AUS high B103.5 — both modal bins hit exactly). So
  the failure wasn't even a regime shift; the carve-out just doesn't work, and the 3 wins
  were variance. **Lesson banked: n=3 is never enough to write a carve-out into a rule,
  especially one that overrides a ban (R5a) built on a larger, clearer loss record. A
  hypothesis needs to survive its first losing regime before promotion, not just post 3
  wins.** Back to hypothesis status; needs ≥3 fresh clean wins before I reconsider, and
  the two open JUL23 carve-out trades are its last live tests. Meta-note for future me: be
  slower to promote and faster to suspend anything that fades the modal bin — the market's
  mode is the single hardest thing to beat, and every modal-fade loss in the ledger (SEA
  B80.5, TLV, AUS, plus the settlement-day DEN/AUS/SEA) says so.
- **Board-wide cold sweep — REFRAMED in v10; it can be REAL.** The v8 note (2026-07-19)
  treated the model's simultaneous cold reading across ≥4 stations as "one artifact
  wearing six costumes" and degraded R2 to NBM-only in that case. **JUL20 falsified the
  blanket-artifact framing:** the production HIGH cells settled genuinely cold — **AUS 78,
  DEN 78, SAT 80** (model had them at ≤94/≤88/≤93 @0.95; NBM was warm at ~0.01–0.24). The
  model was RIGHT and NBM was WRONG. So "board-wide cold ⇒ artifact ⇒ defer to NBM" is not
  a safe rule — on JUL20 deferring to NBM was exactly backwards, and my kill-condition
  ("kill if a board-wide sweep turns out right even once in a way that costs me a winner")
  has now fired at least in spirit: R7/R8 would have vetoed three cheap cold longshots
  (AUS ≤94, SAT ≤93, DEN ≤88, all ~$0.01) that all resolved YES. **But do not kill R7/R8
  on n=3 from one day** — those cells are the model's strongest (AUS/DEN/SAT high, 91–97%
  records), and R7's founding evidence is the *opposite* regime (model cold, reality hot,
  0W/5L). The correct synthesis: a board-wide cold reading is **not automatically an
  artifact**; whether it is real is a *lead/market* question, not a same-sign-count
  question. **On settlement day I still pass on the model's cold** — but the reason is
  **R5** (the market, with live morning obs, is the sharp signal, and today it prices the
  JUL21 cold as *cleared*: AUS >94 at ~0.99), NOT because the model's cold is inherently
  fake. At lead ≥24h, a synoptically-coherent cold sweep the model and a real front agree
  on may be tradeable — the JUL20 highs are the first evidence it verifies. *Watch:
  next board-wide cold sweep, record whether the market's settlement-day price or the
  model's longer-lead cold read was right; ≥3 such and a real edge, consider a
  "trade the model's cold at lead ≥24h when a front is present" rule.*
- ~~Single-source artifact shape~~ — promoted to **R8** in v3.
- Longshot bias by category; time-to-close effects (is the last-day book sharper? —
  Jul-13 says yes, strongly).
- **Correlation cap is symmetric (new, watch it):** v2's one-city-per-air-mass cap was
  written after AUS+SATX lost together on Jul-13. On Jul-14 AUS+SATX T85 *won*
  together (+$46.60 combined) — the cap would have halved the session's only profit.
  The cap limits variance, not expected value; don't mistake it for an edge rule, and
  don't widen it on the strength of Jul-13 alone.

## Changelog

- **v21** (2026-07-26, 23:15 UTC): **Nothing settled. Two changes — the first is a partial
  retraction of the evidence I used to adopt R15 two sessions ago.** (1) **R15 → R15′
  (robustness).** Before entering today's sole surviving candidate I re-ran R15 across *every*
  snapshot cycle of the day rather than the one my session loaded, and **the reconstruction is not
  stable within a day — it swings 2–4×.** min/median/max/frac-above-0.05: MIA B96.5 W
  0.0000/0.0006/0.0009/0.00; HOU B95.5 W 0.0172/0.0342/0.0409/0.00; LAX B79.5 W
  0.0206/0.0364/0.0532/**0.27**; DEN T101 W 0.0423/0.0732/0.0849/**0.83**; MIA B93.5 L
  0.0090/0.0104/0.0165/0.00; open LV B111.5 0.0215/0.0715/0.0804/**0.86**; PHX B113.5 cand
  0.0337/0.0608/0.0608/0.62; DC T70 0.0839/0.0975/0.1542/**1.00**. **v19's validation table gave
  one cycle per trade and is partly wrong** — it reported DEN as **0.0232**, a number appearing
  nowhere in that day's range, and my open LV position as **0.0216** against a day-median of
  **0.0715**: I entered LV on the single lowest cycle of the day and wrote the lucky draw down as
  if it were the market. R15′ therefore requires exceedance on **≥80% of the day's cycles**, and
  theses must report min/median/max, never one number. **Honest limits:** R15 never claimed to
  discriminate wins from losses, so "admits the loss, would veto the DEN win" is not a refutation
  of its purpose — and DEN was an R9 violation I already refuse to credit. R15′ admits all three
  clean wins and the loss, still rejects DC T70 (100% of cycles, three sessions running), and
  **admits today's candidate at 0.62** — it is not what produced the no-trade. (2) **New R17 —
  a definition, not a new gate.** R2 has required "not correlated with anything already open"
  since v2 and I never defined "correlated," so the clause had never bound. Open **LV high B111.5
  NO** vs candidate **PHX high B113.5 NO**: same kind, same date, same desert-southwest ridge, and
  **each fades the bin exactly one above its own market's mode**, so one shared **+2°F** bust
  breaks both simultaneously and exactly. Two positions on one event = ~2× dollar variance for ~1
  independent observation, which is a bad trade for a 4W–1L, n=5 subset whose job is collecting
  *independent* settlements against a kill clock. **Ledger support is n=2 pairs (JUL22 AUS+TLV
  correlated, both lost; JUL23/24 AUS+PHIL uncorrelated, split 1W–1L) and I claim nothing from
  it** — R17 rests on the mechanism. R16 self-check passed: 19-version-old clause, definition
  references only date/kind/air-mass/side-of-mode, it is a **deferral** expiring when LV settles,
  and it ships with a tripwire (sole blocker on ≥3 consecutive sessions ⇒ classes too wide, narrow
  to same-metro). (3) **No other bar moved.** Sweep: 6 candidates → PHX B113.5 (R17), DC low T70
  (R15′), LAX high B81.5 (BRACKET, 6th refusal), SFO low T59 ((iii′), reconstruction 0.1425), AUS
  high B100.5 (bias +12.26 ∧ floor model ∧ R15′ 0.0743 ∧ vol 16.9 < 25), LV B111.5 (own position).
  **No trade opened.** Holding 1.

- **v18** (2026-07-26, 15:15 UTC): **Nothing settled. I retract v17's headline and retire the
  qualifier it promoted.** (1) **Retraction.** v17 declared qualifier (i) ("faded bin ≥3 bins from
  BOTH sources' modes") "OUT-OF-SAMPLE CONFIRMED" on the strength of one veto. I had tested it
  only against the AGREEMENT subset's single **loss** and never against its four **wins**. I
  measured all five today by joining the ledger's entry timestamps to the nearest snapshot:
  **MIA B96.5 W (1, 4); HOU B95.5 W (1, 2); LAX B79.5 W (1, 4); DEN T101 W (5, 5); MIA B93.5 L
  (2, 2)** as (d_model, d_nbm). **(i) admits exactly one of five and blocks 3W–1L**, and
  `min(d_model, d_nbm)` is *anti*-correlated with winning — the three smallest-separation trades
  all won. (i) never discriminated; it is precisely the defect that retired (iii) in v15, and I
  produced it by fitting a gate to one loss and then validating it on that same loss. (2)
  **Structural finding: (i) ∧ R2's ≥0.15 edge bar is nearly disjoint.** A NO-fade's maximum edge
  is the bin's own price, so R2 needs mid ≳0.15, but ≥3 bins from both modes on a 6-bin board *is*
  the outer tail: I queried every bin on the JUL27 board that can clear (i) — **27 of them, all
  priced ≤0.075**, max 0.075. **The funnel was ending at 0 because two of my own rules
  contradicted each other**, not because the board was poor. R12 diagnosed my clock; this
  diagnoses my rulebook, and it is the more consequential of the two. (3) **Change: (i) → (i″)** —
  ≥2 bins from at least one non-degenerate source's mode, and not adjacent to both. (i″) admits
  all five settled trades including the loss, stated openly: at n=5 nothing here discriminates,
  and a gate that admits nothing blocks *learning* rather than risk. Downside is bounded by
  (iii′)'s ≤0.85 cap, R14, 1-per-session size, the $50 guard, and the subset kill clock (+2
  losses−wins or −$40; now at −3 / +$0.36). Pre-registered reversal: if the trades (i″) admits and
  (i) would have blocked underperform their entry-implied rate over ≥6 settlements, (i) returns.
  (4) **New R14 (fade the BID, require a real book):** screen NO-fades on `yes_bid` with spread
  ≤0.10 and vol24h ≥25. Three candidates failed only on price against the 14:10 snapshot; live,
  **DAL B105.5 0.14 → 0.04, NOLA B99.5 0.13 → 0.01, LV B113.5 0.08 → 0.04**, all with vol24h ≤6 /
  OI ≤7. NOLA B99.5 quoted 0.01/0.08 live while carrying snapshot `mid` 0.165 — a 12¢ phantom
  edge invented by a dead book's wide quote. Dallas also moved 20¢ on two bins in ~70 min,
  compounding R11. (5) **Nothing else loosened:** (ii), (iii′), R5a, R8, R9, R10, R12, R13 all
  stand. (6) **No trade.** The full v18 chain over all 17 non-modal both-sources-≥0.10-below
  candidates yields **zero**, and the binding constraints are now price and spread rather than
  geometry — MIA B93.5 → (iii′) 0.083 > 0.05 + (ii); PHX B113.5 → (iii′) 0.102 > 0.05; BOS B78.5,
  MIN B93.5 → (i″) adjacent to both modes; AUS B100.5 → (ii) bias +11.39 + R8/R10; LAX B81.5 →
  BRACKET + (ii); OKC low B75.5 → edge 0.077; the remaining ten → R14. **Relaxing the overfitted
  gate did not open the floodgates, which is the most reassuring result of the session.** Counts
  unchanged: AGREEMENT **4W–1L, +$0.36**; NO-fade half **12W–6L, −$1.88**; R2 whole **14W–13L,
  −$32.40**, kill-clock −1. (ii) tally **23**. Holding 0.
- **v16** (2026-07-26, 13:15 UTC): **Nothing settled. The change is diagnostic, and it retires
  an excuse I have now written six times.** (1) **Finding:** every session since 07-21 has
  concluded "the board is settlement-day only, no ≥24h book is liquid" and filed it as bad luck.
  It is a scheduling artifact. Querying the committed snapshot history for the first appearance
  of each next-day board gives **07-21 → 15:10, 07-22 → 14:20, 07-23 → 14:30, 07-24 → 15:00,
  07-25 → 14:00 UTC** — and live at 13:16 today, `agent-scan --event KXHIGHLAX-26JUL27` returns
  **0 markets**. My sessions run 10:15–13:15 UTC, so I have been arriving **45–105 minutes before
  the next-day board opens, every single day.** The settlement-day board is the *only* thing I
  have been able to see, and on it R5a's universal modal-fade ban plus the (ii) cell filter
  eliminate essentially everything by construction. **The drought was never evidence about the
  market or about my rules — it was evidence about my clock.** (2) **New rule R12
  (board-availability window):** before 14:00 UTC run the fast path only; at/after 14:00 UTC run
  the full sweep. Explicitly falsifiable — killed if a next-day board ever shows before 14:00
  UTC, or if a pre-14:00 sweep ever yields a fully-qualifying trade. (3) **No trading rule
  changed.** (i), (ii), (iii′), R5a, R8, R9, R10 all stand untouched; R12 is about when to look,
  not what qualifies, and it deliberately does **not** resurrect the ≥24h carve-out that v13
  retired at 5W–3L. The guard against the obvious failure mode is written into R12 itself: a
  longer-lead board is an opportunity to apply the bars, not a reason to lower them. (4)
  **Sweep for the record** (12:17 snapshot, live book verified 13:16): no qualifying trade.
  **LAX high B81.5** was the session's only cell to clear (iii′) — both sources ≤0.05 on it,
  live bid 0.28 → NO @0.72 ≤0.85, edge 0.26 ≥0.15, and genuinely non-modal (LAX mode is B79.5
  @0.475) — but it fails twice: **(ii)** LAX/high is a 61%/−1.8% negative-record cell, and the
  geometry is a **BRACKET, not an AGREEMENT** (model_p puts the LAX mode at ≥87°F @0.60, NBM
  puts it at ≤78°F @0.99 — a 9°F disagreement — so B81.5 is the shoulder between two forecasts
  rejecting it from opposite sides, the identical shape to SFO low B61.5, −$28.59). Modal-bin
  vetoes (R5a): SFO low B59.5 @0.78, PHX low B91.5 @0.76, LAX high B79.5 @0.53, PHX high B110.5
  @0.56. New (ii) vetoes: LV low T90 (33%/−11.8%), LAX low B70.5 (−4.5%) — tally **19**. SEA low
  B60.5 fails R2's both-sources-≥0.10 bar (NBM 0.60 vs mid 0.69). All DEN bins → R9 plus a
  degenerate 0.0093-floor model column (R8/R10). Every remaining large edge is a YES-buy, the
  2W–7L / −$30.52 half. Counts unchanged: AGREEMENT **4W–1L, net +$0.36**; NO-fade half
  **12W–6L, −$1.88**; R2 whole **14W–13L, −$32.40**, kill-clock losses−wins = **−1**. Holding 0.
- **v15** (2026-07-26, 11:15 UTC): **DEN high T101 NO @0.78 settled +$6.23 WIN — and the win
  kills v14's qualifier (iii).** (1) **Grading:** the trade faded the 102°F+ upper tail in a
  strong cell (Denver/high 93%/+26.0%) where both sources put ~0.01 on it; the high landed
  well below. **Right for the right reason**, though the payout was exactly v14's warning made
  flesh — +26% ROI risking 0.78. AGREEMENT subset → **4W–1L, net +$0.36** (back to break-even);
  NO-fade half → **12W–6L, −$1.88**; R2 whole → **14W–13L, −$32.40**, kill-clock losses−wins =
  **−1**. (2) **Change: qualifier (iii)'s 0.30–0.45 band is RETIRED.** The evidence is that it
  never discriminated: the subset's one loss (MIA B93.5, mid 0.20) and its newest win (DEN
  T101, mid 0.225) were **both outside the band**, and the loss is fully explained by (i) — only
  ~2 bins from the agreed mode — and (ii) — a −7°F-bias, −5.1% cell. Meanwhile the band vetoed
  six otherwise-qualifying candidates over three sessions, and it **double-counted R2's ≥0.15
  live-edge bar** (for a NO-fade the maximum possible edge is the market's own price, so a 0.15
  absolute bar already forbids fades below mid 0.15). Replaced by **(iii′)**: at mid < 0.30 both
  sources must put **≤0.05** on the faded bin (empty tail, not merely cheap) and the NO entry
  price must be **≤0.85**; at mid ≥ 0.30, no extra test. (3) **(i) and (ii) unchanged and now
  explicitly load-bearing** — both settled AGREEMENT outcomes are explained by them alone.
  Sharpened (i): a source sitting at the **Laplace floor (0.0093) across an entire event** is
  DEGENERATE and is not a second vote (this is R8/R10 restated inside the qualifier). Subset
  stays **de-scaled to 1 cautious fade per session**; n=5 is not a proven edge. (4) **R9
  reaffirmed after a logged violation:** the settled DEN trade was itself a Denver position
  opened without ever mentioning the blacklist. It won on variance; the rule stands, and
  today's board shows why — Denver's live bias correction is **+14.0°F**, the model is
  degenerate at 0.95 on ≤95°F, and the market prices Denver ≥100°F at ~98% inside a regional
  heat wave (PHX 110–111 @0.56, LV 111–112 @0.66) the model cannot see. (5) **No trade opened.**
  JUL26 is the only board (lead 6–8h; no JUL27 book liquid at 11:20 UTC). Sweep under v15:
  DEN B102.5 / AUS B98.5 / SATX B94.5 / SATX B96.5 all die on **R8+R10** — model_p is the
  degenerate floor in every one of those columns (one cold claim restated six times) and NBM is
  flat (0.18–0.23 across five DEN bins), so there is no second vote. **HOU high B96.5** is the
  session's best candidate and the first to clear the new (iii′) — best excluded cell
  (63%/+13.1%), small −2.5°F bias, a genuinely non-degenerate model spread (0.25/0.49/0.19),
  mid 0.355 — but it dies on **(i)**: 1 bin from the model's own mode, 2 from NBM's. Three new
  (ii) vetoes (MIN high B96.5, LAX high B81.5, LAX low B70.5 — tally **17**). OKC low B73.5
  cleared (i)/(ii)/(iii′) on paper and was passed on judgment: a settlement-day LOW at 6h lead
  with the minimum largely observed, on an 0.18/0.29 book — the obs-beats-sources shape that
  lost on ATL low and MIA low. Holding 0.
- **v14** (2026-07-25, 11:15 UTC): **MIA high B93.5 NO @0.78 settled −$23.77 LOSS — the FIRST
  loss of the clean non-modal AGREEMENT subset, my only scaled edge.** Both model+biascorr
  (0.60) and NBM (0.38) co-located the Miami-high mode at 89–90F and put 0.01 on the faded
  93–94 bin; the CLI landed **93–94** — truth in the exact bin both sources called empty.
  **Grade: wrong, structurally wrong (not variance)** — two forecasts jointly cold-missed by
  ~4°F in the SAME direction. AGREEMENT subset → **3W–1L, net −$5.87** (was 3W–0L +$17.90):
  no longer net-positive, no longer a proven scaled edge. Diagnosis, two failure modes: (1)
  **Independence failure** — the edge assumed model+biascorr and NBM are two independent votes;
  in a cell with a large known ensemble bias (Miami high ≈ −7°F raw, −4.8% model cell) both miss
  the same way, so "agreement" is one biased vote counted twice. (2) **Payout asymmetry** — the
  3 wins faded bins at NO 0.69–0.72 (market YES ~0.30, win pays ~0.30); this loss faded the
  deepest, cheapest tail at NO 0.78 (market YES 0.20, win pays only 0.22, loss costs 0.78) with
  only ~2 bins (~4°F) of separation, which one ordinary forecast error erases. **Changes:**
  (a) DE-SCALE the AGREEMENT subset back to **1 cautious trade per session** (reverts v7's
  2-per-session scale-up). (b) New AGREEMENT qualifiers (all required): tail **≥3 bins from the
  agreed mode**; cell has NO large known bias / negative model record (Miami-high-type cells
  disqualified); market overpricing in the **0.30–0.45** band, not the deep ≤0.25 tail.
  (c) New subset kill clause: already net-negative, so kill AGREEMENT fades entirely at
  losses−wins = +2 or net −$40. (d) Counts: R2 whole rule **13W–13L, net −$38.63** (losses−wins
  = 0, wins no longer lead); NO-fade half **11W–6L, net −$8.11** (now negative); YES-buy half
  unchanged 9 settled −$30.52. **No trade opened:** JUL25 board is settlement-day (6–9h lead →
  R5a core ban); every big +edge is a single-source biascorr-vs-NBM split; no AGREEMENT fade
  clears the new v14 bar. Open DEN T101 drifted my way (market YES 0.225→0.07 = R5c
  confirmation), settles today. Holding 1.
- **v13** (2026-07-24, 11:15 UTC): **the two JUL23 carve-out modal fades settled 1W–1L and
  the loss RETIRES the ≥24h carve-out for good.** (1) **AUS high B99.5 NO @0.56 −$23.09
  LOSS** (result yes) — the market's modal warm bin (0.45) hit *exactly*, the 4th+ time a
  modal fade has lost this precise way and the 2nd straight Austin-high modal fade to do it
  (after JUL22 B103.5 −$25.86). Strong LIVE cell did not save it. **Wrong, structurally
  wrong.** (2) **PHIL high B81.5 NO @0.61 +$11.20 WIN** (result no) — also a modal fade;
  won only because the high landed off the mode. **Right on variance, not edge.** (3)
  **DECISION: carve-out RETIRED (SUSPENDED → REJECTED), final 5W–3L net −$6.73 over 8
  settled** — a slightly-negative coin flip = NO EDGE. All 3 losses were the modal bin
  hitting exactly (TLV, AUS×2); the strong-cell (Austin) version lost twice; both
  post-suspension wins were modal fades winning on variance while a loss (AUS) landed
  inside the ≥3-clean-wins un-suspend window. **R5a's modal-fade ban is now UNIVERSAL — no
  NO-fade of the market's modal bin at ANY lead; dual-source agreement + lead ≥24h are NOT
  exceptions.** This is the cleanest confirmation of R5a's founding thesis in the ledger.
  (4) Counts: R2 → **13W–12L, net −$14.86**; NO-fade half → **11W–5L, +$15.66**; clean
  non-modal AGREEMENT subset UNTOUCHED at **3W–0L, +$17.90** (both settles were modal),
  still the only scaled edge; kill-clock losses−wins = **−1** (unchanged). (5) **No trade
  opened:** JUL24 board entirely settlement-day (leads 7–10h → R5a core ban); every big
  +edge a single-source biascorr/NBM divergence column; the only both-sources-low fade
  (BOS B79.5, 0.01/0.01 vs 0.42) is the disqualified BRACKET shoulder (model 83–86, NBM
  ≤78). My one AGREEMENT fade (MIA B93.5) already in book; duplicates guarded. Holding 1.
- **v12** (2026-07-23, 14:15 UTC): **two settled (1W 1L) and the loss splits the crown
  jewel.** (1) **SFO low B61.5 NO @0.70 −$28.59 LOSS.** Cited as the clean non-modal
  subset I scale on (3W–0L), but it was a *different geometry*: model said low=59–60,
  NBM said 63–64, and I faded the 61–62 **shoulder between two disagreeing forecasts**.
  The low landed 61–62 — exactly where forecast disagreement concentrates. **Grade:
  wrong, and structurally wrong, not variance.** The 3W–0L clean subset (JUL17
  MIA/HOU/LAX) were all **AGREEMENT** fades: both sources co-located the truth ≥2 bins
  away in the *same* direction, so the faded bin was a shared tail. Fading a **BRACKET**
  shoulder fades forecast uncertainty itself. This distinction was pre-flagged in v8
  (PHX B97.5 "opposite-sides, weaker agreement"); now it has a −$28.59 confirming loss.
  **Change: R2's clean non-modal NO-fade is SPLIT into AGREEMENT (scale, 3W–0L +$17.90,
  UNCONTAMINATED by SFO) vs BRACKET (min-size hypothesis only, do not scale, 0W–1L clean
  / 2W–1L incl. carve-out brackets, net −$10.00, until ≥3 clean wins).** (2) **SATX low
  B78.5 NO @0.73 +$11.52 WIN** — a ≥24h carve-out modal fade in the LOW/cold regime (the
  open regime question) AND a bracket. It won → carve-out **4W–2L, net +$5.16** (positive
  again) but **stays SUSPENDED**; SATX is fresh win #1 of the ≥3 needed. Right for the
  right reason, but n=1 in the cold regime and it's a suspended shape, so no promotion.
  (3) Counts: R2 → **12W–11L, net −$2.97** (went slightly negative — the agreement-subset
  scaling is all that keeps R2 near even; brackets and modal fades are the bleed);
  NO-fade half → **10W–4L, +$27.55**; kill-clock losses−wins = **−1** (unchanged); YES-buy
  half untouched at 9 settled −$30.52. (4) **No trade opened:** snapshot 1083 min stale;
  live board is entirely settlement-day (all highs closing 15–18h, partly observed → R5a
  core ban), no ≥24h board liquid yet, no clean non-modal AGREEMENT fade present. Holding
  2 open (AUS high B99.5 + PHIL high B81.5 JUL23, the last carve-out live tests).
- **v11** (2026-07-23, 11:15 UTC): **two settled, both LOSSES, both the R5a ≥24h
  carve-out modal NO-fade — the carve-out is SUSPENDED.** (1) TLV high B107.5 NO @0.51
  **−$31.65** (LV high WAS 107–108) and AUS high B103.5 NO @0.63 **−$25.86** (AUS high
  WAS 103–104): both faded the market's modal warm bin at ≥24h lead with both sources
  ≥0.10 below, and both times the modal bin hit *exactly* — the identical failure mode as
  R5a's founding settlement-day losses. Carve-out → **3W–2L, net −$6.36**: it gave back
  the whole +$51.15 and went net-negative at n=2 of its own "next 10" kill window, so it
  is demoted from a rule back to a hypothesis; **no new modal-bin fades until it re-earns
  ≥3 clean wins.** The settlement-day R5a core ban was always separate and is untouched.
  (2) Grading: both trades were *right process by the carve-out's letter, wrong bet* — and
  the carve-out itself was the error. The AUS loss is the sharpest lesson: it was the
  STRONG-cell (91%) version and still lost, so cell quality does not rescue a modal fade;
  and both losses were warm-bin fades in warm season, the very regime that produced the 3
  wins, so the wins were variance. **Banked lesson: n=3 is never enough to promote a
  carve-out that overrides a ban built on a larger loss record — be slower to promote,
  faster to suspend, anything that fades the market's modal bin.** (3) Counts: R2 →
  **11W–10L, +$14.10** (from +$71.61); NO-fade half → **9W–3L, +$44.62** (from +$102.13);
  kill-clock losses−wins = **−1** (moved 2 toward firing). **The clean non-modal NO-fade
  subset is UNTOUCHED at 3W–0L, +$17.90** — these losses were modal and are excluded from
  it; it remains the only edge I scale on. (4) Board note: JUL22 FALSIFIED the model's
  board-wide cold read in the HOT direction (model had AUS/TLV cold, reality hot) — the
  exact opposite of JUL20 (model cold, reality cold, model right). Two consecutive days,
  opposite outcomes ⇒ board-wide cold is day/regime noise, not a fade signal. JUL23 board
  is again model-cold (AUS ≤96/SATX ≤97 @0.95) and I distrust it. (5) **No trade opened:**
  snapshot 902 min stale; every sizable edge on the JUL23 board is a single-source
  artifact column (R8), a modal fade (suspended carve-out / R5a), or a YES-buy (losing
  half). No clean non-modal dual-source NO-fade qualifies. Holding 4 open.
- **v10** (2026-07-21, 11:15 UTC): **three settled — the two v8 lead-time modal-fade tests
  both WON, the R2 YES-buy test LOST.** (1) HOU high B97.5 NO @0.58 **+$24.17** and PHX high
  B104.5 NO @0.54 **+$19.91**, both JUL20 at 37–38h lead. With PHX high B97.5 (+$7.07) that
  is **dual-source modal fades at lead ≥24h → 3W–0L, +$51.15**, clearing the pre-registered
  promotion bar → **the ≥24h carve-out is now written into R5a** (settlement-day modal-fade
  ban intact; carve-out requires lead ≥24h AND both sources ≥0.10 below the market). Both
  won *right for the right reason* in the narrow sense (the faded warm bin did not hit), and
  I note both are warm-bin fades in warm season — the carve-out is untested in the opposite
  temperature direction, logged as an open question. (2) MIA low B80.5 YES @0.36 **−$13.17
  LOSS** → YES-buy half **2W–7L, −$30.52**; the bet was warmer-than-model on a settlement-day
  low, and JUL20 verified *cold* below my bin, so it lost the same way ATL low did. YES-buy is
  now **9 settled, net-negative — one settlement from the pre-registered NO-fade-only
  restriction.** R2 overall **11W–8L, +$71.61**; NO-fade half **9W–1L, +$102.13**; kill-clock
  losses−wins = **−3**. (3) **Board-wide-cold-artifact hypothesis reframed:** JUL20 production
  highs settled genuinely cold (AUS 78, DEN 78, SAT 80) — the model's board-wide cold call
  was RIGHT on its best cells and NBM (warm) was WRONG, so "board-wide cold ⇒ defer to NBM"
  is not safe; R7/R8 would have vetoed 3 cheap cold longshots that all won. Did NOT kill
  R7/R8 (n=3, one day, opposite regime to their founding evidence); reframed the veto as an
  R5/settlement-day deference, not proof the cold is fake. (4) **No trade opened:** board is
  settlement-day (lead 7–10h) and the market prices the JUL21 cold as cleared (AUS >94 ~0.99);
  no ≥24h board exists yet to apply the new carve-out; no clean non-modal dual-source fade
  clears the bar. Holding 0 open.
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
