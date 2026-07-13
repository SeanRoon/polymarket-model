from __future__ import annotations

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# Stations whose model is currently miscalibrated badly enough that emitting
# signals would lose money in expectation. Revisit when their recent Brier
# (per `polymarket compare-to-resolved`) is at or below the market's.
DEFAULT_SIGNAL_EXCLUDED_STATIONS: frozenset[str] = frozenset({
    "KLAX", "KMIA", "KNYC",
    # Cities added 2026-06-18 for DATA COLLECTION ONLY. Excluded from live signals
    # until they have ~30d of paired (model_p, resolution) data, a bias estimate, and
    # a validated model. Exclusion blocks live trading but NOT snapshot recording, so
    # model_p + prices still accrue. Re-enable per-cell as each proves out.
    # KSAT graduated 2026-07-06: /high re-enabled after 11+ weeks at 94%+ win rate and
    # +31-43% ROI in paper; /low stays dark via DEFAULT_SIGNAL_EXCLUDED_CELLS below.
    "KATL", "KBOS", "KDFW", "KDCA", "KHOU", "KLAS", "KMSP", "KMSY",
    "KOKC", "KPHX", "KSEA", "KSFO",
})


# Stations whose bin probabilities get an isotonic recalibration pass (fit by
# `polymarket compute-calibration`, applied by the recorder as a recorded `calibrated_p`
# column). Phase 3 pilot scope: the marine stations KLAX/KMIA, which are over-confident
# despite small temperature bias (see `calibration/isotonic.py`). Calibration is recorded
# but does NOT drive live signals yet — the column accrues out-of-sample evidence to
# justify re-enabling those stations. `kind` granularity lives in the fit, not here.
DEFAULT_CALIBRATION_STATIONS: frozenset[str] = frozenset({"KLAX", "KMIA"})


# Finer-grained exclusion than `DEFAULT_SIGNAL_EXCLUDED_STATIONS`: drop signals for a
# single (station_id, kind) cell while keeping the station's other book live. Needed
# because a whole-station exclude is too blunt where high and low diverge — e.g. Chicago
# (KMDW) /high is a persistent loser (cum eval PnL ~-9, negative paper ROI) but /low is
# profitable, so excluding KMDW would discard the good book. See data/reports/model-watch.md.
# `kind` is lowercase 'high' | 'low'. A station listed here AND in the station set above is
# redundant (the station exclude already covers both kinds).
DEFAULT_SIGNAL_EXCLUDED_CELLS: frozenset[tuple[str, str]] = frozenset({
    # Chicago: /high is a persistent loser (above); /low was profitable for weeks but its
    # paper ROI decayed to negative on three consecutive reads (2026-06-27 -0.33% ->
    # 06-28 -0.73% -> 06-29 -0.95%), so the model edge itself is gone — excluded 2026-06-29.
    # Both kinds now excluded => Chicago is fully dark; live cells are Austin/high + Denver/high.
    ("KMDW", "high"), ("KMDW", "low"),
    # New low books on existing live-traded high cities (Austin, Denver) — collect
    # data without trading them until validated; the station's high book stays live.
    ("KAUS", "low"), ("KDEN", "low"),
    # San Antonio: /high graduated to live 2026-07-06 (see station set above), but /low
    # has been a consistent paper loser the whole time (~45% win, ~-18% ROI per-bin) —
    # keep it excluded so only the proven high book trades.
    ("KSAT", "low"),
})


def _coerce_cell(item: object) -> tuple[str, str]:
    """Normalize one excluded-cell entry to (station_id, kind_lower).

    Accepts either a (station, kind) pair (list/tuple) or a 'STATION:kind' string.
    """
    if isinstance(item, str):
        station, sep, kind = item.partition(":")
        if not sep:
            raise ValueError(f"excluded cell {item!r} must be 'STATION:kind'")
        return station.strip(), kind.strip().lower()
    if isinstance(item, (list, tuple)) and len(item) == 2:
        station, kind = item
        return str(station).strip(), str(kind).strip().lower()
    raise ValueError(f"excluded cell {item!r} must be 'STATION:kind' or a (station, kind) pair")


