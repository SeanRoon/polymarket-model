"""Probe Kalshi public API to confirm field shapes before integrating."""
import json
import httpx

BASE = "https://api.elections.kalshi.com/trade-api/v2"  # try this too
PROD = "https://external-api.kalshi.com/trade-api/v2"
HEADERS = {"User-Agent": "polymarket-model-probe/0.1", "Accept": "application/json"}


def hit(client: httpx.Client, base: str, path: str, params: dict | None = None) -> dict | list | None:
    try:
        r = client.get(f"{base}{path}", params=params)
        print(f"  {r.request.url}")
        print(f"    -> {r.status_code} ({len(r.text)} bytes)")
        if r.status_code != 200:
            print(f"    body: {r.text[:200]}")
            return None
        return r.json()
    except Exception as ex:
        print(f"    ERR {ex!r}")
        return None


def main() -> None:
    with httpx.Client(timeout=30, headers=HEADERS) as c:
        # 1) Confirm production base URL
        print("=== production base probes ===")
        for base in (PROD, BASE):
            print(f"--- {base} ---")
            ev = hit(c, base, "/events", {"limit": 1})
            if ev is not None:
                # If we got something, this base works
                if isinstance(ev, dict) and ev.get("events"):
                    print(f"    events count={len(ev['events'])}")
                    e0 = ev["events"][0]
                    print(f"    first event keys: {sorted(e0.keys())}")
                    print(f"    first event ticker: {e0.get('event_ticker')!r}")
                    break

        # 2) Try common weather series tickers
        print("\n=== weather series existence ===")
        for ticker in ("KXHIGHNY", "KXHIGHCHI", "KXHIGHMIA", "KXHIGHLAX", "KXHIGHAUS", "KXHIGHDEN",
                       "KXLOWNY", "KXLOWTNY", "KXLOWTCHI", "KXLOWMIA"):
            r = hit(c, base, f"/series/{ticker}")
            if isinstance(r, dict):
                series = r.get("series", r)
                print(f"    {ticker}: {series.get('title')!r} freq={series.get('frequency')}")

        # 3) For NY high, list open events
        print("\n=== open events for KXHIGHNY ===")
        evs = hit(c, base, "/events", {"series_ticker": "KXHIGHNY", "status": "open", "limit": 10})
        if isinstance(evs, dict):
            ev_list = evs.get("events") or []
            print(f"  open events: {len(ev_list)}")
            for e in ev_list[:5]:
                print(f"    {e.get('event_ticker')} | {e.get('title')!r} | end={e.get('strike_date') or e.get('close_time')}")

            if ev_list:
                first_event_ticker = ev_list[0].get("event_ticker")
                # 4) Pull markets for that event
                print(f"\n=== markets for {first_event_ticker} ===")
                mks = hit(c, base, "/markets", {"event_ticker": first_event_ticker, "status": "open", "limit": 30})
                if isinstance(mks, dict):
                    m_list = mks.get("markets") or []
                    print(f"  markets: {len(m_list)}")
                    if m_list:
                        m0 = m_list[0]
                        print(f"  first market keys: {sorted(m0.keys())}")
                        print(json.dumps({k: m0.get(k) for k in (
                            "ticker", "event_ticker", "subtitle", "yes_sub_title", "title",
                            "floor_strike", "cap_strike", "open_time", "close_time", "expiration_time",
                            "yes_bid", "yes_ask", "last_price", "previous_yes_bid", "previous_yes_ask",
                            "yes_bid_dollars", "yes_ask_dollars", "last_price_dollars",
                            "volume", "volume_24h", "open_interest",
                            "status", "market_type", "category",
                            "rules_primary", "rules_secondary",
                        ) if k in m0}, indent=2, default=str)[:3000])
                        # All bins, brief
                        print("\n  all bins:")
                        for m in m_list:
                            print(f"    {m.get('ticker'):<40} floor={m.get('floor_strike')} cap={m.get('cap_strike')} "
                                  f"yes_bid={m.get('yes_bid')} yes_ask={m.get('yes_ask')} subtitle={m.get('yes_sub_title') or m.get('subtitle')!r}")

                        # 5) orderbook of one bin
                        ticker = m0.get("ticker")
                        print(f"\n=== orderbook for {ticker} ===")
                        ob = hit(c, base, f"/markets/{ticker}/orderbook", {"depth": 5})
                        if isinstance(ob, dict):
                            print(json.dumps(ob, indent=2, default=str)[:1500])


if __name__ == "__main__":
    main()
