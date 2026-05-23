from __future__ import annotations

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]


# Stations whose model is currently miscalibrated badly enough that emitting
# signals would lose money in expectation. Revisit when their recent Brier
# (per `polymarket compare-to-resolved`) is at or below the market's.
DEFAULT_SIGNAL_EXCLUDED_STATIONS: frozenset[str] = frozenset({"KLAX", "KMIA"})


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

    # Kalshi authenticated-API creds. Both must be set to use `polymarket exec` commands.
    # The private key file must be the RSA PEM Kalshi gave you when you created the API
    # key in the dashboard. Store it outside the repo (.gitignore already covers *.pem).
    kalshi_api_key_id: str | None = None
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

    @property
    def cache_db_path(self) -> Path:
        return self.data_dir / self.cache_db_filename

    @property
    def reports_dir(self) -> Path:
        return self.data_dir / self.reports_dirname


settings = Settings()
