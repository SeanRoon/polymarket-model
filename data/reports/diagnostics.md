# Model diagnostics

_Generated 2026-06-25 15:40 UTC. Deterministic flags from `polymarket diagnose`; see `model-watch.md` for the agent's interpretation._

**58 flag(s):** 1 critical, 1 warn, 1 good, 55 info

| severity | code | dimension | detail | suggestion |
|:---------|:-----|:----------|:-------|:-----------|
| critical | exclude_candidate | Chicago (KMDW) | Model worse than market and losing: Brier 0.148 vs 0.079 (gap +0.069), PnL -1.86 over n=9162. | Consider adding KMDW to signal_excluded_stations until calibration improves. |
| warn | regression_wow | Miami / high | Brier worsened 0.105 -> 0.125 (+0.020) over the last 7d vs the prior 7d. | Check `git log` for changes landing in this window; inspect recent forecasts vs resolutions. |
| good | reenable_candidate | San Antonio (KSAT) | Excluded station now matches/beats market: model Brier 0.111 <= market 0.119 over n=1140. | Consider removing KSAT from signal_excluded_stations. |
| info | exclusion_holds | Atlanta (KATL) | Still miscalibrated: model Brier 0.208 vs market 0.073 (gap +0.135) over n=894. | Keep KATL excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Boston (KBOS) | Still miscalibrated: model Brier 0.107 vs market 0.043 (gap +0.065) over n=882. | Keep KBOS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Dallas (KDFW) | Still miscalibrated: model Brier 0.136 vs market 0.075 (gap +0.061) over n=930. | Keep KDFW excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Houston (KHOU) | Still miscalibrated: model Brier 0.143 vs market 0.062 (gap +0.081) over n=1002. | Keep KHOU excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Las Vegas (KLAS) | Still miscalibrated: model Brier 0.193 vs market 0.041 (gap +0.152) over n=1086. | Keep KLAS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Los Angeles (KLAX) | Still miscalibrated: model Brier 0.233 vs market 0.066 (gap +0.167) over n=5178. | Keep KLAX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Miami (KMIA) | Still miscalibrated: model Brier 0.169 vs market 0.059 (gap +0.110) over n=3852. | Keep KMIA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Minneapolis (KMSP) | Still miscalibrated: model Brier 0.179 vs market 0.065 (gap +0.113) over n=1044. | Keep KMSP excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New Orleans (KMSY) | Still miscalibrated: model Brier 0.197 vs market 0.072 (gap +0.125) over n=1020. | Keep KMSY excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New York City (KNYC) | Still miscalibrated: model Brier 0.170 vs market 0.071 (gap +0.098) over n=4440. | Keep KNYC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Oklahoma City (KOKC) | Still miscalibrated: model Brier 0.137 vs market 0.068 (gap +0.069) over n=1026. | Keep KOKC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Phoenix (KPHX) | Still miscalibrated: model Brier 0.114 vs market 0.064 (gap +0.050) over n=1062. | Keep KPHX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | San Francisco (KSFO) | Still miscalibrated: model Brier 0.180 vs market 0.080 (gap +0.100) over n=1074. | Keep KSFO excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Seattle (KSEA) | Still miscalibrated: model Brier 0.161 vs market 0.090 (gap +0.071) over n=1104. | Keep KSEA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Washington DC (KDCA) | Still miscalibrated: model Brier 0.141 vs market 0.076 (gap +0.065) over n=912. | Keep KDCA excluded; revisit after Phase 3 calibration. |
| info | nbm_beats_ecmwf | Atlanta / high / 0-6h | NBM lower Brier 0.163 vs ECMWF 0.221 (gap 0.058) over n=138. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / high / 6-24h | NBM lower Brier 0.154 vs ECMWF 0.202 (gap 0.049) over n=192. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / low / 0-6h | NBM lower Brier 0.066 vs ECMWF 0.229 (gap 0.163) over n=156. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / low / 6-24h | NBM lower Brier 0.084 vs ECMWF 0.210 (gap 0.126) over n=228. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 0-6h | NBM lower Brier 0.062 vs ECMWF 0.109 (gap 0.046) over n=156. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / high / 0-6h | NBM lower Brier 0.130 vs ECMWF 0.166 (gap 0.036) over n=1524. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / high / 0-6h | NBM lower Brier 0.095 vs ECMWF 0.117 (gap 0.022) over n=132. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Dallas / low / 0-6h | NBM lower Brier 0.133 vs ECMWF 0.168 (gap 0.036) over n=138. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Denver / low / 6-24h | NBM lower Brier 0.194 vs ECMWF 0.218 (gap 0.024) over n=234. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / high / 0-6h | NBM lower Brier 0.090 vs ECMWF 0.133 (gap 0.043) over n=276. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 0-6h | NBM lower Brier 0.109 vs ECMWF 0.217 (gap 0.109) over n=120. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 6-24h | NBM lower Brier 0.112 vs ECMWF 0.219 (gap 0.107) over n=198. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / high / 0-6h | NBM lower Brier 0.111 vs ECMWF 0.189 (gap 0.077) over n=264. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / high / 6-24h | NBM lower Brier 0.120 vs ECMWF 0.167 (gap 0.047) over n=198. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 0-6h | NBM lower Brier 0.114 vs ECMWF 0.205 (gap 0.090) over n=216. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 6-24h | NBM lower Brier 0.107 vs ECMWF 0.236 (gap 0.129) over n=210. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / high / 0-6h | NBM lower Brier 0.161 vs ECMWF 0.194 (gap 0.032) over n=270. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / high / 6-24h | NBM lower Brier 0.148 vs ECMWF 0.199 (gap 0.051) over n=204. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / low / 0-6h | NBM lower Brier 0.080 vs ECMWF 0.174 (gap 0.094) over n=132. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / low / 6-24h | NBM lower Brier 0.097 vs ECMWF 0.131 (gap 0.034) over n=204. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New Orleans / high / 0-6h | NBM lower Brier 0.141 vs ECMWF 0.204 (gap 0.063) over n=264. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New Orleans / high / 6-24h | NBM lower Brier 0.142 vs ECMWF 0.230 (gap 0.088) over n=210. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New Orleans / low / 0-6h | NBM lower Brier 0.150 vs ECMWF 0.172 (gap 0.021) over n=144. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New Orleans / low / 6-24h | NBM lower Brier 0.132 vs ECMWF 0.183 (gap 0.051) over n=174. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 0-6h | NBM lower Brier 0.125 vs ECMWF 0.190 (gap 0.065) over n=1542. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 24-72h | NBM lower Brier 0.123 vs ECMWF 0.184 (gap 0.061) over n=252. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 6-24h | NBM lower Brier 0.125 vs ECMWF 0.181 (gap 0.056) over n=1428. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Oklahoma City / low / 0-6h | NBM lower Brier 0.145 vs ECMWF 0.206 (gap 0.061) over n=144. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / high / 0-6h | NBM lower Brier 0.094 vs ECMWF 0.150 (gap 0.056) over n=282. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 0-6h | NBM lower Brier 0.073 vs ECMWF 0.101 (gap 0.028) over n=132. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / low / 6-24h | NBM lower Brier 0.075 vs ECMWF 0.098 (gap 0.024) over n=198. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 0-6h | NBM lower Brier 0.098 vs ECMWF 0.246 (gap 0.147) over n=156. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 6-24h | NBM lower Brier 0.114 vs ECMWF 0.238 (gap 0.123) over n=204. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / high / 0-6h | NBM lower Brier 0.163 vs ECMWF 0.204 (gap 0.042) over n=252. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / high / 6-24h | NBM lower Brier 0.150 vs ECMWF 0.224 (gap 0.073) over n=210. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 0-6h | NBM lower Brier 0.087 vs ECMWF 0.133 (gap 0.046) over n=222. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 6-24h | NBM lower Brier 0.094 vs ECMWF 0.138 (gap 0.043) over n=198. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / high / 0-6h | NBM lower Brier 0.118 vs ECMWF 0.167 (gap 0.049) over n=270. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / high / 6-24h | NBM lower Brier 0.128 vs ECMWF 0.151 (gap 0.023) over n=216. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 0-6h | NBM lower Brier 0.143 vs ECMWF 0.183 (gap 0.041) over n=228. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
