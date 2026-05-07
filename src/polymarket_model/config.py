from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    polymarket_gamma_base_url: str = "https://gamma-api.polymarket.com"
    polymarket_clob_base_url: str = "https://clob.polymarket.com"
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
    sum_of_mids_low: float = 0.97
    sum_of_mids_high: float = 1.04
    outside_bin_mass_max: float = 0.02
    max_lead_days_for_signal: int = 7

    @property
    def cache_db_path(self) -> Path:
        return self.data_dir / self.cache_db_filename

    @property
    def reports_dir(self) -> Path:
        return self.data_dir / self.reports_dirname


settings = Settings()