# Per-(station, kind) weight on the NBM probabilistic forecast when blended with the ECMWF
# ensemble empirical CDF:  blended_p = (1 - w) * ecmwf_p + w * nbm_p.  Cells absent here use
# `nbm_blend_default_weight` (0.0 = pure ECMWF, i.e. unchanged behavior). NBM has beaten
# ECMWF across all three lead buckets on Chicago/high (KMDW) and NYC/high (KNYC) for weeks
# (see data/reports/model-watch.md — "the single highest-leverage Phase 3 deliverable"); a
# 50/50 blend captures that edge while halving reliance on either source alone. Data-fit
# optimal weights are deferred to the isotonic-calibration workstream. `kind` is lowercase.
DEFAULT_NBM_BLEND_WEIGHTS: dict[tuple[str, str], float] = {
    ("KMDW", "high"): 0.5,
    ("KNYC", "high"): 0.5,
    # Low books where NBM dominates the ECMWF ensemble (added 2026-07-13, from
    # data/reports/evaluation.md): overnight minima are a persistent ECMWF weakness —
    # NBM Brier at 6-24h is ~half ECMWF's or better on all four cells, and on
    # Houston/Boston lows NBM alone beats the MARKET at 24-72h leads. All four are
    # signal-excluded (station or cell), so this only upgrades the recorded
    # model_p/paper track toward the model we'd actually promote. 0.7 not 0.5: the
    # NYC/high experience showed 50/50 underweights NBM where it clearly dominates
    # (blend 0.13 vs pure NBM 0.11 at 6-24h).
    ("KHOU", "low"): 0.7,
    ("KBOS", "low"): 0.7,
    ("KSAT", "low"): 0.7,
    ("KPHX", "low"): 0.7,
    # OKC/high: NBM ≈ market Brier (0.105 vs 0.107 at 6-24h) with the best simulated
    # NBM PnL of the new highs; gap to ECMWF is smaller than the lows', so 50/50.
    ("KOKC", "high"): 0.5,
}


