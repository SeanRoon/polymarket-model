# Model diagnostics

_Generated 2026-06-23 15:49 UTC. Deterministic flags from `polymarket diagnose`; see `model-watch.md` for the agent's interpretation._

**47 flag(s):** 1 critical, 46 info

| severity | code | dimension | detail | suggestion |
|:---------|:-----|:----------|:-------|:-----------|
| critical | exclude_candidate | Chicago (KMDW) | Model worse than market and losing: Brier 0.147 vs 0.079 (gap +0.068), PnL -0.15 over n=8844. | Consider adding KMDW to signal_excluded_stations until calibration improves. |
| info | exclusion_holds | Atlanta (KATL) | Still miscalibrated: model Brier 0.226 vs market 0.061 (gap +0.165) over n=588. | Keep KATL excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Boston (KBOS) | Still miscalibrated: model Brier 0.081 vs market 0.040 (gap +0.041) over n=582. | Keep KBOS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Dallas (KDFW) | Still miscalibrated: model Brier 0.111 vs market 0.083 (gap +0.028) over n=612. | Keep KDFW excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Houston (KHOU) | Still miscalibrated: model Brier 0.138 vs market 0.070 (gap +0.068) over n=660. | Keep KHOU excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Las Vegas (KLAS) | Still miscalibrated: model Brier 0.213 vs market 0.029 (gap +0.184) over n=708. | Keep KLAS excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Los Angeles (KLAX) | Still miscalibrated: model Brier 0.235 vs market 0.066 (gap +0.169) over n=4854. | Keep KLAX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Miami (KMIA) | Still miscalibrated: model Brier 0.171 vs market 0.059 (gap +0.113) over n=3726. | Keep KMIA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Minneapolis (KMSP) | Still miscalibrated: model Brier 0.172 vs market 0.057 (gap +0.115) over n=684. | Keep KMSP excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New Orleans (KMSY) | Still miscalibrated: model Brier 0.213 vs market 0.081 (gap +0.132) over n=666. | Keep KMSY excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | New York City (KNYC) | Still miscalibrated: model Brier 0.169 vs market 0.072 (gap +0.097) over n=4308. | Keep KNYC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Oklahoma City (KOKC) | Still miscalibrated: model Brier 0.146 vs market 0.078 (gap +0.068) over n=660. | Keep KOKC excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Phoenix (KPHX) | Still miscalibrated: model Brier 0.107 vs market 0.049 (gap +0.058) over n=696. | Keep KPHX excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | San Antonio (KSAT) | Still miscalibrated: model Brier 0.114 vs market 0.101 (gap +0.013) over n=786. | Keep KSAT excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | San Francisco (KSFO) | Still miscalibrated: model Brier 0.194 vs market 0.087 (gap +0.107) over n=720. | Keep KSFO excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Seattle (KSEA) | Still miscalibrated: model Brier 0.163 vs market 0.079 (gap +0.083) over n=726. | Keep KSEA excluded; revisit after Phase 3 calibration. |
| info | exclusion_holds | Washington DC (KDCA) | Still miscalibrated: model Brier 0.133 vs market 0.079 (gap +0.054) over n=588. | Keep KDCA excluded; revisit after Phase 3 calibration. |
| info | nbm_beats_ecmwf | Atlanta / high / 0-6h | NBM lower Brier 0.169 vs ECMWF 0.247 (gap 0.077) over n=102. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / high / 6-24h | NBM lower Brier 0.155 vs ECMWF 0.209 (gap 0.054) over n=120. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / low / 0-6h | NBM lower Brier 0.046 vs ECMWF 0.247 (gap 0.202) over n=102. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Atlanta / low / 6-24h | NBM lower Brier 0.055 vs ECMWF 0.229 (gap 0.173) over n=150. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Boston / low / 0-6h | NBM lower Brier 0.027 vs ECMWF 0.062 (gap 0.034) over n=102. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Chicago / high / 0-6h | NBM lower Brier 0.132 vs ECMWF 0.169 (gap 0.036) over n=1458. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / high / 0-6h | NBM lower Brier 0.087 vs ECMWF 0.133 (gap 0.046) over n=180. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Houston / low / 6-24h | NBM lower Brier 0.139 vs ECMWF 0.182 (gap 0.043) over n=138. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / high / 0-6h | NBM lower Brier 0.111 vs ECMWF 0.224 (gap 0.114) over n=180. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / high / 6-24h | NBM lower Brier 0.118 vs ECMWF 0.205 (gap 0.087) over n=126. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 0-6h | NBM lower Brier 0.113 vs ECMWF 0.220 (gap 0.107) over n=144. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Las Vegas / low / 6-24h | NBM lower Brier 0.094 vs ECMWF 0.239 (gap 0.146) over n=132. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Los Angeles / low / 0-6h | NBM lower Brier 0.086 vs ECMWF 0.125 (gap 0.039) over n=114. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / high / 0-6h | NBM lower Brier 0.135 vs ECMWF 0.211 (gap 0.076) over n=180. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Minneapolis / high / 6-24h | NBM lower Brier 0.118 vs ECMWF 0.219 (gap 0.101) over n=126. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New Orleans / high / 0-6h | NBM lower Brier 0.152 vs ECMWF 0.228 (gap 0.076) over n=168. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New Orleans / high / 6-24h | NBM lower Brier 0.140 vs ECMWF 0.269 (gap 0.129) over n=138. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 0-6h | NBM lower Brier 0.127 vs ECMWF 0.191 (gap 0.063) over n=1488. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 24-72h | NBM lower Brier 0.124 vs ECMWF 0.181 (gap 0.057) over n=240. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | New York City / high / 6-24h | NBM lower Brier 0.127 vs ECMWF 0.181 (gap 0.053) over n=1362. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Phoenix / high / 0-6h | NBM lower Brier 0.104 vs ECMWF 0.179 (gap 0.075) over n=192. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 0-6h | NBM lower Brier 0.108 vs ECMWF 0.232 (gap 0.124) over n=108. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Antonio / low / 6-24h | NBM lower Brier 0.120 vs ECMWF 0.236 (gap 0.116) over n=156. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / high / 0-6h | NBM lower Brier 0.166 vs ECMWF 0.213 (gap 0.047) over n=174. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / high / 6-24h | NBM lower Brier 0.159 vs ECMWF 0.219 (gap 0.060) over n=138. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 0-6h | NBM lower Brier 0.093 vs ECMWF 0.162 (gap 0.069) over n=150. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | San Francisco / low / 6-24h | NBM lower Brier 0.115 vs ECMWF 0.176 (gap 0.061) over n=132. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / high / 0-6h | NBM lower Brier 0.106 vs ECMWF 0.148 (gap 0.042) over n=186. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / high / 6-24h | NBM lower Brier 0.110 vs ECMWF 0.147 (gap 0.037) over n=138. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
| info | nbm_beats_ecmwf | Seattle / low / 0-6h | NBM lower Brier 0.142 vs ECMWF 0.199 (gap 0.056) over n=156. | Consider weighting toward NBM for this cell, or an ECMWF/NBM blend. |
