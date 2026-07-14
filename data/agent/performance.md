# Agent paper-trading performance

_Generated 2026-07-14 01:15 UTC by `polymarket agent-report`. PAPER ONLY. See `strategy.md` for the playbook and `journal.md` for reasoning._

## Bankroll

| metric | value |
|:-------|------:|
| starting bankroll | $1000.00 |
| free cash | $672.41 |
| open positions | 14 ($327.59 at risk) |
| settled | 0 (0 wins, -) |
| realized PnL | $+0.00 on $0.00 staked (-) |

## By strategy version

| version | n | wins | win_rate | staked$ | pnl$ | roi |
|:--------|--:|-----:|---------:|--------:|-----:|----:|
| v1 | 0 | 0 | - | 0.00 | +0.00 | - |

## By category

| category | n | wins | win_rate | staked$ | pnl$ | roi |
|:---------|--:|-----:|---------:|--------:|-----:|----:|
| Climate and Weather | 0 | 0 | - | 0.00 | +0.00 | - |

## Open positions

| opened | ticker | side | count | entry$ | cost$ | strategy | thesis |
|:-------|:-------|:-----|------:|-------:|------:|:---------|:-------|
| 07-12 23:44 | KXHIGHDEN-26JUL13-T93 | yes | 150 | 0.07 | 11.19 | v1 | Model 0.95 that Denver high stays <=92F Jul13 vs market 0.05; NBM disagrees (0.1 |
| 07-12 23:44 | KXHIGHAUS-26JUL13-T89 | yes | 100 | 0.17 | 17.99 | v1 | Model 0.95 + NBM 0.64 both above market 0.21 that Austin high stays <=88F Jul13. |
| 07-12 23:44 | KXHIGHTSATX-26JUL13-T90 | yes | 100 | 0.34 | 35.58 | v1 | Model 0.95 + NBM 0.54 vs market 0.30 that San Antonio high stays <=89F Jul13. Be |
| 07-12 23:44 | KXHIGHMIA-26JUL13-B92.5 | yes | 30 | 0.32 | 10.06 | v1 | Both models above market on Miami high 92-93F Jul13: model 0.66, NBM 0.45, mid 0 |
| 07-13 13:05 | KXHIGHDEN-26JUL13-B97.5 | no | 60 | 0.50 | 31.05 | v1 | Fade market's modal bin. Market implies P(97-98)=0.50; ensemble+biascorr says 0. |
| 07-13 13:05 | KXHIGHAUS-26JUL13-B93.5 | no | 50 | 0.66 | 33.79 | v1 | Fade market's modal-adjacent bin. Market implies P(93-94)=0.345; ensemble+biasco |
| 07-13 13:06 | KXHIGHTSATX-26JUL13-B92.5 | no | 55 | 0.58 | 32.84 | v1 | Fade market's modal bin. Market implies P(92-93)=0.44; ensemble+biascorr 0.01, N |
| 07-13 13:16 | KXHIGHTSEA-26JUL13-B76.5 | yes | 80 | 0.13 | 11.04 | v1 | My est ~0.50 vs market 0.13 ask. Corrected ECMWF 0.77 AND NBM 0.49 both put Seat |
| 07-13 14:17 | KXHIGHTSEA-26JUL13-B80.5 | no | 35 | 0.63 | 22.63 | v1 | My P(SEA high 80-81F Jul13) ~0.05 vs market implied 0.37 (NO costs 0.64). Both m |
| 07-13 16:17 | KXHIGHDEN-26JUL14-T93 | yes | 150 | 0.10 | 15.95 | v1 | P(DEN high <=92F Jul14) ~0.90: model+biascorr 0.95 AND NBM 0.70 both far above m |
| 07-13 16:17 | KXHIGHAUS-26JUL14-T85 | yes | 60 | 0.55 | 34.04 | v1 | P(AUS high <=84F Jul14) ~0.80: model+biascorr 0.95, NBM 0.45, market 0.53. Austi |
| 07-13 16:17 | KXHIGHTSATX-26JUL14-T85 | yes | 50 | 0.57 | 29.36 | v1 | P(SATX high <=84F Jul14) ~0.80: model+biascorr 0.95, NBM 0.38, market 0.53. San  |
| 07-13 18:18 | KXHIGHDEN-26JUL14-B95.5 | no | 40 | 0.59 | 24.28 | v1 | My P(DEN high 95-96F Jul14) ~0.10 vs market 0.41 (NO costs ~0.59). Both models e |
| 07-13 18:18 | KXHIGHTBOS-26JUL14-B94.5 | yes | 50 | 0.34 | 17.79 | v1 | My est P(BOS high 94-95F Jul14) ~0.40 vs market 0.20 ask. Dual-model agreement a |

## Last 20 settled

| settled | ticker | side | entry$ | pnl$ | strategy | thesis |
|:--------|:-------|:-----|-------:|-----:|:---------|:-------|
