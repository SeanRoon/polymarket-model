"""Read-only authenticated client for Kalshi's `/portfolio/*` endpoints.

This client deliberately exposes ONLY GET methods. Order placement, cancellation,
and any other mutating operation belongs in a separate (private) repo, behind
hard kill-switches and per-tick confirmations — none of which exist here yet.

The base URL and retry/backoff behavior mirror `markets.client.KalshiClient`;
the difference is that every request runs through `KalshiAuth.headers()` to
attach the signed RSA-PSS headers Kalshi requires for portfolio endpoints.
"""
from __future__ import annotations

from typing import Any
from urllib.parse import urlsplit

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from polymarket_model.config import settings
from polymarket_model.execution.auth import KalshiAuth
from polymarket_model.logging_setup import get_logger

log = get_logger(__name__)

_RETRYABLE = retry_if_exception_type((httpx.HTTPError, httpx.TimeoutException))
_WAIT = wait_exponential(multiplier=0.5, min=0.5, max=8.0)


def _path_for_signing(base_url: str, path: str) -> str:
    """Return the path-only string Kalshi expects in the signed message.

    Kalshi signs `timestamp + METHOD + path`, where `path` includes the API
    version prefix (e.g. `/trade-api/v2/portfolio/balance`) and excludes any
    query string. httpx's `base_url` already contains that prefix, so we
    combine the URL components manually rather than letting httpx do it.
    """
    base_path = urlsplit(base_url).path.rstrip("/")
    return base_path + path


class KalshiAuthedClient:
    """Read-only authenticated client. GET methods only — no order placement."""

    def __init__(
        self,
        auth: KalshiAuth | None = None,
        base_url: str | None = None,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._auth = auth or KalshiAuth.from_settings()
        self._base_url = base_url or settings.kalshi_base_url
        self._transport = transport

    def _client(self) -> httpx.Client:
        kwargs: dict[str, Any] = {
            "base_url": self._base_url,
            "timeout": settings.http_timeout_seconds,
            "headers": {"User-Agent": settings.http_user_agent, "Accept": "application/json"},
        }
        if self._transport is not None:
            kwargs["transport"] = self._transport
        return httpx.Client(**kwargs)

    @retry(retry=_RETRYABLE, wait=_WAIT, stop=stop_after_attempt(settings.http_max_retries), reraise=True)
    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        signed_path = _path_for_signing(self._base_url, path)
        headers = self._auth.headers(method="GET", path=signed_path)
        with self._client() as c:
            r = c.get(path, params=params, headers=headers)
            if r.status_code == 404:
                return None
            r.raise_for_status()
            return r.json()

    def get_balance(self) -> dict[str, Any] | None:
        return self._get("/portfolio/balance")

    def get_positions(self, *, limit: int = 200) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        cursor: str | None = None
        while True:
            params: dict[str, Any] = {"limit": limit}
            if cursor:
                params["cursor"] = cursor
            data = self._get("/portfolio/positions", params=params) or {}
            page = data.get("market_positions") or []
            out.extend(page)
            cursor = data.get("cursor")
            if not cursor or not page:
                break
        return out

    def get_fills(self, *, limit: int = 200) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        cursor: str | None = None
        while True:
            params: dict[str, Any] = {"limit": limit}
            if cursor:
                params["cursor"] = cursor
            data = self._get("/portfolio/fills", params=params) or {}
            page = data.get("fills") or []
            out.extend(page)
            cursor = data.get("cursor")
            if not cursor or not page:
                break
        return out

    def get_settlements(self, *, limit: int = 200) -> list[dict[str, Any]]:
        """Settled markets (realized PnL). Read-only GET, paginated like fills."""
        out: list[dict[str, Any]] = []
        cursor: str | None = None
        while True:
            params: dict[str, Any] = {"limit": limit}
            if cursor:
                params["cursor"] = cursor
            data = self._get("/portfolio/settlements", params=params) or {}
            page = data.get("settlements") or []
            out.extend(page)
            cursor = data.get("cursor")
            if not cursor or not page:
                break
        return out
