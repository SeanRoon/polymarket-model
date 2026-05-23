"""KalshiAuthedClient: auth headers attached, base-path included in signed string, pagination."""
from __future__ import annotations

import httpx
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from polymarket_model.execution.auth import KalshiAuth
from polymarket_model.execution.client import KalshiAuthedClient, _path_for_signing


@pytest.fixture(scope="module")
def auth() -> KalshiAuth:
    priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return KalshiAuth(key_id="test-key", private_key=priv)


def _client_with_handler(auth: KalshiAuth, handler) -> KalshiAuthedClient:
    transport = httpx.MockTransport(handler)
    return KalshiAuthedClient(
        auth=auth,
        base_url="https://api.elections.kalshi.com/trade-api/v2",
        transport=transport,
    )


def test_path_for_signing_includes_api_version_prefix():
    # The signed path must include /trade-api/v2; httpx's base_url already has it.
    p = _path_for_signing("https://api.elections.kalshi.com/trade-api/v2", "/portfolio/balance")
    assert p == "/trade-api/v2/portfolio/balance"


def test_path_for_signing_handles_trailing_slash_on_base():
    p = _path_for_signing("https://example.test/trade-api/v2/", "/portfolio/positions")
    assert p == "/trade-api/v2/portfolio/positions"


def test_get_balance_attaches_required_auth_headers(auth):
    captured: dict[str, httpx.Request] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["req"] = request
        return httpx.Response(200, json={"balance": 12345})

    client = _client_with_handler(auth, handler)
    out = client.get_balance()

    assert out == {"balance": 12345}
    req = captured["req"]
    assert req.headers["KALSHI-ACCESS-KEY"] == "test-key"
    assert req.headers["KALSHI-ACCESS-TIMESTAMP"].isdigit()
    assert req.headers["KALSHI-ACCESS-SIGNATURE"]
    assert req.url.path == "/trade-api/v2/portfolio/balance"


def test_404_returns_none_without_raising(auth):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"error": "not found"})

    client = _client_with_handler(auth, handler)
    assert client.get_balance() is None


def test_get_positions_paginates_through_cursor(auth):
    pages = [
        {"market_positions": [{"ticker": "A"}, {"ticker": "B"}], "cursor": "next-1"},
        {"market_positions": [{"ticker": "C"}], "cursor": None},
    ]
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(200, json=pages[len(calls) - 1])

    client = _client_with_handler(auth, handler)
    out = client.get_positions(limit=2)

    assert [p["ticker"] for p in out] == ["A", "B", "C"]
    assert len(calls) == 2
    # Second call should include the cursor returned by the first.
    assert "cursor=next-1" in str(calls[1].url)


def test_get_fills_returns_empty_list_when_no_data(auth):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"fills": [], "cursor": None})

    client = _client_with_handler(auth, handler)
    assert client.get_fills() == []


def test_client_class_exposes_no_mutating_methods():
    """Sanity check: the read-only client must not grow POST/PUT/DELETE accessors by accident."""
    forbidden = {"place_order", "cancel_order", "create_order", "post", "put", "delete"}
    public = {n for n in dir(KalshiAuthedClient) if not n.startswith("_")}
    assert forbidden.isdisjoint(public), f"Mutating method leaked into read-only client: {forbidden & public}"
