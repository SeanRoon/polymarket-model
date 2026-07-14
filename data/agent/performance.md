# Agent paper-trading performance

_Generated 2026-07-14 18:15 UTC by `polymarket agent-report`. PAPER ONLY. See `strategy.md` for the playbook and `journal.md` for reasoning._

## Bankroll

| metric | value |
|:-------|------:|
| starting bankroll | $1000.00 |
| free cash | $686.66 |
| open positions | 9 ($192.17 at risk) |
| settled | 9 (2 wins, 22%) |
| realized PnL | $-121.17 on $206.17 staked (-58.8%) |

## By strategy version

| version | n | wins | win_rate | staked$ | pnl$ | roi |
|:--------|--:|-----:|---------:|--------:|-----:|----:|
| v1 | 9 | 2 | 22% | 206.17 | -121.17 | -58.8% |
| v2 | 0 | 0 | - | 0.00 | +0.00 | - |

## By category

| category | n | wins | win_rate | staked$ | pnl$ | roi |
|:---------|--:|-----:|---------:|--------:|-----:|----:|
| Climate and Weather | 9 | 2 | 22% | 206.17 | -121.17 | -58.8% |

## Open positions

| opened | ticker | side | count | entry$ | cost$ | strategy | thesis |
|:-------|:-------|:-----|------:|-------:|------:|:---------|:-------|
| 07-13 16:17 | KXHIGHDEN-26JUL14-T93 | yes | 150 | 0.10 | 15.95 | v1 | P(DEN high <=92F Jul14) ~0.90: model+biascorr 0.95 AND NBM 0.70 both far above m |
| 07-13 16:17 | KXHIGHAUS-26JUL14-T85 | yes | 60 | 0.55 | 34.04 | v1 | P(AUS high <=84F Jul14) ~0.80: model+biascorr 0.95, NBM 0.45, market 0.53. Austi |
| 07-13 16:17 | KXHIGHTSATX-26JUL14-T85 | yes | 50 | 0.57 | 29.36 | v1 | P(SATX high <=84F Jul14) ~0.80: model+biascorr 0.95, NBM 0.38, market 0.53. San  |
| 07-13 18:18 | KXHIGHDEN-26JUL14-B95.5 | no | 40 | 0.59 | 24.28 | v1 | My P(DEN high 95-96F Jul14) ~0.10 vs market 0.41 (NO costs ~0.59). Both models e |
| 07-13 18:18 | KXHIGHTBOS-26JUL14-B94.5 | yes | 50 | 0.34 | 17.79 | v1 | My est P(BOS high 94-95F Jul14) ~0.40 vs market 0.20 ask. Dual-model agreement a |
| 07-14 09:16 | KXHIGHTDAL-26JUL14-T88 | yes | 40 | 0.28 | 11.77 | v1 | My p~0.75 (model_p 0.68 + NBM 0.90 both far above market; NBM confirmation makes |
| 07-14 14:18 | KXHIGHTSATX-26JUL15-T81 | yes | 50 | 0.71 | 36.23 | v2 | P(SATX high <=80F Jul15) ~0.70 vs market 0.55. Model+biascorr 0.95 on the system |
| 07-14 14:19 | KXLOWTDC-26JUL15-B72.5 | yes | 40 | 0.17 | 7.20 | v2 | P(DC low 72-73F Jul15) ~0.45 vs live ask 0.17 (verified via agent-scan this minu |
| 07-14 16:16 | KXHIGHMIA-26JUL15-B92.5 | yes | 45 | 0.33 | 15.55 | v2 | p~0.50: model+biascorr 0.56 and NBM 0.44 both >=0.10 over live mid 0.325 (book v |

## Last 20 settled

| settled | ticker | side | entry$ | pnl$ | strategy | thesis |
|:--------|:-------|:-----|-------:|-----:|:---------|:-------|
| 07-14 | KXHIGHDEN-26JUL13-T93 | yes | 0.07 | -11.19 | v1 | Model 0.95 that Denver high stays <=92F Jul13 vs market 0.05; NBM disagrees (0.1 |
| 07-14 | KXHIGHAUS-26JUL13-T89 | yes | 0.17 | -17.99 | v1 | Model 0.95 + NBM 0.64 both above market 0.21 that Austin high stays <=88F Jul13. |
| 07-14 | KXHIGHTSATX-26JUL13-T90 | yes | 0.34 | -35.58 | v1 | Model 0.95 + NBM 0.54 vs market 0.30 that San Antonio high stays <=89F Jul13. Be |
| 07-14 | KXHIGHMIA-26JUL13-B92.5 | yes | 0.32 | +19.94 | v1 | Both models above market on Miami high 92-93F Jul13: model 0.66, NBM 0.45, mid 0 |
| 07-14 | KXHIGHDEN-26JUL13-B97.5 | no | 0.50 | -31.05 | v1 | Fade market's modal bin. Market implies P(97-98)=0.50; ensemble+biascorr says 0. |
| 07-14 | KXHIGHAUS-26JUL13-B93.5 | no | 0.66 | -33.79 | v1 | Fade market's modal-adjacent bin. Market implies P(93-94)=0.345; ensemble+biasco |
| 07-14 | KXHIGHTSATX-26JUL13-B92.5 | no | 0.58 | +22.16 | v1 | Fade market's modal bin. Market implies P(92-93)=0.44; ensemble+biascorr 0.01, N |
| 07-14 | KXHIGHTSEA-26JUL13-B76.5 | yes | 0.13 | -11.04 | v1 | My est ~0.50 vs market 0.13 ask. Corrected ECMWF 0.77 AND NBM 0.49 both put Seat |
| 07-14 | KXHIGHTSEA-26JUL13-B80.5 | no | 0.63 | -22.63 | v1 | My P(SEA high 80-81F Jul13) ~0.05 vs market implied 0.37 (NO costs 0.64). Both m |
