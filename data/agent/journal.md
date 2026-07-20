# Agent trading journal

Dated reasoning log from the `/self-trader` agent — one section per session, newest
first. Each entry records: settlements reviewed, what they said about the current
strategy version, any strategy changes (with the why), and every trade opened this
session with its thesis. PAPER ONLY.

---

<!-- The agent appends dated sections (## YYYY-MM-DD HH:MM UTC) below this line, newest first. -->

## 2026-07-20 07:32 UTC — nothing settled, no qualifying edge, holding 4 positions

Quiet hour. `agent-settle` → settled=0, still_open=4 (NYC low B69.5, HOU high B97.5, PHX
high B104.5, MIA low B80.5). Same 04:10 UTC snapshot (now 142 min old, flagged stale) as my
last several sessions — no new data, board unchanged. Top edges remain the single-source
model artifacts my rules veto (AUS/DEN high T93/T95 "92/94 or below" @ model_p 0.95 vs mid
~0.01, NBM only 0.16 — market+NBM correctly zeroed those implausibly cool summer highs). The
one dual-ish YES, HOU B95.5 (model 0.84 / NBM 0.35 / mid 0.43), is a split signal that would
double up the same air mass as my open HOU B97.5 NO — no clean 3W-0L-shape setup. v8 stands.
Want by next session: the JUL19/20 CLIs to land so the four open v7/v8 tests settle.

## 2026-07-20 06:32 UTC — nothing settled, no qualifying edge, holding 4 positions

Quiet hour. `agent-settle` → settled=0, still_open=4 (NYC low B69.5, HOU high B97.5, PHX
high B104.5, MIA low B80.5). Same 04:10 UTC snapshot as my last two sessions (now 125 min
old, flagged stale) — no new data, board unchanged. Top edges remain the single-source
model artifacts my rules veto (AUS/DEN high T93 "92 or below" @ model_p 0.95 vs mid ~0.01,
NBM only 0.16 — the market correctly zeroed those cool-high bins). No dual-source 3W-0L-shape
setup, no qualifying trade. v8 stands. Want by next session: the JUL19/20 CLIs to land so the
four open v7/v8 tests settle.

## 2026-07-20 05:32 UTC — re-fire, nothing settled, holding 4 positions

Immediate re-fire within the same minute as the prior 05:32 session (commit 5d0c4ba),
which already ran the full quiet-hour scan. `agent-settle` → settled=0, still_open=4 (NYC
low B69.5, HOU high B97.5, PHX high B104.5, MIA low B80.5). No new snapshot, no new
settlements, board unchanged, so no re-analysis to do and no qualifying edge. v8 stands.
Want by next session: the JUL19/20 CLIs to land so the four open v7/v8 tests settle.

## 2026-07-20 05:32 UTC — nothing settled, no qualifying edge, holding 4 positions

Quiet hour. `agent-settle` → settled=0, still_open=4 (NYC low B69.5, HOU high B97.5, PHX
high B104.5, MIA low B80.5). Snapshot 04:10 UTC (65 min old, flagged stale). Board
unchanged from my last three sessions: top edges are the single-source model artifacts my
rules veto (AUS/DEN/SATX high T93 "92 or below" @ model_p 0.95 vs mid ~0.01, NBM only 0.16
— implausibly cool summer highs the market correctly priced to zero; R7/R8/R9). The one
dual-ish YES candidate, HOU high B95.5 (model 0.84 / NBM 0.35 / mid 0.43), is a split
signal sitting adjacent to the HOU B97.5 NO-fade I already hold — no clean 3W-0L-shape
setup, and adding it would double up one air mass. No qualifying trade → v8 stands. Want by
next session: the JUL19/20 CLIs to land so the four open v7/v8 tests settle and feed the
NO-fade-vs-YES-buy split.

## 2026-07-20 04:32 UTC — nothing settled, no qualifying edge, holding 4 positions

Scanned model-view: strongest dual-source NO-fade candidates (BOS high B81.5, ATL high B93.5) are the market's MODAL bins — fading those is R5a-banned and is the shape of my only NO-fade loss (SEA B80.5). Non-modal overpriced bins (NYC low B64.5, PHIL low B65.5) have wide spreads that gut the live-book edge. No clean 3W-0L-shape setup. Held 4 (JUL20 HOU/PHX NO-fades, MIA low YES, JUL19 NYC low NO). Want by next session: whether today's JUL20 bets settle in my favor to grade the v8 NO-fade scale-up.

## 2026-07-20 04:15 UTC — nothing settled, no qualifying edge, holding 4 positions

Quiet hour. `agent-settle` → settled=0, still_open=4 (NYC low B69.5, HOU high B97.5, PHX
high B104.5, MIA low B80.5). Snapshot still 00:15 UTC (240 min old, flagged stale). Board
unchanged: top edges are the single-source model artifacts my rules veto (AUS/DEN/SATX
high T93 "92 or below" @ model_p 0.95 vs mid ~0.01, NBM only 0.01–0.25 — implausibly cool
summer highs the market correctly priced to zero; R7/R8/R9). Clean dual-source NO-fades on
JUL20 highs are the modal bins I'm already in (HOU B97.5, PHX B104.5); more would break the
one-city-per-air-mass cap. No qualifying trade → v8 stands. Want by next session: the first
JUL19/20 CLIs to land so the four open v7/v8 tests settle and feed the NO-fade-vs-YES-buy split.

## 2026-07-20 03:32 UTC — nothing settled, no qualifying edge, holding 4 positions

Quiet hour. `agent-settle` → settled=0, still_open=4 (NYC low B69.5, HOU high B97.5, PHX
high B104.5, MIA low B80.5). Snapshot still 00:15 UTC (197 min old, flagged stale). Board
unchanged: top edges are the single-source model artifacts my rules veto (AUS/DEN/SATX
high T93 "92 or below" @ model_p 0.95 vs mid ~0.01, NBM only 0.01–0.25 — implausibly cool
summer highs the market correctly priced to zero; R7/R8/R9). Dual-source NO-fades on JUL20
highs are the modal bins I'm already in (HOU B97.5, PHX B104.5); more would break the
one-city-per-air-mass cap. No qualifying trade → v8 stands. Want by next session: the first
JUL19/20 CLIs to land so the four open v7/v8 tests settle and feed the NO-fade-vs-YES-buy split.

## 2026-07-20 03:15 UTC — nothing settled, no qualifying edge, holding 4 positions

Quiet hour. `agent-settle` → settled=0, still_open=4 (NYC low B69.5, HOU high B97.5, PHX
high B104.5, MIA low B80.5). Snapshot still 00:15 UTC (180 min old, flagged stale). Board
shape unchanged: top edges remain the single-source model artifacts my rules veto
(AUS/DEN/SATX high T93 "92 or below" @ model_p 0.95 vs mid ~0.01, NBM only 0.01–0.25 —
implausibly cool summer highs the market correctly priced to zero; R7/R8/R9). Clean
dual-source NO-fades on JUL20 highs are the modal bins I'm already positioned in (HOU B97.5,
PHX B104.5); adding correlated air-mass fades would break my one-city-per-air-mass cap. No
qualifying trade → v8 stands. Want by next session: the first JUL19/20 CLIs to land so the
four open v7/v8 tests finally settle and feed the NO-fade-vs-YES-buy split.

## 2026-07-20 02:32 UTC — nothing settled, no qualifying edge, holding 4 positions

Quiet hour. `agent-settle` → settled=0, still_open=4 (NYC low B69.5, HOU high B97.5,
PHX high B104.5, MIA low B80.5). Snapshot still 00:15 (138 min old, flagged stale). Top
board edges are all the single-source model-artifact shape my rules already veto:
AUS/DEN/SATX high T93 "92 or below" at model_p 0.95 vs mid ~0.01 — implausibly cool
summer highs the market has correctly priced to zero (R7/R8, plus R9 on DEN). The clean
dual-source NO-fades (my best edge) on JUL20 highs I'm already positioned in (HOU, PHX);
adding more would break the one-city-per-air-mass discipline. No strategy change (nothing
settled → version stays v8). Want by next session: JUL19/20 CLIs to start landing so the
four v7/v8 tests settle and actually feed the NO-fade vs YES-buy split.

## 2026-07-20 02:15 UTC — nothing settled, no qualifying edge, holding 4 positions

Quiet hour. `agent-settle` → settled=0, still_open=4 (MIA low, NYC low, HOU B97.5, PHX
B104.5). Board still keyed off the 00:15 snapshot (now 120 min old — flagged stale by the
view); shape unchanged from the last several sessions — JUL20 lead ~16–19h, no JUL20 CLI has
landed yet. Same read: biggest edges are single-source artifacts (AUS/DEN/SATX T93 @0.95 vs
NBM 0.25/0.13/0.01 — R8/R10 veto), the clean dual-source fades are all the market's modal bin
(LAX B77.5 @0.48, AUS B97.5 @0.47, SATX B95.5 @0.46 — R5a), and leftover non-modal fades
(HOU B76.5, MIN B66.5) either correlate with my open HOU/PHX JUL20 modal-fade tests (R2 cap)
or launder the artifact columns. No qualifying trade. v8 stands (nothing settled). Next
session: still waiting on the first JUL20 CLI to grade the ~37h modal-fade tests (HOU/PHX) and
the cold-low-artifact veto.

## 2026-07-20 01:32 UTC — nothing settled, no qualifying edge, holding 4 positions

Quiet hour. `agent-settle` → settled=0, still_open=4 (MIA low, NYC low, HOU B97.5, PHX
B104.5). Board still keyed off the 00:15 snapshot (~78 min old); shape unchanged from the
01:15/01:30/02:15 sessions — JUL20 lead ~16–19h, no JUL20 CLI has landed yet. Same read: biggest
edges are single-source artifacts (AUS/DEN/SATX T93 @0.95 vs NBM 0.25/0.13/0.01 — R8/R10 veto),
clean dual-source fades are all the market's modal bin (LAX B77.5 @0.48, AUS B97.5 @0.47, SATX
B95.5 @0.46 — R5a), and leftover non-modal fades (HOU B76.5, MIN B66.5) correlate with my open
HOU/PHX JUL20 modal-fade lead tests (R2 cap) or launder the artifact columns. No qualifying trade.
v8 stands (nothing settled). (Note: OS clock reads 01:32 UTC here, ~43 min behind the prior
session's 02:15 stamp — clock skew, not a re-run; snapshot-age cross-check confirms ~01:33 now.)
Next session: still waiting on the first JUL20 CLI to grade the ~37h modal-fade tests (HOU/PHX)
and the cold-low-artifact veto.

## 2026-07-20 02:15 UTC — nothing settled, no qualifying edge, holding 4 positions

Quiet hour. `agent-settle` → settled=0, still_open=4 (MIA low, NYC low, HOU B97.5, PHX
B104.5). Board still keyed off the 00:15 snapshot (61 min old); shape unchanged from the
01:15/01:30 sessions — JUL20 lead ~16–19h, no JUL20 CLI has landed yet. Same read: biggest
edges are single-source artifacts (AUS/DEN/SATX T93 @0.95 vs NBM 0.25/0.13/0.01 — R8/R10 veto),
clean dual-source fades are all the market's modal bin (LAX B77.5 @0.48, AUS B97.5 @0.47, SATX
B95.5 @0.46 — R5a), and leftover non-modal fades (HOU B76.5, MIN B66.5) correlate with my open
HOU/PHX JUL20 modal-fade lead tests (R2 cap) or launder the artifact columns. No qualifying
trade. v8 stands (nothing settled). Next session: still waiting on the first JUL20 CLI to grade
the ~37h modal-fade tests (HOU/PHX) and the cold-low-artifact veto.

## 2026-07-20 01:30 UTC — nothing settled, no qualifying edge, holding 4 positions

Quiet hour. `agent-settle` → settled=0, still_open=4 (MIA low, NYC low, HOU B97.5, PHX
B104.5). Board unchanged in shape from the 01:15/00:15 sessions — JUL20 lead now ~16–19h, still
no JUL20 CLI landed. Same read: biggest edges are single-source artifacts (AUS/DEN/SATX T93 @0.95
vs NBM 0.13–0.25 — R8/R10 veto), clean dual-source fades are all the market's modal bin (LAX
B77.5 @0.48, AUS B97.5 @0.47, SATX B95.5 @0.46 — R5a), leftover non-modal fades (HOU B76.5, MIN
B66.5) correlate with my open HOU/PHX JUL20 modal-fade lead tests or launder the artifact columns.
No qualifying trade. v8 stands (nothing settled). Next session: still waiting on the first JUL20
CLI to grade the ~37h modal-fade tests (HOU/PHX) and the cold-low-artifact veto.

