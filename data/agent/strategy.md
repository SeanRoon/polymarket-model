# Agent strategy playbook

**Version: v32** (2026-07-28 08:15 UTC — **nothing settled, and the snapshot is byte-identical to the one
I swept "in full" two hours ago — so by R20 this hour should have been a fast path. It was not. I ran the
funnel as a QUERY instead of reading the top of the edge-sorted view, and found FOUR qualifying candidates
that two prior "full sweeps" had enumerated away, including a whole DIRECTION I had never screened. One new
rule (R22), one tripwire counting convention fixed, one misreading of my own R19′ table corrected. All four
candidates refused on rules that already existed. Zero trades.**)
`agent-settle settled=0 still_open=1`. Newest snapshot **0610.parquet (06:17 UTC, 121 min old)** — the same
file the 06:20 and 07:15 sessions used; re-checked mtime **after** the pull per the 06:20 addendum, nothing
new came down. LV JUL27 B111.5 is **closed** (08:00 UTC) with `result` still empty — awaiting settlement.

**1. NEW — R22: my "full sweep" was reading the top of a sorted list, and the top of that list is the one
place R13′ guarantees candidates cannot be.** The 06:20 addendum called itself a full re-sweep of 0610 and
concluded: one high-side survivor (MIA B94.5), "everything else" being a blacked-out low, an R21 cell, or an
already-modal bin. **That enumeration is false, and I proved it by writing the funnel as SQL against the same
file.** Four qualifying bins on that board are none of those three things:

| candidate | shape | model_p | nbm_p | snapshot mid | R18 ratio | why it was missed |
|:---|:---|--:|--:|--:|--:|:---|
| DAL high B102.5 | **YES-buy** | 0.806 | 0.427 | 0.295 | — | wrong *direction* — never screened |
| LV high B111.5 (JUL28) | NO-fade | 0.009 | 0.029 | 0.290 | 0.423 | below the read-off point |
| PHIL high B81.5 | NO-fade | 0.083 | 0.095 | 0.325 | 0.890 | below the read-off point |
| OKC high B102.5 | NO-fade | 0.139 | 0.224 | 0.370 | 0.961 | below the read-off point |

**The mechanism is R13′ turned against me.** R13′ says a bin's both-sources-below gap is bounded above by
the price the market put there, so the largest gaps only exist where the market placed its mass — i.e. **the
top of an edge-sorted view is structurally the modal bins**, the exact set R5a bans. I have been reading the
first ~15 rows of `agent-model-view`, adjudicating the modal bins I found there, and calling the funnel
empty. **R13′ was telling me for five sessions that my candidates live in the middle of that list, and I
kept reading the top.** The DAL row is the worse half: `agent-model-view` sorts by **signed** edge, so a
YES-side candidate and a NO-side candidate never appear near each other, and **I had never once enumerated
the YES direction** — R2 explicitly has a YES-buy half (2W–7L, −$30.52) that I have not screened for in
weeks. A losing sub-rule I never look for is not evidence that the shape does not occur.
**R22 operationally:** the funnel is a **query over the newest snapshot**, run in both directions
(`model_p − mid ≥ 0.10 AND nbm_p − mid ≥ 0.10`, and the same with the signs reversed), with modality and the
R18 ratio computed per event — never a read of the sorted view's top rows. The sorted view is for orientation
only. **R16 self-check:** R22 is a procedure, not a gate; it *increases* candidate supply; and every one of
the four candidates it surfaced today was then refused on pre-existing rules. A rule adopted in the loosening
direction that produced zero trades on adoption day is not one I reverse-engineered to let myself trade.
*Kill if: over ≥5 boards the query surfaces nothing the sorted-view read did not already contain — then the
truncation was costing me nothing and R22 is ceremony.*

**2. All four refused, each on a rule that already existed — no bar was moved to accommodate any of them.**
**DAL high B102.5 (YES @0.30) → R5(b), and it is the DAL T101 shape verbatim.** The tape across nine
committed cycles: B102.5 mid **0.375 → 0.445 → 0.305 → 0.320 → 0.295 → 0.255 → 0.255 → 0.275 → 0.295**
while B100.5 ran **0.285 → 0.345 → 0.395 → 0.445 → 0.495 → 0.510 → 0.485 → 0.515 → 0.545** — a monotone
**+0.26** climb into the bin my sources reject and a **−0.15** slide out of the bin they like, over ~15h.
Meanwhile `model_p` went 0.25 → 0.71 → 0.82 → 0.806. **The edge grew from 0.27 to 0.51 and roughly half of
that growth is pure adverse price movement**, which is R5(b)'s definition of a trade not to take. NBM
corroborates the market, not me: q50 drifted **102.50 → 102.46 → 102.35**, cooler each cycle — NBM
*followed* the market, the same detail that strengthened the DAL T101 refusal in v23.
**LV high B111.5 JUL28 → (ii‴), re-confirmed on a fresh cycle.** This is (ii‴)'s own founding case and it
still fires: Las Vegas/high NBM signed error over JUL22–26 is **−1.77, −2.29, −3.73, −0.97, −2.91, mean
−2.33°F, cold 5 of 5**; today's q50 **108.56 + 2.33 = 110.89** lands **inside** the faded 111–112 bin's
support [110.5, 112.5) — and **JUL26 realized 111**, in that exact bin. Everything else about it is clean
(non-modal, R18 ratio 0.423 mid-support, both sources ≤0.05, NO entry 0.72, 2¢ spread), which is precisely
why (ii‴) exists.
**PHIL high B81.5 → BRACKET *and* (ii‴), two independent kills.** The sources are not agreeing: model's mode
is **T84 @0.454** (≥85°F) and NBM's is **T77 @0.578** (≤76°F) — they reject the 81–82 bin **from opposite
sides**, 8°F apart, with the market sitting between them. That is the SFO low B61.5 shape (0W–1L, −$28.59):
fading a bracket shoulder is fading forecast *disagreement*, and the truth lands there disproportionately.
Independently, Philadelphia/high NBM runs **−2.20°F cold, 5 of 5** (−4.41, −1.43, −2.39, −2.22, −0.54), so
correcting q50 76.28 → 78.48 moves it **toward** the bin I would be selling. Also worth naming: PHIL q50
**76.28** against a market mode of 83–84 is the **v24 Northeast stale-18Z cold displacement** reappearing at
`nbm_lead_hours` **27**, not an edge.
**OKC high B102.5 → BRACKET + R18 at the worst ratio I have ever screened.** Model's mode is **B104.5
@0.750**, NBM's is **B100.5 @0.457**; the faded 102–103 bin is the shoulder between them. And the market
prices B104.5 @0.385 vs B102.5 @0.370 — an **R18 ratio of 0.961**, outside my observed support of 0.33–0.76
and worse than the 0.948 that R18 was written to refuse. This is a genuine two-way coin flip, not a tail the
market overprices. *Noted for the record:* (ii‴) does **not** fire here — OKC/high's NBM error is +2.10,
+2.24, −0.31, −1.84, −1.60, **mean +0.12, signs mixed 3/2** — so the rule is discriminating between cells
rather than blanket-vetoing, which is the anti-learning-blocker evidence v31 asked for.

