from __future__ import annotations

import json
from typing import Any

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from polymarket_model.config import settings
from polymarket_model.logging_setup import get_logger

log = get_logger(__name__)


_RETRYABLE = retry_if_exception_type((httpx.HTTPError, httpx.TimeoutException))
_WAIT = wait_exponential(multiplier=0.5, min=0.5, max=8.0)


def _client(base_url: str) -> httpx.Client:
    return httpx.Client(
        base_url=base_url,
        timeout=settings.http_timeout_seconds,
        headers={"User-Agent": settings.http_user_agent, "Accept": "application/json"},
    )


class GammaClient:
    """Read-only client for Polymarket's Gamma metadata API."""

    def __init__(self, base_url: str | None = None) -> None:
        self._base_url = base_url or settings.polymarket_gamma_base_url

    @retry(retry=_RETRYABLE, wait=_WAIT, stop=stop_after_attempt(settings.http_max_retries), reraise=True)
    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        with _client(self._base_url) as c:
            r = c.get(path, params=params)
            r.raise_for_status()
            return r.json()

    def get_event_by_slug(self, slug: str) -> dict[str, Any] | None:
        data = self._get("/events", params={"slug": slug})
        if isinstance(data, list) and data:
            return data[0]
        return None

    def list_active_events_by_tag(self, tag_id: int | str, limit: int = 500) -> list[dict[str, Any]]:
        """List active, open events for a given tag id (e.g. 84 for Weather)."""
        out: list[dict[str, Any]] = []
        offset = 0
        page_size = 100
        while True:
            page = self._get(
                "/events",
                params={
                    "tag_id": tag_id,
                    "active": "true",
                    "closed": "false",
                    "limit": page_size,
                    "offset": offset,
                },
            )
            if not isinstance(page, list) or not page:
                break
            out.extend(page)
            if len(page) < page_size or len(out) >= limit:
                break
            offset += page_size
        return out[:limit]


class ClobClient:
    """Read-only client for Polymarket's CLOB price endpoints. No auth required."""

    def __init__(self, base_url: str | None = None) -> None:
        self._base_url = base_url or settings.polymarket_clob_base_url

    @retry(retry=_RETRYABLE, wait=_WAIT, stop=stop_after_attempt(settings.http_max_retries), reraise=True)
    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        with _client(self._base_url) as c:
            r = c.get(path, params=params)
            r.raise_for_status()
            return r.json()

    def get_midpoint(self, token_id: str) -> float | None:
        try:
            data = self._get("/midpoint", params={"token_id": token_id})
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return None
            raise
        mid = data.get("mid") if isinstance(data, dict) else None
        return float(mid) if mid is not None else None

    def get_book(self, token_id: str) -> dict[str, Any] | None:
        try:
            data = self._get("/book", params={"token_id": token_id})
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return None
            raise
        return data if isinstance(data, dict) else None

    @staticmethod
    def best_bid_ask(book: dict[str, Any] | None) -> tuple[float | None, float | None, float | None, float | None]:
        """Return (best_bid_price, best_ask_price, best_bid_size, best_ask_size)."""
        if not book:
            return None, None, None, None
        bids = book.get("bids") or []
        asks = book.get("asks") or []
        # CLOB returns sorted; bids descending best-first, asks ascending best-first.
        best_bid = bids[0] if bids else None
        best_ask = asks[0] if asks else None
        bb = float(best_bid["price"]) if best_bid else None
        bs = float(best_bid["size"]) if best_bid else None
        ba = float(best_ask["price"]) if best_ask else None
        as_ = float(best_ask["size"]) if best_ask else None
        return bb, ba, bs, as_


def parse_json_field(value: Any) -> Any:
    """Polymarket Gamma returns clobTokenIds, outcomes, outcomePrices as JSON-encoded strings.
    Accepts already-parsed lists for forward compatibility.
    """
    if value is None:
        return None
    if isinstance(value, (list, dict)):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return None
    return None