def _coerce_blend_weights(v: object) -> dict[tuple[str, str], float]:
    """Normalize blend-weight config to {(station, kind_lower): weight}.

    Accepts a dict (keys = (station, kind) pairs or 'STATION:kind' strings), or an env-style
    string of comma-separated 'STATION:kind:weight' entries, e.g. "KMDW:high:0.5,KNYC:high:0.6".
    """
    if v is None or v == "":
        return {}
    out: dict[tuple[str, str], float] = {}
    if isinstance(v, str):
        for entry in v.split(","):
            entry = entry.strip()
            if not entry:
                continue
            station, _, rest = entry.partition(":")
            kind, sep, weight = rest.partition(":")
            if not sep:
                raise ValueError(f"blend weight {entry!r} must be 'STATION:kind:weight'")
            out[(station.strip(), kind.strip().lower())] = float(weight)
        return out
    if isinstance(v, dict):
        for k, weight in v.items():
            out[_coerce_cell(k)] = float(weight)
        return out
    raise TypeError(f"nbm_blend_weights: unsupported type {type(v)!r}")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    kalshi_base_url: str = "https://api.elections.kalshi.com/trade-api/v2"
    open_meteo_base_url: str = "https://ensemble-api.open-meteo.com/v1"
    nws_base_url: str = "https://api.weather.gov"

    http_user_agent: str = "polymarket-model/0.1 (rooneysw@gmail.com)"
    http_timeout_seconds: float = 30.0
    http_max_retries: int = 4

    data_dir: Path = Field(default=PROJECT_ROOT / "data")
    cache_db_filename: str = "cache.duckdb"
    reports_dirname: str = "reports"

    log_level: str = "INFO"
    log_json: bool = False

    min_edge: float = 0.02
    kelly_fraction: float = 0.25
    fee_assumption: float = 0.02
    sum_of_mids_low: float = 0.95
    sum_of_mids_high: float = 1.08
    outside_bin_mass_max: float = 0.02
    max_lead_days_for_signal: int = 7

    signal_excluded_stations: frozenset[str] = Field(
        default_factory=lambda: DEFAULT_SIGNAL_EXCLUDED_STATIONS,
    )

    # Stations to isotonic-recalibrate. Env override is comma-separated station ids,
    # e.g. CALIBRATION_STATIONS="KLAX,KMIA". Empty string disables calibration entirely.
    calibration_stations: frozenset[str] = Field(
        default_factory=lambda: DEFAULT_CALIBRATION_STATIONS,
    )

    # Per-(station, kind) exclusions. Env override format is comma-separated
    # 'STATION:kind' pairs, e.g. SIGNAL_EXCLUDED_CELLS="KMDW:high,KORD:low".
    signal_excluded_cells: frozenset[tuple[str, str]] = Field(
        default_factory=lambda: DEFAULT_SIGNAL_EXCLUDED_CELLS,
    )

    # ECMWF/NBM blend. `nbm_blend_weights` overrides the per-cell NBM weight; cells absent
    # fall back to `nbm_blend_default_weight`. Env override for the map is comma-separated
    # 'STATION:kind:weight', e.g. NBM_BLEND_WEIGHTS="KMDW:high:0.5,KNYC:high:0.6".
    nbm_blend_default_weight: float = 0.0
    nbm_blend_weights: dict[tuple[str, str], float] = Field(
        default_factory=lambda: dict(DEFAULT_NBM_BLEND_WEIGHTS),
    )

    # Kalshi authenticated-API creds. `kalshi_api_key_id` is always required; for the
    # private key supply EITHER the PEM contents directly (recommended — paste into .env
    # between double quotes, multiline OK) OR a path to a PEM file on disk. Inline wins
    # if both are set. The repo's .gitignore covers .env and *.pem.
    kalshi_api_key_id: str | None = None
    kalshi_private_key_pem: str | None = None
    kalshi_private_key_path: Path | None = None

    @field_validator("signal_excluded_stations", mode="before")
    @classmethod
    def _parse_excluded_stations(cls, v: object) -> frozenset[str]:
        if v is None or v == "":
            return frozenset()
        if isinstance(v, str):
            return frozenset(s.strip() for s in v.split(",") if s.strip())
        if isinstance(v, (list, tuple, set, frozenset)):
            return frozenset(str(s) for s in v)
        raise TypeError(f"signal_excluded_stations: unsupported type {type(v)!r}")

    @field_validator("calibration_stations", mode="before")
    @classmethod
    def _parse_calibration_stations(cls, v: object) -> frozenset[str]:
        if v is None or v == "":
            return frozenset()
        if isinstance(v, str):
            return frozenset(s.strip() for s in v.split(",") if s.strip())
        if isinstance(v, (list, tuple, set, frozenset)):
            return frozenset(str(s) for s in v)
        raise TypeError(f"calibration_stations: unsupported type {type(v)!r}")

    @field_validator("signal_excluded_cells", mode="before")
    @classmethod
    def _parse_excluded_cells(cls, v: object) -> frozenset[tuple[str, str]]:
        if v is None or v == "":
            return frozenset()
        if isinstance(v, str):
            return frozenset(_coerce_cell(s) for s in v.split(",") if s.strip())
        if isinstance(v, (list, tuple, set, frozenset)):
            return frozenset(_coerce_cell(s) for s in v)
        raise TypeError(f"signal_excluded_cells: unsupported type {type(v)!r}")

    @field_validator("nbm_blend_weights", mode="before")
    @classmethod
    def _parse_blend_weights(cls, v: object) -> dict[tuple[str, str], float]:
        return _coerce_blend_weights(v)

    def nbm_blend_weight_for(self, station_id: str | None, kind: str | None) -> float:
        """NBM blend weight for a cell, falling back to the global default.

        Returns 0.0 (pure ECMWF) for any cell not listed when the default is unchanged.
        """
        if not station_id or not kind:
            return self.nbm_blend_default_weight
        return self.nbm_blend_weights.get(
            (station_id, kind.lower()), self.nbm_blend_default_weight
        )

    @property
    def cache_db_path(self) -> Path:
        return self.data_dir / self.cache_db_filename

    @property
    def reports_dir(self) -> Path:
        return self.data_dir / self.reports_dirname


settings = Settings()