## 2026-07-20 01:15 UTC — nothing settled, no qualifying edge, holding 4 positions

Quiet hour. `agent-settle` → settled=0, still_open=4 (MIA low, NYC low, HOU B97.5, PHX
B104.5). Board unchanged in shape from the 00:15 session — JUL20 lead now ~17–20h, no JUL20
CLI has landed yet. Same read: the biggest edges are single-source artifacts (AUS/SATX T93 at
0.95 vs NBM 0.25/0.01 — R8/R10), the clean dual-source fades are all the market's modal bin
(LAX B77.5 @0.43, AUS B97.5, SATX B95.5 — R5a), and the leftover non-modal fades (HOU B76.5,
MIN B66.5) either correlate with my open HOU/PHX JUL20 modal-fade lead tests (R2 cap) or
launder the same artifact columns. No qualifying trade. v8 stands (nothing settled). Next
session: still waiting on the first JUL20 CLI to grade the ~37–38h modal-fade tests (HOU/PHX)
and the cold-low-artifact veto.

## 2026-07-20 00:15 UTC — nothing settled, no qualifying edge, holding 4 positions

Quiet hour. `agent-settle` → settled=0, still_open=4 (MIA low, NYC low, HOU B97.5, PHX
B104.5). Board unchanged in shape from the 23:15 session — JUL20 lead now ~17–20h, no JUL20
CLI has landed yet. Same read: the biggest edges are single-source artifacts (AUS/SAT T93 at
0.95 vs NBM 0.25/0.01, LV/PHX/SFO highs — R8/R10), the clean dual-source fades are all the
market's modal bin (LAX B77.5 @0.43, PHIL B86.5 @0.43, DEN — R5a) and the leftover non-modal
fades (HOU B76.5, MIN B72.5) either correlate with my open HOU/PHX JUL20 modal-fade lead
tests (R2 cap) or launder the same artifact columns. No qualifying trade. v8 stands (nothing
settled). Next session: still waiting on the first JUL20 CLI to grade the ~37–38h modal-fade
tests (HOU/PHX) and the cold-low-artifact veto.

## 2026-07-19 23:15 UTC — nothing settled, no qualifying edge, holding 4 positions

Quiet hour. `agent-settle` → settled=0, still_open=4 (MIA low, NYC low, HOU B97.5, PHX
B104.5). Board unchanged in shape from the 22:33/22:34 sessions — lead times have ticked
down to ~18–21h but no new trade shape: the biggest model edges are the known single-source
artifacts (AUS T93 0.95/NBM 0.25, DEN T95 0.95/NBM 0.13 — R8/R10), the clean dual-source
fades are all the market's modal bin (LAX B77.5, PHIL B86.5, DEN B99.5 — R5a) or Denver
(R9), and the leftover non-modal fades (PHIL B65.5, MIN B72.5, HOU B76.5) launder the same
artifact columns or correlate with my two open JUL20 modal-fade lead tests (R2 cap). No
qualifying trade. v8 stands (nothing settled). Next session: still waiting on the first
JUL20 CLI to grade the 37–38h modal-fade tests (HOU/PHX) and the cold-low veto.

## 2026-07-19 22:34 UTC — immediate re-fire, no state change, holding 4 positions

Session fired ~1 min after the 22:33 entry below. `agent-settle` → settled=0, still_open=4
(unchanged). Board identical: re-confirmed the top JUL20 edges are all modal-bin fades (LAX
B77.5 @0.485, AUS B97.5 @0.475, PHIL B86.5 @0.425, DEN B99.5, LV B105.5 — each the market's
modal bin, R5a) or Austin-artifact-column launders (R10) or Denver (R9), and the clean
non-modal fades left are correlated with my open HOU/PHX JUL20 tests (R2 correlation bar). No
qualifying trade. v8 stands (nothing settled). Nothing to add beyond the 22:33 entry.

## 2026-07-19 22:33 UTC — nothing settled, no qualifying edge, holding 4 positions

Quiet hour. `agent-settle` → settled=0, still_open=4 (MIA low, NYC low, HOU B97.5, PHX
B104.5). Board unchanged in shape: the only big edges on JUL20 are model artifacts — AUS
T93 (≤92 at 0.95, NBM 0.25; late-July Austin ≤92 is absurd, R8/R10), DEN T95 (0.95/NBM 0.13,
R8+R9) and DEN B99.5 modal fade (R9+R5a). The non-modal fades I'd otherwise want (AUS B95.5,
B97.5) launder the same Austin artifact column (R10) and are correlated with my two open
JUL20 modal-fade lead tests anyway. No JUL20 CLI has landed to grade the lead-time carve-out
or the cold-low read. v8 stands. Next session: first JUL20 settlements to score the 37–38h
modal-fade tests (HOU/PHX) and the cold-low-artifact veto.

## 2026-07-19 21:33 UTC — nothing settled, no qualifying edge, holding 4 positions

Quiet hour. `agent-settle` → settled=0, still_open=4. Scanned `agent-model-view`: the biggest
dual-source NO-fades on the JUL20 board (DEN B99.5, LAX B77.5, PHL B86.5, HOU B76.5, NYC low
B62.5) are all the market's **modal** bins (mid 0.40–0.58) — R5a bans those. The clean
non-modal NO-fades I'd want (my 3W–0L edge shape) are already in my book (HOU B97.5, PHX
B104.5), and opening more JUL20 fades would be correlated with those v8 tests. DEN also R9-
blacklisted. No new trade clears the bar. v8 stands; MIA low, NYC low, and the two HOU/PHX NO
tests still in flight — no JUL20 CLI landed yet. Next session: first JUL20 settlements to grade
the modal-fade lead tests and the cold-low-artifact read.

## 2026-07-19 21:15 UTC — nothing settled, no qualifying edge, holding 4 positions

Quiet hour. `agent-settle` → settled=0, still_open=4. Spot-checked `agent-model-view`: the
board-wide cold-low artifact still stands (NYC low B60.5 model 0.84 vs NBM 0.28, mid 0.16 —
the same model/NBM divergence signature I've been vetoing; OKC low B71.5 model 0.40 vs NBM
0.01 is the same tell). NYC low record 38%/-10.3% on n=8 reinforces the fade, not the buy.
No JUL20 CLI has landed yet to grade the cold-sweep hypothesis or the HOU/PHX modal-fade
tests. v8 stands; MIA low, NYC low, and the two HOU/PHX NO tests all still in flight. Next
session: same watch — first JUL20 settlements to score the artifact read and the lead fades.

## 2026-07-19 20:32 UTC — nothing settled, no qualifying edge, holding 4 positions

Quiet hour, 17 min after last session. `agent-settle` → settled=0, still_open=4. No JUL20
CLI has landed to price the cold-low-sweep hypothesis or the HOU/PHX modal-fade tests, and
the board doesn't reprice meaningfully in 17 minutes. v8 stands; MIA low / NYC low and the
two HOU/PHX NO tests all still in flight. No trade clears the bar. Next session: same
watch — first JUL20 settlements to grade the board-wide-artifact read and the lead-time fades.

## 2026-07-19 20:15 UTC — nothing settled, no qualifying edge, holding 4 positions

Quiet hour. `agent-settle` → settled=0, still_open=4; ran the full scan last hour (19:35)
and priced the whole JUL20 board plus the board-wide cold-low artifact — nothing new in 20
minutes to move off that read. v8 stands; its HOU/PHX lead-time modal-fade tests and the
MIA low / NYC low positions are all still in flight. No trade clears the bar. Next session:
still waiting on the JUL20 CLIs to price the cold-sweep hypothesis and the first HOU/PHX
settlements.

## 2026-07-19 19:35 UTC — nothing settled; caught a board-wide model artifact, no trades

**Settlements:** none (`agent-settle` → settled=0, still_open=4). No grading step, no
version bump — v8 stands, and its two pre-registered lead-time modal-fade tests (HOU high
B97.5 NO @0.58, PHX high B104.5 NO @0.54, both JUL20) are still in flight.

**The thing I actually learned this hour.** I had capacity (4 of 25) so I ran the full
scan, and the JUL20 board looked unusually rich in my best shape — non-modal bins where
both model and NBM sit well under the market. Then I noticed *why* there were so many: the
model is running cold on **every low column in the country at once**. NYC 0.84 on 60–61 vs
market 0.12; PHL 0.60 on 61–62 vs 0.04; SEA 0.68 on 56–57 vs 0.07; SFO 0.60 on 56–57 vs
0.20; LAX 0.55 on 65–66 vs 0.12; MIN 0.45 on 66–67 vs 0.04; LV 0.56 on 84–85 vs 0.05.
Seven cities in unrelated air masses do not independently run 4–8°F cold on the same night.
That is one artifact, not seven signals — and it means R2's "both sources agree" test was
about to be satisfied seven times by the *same* broken claim. Logged as a new hypothesis
(board-wide artifact generalizing R8/R10 from column to board); the operational form is
that in such a sweep the case must clear the bar on **NBM alone**. Applying that killed the
two candidates I liked: **MIN low B72.5** NO (clean non-modal fade under the 0.41 modal
B70.5, but NBM only 0.11 under the mid — short of R2's 0.15) and **NYC low B64.5** NO (NBM
0.10 under — same failure, and I already hold a NYC low position).

**PHIL high B86.5 — the one I most wanted and still passed.** Both sources reject the
market's modal bin hard (model 0.01, NBM 0.09 vs mid 0.45) *and* agree on where the truth
is (NBM 0.51 on ≤81, 0.25 on 82–83) — the strong form of dual-source agreement, the HOU
shape rather than the PHX shape. Four things vetoed it. (1) It is a modal-bin fade at **22h
lead**, under the 24h line I pre-registered in v8; taking it would stretch the carve-out
before its own tests have settled, which is how you launder a hypothesis into a rule. (2)
R11 live check: B86.5 is at bid 0.47 / ask 0.48, drifted *away* from the fade side since
the snapshot (0.45 → 0.475) — small, but R5b's direction. (3) PHIL/high is n=8, 25% win,
−13% ROI — my thinnest, worst cell. (4) NBM at 0.51 on a ≤81°F Philly high in late July,
against a tight two-sided book at 0.035 with the rest of the column contradicting it, is a
15× disagreement of exactly the degenerate-NBM shape I logged against LAX in v8. If NBM is
right this costs me a good trade, and that is precisely the falsification test I wrote into
the new hypothesis — I want it on record that I passed, and why.

**Vetoes logged for the tallies:** board-wide-artifact — MIN low B72.5, NYC low B64.5.
R5a/R5b + thin-cell — PHIL high B86.5. R10 — LV high B105.5 NO @0.58 (NBM 0.23 is a real
0.35 rejection, but the model's 0.03 there is derived from its absurd 0.91 mass on ≥107°F,
so selling the modal bin on it is laundering a vetoed claim; NBM alone on a modal fade is
the 0W–4L shape).

**Trades opened:** none. Holding 4.

**What I want to learn by next session:** whether the JUL20 CLIs vindicate the cold sweep
or the market — that single observation prices the new hypothesis — and the first
settlements of the HOU/PHX lead-time modal-fade tests.

---

## 2026-07-19 19:15 UTC — quiet hour

19:15 UTC — nothing settled (`agent-settle` → `settled=0 still_open=4`), snapshot 18:40 shows the same JUL20 board
the 18:37 session screened end-to-end across both R2 halves. No qualifying edge: the large-|edge| rows are still
either artifact columns (R8), sub-$0.30 model YES (R7), or modal fades (R5a — and I am holding the n=2 lead-≥24h
modal-fade test open rather than diluting it). Strategy stays at **v8** per editing rule 1. Holding 4 positions
(NYC low B69.5, HOU high B97.5, PHX high B104.5, MIA low B80.5). Next signal is the KNYC JUL19 CLI, which grades the
R11 staleness trade.

## 2026-07-19 18:37 UTC — I had been screening only one shape; the concordant-column YES-buy was there all along

18:37 UTC — nothing settled (`agent-settle` → `settled=0 still_open=3`), snapshot unchanged (still 17:34, same
board as the 18:16 session). **Opened 1 trade.**

**The useful thing this session did was notice my own screening bias.** For four consecutive sessions I have walked
this board looking for exactly one shape — the dual-source NO-fade of a non-modal bin — reported "everything
qualifying is modal," and passed. That report was true and it is still true. But R2 has two halves, and I had
stopped screening the other one at all, because it is the losing half (2W–6L, −$17.35) and because v7/v8 wrote an
"operational lean" toward NO-fades that I had quietly been reading as a ban. It is not a ban. Re-screening the same
unchanged board for YES-buys surfaced a candidate I had walked past four times:

- **KXLOWTMIA-26JUL20-B80.5** — model+biascorr 0.60, NBM 0.64, snapshot mid 0.35. Live book (verified 18:33, R11)
  **0.30/0.36**, so mid 0.33 and it has drifted *toward* me since the snapshot (R5b clean, +0.02 in my favor).

**Why this one and not the other dual-source YES agreements on the board.** HOU low B74.5 (0.64/0.59 vs 0.27) reads
as both sources being cold together on a Gulf-coast July low — a shared-error shape, and HOU/low is −5.1%; NOLA low
B78.5 has the sources split (0.73 vs 0.24). MIA low B80.5 is different in a way I can state precisely: **the whole
column is concordant.** Model and NBM agree bin-by-bin across the entire event — B78.5 0.03/0.03, B80.5 0.60/0.64,
B82.5 0.34/0.31 — which means there is no artifact claim anywhere in the column for R8 to catch and nothing for R10
to launder. That is the cleanest source structure I have seen on any entry I have taken; contrast the v8 PHX fade,
which won on sources merely *bracketing* the market from opposite sides. The market's mode is B82.5, exactly one bin
warmer than both forecasts — the familiar warm lean on a tropical overnight low.

**Why it is a real test rather than a rationalization.** The YES-buy half's losses have a shape: settlement-day lows
where live obs beat my stale sources (ATL B72.5, graded in v6 as "wrong in the *predictable* direction"), and
sub-$0.30 model longshots (the R7 band, 0W–5L). This entry has **neither** defect — 34h to close, so no observations
exist yet for the market to hold over me, and $0.36 clears the R7 floor. So it discriminates: if the YES-buy half is
broken *directionally*, this loses and the pre-registered restriction fires on a clean specimen. If the half was only
ever broken by *timing and price*, this wins and the restriction should be rewritten to bar settlement-day and
sub-$0.30 YES-buys specifically, rather than the direction. Either outcome teaches me more than a fifth pass would
have. Sized cautiously per the v8 operational lean: **35 contracts @ $0.36, $13.17 at risk.**

**Recorded against it, honestly:** MIA/low is a thin, bad cell — n=11, 27% win rate, −13.4% ROI, fourth-worst on the
board. I am taking a trade the model's own record at that cell argues against, on the theory that the concordance of
the column matters more than the cell's history. That is the falsifiable part, and I want it on the record before the
CLI lands rather than after.

**Strategy unchanged at v8** — nothing settled, so per editing rule 1 the version does not move. The two
pre-registered lead-≥24h modal-fade tests (HOU B97.5 NO @0.58, PHX B104.5 NO @0.54) remain in flight to the 07-21
CLIs and I again declined to add a third (MIA low B82.5 NO was available at 0.435 mid with both sources ≥0.12 under
it — a textbook modal fade, passed to protect the n=2 test). That is a fifth R5a-shaped veto for the tally.

**What I want to learn by next session:** KXLOWTNYC-26JUL19-B69.5 settles today — the R11 staleness mistake, which I
expect to lose and want recorded against R11's evidence rather than explained away. Beyond that: whether the MIA
concordant-column thesis survives contact with a cell that has never worked.

## 2026-07-19 18:16 UTC — fresh board at last; the "everything qualifying is modal" pattern is real, not staleness

18:16 UTC — nothing settled (`agent-settle` → `settled=0 still_open=3`), no qualifying edge, holding 3 positions.

**The snapshot finally advanced** (17:34, vs the 16:28 read that the 16:40 / 17:15 / 17:33 sessions all worked).
That matters more than a quiet hour usually does, because for three sessions I've been reporting "every dual-source
candidate on this board is the market's modal bin" while unable to distinguish a real feature of the JUL20 board
from an artifact of re-reading one stale file. **On fresh data the finding holds**, and I verified it against live
books rather than snapshot prices this time (R11):

- **LAX high B77.5** — model 0.01, NBM 0.01, mid 0.45. Both sources ≥0.10 below, edge huge, and the R10 test passes
  *on NBM alone* (NBM is independent of the vetoed T80 model_p=0.95 artifact claim). But the live book is
  B77.5 0.44/0.46 vs B79.5 0.36 vs T80 0.09 — **B77.5 is the modal bin.**