**3. (ii‴)'s firing ratio, re-checked as v31 promised — and the counting convention fixed.** v31 flagged
that (ii‴) fired on 3 of 4 non-modal survivors and worried it was "eating the funnel." On today's properly
enumerated board it fires on **3 of 4 NO-fades again** (LV, PHIL, MIA) — but that raw ratio is the wrong
statistic, and I was about to narrow a rule on it. **(ii‴) is the SOLE blocker on exactly 1 of 4** (LV
B111.5): MIA is disqualified independently by (ii′), PHIL is independently a BRACKET, OKC it does not touch.
**Convention, adopted here and applied to every anti-learning-blocker tripwire I own (R17's, (ii″)'s,
(ii‴)'s): count SOLE-blocker firings, not firings.** A veto that co-fires with an independent kill costs me
nothing and cannot be "eating the funnel"; only a sole blocker removes a candidate I would otherwise have
taken. This is how R5(b)'s veto log has always been counted ("R5(b)'s FIRST clean **sole-blocker** firing")
— I simply never generalized it. **(ii‴) sole-blocker count: 1.** Not narrowing.

**4. CORRECTION — I have been misreading R19′'s own staleness table for four consecutive sessions.**
Sessions at 04:15, 05:15, 06:15 and 07:15 all quoted "R19′'s 60–110 min overnight baseline." **That row is
the 11:00–23:45 UTC row.** R19′'s table reads: 01:00→05:00 = **3h20m–4h05m**; 05:00→10:00 = **2h10m–3h35m**;
11:00→23:45 = 60–110 min. So the 06:15 session's disclosure ("156 min, **outside** the 60–110 baseline") was
owed under a misreading — 156 min at 06:15 UTC is *inside* the 2h10m–3h35m morning band and disclosure-free.
Today's 121-min snapshot at 08:15 UTC is likewise **normal, in fact fresher than baseline**, and I owe no
disclosure. This is the exact error R19′ was written to stop ("say N minutes old against an X-hour normal
**for this hour**") and I reintroduced it by quoting the wrong row from memory. No refusal in those sessions
rested on it — they stood on (ii‴), R5a and R21 — but a premise carrying rhetorical weight should be right.

**Position:** LV high **JUL27** B111.5 NO (30 @ 0.70, $21.45 at risk) — market **closed** at 08:00 UTC,
`status=closed`, `result` empty, book gone. Marks ~+$8.55 on the last two-sided quotes. **Not settled, not
graded** — `agent-settle` decides, and it returned `settled=0` this hour.

**Superseded header (v31, 2026-07-28 04:15 UTC — **no paper trade settled, but NEW GROUND TRUTH arrived and it
closed the biggest open question in this playbook: I now know exactly WHY the Austin/San Antonio/Denver
high resolutions are wrong, and v30's stated mechanism — "a parser signature" — was WRONG. One rule
amended (R21), no new rules, zero trades.**)
`agent-settle settled=0 still_open=1`. Newest snapshot **0340.parquet (04:17 UTC, 35 min old)** — the first
new file in **~3.5h**, so R20's byte-identical fast path does **not** apply and I re-swept the JUL28 board
in full on fresh sources. Well inside R19′'s 60–110 min baseline; no staleness disclosure owed.

**1. AMENDED — R21's mechanism, established from the raw CLI text rather than inferred from symptoms.**
JUL27's CLI posted for exactly three stations — **KAUS, KSAT, KDEN**, the three R21 cells — which handed me
a direct test. The values: AUS high **80**, SATX high **80**, DEN high **83**, against late-July normals of
98 / 96 / 90. v30 called this "a parser signature, not weather." **It is neither.** The parser reads the
document correctly; the *document is the wrong document*. Every one of those files is stamped
**`VALID AS OF 0700 AM LOCAL TIME`** (Denver: 0600), i.e. it is an **intermediate morning CLI covering only
midnight→dawn**, and its `MAXIMUM` is the overnight carryover max: Austin `MAXIMUM 80 12:05 AM`, San Antonio
`80 12:45 AM`, Denver `83 1:16 AM`. The CLI's own DEPARTURE-FROM-NORMAL column says **−18 / −16 / −7**.
**Three independent predictions of this mechanism, all confirmed:** *(i)* only `high` breaks, because the
daily min *is* in-window (`MINIMUM 74 5:40 AM` etc.) — matches the observed high-only corruption exactly;
*(ii)* the error equals (afternoon high − overnight max), which is the observed 11–25°F; *(iii)* it should
be confined to the offices that issue the intermediate product — and scanning `raw_text` across **all 20
stations, exactly KAUS/KSAT/KDEN carry the stamp and the other 17 carry none. Zero false positives, zero
false negatives.** A clean partition is as close to proof as this exercise gets.
**Why the amendment matters operationally rather than just intellectually:** v30's reopening test was
"re-run the market-settlement cross-check monthly, reopen when they agree." **That test can never fire** —
this is a structural fact about which product KEWX and KBOU publish, not an intermittent fault, so those
three cells would have stayed closed forever on a criterion incapable of clearing. v31 replaces it with the
stamp test, which *can* fire the day the fetcher moves to the end-of-day product.
**And I retracted an overreach of my own while I was in there.** v30 claimed this "retro-explains the
degenerate model columns I have been vetoing under R8/R10 for weeks." It explains the AUS/SATX/DEN ones —
via a derivable chain, `compute-bias` → +12°F phantom correction → ensemble pushed off the bottom of the
board → `model_p` 0.95 on T97. It does **not** explain **LAX/high (model 0.95 on T83)** or **Chicago/low
(model 0.84 on T64)**, both degenerate on *this* board at stations with clean, unstamped resolutions.
**R8/R10 keeps independent work and a second degeneracy mechanism is still unidentified.** Saying so costs
me a tidier story and is the difference between a finding and a narrative.

**2. NO new rule, deliberately — and (ii‴) got a real out-of-sample confirmation instead.**
I measured NBM's signed error (`nbm_q50 − realization`) over JUL22–26 across every valid cell, 183 pairs:
**highs run −0.73°F cold (70% of days), lows run +1.40°F warm (only 27% cold)** — NBM under-forecasts the
diurnal range, with the low-side warm bias about double the high-side and far more consistent (16 of 20 low
cells warm; Austin +4.03, San Antonio +3.42, Houston +3.07, Seattle +3.03, Denver +2.79, OKC +2.63). The
high-side splits *geographically* rather than uniformly — coastal/southwest cold (Miami −3.72, Atlanta
−3.11, Boston −2.86, LAX −2.43), Plains warm (Dallas +2.22, OKC +1.97) — so "highs run cold" is **not** a
venue-wide truth and I am not writing one.
**I drafted a rule off this and then killed it, which is the point of this section.** The natural R22 —
"raise R2's live bar to 0.20 for any fade of a low bin below the forecast" — **would have changed exactly
zero decisions on this board**, because (ii‴) already killed every such candidate. A rule with no bite,
added on the strength of one 5-day window inside a single synoptic regime, is the churn pattern I flagged
at v29/16:15 and would repeat v17's retracted (i). **The measurement is recorded as evidence for (ii‴), not
promoted to a rule.** What it genuinely buys me: it **defuses (ii‴)'s own "eating the funnel" kill-clause.**
(ii‴) fired on **3 of today's 4 non-modal survivors** — up from 2 of 6 in v30, and close to "most of the
board." The measurement says that is **not miscalibration**: a widespread real bias *should* produce
widespread firing, and R13′ sends me hunting the 2nd-priced bin, which in a heat wave sits on the dangerous
side. I am leaving (ii‴)'s threshold alone and re-checking the ratio next session.
*Honest caveat, stated not buried:* 5 consecutive days in one heat-wave regime is **not** an independent
sample. Re-measure over a regime change before this evidence is leaned on any harder.

**3. Zero trades. Full JUL28 adjudication, and R13′ posts a fifth consecutive confirmation.**
Every one of the largest gaps on the board is the market's **modal** bin → **R5a** (LAX high B78.5, SFO low
B59.5, CHI low B68.5, DAL low B79.5 & high B100.5, NYC low B69.5, PHIL low B71.5, PHX low T92, ATL low
B75.5, AUS low B73.5, OKC low B73.5 & high B102.5, NOLA high B94.5, PHIL high B81.5, NYC high B79.5). Four
non-modal AGREEMENT candidates survived to real adjudication and **all four died, three of them to (ii‴)
measured fresh this session, not carried forward:**
**LAX high B80.5** (both sources 0.01 vs mid 0.325, R18 ratio 0.589 ✓, live 0.32/0.33 on 6,035 vol, edge
0.31 ✓) → **R8/R10** (model 0.95 on T83, which the market prices 0.05 and NBM 0.01 — one usable source, so
R2's dual-source premise fails) **and independently (ii‴)** (cell −2.43°F cold, 5/5; correcting q50 ~76.5
upward moves *toward* the 80–81 bin I would be selling).
**MIA high B94.5** (0.05/0.01 vs mid 0.255, ratio 0.622 ✓, live 0.25/0.26, edge 0.20 ✓) → **(ii‴), and this
is the cleanest firing the rule has had.** Miami/high is **−3.72°F cold, 5 of 5 days**, and **JUL26 already
ran the experiment: the high realized 94 — inside the exact bin — against NBM's 86.11, a −7.89°F miss.**
Selling 94–95 here is selling the outcome that just happened. (ii′) disqualifies the cell too.
**OKC low B71.5** → **(ii‴)**, and it hurt: it cleared everything else including R2's live bar **by one
cent** (bid 0.17 − 0.01 = **0.16** vs the 0.15 floor), R18 (0.514), (iii′) (both at floor, NO entry 0.83 ≤
0.85), (i″) (d=3 from both modes). But OKC/low is **+2.63°F warm, 5 of 5**, and the faded 71–72 bin sits
*below* q50 78.88 — the bias points straight at it. **Refused.**
**CHI low B66.5** → **R8/R10** (model 0.84 on T64, market 0.015), **(ii‴)** (+1.50°F warm, 5/5, faded bin
below q50), and an **8¢ spread** (0.28/0.36) on 575 vol that R14 would have discounted anyway.
Remaining non-modal bins all fail **R18**: NYC high B77.5 (0.878), PHIL high B79.5 (0.829), BOS high B81.5
(0.938), SATX low B74.5 (0.976) — all far outside the 0.33–0.76 support. AUS/SATX/DEN high → **R21**.
Denver → **R9**. **No trade opened. Holding 1.**
**Position:** LV high **JUL27** B111.5 NO @0.70 (30 lots, $21.45 at risk) — B109.5 quotes **0.99/1.00** and
my faded 111–112 bin **0.00/0.01** on 7,413 contracts, so NO marks ~0.995 ⇒ **≈ +$8.85** with **4h to
close**. **Quoted as decided; not settled, not graded** — `agent-settle` decides, not the tape.

**Superseded header (v30, 2026-07-27 19:15 UTC — **the most important session this playbook has had. Nothing
settled, but I went looking for a bias measurement to adjudicate ONE candidate and found that the
GROUND TRUTH ITSELF IS CORRUPT in exactly the three cells the model calls its best. Two new rules,
both TIGHTENINGS, and the trade I have chased for three sessions finally cleared every price gate —
and I refused it on evidence I went and measured.**)
`agent-settle settled=0 still_open=1`. Newest snapshot **1855.parquet (18:57 UTC, 18 min old)** — the
sources genuinely moved since last session's 1720 file, so **R20's subset shortcut does not apply** and
I re-swept the whole 36-event JUL28 board on new mids. NBM cycle **06:00 UTC**.

**1. NEW — R21: the NWS CLI resolutions for Austin/high, San Antonio/high and Denver/high are WRONG by
11–25°F, and those are the three cells whose track record my whole piggyback premise rests on.**
I set out to measure NBM's per-cell bias (for §2 below) and the table returned Denver/high **+17.6°F**,
San Antonio/high **+15.8°F**, Austin/high **+15.4°F** — magnitudes no forecast bias plausibly reaches in
late July. So I cross-checked `data/resolutions.parquet` against **the market's own settlement**: for
every event since JUL23, take the bin the market settled at ≥0.90 and ask whether the CLI value falls
inside it. **Across 17 cities every closed-bin settlement agrees — except three cells, which disagree
every single day:**

| cell | market settled | CLI says | error |
|:---|:---|---:|---:|
| Austin/high JUL23–26 | B99.5 / B95.5 / B97.5 / B96.5 | 88 / 80 / 79 / 78 | **−11 to −18°F** |
| San Antonio/high JUL23–26 | B98.5 / B93.5 / B93.5 / B94.5 | 88 / 82 / 78 / 78 | **−11 to −16°F** |
| Denver/high JUL23–26 | B88.5 / B95.5 / B100.5 / B102.5 | 69 / 70 / 77 / 79 | **−19 to −25°F** |

**Austin/low, San Antonio/low and Denver/low at the same stations parse correctly on the same days.**
Same station, same file, same day — only the `high` value is broken. That is a parser signature, not
weather. **Three consequences, and they reach backwards through my whole playbook:**
*(a)* **Austin/high (91%, +27.5%), Denver/high (93%, +26.1%), San Antonio/high (98%, +30.6%) are the
only strongly-positive cells in the entire 40-cell track record, and all three are scored against an
answer key that is wrong by 11–25°F.** Their ROI is not evidence of skill; it is an artifact of grading
against broken ground truth. This does not prove the cells are bad — it proves **their record carries no
information**, and **R1's piggyback premise ("Austin/high and Denver/high have long profitable
histories") is void for those three cells** until the resolutions are fixed.
*(b)* **It explains `model_bias_applied_f`.** `compute-bias` is mean(model_expected − actual) against
these same corrupt values, so the +12.5 (AUS), +11.0 (SATX), +13.4 (DEN) corrections I have been reading
as "ensemble bias" for weeks are **manufactured from bad ground truth** and are shifting those ensembles
by 11–13°F in the wrong direction.
*(c)* **It retro-explains R8/R10 and R9.** I have refused AUS/SATX/DEN highs for weeks on "the model
column is degenerate — 0.954 on the bottom bin." That degeneracy is the corrupt bias correction pushing
the whole ensemble off the board. **R9 (Denver blacklist) and R8/R10 were right for a mechanism I could
not see.** This is the rare case where a rule I adopted on symptoms turns out to have a real cause.
**R21 operationally:** treat `model_p`, `model_bias_applied_f` and the production track record as
**UNUSABLE for Austin/high, San Antonio/high and Denver/high**. NBM (`nbm_q50`) is unaffected — it is not
derived from resolutions — but a single surviving source cannot satisfy R2's dual-source premise, so
**those three cells are closed to me entirely** until the CLI values agree with market settlement again.
**Re-test monthly with the same market-settlement cross-check; reopen the moment they agree.**
*Honest scope:* this is a **read-only finding**. I may not touch the parser, `resolutions.parquet`, or
any code — and I have not. It is recorded here so future sessions of mine do not trust those numbers,
and flagged in the journal as something the operator will want to know about `weather/nws.py`.
*Caveat:* my cross-check flagged ~35 open-bin (`T*`) rows too; **those are my test's own boundary
handling, not corruption** — an open bin has one NULL strike, so my `lo ≤ v < hi` comparison fails on
NaN. Every one I inspected was actually consistent. **Only the closed-bin mismatches are real, and they
are confined to exactly those three cells.** Saying this is the difference between a finding and a scare.

**2. NEW — (ii‴): (ii″)'s single-day test misses by 0.14°F what a five-day measurement screams, and it
misses it on the one candidate I have wanted for three consecutive sessions.**
`KXHIGHTLV-26JUL28-B111.5` NO cleared **everything** this hour, live: R2 at the snapshot mid (model
0.028 / NBM 0.025 vs mid 0.245 ⇒ gaps 0.217 / 0.220), **R5a** (mode is B109.5 @0.605; B111.5 is the
2nd-priced bin, R13′'s hunting ground), **(i″)** (d_nbm = 2 from NBM's B107.5 mode, d_model = 1 — ≥2 from
one source and not adjacent to both), **(iii′)** (both ≤0.05; NO entry 0.76 ≤ 0.85), **(ii′)**
(`model_bias_applied_f` −1.82°F), **R18** (ratio 0.245/0.605 = **0.405**, mid-support), **R8/R10** (both
columns have real structure), **R9**, **R15′** (upper-tail reconstruction σ = (110.642 − 108.649)/1.2816
= 1.555 ⇒ P(110.5 ≤ X ≤ 112.5) = **0.010**, a genuine near-zero), and — for the first time in three
sessions — **R14 and R2's live bar**: live **bid 0.24 / ask 0.25, spread 0.01, vol24h 111, OI 93**, live
edge **0.24 − 0.028 = 0.212 ≥ 0.15**. The 26-lot placeholder book that killed it at 18:15 is now real.
**And (ii″) as literally written passes it by 0.14°F.** (ii″) looks at the most recent settled day only:
JUL26 Las Vegas high **realized 111°F** — *inside the bin I want to sell* — against NBM q50 **108.09**
(−2.9°F) and model mode B109.5 (−1.5°F), both cold. Larger error **2.86°F**, bar **3.0°F**. Waved through.
**So I measured the cell properly instead of taking the technicality.** NBM q50 vs the CLI (KLAS parses
correctly — it is not one of R21's three cells), last five settled days:

| date | realized | NBM q50 | error | model mode | model error |
|:---|---:|---:|---:|:---|---:|
| JUL22 | 108 | 106.23 | −1.8 | B107.5 | −0.5 |
| JUL23 | 112 | 109.71 | −2.3 | B110.5 | −1.5 |
| JUL24 | 114 | 110.27 | **−3.7** | B111.5 | −2.5 |
| JUL25 | 113 | 112.03 | −1.0 | B113.5 | +0.5 |
| JUL26 | **111** | 108.09 | −2.9 | B109.5 | −1.5 |

**Five of five cold, mean −2.33°F**, and the model mode cold on five of six. **The displacement points
straight at the bin I am selling:** sources centre JUL28 at **108.65**; correct by the measured +2.33°F
and you get **110.98** — the lower edge of the 111–112 bin. And **JUL26 already ran this exact experiment:
the high landed 111, in this exact bin, with these exact two sources putting 0.065 and 0.005 on it.**
**(ii‴), replacing (ii″)'s single-day trigger:** before any AGREEMENT fade, compute the cell's mean
signed `nbm_q50 − realization` over the **last 5 settled days**. If **|mean| ≥ 1.5°F**, the sign is
consistent on **≥4 of 5** days, **and** correcting the current central estimate by that mean moves it
**toward or into the faded bin**, the fade is **DISQUALIFIED**. The directionality is the point and (ii″)
lacked it: a cold bias only hurts a fade of a bin *above* the forecast — fading a bin *below* it, the
same bias is protection. (ii″) is subsumed; (ii′) is unchanged.
**Anti-learning-blocker count, measured not asserted.** Of 37 valid cells (the 3 R21 cells excluded), 17
carry a ≥1.5°F consistent bias — but the veto is **directional**, so on today's six R5a survivors it
fires on exactly **two**: LV high B111.5 (blocked) and OKC low B71.5 (blocked — cell bias **+2.17°F warm**,
faded bin 71–72 sits *below* q50 78.88, so the bias points at it). **The second is (ii″)'s own founding
case, reached by a better route** — a consistency check I would rather have failed than skipped.
**R16 self-check.** A **tightening** that refuses the candidate I have chased for three sessions, on a
quantity measured from CLI ground truth and committed snapshots that exist independently of my wanting
the trade, computed **before** the decision, and referencing only (station, kind) — nothing about B111.5's
geometry. That is the R16-safe direction. **Zero demonstrated discriminating power: n=0 settled trades
governed by it.** It says "my sources are systematically displaced toward the bin I want to sell," not
"this loses." Dressing it up further would repeat v17's retracted (i).
*Kill (ii‴) if: over ≥6 candidates it disqualifies, the blocked fades would have won at or above their
entry-implied rate. Narrow it if it ever fires on most of a board.*

**3. Zero trades. The full 36-event adjudication, and R13′ posts its strongest confirmation yet.**
Seventeen bins cleared R2's dual-source bar at the snapshot mid. **Eleven are the market's modal bin —
including all TEN of the ten largest gaps** (LV low T87, LAX low B68.5, HOU low B78.5, SFO low B59.5,
AUS high B99.5, CHI low B68.5, SATX high B97.5, PHIL low B71.5, MIN low B71.5, DAL low B79.5) → **R5a**.
That is R13′'s fourth consecutive confirmation and the cleanest: the gap on a bin is bounded above by the
price the market put there, so the biggest gaps can only live where the market put its mass. Of the six
survivors: **LV high B111.5 → (ii‴)** (above). **OKC low B71.5 → (ii‴)** and (ii″). **MIA high B94.5 →
(ii′)**, Miami/high disqualified outright. **PHIL high B79.5** dies three times — **R18** (ratio
0.265/0.275 = **0.964**, further outside the 0.33–0.76 support than the DAL candidate that founded the
rule), **R8/R10** (model puts 0.787 on T84, a bin the market prices 0.055 and NBM 0.005 — the column is
an artifact, leaving one usable source), and R5a-by-a-cent is doing no work at that ratio. **MIA low
B75.5 → R2's live bar** (bid 0.17 − model 0.046 = **0.124 < 0.15**). **LAX low T69 → R2's live bar**
(bid 0.11 − 0.009 = 0.101) **and (iii′)** (NO entry 0.89 > 0.85). **No trade opened. Holding 1.**
**What this hour actually proves.** For three sessions I recorded that R14 was the binding constraint and
that this candidate kept dying on price. This hour price cleared, every gate cleared, and the refusal had
to come from somewhere I had not looked — so I went and looked. **The rule that saved me was one I did
not have when the session started, and finding it required measuring my sources against ground truth
rather than reasoning about my own process.** That is the opposite of the churn pattern I flagged at 16:15.
**Position:** LV high **JUL27** B111.5 NO @0.70 (30 lots, $21.45 at risk) — live **0.17/0.18** ⇒ NO worth
**0.825**, mark **+$3.75**, the best since entry and a fourth consecutive favorable tick (B109.5 is 0.72
with 13h to close and the high forming now). **Stated against my own interest: the JUL27 twin going my
way is NOT evidence for the JUL28 fade.** One favorable unsettled intraday mark cannot outweigh a
five-day measured bias, and I have already been wrong-then-right about exactly this within four hours
(v25/v26). The consecutive-day correlation hypothesis parked at 16:15 **recurred** — this time the trade
was live and only (ii‴) stopped it; see Open hypotheses, still parked, still not needed.

**Superseded header (v29, 2026-07-27 16:15 UTC — **the first fully-covered next-day sweep in the history of this
playbook: R12's board finally listed AND my snapshot covered it, so all 36 JUL28 events were adjudicated
on real sources. It produced ZERO trades and ONE amendment — and the amendment is the first in this
stretch grounded in a VERIFIED FORECAST MISS rather than in reasoning about my own process.**)
`agent-settle settled=0 still_open=1`. Newest snapshot **1530.parquet (15:31 UTC, 52 min old at 16:23)** —
inside R19′'s 60–110 min baseline for this window, so **no staleness disclosure is owed this hour**;
today's file count recovered to 5. NBM cycle **06:00 UTC** (~10h), the freshest I have run on.

**1. NEW — (ii″): (ii′)'s bias veto is BLIND TO NBM, and today a settled outcome shows what that costs.**
(ii′) disqualifies an AGREEMENT fade when the cell has a large known bias, and it checks exactly one
number: `model_bias_applied_f`, the *model's* rolling error. **It says nothing whatsoever about NBM.**
That is a hole in the rule's own stated mechanism — the subset's only loss (MIA B93.5) failed *because
both sources missed the same way*, and a model-only bias column cannot detect that by construction.
**Founding measurement, and it is an outcome, not an argument.** Today's best-looking candidate on the
whole board was **`KXLOWTOKC-26JUL28-B73.5`** (73–74°F, snapshot mid 0.30, the 2nd-priced bin — exactly
where **R13′** says to hunt). It clears **R5a** (market mode is B75.5 @0.355), **(i″)** (d_model = 2 from
the model's B77.5 mode), **(iii′)** (both sources at the Laplace floor — a genuinely empty tail — and NO
entry 0.75 ≤ 0.85), **R14** live (bid 0.25, spread 0.07, vol24h 175), **R15′** (B73.5 is closed, near tail
is lower: σ = (78.881 − 76.908)/1.2816 = 1.539 ⇒ P(72.5 ≤ X ≤ 74.5) = **0.0022**, so NBM's 0.005 is a real
vote, not a discretization artifact), **R8/R10**, **R9**, and **R17**. It fails nothing I had written.
**Then I checked what those same two sources said about YESTERDAY in this same cell:**

| | JUL27 (low fully realized) | JUL28 (today's candidate) |
|:---|:---|:---|
| NBM q50 | **78.53** | **78.88** |
| model mode | B73.5 @0.491 / B75.5 @0.435 | B77.5 @0.694 |
| realization | **71–72°F** — market has B71.5 at **0.98/1.00** at 11:20 CDT | — |
| joint error | NBM **+6.8°F warm**, model **≈+2°F warm** — *same direction* | forecast essentially unchanged |

**Both sources busted warm on the same day in the same cell, and today they are repeating the identical
distribution.** That is not two independent votes; it is one warm-biased vote counted twice — (ii′)'s own
mechanism, firing on a cell (ii′) waves through, because `model_bias_applied_f` here is only +4.96°F and
NBM's +6.8°F miss is invisible to it. Fading 73–74°F on the strength of "both sources say 77–79°F" would
have been betting on precisely the forecast that just failed by 5–7°F.
**(ii″) operationally, run before any AGREEMENT fade:** take the most recent settled day for that
(station, kind); compare the realization against what `model_p` and `nbm_q50` said for that same day. **If
both sources' central estimates fall on the SAME side of the realization and the larger error is ≥3°F,
and the current cycle has not materially moved, the cell is DISQUALIFIED for AGREEMENT fades on today's
board.** (ii′) is unchanged and still applies; (ii″) is an additional veto covering the source (ii′) cannot see.
**Honest caveats, stated rather than buried.** *(a)* JUL27's CLI has not posted — `data/resolutions.parquet`
runs through JUL26 — so the realization above is the **market's own settlement-grade price** (0.98/1.00 on
B71.5 with the minimum long since formed), a proxy, not ground truth. The CLI confirms or refutes it
tomorrow and I will record which. *(b)* This is not a brand-new discovery: **R12″** already documented this
exact OKC-low bust from the intraday tape. What is new is the *scope* — R12″ blackouts a low during its
own observation hours; (ii″) carries the lesson **across days** into the next board's fade decisions.
*(c)* **Zero demonstrated discriminating power** — n=0 settled trades governed by it. Like R18, it says
"outside what my sources have earned," not "likely to lose." Dressing it up further would repeat v17's
retracted (i) overreach.
**R16 self-check, applied honestly.** It is a **tightening**, and it refuses a candidate I was actively
leaning toward — the opposite of reverse-engineering a gate to permit a trade. The quantity was measured
from data that exists independently of my wanting the trade (`nbm_q50` and a settled market price), and
it was measured **before** the decision. It is not fitted to this candidate's geometry: it references only
(station, kind, previous day's realization), nothing about B73.5. **Anti-learning-blocker count: on today's
36-event board (ii″) fired on exactly ONE cell.** If that count ever approaches "most cells," the rule is
eating the funnel and must be narrowed.
*Kill (ii″) if: over ≥6 candidates it disqualifies, the blocked fades would have won at or above their
entry-implied rate — i.e. a joint miss yesterday does not predict a joint miss today.*

**2. Zero trades, and every refusal names a rule and a number.** The board was 36 events, fully covered,
and this is the complete adjudication: **OKC low B73.5 → (ii″)** (above). **PHIL low T72** cleared (i″)
(d = 2/2), (iii′) (both sources at floor) and R18 (ratio 0.465) on the snapshot, then **R14** killed it —
snapshot bid **0.18 → live 0.05**, i.e. a NO entry of **0.95** and a live edge of 0.04 against R2's 0.15
bar. **LV high JUL28 B111.5** was the cleanest candidate I have screened in weeks — (i″) passes
(d_nbm = 2, d_model = 1, not adjacent to both), (iii′) passes (both ≤0.05), bias only −1.12°F, **R18 ratio
0.381** squarely inside the 0.33–0.76 support — and **R14 killed it too**: snapshot bid **0.22 → live
0.15**, NO entry **0.85**, live edge ≈**0.12 < 0.15**, on a **26-lot** book. **MIN low T72** fails (iii′)
at the live mid (0.28 < 0.30 with nbm 0.102 > 0.05) and R18 caps it to explore size anyway (ratio 0.918).
**AUS high B99.5** — my best cell — is refused three times over: **R5a** (it IS the mode, 0.455),
**(ii′)** (`model_bias_applied_f` = **+12.26°F**, larger than the −7°F that broke MIA), and **R8/R10**
(the model column is degenerate: 0.954 on T97, 0.009 on all five others). **LAX high B80.5** dies on
**R8/R10** — model 0.954 on T83, a bin the market prices 0.025 and NBM prices 0.005, so the whole model
column is an artifact and only one usable source remains. **DC low T72, CHI low B68.5, AUS low B73.5,
DAL low B79.5, ATL low B75.5, LV low T87** are all the market's modal bin → **R5a**. Denver → **R9**.
**No trade opened. Holding 1.**
**What this hour actually proves: R14 is the binding constraint on this playbook, not the source gates.**
Two of the three candidates that cleared every geometry, source and bias test died on a 5–7¢ collapse
between a 50-minute-old snapshot bid and the live bid. That is the same phantom-edge mechanism R14 was
founded on, now confirmed on a **long-lead** board where I had assumed the snapshot decayed more slowly.
**Position:** LV high JUL27 B111.5 NO @0.70 (30 lots, $21.45 at risk) — the JUL27 book quotes it near
0.30, so the mark is roughly flat. Note the coincidence worth watching: I nearly opened the **identical**
bin one day later, which R17 does **not** currently catch (its clause (b) requires the same settlement
date). Logged as an open hypothesis rather than adopted — R14 refused the trade anyway, and inventing a
rule I did not need is exactly the churn pattern I flagged an hour ago.

**Superseded header (v28, 2026-07-27 14:15 UTC — **nothing settled, no trade was mechanically possible on either
board, and the session's whole value is a RETRACTION: the "frozen cron" I have asserted in three
consecutive session headers does not exist. I measured the snapshot recorder's actual cadence for the
first time and it is a stable diurnal pattern I have been misreading as an incident since v25.**)
`agent-settle settled=0 still_open=1`. Newest snapshot **1230.parquet (106 min old)**; no new snapshot
commit upstream since 12:35 (checked twice, 14:16 and 14:19).

**1. RETRACTION — the cron was never frozen. R19 gets a measured baseline (R19′).** I have written
"the cron re-froze" (v25), "cron frozen a fourth consecutive session" (v26) and "the cron UN-FROZE"
(v27). I had never once checked what this cron's *normal* cadence is. Counting committed files:

| day | files | gap after ~01:00 | morning gaps (→~10:00) | afternoon/evening gaps | first snapshot after 12:45 |
|:----|------:|:---|:---|:---|:---|
| 07-22 | 13 | 3h25m | 2h50m, 2h40m | 60–110 min | **14:20** |
| 07-23 | 12 | 3h35m | 2h45m, 2h30m | 60–110 min | **14:30** |
| 07-24 | 13 | 3h35m | 2h45m, 2h40m | 60–110 min | **15:00** |
| 07-25 | 15 | 3h20m | 2h30m, 2h10m | 60–110 min | **14:00** |
| 07-26 | 15 | 3h35m | 2h45m, 2h10m | 60–110 min | **14:10** |
| 07-27 | 4 so far | 4h05m | 3h30m, 3h35m | — | *not yet at 14:19* |

**The nominal cadence is every 15 min (96/day). The delivered cadence is 12–15/day — about one run in
seven.** GHA throttles scheduled workflows on public repos, so this is a structural property of my data
source, not an incident. **Every "freeze" I flagged sits inside the ordinary distribution.** The worst
of them: at 10:15 (v25) I called the cron "re-frozen" over a snapshot that was **80 minutes old**, when
the baseline morning gap is **2h10m–2h50m** — that was not slow, it was early. v27's "the cron UN-FROZE"
is likewise empty: the 12:30 snapshot is the ordinary late-morning cycle (cf. 12:15 / 12:05 / 12:45 /
12:00 on the four prior days), and the "first fully-fresh sweep in five sessions" was just a sweep run
shortly after a cycle that lands at that hour **every single day**.
**Honest counter-evidence, stated rather than buried:** today genuinely IS slow. Its three gaps
(4h05m, 3h30m, 3h35m) all sit at or above the top of their respective observed ranges, and 4 files by
14:19 versus a 6-day median of ~6–7. So "today is at the slow end of normal" is correct; **"frozen" was
never correct, and "un-froze" was meaningless.**
**What this does NOT change:** no refusal is revisited. The DAL T101 refusals rest on R5(b), R20 and
R13′, not on cron pathology, and NBM's cycle age is a separately-recorded field (`nbm_cycle_utc`) that
was genuinely 16–18h stale — that half of R19 stands untouched. What changes is that I stop treating
ordinary morning staleness as a finding, and stop letting the word "frozen" do rhetorical work in a
refusal that is already justified.

**2. NEW — R12‴: the sweep predicate is SOURCE COVERAGE, not board listing.** Today is the first time
my hourly schedule has landed inside R12's advertised 14:00–15:10 window with the next-day board
actually live: `KXHIGHAUS-26JUL28` quotes a full six-bin book at **40h to close** at 14:16. **And I have
zero forecast coverage of it** — the newest snapshot (1230) predates the listing, so
`agent-model-view --min-lead-hours 20` returns `_none at this threshold_`: no `model_p`, no `nbm_p`, on
any JUL28 bin. R2 and R1 both require sources; with neither, the live book is the *only* input, and
trading off it alone is R20's manufactured-edge failure in its purest possible form. **A board that has
listed but that my newest snapshot does not cover is NOT sweepable.** The danger here is specifically
that this is the *good* board — 40h lead, the window R12 spent six sessions telling me I was missing —
so the pressure to substitute the tape for the missing model is at its maximum precisely when I have the
least to go on. That is R16's failure mode with a countdown clock on it.
**The scheduling half, and it is the actionable part.** The first snapshot to cover the next-day board
lands at **14:00 / 14:10 / 14:20 / 14:30 / 15:00** across the five measured days (median ~14:20).
**My 14:15 session races it and loses 4 days in 5; my 15:15 session has coverage 5 of 5.** R12's v17
advice ("git pull again a few minutes later") was calibrated to a 15-min cron that does not exist —
at the real cadence the wait is 5–45 minutes, not "a few." **Operationally: at 14:15, check coverage
once; if absent, take the fast path and treat 15:15 as the first real sweep of the next-day board.**
*Kill R12‴ if: over ≥5 days the 14:15 session does have coverage (then the cadence has changed and the
15:15 framing is costing me an hour of lead), or if a coverage-less sweep ever produces a candidate that
clears every gate on sources I did not have — which is impossible by construction, and saying so is the
point.*

**3. Zero trades, and today it is PROVABLE rather than a judgment call — R20 earns its keep by saving
the sweep.** JUL28: no coverage (R12‴). JUL27: the snapshot is byte-identical to the one v27 fully
adjudicated an hour ago, and **under R20 qualification is evaluated at the snapshot mid** — so the
qualifying set is *identical* to last session's, which was empty, while R20(b) lets live prices only
*add* vetoes. **The candidate set on JUL27 is therefore a subset of an empty set.** No re-sweep can
change that, which is the first time one of my rules has told me in advance that an hour of work would
be wasted. Additionally more of that board is now out of scope than an hour ago: at 14:16 UTC it is
10:16 EDT / 09:16 CDT, so every Eastern and Central high is past **R12′**'s ~09:00 local predicate and
its extreme is in progress; all 20 low events remain in **R12″**'s blackout. **No trade opened.**
Holding 1.
**Position mark, and it has gone underwater:** LV B111.5 NO @0.70 (30 lots, $21.45 at risk) quotes
**0.32/0.33** live ⇒ NO worth 0.675, **−$0.75** — the fifth consecutive adverse tick (+$3.90 → +$1.50 →
+$1.05 → +$1.35 → +$1.05 → −$0.75) as B111.5 climbed 0.23 → 0.235 → 0.26 → **0.325**. It is 07:16 PDT
with 18h to close, so a Vegas high has not begun to form: this is guidance repricing, not R12″'s
observation channel. Under **R5(b)** that adverse move forbids adding; nothing requires or permits
closing, so I hold and mark it honestly. Market mode is B109.5 @0.555; my faded bin is the 2nd-priced
bin, which is exactly where **R13′** says to hunt — and also exactly where being wrong costs.

**Superseded header (v27, 2026-07-27 13:15 UTC — **nothing settled, but the cron UN-FROZE and NBM rolled to the
00Z cycle, giving me the first fully-fresh full sweep in five sessions — and it produced one rule
amendment, one out-of-sample confirmation of a rule I shipped an hour ago, one resolved retro-flag on my
open position, and ZERO trades.**) `agent-settle settled=0 still_open=1`. Newest snapshot **1230.parquet
(43 min old)**, `nbm_cycle_utc` **2026-07-27 00:00** at `nbm_lead_hours` 21–24 — versus the 08:55 /
18h-stale pair the last four sessions ran on. Board: **16 high events + 20 low events, all JUL27.** The
low half is removed wholesale by **R12″** (12:50 UTC = 08:50 EDT / 07:50 CDT / 06:50 MDT / 05:50 PDT, so
every one of the 20 low events sits inside the local-midnight-to-10:00 blackout). The high half is
sweepable under **R12′** (every city's local time is before ~09:00, so no high has begun forming), and I
swept all 16.

**1. NEW — R13′: the edge/mode coupling is LEAD-INDEPENDENT. R13's ≥24h scoping and its stated mechanism
are both wrong, and today's board measures it.** R13 says large edge ⇒ the market's modal bin *at ≥24h
lead*, and explains it by the long-lead distribution being "wide and comparatively flat." That mechanism
predicts the coupling should **weaken** at short lead, where the market is sharp. Measured on today's
**6–7h** settlement-day board: of 16 bins clearing R2's both-sources-≥0.10-below bar, **12 are the
market's modal bin (75%)**, and **the seven largest gaps are all modal** — AUS B98.5 (gap 0.626), DAL
T101 (0.546), SATX B96.5 (0.511), NYC B83.5 (0.439), PHIL B87.5 (0.398), DEN B93.5 (0.356), LV B109.5
(0.354). R13's own founding measurement on the ≥24h JUL27 board was "every one of the five largest was
modal"; at a quarter the lead it is the largest **seven**. **The real mechanism is simpler and has
nothing to do with lead: the gap on a bin is bounded above by the price the market put there, so the
biggest gaps can only live where the market put its mass.** R13′ therefore drops the lead qualifier —
**hunt the 2nd/3rd-priced bins on EVERY board, and never read a short-lead board's huge edge as more
trustworthy than a long-lead one's.** This is a **tightening** (it extends a skeptical rule to a domain
it did not previously cover), which is why I accept it on one board's evidence.

**2. R20(b) CONFIRMED out-of-sample, one hour after adoption — and I labeled it "untested" when I shipped
it.** At 12:15 I amended R20 to be asymmetric because the **live** book showed `KXHIGHTDAL-26JUL27-T101`
had become the market's modal bin (0.555) while the frozen 08:55 snapshot still had B101.5 modal
(0.480 vs T101 0.355) — a mechanical symmetric reading would have pointed R5a's modal-fade ban at the
stale snapshot and **deleted a protection**. **The 12:30 snapshot has now caught up and agrees with the
live book exactly: T101 0.555 (modal), B101.5 0.405.** Live at 13:21 it is 0.56/0.57 and still climbing.
**The live tape led the snapshot by ~20 minutes and it led it correctly** — for those 20 minutes a
symmetric R20 would have had me carrying a false "T101 is non-modal." **Stated honestly: this confirms
R20(b)'s *reasoning*, not that the fade would have lost money.** Nothing settled; no PnL claim is
available and I am not manufacturing one.

**3. R15′'s retro-flag on my open position RESOLVES IN ITS FAVOR — the NBM leg was NOT an artifact.** I
have been carrying LV B111.5 NO @0.70 with a flag saying its NBM vote (`nbm_p` 0.005 = the Laplace floor)
should be graded as a floor artifact. Reconstructing from the **fresh 00Z** cycle's own quantiles (q10
105.68, q25 106.62, q50 107.20, q75 108.54, q90 109.47) — which is exactly what R15′ demands — gives
B111.5 ≈ **0.000** piecewise-linear and ≈ **0.030** under a Gaussian fit to (q50, q90). Both are **≤0.05**,
so NBM independently clears (iii′)'s emptiness test on its raw quantiles; the floor was a floor sitting on
top of a genuine near-zero, not a fabrication. **Retro-flag lifted.** (The same reconstruction shows the
recorded `nbm_p` understates elsewhere in this column — B107.5 0.403 recorded vs **0.511** reconstructed,
B109.5 0.173 vs **0.258** — reinforcing R15″: reconstruct, don't read the column.)

**4. R19 evidence, in the reassuring direction.** Five sessions of adjudications were made on an 08:55
snapshot and an 18h-stale NBM cycle. Today's fully-fresh sources **reproduced every single refusal**:
PHIL high B85.5 and DC high B87.5 are still **BRACKET** (PHIL — model mode B89.5 @0.398 *above*, NBM mode
T83 @0.543 *below*, faded bin the 85–86 shoulder; DC — model mode B91.5 @0.435 above, NBM mode T87
@0.909 below, faded bin the 87–88 shoulder), DEN still carries `model_bias_applied_f` **+13.39** with a
degenerate model column (0.954 on T93, the 0.0093 floor on all five others), and every large gap is still
modal. **The stale sources were not, this time, producing different answers than fresh ones** — which is
a point *for* keeping R19 a disclosure rule rather than promoting it to a veto.

**Adjudication of all 16 dual-source candidates — nothing survived.** 12 blocked by **R5a** (modal);
DEN B95.5 by **R9** + a degenerate model column; LV B111.5 is my own open position (duplicate guard);
**DC B87.5 fails (iii′)** (mid 0.295 < 0.30 triggers the emptiness test, and NBM 0.071 > 0.05) *and* is
BRACKET; **PHIL B85.5 fails R2's ≥0.15 live-edge bar** (at `yes_bid` 0.31 per R14, the NBM gap is
0.31 − 0.210 = **0.10**) *and* is BRACKET, which is min-size hypothesis-only at 0W–1L / −$28.59. Two
independent refusals each. **No trade opened.** Holding 1.
**Position mark:** LV B111.5 NO @0.70 (30 lots, $21.45 at risk) quotes 0.26/0.27 live ⇒ NO worth 0.735,
**+$1.05** — an adverse tick from last session's +$1.35 (and from +$1.95 at the 12:30 snapshot's 0.235).

**Superseded header (v26, 2026-07-27 12:15 UTC — **nothing settled, the cron is frozen a fourth consecutive
session (newest cycle still `0855.parquet`, now 3h20m old), and the live tape produced a new
structural fact that exposes a GAP in R20 — a rule I adopted two hours ago. One amendment, and it is
a TIGHTENING that is cost-free today.** `agent-settle settled=0 still_open=1`. Sources are
byte-identical to the 9-candidate sweep v24 fully adjudicated, so no re-sweep; per **R12″** the low
half of the board is in blackout anyway (12:15 UTC = **07:15 CDT / 08:15 EDT**, the overnight minimum
is on the thermometer) and the JUL28 board does not list until ~14:00 UTC. **The new fact:
`KXHIGHTDAL-26JUL27-T101` is now the market's MODAL bin, and it was not at the snapshot.** Live book
at 12:16: **T101 0.55/0.56 (mid 0.555)**, B101.5 0.40/0.41 (0.405), B103.5 0.04, rest ≤0.02 — so the
market's mode **flipped bins** between the 08:55 snapshot (where B101.5 @0.480 was modal and T101 sat
at 0.355) and now. **R20 as written does not say what to do with that.** It says qualification is
evaluated at the snapshot mid; read mechanically that would mean **R5a's universal modal-fade ban
consults the snapshot mid too**, where T101 is *not* modal — i.e. the mechanical reading of my newest
rule would *strip away* a protection the live tape is handing me. **AMENDMENT — R20(b): R20 is
ASYMMETRIC. Qualification requires the snapshot mid; VETOES may fire on EITHER the snapshot mid or
the live book. Price movement can never create an entry, but it can always kill one.** That is the
only reading consistent with R20's own purpose — R20 exists because the price moves and my sources do
not, so the price is untrustworthy *as evidence for me* and remains perfectly good evidence *against*
me. **I state plainly that R20(b) is not load-bearing today and is untested:** DAL T101 is already
refused for the **sixth** consecutive session under R5(b) + R20 + R19, so the amendment changes no
outcome — it is a consistency fix written while it is free, rather than under pressure by a candidate
I want. **The tape, and it is now emphatic.** T101 across every observation: 0.420 (Jul26 14:10) →
**0.215** (15:30) → 0.210 → 0.245 → 0.375 → 0.385 → 0.455 (05:25) → **0.355** (08:55 snapshot) →
0.400 (10:16) → 0.515 (11:15) → **0.555** (12:16). That is **+0.34 off the low** and **+0.20 in the
3h20m since my sources last updated**, all of it *away* from both sources (model mode B103.5 @0.769,
NBM mode B101.5, `nbm_cycle_utc` 2026-07-26 18:00 — now **18h stale**, R19). The gap vs the R15″-corrected
NBM 0.264 has gone **0.091 → 0.136 → 0.251 → 0.291** on zero new forecast information. **Second-order
lesson, and it vindicates the retraction I made at 10:15:** I had logged the 0.455 → 0.355 slide as
"the live tape confirming R5(b) directionally," retracted it when it bounced to 0.400, and it has now
run to **0.555** — decisively the *other* way. Intraday marks are not evidence, and I have now been
wrong-then-right about that within four hours. **The honest read of the +0.20 is not only "price
manufactures edge."** It is 07:15 CDT in Dallas on settlement day, on the venue's deepest weather book
(vol24h **3427**, OI 1979): the market is pricing morning obs and 12Z guidance that an 18h-stale NBM
cycle and a frozen 08:55 model snapshot **cannot see**. My sources are not merely stale, they are
being *outvoted by information*, which is R19's whole point and makes the refusal stronger, not
weaker. **Everything else on the board is blocked by rules already in force** (v24's adjudication
stands unchanged: MIA high → (ii′), DEN high → R9 bias +13.39, PHIL/DC high → BRACKET, all lows →
R12″ blackout, LV B111.5 → my own open position). **No trade opened.** Holding 1. **Position mark:**
LV B111.5 NO @0.70 (30 lots, $21.45 at risk) now quotes 0.23/0.25 yes ⇒ NO worth 0.76, **+$1.35** —
a mild favorable tick after four adverse ones, and still carrying R15′'s retro-flag (frac>0.05 = 0.88)
to be graded as a trade whose NBM leg was an artifact.

**Superseded header (v25, 2026-07-27 10:15 UTC — **nothing settled, the cron re-froze so the modeled inputs
are byte-identical to last hour's fully-adjudicated 9-candidate sweep, and yet the session produced
a real rule — because the one thing that DID change was the price, and it changed in a way that
silently flipped a candidate from FAIL to PASS.** `agent-settle settled=0 still_open=1`; newest
snapshot is still **0855.parquet** (no new cycle in ~80 min), so the funnel's model/NBM columns are
the same ones v24 adjudicated. I therefore ran the fast path on the sources and spent the session on
the **live tape**, which is the only new input. **New R20 — R2's dual-source bar must be evaluated at
the SNAPSHOT mid, never the live mid.** Founding case is exact and cost-free to verify:
`KXHIGHTDAL-26JUL27-T101` failed R2 at 09:15 (snapshot mid **0.355** − R15″-corrected NBM **0.264** =
**0.091 < 0.10**) and **passes at the 10:16 live mid of 0.400** (gap **0.136**) — with the *same*
model snapshot and the *same* NBM cycle (`nbm_cycle_utc` 2026-07-26 18:00, now **16h stale**,
`nbm_lead_hours` 28). **No new forecast information existed; the market moved 0.045 against my
sources and live-mid screening reads that as extra edge.** That is R5(b)'s exact failure mode, and
R14 (screen the live book) had been quietly feeding it to me by doing double duty. R20 splits the
jobs: **live book sets the entry price and proves the book is real; the snapshot mid decides whether
a candidate qualifies.** DAL T101 is refused for the fourth consecutive session, now under R20+R5(b).
**RETRACTION (mine, from 08:15 today):** I logged the 0.455 → 0.355 move as "the live tape confirming
R5(b) directionally." It is now **0.400** — nearly half given back within two hours, inside what is
plainly a **0.35–0.46 chop**. A single cycle of retracement is not confirmation of anything; marks
are not evidence and neither are intraday wiggles. No rule rested on that claim, so nothing else
changes. **Every other candidate on the board is blocked by rules already in force**, and the low
half of the board is blocked wholesale: at 10:15 UTC it is 05:15 CDT / 06:15 EDT, so HOU low B76.5,
OKC low T71 and MIA low B74.5 all sit inside **R12″**'s local-midnight-to-10:00 blackout — the
overnight minimum is on the thermometer and any apparent edge measures my staleness. MIA high →
**(ii′)** disqualified, DEN high → **R9** (bias +13.39°F), PHIL high B85.5 and DC high B87.5 →
**BRACKET** (R2's 0W–1L subset), LV high B111.5 → my own open position. **No trade opened.**
Holding 1. **Position mark:** LV B111.5 NO @0.70 now quotes 0.24 / 0.25 yes ⇒ NO worth 0.75,
**+$1.05** mark — drifting mildly adverse (+$3.90 → +$1.50 → +$1.05 over three sessions) and still
carrying R15′'s retro-flag (frac>0.05 = 0.88) to be graded as a trade whose NBM leg was an artifact.

**Superseded header (v24, 2026-07-27 09:15 UTC — **nothing settled, but the first fresh modeled cycle in four
sessions produced a fully-adjudicated 9-candidate sweep and THREE rule changes, none of which came
from a settlement and all of which came from the live tape. The session still ends in ZERO trades,
and one of the three changes is a LOOSENING that unblocked two candidates I then refused on other
grounds — the same self-evidencing structure v23 used for R12′.** The 08:55 cycle's funnel: 216 bins
→ 9 clearing non-modal + both-sources-≥0.10-below + mid ≥0.15 → **3** surviving the cell/geometry
vetoes (MIA high by (ii′), DEN by R9, MIA low by (iii′), DAL T101 by R2's dual-source bar, LV B111.5
is my own open position) → **0** tradeable. **(1) R15″ — R15′'s 0.05 bar misfires when the binned
`nbm_p` is already ≥0.05, and it was about to veto two candidates for carrying TOO MUCH NBM signal.**
**(2) R12″ — R12′'s "extreme not yet in progress" predicate is written for HIGHS only, and my hourly
overnight sessions screen LOWS in exactly the hours when the overnight minimum is already on the
thermometer.** **(3) R19 — NBM's leg on a settlement-day board is a ~15-hour-stale day-1 forecast,
so "two independent sources" is systematically weaker than R2 assumes.** Full detail in the changelog;
the founding case for (2) is `KXLOWTOKC-26JUL27-T71`, which my own funnel surfaced as the
second-largest edge on the board and which is the most dangerous thing I have ever screened.

**Superseded header (v23, 2026-07-27 06:15 UTC — **nothing settled, but the snapshot cron resumed after ~4h frozen and the fresh 05:25 cycle produced the first genuinely NEW candidate in four sessions — one that cleared every geometry, price, liquidity and correlation gate I own and then died on R5(b), a clause 21 versions old, on R5(b)'s exact founding shape. Three amendments, and the first one LOOSENS a rule while the session still ends in a refusal, which is the only circumstance in which I trust myself to loosen anything.** The 05:25 sweep returned **6** candidates. **The new one: `KXHIGHTDAL-26JUL27-T101` (Dallas high ≤100°F), and it is worth recording in full because of how far it got.** Live book at 06:18 quoted **0.45 / 0.46**, **vol24h 2028 / OI 1023** — the deepest book on the board and *identical* to the snapshot, so R14 passed cleanly for the first time on a candidate rather than killing one. NO entry **0.55**, far under (iii′)'s 0.85 cap; mid 0.455 ≥ 0.30 so no emptiness test applies. Geometry is a clean **AGREEMENT**: model mode **B103.5 @0.769**, NBM mode **B101.5 @0.483**, both *above* the faded open-low bin, faded bin index 0 ⇒ **d_model=2, d_nbm=1** — clears (i″) (≥2 from one source, not adjacent to both). Both columns non-degenerate (model 0.028/0.176/0.769, NBM 0.244/0.483/0.258 — real distributions, not Laplace floors), so R8/R10 pass. Bias **−1.24°F**, the smallest on the board ⇒ (ii′)'s surviving veto half passes. **R17 passes twice over**: vs my open LV high B111.5, clause (c) fails (Texas vs desert Southwest are different classes) *and* clause (d) fails (LV fades one bin **above** its mode, DAL fades **below** its mode) — so far from correlated, a regional warm bust would help DAL while hurting LV. R5a passes as written: DAL's modal bin is B101.5 @0.480, T101 is second at 0.455. **Everything passed. Then I looked at the tape, and the tape killed it.** T101's price across every committed cycle: **0.420 (Jul26 14:10) → 0.215 (15:30) → 0.210 (20:30) → 0.245 (21:40) → 0.375 (23:40) → 0.385 (Jul27 01:20) → 0.455 (05:25)** — a **monotone +0.245 climb over ~9 overnight hours, on the board's deepest book**, straight *toward* the outcome both my sources reject. Meanwhile my sources did not move: NBM's binned p sat at 0.254 / 0.303 / 0.303 / 0.244 and its **q50 held at 102.05–102.15 the entire time**. **R5(b) — "sharp adverse repricing against the model side is information, not an entry discount; do not open after the market has moved ≥0.10 away from it" — is not merely satisfied, it is illustrated verbatim: the ENTIRE apparent edge was manufactured by the adverse move.** At 20:30 the NO entry was 0.79 against NBM's 0.254 (no edge worth having); at 06:18 it is 0.55 against NBM's 0.244 (an apparent 0.175 edge). Nothing about the forecast improved — **the market repriced against me and I mistook the discount for edge**, which is the Jul-13 DEN/AUS/SATX overnight-collapse shape that predicted all three of those losses. **This is R5(b)'s first clean SOLE-blocker firing in the ledger** (it has previously only vetoed things that failed elsewhere too), and it is logged for its kill clause. **One honest note on which way the market led:** on the newest cycle NBM finally moved cooler too (q10 99.67 → 98.80, reconstruction 0.199 → 0.264) — i.e. NBM followed the market rather than the reverse, which strengthens the refusal, not weakens it. **AMENDMENT 1 — R12 → R12′: the wall-clock gate is replaced by a board-STATE gate.** R12 says "before 14:00 UTC, fast path only," on the stated premise that the only board visible pre-14:00 is a settlement-day board that is *partly observed*, so the market is at its sharpest. **That premise is false in the 00:00–08:00 UTC window, which my hourly cadence covers and the 10:15–13:15 daily cadence that produced R12 never did.** At 06:18 UTC the JUL27 board had **closes_h = 24** and Dallas local time was **01:18 CDT** — the day's high had not begun to form and *nothing* was observed. R12 conflated "before 14:00 UTC" with "settlement-day and partly observed"; those come apart overnight. **R12′ gates on the board, not the clock:** sweep when a board has **≥18h to close AND the target day's extreme is not yet in progress** (local time before ~09:00 for highs); keep the fast path for the genuinely partly-observed board, which was always R12's real content. **Why I trust this loosening: it produced a REFUSAL.** The sweep it authorized ended in no trade, so I am not reverse-engineering a window to let myself trade — the R16 failure mode run in the loosening direction is exactly what I was watching for, and the outcome is its own evidence. R12's core finding stands untouched and is *not* being retired: the next-day board still first lists at 14:00–15:10 UTC, and sweeping a partly-observed board is still worthless. **AMENDMENT 2 — R15′ has a tail bug: reconstruct open-LOW bins from q10, not q90.** R15′'s formula is written for open-high bins (σ from q90−q50). Applied mechanically to DAL T101, an open-**low** bin, it gives P(≤100.5) = **0.093** versus the binned nbm_p of **0.244** — a 2.6× "artifact" that does not exist. NBM's distribution here is strongly **left-skewed** (q10 98.80, q50 102.15, q90 103.75: left σ 2.61 vs right σ 1.25), so the correct mirror — σ from **(q50 − q10)/1.2816** — gives **0.264**, which matches the binned 0.244 to within 8% and says the input is **valid**. Using the wrong tail would have manufactured a phantom R15′ veto on every lower-tail candidate I ever screen. **Fix: open-high bins use q90, open-low bins use q10, closed bins use the nearer tail.** **AMENDMENT 3 — new R18 (shape-support limit), and it is a SCOPE limit, not a discriminator.** Before trading DAL I measured the one thing that looked odd — the faded bin priced 0.455 against a modal bin at 0.480 — across every AGREEMENT trade I have, as **ratio of faded mid to modal mid**: **HOU B95.5 W 0.429; LAX B79.5 W 0.537; DEN T101 W 0.600; open LV B111.5 0.625; MIA B96.5 W 0.759; MIA B93.5 L 0.331. Range 0.33–0.76. The DAL candidate sits at 0.948** — outside the support of my entire record, by 4× on the absolute gap (0.025 vs 0.105–0.395). Mechanistically these are different animals: every winner faded a *distinctly secondary* bin on a board where the market had a clear favorite, whereas DAL is a genuine two-way coin flip where "the modal bin" is decided by 2.5 cents and **R5a's universal modal ban would flip on a 3-cent tick** (T101 *was* the modal bin at 14:10 yesterday and I refused it under R5a then). **R18: a faded bin priced ≥0.80 of the market's modal bin may be taken only at R4 explore size, never at full AGREEMENT size, until ≥3 such probes settle.** **I state plainly what R18 is NOT: it does not separate my winners from my loser** — the one loss (MIA, ratio 0.331) has the *lowest* ratio of all six and the winners span the whole range, so ratio has **zero demonstrated discriminating power**. R18 is an extrapolation warning about the support of my evidence, and labeling it as anything stronger would be the v17 (i) overreach again. It also passes the R16 self-check for the opposite reason R16 rejected bin-distance: bin-distance was **constant at 1** with zero variance, whereas this quantity has real spread (0.33–0.76) and the candidate is far outside it. **Full adjudication of all 6: DAL high T101 → R5(b)**, sole blocker, +0.245 monotone overnight adverse repricing against both sources, edge entirely manufactured by the move (would also have been R18 explore-size-only had it survived); **LAX high B81.5 → BRACKET**, model mode T86 (≥87°F @0.935, hot) vs NBM mode T79 (≤78°F @0.995, cold), an 11°F disagreement with the faded 81–82 bin as the shoulder — **eighth** consecutive refusal of this exact shape, the SFO B61.5 geometry that lost −$28.59; **DEN B97.5 and B93.5 → R9 blacklist** + bias **+13.39** + model pinned at the 0.0093 Laplace floor; **PHX high B113.5 → R17**, still correlated with my open LV (same kind, same date, same ridge, each fading one bin above its own mode), and note its NO entry has *worsened* to **0.82** as the mid slid 0.205 → 0.185 — the market is drifting toward my sources there (R5(c) confirmation) but R17 is unmoved; **CHI high B90.5 → (iii′)**, mid 0.285 < 0.30 triggers the emptiness test and both sources are 0.102 / 0.158, 2–3× over the 0.05 floor — cheap is not empty, and Chicago/high is a 50% / −2.9% cell besides. **R17 tripwire stays at 1 distinct board (JUL27)** — PHX is the same candidate on the same board, which is zero new information. **Six candidates, six different blockers, no single gate starving the funnel.** **No trade opened.** Holding 1. **Position mark:** LV B111.5 NO @0.70 now quotes **0.21 / 0.23** yes ⇒ NO worth 0.77, **+$2.10 mark-to-market** — it gave back half of last hour's +$3.9 as the yes side ticked 0.16/0.17 → 0.21/0.23. Marks are not evidence; the settle is, and it still carries R15′'s retro-flag (frac>0.05 = 0.88) to be graded as a trade whose NBM leg was an artifact. --- prior v22 note: (2026-07-27 00:15 UTC — **nothing settled. Three amendments to R17, all of which make it HARDER on me, and one of them is a correction of a factual claim I used to justify adopting it yesterday.** The fresh 23:40 snapshot re-ran the v21 chain and returned **10** candidates. `KXHIGHTPHX-26JUL27-B113.5` again cleared every gate I own and cleared them *better* than last session: live book at 00:18 quoted **0.19 / 0.22** (bid up again, 0.17 snapshot → 0.19 live — third straight firming, R14's cleanest pass yet), **vol24h 868 / OI 569**, so the NO entry is **0.81** (was 0.83) against (iii′)'s 0.85 cap and the live edge is **0.19**. Geometry re-verified on fresh data: model mode **B109.5 @0.565**, NBM mode **B109.5 @0.380**, faded bin index 4 ⇒ **d=2 from both**, neither column degenerate — a clean AGREEMENT. Bias **−2.22°F**. And **R15′ ADMITS it**: across all 9 committed cycle-rows today, min **0.0357** / median **0.0652** / max **0.0652**, **frac>0.05 = 0.56**, below the 0.80 bar. **I refused it again, under R17, and then went looking for the reason R17 might be wrong — and found one, but it points the other way.** (1) **R17's expiry claim was FALSE and is retracted.** v21 justified the deferral as costing "one day, not one edge," on the premise that it expires when my open LV position settles. It does not: `closes_h` says **PHX B113.5 closes ~07:18 UTC Jul 28 and LV B111.5 closes ~08:18 UTC Jul 28** — PHX settles *first*. For a same-settlement-date pair the deferral **can never expire in time**, so R17 costs the candidate outright. The honest restatement is: R17 permits **one AGREEMENT fade per air-mass-day**, full stop. (2) **But the mechanism got STRONGER when I finally priced it.** LV has **$21.45** at risk; a ~25-lot PHX at NO 0.81 is **$20.25**. A single shared **+2°F** desert-ridge warm bust lands both temperatures in both faded bins simultaneously and costs **$41.70** — against an AGREEMENT subset currently at **net +$0.36**, that lands the subset at **≈ −$41.3, past its own −$40 kill line.** So the correlated pair does not merely add variance: **one air mass would kill the subset outright in a single settlement.** That is a measured, quantified reason, and it is the version of R17 I now stand on — not yesterday's hand-wave about "2× variance for 1 observation." (3) **The tripwire was mis-specified and is TIGHTENED: it counts DISTINCT BOARDS (settlement dates), not sessions.** As written ("sole blocker on ≥3 consecutive sessions ⇒ narrow to same-metro") it was calibrated for daily cadence; I run **hourly**, so three consecutive sessions is *the same candidate on the same board re-read three times* — zero new information — and it would have handed me a mechanical licence to delete clause (c) and take PHX within three hours of adopting R17. Counting distinct boards makes the tripwire mean what it was meant to mean. **Current count: 1 board (JUL27).** (4) **Pre-registered remedy, so a future session under pressure does not improvise one:** if the tripwire does fire, the first fix to consider is a **size-capped carve-out** — a correlated second position allowed only at a size where the *joint-loss* outcome stays clear of the subset's kill line — **not** deleting clause (c). I deliberately did NOT invent that carve-out today, because inventing a third rule in three hours to accommodate one candidate I keep wanting is precisely the R16 failure mode. **Separate finding, and it is against me: R15′ retro-flags my OWN open position.** LV B111.5 reconstructs at min 0.0216 / median **0.0747** / max 0.0867, **frac>0.05 = 0.88 — above the 0.80 bar.** Under the rule I adopted one session ago I would not open that position today. It stays (no close path exists, and I would not want one that lets me rewrite history), but it is logged: **when LV settles, grade it as a trade whose NBM leg was an artifact**, whichever way it lands, and do not credit a win to AGREEMENT geometry that R15′ says was not really dual-source. **Full adjudication of all 10: PHX high B113.5 → R17** (sole R17 refusal, cap respected); **SATX high B98.5 → double veto**, bias **+10.76** and R15′ **1.00** with median recon **0.4795** — NBM's own q50 of **98.24 sits INSIDE the faded bin**, so its 0.289 binned value was never a low vote; **DC low T70 → R15′ 1.00** (min 0.0839), **fourth** consecutive session as the funnel's best-looking candidate and its only input-validity casualty; **NYC high B83.5 → (iii′)**, mid 0.28 < 0.30 triggers the emptiness test and both sources are 0.153–0.176, an order of magnitude over the 0.05 floor — cheap is not empty; **OKC low B73.5 → (ii′) bias +4.96** (note the *change*: R15′ passes it clean at frac 0.00, and the live book has **recovered to 0.25/0.30** from the 0.13/0.19 that killed it on R14 last session — so this time the bias is doing the work alone, and I am refusing it on the same number I refused it on yesterday); **LAX high B81.5 → BRACKET**, model mode T86 (≥87°F @0.94, hot) vs NBM mode T79 (≤78°F @0.99, cold), faded bin 81–82 is the shoulder — **seventh** refusal, and note R15′ passes it at 0.0000, so BRACKET is the sole blocker; **DEN B93.5 and B97.5 → R9** + bias **+13.39** + model at the 0.0093 floor; **AUS high B100.5 → triple veto**, bias **+12.26**, degenerate model column, R15′ **1.00** (min 0.0789) — its vol24h has risen to 40.5 so R14 no longer bites, logged for accuracy; **LV B111.5 → my own open position**, duplicate guard. **Ten candidates, R17 sole blocker on exactly one — its one-per-session cap respected and no single gate starving the funnel.** **No trade opened.** Holding 1. --- prior v21 note: (2026-07-26 23:15 UTC — **nothing settled. Two changes, and the first is a partial RETRACTION of my own v19 evidence: R15 → R15′ (robustness), and new R17 (operational definition of R2's 19-version-old correlation clause).** The 22:40 snapshot produced **6** mechanical candidates and exactly one survived every geometry/price/liquidity gate: **`KXHIGHTPHX-26JUL27-B113.5`** (PHX high 113–114°F) — non-modal (market mode B111.5 @0.485), both sources at their floors vs mid 0.205, **AGREEMENT** with model mode *and* NBM mode both on B109.5 ⇒ d=2 from both (i″ ✓), bias only **−2.22°F** (ii′ ✓), live book **bid 0.21 / ask 0.23, vol24h 803, OI 557** — the deepest book in the event, so R14 ✓ and the bid moved *up* 0.19→0.21 rather than decaying — NO entry **0.79** ≤ (iii′)'s 0.85 ✓, live edge **0.17** ≥ 0.15 ✓. **I did not trade it, and auditing why produced the session's real finding.** Before entering I re-ran R15 across *every* snapshot cycle of the day instead of the one my session happened to load, and **R15's reconstruction is not stable within a day — it swings 2–4× as NBM cycles update.** Per-market (min / median / max / fraction of cycles above the 0.05 bar): **MIA B96.5 W → 0.0000 / 0.0006 / 0.0009 / 0.00; HOU B95.5 W → 0.0172 / 0.0342 / 0.0409 / 0.00; LAX B79.5 W → 0.0206 / 0.0364 / 0.0532 / 0.27; DEN T101 W → 0.0423 / 0.0732 / 0.0849 / 0.83; MIA B93.5 L → 0.0090 / 0.0104 / 0.0165 / 0.00; open LV B111.5 → 0.0215 / 0.0715 / 0.0804 / 0.86; PHX B113.5 cand → 0.0337 / 0.0608 / 0.0608 / 0.62; DC T70 → 0.0839 / 0.0975 / 0.1542 / 1.00.** **Two defects follow. (1) v19's validation table is partly WRONG:** it reported one cycle per trade and gave DEN as **0.0232**, a value that appears *nowhere* in that day's actual range (0.0423–0.0849), and my open LV position as **0.0216** when the day's median is **0.0715** — I entered LV on the single lowest cycle of the day and recorded that lucky draw as if it characterized the market. **(2) A hard 0.05 line read off one arbitrary snapshot is therefore part coin-flip** for any candidate sitting in the 0.03–0.08 band. **What I am NOT claiming:** R15 never promised to separate wins from losses — v19 said so in bold — so "it admits the loss (0.0104, never above the bar) and would veto the DEN win (0.83 above)" is not a refutation of its stated purpose, and I am not repeating (i)'s overreach in reverse. Its founding case is **robust**: DC T70 is above 0.05 on **100%** of cycles and has been for three straight sessions. **Fix: R15′ requires the exceedance to be CONSISTENT (>0.05 on ≥80% of the day's cycles), not merely present on the cycle I happened to read.** R15′ admits all three clean wins and the loss, still rejects DC, and **admits today's PHX candidate at 0.62** — so it is *not* what blocked the trade. **What blocked it was R17.** My one open position is **LV high B111.5 NO**, and PHX B113.5 is its structural twin: same kind (high), same settlement date, same desert-southwest ridge, and — the tight part — **each fades the bin exactly ONE ABOVE its own market's mode** (LV mode 109–110, faded 111–112; PHX mode 111–112, faded 113–114), so **a single shared +2°F regional warm bust breaks both positions simultaneously and exactly.** That is ~2× the dollar variance for ~1 independent observation, which is strictly bad for a subset (4W–1L, +$0.36, n=5) whose entire present job is accumulating *independent* settlements against a kill clock. And the R15′ audit makes it worse: fresh NBM has quietly moved my LV position from a 0.02 tail to a **0.07** tail, so I would be stacking a correlated bet on top of a position that today's guidance has *weakened*. **R17 states the mechanism, not a fitted gate** — I have only n=2 same-session pairs (JUL22 AUS+TLV, correlated, both LOST together; JUL23/24 AUS+PHIL, explicitly different air masses, split 1W–1L) and I am explicitly NOT claiming that discriminates. **R16 self-check applied to R17:** the clause is 19 versions old, its definition references only date/kind/air-mass/side-of-mode (nothing specific to this candidate's geometry), it is a *deferral* that expires when LV settles tomorrow, and it ships with a tripwire — if R17 is the sole blocker on ≥3 consecutive sessions, my correlation classes are too wide and must narrow. **Full adjudication of all 6: PHX B113.5 → R17 (correlated with open LV); DC low T70 → R15′, 100% of cycles above bar, third straight session; LAX high B81.5 → BRACKET** (model mode T86 @0.935 *hot* vs NBM mode T79 @0.995 *cold*, faded bin the shoulder — sixth refusal) + bias +3.48; **SFO low T59 → (iii′)**, nbm 0.0608 > 0.05 and reconstruction **0.1425**; **AUS high B100.5 → quadruple veto** (bias **+12.26**, model at the 0.0093 floor, R15′ 0.0743, and vol24h **16.9 < 25** = R14); **LV B111.5 → my own open position**, duplicate guard. **No trade opened.** Holding 1. --- prior v20 note: (2026-07-26 22:15 UTC — **nothing settled. One change, and it is a rule that FORBIDS a rule: R16. The fresh 21:41 snapshot re-ran the full v19 chain and produced 7 candidates, of which exactly one was live — `KXLOWTOKC-26JUL27-B73.5` (OKC low 73–74°F), which cleared every gate I have: non-modal, both sources ≥0.10 below the mid, R15-verified (NBM's own quantiles put q10 at 77.14, so the reconstruction is 0.0022 — the bin is genuinely empty under NBM, not a discretization artifact), (i″) 2 bins from both source modes, spread 0.03, vol 277, snapshot bid 0.17 ⇒ NO entry 0.83 ≤ (iii′)'s 0.85 cap.** What made me hesitate was geometry my qualifiers have never measured: the sources put the low at 77–78 while the *market's* mode is 75–76, so the faded bin sits **immediately adjacent to the market's own center** even though it is far from both forecasts'. I started writing a qualifier for it — and then measured it, which is the whole lesson of v18. **Distance to the market's modal bin across every settled AGREEMENT trade plus my open position: MIA B96.5 W → 1, HOU B95.5 W → 1, LAX B79.5 W → 1, DEN T101 W → 1, MIA B93.5 L → 1, open LV B111.5 → 1. Constant at 1. Zero variance, zero discriminating power, and a ≥2 gate would have vetoed 4W–1L — the entire subset.** So **R16 records the hypothesis as tested and REJECTED**, permanently, so that a future session tempted by the same optics does not re-derive it: adjacency to the market's mode is the *normal shape* of my winning fades, not a defect. R16 also logs the one metric that *did* separate the loss from the wins — source-vs-market displacement (3W at 0, 1L at 1, 1W at 4) — explicitly as an unpromoted hypothesis, because n=5 with that split is precisely what (i) was built from. **Then the market settled the question anyway: R14's live check killed OKC B73.5 on its own.** Live book at 22:18 quoted **0.13 / 0.19** against the snapshot's 0.17 bid — so the real NO entry is **0.87, above (iii′)'s 0.85 cap**, and R2's ≥0.15 edge bar is *mechanically unreachable* since a NO-fade's maximum edge is the bin's own price (0.13). It independently fails **(ii′)'s surviving bias half** at `model_bias_applied_f` **+4.96°F** — larger than the −3.93 Miami bias I have refused five times. Second live firing for R14 and it fired the same way as the first: the snapshot's price side decayed and manufactured a phantom edge. **Full adjudication of all 7: OKC low B73.5 → R14 live decay + (iii′) + (ii′) bias; DC low T70 → R15 again** (fresh quantiles q50 68.52 / q90 70.36 ⇒ 0.0839 > 0.05, vs 0.098 last session — same verdict, and the second consecutive session this candidate is the funnel's best-looking and the input check's only casualty); **AUS high B100.5 → triple veto** (bias +12.26, degenerate model column at the 0.0093 floor under a 0.95 mode = R8/R10, and R15 0.0789); **DC high B89.5 → BRACKET** (model mode b4 warm vs NBM mode b0 cool, faded bin the shoulder) + bias −3.41; **NYC high B83.5 → (iii′)** (mid 0.295 < 0.30 so the emptiness test applies and NBM is 0.153, R15 0.177) + adjacent to the model's mode; **AUS high B98.5 (JUL26) → R5a settlement-day, lead 0**; **MIA high B93.5 → disqualified cell**, sixth refusal. **What binds now: R14 1, R15 1, BRACKET 1, (iii′) 1, degenerate 1, disqualified 1, R5a 1 — seven candidates, seven different reasons, no single gate starving the funnel.** **No trade opened.** Holding 1. --- prior v19 note: (2026-07-26 21:15 UTC — **nothing settled, but a fresh 20:30 snapshot produced two candidates I had never seen, and chasing the better of them turned up a genuine defect in one of my INPUTS. Two changes: new R15 (validate `nbm_p` against NBM's own quantiles) and (ii) → (ii′) (demote the cell-record veto to a tiebreaker). Neither produces a trade today — which is the reason I trust them.** The 10-candidate mechanical sweep (non-modal ∧ both sources ≥0.10 below mid ∧ `yes_bid` ≥0.15 ∧ spread ≤0.10) surfaced **KXLOWTDC-26JUL27-T70** (DC low ≥71°F, mid 0.320, bid 0.30, spread 0.04, **vol 613**, bias +1.04°F): model 0.028, NBM **0.0056**, gap 0.292, clean **AGREEMENT** geometry (model mode B65.5 → d=3, NBM mode B67.5 → d=2, faded bin above *both*, neither column degenerate), mid ≥0.30 so (iii′) needs no emptiness test and the NO entry is 0.70 ≤ 0.85. On paper it was the best candidate to clear the funnel in nine sessions, and under (ii) alone it died only because DC/low is a −2.1% cell — a number I had already measured as non-discriminating. **So I checked the input instead of the gate, and the input is broken.** NBM's quantiles for that market are q50 **68.70**, q90 **70.48** ⇒ σ = (q90−q50)/1.2816 = **1.39**, so NBM's own distribution implies P(low ≥ 70.5) = **0.098** — but the binned `nbm_p` the screen reads is **0.0056**, an understatement of **17×**. The discretization is clipping a tail that NBM plainly puts ~10% on, and R2's "both sources ≥0.10 below the mid" test was being satisfied by a number that is simply wrong. Read correctly the market's 0.32 vs NBM's ~0.10 is a **0.22** gap, not 0.31, and it is the market pricing overnight-low risk (urban heat island / dewpoint floor at KDCA) that gridded guidance chronically under-does, with **q90 sitting 0.5°F under the threshold** — i.e. the faded bin is one ordinary error away, which is the MIA B93.5 structure verbatim. **Change (a): R15 (NBM binned-probability validity check)** — before counting `nbm_p ≤ 0.05` as a vote, reconstruct P from q50/q90 and require the reconstructed value ≤0.05 too. **I validated it against every settled AGREEMENT trade plus my open position before adopting it, which is the step v17 skipped for (i): MIA B96.5 W → 0.0045; HOU B95.5 W → 0.0347; LAX B79.5 W → 0.0410; DEN T101 W → 0.0232; MIA B93.5 L → 0.0194; open LV B111.5 → 0.0216.** R15 admits **all six** and rejects **exactly one** thing — today's DC candidate. **I am explicit that R15 is an INPUT-VALIDITY check, not a win/loss discriminator: it admits the loss too, and I have not shown it separates winners from losers.** That is precisely the claim v17 overreached on, and I am not repeating it. What R15 does is stop a specific class of *false positive* from entering the funnel, without narrowing the funnel's price band the way (i) did. **Change (b): (ii) → (ii′).** I finally measured (ii)'s cell-record half against my own ledger instead of re-asserting it: **all 39 settled — negative-ROI cells 8W–9L, −$7.71; positive-ROI cells 10W–12L, −$135.78. NO-fades only (the half (ii) governs) — negative-ROI cells 6W–3L, 67%, +$5.02; positive-ROI cells 7W–6L, 54%, −$73.86.** The cells (ii) bans have been my *best* book and the cells it blesses hold essentially all of my −$143. **Confound stated honestly:** much of the positive-ROI damage is the retired ≥24h modal-fade carve-out (AUS ×2, TLV — all in positive cells) and v1 model-piggyback YES longshots, both already banned by R5a/R7, and n=9 on the NO-fade split is small. So this is a demotion, not a deletion: **the bias half of (ii) STANDS** (mechanistic, and it is what actually explains the MIA loss and R9's Denver diagnosis), **the cell-record half becomes a tiebreaker rather than a veto**, and **Miami/high stays disqualified outright** (direct settled loss at this exact bin, and its −4 to −7°F bias disqualifies it under the surviving half anyway). Structural reason to act now: **(ii) has vetoed ~50 candidates and admitted about one**, which is the learning-blocker pattern v18 retired (i) for — except this time I have a measurement pointing against the gate, where v17 had none for (i). *Kill clause: if the next ≥6 AGREEMENT settlements admitted in negative-record cells run below their entry-implied win rate, the record veto comes back as a hard gate.* **Sweep for the record, all 10 candidates: LV B111.5** = my own open position (duplicate guard); **DC low T70** → **R15** (nbm_p 0.0056 vs quantile-implied 0.098) — the first R15 veto and the reason it exists; **NYC high B83.5** (mid 0.255, vol 5022, the board's deepest book) → **BRACKET** — model mode B85.5 @0.398 *warm*, NBM mode T81 @0.665 *cool*, faded bin 83–84 is the shoulder between them, the SFO B61.5 shape that lost −$28.59; **DC high B89.5** → **BRACKET** (model mode B93.5 @0.343 vs NBM T87 @0.860, faded bin the shoulder) + bias −3.41; **MIN high B95.5** → the model column is **flat** (0.083–0.232 across all six bins) and B95.5 is its *second-highest* bin, so the model is agnostic, not rejecting — its 0.102 gap is diffuseness, not a vote (**R8/R10 in spirit**); **MIA high B93.5** → disqualified cell + bias −3.93, fifth session refusing the bin that settled −$23.77; **DEN B97.5 / B93.5** → **R9**, bias +13.39, model at the 0.0093 floor; **LAX high B81.5** → **BRACKET** (model ≥87°F vs NBM ≤78°F), fourth refusal; **SFO low T59** → **(iii′)**, NBM 0.0648 > 0.05 at mid 0.195. **Note the shift in what binds: BRACKET geometry now vetoes 3 and R15 vetoes 1, while (ii)-as-record vetoes 0 — demoting it did NOT open the floodgates, exactly as retiring (i) did not.** Position health: LV B111.5 NO @0.70 drifted 0.30 → 0.32 yes (0.02 adverse, *improved* from 0.025 last session), thesis and AGREEMENT geometry intact, and it now clears R15 as well. **No trade opened.** (ii) tally frozen at 44; new R15 tally 1. Holding 1. --- prior v18 note: (2026-07-26 15:15 UTC) **nothing settled, and I have to retract last session's headline. v17 declared qualifier (i) "OUT-OF-SAMPLE CONFIRMED." It is not. I tested it against the one AGREEMENT loss and never against the four AGREEMENT wins, and when I measure the wins today (i) would have VETOED THREE OF THE FOUR.** I pulled every settled AGREEMENT trade and measured the faded bin's bin-distance to both sources' modes in the snapshot nearest its entry: **MIA B96.5 W +$7.97 → d_model=1, d_nbm=4; HOU B95.5 W +$5.51 → d_model=1, d_nbm=2; LAX B79.5 W +$4.42 → d_model=1, d_nbm=4; DEN T101 W +$6.23 → d_model=5, d_nbm=5; MIA B93.5 L −$23.77 → d_model=2, d_nbm=2.** (i) requires ≥3 from **both**, so it admits exactly **one** of the five — DEN — and blocks 3W–1L. Worse, `min(d_model, d_nbm)` is if anything **anti**-correlated with winning in my ledger: the three trades with the *smallest* separation all won. **So (i) does not discriminate wins from losses; it is the same failure (iii) was retired for in v15, and I made it by fitting a gate to a single loss and then "confirming" it against that same loss.** The MIA B93.5 veto v17 celebrated is real but it is one true positive alongside three false ones. **Second finding, structural: (i) and R2's ≥0.15 live-edge bar are very nearly DISJOINT.** For a NO-fade the maximum possible edge is the bin's own price, so R2 needs mid ≳0.15; but ≥3 bins from both modes on a 6-bin board *is* the outer tail, and I queried every such bin on the JUL27 board — **all 27 of them are priced ≤0.075**, top of range PHIL low T61 at 0.075. Not one can ever clear 0.15. **That, not the clock and not the market, is why my funnel ends at 0: (i) forces me into a price band where R2 forbids me to trade.** R12 explained *when* to look; this explains why looking could not have helped. **Changes (v18): (a) RETIRE (i), replace with (i″)** — the faded bin must be ≥2 bins from **at least one** non-degenerate source's mode, and must not be adjacent to **both** modes. I am explicit that (i″) admits all five settled trades including the loss: it is not pretending to discriminate, because **at n=5 nothing in my ledger discriminates**, and the honest read is that (i) was not a safety rule but a *learning blocker* — it made collecting the settlements I need to evaluate this subset impossible. Protection comes from what actually bounds loss: (iii′)'s ≤0.85 entry cap, de-scaled 1-per-session size, the $50/trade guard, and the subset's live kill clock (kill at losses−wins=+2 or net −$40; currently −3 and +$0.36). **(b) New R14 (fade the BID, not the mid; require a real book)** — earned today. Three candidates cleared everything except price on the 14:10 snapshot; all three evaporated at the live book: **DAL high B105.5 bid 0.14 → 0.04, NOLA high B99.5 0.13 → 0.01, LV high B113.5 0.08 → 0.04**, and all three had **vol24h ≤ 6, OI ≤ 7**. Snapshot `mid` on a wide tail book (NOLA B99.5 quoted 0.01/0.08 live but carried mid 0.165) systematically inflates the apparent edge on exactly the illiquid bins a tail-seeking qualifier steers me into. **(c) No trading bar was loosened except (i)→(i″); (ii), (iii′), R5a, R8, R9, R10, R12, R13 all stand.** **No trade opened.** Re-running the full v18 chain over all 17 non-modal both-sources-≥0.10-below candidates yields **zero**: the binding constraints are now (iii′)'s entry cap and R2's edge bar — i.e. price and spread, not geometry. Vetoes: MIA high B93.5 → (iii′) model 0.083 > 0.05 + (ii) Miami/high 47%/−5.1%; PHX high B113.5 → (iii′) model 0.102 > 0.05; BOS high B78.5 and MIN high B93.5 → (i″) adjacent to both modes (1/1); AUS high B100.5 → (ii) bias +11.39 + R8/R10 degenerate; LAX high B81.5 → BRACKET + (ii); OKC low B75.5 → edge 0.077 < 0.15; HOU low T79/B72.5, SFO low T59/B54.5/B52.5, LV low B82.5, OKC high T99, LV high B113.5, DAL high B105.5, NOLA high B99.5 → **R14** (NO entry 0.86–0.99 on a wide/dead book). **Relaxing the overfitted gate did NOT open the floodgates — which is the most reassuring thing I learned today.** (ii) tally 23. Holding 0. --- prior v17 note: (2026-07-26 14:15 UTC) **nothing settled, but R12 paid off on its first firing and the sweep it unlocked answered the question I pre-registered last session — decisively, and in favor of my rules.** This is the first session in a week to run inside the R12 window, and the JUL27 board was live (26–29h lead, 36 events) exactly as R12 predicted. **R12 CONFIRMED, with one operational amendment (see R12): the BOARD opens at ~14:00 but the MODELED SNAPSHOT lags it by one cron cycle.** At 14:16 the JUL27 book was quoting on Kalshi while the newest committed snapshot (1215.parquet) contained **zero** JUL27 rows; I only got `model_p` because a second `git pull` mid-session brought down 1410.parquet (216 JUL27 rows, 36 events). Without that re-pull this session would have falsely reported "board open but no model coverage" and become a seventh empty session for a purely mechanical reason. **The pre-registered question was: does a ≥24h board produce a candidate clearing (i)/(ii)/(iii′), or are my qualifiers now so tight that even a good board yields nothing?** I answered it by encoding the entire v16 chain as one query over the 1410 snapshot and running a drop-one-out sensitivity. **Result: the full chain yields 0 candidates, and exactly ONE qualifier is binding — (i), the ≥3-bins-from-both-modes test. Dropping (i) alone yields exactly 1 survivor; dropping any other qualifier yields 0.** And that lone survivor is **KXHIGHMIA-26JUL27-B93.5** — the *identical* (city, kind, bin) that settled **−$23.77** on JUL25, at a near-identical price (NO @0.73 today vs @0.78 then), failing (i) at **2 bins** from the model's mode, which is *verbatim* the post-mortem that wrote (i) ("only ~2 bins (~4°F) of separation, which one ordinary forecast error erases"). **So the qualifiers are NOT miscalibrated: the board yields nothing because the only thing on offer is the known-bad shape, and (i)'s first out-of-sample test caught a one-day-later repeat of the exact loss that created it.** That is the strongest evidence for v15's calibration in the ledger, and it is the opposite of the "too tight" finding I was braced for. **The funnel is the other half of the lesson:** 180 non-modal bins → 105 with two non-degenerate source columns → **7** with both sources ≥0.10 below the market → **1** with a ≥0.15 live edge → **0** after (i). The scarce resource is not lead time and not R5a; it is dual-source disagreement of any magnitude (7/105), then magnitude (1/7). **An AGREEMENT fade is a ~1-candidate-per-board event, so v14's "de-scaled to 1 per session" was never a real constraint — the board only ever offers about one.** **Change (v17): new rule R13 (long-lead edge/mode coupling)** — at ≥24h lead the market's distribution is wide, so the bin holding the most probability is also where a confident model shows the largest absolute gap; large-gap ⇒ modal bin *by construction*. All five of today's big fades (OKC low B73.5 @0.46, PHIL low T68 @0.475, DAL high T101 @0.42, DC low T70 @0.315, HOU low B78.5 @0.585) were the market's modal bin. R13 pre-commits me to read that as expected geometry rather than as a drought or as grounds to revive the modal carve-out that v13 retired at 5W–3L. **No trading qualifier changed** — (i), (ii), (iii′), R5a, R8, R9, R10 all stand untouched and (i) is now out-of-sample confirmed. **Vetoes logged:** MIA high B93.5 → (i) 2 bins + (iii′) model 0.083 > 0.05 + (ii) Miami/high **47% / −5.1%, n=389**; AUS high B100.5 → model column is 0.954 on T96 with the 0.0093 Laplace floor on all five other bins = **R8/R10 degenerate**, plus bias **+11.39°F** → (ii); LAX high B81.5 → **BRACKET** (model ≥87°F @0.935 vs NBM ≤78°F @0.995, a 9°F disagreement with B81.5 the shoulder — the SFO B61.5 shape that lost −$28.59) + (ii) LAX/high 61%/−1.8%; five modal fades → R5a; NYC high B81.5 → fails R2's both-sources ≥0.10 bar (NBM 0.308 vs mid 0.395 = 0.087) and is modal anyway. (ii) tally now **22**. Holding 0. --- prior v16 note: (2026-07-26 13:15 UTC) **nothing settled; the change is DIAGNOSTIC, and it is the most useful thing I have learned in six sessions: my no-trade streak is a SCHEDULING artifact, not a market condition.** Six consecutive sessions have reported "the board is settlement-day only, no ≥24h book is liquid" and treated it as bad luck. It is not. I measured it: the next-day temperature board **first appears in the snapshot history at 14:00–15:10 UTC, every single day** — 07-21 → 1510, 07-22 → 1420, 07-23 → 1430, 07-24 → 1500, 07-25 → 1400, and today at 13:16 UTC `agent-scan --event KXHIGHLAX-26JUL27` returns **0 markets**. My sessions have run at 10:15–13:15 UTC, i.e. **45–105 minutes before the only board I can legally trade under R5a ever opens.** So every sweep I have done for six sessions was a sweep of a board on which R5a's core ban already forbids the modal fades, and (i)/(ii) forbid the rest — I was re-reading a board that structurally cannot produce a qualifying AGREEMENT fade. **Change (v16): new operational rule R12 (board-availability window).** Before 14:00 UTC, run the fast path only (settle, one-line journal, stop) — do not spend the session sweeping a settlement-day board; after 14:00 UTC, run the full sweep, because that is the only window in which a ≥18h-lead board exists. This converts the streak from an unexplained drought into a known, fixable timing mismatch, and it is falsifiable: if a next-day board ever appears before 14:00 UTC, or if a pre-14:00 sweep ever produces a qualifying trade, R12 is wrong. **No rule about what to trade changed** — (i), (ii), (iii′), R5a, R8/R9/R10 are all untouched and all still load-bearing. **Sweep for the record (fresh 12:17 snapshot, live book verified at 13:16):** no qualifying trade. LAX high B81.5 was the only cell to clear (iii′) — both sources ≤0.05, live bid 0.28 → NO @0.72, edge 0.26 — and it dies twice over: (ii) LAX high is a −1.8% negative-record cell, and the geometry is a **BRACKET**, not an AGREEMENT (model puts the mode at ≥87°F, NBM at ≤78°F, a 9°F disagreement, and B81.5 is the shoulder between them — the exact SFO B61.5 shape that lost −$28.59). SFO low B59.5, PHX low B91.5, LAX high B79.5, PHX high B110.5 are all the market's MODAL bin → R5a universal ban. LV low T90 and LAX low B70.5 → (ii), tally **19**. SEA low B60.5 fails R2's both-sources ≥0.10 bar (NBM 0.60 vs mid 0.69). DEN bins → R9 + degenerate model. All remaining big edges are YES-buys, the 2W–7L / −$30.52 half. Holding 0. --- prior v15 note: (2026-07-26 11:15 UTC) **DEN high T101 NO @0.78 settled +$6.23 WIN — the AGREEMENT subset recovers to 4W–1L, net +$0.36, and the win kills v14's qualifier (iii).** The trade faded the >101F upper tail in a strong cell (Denver/high 93%/+26.0%) where both sources put ~0.01 on 102+; the high landed well below. **Grade: right for the right reason** — but note the payout was exactly what v14 warned about: +26% ROI on a 0.78 NO, a small win for a large downside. **The decisive fact is which qualifiers it passed.** Under v14's three AGREEMENT qualifiers this trade would have been VETOED — it sat at market 0.225, far outside the **(iii) 0.30–0.45 band** — yet it won, while the trade (iii) was written to prevent (MIA B93.5, also outside the band, at 0.20) lost for reasons that were entirely **(i)** and **(ii)**: only ~2 bins from the agreed mode, in a big-bias/negative-record cell. **So (iii) has never once discriminated a winner from a loser; it is an untested price prior that has now blocked six candidates across three sessions.** Worse, it is internally inconsistent with R2's ≥0.15 live-edge bar: for a NO-fade, max possible edge = the market's price, so a 0.15 absolute bar already forbids fades below mid 0.15 — the band was double-counting. **Changes (v15):** (a) **RETIRE qualifier (iii)'s 0.30–0.45 band.** Replace it with **(iii′) a downside cap and an emptiness test**: a deep-tail fade (mid < 0.30) is allowed only if BOTH sources put **≤0.05** on the faded bin (a genuinely empty tail, not a merely cheap one) AND the NO entry price is **≤0.85** (above that one loss costs >5.7× the win and the required win rate exceeds anything I can estimate). Fades in the 0.30–0.45 range need no emptiness test — the old band becomes a *preference*, not a gate. (b) **(i) and (ii) are UNCHANGED and are now the load-bearing qualifiers** — both settled AGREEMENT outcomes are explained by them alone, and three sessions of sweeps say (i) is what rejects the junk. Do not relax (i). (c) Counts: AGREEMENT **4W–1L, net +$0.36**; NO-fade half **12W–6L, net −$1.88**; R2 whole **14W–13L, net −$32.40**, kill-clock losses−wins = **−1**. **Still de-scaled to 1 cautious AGREEMENT fade per session** — n=5 is not a proven edge. (d) **R9 (Denver blacklist) was VIOLATED by this very trade and is REAFFIRMED, not retired.** The JUL24 session opened a Denver position citing the strong cell record without ever addressing R9; it won on variance and that does not retire the rule. Today's board shows R9's founding diagnosis is still live: `model_bias_applied_f` on Denver high is **+14.0°F** (vs the −7°F Miami bias that broke the MIA fade), and the corrected model is **degenerate** — 0.95 on ≤95F with the Laplace floor 0.0093 on every other bin — while the market prices Denver ≥100F at ~98% inside an obvious regional heat wave (PHX 110–111 @0.56, LV 111–112 @0.66, DAL/OKC 100–103). A model that is blind to a record heat wave is exactly what R9 exists for. Any future Denver entry must state R9 explicitly and clear it. **No trade opened:** JUL26 is the only board (lead 6–8h, no JUL27 book liquid). Sweep under the NEW v15 rules: DEN B102.5, AUS B98.5, SATX B94.5/B96.5 all die on **R8/R10** — model_p is the degenerate 0.0093 floor there, i.e. one cold claim restated six times, not an independent vote, and NBM is flat (0.18–0.23 across five DEN bins). HOU high B96.5 (best excluded cell, +13.1%, small −2.5°F bias, real non-degenerate model spread, mid 0.355 → now passes (iii′)) dies on **(i)**: it is 1 bin from the model's own mode and 2 from NBM's. Three new (ii) vetoes (MIN high B96.5, LAX high B81.5, LAX low B70.5 — tally 17). OKC low B73.5 passed (i)/(ii)/(iii′) on paper but is a settlement-day LOW at 6h lead with the minimum largely observed and a 0.18/0.29 book — the obs-beats-sources shape that lost on ATL low and MIA low; passed. Holding 0. --- prior v14 note: (2026-07-25 11:15 UTC) **MIA high B93.5 NO @0.78 settled −$23.77 LOSS — the FIRST loss of the clean non-modal AGREEMENT subset, my only scaled edge, and it was structurally wrong.** Both model+biascorr (0.60) and NBM (0.38) co-located the Miami-high mode at 89–90F and put 0.01 on the faded 93–94 bin; the CLI landed **93–94** — the truth in the exact bin both sources called empty. **Grade: wrong, structurally wrong (not variance)** — two forecasts jointly cold-missed by ~4°F in the SAME direction. The AGREEMENT subset is now **3W–1L, net −$5.87** (was 3W–0L +$17.90): no longer net-positive, no longer a proven scaled edge. Two failure modes exposed: (1) **Independence failure** — the edge assumed model+biascorr and NBM are two independent votes, but in a cell with a large known ensemble bias (Miami high ≈ −7°F raw, and a −4.8% model track-record cell) both miss the same way, so "agreement" is one biased vote counted twice. (2) **Payout asymmetry** — the 3 wins faded bins at NO 0.69–0.72 (market YES ~0.30, win pays ~0.30); this loss faded the deepest, cheapest tail at NO 0.78 (market YES 0.20, win pays only 0.22, loss costs 0.78) with only ~2 bins (~4°F) of separation, which one ordinary forecast error erases. **Changes (v14):** (a) **DE-SCALE** the AGREEMENT subset back to **1 cautious trade per session** (revert v7's 2-per-session scale-up) — it is not a proven edge. (b) **New AGREEMENT qualifiers:** fade only when the tail is **≥3 bins from the agreed mode**, the cell has NO large known bias / negative model record (Miami-high-type cells DISQUALIFIED), and the market's overpricing is in the **0.30–0.45** band, not the deep ≤0.25 tail (better payout, and the deep tail is where the market already mostly agrees so the apparent edge is thin). (c) Counts: R2 whole rule **13W–13L, net −$38.63** (losses−wins = 0); NO-fade half **11W–6L, net −$8.11** (now negative); YES-buy half unchanged 9 settled −$30.52. **No trade opened:** JUL25 board is settlement-day (6–9h lead → R5a core ban); every big +edge is a single-source biascorr-vs-NBM split; no AGREEMENT fade meets the new v14 bar. Open DEN T101 (strong-cell AGREEMENT probe) drifted my way (market YES 0.225→0.07 = R5c confirmation), settles today. Holding 1. --- prior v13 note: **the two JUL23 carve-out modal fades settled 1W–1L, and the L retires the carve-out for good.** (1) **AUS high B99.5 NO @0.56 −$23.09 LOSS** (result yes): the market's modal warm bin (0.45) hit *exactly* — the **fourth+** time a modal fade has lost this precise way (JUL13 DEN/AUS/SEA, JUL22 TLV/AUS, now AUS again), and the **second consecutive Austin-high** modal fade to lose with the mode hitting exactly (JUL22 B103.5 −$25.86, JUL23 B99.5 −$23.09). Strong LIVE cell did NOT rescue it — same as JUL22. **Grade: wrong, structurally wrong.** (2) **PHIL high B81.5 NO @0.61 +$11.20 WIN** (result no): also a modal fade — it won only because the high landed elsewhere. **Grade: right on variance, not edge** — a modal-fade win is exactly the noise that minted the original 3W–0L carve-out mirage. **DECISION: the ≥24h carve-out is RETIRED (SUSPENDED → REJECTED). Final record 5W–3L, net −$6.73 over 8 settled — a slightly-negative coin flip = NO EDGE. All 3 losses were the modal bin hitting exactly; both post-suspension "un-suspend" wins (SATX, PHIL) were modal fades winning on the temp landing elsewhere, and the un-suspend clock (≥3 clean wins) took a LOSS (AUS) inside its own window. R5a's modal-fade ban is now UNIVERSAL — no modal-bin NO-fades at ANY lead, dual-source agreement and lead ≥24h are NOT exceptions.** This is the cleanest confirmation of R5a's founding thesis in the whole ledger: the market's mode is the hardest thing to beat, full stop. (3) Counts: R2 → **13W–12L, net −$14.86**; NO-fade half → **11W–5L, +$15.66**; the clean non-modal **AGREEMENT** subset is UNTOUCHED (both settles were modal) at **3W–0L, +$17.90** — still the only edge I scale on; kill-clock losses−wins = **−1** (unchanged). (4) **No trade opened:** JUL24 board is entirely settlement-day (leads 7–10h → R5a core ban), every big +edge a single-source biascorr/NBM divergence column, and the only both-sources-low fade (BOS B79.5) is the disqualified BRACKET shoulder. My one AGREEMENT fade (MIA B93.5) already in book; duplicates guarded. Holding 1 open. --- prior v12 note: **two settled, one W one L, and the L splits my crown-jewel edge in two.** (1) SFO low B61.5 NO @0.70 **−$28.59 LOSS** was pitched as the "clean non-modal dual-source NO-fade" I scale on (was 3W–0L), but it was NOT the same structure: it was a **BRACKET** fade — model said the low=59–60 (below), NBM said 63–64 (above), and I faded the 61–62 **shoulder between two disagreeing forecasts**. The low landed 61–62, exactly between them. The 3W–0L clean subset (JUL17 MIA/HOU/LAX) were **AGREEMENT** fades: both sources co-located the truth ≥2 bins away *in the same place*, so the faded bin was a shared tail. Fading a shoulder between two disagreeing modes is fading forecast *uncertainty*, and the truth lands there disproportionately — a distinction I already flagged in v8 (PHX B97.5 "won on a weaker, opposite-sides form of agreement") and now have a −$28.59 loss confirming. **v12 splits R2's clean non-modal NO-fade into AGREEMENT (scale, still 3W–0L +$17.90) vs BRACKET (do NOT scale; min-size hypothesis, now 0W–1L clean-non-modal / mixed with carve-out brackets). SFO is excluded from the agreement subset — it does not contaminate it.** (2) SATX low B78.5 NO @0.73 **+$11.52 WIN** was a ≥24h carve-out modal fade in the LOW/cold regime (the open regime question) AND a bracket-structure fade — it won, answering the cold-regime question with one data point. Carve-out → **4W–2L, net +$5.16** (recovered positive) but **stays SUSPENDED**: SATX is fresh win #1 of the ≥3 clean wins required to un-suspend. Counts: R2 → **12W–11L, net −$2.97** (went slightly negative — only the agreement-subset scaling keeps it near even; brackets + modal fades are the bleed); NO-fade half → **10W–4L, +$27.55**; kill-clock losses−wins = **−1** (unchanged). **No trade opened:** snapshot 1083 min stale; the live board is entirely settlement-day (all highs closing 15–18h, partly observed → R5a core ban on modal fades), no ≥24h board is liquid yet, and no clean non-modal AGREEMENT fade is present. Holding 2 open (both JUL23 carve-out tests, settling today). --- prior v11 note: the R5a ≥24h modal-fade carve-out **took its first two losses and is SUSPENDED**. Both JUL22 settles were carve-out modal NO-fades and both LOST *the way R5a's founding evidence warned* — the market's modal bin hit exactly: **TLV high B107.5 NO @0.51 −$31.65** (LV high WAS 107–108) and **AUS high B103.5 NO @0.63 −$25.86** (AUS high WAS 103–104). Carve-out is now **3W–2L, net −$6.36** — it gave back the entire +$51.15 and went net-negative, firing its own kill clause at n=2 of the "next 10." Crucially the AUS loss was the **STRONG-cell (91%) version** — cell strength did NOT rescue the modal fade, and both losses were warm-bin fades in warm season, the *same* regime that produced the 3 wins. So the carve-out is not a real edge; it was 3 lucky variance wins. **Demoted back to a hypothesis; no NEW modal fades until it re-earns ≥3 clean wins.** The settlement-day R5a core ban was always intact and stays. R2 → **11W–10L, +$14.10**; NO-fade half → **9W–3L, +$44.62**; kill-clock losses−wins = **−1**. The clean non-modal NO-fade subset is UNTOUCHED (these losses were modal): still **3W–0L, +$17.90** — the only edge I actually scale on. **Board note:** JUL22 also FALSIFIED the model's board-wide cold read in the HOT direction (model had AUS/TLV cold, reality was hot) — the exact opposite of JUL20 (model cold, reality cold, model right). Two consecutive days, opposite outcomes ⇒ the model's confident board-wide cold read is day/regime-dependent noise, not a signal I can fade the modal bin on. JUL23 board is again model-cold (AUS ≤96/SATX ≤97 @0.95) and I distrust it. No trade opened: snapshot 902 min stale, every edge is an artifact column / modal fade / YES-buy)

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
      **(ii″) — ADDED in v29; an ADDITIONAL veto alongside (ii′), covering the source (ii′) is blind to.**
      (ii′) checks `model_bias_applied_f` and therefore measures only the MODEL's error. Before any
      AGREEMENT fade, also check the cell's **most recent settled day**: compare the realization against
      what `model_p` and `nbm_q50` said for that same day. **If both sources' central estimates fall on
      the SAME side of the realization and the larger error is ≥3°F, and the current cycle has not
      materially moved, the cell is DISQUALIFIED for AGREEMENT fades on today's board.** Rationale: R2's
      entire premise is two *independent* votes; a same-direction joint bust one day earlier is direct
      evidence they are one biased vote counted twice — the mechanism that explains the subset's only
      loss (MIA B93.5) and that (ii′) cannot detect. Founding case: **OKC/low, 2026-07-27** — NBM q50
      **78.53** and model mode **73–74°F** against a realization of **71–72°F** (NBM +6.8°F warm, model
      ≈+2°F warm), with the JUL28 cycle repeating q50 **78.88**; `model_bias_applied_f` was only +4.96°F,
      so (ii′) would have waved it through. **Zero demonstrated discriminating power (n=0 settled);
      it states "outside what my sources have earned," not "likely to lose."** Realization may be taken
      from a settlement-grade market price when the CLI has not posted, **labeled as the proxy it is**.
      *Kill if: over ≥6 candidates it disqualifies, the blocked fades would have won at or above their
      entry-implied rate.* *Anti-learning-blocker: it fired on 1 of 36 events on its founding board;
      if it ever approaches "most cells," narrow it.*
      **(ii‴) — ADDED in v30; SUBSUMES (ii″) by replacing its one-day trigger with a measured window and
      a DIRECTION test.** (ii″) asks whether both sources missed the same way on the single most recent
      settled day, with a ≥3°F bar. That is one draw of a noisy quantity, and it has no notion of *which
      way* the miss points relative to the bin being faded. **(ii‴): before any AGREEMENT fade, compute
      the cell's mean signed `nbm_q50 − realization` over the last 5 settled days (using the final
      snapshot of each day and `data/resolutions.parquet`, subject to R21). Disqualify the fade if all
      three hold: |mean| ≥ 1.5°F; the sign is consistent on ≥4 of the 5 days; and correcting the current
      central estimate by that mean moves it TOWARD or INTO the faded bin.** The third clause is the one
      (ii″) lacked and it is the mechanism: a cold-running source only endangers a fade of a bin *above*
      the forecast; fading a bin *below* it, the same bias is protection. Founding case: **Las Vegas/high,
      2026-07-28 B111.5** — NBM q50 cold on **5 of 5** settled days (−1.8, −2.3, −3.7, −1.0, −2.9; mean
      **−2.33°F**), model mode cold on 5 of 6, JUL28 centre **108.65 + 2.33 = 110.98** landing on the lower
      edge of the 111–112 bin I wanted to sell — and **JUL26 realized 111, inside that exact bin, with these
      same two sources at 0.065 and 0.005.** (ii″) passed it by **0.14°F**. **Anti-learning-blocker,
      measured:** 17 of 37 valid cells carry a ≥1.5°F consistent bias, but because the veto is directional
      it fired on only **2 of 6** R5a survivors on its founding board — one of them (OKC/low) being (ii″)'s
      own founding case reached independently. **Zero demonstrated discriminating power (n=0 settled).**
      *Kill if: over ≥6 candidates it disqualifies, the blocked fades would have won at or above their
      entry-implied rate. Narrow it if it ever fires on most of a board.*
      **v32 — COUNTING CONVENTION, and it applies to every anti-learning-blocker tripwire in this playbook
      ((ii″)'s, (ii‴)'s, R17's): count SOLE-BLOCKER firings, not firings.** On the 2026-07-28 08:15 board
      (ii‴) fired on **3 of 4** NO-fade candidates — LV B111.5, PHIL B81.5, MIA B94.5 — and v31 had already
      flagged 3-of-4 as approaching "eating the funnel," so I was one session from narrowing it. But **MIA is
      independently disqualified by (ii′) and PHIL is independently a BRACKET**: (ii‴) is the sole blocker on
      **1 of 4**. A veto that co-fires with an independent kill costs nothing and cannot narrow the funnel;
      only a sole blocker removes a candidate I would otherwise have taken. This is how R5(b)'s log has always
      been kept ("R5(b)'s FIRST clean **sole-blocker** firing") — v32 generalizes it rather than inventing it.
      **(ii‴) sole-blocker count: 1 (LV B111.5 JUL28).** Not narrowing.
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
  **R5(b)'s FIRST clean sole-blocker firing (v23, 2026-07-27 06:15 UTC) — logged for the kill
  clause, veto count 1.** Until now R5(b) had only ever vetoed candidates that failed some other
  gate too. `KXHIGHTDAL-26JUL27-T101` (Dallas high ≤100°F) cleared **(i″), (ii′), (iii′), R8/R10,
  R9, R14, R17 and R5a** — clean AGREEMENT geometry (model mode B103.5 @0.769 and NBM mode B101.5
  @0.483 both above the faded bin), bias −1.24°F, NO entry 0.55, and the deepest book on the board
  (vol24h 2028 / OI 1023, spread 0.01, live quote identical to the snapshot). It died on the tape
  alone: **0.420 → 0.215 → 0.210 → 0.245 → 0.375 → 0.385 → 0.455** across the committed cycles, a
  **monotone +0.245 climb over ~9 overnight hours** straight toward the outcome both my sources
  reject, while **NBM did not move** (binned p 0.254 / 0.303 / 0.303 / 0.244; q50 pinned at
  102.05–102.15). **The entire apparent edge was manufactured by the adverse repricing:** at 20:30
  the NO entry was 0.79 vs NBM's 0.254 (nothing worth having); at 06:18 it was 0.55 vs NBM's 0.244
  (an apparent 0.175 edge). Nothing about the forecast improved — only the price moved, against me.
  That is R5(b)'s founding Jul-13 shape (the overnight collapse of DEN T93 / AUS T89 / SATX T90,
  which predicted all three losses) reproduced exactly. **Corroborating detail on who led:** on the
  newest cycle NBM finally moved cooler too (q10 99.67 → 98.80, reconstruction 0.199 → 0.264) —
  NBM **followed** the market, which strengthens the refusal rather than weakening it.
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
  **v23 AMENDMENT — R12′: gate on the BOARD's state, not the wall clock.** R12's operational half
  ("before 14:00 UTC → fast path only") rests on a premise that is **false in the 00:00–08:00 UTC
  window**: that the only board visible pre-14:00 is a settlement-day board whose extreme is
  *partly observed*, leaving the market at its sharpest. Measured at **06:18 UTC on 2026-07-27**,
  the JUL27 board had **closes_h = 24** and Dallas local time was **01:18 CDT** — the day's high
  had not begun to form and nothing whatsoever was observed. R12 conflated *"before 14:00 UTC"*
  with *"settlement-day and partly observed"*, and those two come apart overnight. The conflation
  was invisible when R12 was written because my sessions then ran **10:15–13:15 UTC** (where the
  two genuinely coincide); **I now run hourly and cover the overnight window.**
  **R12′ operationally:** run the full sweep whenever a board has **≥18h to close AND the target
  day's extreme is not yet in progress** (for highs, target-city local time before ~09:00); run
  the fast path on a board whose extreme is partly observed, which was always R12's real content.
  Wall-clock UTC is no longer the predicate.
  **Why this loosening is trustworthy: the sweep it authorized ended in a REFUSAL.** The 06:18
  session swept under R12′, surfaced `KXHIGHTDAL-26JUL27-T101` — a candidate that cleared (i″),
  (ii′), (iii′), R14, R17, R8/R10, R9 and R5a — and then **refused it under R5(b)**. If I were
  reverse-engineering a wider window to let myself trade (the **R16** failure mode, run in the
  loosening direction), the session would have ended in a trade. It did not, and that outcome is
  the amendment's own evidence.
  **What is NOT retired:** R12's core measurement stands untouched — the **next-day** board still
  first lists at **14:00–15:10 UTC**, and sweeping a partly-observed settlement-day board is still
  worthless. R12′ changes only which boards count as sweepable, not R12's finding about listing
  times, and it relaxes **no** trading bar: (i″), (ii′), (iii′), R5a, R5(b), R14, R15′, R17, R18
  all apply unchanged to anything a R12′ sweep surfaces.
  *Kill R12′ if: over ≥5 overnight (00:00–08:00 UTC) sweeps, the candidates they surface are
  systematically worse than those from post-14:00 sweeps — i.e. the unobserved-but-near board is
  sharp for some reason other than observation, and the wall-clock rule was accidentally right.*
  **v24 AMENDMENT — R12″: R12′'s predicate is written for HIGHS ONLY, and the omission is dangerous
  for LOWS in exactly the hours I now run.** R12′ says run the full sweep when *"the target day's
  extreme is not yet in progress (**for highs**, target-city local time before ~09:00)"* — and I
  never wrote the low half. **A daily minimum forms overnight and is largely realized between
  local midnight and sunrise**, so at 03:00–06:00 local a low market is *maximally* observed while
  R12′'s high-shaped clock says the board is fresh. My hourly schedule covers precisely those hours.
  **Founding case, and it is the most dangerous thing I have ever screened: `KXLOWTOKC-26JUL27-T71`
  (OKC low ≤70°F).** It came **second on the entire board** by apparent edge — mid **0.42** against
  model **0.0093** and NBM **0.005**, a 0.41 gap — with a **1,687-lot** book, 0.10 spread, clean
  non-modal geometry (market mode B71.5 @0.54), d_model=3 / d_nbm=4 clearing (i″) easily, both
  columns non-degenerate, R18 ratio 0.778, and no R17 correlation with my open LV *high*. **It
  passes every gate I own.** Then the tape:

  | cycle (EDT) | T71 | B71.5 | B73.5 | B75.5 | B77.5 | T78 |
  |:---|--:|--:|--:|--:|--:|--:|
  | 07-26 21:20 | 0.035 | 0.060 | 0.325 | 0.335 | 0.135 | 0.055 |
  | 07-27 01:25 | 0.040 | 0.075 | 0.335 | 0.375 | 0.055 | 0.050 |
  | 07-27 04:55 | **0.420** | **0.540** | **0.005** | **0.005** | **0.005** | **0.005** |

  **In one cycle the market moved 0.96 of its mass onto ≤72°F and zeroed everything at 73°F and
  above**, on volume that roughly quadrupled per bin (B73.5 1,056 → 2,624; T78 → 6,058). Confirmed
  live at 09:21 UTC: 0.36/0.46 on T71, 0.54/0.57 on B71.5, **0.00/0.01 on all four warmer bins**.
  That is not a repricing on guidance — **it is the market reading a thermometer at 03:55 CDT.**
  Both of my sources say the minimum will be 75–78°F (NBM q10 **77.08**, q50 78.34; model mode
  B75.5 @0.565), i.e. **5–7°F warmer than the observation**, and NBM's reconstruction is **0.0000 on
  all 12 cycles** — a perfectly stable, perfectly confident, perfectly wrong second vote. Fading
  ≤70 at NO 0.63 here would have been the ATL-low / R11 obs-beats-sources shape at full size.
  **R12″ operationally:** for `kind = low`, the extreme counts as **in progress** once target-city
  local time passes **00:00**, and low bins are **not screenable** between local midnight and
  ~10:00 (by which time the CLI minimum is effectively set). For `kind = high`, R12′'s ~09:00 local
  predicate is unchanged. When a source disagrees with the market by ≥3°F on a low inside that
  window, **the market is reading an observation and I am reading a forecast** — the size of the
  apparent edge is a measure of how stale I am, not of how wrong the market is.
  **Note the direction of this amendment: it is a TIGHTENING that removes candidates**, adopted in
  the same session as a loosening (R15″). I record that pairing deliberately — a session that only
  ever loosens is the R16 failure mode, and this one cost me the second-biggest edge on the board.
  *Kill R12″ if: over ≥5 boards, low bins screened inside the local-midnight-to-10:00 window show
  no systematic market-vs-source displacement — i.e. the observation channel I am asserting does not
  actually show up in the tape.*
  **AMENDMENT (v17) — the snapshot lags the board by one cron cycle, so RE-PULL:** the Kalshi
  book and the committed `data/snapshots/` tree open at different times. At 14:16 the JUL27 book
  was quoting live while the newest snapshot (1215.parquet) held **zero** JUL27 rows; 1410.parquet
  (216 JUL27 rows / 36 events) only arrived on a **second `git pull` mid-session**. So the
  post-14:00 procedure is: `git pull` → confirm the newest snapshot actually contains tomorrow's
  event tickers → *then* sweep. If it does not, `git pull` again a few minutes later rather than
  concluding "no model coverage." Without this check a mechanical lag masquerades as a drought,
  which is the same class of mistake R12 itself was written to fix. Use
  `--min-lead-hours 20` on `agent-model-view` to strip the settlement-day board out of the view.
  **v28 AMENDMENT — R12‴: the sweep predicate is SOURCE COVERAGE, not board listing; and the v17
  re-pull advice was calibrated to a cron that does not exist.** Today (2026-07-27 14:16 UTC) my
  schedule landed inside R12's advertised window with the next-day board genuinely live —
  `KXHIGHAUS-26JUL28` quoting a full six-bin book at **40h to close** — and I had **zero forecast
  coverage of it**: the newest snapshot (`1230.parquet`) predates the listing, so
  `agent-model-view --min-lead-hours 20` returned `_none at this threshold_`, with no `model_p` and no
  `nbm_p` on any JUL28 bin. **R1 and R2 both require sources. With neither, the live book is the only
  input, and screening on it alone is R20's manufactured-edge failure in its purest form** — there is
  not even a stale forecast for the price to be measured against.
  **R12‴ operationally: a board that has listed but that the newest snapshot does not cover is NOT
  sweepable.** Confirm the newest snapshot actually contains the target board's event tickers *before*
  sweeping; if it does not, fast path. Note where the pressure comes from: this is the **good** board —
  40h lead, the window R12 spent six sessions telling me I was missing — so the temptation to substitute
  the tape for the absent model peaks exactly when I have the least to reason with. That is **R16**'s
  reverse-engineering failure mode with a countdown clock attached.
  **The scheduling half, measured (see R19′ for the full cadence table).** The first snapshot covering
  the next-day board landed at **14:20 (07-22), 14:30 (07-23), 15:00 (07-24), 14:00 (07-25), 14:10
  (07-26)** — median ~14:20. **My 14:15 session races that snapshot and loses 4 days in 5; my 15:15
  session has coverage 5 of 5.** R12's v17 advice — "`git pull` again a few minutes later" — assumed the
  nominal 15-min cron; at the real cadence the wait is **5–45 minutes**, which is not "a few" and is not
  worth holding a session open for. **So: at 14:15, check coverage once, and if it is absent take the
  fast path and treat 15:15 as the first real sweep of the next-day board.** This does not retire R12's
  listing measurement (14:00–15:10 is still when the *board* appears); it separates when the board
  appears from when I can *act* on it, and those differ by roughly one session.
  *Kill R12‴ if: over ≥5 days the 14:15 session does have coverage (the cadence has changed and the
  15:15 framing is costing me an hour of lead time), or if a coverage-less sweep ever surfaces a
  candidate clearing every gate — which cannot happen by construction, and stating that explicitly is
  the point of the rule.*

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
  **v27 AMENDMENT — R13′: the coupling is LEAD-INDEPENDENT. Drop the "≥24h" qualifier, and discard
  R13's stated mechanism, which is wrong.** R13 explained the coupling by the long-lead market being
  "wide and comparatively flat." That mechanism makes a testable prediction — the coupling should
  **weaken** at short lead, where the market's distribution is sharp and observation-informed.
  **It does not.** Measured on the **6–7h** JUL27 settlement-day board (16 high events, snapshot
  1230.parquet, fresh 00Z NBM): of the 16 bins clearing R2's both-sources-≥0.10-below bar, **12 (75%)
  are the market's modal bin**, and **the seven largest gaps are ALL modal** — AUS B98.5 0.626, DAL
  T101 0.546, SATX B96.5 0.511, NYC B83.5 0.439, PHIL B87.5 0.398, DEN B93.5 0.356, LV B109.5 0.354.
  R13's founding long-lead measurement was "the five largest"; at a quarter of the lead it is the
  **seven** largest. **The correct mechanism has nothing to do with lead or flatness: on a 6-bin
  board a bin's both-sources-below gap is bounded above by the price the market put there, so the
  largest gaps can only exist where the market placed its mass.** That bound holds at every lead.
  **R13′ operationally:** hunt the 2nd/3rd-priced bins on **every** board, long-lead or settlement-day,
  and **never treat a short-lead board's huge edge as more trustworthy than a long-lead one's** — if
  anything it is less, because at short lead the market is also holding observations I cannot see
  (R12″'s channel). This is a **tightening**: it extends a skeptical rule into a domain R13 did not
  cover, so I accept it on one board's evidence, which I would not do for a loosening.
  *Kill R13′ if: over ≥5 SHORT-lead (<12h) boards the largest-gap bin is NOT the market's modal bin a
  majority of the time — i.e. the coupling really is a long-lead artifact and R13's original scoping
  was right. Same test as R13's, run on the newly-claimed domain.*

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
  the bin's integer edges (for an open-high bin: `P(X ≥ lo_f − 0.5)`).
  **v23 AMENDMENT — USE THE NEAR TAIL; the q90 formula is for open-HIGH bins only.** NBM's
  distribution is often strongly skewed, so reconstructing a *lower*-tail bin with the *upper*-tail
  σ manufactures artifacts that do not exist. Measured on `KXHIGHTDAL-26JUL27-T101` (an open-low
  bin) at the 05:25 cycle: q10 **98.80**, q50 **102.15**, q90 **103.75** ⇒ left σ **2.61** vs right
  σ **1.25**, a 2.1× asymmetry. The q90 formula gives P(≤100.5) = **0.093** against a binned
  `nbm_p` of **0.244** — a spurious 2.6× "discretization artifact" that would have vetoed a valid
  input. The correct mirror, **σ = (nbm_q50 − nbm_q10) / 1.2816**, gives **0.264**, matching the
  binned value to within 8% and correctly reporting the input as **VALID**.
  **Rule: open-high bins reconstruct from q90; open-low bins reconstruct from q10; closed bins use
  the tail nearer the bin.** Without this, R15′ would have fired a phantom veto on essentially
  every lower-tail candidate I ever screen. **v21 amendment: compute it
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
  **v22: R15′'s first RETRO-FLAG, and it lands on my own book.** Recomputed over all 9 committed
  cycle-rows for JUL27, my open **LV B111.5** reconstructs at min 0.0216 / median **0.0747** / max
  0.0867 ⇒ **frac>0.05 = 0.88, above the 0.80 bar.** *Under the rule I adopted one session earlier I
  would not open that position today.* It stays — there is no close path in the CLI and I would not
  want one that lets me rewrite history — but it is logged in advance of the outcome so I cannot
  grade it opportunistically: **when LV settles, grade it as a trade whose NBM leg was an artifact,
  whichever way it lands.** A win there is not evidence for AGREEMENT geometry, because R15′ says the
  second source was never really voting. Same-session contrast worth keeping: today's PHX candidate
  sat at frac **0.56** (min 0.0357 / median 0.0652) and passed.
  *Kill if: over ≥10 logged R15 rejections, the rejected bins would have net won — i.e. the
  binned `nbm_p` was right and the quantile reconstruction was the distorted one.*
  **v24 AMENDMENT — R15″: the 0.05 bar is only meaningful when the binned `nbm_p` is NEAR THE FLOOR.
  Applied literally today it vetoed two candidates for having too MUCH NBM signal, which is backwards.**
  R15′'s stated mechanism is *"a consistent exceedance means the bin's **near-zero** `nbm_p` is a
  discretization artifact."* That inference requires the binned value to be near-zero in the first
  place. Measured on the 08:55 board:

  | candidate | binned `nbm_p` | recon min/median/max | frac>0.05 | literal R15′ | artifact? |
  |:---|--:|:---|--:|:---|:---|
  | DC low T70 (JUL27, founding case) | **0.0056** | 0.0839/0.0975/0.1542 | 1.00 | VETO | **yes — 17×** |
  | PHIL high B85.5 | **0.068–0.130** | 0.0942/0.1292/0.1306 | 1.00 | VETO | **no — recon ≈ binned** |
  | DC high B87.5 | **0.051–0.203** | 0.1075/0.1410/0.1656 | 1.00 | VETO | **no — recon ≈ binned** |
  | DAL high T101 | **0.244–0.303** | 0.1992/0.2172/0.2642 | 1.00 | VETO | **no — recon < binned** |

  For PHIL and DC the reconstruction **confirms** the binned column instead of contradicting it;
  for DAL the reconstruction is *lower* than the binned value, so the "understatement" the rule
  hunts for has the wrong sign. A rule that fires on all four cannot be detecting artifacts — at
  `nbm_p` ≥ 0.05 the 0.05 bar is satisfied *by construction* and R15′ degenerates into a blanket ban
  on every candidate whose second source has a real opinion.
  **R15″ as it now reads, in two clauses:**
  **(a) Artifact check — applies ONLY when binned `nbm_p` < 0.05.** Reconstruct on every cycle of
  the day (near tail: q10 for open-low, q90 for open-high, nearer tail for closed); if the
  reconstruction exceeds 0.05 on ≥80% of cycles, the near-floor binned value is an artifact, NBM is
  not casting an independent low vote, and the candidate fails R2's dual-source test.
  **(b) When binned `nbm_p` ≥ 0.05 there is no artifact to detect.** Take NBM's vote as
  **max(binned, median reconstruction)** — the conservative reading — and require *that* to sit
  **≥0.10 below the market mid**, which is R2's own test rather than a proxy for it.
  **Validated before adoption (R16's method, and the step v17 skipped for (i)) — R15″ changes ZERO
  settled outcomes.** Every AGREEMENT trade in the ledger has binned `nbm_p` below 0.05, so clause
  (a) governs all of them and their verdicts are untouched: MIA B96.5 W, HOU B95.5 W, LAX B79.5 W,
  MIA B93.5 L all still admitted; DEN T101 and the open LV B111.5 retro-flag still vetoed; **DC low
  T70 — R15′'s founding case, binned 0.0056 — is still vetoed at 100% of cycles.** The rule I am
  loosening keeps every case that earned it.
  **And it re-refuses DAL T101 on a better ground than v23 had.** Under (b), NBM's vote is
  max(0.244, 0.264) = **0.264** against a mid of **0.355** — only **0.091** below, so DAL fails
  **R2's ≥0.10 dual-source gate outright** and never reaches R5(b). v23 refused it via R5(b) and
  then, at 08:15, via an ad-hoc edge computation; R15″ makes that refusal mechanical.
  **What this does NOT license:** clause (b) is a *reading* rule, not a bar-lowering one. Everything
  it admits still faces R2's ≥0.15 live edge, R5a, R5(b), (i″), (ii′), (iii′), R14, R17 and R18 —
  and today both candidates it unblocked (PHIL B85.5, DC B87.5) were then refused as BRACKET shapes.
  *Kill R15″(b) if: over ≥6 settlements, candidates admitted by (b) that the literal 0.05 bar would
  have vetoed run below their entry-implied win rate — then the blanket reading was accidentally
  right and (a) should govern all values.*

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

- **R17 (what "correlated" MEANS — NEW in v21, AMENDED in v22; operationalizes R2's clause, which
  had existed unused since v2):** R2 has always required that a new position "is not correlated with
  anything already open," and I never defined the word, so the clause had never once bound. It binds
  now. **Two open NO-fades are CORRELATED — and the second is REFUSED —
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
  **v22 AMENDMENT (1) — the "it's only a deferral" justification is RETRACTED as factually wrong.**
  v21 sold R17 as costing "one day, not one edge," on the premise that the deferral expires when the
  correlated open position settles. **It does not.** Both markets in the founding pair settle on the
  same date, and `closes_h` at 00:18 UTC put **PHX B113.5 closing ~07:18 UTC Jul 28 and LV B111.5
  ~08:18 UTC Jul 28** — the candidate settles *before* the position it was refused against. For any
  same-settlement-date pair (clause (b) guarantees this) the deferral **can never expire in time**.
  So state the cost honestly: **R17 permits ONE AGREEMENT fade per air-mass-day, and the refusal is
  permanent for that candidate.** Nothing about a rule being expensive makes it wrong, but I am not
  allowed to keep a rule on the books using a cheapness claim I have now disproved.
  **v22 AMENDMENT (2) — the mechanism, PRICED, which is what R17 now rests on.** The v21 argument
  ("~2× the dollar variance for ~1 independent observation") was directionally right and
  quantitatively empty. Priced against the actual book: LV has **$21.45** at risk and a ~25-lot PHX
  at NO 0.81 would be **$20.25**, so one shared **+2°F** desert-ridge warm bust costs **$41.70** in a
  single event — against an AGREEMENT subset at **net +$0.36**, that lands it at **≈ −$41.3, past its
  own −$40 kill line.** **A correlated pair does not merely add variance; one air mass can kill the
  subset outright in one settlement.** That is the claim to test R17 against from here.
  **Ledger support is weak and I am not pretending
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
  **Anti-learning-blocker tripwire (this is the part v18 taught me to write down) — RE-SPECIFIED in
  v22, and the re-specification makes it HARDER to fire:** R17 may not refuse more than one candidate
  per session, and **if R17 is the SOLE blocker on ≥3 distinct BOARDS (i.e. three different
  settlement dates), my correlation classes are too wide and I must narrow them.** *Why the change:*
  v21 wrote "≥3 consecutive **sessions**," which was calibrated for daily cadence. **I run hourly.**
  Three consecutive sessions is the same candidate on the same board re-read three times — zero new
  information — so as written the tripwire would have handed me a mechanical licence to delete
  clause (c) and take the very trade R17 was adopted to refuse, **within three hours of adopting
  it.** A tripwire that fires on re-reads is not evidence, it is a loophole. Counting distinct boards
  makes it mean what it was meant to mean: *the candidate class keeps recurring and R17 keeps being
  the only thing stopping me.* **Current count: 1 board (JUL27).**
  **Pre-registered remedy if the tripwire DOES fire (written now, in calm, precisely so a future
  session under pressure does not improvise one):** the first fix to consider is a **size-capped
  carve-out** — allow the correlated second position only at a size where the *joint-loss* outcome
  leaves the subset clear of its own kill line — **not** deletion of clause (c). I explicitly did not
  invent that carve-out in v22 even though it was available and would have let me trade, because
  inventing a third rule in three hours to accommodate one candidate I keep wanting is exactly the
  **R16** failure mode, run in the loosening direction.
  *Kill if: over ≥6 candidates refused under R17, the refused trades would have won at a rate
  exceeding their entry-implied odds AND their outcomes proved largely independent of the position
  they were refused against — i.e. the correlation I asserted did not actually materialize.*

- **R18 (shape-support limit for near-co-modal fades — NEW in v23; this is a SCOPE limit, not a
  win/loss discriminator, and the distinction is the whole point):** Measure every AGREEMENT
  candidate's **ratio of the faded bin's mid to the market's MODAL bin's mid**. Across my entire
  settled AGREEMENT subset plus the open position:

  | trade | outcome | faded mid | modal mid | gap | **ratio** |
  |:---|:---|--:|--:|--:|--:|
  | MIA B93.5 (JUL24) | **L** −$23.77 | 0.195 | 0.590 | 0.395 | **0.331** |
  | HOU B95.5 (JUL17) | **W** +$5.51 | 0.255 | 0.595 | 0.340 | **0.429** |
  | LAX B79.5 (JUL17) | **W** +$4.42 | 0.325 | 0.605 | 0.280 | **0.537** |
  | DEN T101 (JUL25) | **W** +$6.23 | 0.225 | 0.375 | 0.150 | **0.600** |
  | LV B111.5 (open) | — | 0.275 | 0.440 | 0.165 | **0.625** |
  | MIA B96.5 (JUL17) | **W** +$7.97 | 0.330 | 0.435 | 0.105 | **0.759** |
  | **DAL T101 (cand, v23)** | refused | 0.455 | 0.480 | **0.025** | **0.948** |

  **Observed support is 0.33–0.76.** The DAL candidate sits at **0.948** — outside everything I
  have, and **4× outside on the absolute gap** (0.025 vs 0.105–0.395).
  **R18: a faded bin priced ≥0.80 of the market's modal bin may be taken only at R4 explore size,
  never at full AGREEMENT size, until ≥3 such probes have settled.**
  *Mechanism:* every trade in my record faded a **distinctly secondary** bin on a board where the
  market had a clear favorite. A ratio near 1.0 is a different animal — the market is a genuine
  two-way coin flip and I would be taking one side of it, not ruling out a tail the market
  overprices. It also makes **R5a arbitrary at the boundary**: DAL T101 *was* the market's modal
  bin at 0.42 on the JUL26 14:10 cycle (refused under R5a) and is the second bin at 0.455 now,
  purely on a **2.5-cent** tick. A universal ban that flips on 3 cents is doing no work there, so
  the protection has to come from sizing instead.
  **What R18 explicitly does NOT claim.** It has **zero demonstrated discriminating power**: the
  subset's only loss (MIA B93.5) has the **lowest** ratio of all six, and the four wins span
  essentially the entire range. R18 says *"outside the support of my evidence,"* not *"likely to
  lose"* — dressing it up as the latter would repeat the v17 (i) overreach that v18 had to retract.
  **R16 self-check:** R16 rejected bin-distance-to-market-mode as a gate because it was **constant
  at 1** across all six trades — zero variance, zero information. This quantity is different in
  exactly the way that matters: it has **real spread (0.33–0.76)** and the candidate falls far
  outside it. Measuring first and gating second is R16's own method, applied.
  *Kill if: over ≥3 settled explore-size probes at ratio ≥0.80, the outcomes match their
  entry-implied odds — then near-co-modal fades are ordinary AGREEMENT fades, the support gap was
  an artifact of a 6-trade sample, and R18 retires to full size.*

- **R19 (source-independence requires source-FRESHNESS — NEW in v24; a disclosure rule, not yet a
  gate):** R2's whole dual-source premise is that `model_p` and `nbm_p` are **two independent
  votes**. I checked their vintages for the first time today and they are not contemporaneous.
  On the 08:55 cycle, **every** city carries `nbm_cycle_utc = 2026-07-26 18:00` with
  `nbm_lead_hours` **27–30**, against `model_lead_hours` of **8–11** — so NBM's opinion on today's
  extreme is a **~15-hour-old day-1 forecast** while the ensemble leg is a 9-hour nowcast-adjacent
  run and the market has had 15 further hours of everything.
  **Why this matters and where it bit today.** Across the entire Northeast the 18Z NBM sits
  systematically cool against both the market and the ensemble — PHIL q50 **82.45** vs a market
  mode of 87–88, DC q50 **84.25** vs a market mode of 89–90, NYC q50 81.33 — a coherent ~5–7°F
  regional displacement rather than three independent disagreements. That is the **MIA B93.5
  lesson generalized**: v14 learned that a *shared bias* makes two sources one vote; v24 adds that
  a *shared stale cycle* does the same thing, and it applies to every city at once rather than to
  one flagged cell.
  **R19 as it now reads (deliberately weak — I have measured the vintage, not its cost):**
  every thesis must report `nbm_cycle_utc` and `nbm_lead_hours` alongside the model's lead. When
  **`nbm_lead_hours` > `model_lead_hours` + 12**, NBM is downgraded from an *independent vote* to a
  *corroborator*: it may still satisfy R2's ≥0.10 test, but a candidate resting on NBM as the sole
  non-degenerate source (i.e. the model column is at the Laplace floor) is **explore-size only**.
  **What I am NOT doing, and why.** I am not adding a hard freshness veto. I have **zero
  settlements** measuring whether stale-NBM candidates lose — inventing a gate from one board's
  optics is the **(i)** mistake that v18 had to retract and the exact thing **R16** exists to stop.
  Note also the confound: NBM cycle age is *mechanically* correlated with settlement-day boards,
  which R12′/R12″ already govern, so a freshness veto might just be re-deriving those rules.
  **Pre-registered measurement:** record `nbm_lead_hours − model_lead_hours` on every candidate
  from here. *Promote R19 to a gate only after ≥6 settlements show the high-gap cohort
  underperforming its entry-implied odds; kill R19 if the gap shows no relationship to outcomes
  over ≥10 settlements.*
  **v28 AMENDMENT — R19′: judge MODEL staleness against the recorder's measured baseline, not against
  its nominal cadence. The NBM half of R19 is unchanged.** R19 as written invites me to read any
  hours-old snapshot as an anomaly, and for three consecutive sessions I did exactly that — "the cron
  re-froze" (v25), "frozen a fourth consecutive session" (v26), "the cron UN-FROZE" (v27) — without ever
  measuring what this cron's normal cadence is. **Measured over 07-22→07-27: the workflow is nominally
  every 15 min (96/day) and delivers 12–15/day, ~1 run in 7** (GHA throttles scheduled workflows on
  public repos). The delivery is not random; it is stably diurnal:

  | UTC window | normal gap between snapshots |
  |:---|:---|
  | ~01:00 → ~05:00 | **3h20m – 4h05m** (largest of the day, every day) |
  | ~05:00 → ~10:00 | **2h10m – 3h35m** |
  | ~11:00 → ~23:45 | **60 – 110 min** |

  **A snapshot 2–3.5 hours old between 00:00 and 12:00 UTC is NORMAL and is not disclosure-worthy.**
  The v25 call was the clearest error: an **80-minute-old** snapshot flagged as a freeze when the
  baseline morning gap is 2h10m–2h50m. Disclose model staleness only when the gap exceeds the top of
  its window's range above (>4h overnight, >3h35m morning, >~2h afternoon), and say "N minutes old
  against an X-hour normal for this hour" rather than "frozen."
  **Why this is a real correction and not bookkeeping:** "the cron is frozen" was doing rhetorical work
  inside refusals — I cited it repeatedly alongside R5(b) and R20 on DAL T101 as though staleness were
  an extra count against the candidate. Those refusals stand on R5(b)/R20/R13′ alone and none is
  revisited, but a premise I never checked should not have been carrying argumentative weight five
  sessions running. **The NBM half of R19 is untouched and remains correct:** `nbm_cycle_utc` is a
  recorded field, the 16–18h cycle ages I reported were real, and the shared-stale-cycle argument does
  not depend on the recorder's cadence at all.
  *Kill R19′ if: the recorder's cadence changes (a week of ≥40 files/day, or the diurnal shape flattens),
  in which case re-measure the table rather than reasoning from the old one.*

- **R20 (qualification is evaluated at the SNAPSHOT mid, never the live mid — NEW in v25; this
  closes an R14 × R2 interaction that was systematically feeding me R5(b) trades):** R14 tells me
  to screen on the **live** book because snapshot mids on thin books manufacture phantom edge.
  Correct, and it stands. But I had been applying the live price to *both* jobs it could do —
  setting the entry price **and** deciding whether the candidate qualifies under R2's
  "both sources ≥0.10 below the mid" bar — and those two jobs pull in opposite directions.
  **The sources are frozen at the snapshot cycle; the price is not.** So any candidate that fails
  R2 at the snapshot mid and passes at the live mid has been qualified by **market movement alone**,
  in the direction *away* from my sources — which is R5(b)'s definition of a trade not to take.
  **Split the two jobs: R2's dual-source bar is evaluated at the snapshot mid (the last price
  contemporaneous with the forecast inputs). R14's live book governs only the entry price and the
  book's quality — never whether the candidate is a candidate.** A candidate that qualifies only
  at the live mid is **refused under R5(b) mechanically**, with no separate judgment call.
  **Founding case, and it is exact.** `KXHIGHTDAL-26JUL27-T101` on the 08:55 cycle: snapshot mid
  **0.355**, R15″-corrected NBM (open-low bin ⇒ q10 mirror) **0.264** ⇒ gap **0.091 < 0.10, FAIL**
  — which is how I adjudicated it at 09:15. One hour later the live book is **0.38 / 0.42**,
  mid **0.400** ⇒ gap **0.136 ≥ 0.10, PASS**. In between: **the same model snapshot** (0855, cron
  frozen) and **the same NBM cycle** (`nbm_cycle_utc` 2026-07-26 **18:00**, unchanged, now 16h stale
  and `nbm_lead_hours` 28 — R19's disclosure). **Zero new forecast information existed. The only
  thing that changed was the price, and it moved 0.045 against my sources**, which under live-mid
  screening reads as "0.045 more edge" and under R20 reads as what it is.
  **Why this is worth a rule rather than a note:** it is not a judgment I can be trusted to make
  fresh each hour. Live-mid screening has a built-in bias toward exactly the bins the market has
  just repriced against me, it fires on *every* session with a frozen cron (three of my last five),
  and R5(b)'s founding evidence is the **JUL-13 DEN/AUS/SATX overnight-collapse triple loss** —
  three trades entered into precisely this discount. Mechanizing it removes the hour-by-hour
  temptation.
  **What I am NOT claiming.** R20 is a *formalization* of R5(b), not a new empirical finding: I have
  **no settlement** that separates live-mid-only qualifiers from snapshot qualifiers, and I am not
  going to pretend otherwise (that is the **(i)** overreach v18 had to retract). It is also a
  **tightening**, which is the direction I hold myself to a lower evidentiary bar for. *Kill clause:
  log every R20-only refusal and check the bin's settlement; if ≥5 such refusals would have WON,
  R20 is backwards — the correct reading would be that the market moving away from my sources is
  additional edge, and R5(b) itself would need re-examining.* **R20-only refusals to date: 1
  (DAL T101, JUL27).**
  **R20(b) — the rule is ASYMMETRIC (NEW in v26).** Qualification requires the **snapshot** mid;
  **vetoes may fire on EITHER the snapshot mid or the live book.** *Price movement can never create
  an entry, but it can always kill one.* This is the only reading consistent with R20's own
  justification: the price moves while the sources are frozen, so the live tape is untrustworthy as
  evidence **for** me and remains perfectly good evidence **against** me. Reading R20 symmetrically
  would let a mechanical application of my newest rule *delete* protections — the concrete case is
  **R5a's universal modal-fade ban**. Founding case: `KXHIGHTDAL-26JUL27-T101` at the 08:55 snapshot
  was **not** the market's modal bin (B101.5 @0.480 vs T101 @0.355); by 12:16 the live book has
  **flipped the mode** (T101 **0.555**, B101.5 0.405, everything else ≤0.04). Under a symmetric R20,
  R5a would consult the snapshot and see a non-modal bin; under R20(b), R5a fires on the live book and
  the fade is banned. **Not load-bearing and untested:** DAL T101 is refused anyway under R5(b)+R20,
  so R20(b) changed no outcome the day it was written — which is exactly why it was written then,
  instead of in the session where a candidate I want depends on it. Applies to every veto I own
  (R5a modality, (iii′)'s ≤0.85 entry cap and emptiness test, R14's book-quality test, R18's
  faded/modal price ratio), not just to R5a.
  **CONFIRMED OUT-OF-SAMPLE (v27, 2026-07-27 13:15 UTC — one hour after adoption).** The cron un-froze
  and the **12:30 snapshot caught up to the live book exactly**: `KXHIGHTDAL-26JUL27-T101` **0.555 and
  modal**, B101.5 0.405 — precisely what the 12:16 live tape said and the 08:55 snapshot denied. Live at
  13:21 it is 0.56/0.57, still climbing. **The live book led the snapshot by ~20 minutes and it led it
  correctly**; a symmetric R20 would have had me carrying a false "T101 is non-modal" through that
  window and, applied mechanically, would have handed R5a a stale premise. **What this does and does not
  establish:** it confirms R20(b)'s *reasoning* — the live price is reliable evidence **against** a
  candidate even while it is unreliable **for** one — because the fresher source vindicated the tape.
  It establishes **nothing about PnL**: nothing settled, and I will not grade a rule by a counterfactual
  I cannot run. R20(b) remains a tightening held to a tightening's evidentiary bar.

- **R21 (resolution-integrity veto — NEW in v30, MECHANISM ESTABLISHED in v31; the ground truth itself
  can be wrong, and in three cells it is — for a reason I can now name, test, and predict):**
  Before trusting any quantity derived from `data/resolutions.parquet` — the production track record,
  `model_bias_applied_f`, my own (ii‴) bias measurement — check the station's stored `raw_text` for the
  string **`VALID AS OF <hh>00 AM LOCAL TIME`**. That one-line test is the whole rule.
  **The cause is NOT a parser bug, which is what v30 asserted and got wrong.** The numeric extraction is
  correct; the *document* is the wrong document. **KEWX (Austin, San Antonio) and KBOU (Denver) issue an
  early-morning INTERMEDIATE CLI** — Austin/San Antonio at 746 AM CDT "VALID AS OF 0700 AM LOCAL TIME",
  Denver at 632 AM MDT "VALID AS OF 0600 AM LOCAL TIME" — and `fetch-resolution` captures that instead of
  the end-of-day report. Its `MAXIMUM` field is therefore **the maximum since local midnight**, which on a
  summer morning is the previous evening's carryover, logged in the small hours. JUL27 verbatim:
  Austin `MAXIMUM 80 12:05 AM` (normal 98, the CLI's own DEPARTURE column reads **−18**), San Antonio
  `MAXIMUM 80 12:45 AM` (**−16**), Denver `MAXIMUM 83 116 AM` (**−7**).
  **This explains every previously-unexplained feature of the corruption, which is how I know it is right:**
  *(a)* **why only `high` breaks** — the daily minimum occurs near dawn, *inside* the midnight-to-0600/0700
  window (Austin `MINIMUM 74 5:40 AM`, Denver `76 4:59 AM`, San Antonio `75 5:59 AM`), so the low is a true
  daily low while the max is not; *(b)* **why the error is 11–25°F and always negative** — it is exactly
  (afternoon high − overnight carryover max); *(c)* **why exactly these three cells** — scanning `raw_text`
  across all 20 stations, **KAUS, KSAT and KDEN carry the `VALID AS OF` stamp and the other 17 carry none.
  Zero false positives, zero false negatives.**
  **Consequences:** *(a)* Austin/high (+27.5%), Denver/high (+26.1%) and San Antonio/high (+30.6%) are the
  only strongly-positive cells in the whole 40-cell table and **all three are graded against a broken answer
  key — their record carries no information**, and R1's piggyback premise is void for them. *(b)*
  `compute-bias` is mean(model_expected − actual) against these values, so the +12.5 / +11.0 / +13.4°F
  "ensemble bias" corrections are **manufactured**, and the recorder subtracts them, pushing those ensembles
  ~12°F cold — which is **precisely** why `model_p` reads 0.95 on the bottom bin (AUS/SATX high T97) in
  those cells. That is now a derivation, not a conjecture. *(c)* **Correcting v30's overreach:** v30 claimed
  this "retro-explains the degenerate model columns I have been vetoing under R8/R10 for weeks." It explains
  the AUS/SATX/DEN ones only. **LAX/high (model 0.95 on T83) and Chicago/low (model 0.84 on T64) were
  degenerate on this very board with clean, unstamped resolutions** — so R8/R10 retains independent work and
  a second, still-unidentified degeneracy mechanism exists. R9 stands on its own record.
  **Operationally: Austin/high, San Antonio/high and Denver/high are CLOSED to me** — `model_p` and the
  track record are unusable there, and `nbm_q50` alone cannot satisfy R2's dual-source premise. **The `low`
  cells at these same three stations remain usable** (the min is in-window), with the standing caveat that a
  day whose minimum falls after 07:00 local — a cold-front afternoon collapse, essentially absent in July —
  would break them too.
  **Re-test changed in v31, because the old one could never fire.** v30 said "re-run the market-settlement
  cross-check monthly; reopen when they agree." That is futile: this is a **structural property of which
  product those two offices issue**, so it will not self-heal and the cells would stay closed forever on a
  test that can only ever fail. **The correct reopening test is the stamp**: reopen a cell when its stored
  `raw_text` no longer contains `VALID AS OF … AM LOCAL TIME` (i.e. the fetcher has moved to the end-of-day
  product), then rebuild its record forward from that date and discard the corrupt history.
  **This is a read-only finding.** I may not and did not touch the parser, `resolutions.parquet`, or any
  code. **The operator should know that `weather/nws.py` is fetching KEWX's and KBOU's intermediate morning
  CLI rather than the final one** — flagged in the journal; the fix is theirs to make, not mine.
  *Method caveat retained from v30:* the old cross-check flagged ~35 **open-bin** (`T*`) rows as artifacts of
  its own NaN boundary handling; only closed-bin mismatches ever counted. The `VALID AS OF` test supersedes
  it and has no such artifact. *Kill if: the stamp disappears from these stations' CLI text (then reopen as
  above), or if a stamped station's `high` values are ever shown to match market settlement anyway.*

- **R22 (enumerate the funnel as a QUERY, in BOTH directions — NEW in v32; a procedure rule, and it exists
  because R13′ makes the sorted view systematically misleading):** The candidate set is produced by running
  the funnel **as a query over the newest snapshot**, never by reading the top rows of
  `agent-model-view`'s edge-sorted table. Two passes, both required:
  **(a) NO-fade pass:** `midpoint − model_p ≥ 0.10 AND midpoint − nbm_p ≥ 0.10`.
  **(b) YES-buy pass:** `model_p − midpoint ≥ 0.10 AND nbm_p − midpoint ≥ 0.10`.
  Compute modality (`midpoint = max(midpoint) over event`) and the **R18 ratio** in the same query, so R5a
  and R18 are evaluated on the whole set rather than on whichever rows I happened to read.
  **Why this is a rule and not a note — I caught myself getting it wrong on a board I had already called
  swept.** The 06:20 addendum on `0610.parquet` declared a full re-sweep and reported exactly one high-side
  survivor (MIA B94.5), classifying everything else as a blacked-out low, an R21 cell, or an already-modal
  bin. Re-run as SQL against the identical file, that same board carries **four** qualifying bins that are
  none of those: DAL high B102.5 (YES side, model 0.806 / NBM 0.427 vs mid 0.295), LV high B111.5 JUL28
  (ratio 0.423), PHIL high B81.5 (0.890), OKC high B102.5 (0.961).
  **The mechanism is R13′ pointed at my own procedure.** R13′ establishes that a bin's both-sources-below
  gap is bounded above by the price the market put there, so the largest gaps can only exist where the
  market placed its mass — **the top of an edge-sorted view is structurally the modal bins**, which R5a
  bans universally. Reading the top and stopping therefore samples the funnel *exactly* where candidates
  cannot be. R13′ has been telling me since v17 to "hunt the 2nd/3rd-priced bins"; I wrote that down five
  times and kept reading row 1.
  **The direction half is worse than the truncation half.** `agent-model-view` sorts on **signed** edge, so
  YES-side and NO-side candidates occupy opposite ends of one table and never appear together. **I had not
  enumerated the YES direction in weeks.** R2 has an explicit YES-buy half (2W–7L, −$30.52, one settlement
  from its pre-registered restriction) — a sub-rule with a losing record that I never screen for cannot
  reach its own kill clause, and its absence from my journals was reading as "the shape does not occur."
  **R16 self-check, applied before adoption:** R22 is a procedure, not a gate; it references nothing
  specific to any candidate; it moves in the **loosening** direction (more candidates, not fewer), which is
  the direction I hold to the *higher* evidentiary bar — so note that all four bins it surfaced on adoption
  day were refused on rules that already existed (R5(b), (ii‴), BRACKET, R18), and the session ended in
  **zero trades**. A supply-increasing rule that produced no trade is not one I built to let myself trade.
  *Kill if: over ≥5 boards the two-direction query surfaces nothing the sorted-view read did not already
  contain — then the truncation was costing me nothing and R22 is ceremony.*

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

- **R17's correlation classes may need a CONSECUTIVE-DAY clause for the same city+bin+direction
  (added 2026-07-27 16:15 UTC — parked deliberately, NOT adopted).** R17 refuses a second AGREEMENT
  fade when four clauses hold, one of which is **(b) same settlement date**. Today I came within one
  live-price check of opening **`KXHIGHTLV-26JUL28-B111.5` NO** while already holding
  **`KXHIGHTLV-26JUL27-B111.5` NO** — same city, same bin, same direction, one day apart, under one
  persistent desert ridge — and **R17 does not catch it**, because clause (b) fails. R17's stated
  mechanism ("one identifiable meteorological event costs me twice") arguably applies with *more* force
  across adjacent days of a stable ridge than across two cities on one board, which is the case it was
  written for. **Why this is a hypothesis and not a rule: I did not need it.** R14 refused the trade on
  its own (live bid 0.15 ⇒ NO entry 0.85, edge 0.12 < 0.15, 26-lot book), and adopting a gate I did not
  need, in the same hour I adopted another one, is exactly the churn pattern below. **Pre-registered
  remedy so a future session does not improvise one under pressure:** if this recurs, extend R17 with a
  **size cap**, not a refusal — R17's own remedy language — sized so the joint-loss outcome leaves the
  AGREEMENT subset clear of its −$40 kill line. Worked example from today: subset at +$0.36, LV JUL27
  risking $21.45 ⇒ the second position must risk < **$18.91**, i.e. ≤ 24 lots at a 0.78 entry.
  *Confirm if: a same-city consecutive-day pair is ever open simultaneously and both settle the same way
  on one shared forecast bust. Refute if: such pairs split, i.e. day-to-day errors decorrelate.*
- **My rule-change rate is decoupled from my evidence rate, and that is a hazard (added
  2026-07-27 15:15 UTC, no version bump — this is a hypothesis, not a rule).** In the six
  hours v23→v28 I bumped the playbook **five times** while settling **zero** trades. Every
  one of those bumps was justified by reasoning or by a measurement, never by an outcome.
  Editing rule 3 kills a rule after ≥10 settled trades underwater — a test that a rule
  written and rewritten hourly on an empty book can never reach. The suspicion: an hourly
  cadence with nothing settling creates pressure to produce *a* deliverable, and a rule
  edit is the cheapest one available. *What would confirm it:* a rule adopted in this
  stretch getting falsified by the first settlements that touch it, or two consecutive
  rules contradicting each other (v27's R20(b) already amended R20 one hour after R20 was
  adopted). *What would refute it:* the v23–v28 rules surviving contact with ≥10 settled
  trades. *Provisional discipline, not yet binding:* bump the version only when an active
  rule actually changes, and prefer parking a new idea here over promoting it. Today I
  followed it — R12‴'s scheduling estimate missed and I left the version alone (see the
  15:15 journal entry).
  **v29 UPDATE — the count is now SIX bumps in seven hours on zero settled trades, and I am
  drawing the distinction the hypothesis needs rather than just incrementing it.** Every one of
  the previous five was grounded in *reasoning about my own process* or in a measurement of my
  own data pipeline (cron cadence, board listing times, snapshot-vs-live asymmetry). **(ii″) is
  the first grounded in a VERIFIED FORECAST MISS** — NBM q50 78.53 against a realized 71–72°F in
  a cell whose next-day forecast is unchanged. That is an outcome external to me, which is the
  category of evidence editing rule 2 actually asks for, and it is the closest thing to a
  settlement I can get while my book is empty. **I also declined a second, separately plausible
  edit this same hour** (the R17 consecutive-day clause, parked above) precisely because R14 had
  already made it unnecessary. *Sharpened test:* if the outcome-grounded edits survive contact
  with settlements while the process-grounded ones get retracted, the hazard is real and the fix
  is a source-of-evidence gate on edits, not a rate limit.
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

- **v32** (2026-07-28, 08:15 UTC): **Nothing settled (`settled=0 still_open=1`) and the snapshot was
  byte-identical to the one I had already swept — an R20 fast-path hour by the book. It was not, because the
  "full sweep" it was byte-identical to turned out to be wrong. ONE new rule (R22), one tripwire counting
  convention, one correction to how I read R19′. ZERO trades.**
  *R22 — enumerate the funnel as a query, in both directions.* Re-running the 06:20 addendum's "full
  re-sweep" of `0610.parquet` as SQL against the identical file surfaced **four** qualifying bins the prose
  enumeration had classified away as "blacked-out low / R21 / already modal": **DAL high B102.5** (YES side,
  model 0.806 / NBM 0.427 vs mid 0.295), **LV high B111.5 JUL28** (R18 ratio 0.423), **PHIL high B81.5**
  (0.890), **OKC high B102.5** (0.961). Mechanism is **R13′ turned on my own procedure**: a both-sources-below
  gap is bounded by the price the market put there, so the top of an edge-sorted view is structurally the
  modal bins that R5a bans — reading the top samples the funnel exactly where candidates cannot be. Worse,
  `agent-model-view` sorts on *signed* edge, so **I had not enumerated the YES direction in weeks**; R2's
  YES-buy half (2W–7L, one settlement from its pre-registered restriction) cannot reach its own kill clause
  if I never screen for it. R16 self-check: procedure not gate, loosening direction, and **all four
  candidates were refused on pre-existing rules** — adoption day ended in zero trades.
  *All four refusals, on rules that already existed.* **DAL B102.5 → R5(b)**, the DAL T101 shape verbatim:
  across nine cycles B100.5 climbed 0.285 → **0.545** while B102.5 slid 0.445 → **0.295**, so the apparent
  edge grew 0.27 → 0.51 with roughly half of that growth being pure adverse price movement, and NBM's q50
  drifted cooler (102.50 → 102.35) *following the market*. **LV B111.5 → (ii‴)** re-confirmed on a fresh
  cycle: LV/high NBM cold **5 of 5**, mean **−2.33°F**, q50 108.56 + 2.33 = **110.89**, inside the faded
  bin's [110.5, 112.5) support, with JUL26 having realized **111**. **PHIL B81.5 → BRACKET *and* (ii‴)**:
  model's mode T84 (≥85°F) and NBM's mode T77 (≤76°F) reject the bin from opposite sides 8°F apart — the SFO
  B61.5 shape — and PHIL/high NBM runs −2.20°F cold 5/5. **OKC B102.5 → BRACKET + R18 at ratio 0.961**, worse
  than the 0.948 R18 was written to refuse; (ii‴) correctly does *not* fire there (mean +0.12, signs mixed).
  *Tripwire counting convention.* (ii‴) fired on 3 of 4 candidates and v31 had flagged that ratio as
  near-narrowing — but MIA is independently killed by (ii′) and PHIL is independently a BRACKET, so **(ii‴)
  is the sole blocker on 1 of 4**. Adopted for every anti-learning-blocker tripwire: **count sole-blocker
  firings, not firings** — a co-firing veto cannot be eating the funnel. Generalizes how R5(b)'s log was
  always kept. (ii‴) sole-blocker count: **1**.
  *Correction.* Four consecutive sessions quoted "R19′'s 60–110 min overnight baseline"; **that is the
  11:00–23:45 row.** Overnight is 3h20m–4h05m (01–05 UTC) and 2h10m–3h35m (05–10 UTC), so the 06:15
  session's staleness disclosure was owed under a misread and today's 121-min snapshot is *fresher* than
  its baseline. No refusal rested on it, but a premise carrying rhetorical weight should be right.
  *Trades:* none. Holding 1 (LV JUL27 B111.5 NO — market closed 08:00 UTC, `result` empty, unsettled).

- **v31** (2026-07-28, 04:15 UTC): **Nothing settled (`settled=0 still_open=1`), but new GROUND TRUTH
  arrived and it overturned a mechanism I asserted one session ago. ONE rule amended (R21), ZERO new
  rules, ZERO trades.**
  *R21 mechanism established, v30's diagnosis retracted.* JUL27's CLI posted for exactly the three R21
  stations (KAUS/KSAT/KDEN) — AUS high **80**, SATX high **80**, DEN high **83** vs normals 98/96/90.
  v30 called this "a parser signature, not weather." **Wrong.** The parser reads correctly; the captured
  *document* is an **intermediate morning CLI** stamped `VALID AS OF 0700 AM LOCAL TIME` (Denver 0600),
  so `MAXIMUM` is the midnight→dawn carryover max (`80 12:05 AM`, `80 12:45 AM`, `83 1:16 AM`), not the
  daily high. Evidence: three predictions of the mechanism all confirmed — only `high` breaks because the
  min *is* in-window (`74 5:40 AM` etc.); the error equals (afternoon high − overnight max) = the observed
  11–25°F; and scanning `raw_text` across **all 20 stations, exactly KAUS/KSAT/KDEN carry the stamp, the
  other 17 carry none — zero false positives, zero false negatives.**
  *Operational change:* v30's reopening test ("re-run the market-settlement cross-check monthly, reopen
  when they agree") **could never fire** — the cause is structural, so those cells would stay closed
  forever on an unclearable criterion. Replaced with the **`VALID AS OF` stamp test**, which can. Also
  narrowed v30's claim that this "retro-explains the degenerate model columns": it explains AUS/SATX/DEN
  (derivable via the +12°F phantom `compute-bias` correction) but **not LAX/high or Chicago/low, both
  degenerate on this board at unstamped stations** — R8/R10 keeps independent work.
  *A rule I measured, drafted, and deliberately did NOT adopt.* NBM signed error over JUL22–26, 183 pairs,
  all valid cells: **highs −0.73°F cold (70% of days), lows +1.40°F warm (27% cold)** — NBM under-forecasts
  the diurnal range, with the low-side bias ~2× the high-side and far more consistent (16/20 low cells
  warm). The obvious R22 ("raise R2's live bar to 0.20 for fades of low bins below the forecast") would
  have changed **zero** decisions this board — (ii‴) already killed all of them — so on one 5-day
  single-regime sample it was churn, not a rule. Recorded as **evidence for (ii‴)** instead: it defuses
  (ii‴)'s own "eating the funnel" kill-clause, which mattered because (ii‴) fired on **3 of 4** non-modal
  survivors today (vs 2 of 6 in v30). Widespread real bias ⇒ widespread firing is correct behaviour, not
  miscalibration. Threshold left alone; ratio re-checked next session.
  *Trades:* none. Four non-modal AGREEMENT candidates adjudicated and all four refused — LAX high B80.5
  (R8/R10 + (ii‴)), MIA high B94.5 ((ii‴): cell −3.72°F cold 5/5, and JUL26 realized **94, inside the
  bin**, vs NBM 86.11), OKC low B71.5 ((ii‴) +2.63°F warm 5/5, after clearing R2's live bar by **one
  cent**), CHI low B66.5 (R8/R10 + (ii‴) + 8¢ spread). Every largest gap on the board was modal → R5a,
  R13′'s fifth consecutive confirmation.

- **v30** (2026-07-27, 19:15 UTC): **Nothing settled (`settled=0 still_open=1`). Fresh 1855 snapshot
  (18:57 UTC), full 36-event JUL28 re-sweep, ZERO trades, TWO new rules — both tightenings, and the
  larger one is a data-integrity finding that reaches backwards through the whole playbook.**
  *R21:* chasing an implausible NBM bias table (Denver/high +17.6°F, San Antonio/high +15.8°F,
  Austin/high +15.4°F) I cross-checked `data/resolutions.parquet` against **the market's own
  settlement** — for every settled event since JUL23, does the CLI value fall inside the bin the market
  settled at ≥0.90? **Every closed-bin settlement across 17 cities agrees except three cells, which fail
  every single day by 11–25°F: Austin/high, San Antonio/high, Denver/high** (e.g. Denver JUL26, market
  settled 102–104°F, CLI says 79). The `low` cells at those same stations parse correctly on the same
  days — a parser signature, not weather. **Those three cells are the ONLY strongly-positive cells in the
  40-cell track record (+27.5% / +30.6% / +26.1%), so their ROI is an artifact of grading against a broken
  answer key**, `compute-bias` inherits the corruption (the +11 to +13°F "ensemble bias" corrections are
  manufactured from it), and it retro-explains the degenerate model columns I have vetoed under R8/R10 and
  R9 for weeks — **those rules were right for a mechanism I could not see.** All three cells are now closed
  to me; re-test monthly. Read-only finding: no code, no `resolutions.parquet`, operator notified via
  journal. Method caveat recorded — the ~35 open-bin (`T*`) flags are my test's NaN-boundary artifact,
  only closed-bin mismatches are real.
  *(ii‴):* `KXHIGHTLV-26JUL28-B111.5` NO — chased for three sessions — **finally cleared every gate**,
  including the live bar that had killed it twice (bid **0.24**, spread 0.01, vol24h 111, edge **0.212**;
  R5a 2nd-priced under B109.5 @0.605, (i″) d_nbm 2, (iii′) both ≤0.05 entry 0.76, R18 ratio 0.405, (ii′)
  bias −1.82, R15′ reconstruction 0.010). **(ii″) passed it by 0.14°F** (JUL26: realized 111 — *inside the
  faded bin* — vs NBM q50 108.09 and model mode B109.5, larger error 2.86 against a 3.0 bar). So I measured
  the cell over five days instead of one: **NBM cold 5 of 5, mean −2.33°F**, model mode cold 5 of 6, and
  108.65 + 2.33 = **110.98** — the displacement points straight into the bin I wanted to sell. (ii‴)
  replaces the one-day trigger with a 5-day mean (|mean| ≥ 1.5°F, sign consistent ≥4/5) **plus a direction
  clause** (the correction must move the estimate toward the faded bin) — the clause (ii″) lacked, since a
  cold bias only endangers fades of bins *above* the forecast. Fired on **2 of 6** R5a survivors, one of
  them being (ii″)'s own OKC/low founding case reached independently. n=0 settled ⇒ zero demonstrated
  discriminating power, stated as such.
  *R13′ confirmed a fourth time, most cleanly yet:* of 17 dual-source qualifiers, 11 are the market's modal
  bin and **all ten of the ten largest gaps are modal** → R5a. Other refusals: PHIL high B79.5 dies three
  times (R18 ratio **0.964**, R8/R10 artifact column, R5a-by-a-cent); MIA high B94.5 → (ii′); MIA low B75.5
  and LAX low T69 → R2's live bar (0.124 and 0.101). Holding 1: LV **JUL27** B111.5 NO @0.70, live 0.17/0.18
  ⇒ mark **+$3.75**, best since entry — recorded with the explicit note that the twin going my way is *not*
  evidence for the JUL28 fade.
- **v29** (2026-07-27, 16:15 UTC): **Nothing settled (`settled=0 still_open=1`). The first next-day
  board I have ever swept with actual source coverage — 36 JUL28 events, model_p + nbm_p on every bin,
  NBM cycle 06:00 UTC — fully adjudicated, ZERO trades, ONE amendment.** *Evidence for (ii″):* the
  board's best candidate, `KXLOWTOKC-26JUL28-B73.5` (2nd-priced bin, snapshot mid 0.30), cleared **every
  gate I own** — R5a (mode is B75.5 @0.355), (i″) (d_model = 2), (ii′) (`model_bias_applied_f` +4.96°F),
  (iii′) (both sources at the Laplace floor, NO entry 0.75), R14 live (bid 0.25, spread 0.07, vol24h 175),
  R15′ (lower-tail reconstruction P = 0.0022, so NBM's 0.005 is a genuine vote), R8/R10, R9, R17. Then the
  cross-day check: **on JUL27 in this same cell NBM said q50 = 78.53 and the model's mode was 73–74°F,
  and the minimum realized at 71–72°F** (market has B71.5 at 0.98/1.00 with the low long since formed) —
  **NBM +6.8°F warm, model ≈+2°F warm, same direction** — and the JUL28 cycle repeats q50 = **78.88**.
  So (ii′)'s model-only bias column waved through a cell whose two "independent" sources had just busted
  together. **(ii″) adds the missing veto:** disqualify AGREEMENT fades where both sources fell on the
  same side of the previous settled day's realization with the larger error ≥3°F and the cycle unmoved.
  Caveats recorded in the rule: JUL27's CLI has not posted (market price used as a labeled proxy), R12″
  already saw this bust intraday so only the cross-day *scope* is new, and n=0 settled ⇒ zero demonstrated
  discriminating power. Fired on **1 of 36** events. *Other refusals, each with a number:* **PHIL low T72**
  and **LV high JUL28 B111.5** both cleared the full source/geometry funnel — LV with an R18 ratio of
  **0.381**, squarely inside the 0.33–0.76 support — and **both died on R14**, bid 0.18→0.05 and 0.22→0.15
  between a 50-minute-old snapshot and the live book (NO entries 0.95 and 0.85; live edges 0.04 and 0.12
  against R2's 0.15 bar). **MIN low T72** → (iii′) at the live mid + R18 ratio 0.918. **AUS high B99.5**
  → R5a + (ii′) (bias **+12.26°F**) + R8/R10 (model degenerate). **LAX high B80.5** → R8/R10 (model 0.954
  on a bin priced 0.025). Six more modal bins → R5a; Denver → R9. **Standing finding: R14, not the source
  gates, is what actually binds this playbook** — and it binds on long-lead boards too, which I had
  assumed decayed more slowly. *Parked, not adopted:* an R17 consecutive-day clause (I nearly opened the
  identical LV B111.5 bin one day after the one I hold; R17 clause (b) does not catch it), with a
  pre-registered size-cap remedy of ≤24 lots. *No version bump was spent on it because R14 refused the
  trade anyway.* Churn hypothesis updated: 6 bumps / 7 hours / 0 settlements, but this is the first one
  driven by an **outcome external to my own process**, and that distinction is now the hypothesis's test.
- **v28** (2026-07-27, 14:15 UTC): **Nothing settled (`settled=0 still_open=1`); no trade was
  mechanically possible on either board; the session's value is a RETRACTION and two rules.**
  **RETRACTION — the "frozen cron" does not exist, and I asserted it in three consecutive headers.**
  First measurement of the recorder's actual cadence (07-22→07-27): nominal 96/day, **delivered 12–15/day
  (~1 run in 7)**, in a stable diurnal shape — 3h20m–4h05m gap after ~01:00 UTC, 2h10m–3h35m through the
  morning, 60–110 min from ~11:00 UTC onward. **Every "freeze" I flagged sits inside that distribution**;
  the v25 call flagged an **80-minute-old** snapshot against a 2h10m–2h50m baseline, and v27's "the cron
  UN-FROZE" describes the ordinary late-morning cycle that lands ~12:00–12:45 every day. Honest
  counter-evidence: today IS slow — its gaps (4h05m/3h30m/3h35m) are at or above the top of each window's
  range and it has 4 files by 14:19 vs a ~6–7 median — so *"slow end of normal"* is right and *"frozen"*
  never was. **No refusal is revisited** (DAL T101 rests on R5(b)/R20/R13′), and the NBM half of R19 is
  untouched: `nbm_cycle_utc` is a recorded field and those 16–18h ages were real. **→ NEW R19′:** judge
  model staleness against the measured per-window baseline, disclose only above it, and say
  "N min old against an X-hour normal for this hour" instead of "frozen."
  **NEW R12‴ — the sweep predicate is SOURCE COVERAGE, not board listing.** First session to land inside
  R12's 14:00–15:10 window with the next-day board actually live (`KXHIGHAUS-26JUL28`, six-bin book, 40h
  to close) — **and zero coverage of it**: `agent-model-view --min-lead-hours 20` returns
  `_none at this threshold_`, no `model_p`/`nbm_p` on any JUL28 bin, because the newest snapshot (1230)
  predates the listing. R1/R2 both require sources; with none, the live book is the only input and
  screening on it is R20's failure mode in pure form. A listed-but-uncovered board is **not sweepable**,
  and the pressure peaks precisely because this is the *good* 40h board (R16's shape with a clock on it).
  **Scheduling half:** first covering snapshot landed 14:20 / 14:30 / 15:00 / 14:00 / 14:10 across five
  days — **my 14:15 session loses that race 4 days in 5; 15:15 has coverage 5 of 5.** v17's "git pull
  again in a few minutes" assumed the nominal cron; the real wait is 5–45 min. So: check coverage once at
  14:15, else fast path, and treat **15:15 as the first real sweep** of the next-day board.
  **Zero trades, provably rather than by judgment.** JUL28 → no coverage (R12‴). JUL27 → the snapshot is
  byte-identical to the one v27 fully adjudicated, and **R20 evaluates qualification at the snapshot
  mid**, so the qualifying set equals last session's (empty) while R20(b) lets live prices only *add*
  vetoes — the candidate set is a subset of an empty set. **First time a rule of mine has established in
  advance that an hour of sweeping would be wasted.** Scope also shrank: at 14:16 UTC every Eastern and
  Central high is past R12′'s ~09:00 local predicate, and all 20 lows sit in R12″'s blackout.
  **Position:** LV B111.5 NO @0.70 (30 lots) marks **−$0.75** at a live 0.32/0.33 — fifth straight adverse
  tick, now underwater; guidance repricing (07:16 PDT, 18h to close), not R12″ observation. R5(b) forbids
  adding; holding.
- **v27** (2026-07-27, 13:15 UTC): **Nothing settled (`settled=0 still_open=1`), but the cron UN-FROZE
  and NBM rolled to the 00Z cycle — the first fully-fresh full sweep in five sessions (snapshot
  `1230.parquet`, 43 min old; `nbm_cycle_utc` 2026-07-27 00:00 at 21–24h lead). One rule amendment, one
  out-of-sample confirmation, one retro-flag resolved, ZERO trades.**
  **NEW R13′ — the edge/mode coupling is LEAD-INDEPENDENT; R13's "≥24h" scoping and its
  "wide/flat long-lead board" mechanism are both wrong.** R13's mechanism predicts the coupling weakens
  at short lead. Measured on today's **6–7h** board (16 high events): of 16 bins clearing R2's
  both-sources-≥0.10-below bar, **12 (75%) are the market's modal bin** and **the seven largest gaps are
  all modal** (AUS B98.5 0.626, DAL T101 0.546, SATX B96.5 0.511, NYC B83.5 0.439, PHIL B87.5 0.398,
  DEN B93.5 0.356, LV B109.5 0.354) — versus R13's founding long-lead "five largest." The real
  mechanism is a bound, not a lead effect: **a bin's both-sources-below gap cannot exceed the price the
  market put there**, so the biggest gaps live where the market placed its mass, at every lead.
  Operationally: hunt 2nd/3rd-priced bins on *every* board, and never treat a short-lead board's huge
  edge as more trustworthy — at short lead the market also holds observations I cannot see (R12″).
  Accepted on one board because it is a **tightening**; kill clause mirrors R13's, run on <12h boards.
  **R20(b) CONFIRMED out-of-sample one hour after I shipped it labeled "untested."** The 12:30 snapshot
  caught up to the 12:16 live book exactly — `KXHIGHTDAL-26JUL27-T101` **0.555, now modal**, B101.5
  0.405 (the 08:55 snapshot had B101.5 @0.480 modal, T101 @0.355); live 13:21 0.56/0.57. **The tape led
  the snapshot by ~20 min and led it correctly**, so the veto R20(b) preserved was the right one.
  Confirms the *reasoning*, not PnL — nothing settled.
  **R15′ retro-flag on the open LV B111.5 NO RESOLVED in the position's favor.** Reconstructing NBM
  from the fresh 00Z quantiles (q10 105.68 / q25 106.62 / q50 107.20 / q75 108.54 / q90 109.47) gives
  B111.5 ≈ **0.000** piecewise-linear, ≈ **0.030** Gaussian — both ≤0.05, so NBM clears (iii′)'s
  emptiness test on its own quantiles and the Laplace floor was sitting on a genuine near-zero. Flag
  lifted. Same reconstruction re-confirms R15″ (recorded `nbm_p` understates: B107.5 0.403 → **0.511**,
  B109.5 0.173 → **0.258**).
  **R19 evidence, reassuring direction:** the fresh sources **reproduced every refusal** made on the
  stale ones — PHIL B85.5 and DC B87.5 still BRACKET, DEN still bias **+13.39** with a degenerate model
  column (0.954 on T93, floor on the other five), every large gap still modal. Argues for keeping R19 a
  disclosure rule rather than promoting it to a veto.
  **Sweep:** R12′ authorized all 16 high events (every city local-time before ~09:00, no high formed);
  **R12″ removed all 20 low events wholesale** (08:50 EDT / 07:50 CDT / 06:50 MDT / 05:50 PDT — all
  inside the local-midnight-to-10:00 blackout). All 16 dual-source candidates refused, each on ≥2
  independent grounds: 12 by **R5a** (modal), DEN B95.5 by **R9** + degeneracy, LV B111.5 = my own open
  position, **DC B87.5** by **(iii′)** (mid 0.295 < 0.30, NBM 0.071 > 0.05) + BRACKET, **PHIL B85.5** by
  **R2's ≥0.15 live-edge bar** (NBM gap at `yes_bid` 0.31 is only 0.10) + BRACKET (0W–1L, −$28.59).
  **R12's kill clause tested and not triggered: this pre-14:00 sweep produced no trade clearing all
  governing bars, so R12/R12′ stand.** No trade; holding 1; LV mark **+$1.05** (adverse tick).

- **v26** (2026-07-27, 12:15 UTC): **Nothing settled (`settled=0 still_open=1`), cron frozen a fourth
  consecutive session (newest cycle still `0855.parquet`, 3h20m old), so the modeled sources are
  byte-identical to the sweep v24 fully adjudicated and no re-sweep was run. One amendment, sourced
  entirely from the live tape, ZERO trades.** **NEW R20(b): R20 is ASYMMETRIC — qualification
  requires the snapshot mid, but vetoes may fire on EITHER the snapshot mid or the live book. Price
  movement can never create an entry; it can always kill one.** The gap was found by a fact the tape
  produced two hours after R20 shipped: **`KXHIGHTDAL-26JUL27-T101` is now the market's modal bin and
  was not at the snapshot.** Live at 12:16 — T101 **0.555**, B101.5 0.405, B103.5 0.04, rest ≤0.02;
  at the 08:55 snapshot — B101.5 **0.480** modal, T101 0.355. The market's **mode flipped bins**. Read
  symmetrically, R20 would send **R5a's universal modal-fade ban** to the snapshot mid, see a
  non-modal bin, and *remove* a protection the live book is offering — i.e. a mechanical reading of my
  newest rule would loosen me. R20(b) resolves it in the only direction consistent with R20's own
  reasoning (the price is untrustworthy *for* me, fine *against* me), and applies to every veto I own,
  not just R5a. **Honest labeling: R20(b) is untested and was NOT load-bearing today** — DAL T101 is
  refused for the **sixth** straight session under R5(b) + R20 + R19 regardless — which is precisely
  why it was worth writing now rather than in a session where a candidate I want turns on it (the R16
  failure mode, run pre-emptively). **The tape, and it is emphatic:** T101 went 0.420 (Jul26 14:10) →
  **0.215** → 0.210 → 0.245 → 0.375 → 0.385 → 0.455 → **0.355** (08:55 snapshot) → 0.400 (10:16) →
  0.515 (11:15) → **0.555** (12:16) — **+0.34 off the low, +0.20 since my sources last updated**, all
  away from both of them; the gap vs R15″-corrected NBM (0.264) has run **0.091 → 0.136 → 0.251 →
  0.291** on **zero** new forecast information (`nbm_cycle_utc` still 2026-07-26 18:00, now 18h stale).
  **Second-order finding, and it vindicates v25's retraction:** at 08:15 I called the 0.455 → 0.355
  slide "the live tape confirming R5(b) directionally"; I retracted it at 10:15 when it bounced to
  0.400; it has now run to 0.555, decisively the other way. Intraday marks are not evidence, and I
  have been wrong-then-right about that inside four hours. **A read that makes the refusal stronger,
  not weaker:** it is 07:15 CDT in Dallas on settlement day and this is the venue's deepest weather
  book (vol24h 3427 / OI 1979) — the +0.20 is the market pricing morning obs and 12Z guidance that an
  18h-stale NBM cycle and a frozen 08:55 snapshot cannot see. My sources are not merely stale, they
  are being outvoted by information (R19's whole point). **No other candidate was reconsidered** —
  v24's adjudication of the identical sources stands, and R12″ blackouts the entire low half (07:15
  CDT / 08:15 EDT). **No trade opened.** Holding 1; LV B111.5 NO @0.70 marks **+$1.35** (yes 0.23/0.25
  ⇒ NO 0.76), one favorable tick after four adverse.

- **v25** (2026-07-27, 10:15 UTC): **Nothing settled (`settled=0 still_open=1`), so no grading step.
  The snapshot cron re-froze — newest cycle is still `0855.parquet`, the one v24 fully adjudicated —
  so the model and NBM columns are byte-identical to last hour and a re-sweep of the sources would
  have been theatre. One rule change, sourced entirely from the live tape, and ZERO trades.**
  **NEW R20: R2's "both sources ≥0.10 below the mid" bar is evaluated at the SNAPSHOT mid, never the
  live mid.** The defect is an interaction between two rules I trust individually. R14 (v18) says
  screen the **live** book, because snapshot mids on thin books manufacture edge — true, and it
  stands. But I had been letting the live price do two jobs at once: set the entry price *and* decide
  whether a candidate qualifies. **The sources are frozen at the snapshot cycle; the price is not**,
  so a candidate that fails R2 at the snapshot mid and passes at the live mid has been qualified by
  market movement alone, in the direction away from my sources — R5(b)'s definition of a trade to
  refuse. R20 splits the jobs: live book for entry price and book quality, snapshot mid for
  qualification. **Founding case, verifiable to the cent:** `KXHIGHTDAL-26JUL27-T101` failed R2 at
  09:15 (snapshot mid **0.355** − R15″-corrected NBM **0.264** = **0.091**) and **passes at the 10:16
  live mid 0.400** (gap **0.136**), with the same 0855 snapshot and the same `nbm_cycle_utc`
  **2026-07-26 18:00** (16h stale, `nbm_lead_hours` 28 — R19's disclosure firing on my own candidate).
  **No new forecast information existed. The market moved 0.045 against my sources and live-mid
  screening reads that as 0.045 more edge.** Stated honestly: R20 is a **formalization of R5(b), not
  a new empirical finding** — I have zero settlements separating live-mid-only qualifiers from
  snapshot qualifiers, and claiming otherwise would repeat the **(i)** overreach v18 retracted. It is
  a tightening, it fires on every frozen-cron session (three of my last five), and R5(b)'s founding
  evidence is the JUL-13 DEN/AUS/SATX overnight-collapse triple loss — three trades entered into
  exactly this discount. *Kill clause: log every R20-only refusal and check its settlement; ≥5 wins
  among them means R20 is backwards and R5(b) itself needs re-examining.* R20-only refusals: **1**.
  **RETRACTION of my own 08:15 evidence claim.** At 08:15 I recorded DAL T101's 0.455 → 0.355 slide as
  "the live tape confirming R5(b) directionally." At 10:16 it is **0.400** — nearly half given back in
  two hours, and the full tape (0.420 → 0.210 → 0.245 → 0.385 → 0.455 → 0.355 → 0.400) is a **0.35–0.46
  chop**, not a retracement toward my sources. **One cycle of price movement is not confirmation of a
  rule.** I am flagging this as the same species of error as v17's "(i) OUT-OF-SAMPLE CONFIRMED" that
  v18 had to retract, caught two sessions earlier this time. No rule rested on the claim; R5(b) stands
  on its settlements, not on this week's ticks.
  **Full adjudication, all 9 candidates (same funnel as v24, re-checked against live prices and the
  clock):** the **entire low half of the board is blocked wholesale by R12″** — at 10:15 UTC it is
  05:15 CDT / 06:15 EDT, inside the local-midnight-to-10:00 blackout where the overnight minimum is
  already on the thermometer, so **HOU low B76.5, OKC low T71, MIA low B74.5** are unscreenable by
  construction and their apparent edges measure my staleness (this is R12″'s first *routine* firing —
  it was written yesterday off the OKC near-disaster and today it does quiet mechanical work, which is
  what a good rule looks like). Highs: **DAL T101 → R20 + R5(b)**, fourth consecutive refusal, and the
  first R20 firing; **MIA high B93.5 → (ii′)**, disqualified cell, seventh refusal of the bin that
  settled −$23.77; **DEN high B93.5 → R9**, bias **+13.39°F** with the model at the 0.0093 Laplace
  floor; **PHIL high B85.5 and DC high B87.5 → BRACKET**, R2's 0W–1L subset and the SFO B61.5 shape
  that lost −$28.59 (both also rest on the 18Z NBM's coherent ~5–7°F regional cool displacement that
  R19 flagged, so their "second source" is one stale vote shared between them); **LV high B111.5 →
  my own open position**, duplicate guard. **Nine candidates, six distinct blockers, no single gate
  starving the funnel.** **No trade opened.** Holding 1. **Position mark:** LV B111.5 NO @0.70 quotes
  0.24 / 0.25 yes ⇒ NO worth 0.75, **+$1.05** — three sessions of mild adverse drift (+$3.90 → +$1.50
  → +$1.05). Marks are not evidence; the settle is, and per v22 it must be graded as a trade whose
  NBM leg R15′ retro-flags as an artifact (frac>0.05 = 0.88).

- **v24** (2026-07-27, 09:15 UTC): **Nothing settled (`settled=0 still_open=1`), so no grading step.
  Three rule changes, all sourced from the first fresh modeled cycle in four sessions, and the
  session still ends in ZERO trades.** The 08:55 funnel ran 216 bins → **9** clearing non-modal +
  both-sources-≥0.10-below + mid ≥0.15 → **3** past the cell/geometry vetoes → **0** tradeable.
  Refusals in full: MIA high B93.5 by **(ii′)** (Miami/high disqualified outright, and it is the
  same ticker as the subset's only loss); DEN high B93.5 by **R9** (bias **+13.39°F**, model at the
  Laplace floor); MIA low B74.5 by **(iii′)** (mid 0.27 < 0.30 but model 0.139 ≫ 0.05); HOU low
  B76.5 on R2's ≥0.15 bar (NBM only 0.106 below) and R18 ratio 0.817; DAL high T101 by the new
  R15″(b); LV high B111.5 is my own open position. **(1) R15′ → R15″.** Applied literally, R15′
  vetoed PHIL B85.5, DC B87.5 *and* DAL T101 — but their binned `nbm_p` are 0.068–0.130,
  0.051–0.203 and 0.244–0.303, nowhere near the floor, and their reconstructions **confirm** the
  binned column (DAL's is *lower* than it, so the understatement has the wrong sign). At
  `nbm_p` ≥ 0.05 the 0.05 bar is met by construction, so R15′ was degenerating into a ban on every
  candidate whose second source has a real opinion. R15″ scopes the artifact check to binned
  `nbm_p` < 0.05 and otherwise reads NBM's vote as max(binned, median recon) against R2's own ≥0.10
  test. **Validated first: it changes no settled outcome** (every AGREEMENT trade in the ledger has
  binned `nbm_p` < 0.05, so clause (a) governs all of them), **preserves the DC T70 founding veto**
  (binned 0.0056, 100% of cycles), and **re-refuses DAL T101 mechanically** — NBM 0.264 vs mid
  0.355 is 0.091, under R2's 0.10 gate, which is a better ground than v23's R5(b) route.
  **(2) New R12″ — the tightening, and it cost me the board's second-biggest edge.** R12′'s
  "extreme not yet in progress" predicate was written for **highs only** (~09:00 local); a daily
  **minimum** is largely realized between local midnight and sunrise, which is exactly when my
  hourly sessions run. `KXLOWTOKC-26JUL27-T71` passed **every gate I own** — mid 0.42 vs model
  0.0093 / NBM 0.005, 1,687-lot book, non-modal, d_model 3 / d_nbm 4, both columns non-degenerate,
  R18 ratio 0.778, no R17 conflict — and then the tape showed the market moving **0.96 of its mass
  onto ≤72°F in a single cycle** (B73.5 0.335 → 0.005, B75.5 0.375 → 0.005) on ~4× volume, confirmed
  live at 09:21 as 0.00/0.01 across all four warmer bins. Both my sources said 75–78°F (NBM q10
  **77.08**, reconstruction **0.0000 on all 12 cycles**). The market was reading a thermometer at
  03:55 CDT and I was reading a forecast. Low bins are now unscreenable from local midnight to
  ~10:00. **(3) New R19 — source-independence requires source-freshness.** First check of the
  vintages: every city on the 08:55 cycle carries `nbm_cycle_utc = 07-26 18:00`, `nbm_lead_hours`
  **27–30** against `model_lead_hours` **8–11** — NBM is a ~15h-stale day-1 forecast, and it shows
  as a coherent ~5–7°F **regional** cool displacement across PHIL/DC/NYC rather than independent
  disagreements. That is the MIA B93.5 shared-bias lesson generalized from one cell to one cycle.
  Kept deliberately weak (disclosure + explore-size cap when NBM is the sole non-degenerate source)
  because I have **zero settlements** pricing it, and a gate built from one board's optics is the
  **(i)** mistake R16 exists to prevent. **R16 self-check on the whole session:** one loosening and
  one tightening adopted together, the loosening's own beneficiaries (PHIL B85.5, DC B87.5) then
  **refused** as BRACKET shapes — model and NBM modes straddling the faded bin from opposite sides
  at ~7°F separation, the SFO B61.5 shape (0W–1L, −$28.59) at nearly double the width — and the
  session closes with no trade. A ruleset edited toward trading would not have ended here.

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
