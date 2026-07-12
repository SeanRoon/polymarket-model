"""Read-only HTTP client for Kalshi's public market-data endpoints.

No authentication required for /series, /events, /markets, /markets/{ticker}/orderbook.
Production base: https://api.elections.kalshi.com/trade-api/v2 — Kalshi has consolidated
their formerly-separate "elections" and "trading" hosts onto this single host.
"""
from __future__ import annotations

from typing import Any

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from polymarket_model.config import settings
from polymarket_model.logging_setup import get_logger

log = get_logger(__name__)

_RETRYABLE = retry_if_exception_type((httpx.HTTPError, httpx.TimeoutException))
_WAIT = wait_exponential(multiplier=0.5, min=0.5, max=8.0)


class KalshiClient:
    """Read-only client for Kalshi public market data."""

    def __init__(self, base_url: str | None = None) -> None:
        self._base_url = base_url or settings.kalshi_base_url

    def _client(self) -> httpx.Client:
        return httpx.Client(
            base_url=self._base_url,
            timeout=settings.http_timeout_seconds,
            headers={"User-Agent": settings.http_user_agent, "Accept": "application/json"},
        )

    @retry(retry=_RETRYABLE, wait=_WAIT, stop=stop_after_attempt(settings.http_max_retries), reraise=True)
    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        with self._client() as c:
            r = c.get(path, params=params)
            if r.status_code == 404:
                return None
            r.raise_for_status()
            return r.json()

    def get_series(self, series_ticker: str) -> dict[str, Any] | None:
        data = self._get(f"/series/{series_ticker}")
        if not data:
            return None
        return data.get("series", data)

    def list_open_events(self, series_ticker: str, *, limit: int = 100) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        cursor: str | None = None
        while True:
            params: dict[str, Any] = {
                "series_ticker": series_ticker,
                "status": "open",
                "limit": limit,
            }
            if cursor:
                params["cursor"] = cursor
            data = self._get("/events", params=params) or {}
            page = data.get("events") or []
            out.extend(page)
            cursor = data.get("cursor")
            if not cursor or not page:
                break
        return out

    def list_event_markets(self, event_ticker: str, *, limit: int = 200) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        cursor: str | None = None
        while True:
            params: dict[str, Any] = {
                "event_ticker": event_ticker,
                "status": "open",
                "limit": limit,
            }
            if cursor:
                params["cursor"] = cursor
            data = self._get("/markets", params=params) or {}
            page = data.get("markets") or []
            out.extend(page)
            cursor = data.get("cursor")
            if not cursor or not page:
                break
        return out

    def get_orderbook(self, market_ticker: str, *, depth: int = 5) -> dict[str, Any] | None:
        data = self._get(f"/markets/{market_ticker}/orderbook", params={"depth": depth})
        if not data:
            return None
        return data.get("orderbook_fp", data)

    def get_market(self, market_ticker: str) -> dict[str, Any] | None:
        """Single market record — includes status and, once settled, result."""
        data = self._get(f"/markets/{market_ticker}")
        if not data:
            return None
        return data.get("market", data)

    def get_event(self, event_ticker: str) -> dict[str, Any] | None:
        """Single event record — carries the category the market record lacks."""
        data = self._get(f"/events/{event_ticker}")
        if not data:
            return None
        return data.get("event", data)

    def list_all_open_events(
        self, *, limit: int = 200, with_nested_markets: bool = True, max_pages: int = 50
    ) -> list[dict[str, Any]]:
        """Every open event on Kalshi (all series), optionally with markets nested.

        Used by the self-directed paper agent's whole-venue scan; the weather
        pipeline keeps using the per-series `list_open_events`.
        """
        out: list[dict[str, Any]] = []
        cursor: str | None = None
        for _ in range(max_pages):
            params: dict[str, Any] = {"status": "open", "limit": limit}
            if with_nested_markets:
                params["with_nested_markets"] = "true"
            if cursor:
                params["cursor"] = cursor
            data = self._get("/events", params=params) or {}
            page = data.get("events") or []
            out.extend(page)
            cursor = data.get("cursor")
            if not cursor or not page:
                break
        return out