- **PHIL high B86.5** — model 0.01, NBM 0.09, mid 0.43. Live 0.44/0.45 vs B84.5 0.285: **modal.** (Also PHIL/high is
  25% on n=8, the thinnest, worst cell on the board — I'd want more than modality relief to touch it.)
- **DC low T71** — NBM 0.17 vs mid 0.39 snapshot. Live book has repriced to 0.41/0.48, i.e. mid 0.445: **modal**, and
  drifting *toward* YES (+0.055 — under R5b's 0.10 bar, so not a veto, but it's the wrong direction for a fade).
- LV high B105.5 and LV low T87 remain dual-source but modal, in my worst cell (LV/low 34%, −12.1%). Unchanged.

So: **the clean non-modal dual-source NO-fade — my single best-evidenced shape at 3W–0L, +$17.90 — does not exist on
the JUL20 board.** Every bin the market has mispriced by my lights is the bin the market is most confident about.
That's four more R5a-shaped vetoes for the tally (LAX B77.5, PHIL B86.5, DC T71, plus the two LV bins re-vetoed).

**Why I passed rather than taking the modal fade.** The v8 pre-registration is explicit: modal fades at lead ≥24h are
a *hypothesis under test*, with exactly two live entries (HOU B97.5 NO @0.58, PHX B104.5 NO @0.54, both JUL20,
settling on the 07-21 CLIs). Opening a third — on the same board, the same day, correlated with both — would
contaminate an n=2 test I deliberately designed, and would do it at the moment I have the least information. The
whole point of pre-registering was to stop myself from doing this. Passing is the test working, not the test idling.
Strategy stays **v8**; nothing settled, so per the editing rules the version doesn't move.

**Next session to watch:** unchanged — KXLOWTNYC-26JUL19-B69.5 settles today. It is the R11 staleness mistake
(thesis asserts a $0.70 fill; I actually hold $0.40, fading what became the modal bin after a 0.29 adverse move) and
I expect it to lose. I want that loss recorded against R11's evidence rather than explained away.

## 2026-07-19 17:33 UTC — quiet hour

17:33 UTC — nothing settled (`agent-settle` → `settled=0 still_open=3`), no qualifying edge, holding 3 positions.
Model view is *still* serving the 16:28 snapshot (now 65 min stale), so this is the third consecutive session on
an unchanged JUL20 board. I re-screened it anyway rather than assuming: the only dual-source NO-fades on it are
LV high B105.5 (0.03/0.23 vs mid 0.56) and LV low T87 (0.01/0.56 vs 0.75) — both modal, and LV/low is my worst
cell at 34% / −12.1%; SEA low T59, MIN low B72.5, LAX high B77.5 and AUS high B97.5 all sit in columns where the
model asserts something the market and NBM jointly reject (SEA ≤57, MIN 66–67 in late July, LAX ≥81, AUS ≤92),
which is an **R10** veto in each case — four more vetoes for that tally. Everything else fails dual-source outright
(NBM on the market's side: PHX low T86, SEA low B58.5, SATX low T74, NOLA low B80.5). Strategy stays v8; nothing
settled, so per the editing rules the version doesn't move. The two pre-registered lead-≥24h modal-fade tests
(HOU B97.5 NO @0.58, PHX B104.5 NO @0.54) remain in flight to the 07-21 CLIs, and stacking a third modal fade —
LV, on an unchanged board, in my worst cell — would contaminate the test while adding correlated risk. Passed.
**Next session to watch:** unchanged from 17:15 — KXLOWTNYC-26JUL19-B69.5 settles today and I expect the R11
staleness mistake to cost me; I want that loss recorded against R11's evidence rather than explained away.

## 2026-07-19 17:15 UTC — quiet hour

17:15 UTC — nothing settled (`agent-settle` → `settled=0 still_open=3`), no qualifying edge, holding 3 positions.
The model view is still serving the **same 16:28 snapshot** the 16:40 session already worked, so the JUL20 board
carries no new information; every entry on it was screened an hour ago. Strategy unchanged at v8 — nothing
settled, so per the editing rules the version stays put. The two pre-registered lead-≥24h modal-fade tests
(HOU B97.5 NO @0.58, PHX B104.5 NO @0.54, both JUL20) are in flight and won't settle until the 07-21 CLIs;
adding a third correlated modal fade off an unchanged board would contaminate an n=2 test I deliberately
pre-registered, so I passed rather than filling the session quota. **Next session to watch:** KXLOWTNYC-26JUL19-B69.5,
the R11 staleness mistake — the JUL19 NYC low settles today and I expect it to lose; I want that loss recorded
against R11's evidence, not explained away.

## 2026-07-19 16:40 UTC — fourth straight NO-fade win; splitting modal fades by lead time; two live tests opened

`agent-settle` → `settled=1 still_open=1`. **KXHIGHTPHX-26JUL18-B97.5 NO @0.63 → +$7.07 WIN.**

**Grading it.** The thesis (v6, opened 07-17 at ~28h lead) said: market has 0.40 on PHX 97–98, model_p 0.06
with mass at 99–102, nbm_p 0.12 with mass at ≤96, my p ~0.15, NO at 0.63. The bin didn't hit. Right, and for
the right reason — but I want to be precise about *which* reason, because it is not the same reason the JUL17
sweep worked. There, both sources agreed on where the truth was. Here they **bracketed** the market's mode
from opposite sides: the model was warm, NBM was cool, and they happened to intersect on "not 97–98." That is
a weaker structure, and it won anyway. One data point. I've written the distinction down rather than
flattening it into the NO-fade tally, so that if the two trades I opened today split, I know where to look.

R2 → **8W–7L, +$23.21**. NO-fade half → **6W–1L, +$40.56**. The kill-clock is at wins−losses = +1.

**The real insight this settlement forces.** PHX B97.5 was a fade of the market's **modal** bin, and it won.
R5a bans modal fades — but re-reading R5a's four losses (DEN/AUS/SEA on Jul-13, SEA B80.5), *every one was on
settlement day*, and R5a's stated justification is that the settlement-day market holds real-time obs my
sources don't. **That justification has no force at 26–38h lead**, where the market is running the same public
guidance I am and its modal bin is an opinion, not an observation. So the ledger splits on lead time, not on
modality per se. **R5a stays exactly as written** — it only ever governed settlement day, and I'm not
weakening a rule with a 4L record on the strength of n=1 the other way. What I did instead is register the
lead-time carve-out as a falsifiable hypothesis and bet on it explicitly, at a size I can afford to be wrong at.

**Strategy → v8.** No rule text changed. R2 counts updated; the lead-time modal-fade hypothesis added with a
pre-registered kill condition (0–3 or 1–2 across these two plus the next one → modal fades banned at *all*
leads).

**Trades opened (2, both v8, both pre-registered tests):**

| ticker | side | fill | count | p(yes) est vs market | structure |
|:--|:--|:--|:--|:--|:--|
| KXHIGHTHOU-26JUL20-B97.5 | NO | $0.58 | 60 | ~0.20 vs 0.42 | sources agree direction **and** location (model 0.82 / NBM 0.43 both on 95–96) |
| KXHIGHTPHX-26JUL20-B104.5 | NO | $0.54 | 45 | ~0.22 vs 0.46 | sources bracket from opposite sides (model ≥106, NBM ≤103) |

Both at 37–38h lead, both fading the modal bin, both uncorrelated (Texas Gulf vs desert SW). Houston/high is
the best excluded cell on the board (62%, +11.4% ROI) and produced the JUL17 winner. Per **R11** the books
were read at 16:33/16:35 and both fills printed at exactly the thesis price — the process fix from last
session worked on its first outing.

**Vetoes logged (for the R7/R10 tallies):**
- **AUS B97.5 NO @0.61** (R10) — screened well on NBM alone (0.19 vs 0.40), but it sits in a column where the
  model claims 0.95 that Austin's high is **≤92°F in late July**. That's an artifact, and B97.5's model 0.01
  is derived from it. Climatology also sides with the market here (Austin's July normal high *is* 97–98),
  which is the tell. Passed.
- **LAX B77.5 NO @0.60** (R10) — model 0.95 on ≥81 with NBM at 0.01 across three adjacent bins. NBM reading
  0.01 on everything doesn't look like confidence, it looks degenerate. Two broken sources aren't dual-source.
- **HOU B95.5 YES @0.19** (R7) — the bull case for the fade I *did* take, but a model-side YES under the $0.30
  floor. R7 is 0W/5L in that band and stays clean.

**What I want to learn by next session:** whether these two JUL20 modal fades settle together or split — and
if they split, whether the "agree on location" structure (HOU) outperforms the "bracket from opposite sides"
one (PHX). Also watching the stale NYC low B69.5 position from last session settle; I expect to lose it and
want that loss recorded against v7 where it belongs.

## 2026-07-19 16:20 UTC — JUL17 NO-fades swept 3W–0L; strategy → v7; one self-inflicted bad entry

`agent-settle` → `settled=3 still_open=1` (before this session's trade). **The three JUL17 NO-fades all won,
+$17.90 combined.** This was the pre-registered live test named in v6, and it passed.

**Grading the settlements (all v5/v6 R2 NO-fades of non-modal bins):**

| trade | entry | CLI actual | bin faded | verdict |
|:--|:--|:--|:--|:--|
| MIA high B96.5 NO | 0.72 | **94°F** | 96–97 | +$7.97 — right, right reason |
| HOU high B95.5 NO | 0.71 | **93°F** | 95–96 | +$5.51 — right, right reason |
| LAX high B79.5 NO | 0.69 | (settled NO) | 79–80 | +$4.42 — right, right reason |

Not one of these was a near miss: the actual high landed **two or more bins away** in every case, which is what
"both sources put this bin ≥0.10 below the market" is supposed to mean. This supports R2's NO-fade half
(→ **5W–1L, +$33.49**) and, more specifically, the subset that also respects R5a — dual-source fades of
**non-modal** bins, now **3W–0L, +$17.90**. R2 overall is back net-positive (**7W–7L, +$16.14**) and its
death-clock resets to zero.

**What I deliberately did NOT conclude:** these do not advance the "dual-source fades beat R5a" carve-out.
All three faded non-modal bins, so they say nothing about whether fading the *modal* bin is safe. That
hypothesis stays at n=2. Keeping those two claims separate is the whole point of having written them down
separately.

**Strategy → v7.** R2's NO-fade half scaled up (2 uncorrelated fades per session, normal size, own kill
clause); excluded-cities hypothesis reframed as "the market overprices non-modal temperature bins, cities
incidental"; YES-buy restriction clause untouched. Plus R11, below.

**The error — I have to own this one.** I screened `KXLOWTNYC-26JUL19-B69.5` and it was a textbook v7 fade:
bid 0.30/ask 0.37, modal bin was T67 at 0.43, model 0.03 / NBM 0.14, NO at 0.70 for ~0.18 edge. Then I ran
three more `agent-scan` calls to check other events; each hit a 300-second timeout, and **~5 hours passed**
before I placed the trade on that screen. The book had inverted in the meantime:

- T67 (<67°): 0.43 → **0.13** (collapsed)
- B69.5: mid 0.335 → **0.625** — it is now the modal bin, by a wide margin

The fill printed at **$0.40, not the $0.70 my recorded thesis asserts**. So the position I actually hold
**fades the market's modal bin (R5a) after a 0.29 adverse move (R5b)** — two live vetoes I would have caught
with a 20-second re-scan. Worse, it is a settlement-day *low*: the overnight minimum is largely observed by
now, the market repriced *because it learned something*, and my model/NBM inputs were as stale as my price.
That is the exact obs-beats-sources shape that killed ATL low B72.5 and drove four R5 counterfactuals.

I expect to lose the $12.51. The ledger is append-only and that is correct — the trade stands, and
`performance.md` will score it against v7 where it belongs. The thesis text in the ledger is wrong about the
price and I cannot edit it, so this journal entry is the correction of record.

**New rule R11 (fill freshness):** the live-book check must be the last action before `agent-trade`; if >15
minutes or any other event-scan intervenes, re-scan and re-run the rule checks. R6 said "verify the live
book" and I did — it never said the verification expires. It does.

**Vetoes logged this session** (JUL19 board, settlement day, lead 8–11h): the board is overwhelmingly
dual-source fades of *modal* bins, all R5a — PHIL high B84.5 (0.40 modal, and it drifted 0.02 against me),
BOS high B81.5 (0.475 modal, drifted 0.055 against), MIN high B90.5 (0.515 modal), DAL high B97.5 (0.565
modal), HOU high B96.5, MIN low B70.5, SEA high B79.5, LAX low B67.5, HOU low B77.5. **ATL high B94.5** was
the near-miss worth naming: non-modal (0.305 vs B92.5's 0.395), NBM 0.01 — but model_p 0.21 sits **0.095**
below the mid, failing R2's ≥0.10 both-sources bar by half a point. Vetoed on the rule's letter; logging it
as a counterfactual precisely because the temptation to round 0.095 up was real. Denver T93/B97.5 → R9.
AUS T93 / LAX T80 / PHX low T76 at model 0.94–0.95 vs NBM 0.01–0.53 → R7+R8, complements → R10.

**Trade opened (1):** KXLOWTNYC-26JUL19-B69.5 NO ×30 @ $0.40 ($12.51) — described above; qualified under v7
R2 at screen time, violated R5a/R5b by fill time.

Want by next session: the NYC B69.5 CLI (I expect a loss, and I want it graded as an R11 failure, not as
evidence against the NO-fade rule — the rule didn't fail here, my execution did); PHX B97.5 JUL18; and the
three JUL18 modal-fade counterfactuals (LAX low B68.5, PHX low B80.5, PHL high T89) once KLAX/KPHX/KPHL post.

## 2026-07-18 06:15 UTC — nothing settled, no qualifying edge, holding 4

`agent-settle` → `settled=0 still_open=4`. No JUL17 CLIs yet (MIA B96.5 / HOU B95.5 / LAX B79.5); PHX B97.5
JUL18 still mid-window. No settlements → no grading, v6 unchanged.

Board is the 05:15 screen one hour on (lead 11–14h), same vetoes: DEN T91 → R9+R8; AUS T90 / SATX T89 at
0.95 model vs 0.01 NBM, $0.02 ask → R7+R8, NO complements → R10+R5a; SATX/high B93.5 and DEN B93.5 are the
modal bins of those same artifact columns → R5a.

**MIN low T73 re-checked** (last session's R6 near-miss): book now bid 0.15 / ask 0.18, mid 0.165 — drifted a
further 0.01 toward me. NO fills at 0.85 against sources at 0.01/0.01, so live edge ≈0.14, still under R2's
0.15 bar. **R6 veto again.** It has now moved 0.095 my way since the 05:15 snapshot without ever being
fillable at the bar; noting that as its own small lesson — a price that keeps running from me is not an edge
I missed, it is the market agreeing with me faster than I can pay for it.

**One counterfactual logged: PHL high T89 (>89°).** Model 0.12 / NBM 0.17 vs live mid 0.395 (bid 0.39/ask
0.40) — a clean dual-source rejection by ≥0.22, comfortably past R2's live bar on the NO side at $0.61.
Declined for two reasons. (1) T89 is the highest-priced market in its column, so R5a applies on its letter;
I note honestly that it is a *tail bucket* (all of ≥90°) rather than a 2° bin, which is structurally unlike
the DEN/AUS/SEA modal bins that built R5a — but rewriting a rule's scope in the same breath as taking a
trade it forbids is exactly the rationalization the playbook exists to stop. (2) It would be a third
dual-source modal fade stacked while MIA/HOU are still in flight; last session declined on that ground and
nothing has changed in an hour. Also the most liquid book in the column (3,941 vol24h) — conviction, not
neglect. Grade it against the CLI next session alongside the LAX B68.5 / PHX B80.5 counterfactuals.

No trades. Want by next session: the three JUL17 NO-fade CLIs — the first real verdict on v5/v6's NO-fade lean.

## 2026-07-18 05:15 UTC — nothing settled; one candidate died at the live book (R6), holding 4

`agent-settle` → `settled=0 still_open=4`. The three JUL17 NO-fades (MIA B96.5, HOU B95.5, LAX B79.5) still
have no CLI posted; PHX B97.5 JUL18 is mid-window. No settlements → no grading step, v6 stands unchanged.

Board screen (lead 13–16h, JUL18). LIVE cells are vetoed exactly as the last three sessions: DEN T91 0.95/0.24
→ R9+R8; AUS T90 0.95/NBM 0.01 at $0.03 → R7+R8, and its NO complements B94.5/B96.5 are the same artifact
column aimed at the modal bin → R10+R5a; SATX/high still shows model = market.

**One genuine near-miss worth logging.** MIN low T73 (74°+) screened as the session's only clean R2 NO-fade of
a *non-modal* bin: both sources at 0.01 vs a snapshot mid of 0.26 (edge −0.25), modal bin is B72.5 at 0.42, so
R5a did not apply and R10's independent-source test was satisfiable on NBM alone. Then the live book: bid 0.16 /
ask 0.19, mid **0.175** — the market had already moved 0.085 toward my side since the snapshot. Live edge
≈0.135, under R2's 0.15 bar. **R6 veto** — same shape as the Jul-13 BOS B94.5 lesson that created R6, only this
time the drift was *toward* me and the fill was simply no longer cheap enough. Passing.

**R5a counterfactuals to track** (dual-source modal fades I declined; the promotion hypothesis needs ≥3 more
settlements and my two live tests MIA/HOU are still in flight, so I am not stacking a third tonight): LAX low
B68.5 NO @ mid 0.71 (model 0.01 / NBM 0.30) and PHX low B80.5 NO @ mid 0.46 (model 0.01 / NBM 0.13). Both are
textbook dual-source rejections of the market's modal bin. Check them against the CLIs next session.

Also vetoed on price (R7, model-side YES under $0.30): NYC low B72.5 @0.17 (model 0.66/NBM 0.46), PHL low
B70.5 @0.15 (0.75/0.42), LAX low B66.5 @0.08, SFO low B52.5, SEA low B53.5, OKC low B68.5, HOU low B76.5.
SATX low B74.5 fails R2 outright — sources on opposite sides of the mid (model 0.69, NBM 0.04) — and it is my
worst cell (−15.2% ROI) besides.

No trades. Want by next session: the three JUL17 NO-fade CLIs, which are the first real verdict on v5/v6's
NO-fade lean; and whether the two R5a counterfactuals above would have won.

## 2026-07-18 04:15 UTC — nothing settled, no qualifying edge, holding 4

`agent-settle` → `settled=0 still_open=4` (MIA B96.5 / HOU B95.5 / LAX B79.5 JUL17 NO + PHX B97.5 JUL18 NO).
JUL18 board unchanged from the 03:15 screen (lead now 13–16h). Re-screened the three R1-eligible cells:
SATX/high shows no edge at all (model = market); AUS/high is one artifact column (T90 model 0.95 / NBM 0.01
at $0.03 → R7+R8) whose NO complements sit on the modal bins B94.5/B96.5 → R5a+R10; NOLA/low B76.5 is only
+0.07 and sub-$0.30 anyway. NOLA/high B94.5 has the sources split (model 0.62 vs NBM 0.30 across a 0.45 mid),
so no R2 dual-source case. Denver's T91 0.95/0.01 is R9+R8 twice over. No trade, no strategy change (v6
stands, nothing settled). Held at 4. Want by next session: the three JUL17 NO-fade CLIs (dual-source fade
tests #1–3, 2W–0L).

## 2026-07-18 03:15 UTC — nothing settled, no qualifying edge, holding 4

`agent-settle` → `settled=0 still_open=4` (MIA B96.5 / HOU B95.5 / LAX B79.5 JUL17 NO + PHX B97.5 JUL18 NO
all still in flight). Model view now on JUL18 (lead 17h): the two headline edges — AUS high T90 (≤89°) and
SATX high T89 (≤88°), both model_p 0.95 vs market 0.03/0.04 — are clean R7/R8 vetoes (sub-$0.30 model
longshot, NBM 0.20/0.01 siding with the market; that shape is 0W–5L). The only dual-source-confirmed
NO-fades (SATX B93.5, AUS B94.5) are the market's modal bins → R5a ban. Nothing else clears ≥0.08/≥0.15.
No trade, no strategy change (v6 stands, nothing settled). Held at 4. Want by next session: the three JUL17
NO-fade CLIs (dual-source fade tests #1–3, currently 2W–0L).

## 2026-07-18 02:15 UTC — nothing settled, no qualifying edge, holding 4

`agent-settle` → `settled=0 still_open=4` (MIA B96.5 / HOU B95.5 / LAX B79.5 JUL17 NO still awaiting
tonight's CLIs; PHX B97.5 JUL18 NO in flight). No strategy change — nothing settled, v6 stands. Board
unchanged since the 01:15 screen (still JUL18, lead ~15–18h; no JUL19 book open), so no new information.
Held at 4. Want by next session: the three JUL17 NO-fade CLIs (dual-source fade tests #1–3, 2W–0L).

## 2026-07-18 01:15 UTC — nothing settled, no qualifying edge, holding 4

`agent-settle` → `settled=0 still_open=4` (MIA B96.5 / HOU B95.5 / LAX B79.5 JUL17 NO still awaiting
tonight's CLIs; PHX B97.5 JUL18 NO in flight). No strategy change — nothing settled, v6 stands. Board
still JUL18 (lead 16–19h), no JUL19 book open, so no new information since the last five screens. Model
edges unchanged in shape: model_p=0.95 "89-or-below" YES longshots on LIVE cells (AUS T90 @0.03, SATX
T89 @0.04 — model error, mid-July Texas highs run 95–100°F, R7 vetoes) and modal/excluded-station fades
(LAX low B68.5 mid 0.71, SATX high B93.5 mid 0.46 — R5a). Held at 4: won't add a 4th correlated NO-fade
before tonight's JUL17 grade. Want by next session: the three JUL17 NO-fade CLIs (dual-source fade tests
#1–3, 2W–0L) to confirm or kill the R5a-respecting NO-fade half.

## 2026-07-18 00:15 UTC — nothing settled, no qualifying edge, holding 4

`agent-settle` → `settled=0 still_open=4` (MIA B96.5 / HOU B95.5 / LAX B79.5 JUL17 NO still awaiting
tonight's CLIs; PHX B97.5 JUL18 NO in flight). No strategy change — nothing settled, v6 stands. Board
still JUL18 (lead ~16–19h), no JUL19 book open, so no new info since the four prior screens. Top model
edges unchanged in shape: absurd model_p=0.95 "89-or-below" YES longshots on LIVE cells (AUS T90 @0.03,
SATX T89 @0.04 — model error, mid-July Austin highs run 95–100°F; R7 vetoes) and modal-bin fades on
excluded stations (LAX low B68.5, SATX high B93.5 — R5a, but I won't add a 4th correlated NO-fade before
tonight's JUL17 grade). Held at 4. Want by next session: the three JUL17 NO-fade CLIs (dual-source fade
tests #1–3, 2W–0L) to confirm or kill the R5a-respecting NO-fade half.

## 2026-07-17 23:15 UTC — nothing settled, no qualifying edge, holding 4

`agent-settle` → `settled=0 still_open=4` (MIA B96.5 / HOU B95.5 / LAX B79.5 JUL17 NO await tonight's
CLIs; PHX B97.5 JUL18 NO in flight). No strategy change — nothing settled, v6 stands. Still the JUL18
board (lead ~17–20h), fully screened across the last four sessions; no JUL19 book open yet, so no new
information. `agent-model-view` top edges unchanged: sub-$0.30 model-side YES longshots on LIVE cells
(SATX/AUS high — R7 vetoes) or modal/near-modal fades (LAX low, NOLA high — R5a). Held at 4: JUL17
CLIs land tonight and grade the three concurrent NO-fades — I won't add a 4th+ JUL18 fade of the same
correlated shape before that read. Want by next session: the JUL17 NO-fade settlements (dual-source
fade tests #1–3, currently 2W–0L) to confirm or kill the R5a-respecting NO-fade half.

## 2026-07-17 22:15 UTC — nothing settled, no qualifying edge, holding 4

`agent-settle` → `settled=0 still_open=4` (MIA B96.5 / HOU B95.5 / LAX B79.5 JUL17 NO await tonight's
CLIs; PHX B97.5 JUL18 NO in flight). No strategy change — nothing settled, v6 stands. Board is now
JUL18: top model edges are all either sub-$0.30 model-side YES longshots on LIVE cells (AUS T90 @0.04,
SATX T89 @0.07 — R7 vetoes) or fades of modal/near-modal bins (LAX low B68.5 mid 0.72 — R5a). The one
live-cell dual-source NO-fade candidate, SATX high B93.5 (model 0.01 / nbm 0.22 / mid 0.46), I passed:
opening a 4th concurrent JUL18 fade before ANY of the pending JUL17 NO-fades settles would over-commit
an unproven directional lean — tonight's three CLIs are exactly the grade I'm waiting on. Want by next
session: the JUL17 NO-fade settlements to confirm or kill the R5a-respecting NO-fade half (now 2W–0L).

## 2026-07-17 21:15 UTC — nothing settled, no qualifying edge, holding 4

`agent-settle` → `settled=0 still_open=4` (MIA B96.5 / HOU B95.5 / LAX B79.5 JUL17 NO await tonight's
CLIs; PHX B97.5 JUL18 NO in flight). No strategy change — nothing settled, v6 stands. Same JUL18 board
(lead 19–22h) fully screened at 17:20/19:17/20:15; no JUL19 book open yet, so no new information.
`agent-model-view` top edges are all ≤0.07 on non-modal bins (Austin/high & SATX/high LIVE cells show
tiny model_p, i.e. no fade signal). Held at 4: still carrying heavy correlated NO-fade exposure (3
JUL17 + PHX JUL18) that grades tonight — wait for that read before adding more of the same shape.
Next session: grade the JUL17 NO-fades (MIA/HOU/LAX) once CLIs land.

## 2026-07-17 20:15 UTC — nothing settled, no qualifying edge, holding 4

`agent-settle` → `settled=0 still_open=4` (MIA B96.5 / HOU B95.5 / LAX B79.5 JUL17 NO await tonight's
CLIs; PHX B97.5 JUL18 NO in flight). No strategy change — nothing settled, v6 stands. Same JUL18 board
(lead 21–24h) I fully screened at 17:20 and 19:17; no JUL19 book open yet, so no new information. Held
at 4: already carrying heavy correlated NO-fade exposure (3 JUL17 + PHX JUL18) that grades tonight —
the disciplined move is to wait for that read (dual-source-fade tests #1–3) before adding more of the
same shape. Next session: grade the JUL17 NO-fades (MIA/HOU/LAX) once CLIs land.

## 2026-07-17 19:17 UTC — nothing settled, no qualifying edge, holding 4

`agent-settle` → `settled=0 still_open=4` (MIA B96.5 / HOU B95.5 / LAX B79.5 JUL17 NO all await
tonight's CLIs; PHX B97.5 JUL18 NO in flight). No strategy change — nothing settled, v6 stands.

Board is the same JUL18 slate (lead 22–25h) I fully screened at 17:20; no JUL19 book open yet, so no
new information since I placed PHX B97.5. Looked at one candidate I hadn't fully priced — **MIN low
JUL18 T73 NO** (model 0.01 / NBM 0.12 vs mid 0.44) — and **vetoed it at the live book (R6):** T73
(≥74°) is bid 0.44 and is the market's *top* bin (next is 72–73 at 0.39). Fading it bets the overnight
low comes in cooler than the market's warm lean, carried almost entirely by NBM (model 0.01 is
artifact-shaped, R8). That is the exact shape ATL low B72.5 lost on last cohort — "the market's warm
lean was exactly right" on a settlement-adjacent low (R5's core lesson). A NO-fade of the market's top
warm-low bin is an R5a-style trap, not a clean dual-source fade — pass. No other JUL18 bin is both
uncorrelated with my four open NO-fades and clean.

Also: this session already carries heavy NO-fade thesis exposure (3 JUL17 NO-fades settle tonight +
PHX JUL18) — the disciplined move is to wait for that read (dual-source-fade tests #1–3) before piling
on more of the same shape, not to force a 5th. Held at 4. **Next session: grade the JUL17 NO-fades
(MIA/HOU/LAX) once CLIs land — that's the real test of the v5/v6 NO-fade lean.**

`agent-settle` → `settled=0 still_open=3` (MIA B96.5 / HOU B95.5 / LAX B79.5 NO all still await
CLIs). No strategy change — nothing settled, v6 stands.

**Housekeeping note:** `git pull` is blocked this session — the operator has uncommitted EMOS
anomaly-space work in the main tree and the incoming resolve commit touches the same
`data/station_emos.parquet`. Not mine to stash. Worked from the local 14:18 snapshot (fresh vs the
12:35 board last screened), verified everything at the live book, and pushed my `data/agent/`-only
commit via a temporary worktree on `origin/main` so the operator's tree stays untouched.

**Opened: KXHIGHTPHX-26JUL18-B97.5 NO ×20 @ $0.63** (fee $0.33, cost $12.93) — v6 R2 NO-fade, the
one weak-cell trade the session allows, and **dual-source-fade live test #3** (after SFO B59.5 and
PHX B106.5 wins). Market's modal bin on PHX JUL18 high is 97–98 at ~0.40 live (bid 0.37 / ask 0.42,
verified per R6 since the snapshot was 3h stale); model_p 0.06, nbm_p 0.12 — both ≥0.25 below the
fill. My p(97–98) ≈ 0.15 → NO ≈ 0.85 vs 0.63 fill. Column is R10-clean (no model-0.95 artifact leg
in PHX high; NBM clears R2's bar alone at 0.25). Lead ~28h — a JUL18 market, so the extreme is
unobserved and R5a (settlement-day modal fades) doesn't apply. **Same honest caveat as LAX B79.5,
pre-noted:** the sources reject the bin by *straddling* it (model's mass at 99–102, NBM's at ≤96 —
NBM has 0.43 on <95 vs the market's 0.065). If the truth splits the difference it lands exactly in
my bin; two straddle-rejections are now in flight (LAX, PHX) and will grade the same lesson together.

Rest of the JUL18 board, vetoed on the usual grounds: SATX T89 / DEN T91 / DC T97 / LAX T79 / SEA
low B51.5 (model 0.6–0.95 vs NBM ≤0.02) → R8 artifact columns; DEN everything → R9; SATX low B74.5,
MIN low B68.5, SFO low B50.5, MIN high B92.5, PHX low T76 etc. → sub-$0.30 model-side YES, R7.
Near-miss NO-fades that failed a bar on NBM alone (R10 columns, so NBM must clear ≥0.15 at the live
fill by itself): SEA low B57.5 (0.13), SFO low B56.5 (0.13), SATX low T77 (0.12), DAL low T77
(0.07). LAX JUL18 B78.5 NO had clean NBM rejection (0.01 vs mid 0.32) but is the same
station/kind/direction as my open LAX JUL17 B79.5 NO — correlated, R2 bans it. PHX low B82.5 NO was
the runner-up (NBM alone 0.26 vs fill) but same city/day as the PHX high trade and R2 allows one.

Next session: the day's CLIs should land — MIA, HOU, LAX B79.5, and counterfactuals #1–#12 all grade
at once, plus the R2 death-clock moves (losses−wins at 3, dies at 5). What I want to learn: does the
NO-fade half survive its first multi-trade settlement day, and do straddle-rejections behave like
same-side rejections or like the ATL/counterfactual market-side wins?

## 2026-07-17 14:15 UTC — nothing settled, no qualifying edge, holding 3

14:15 UTC — nothing settled (MIA B96.5 NO / HOU B95.5 NO / LAX B79.5 NO all await CLIs); latest
snapshot is still the 12:35 board the 13:20 session screened in full — no new information this
hour, fast path, holding 3 positions, v6 stands.

## 2026-07-17 13:20 UTC — nothing settled; opened LAX high B79.5 NO (v6 R2 NO-fade); counterfactuals #10–#12; holding 3

`agent-settle` → `settled=0 still_open=2` (MIA B96.5 NO / HOU B95.5 NO still await CLIs). Fresh 12:35
snapshot (first new board since 11:06). No strategy change — nothing settled, v6 stands.

**Opened: KXHIGHLAX-26JUL17-B79.5 NO ×15 @ $0.69** (fee $0.23, cost $10.58) — v6 R2 NO-fade, the one
weak-cell trade the session allows. Market mid 0.325 on "LAX high exactly 79–80"; model_p 0.01 (its
mass on 81+ at 0.95), nbm_p 0.005 (its mass at/below 77). Dual-source rejection ≥0.10 each, edge 0.30
at the fill. Passes the full gauntlet: **not modal** (T80 @0.60 is the modal bin, and it drifted
TOWARD the model overnight, 0.505→0.605 — R5c confirmation); **not R10-tainted** (NBM rejects the bin
independently of the model's 81+ claim, and clears R2's bar alone); **R5b clean** (bin flat, +0.04
over 15h); high-market at 7h lead ≈ 5:40 AM Pacific, so unlike the morning-low fades the extreme is
NOT yet observed — the obs-beats-sources failure mode that killed ATL doesn't apply here yet.
**Honest caveat, logged for grading:** the two sources reject the bin by *straddling* it (model says
higher, NBM says lower) rather than agreeing where the high lands. Straddle-rejection is structurally
weaker than same-side rejection — if the truth splits the difference (marine-layer burnoff timing),
it lands exactly in my faded bin. If this loses that way, the lesson is "dual-source NO-fade requires
same-side agreement, not just dual rejection" — pre-noting it so the grade is honest either way.

**Counterfactuals #10–#12 (all R5a modal vetoes, dual-source-fade tally):**

- **#10 LAX low B68.5 NO** — model 0.08 / nbm 0.34 vs mid 0.885 (modal). Settlement-morning low with
  obs largely in — the exact ATL-loss shape; expectation is the market side wins. Would fill NO at
  1−bid = **0.19**.
- **#11 SEA low B56.5 NO** — model 0.01 / nbm 0.57 vs mid 0.745 (modal). NBM only 0.17 below and the
  model leg smells like the West-Coast artifact family. Would fill NO at 1−bid = **0.30**.
- **#12 SFO high B66.5 NO** — model 0.18 / nbm 0.19 vs mid 0.39 (modal). The most interesting of the
  three: a *high* market (extreme not yet observed) with genuine same-side dual rejection — the shape
  closest to the SFO/PHX NO-fade winners, vetoed only by modal status. Would fill NO at 1−bid =
  **0.62**. If the carve-out hypothesis is ever promoted, #12 is its cleanest test case.

Everything else on the board vetoed on the usual grounds: DEN bins → R9; sub-$0.30 model-side YES
longshots (SFO high B68.5, PHX high T96, LAX low B66.5, SEA low B52.5, PHX low B72.5/B74.5, LV
B101.5/B103.5, LV low B84.5) → R7; SFO low B50.5 and SEA low B52.5 model 0.7+/nbm 0.01 → R8; LV high
B99.5 and PHX low T77 → sources disagree, R2 dual bar fails; LV low B82.5 → 0.23/0.78 spread fails R6.

Next session: the day's CLIs start landing — the two live NO-fades (MIA, HOU), the new LAX B79.5, and
counterfactuals #1/#3/#4/#6/#7/#8/#9/#10/#11/#12 all grade at once. Biggest question on the board:
does the NO-fade half survive its first multi-trade settlement day?

## 2026-07-17 12:20 UTC — nothing settled, no qualifying edge, holding 2

12:20 UTC — nothing settled (MIA B96.5 NO / HOU B95.5 NO still await CLIs); model snapshot is
still the 11:06 one the 11:20 session already screened in full (no R2-clean entry; #8/#9
logged from it) — no new information this hour, fast path, holding 2 positions, v6 stands.

## 2026-07-17 11:20 UTC — ATL low B72.5 settled −$9.66 (wrong, predictably); v5→v6 (R2 back underwater, YES-buy restriction pre-registered); no new trade; holding 2

`agent-settle` → `settled=1 still_open=2`. **ATL low B72.5 YES ×25 @0.37 LOST −$9.66** (v3 R2
dual-source YES-buy, my p 0.45 via NBM 0.56 + climatology). The CLI: **T73 (">73°") resolved YES —
Atlanta's low came in ≥74°F**, precisely the market's 0.55 warm lean. Grade: **wrong, in the
predictable direction.** The trade was opened mid-morning of settlement day, when the overnight low
was largely observed; the market's warm price WAS the obs, and NBM+climatology were stale — the exact
shape of fade-counterfactuals #1/#3/#4/#6, now confirmed by a settled YES-buy instead of a
counterfactual. It undermines R2's YES-buy half (→ **2W–6L, −$17.35**) and supports R5's premise
(settlement-day summer-low books price real-time obs the sources don't have).

**Strategy v5 → v6.** R2 overall is back underwater: **4W–7L, net −$1.76** (kill clause: losses−wins
= 3, two net losses from death). Pre-registered per editing rule 3: **if the YES-buy half reaches 10
settled while net-negative (2 more YES-buy settlements), R2 restricts to NO-fades only.** NO-fade
half untouched (2W–1L, clean-of-R5a 2W–0L) — MIA B96.5 / HOU B95.5, both still open, are its live
test. Excluded-cities hypothesis re-marked break-even.

**Scan (11:06 snapshot, all lead 6–8h settlement-day):** no R2-clean entry. DEN bins → R9. SATX
B91.5 → counterfactual #7 stands (mid still 0.495). The morning-low boards (MIN/CHI/DAL/OKC/LAX…)
are all the stale-source shape the ATL settle just validated the market on. Two new counterfactuals:

- **#8 DAL high B95.5 NO — correlation veto (NEW bucket: tests the air-mass cap, not R5a).** model
  0.01 / nbm 0.01 vs mid 0.26 (bid 0.25/ask 0.27). Non-modal (B93.5 @0.46 is modal), no R8/R10 taint
  (no artifact T-strike in the DAL column; both sources centered 91–92). This would be an R2-clean
  NO-fade except it's a third same-day TX/Gulf hot-tail fade alongside open HOU B95.5 (same ridge).
  Would fill NO at 1−bid = **0.75**. Grade vs entry-implied 0.75 when the DAL CLI lands — if it wins
  while HOU also wins, that's another point that the correlation cap is variance control with a real
  EV cost (cf. the AUS+SATX Jul-14 note).
- **#9 OKC low B69.5 NO — R5a veto,** same morning-low shape as #1/#3/#4/#6: model 0.12 / nbm 0.25
  vs mid 0.84 (modal). Would fill NO at 1−bid = **0.20**. Logged for completeness of the dual-source-
  fade tally; expectation after ATL is that the market side wins again.

No trades opened. Next session: today's CLIs land in bulk — counterfactuals #1 (MIN), #3 (CHI),
#4 (AUS), #6 (LAX), #7 (SATX), #8 (DAL), #9 (OKC), the MIN low B72.5 R7-veto watch, and above all
the two live v5 NO-fades (MIA B96.5, HOU B95.5) — the NO-fade half's first settled test since it
became the lean.

## 2026-07-17 10:20 UTC — nothing settled, no qualifying edge; logged counterfactuals #6/#7; holding 3

`agent-settle` → `settled=0 still_open=3` (ATL low B72.5 YES, MIA high B96.5 NO, HOU high B95.5 NO —
all await today's CLIs). Fresh 09:17 snapshot this hour (the 06:59 one finally rolled). Full screen
found no R2-clean entry: the only non-modal dual-source fade candidates besides my two open ones were
**AUS high B94.5 NO** (model 0.01/nbm 0.01 vs mid 0.28 — but the model leg is R10-tainted by the AUS
T88 artifact column, NBM's AUS column is cool-shifted 90–91 like the MIA weakness, AND it would be a
third same-day TX/Gulf hot-tail fade on top of HOU+MIA — correlation veto), and the LIVE T-strikes
remain the R7/R8 artifact (AUS T88 / DEN T90 / SATX T87 at model 0.95 vs market 0.01–0.04). DEN → R9.

**Dual-source-fade counterfactual #6: LAX low B68.5 NO — R5a veto.** model 0.32 / nbm 0.34 vs live
mid 0.86 (bid 0.80/ask 0.92; snapshot mid was 0.78 — drifted further AWAY from the sources, same
overnight-obs shape as MIN #1 / CHI #3 / AUS #4). Modal bin, but no R10 taint (LAX B66.5's model 0.64
has NBM 0.30 partial support — not an R8 artifact column). Would fill NO at 1−bid = 0.20. Grade vs
entry-implied 0.20 when the CLI lands. Note the pattern accumulating: every settlement-morning LOW
counterfactual so far (#1/#3/#4/#6) had the market drifting toward the faded bin on live obs — if
these all lose, the carve-out (if any survives) likely needs the "sources not yet contradicted by
same-day obs" qualifier from #1's early read.

**Dual-source-fade counterfactual #7: SATX high B91.5 NO — R5a + R10 veto (ATL-#5 shape).** model
0.01 (tainted: derived from the R8-vetoed T87 claim) / nbm 0.18 vs live mid 0.495 (bid 0.49/ask
0.50, stable since snapshot). Modal bin; NBM alone rejects by 0.31. Would fill NO at 1−bid = 0.51.
Grade vs entry-implied 0.51 when the SATX CLI lands. Like #5, the model here FIGHTS the market's
mode (0.95 on ≤87), unlike the HOU/MIA opens where it endorsed it.

No trades, no strategy change (v5 stands — nothing settled since it was written). Next session:
today's CLIs start landing — ATL low B72.5 settles, plus counterfactuals #1 (MIN), #3 (CHI),
#4 (AUS) and the R7-veto watch (MIN low B72.5); the live MIA/HOU NO-fades grade the v5 lean itself.

## 2026-07-17 09:20 UTC — nothing settled; opened HOU high B95.5 NO (R2 NO-fade); logged counterfactual #5; holding 3

`agent-settle` → `settled=0 still_open=2` (ATL low B72.5 YES, MIA high B96.5 NO — both await today's
CLIs). Same 06:59 snapshot as the last two sessions, but this hour's screen found the one R2-clean
candidate both earlier passes missed:

**Opened: HOU high B95.5 NO ×20 @ 0.71 (cost $14.49), v5 R2 NO-fade.** My p(95–96°)≈0.10 vs market
0.295 (live-verified 09:18, bid 0.29/ask 0.30). This is the cleanest exemplar of the v5 NO-fade shape
on the whole board: BOTH sources reject the bin at ~0.01 (a ~0.28 edge at the live book vs the 0.15
bar), it is NOT the modal bin (B93.5 at 0.595 is), and there is **no R10 taint** — the model AGREES
with the market's modal bin (0.79 on B93.5 vs market 0.595), so its 0.01 on 95–96 comes from a shared
central view, not from a vetoed artifact claim. Sources reject from opposite directions (model
centered 93–94, NBM 91–92), which makes the agreement more independent, and unlike the NBM-cool-column
weakness in the MIA thesis. HOU/high is the model's best excluded cell (59%/+11.3% ROI, n=140,
production graduation watch). Cautions logged honestly: mid drifted 0.24→0.295 since 06:59 (adverse
but under R5b's 0.10 veto); book vol24h=0 (thin, though 1¢ spread); and correlation with the open MIA
B96.5 NO — both are Gulf hot-tail fades on the same day, different air masses (TX ridge vs FL
maritime), so sized small (×20 vs MIA's ×30). If both lose together to a region-wide hot surprise,
that's evidence the R1 air-mass cap should widen to a regime cap.

**Dual-source-fade counterfactual #5: ATL high B92.5 NO — R5a + R10 veto.** model 0.10 / nbm 0.01 vs
live mid 0.435 (bid 0.42/ask 0.45); it IS the modal bin (R5a), and the model's 0.10 derives from its
R7-vetoed hot claim (0.51 on T95 ">95°" vs market 0.02 — R10 laundering shape). NBM alone rejects by
0.41, which would clear R2's bar single-handed. Would fill NO at 1−bid = 0.58. Grade vs entry-implied
0.58 when the ATL CLI lands. Distinct from HOU: there the model endorses the market's mode; here it
fights it.

No strategy change (v5 stands — nothing settled since v5 was written; counterfactuals #1/#3/#4 still
in flight, #5 added). Next session: today's CLIs start landing — ATL low B72.5, MIN low (grades R7
veto + counterfactual #1), CHI/AUS lows (#3/#4), and the two live R2 NO-fades (MIA, HOU) give the
v5 lean its first real test.

## 2026-07-17 08:20 UTC — nothing settled; opened MIA high B96.5 NO (R2 NO-fade); logged counterfactuals #3/#4; holding 2

`agent-settle` → `settled=0 still_open=1`. Model-view snapshot is the SAME 06:59 file last session
reviewed, but re-screening it against v5's R2 NO-fade lean found a candidate the 07:20 blanket pass
skipped, and the live books (08:17) added real information:

**Opened: MIA high B96.5 NO ×30 @ 0.72 (cost $22.03), v5 R2 NO-fade.** My p(96–97°)≈0.08 vs market
0.28/0.30. Both sources reject the bin by ≥0.20 (model 0.08 biascorr, NBM 0.01); the fade target is
NOT the modal bin (B94.5 at 0.485 is — and the model agrees it's modal at 0.62, so no R10 taint:
model and market share the same central view, they disagree only on this hot tail). Two lessons
from this morning applied: (1) unlike the MIN low case, a Miami HIGH at 4am ET carries no
overnight-obs advantage for the market — the obs-contamination critique of stale-snapshot fades
doesn't bite here; (2) mid drifted TOWARD the sources since 06:59 (0.33→0.29), which is R5c
confirmation, not adverse drift. Clean R2 NO-fades respecting R5a were 2W–0L entering this trade.
Known weakness in the thesis: NBM's whole MIA column looks cool-shifted (≈0 on 94–97 where market
and model both put their mode), so its 0.01 may be rejecting the bin for the wrong reason; the
model's 0.08 and the T97 tail at 0.04–0.05 carry more of the weight than raw dual-agreement implies.

**Dual-source-fade counterfactual tracking (hypothesis needs ≥3 more settlements):**
- **#3 CHI low T76 NO — R5a veto.** model 0.01 / nbm 0.08 vs live mid 0.595 (moved AWAY from
  sources, 0.43→0.595 overnight — same warm-obs shape as MIN #1). Still modal. Would fill NO at
  1−bid = 0.42. Grade vs entry-implied 0.42 when CLI lands.
- **#4 AUS low T76 NO — R5a veto.** model 0.01 / nbm 0.31 vs live mid 0.70 (0.46→0.70, adverse).
  Modal. Would fill NO at 0.31. Grade vs 0.31.
- **DC low B78.5 — the other side of the coin, not a counterfactual:** at the 06:59 snapshot it was
  the modal bin at mid 0.51 with model 0.01/nbm 0.04; by 08:18 the market had CONVERGED to the
  sources (mid 0.245, B76.5 now modal). So this morning's settlement-day low books split: MIN/CHI/AUS
  obs sided with the market, DC sided with the sources. The dual-source signal is not dead on
  settlement mornings — but which side wins looks obs-driven, which is exactly R5a's argument. Passed
  on trading the residual DC edge (R2's 1-weak-cell-trade cap went to MIA, which is cleaner).

No strategy change (v5 stands — nothing settled; counterfactual evidence tracked per the
hypothesis's own instructions). Next session: ATL low B72.5 and MIN low CLIs land (grades the R7
veto + counterfactual #1), and MIA B96.5 is my first live test of the R2 NO-fade lean since v5
wrote it down.

## 2026-07-17 07:20 UTC — nothing settled; dual-source-fade counterfactual #1 logged (obs sided with the market); holding 1

`agent-settle` → `settled=0 still_open=1` (ATL low B72.5 YES still open on its CLI). JUL17 board
(snapshot 06:59, lead ~10–13h): the one candidate that cleared every screen except one rule was
**MIN low T75 ("≥76°") NO** — model 0.01 / nbm 0.03 vs mid 0.56 (live bid 0.39 / ask 0.69), both
sources ≥0.10 below the market, R2 NO-fade shape, uncorrelated. It is exactly the v5 dual-source-fade
hypothesis. But it's a settlement-day fade of the column's modal bin → **R5a bans it**, so instead of
trading it I checked the thing R5a says the market has and I don't: **live KMSP obs**. Result:
78.8°F at 01:05 CST, flat for 45+ min, LST-day min so far ≈78.8 — NO needs a 4°+ drop before
sunrise that the 1am trace argues against. The market's 0.56 is real-time-informed and looks RIGHT;
model and NBM look stale. **Logged as dual-source-fade tracked settlement #1 (counterfactual: NO
would have filled at 0.61; grade it when the CLI lands).** Early read: this is evidence FOR R5a and
against an *unconditional* dual-source carve-out — the SFO/PHX wins may need a "sources not yet
contradicted by same-day obs" qualifier if this counterfactual loses. Also: the R7-veto watch item
MIN low B72.5 YES has collapsed 0.25 → 0.20 → live ask 0.07, consistent with the warm obs — R7
looking correct again; settles today. MIN high B95.5 NO was a second, weaker dual-source-fade
near-miss (nbm 0.40 vs bid 0.53 — nbm's own modal bin IS the faded bin; not a clean exemplar, not
tracked). Rest of the board: SATX high T87 model 0.95/nbm 0.04/mid 0.04 → R8; its B91.5 NO
(nbm 0.14 vs bid 0.40, modal bin) → R10 laundering shape, passed; DEN → R9; everything else fails
R1/R2 dual-source or R7. No trades, no strategy change (v5 — hypothesis evidence tracked here per
its own instructions). Next: ATL low settlement, MIN low CLI (grades BOTH the R7 veto and
counterfactual #1 in one shot).

## 2026-07-17 00:15 UTC — nothing settled, no qualifying edge, holding 1

`agent-settle` → `settled=0 still_open=1` (ATL low B72.5 YES still open). JUL17 board unchanged
(snapshot 23:40): same R7/R8 artifact on the LIVE T-strikes. The 23:15 R7-veto (MIN low B72.5 YES)
is now ask 0.20 (was 0.25) — still sub-$0.30, veto stands, outcome still tracked. Its sibling MIN
low B74.5 NO (model 0.03 / nbm 0.48, mid 0.58) fails R2: model leg is the same cold-shifted MIN
artifact, and NBM alone is only a 0.10 edge vs the 0.15 bar — plus it's the modal bin. No trades,
no strategy change (v5). Next: ATL low settlement + the MIN low veto outcome.

## 2026-07-16 23:15 UTC — nothing settled, no qualifying edge, holding 1; logged one R7 veto

`agent-settle` → `settled=0 still_open=1` (ATL low B72.5 YES still open). JUL17 board unchanged
(snapshot 22:40): top LIVE edges still the R7/R8 broken-CDF longshot artifact (AUS T88 / DEN T90 /
SATX T87 model 0.95 vs nbm 0.12–0.30, market 0.03–0.06). **R7 veto logged for the kill-clause
count:** MIN low B72.5 YES @ ask 0.25 (model 0.73, nbm 0.47, mid 0.21) — clears R2's dual-source
letter, but it's a sub-$0.30 model-side YES (R7) and the model's board is cold/warm-shifted broken
today (MIN high B97.5 model 0.69 vs nbm 0.10 in the same city), so "both sources" leans on a broken
source. Same shape as the DC-low-@0.17 winner (NBM-driven cheap YES) — this is the carve-out watch
item; tracking the veto is the free test. If MIN low lands 72–73°F, that's one point against R7's
boundary. No trades, no strategy change (v5). Next: ATL low settlement + this veto's outcome.

## 2026-07-16 22:15 UTC — nothing settled, no qualifying edge, holding 1

`agent-settle` → `settled=0 still_open=1` (ATL low B72.5 YES still open). JUL17 board unchanged
(snapshot 21:37, 38 min old): top LIVE edges still the R7/R8 broken-CDF longshot artifact (AUS/high
T88 & SATX/high T87 model 0.95 vs nbm 0.12–0.22, market 0.04–0.08), with the downstream AUS/high
B92.5 modal-fade still confounded (R10). No qualifying edge, no strategy change (v5). Next: ATL low
settling a v3 win.

## 2026-07-16 21:15 UTC — nothing settled, no qualifying edge, holding 1

`agent-settle` → `settled=0 still_open=1` (ATL low B72.5 YES still open). JUL17 board unchanged;
model-view snapshot 48 min stale. Top LIVE edges unchanged: the R7 broken-CDF longshot artifact
(AUS/high T88, DEN/high T90, SATX/high T87 — model 0.95 on ≤87°F thresholds for ~95°F cities vs
nbm 0.22–0.24, market 0.03–0.08). Confounded, passed again per v5. No qualifying edge, no strategy
change (v5). Next: watch for ATL low B72.5 settling a v3 win.

## 2026-07-16 20:15 UTC — nothing settled, no qualifying edge, holding 1

`agent-settle` → `settled=0 still_open=1` (ATL low B72.5 YES still open). JUL17 board unchanged;
model-view snapshot 52 min stale. Top LIVE edges still the R7 broken-CDF longshot artifact
(AUS/high T88 & SATX/high T87 model 0.95 on ≤86–87°F thresholds for ~95°F Texas cities vs nbm
0.22–0.24, market 0.06). AUS/high B92.5 dual-source 0.01/0.01 modal-fade is downstream of the same
artifact, confounded — passed again. No qualifying edge, no strategy change (v5). Next: watch for
ATL low settling a v3 win and whether JUL17 books sharpen off vol24h≈0.

## 2026-07-16 19:15 UTC — nothing settled, no qualifying edge, holding 1

`agent-settle` → `settled=0 still_open=1` (ATL low B72.5 YES still open). JUL17 board unchanged;
model-view snapshot 80 min stale. Top LIVE edges still the R7 longshot artifact (AUS/DEN/SATX high
model 0.95 on ≤86–87°F thresholds vs nbm 0.22–0.24, market 0.04–0.09 — broken CDF for Texas/CO highs,
which also poisons the AUS/high B92.5=0.01 modal-fade I've passed repeatedly). No qualifying edge, no
strategy change (v5). Next: watch for ATL low settling a v3 win and whether JUL17 books sharpen off vol24h≈0.

## 2026-07-16 18:15 UTC — nothing settled, no qualifying edge, holding 1

`agent-settle` → `settled=0 still_open=1` (ATL low B72.5 YES still open). Same JUL17 board,
now lead 23–26h. Re-confirmed the top LIVE edges (AUS/high T88, DEN/high T90, SATX/high T87
all model 0.95 on a ≤87°F cool threshold) are the R7 longshot artifact — nbm 0.22–0.24, market
0.04–0.09; the model CDF is internally broken for Texas/CO highs today, which also poisons the
downstream AUS/high B92.5=0.01 read. Only dual-source "agreement" is AUS/high B92.5 (0.01/0.01
vs mid 0.45) = confounded modal-fade I've already passed twice, and both 0.01s are downstream of
the same artifact. No qualifying edge. No trades, no strategy change (v5). Next: watch for ATL
low settling a v3 win and whether the JUL17 books sharpen off vol24h≈0.

## 2026-07-16 17:15 UTC — nothing settled, no qualifying edge, holding 1

Nothing settled since 16:18 (ATL low B72.5 YES still open). Board unchanged from last hour's
deep scan — same JUL17 slate (lead ~24–27h), still vol24h≈0 pure-MM quotes. Only same-direction
dual-source instance remains AUS/high B92.5 (model 0.01 / nbm 0.01, mid ~0.40), already passed
last session as a confounded, expensive Texas-cool modal fade — no change. Strategy stays **v5**
(no version bump; nothing settled). No trades. Next session: watch whether JUL17 books sharpen
and whether ATL low settles a win for the v3 rule.

## 2026-07-16 16:18 UTC — nothing settled (ATL low still open); scanned the next-day JUL17 board; no clean edge; no strategy change; holding 1

**Settled:** `agent-settle` → `settled=0 still_open=1`. The lone open (ATL low B72.5 YES @0.37,
v3) hasn't resolved. No grading this session — nothing new to grade. Strategy stays **v5**
(rule: no version bump when nothing settled).

**Scan (had capacity, so I did the wide look).** Unlike the last several sessions, today's
board is the **next-day JUL17** slate (lead ~25–28h, closes ~37–40h out), not settlement-day
artifacts. But every book shows **vol24h = 0** — pure MM quotes, no real opinion priced in yet.
I hunted specifically for my winning half — dual-source NO-fades (both model AND nbm ≥0.10 below
an overpriced bin, same direction), the live carve-out hypothesis (2W–0L: SFO, PHX). Findings:

- **Strong LIVE cells offer only cheap YES longshots → R7 veto.** AUS/high T88 (≤87) model 0.95 /
  nbm 0.22, ask $0.07; SATX/high T87 (≤86) model 0.95 / nbm 0.24, ask $0.09. Both the exact
  sub-$0.30 model-YES shape that's 0W/5L. Vetoed. Denver strong-cell edges → R9 blacklist.
- **The "both-source 0.01" fades are mostly NOT genuine agreement.** LAX/high B79.5 (model 0.01,
  nbm 0.01, mid ~0.31): the model side is an **R8 artifact** — T80 (≥81) shows model 0.95 / nbm
  0.01. Model thinks LAX *hotter*, NBM thinks *cooler*; they merely both exclude the middle bin
  for opposite reasons. Same story DC/high B92.5 — model has DC at 100°+ (T99 model 0.66 / nbm
  0.01, R8 artifact) while NBM says <92 (0.65). Opposite reasons ≠ dual-source agreement. **R8
  veto both.**
- **Austin/high B92.5 was the one genuine same-direction agreement** (model 0.01 via ≤87, nbm
  0.01 via 90–91 — both say *cooler* than 92–93; live NO ~$0.63 on a mid-0.39 modal bin). I
  **passed**: it's a modal-bin fade in my 1W/4L NO-≥$0.50 band, and it sits on the precise
  Jul-13 Texas-high-cool lean that lost catastrophically (AUS B93.5 NO @0.66 → −$33.79). A
  confounded, expensive test that would teach little about the dual-source carve-out while
  risking $30+. The carve-out needs a *clean* test, not this one.

**Dual-source-fade watch (hypothesis, n=2 wins):** today produced **no clean instance** — the
genuinely overpriced bins (≥0.50) never had both sources clearly low (SFO/low B54.5 mid 0.82 had
nbm 0.63, still >50% in-bin — not a rejection), and the both-sources-low bins were internal
model-vs-nbm disagreement or the confounded Austin case. Sample stays at 2.

**No trades.** Want to learn by next session: whether the JUL17 books sharpen (vol > 0) closer to
close, and whether the ATL low settles a win for the v3 rule that opened it.

## 2026-07-16 15:15 UTC — SFO low B59.5 NO settled +$27.41; ledger audit corrected a big R2 miscount; strategy → v5; no new trades; holding 1

**Settled:** `agent-settle` → `settled=1 still_open=1`. **SFO low B59.5 NO @0.30 → +$27.41 WIN**
(v2, an R2 trade opened 07-14 18:17: "NBM-vs-market coastal-low disagreement, live-book verified").
The SF low was not in 59–60; both model (0.01) and NBM (0.41) sat far below the market's 0.735.
Right for the right reason — a dual-source fade of an overpriced bin.

**Grading + the learning event of the session — an R2 audit.** SFO being an R2 win nagged at me
because v4 had R2 written as "1W–5L, one net loss from death." So I queried the ledger directly
(every settled thesis citing R2). The result: **R2 is 4W–6L, net +$7.90 — net-positive, not
dying.** Prior sessions had miscounted for two versions: they credited only MIA Jul-13 as R2's
lone win and filed DC low (+$32.80, Jul-15), PHX (+$10.81, Jul-15), and SFO (+$27.41, now) —
all R2-cited theses — under other rules or as "R5a counterexamples." The death-clock had drifted
badly from the ledger; v4's clock would have **killed a +EV rule on its next loss.** This is
exactly what the grading step exists to catch, and it's a lesson about my own bookkeeping:
recompute the kill-clause from the parquet, don't carry it forward by hand.

**The real signal is directional.** Splitting R2 by side:
- **NO-fade half** (sell overpriced bin, both sources ≥0.10 below market): **2W–1L, +$15.59** —
  SFO (+27.41), PHX (+10.81); the lone loss SEA B80.5 @0.63 was a modal-bin fade R5a bans anyway.
- **YES-buy half** (buy underpriced weak-cell bin): **2W–5L, −$7.69** — MIA/DC won; SEA/BOS/DAL/
  MIA-Jul15/NYC lost. Dual-model agreement does not reliably rescue this half.

**Strategy → v5.** Corrected R2's record to ledger truth (4W–6L, +$7.90; net −2, three losses
from death — not one) and gave it an operational lean toward NO-fades of overpriced bins that
respect R5a. Logged SFO as an R5a counterexample (faded a 0.735 modal bin, won on dual-source
rejection) and registered a new hypothesis — "dual-source-confirmed fades beat R5a" (n=2 wins:
SFO, PHX) — without touching R5a's bar (n too small; need ≥3 more). Weakened the "exclusion is
wisdom" read since R2's excluded-cell PnL is net-positive. No rule *bars* changed.

**Scan / trades:** none. The 07-16 board is again entirely settlement-day (all lead 6h): every
model edge is a West-Coast artifact column — LAX T86 (0.95/0.01), SFO low B52.5 (0.79/0.01), LV
high B109.5 (0.75/0.01), SEA low B55.5 (0.51/0.01) — all R8; the model YES longshots (LV low
B86.5 @0.10 on the 32%-win worst cell, SEA high B69.5 @0.15) are sub-$0.30 → R7. The strong LIVE
cells (SATX/AUS/DEN high) show no edge (model=market). `agent-scan` confirms no farther-out
liquid weather books — all JUL16, closing 14–17h. No qualifying entry. Holding 1 (ATL low B72.5,
my one R3/own-reasoning open — settles next).

**Next session:** watch for the JUL16 CLIs so ATL low B72.5 settles (my first own-reasoning data
point), and log any new dual-source fade toward the R5a carve-out test.

## 2026-07-16 14:15 UTC — nothing settled, no qualifying edge, holding 2 positions

`agent-settle` → settled=0, still_open=2 (SFO low B59.5, ATL low B72.5 — both awaiting
CLI). No grading, strategy stays v4. Board is again entirely settlement-day (all lead_h=6,
JUL16): every big edge is a model-only artifact NBM contradicts — LAX T86 (0.95/0.01),
SFO low B52.5 (0.79/0.01), LV high B109.5 (0.75/0.01), SEA/SFO 0.51/0.01 — all R8 vetoes.
LV low B86.5 (0.64/0.36 @ ask 0.10) is a sub-$0.30 model YES (R7) on the ledger's worst
cell (32% win, −14.3% ROI). Strong LIVE cells (SATX/AUS/DEN high) show no edge, model=market.
LAX low B68.5 has dual agreement (0.94/0.88) but market already at mid 0.88 — no room. R5
lead-floor caution covers the whole 6h board anyway. No trades. Next session: still waiting
on JUL16 CLIs to grade the 2 open — ATL low B72.5 is my first R3/own-reasoning settle.

## 2026-07-16 13:15 UTC — nothing settled, no qualifying edge, holding 2 positions

`agent-settle` → settled=0, still_open=2 (SFO low B59.5, ATL low B72.5 — both JUL15/16
awaiting CLI). No grading, strategy stays v4. Model-view board is entirely settlement-day
(all lead_h=6, JUL16): every qualifying edge trips a veto — LAX T86 (0.95/0.01) and SFO
low B52.5 (0.79/0.01) are R8 single-source artifacts; LV low B86.5 (0.64/0.36 @ ask 0.10)
is a sub-$0.30 model YES (R7) on a 32%-win/−14.3%-ROI cell; the strong LIVE cells (SATX/AUS
high) show no edge at all, model=market. R5 lead-floor caution applies to the whole 6h board.
R2 is one net loss from death so I won't spend it on a weak-cell dual-agreement play. No trades.
Next session: watching for JUL16 CLIs to post so I can finally grade the 2 open (ATL low B72.5
is the one v3 trade in the book — its settle is my first R3/own-reasoning data point).

## 2026-07-16 12:15 UTC — nothing settled, no qualifying edge, holding 2 positions

Quiet session. `agent-settle` → settled=0, still_open=2. No grading (nothing new
resolved), strategy stays v4. Scanned model-view: LIVE board unchanged from 11:16 —
DEN/SATX/AUS bottom T-strikes at model 0.95 / NBM ≤0.22, $0.01–0.05 (R7+R8+R9 veto);
NO complements on modal bins (R5a+R10). Best weak-cell edge NOLA high B91.5 model 0.68
@ ask 0.13 = sub-$0.30 model YES → R7 veto, and R2 is one net loss from death regardless.
No trades. Next session: watching for the JUL16 book to settle so I can grade the 2 open.

## 2026-07-16 11:16 UTC — 6 settled (3W/3L, +$13.76); v2 validated net-positive; strategy → v4; no new trades; holding 2

**Settled (finally — the JUL15 book posted CLIs):** `agent-settle` → `settled=6 still_open=2`.
All six were v2 trades, and as a cohort they went **3W/3L for +$13.76** — the first
net-positive cohort in the ledger. This is the learning event I've been waiting on across the
last several quiet sessions.

**Grading each:**
- **SATX high T81 YES @0.71 → +13.77 WIN.** Strong cell (97%), expensive model-side YES. Right
  for the right reason — the R1+R7 sweet spot (proven cell, price ≥$0.50).
- **DC low B72.5 YES @0.17 → +32.80 WIN.** The cohort's biggest winner, and a sub-$0.30 YES. A
  naive R7 reading would have vetoed it — but R7 is scoped to *model-driven* YES, and this was
  driven by NBM + my own 0.45 estimate on a weak model cell (DC/low −4.5% ROI). Out of scope, so
  R7 stays clean *within* its scope; logged as an honest caveat and a thing to watch (do cheap
  NBM/own-reasoning YES entries deserve a carve-out? n=1, far too early).
- **PHX high B106.5 NO @0.55 → +10.81 WIN.** Both sources p~0.15 vs mid 0.47. If 0.47 was the
  modal bin this is an R5a counterexample — but one win doesn't dent R5a's Jul-13 evidence (modal
  hit *exactly* 3×). Logged, not acted on.
- **MIA high B92.5 YES @0.33 → −15.55 LOSS.** R2 dual-agreement on an excluded cell (MIA high
  46%). Third straight production-excluded dual-agreement loss → R2 now **1W–5L, net −4, one net
  loss from death.** "Exclusion is wisdom" keeps winning.
- **NOLA low B74.5 YES @0.38 → −23.79 LOSS.** An R1-qualifying cell (NOLA/low 74%) whose fill
  still lost — the cell record is a prior, not a promise, exactly as v2 demoted it. Small-n noise
  vs signal is unclear; watch R1's realized record.
- **NYC high B101.5 YES @0.02 → −4.28 LOSS.** R7's pre-registered free test resolved exactly as
  predicted — a sub-$0.30 (indeed sub-$0.05) longshot YES lost.

**Strategy change → v4:** No rules added or removed. Bumped because two rules' evidence/state
changed: R2's kill-count (→1W–5L) and R7 (free test resolved + DC caveat). The headline is that
**v2 is validated** — 6 settled, 50% win, +13.6% ROI, versus v1's 27% / −42.5%. The sign flip
tracks precisely the rules v2 introduced (R5 market respect, R6 live-book discipline); they stay.

**Scan / no trades:** JUL16 LIVE board is the same artifact shape as the last week — DEN T89 /
SATX T83 / AUS T84 at model 0.95 vs NBM ≤0.22, prices $0.03–0.08 (R7+R8 veto; DEN also R9), and
their NO complements sit on the market's modal bins B93.5/B88.5/B85.5 (R5a+R10 veto). Weak-cell
NBM signals (DAL T88 model 0.40/NBM 0.69/mid 0.30; HOU high B89.5) are marginal and route through
a dying R2 — feeding R2 the very cities (DAL) that have been losing it is bad judgment. **Zero
qualifying edges; opened nothing. Holding 2** (SFO low B59.5 NO, ATL low B72.5 YES — ATL settles
today and is R2-adjacent context).

**Next session:** ATL low B72.5 and SFO low B59.5 should settle — watch whether the ATL/low YES
(my own-reasoning trade) confirms or joins the weak-cell loss pile, and whether R2 finally dies.

## 2026-07-16 10:16 UTC — nothing settled, no qualifying edge; NOLA high R2 checked live and vetoed; holding 8

`agent-settle` → `settled=0 still_open=8`; JUL15 book + ATL JUL16 still open, no CLI yet, **no
grading, v3 stands.** Fresher 09:29 snapshot flipped one thing vs the last few sessions: NOLA
high B91.5 now shows dual agreement (model 0.69 / NBM 0.34 / mid 0.235, both above), where prior
stale boards had the two sources straddling the mid. Verified the live book (bid 0.23 / ask 0.24,
20h to close). **Vetoed on R2's correlation clause** — I already hold NOLA low B74.5 YES, so a
NOLA high YES is same-city/same-day/same-air-mass correlated. Independently weak on merits: NBM
only +0.105 over mid (barely clears the 0.10 bar), NOLA/high cell is 63%/−2.3% (n=140), and it's
a bet the high lands *below* the market's modal bin B93.5 @0.50 — the exact "model says cooler
than the market's mode" shape that lost in DEN/AUS/SEA on Jul-13, with R2 already 1W–4L (one net
loss from death). Everything else re-derives as before: SATX T83 / AUS T84 / LAX T86 artifact
columns → R7+R8; DEN → R9; DC low B77.5 @0.12 and HOU low B75.5 @0.06 → R7 longshot floor; CHI
low B74.5 NBM only +0.01 → fails R2; ATL low B72.5 already held → duplicate guard. Nothing new
clears the bar. **Next:** JUL15 book + ATL JUL16 (R2 decider) should post CLI soon — that's the
learning event.

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
