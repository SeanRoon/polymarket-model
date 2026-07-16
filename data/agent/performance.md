# Agent paper-trading performance

_Generated 2026-07-16 05:15 UTC by `polymarket agent-report`. PAPER ONLY. See `strategy.md` for the playbook and `journal.md` for reasoning._

## Bankroll

| metric | value |
|:-------|------:|
| starting bankroll | $1000.00 |
| free cash | $732.15 |
| open positions | 8 ($123.49 at risk) |
| settled | 15 (4 wins, 27%) |
| realized PnL | $-144.36 on $339.36 staked (-42.5%) |

## By strategy version

| version | n | wins | win_rate | staked$ | pnl$ | roi |
|:--------|--:|-----:|---------:|--------:|-----:|----:|
| v1 | 15 | 4 | 27% | 339.36 | -144.36 | -42.5% |
| v2 | 0 | 0 | - | 0.00 | +0.00 | - |
| v3 | 0 | 0 | - | 0.00 | +0.00 | - |

## By category

| category | n | wins | win_rate | staked$ | pnl$ | roi |
|:---------|--:|-----:|---------:|--------:|-----:|----:|
| Climate and Weather | 15 | 4 | 27% | 339.36 | -144.36 | -42.5% |

## Open positions

| opened | ticker | side | count | entry$ | cost$ | strategy | thesis |
|:-------|:-------|:-----|------:|-------:|------:|:---------|:-------|
| 07-14 14:18 | KXHIGHTSATX-26JUL15-T81 | yes | 50 | 0.71 | 36.23 | v2 | P(SATX high <=80F Jul15) ~0.70 vs market 0.55. Model+biascorr 0.95 on the system |
| 07-14 14:19 | KXLOWTDC-26JUL15-B72.5 | yes | 40 | 0.17 | 7.20 | v2 | P(DC low 72-73F Jul15) ~0.45 vs live ask 0.17 (verified via agent-scan this minu |
| 07-14 16:16 | KXHIGHMIA-26JUL15-B92.5 | yes | 45 | 0.33 | 15.55 | v2 | p~0.50: model+biascorr 0.56 and NBM 0.44 both >=0.10 over live mid 0.325 (book v |
| 07-14 18:17 | KXLOWTSFO-26JUL15-B59.5 | no | 40 | 0.30 | 12.59 | v2 | p(SF low 59-60) ~0.41 by NBM, ~0.01 by model+biascorr, vs live mid 0.735 - both  |
| 07-14 19:19 | KXLOWTNOLA-26JUL15-B74.5 | yes | 60 | 0.38 | 23.79 | v2 | p~0.55 (blend: model+biascorr 0.68 on an R1-qualifying cell — NOLA/low 73% win,  |
| 07-15 00:19 | KXHIGHTPHX-26JUL15-B106.5 | no | 25 | 0.55 | 14.19 | v2 | p(PHX high in 106-107) ~0.15: NBM 0.19 and model 0.08 vs market 0.47 mid - both  |
| 07-15 06:18 | KXHIGHNY-26JUL15-B101.5 | yes | 200 | 0.02 | 4.28 | v2 | My p~0.12 vs market 0.02: NBM says 0.25 for NYC high 101-102 and only 0.16 for < |
| 07-16 04:17 | KXLOWTATL-26JUL16-B72.5 | yes | 25 | 0.37 | 9.66 | v3 | My p(ATL low 72-73F Jul16) ~0.45 vs live ask 0.37 (implied 0.37). Sources: NBM 0 |

## Last 20 settled

| settled | ticker | side | entry$ | pnl$ | strategy | thesis |
|:--------|:-------|:-----|-------:|-----:|:---------|:-------|
| 07-15 | KXHIGHDEN-26JUL14-T93 | yes | 0.10 | -15.95 | v1 | P(DEN high <=92F Jul14) ~0.90: model+biascorr 0.95 AND NBM 0.70 both far above m |
| 07-15 | KXHIGHAUS-26JUL14-T85 | yes | 0.55 | +25.96 | v1 | P(AUS high <=84F Jul14) ~0.80: model+biascorr 0.95, NBM 0.45, market 0.53. Austi |
| 07-15 | KXHIGHTSATX-26JUL14-T85 | yes | 0.57 | +20.64 | v1 | P(SATX high <=84F Jul14) ~0.80: model+biascorr 0.95, NBM 0.38, market 0.53. San  |
| 07-15 | KXHIGHDEN-26JUL14-B95.5 | no | 0.59 | -24.28 | v1 | My P(DEN high 95-96F Jul14) ~0.10 vs market 0.41 (NO costs ~0.59). Both models e |
| 07-15 | KXHIGHTBOS-26JUL14-B94.5 | yes | 0.34 | -17.79 | v1 | My est P(BOS high 94-95F Jul14) ~0.40 vs market 0.20 ask. Dual-model agreement a |
| 07-15 | KXHIGHTDAL-26JUL14-T88 | yes | 0.28 | -11.77 | v1 | My p~0.75 (model_p 0.68 + NBM 0.90 both far above market; NBM confirmation makes |
| 07-14 | KXHIGHDEN-26JUL13-T93 | yes | 0.07 | -11.19 | v1 | Model 0.95 that Denver high stays <=92F Jul13 vs market 0.05; NBM disagrees (0.1 |
| 07-14 | KXHIGHAUS-26JUL13-T89 | yes | 0.17 | -17.99 | v1 | Model 0.95 + NBM 0.64 both above market 0.21 that Austin high stays <=88F Jul13. |
| 07-14 | KXHIGHTSATX-26JUL13-T90 | yes | 0.34 | -35.58 | v1 | Model 0.95 + NBM 0.54 vs market 0.30 that San Antonio high stays <=89F Jul13. Be |
| 07-14 | KXHIGHMIA-26JUL13-B92.5 | yes | 0.32 | +19.94 | v1 | Both models above market on Miami high 92-93F Jul13: model 0.66, NBM 0.45, mid 0 |
| 07-14 | KXHIGHDEN-26JUL13-B97.5 | no | 0.50 | -31.05 | v1 | Fade market's modal bin. Market implies P(97-98)=0.50; ensemble+biascorr says 0. |
| 07-14 | KXHIGHAUS-26JUL13-B93.5 | no | 0.66 | -33.79 | v1 | Fade market's modal-adjacent bin. Market implies P(93-94)=0.345; ensemble+biasco |
| 07-14 | KXHIGHTSATX-26JUL13-B92.5 | no | 0.58 | +22.16 | v1 | Fade market's modal bin. Market implies P(92-93)=0.44; ensemble+biascorr 0.01, N |
| 07-14 | KXHIGHTSEA-26JUL13-B76.5 | yes | 0.13 | -11.04 | v1 | My est ~0.50 vs market 0.13 ask. Corrected ECMWF 0.77 AND NBM 0.49 both put Seat |
| 07-14 | KXHIGHTSEA-26JUL13-B80.5 | no | 0.63 | -22.63 | v1 | My P(SEA high 80-81F Jul13) ~0.05 vs market implied 0.37 (NO costs 0.64). Both m |
