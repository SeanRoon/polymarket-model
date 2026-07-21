# Agent paper-trading performance

_Generated 2026-07-21 10:15 UTC by `polymarket agent-report`. PAPER ONLY. See `strategy.md` for the playbook and `journal.md` for reasoning._

## Bankroll

| metric | value |
|:-------|------:|
| starting bankroll | $1000.00 |
| free cash | $855.52 |
| open positions | 3 ($74.09 at risk) |
| settled | 28 (13 wins, 46%) |
| realized PnL | $-70.39 on $535.39 staked (-13.1%) |

## By strategy version

| version | n | wins | win_rate | staked$ | pnl$ | roi |
|:--------|--:|-----:|---------:|--------:|-----:|----:|
| v1 | 15 | 4 | 27% | 339.36 | -144.36 | -42.5% |
| v2 | 7 | 4 | 57% | 113.83 | +41.17 | +36.2% |
| v3 | 1 | 0 | 0% | 9.66 | -9.66 | -100.0% |
| v5 | 2 | 2 | 100% | 36.52 | +13.48 | +36.9% |
| v6 | 2 | 2 | 100% | 23.51 | +11.49 | +48.9% |
| v7 | 1 | 1 | 100% | 12.51 | +17.49 | +139.8% |
| v8 | 0 | 0 | - | 0.00 | +0.00 | - |

## By category

| category | n | wins | win_rate | staked$ | pnl$ | roi |
|:---------|--:|-----:|---------:|--------:|-----:|----:|
| Climate and Weather | 28 | 13 | 46% | 535.39 | -70.39 | -13.1% |

## Open positions

| opened | ticker | side | count | entry$ | cost$ | strategy | thesis |
|:-------|:-------|:-----|------:|-------:|------:|:---------|:-------|
| 07-19 16:35 | KXHIGHTHOU-26JUL20-B97.5 | no | 60 | 0.58 | 35.83 | v8 | R2/R1 NO-fade, dual-source SAME-direction: market has 0.42 on HOU high 97-98 (mo |
| 07-19 16:35 | KXHIGHTPHX-26JUL20-B104.5 | no | 45 | 0.54 | 25.09 | v8 | R2 NO-fade, dual-source rejection from opposite sides (same shape as the PHX JUL |
| 07-19 18:34 | KXLOWTMIA-26JUL20-B80.5 | yes | 35 | 0.36 | 13.17 | v8 | R2 YES-buy, cautious size, opened as a DISCRIMINATING test of the pre-registered |

## Last 20 settled

| settled | ticker | side | entry$ | pnl$ | strategy | thesis |
|:--------|:-------|:-----|-------:|-----:|:---------|:-------|
| 07-20 | KXLOWTNYC-26JUL19-B69.5 | no | 0.40 | +17.49 | v7 | v7 R2 NO-fade of an overpriced NON-modal bin (the shape that just went 3W-0L on  |
| 07-19 | KXHIGHTPHX-26JUL18-B97.5 | no | 0.63 | +7.07 | v6 | R2 NO-fade (v6 operational lean, dual-source-fade live test #3 after SFO B59.5 a |
| 07-19 | KXHIGHMIA-26JUL17-B96.5 | no | 0.72 | +7.97 | v5 | R2 NO-fade (v5 lean): fade MIA high 96-97 bin. My p(yes)~0.08 vs market implied  |
| 07-19 | KXHIGHTHOU-26JUL17-B95.5 | no | 0.71 | +5.51 | v5 | p(HOU high 95-96)~0.10 vs market 0.295 (NO fills 0.71, live-verified 09:18). v5  |
| 07-19 | KXHIGHLAX-26JUL17-B79.5 | no | 0.69 | +4.42 | v6 | v6 R2 NO-fade of overpriced non-modal bin: market mid 0.325 on LAX high 79-80 ex |
| 07-17 | KXLOWTATL-26JUL16-B72.5 | yes | 0.37 | -9.66 | v3 | My p(ATL low 72-73F Jul16) ~0.45 vs live ask 0.37 (implied 0.37). Sources: NBM 0 |
| 07-16 | KXLOWTSFO-26JUL15-B59.5 | no | 0.30 | +27.41 | v2 | p(SF low 59-60) ~0.41 by NBM, ~0.01 by model+biascorr, vs live mid 0.735 - both  |
| 07-16 | KXHIGHTSATX-26JUL15-T81 | yes | 0.71 | +13.77 | v2 | P(SATX high <=80F Jul15) ~0.70 vs market 0.55. Model+biascorr 0.95 on the system |
| 07-16 | KXLOWTDC-26JUL15-B72.5 | yes | 0.17 | +32.80 | v2 | P(DC low 72-73F Jul15) ~0.45 vs live ask 0.17 (verified via agent-scan this minu |
| 07-16 | KXHIGHMIA-26JUL15-B92.5 | yes | 0.33 | -15.55 | v2 | p~0.50: model+biascorr 0.56 and NBM 0.44 both >=0.10 over live mid 0.325 (book v |
| 07-16 | KXLOWTNOLA-26JUL15-B74.5 | yes | 0.38 | -23.79 | v2 | p~0.55 (blend: model+biascorr 0.68 on an R1-qualifying cell — NOLA/low 73% win,  |
| 07-16 | KXHIGHTPHX-26JUL15-B106.5 | no | 0.55 | +10.81 | v2 | p(PHX high in 106-107) ~0.15: NBM 0.19 and model 0.08 vs market 0.47 mid - both  |
| 07-16 | KXHIGHNY-26JUL15-B101.5 | yes | 0.02 | -4.28 | v2 | My p~0.12 vs market 0.02: NBM says 0.25 for NYC high 101-102 and only 0.16 for < |
| 07-15 | KXHIGHDEN-26JUL14-T93 | yes | 0.10 | -15.95 | v1 | P(DEN high <=92F Jul14) ~0.90: model+biascorr 0.95 AND NBM 0.70 both far above m |
| 07-15 | KXHIGHAUS-26JUL14-T85 | yes | 0.55 | +25.96 | v1 | P(AUS high <=84F Jul14) ~0.80: model+biascorr 0.95, NBM 0.45, market 0.53. Austi |
| 07-15 | KXHIGHTSATX-26JUL14-T85 | yes | 0.57 | +20.64 | v1 | P(SATX high <=84F Jul14) ~0.80: model+biascorr 0.95, NBM 0.38, market 0.53. San  |
| 07-15 | KXHIGHDEN-26JUL14-B95.5 | no | 0.59 | -24.28 | v1 | My P(DEN high 95-96F Jul14) ~0.10 vs market 0.41 (NO costs ~0.59). Both models e |
| 07-15 | KXHIGHTBOS-26JUL14-B94.5 | yes | 0.34 | -17.79 | v1 | My est P(BOS high 94-95F Jul14) ~0.40 vs market 0.20 ask. Dual-model agreement a |
| 07-15 | KXHIGHTDAL-26JUL14-T88 | yes | 0.28 | -11.77 | v1 | My p~0.75 (model_p 0.68 + NBM 0.90 both far above market; NBM confirmation makes |
| 07-14 | KXHIGHDEN-26JUL13-T93 | yes | 0.07 | -11.19 | v1 | Model 0.95 that Denver high stays <=92F Jul13 vs market 0.05; NBM disagrees (0.1 |
