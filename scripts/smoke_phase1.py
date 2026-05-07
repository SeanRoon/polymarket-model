"""End-to-end Phase 1 smoke test: discovery -> prices -> ensemble -> model -> compare."""
from polymarket_model.logging_setup import configure_logging
from polymarket_model.markets.discovery import discover_weather_events
from polymarket_model.markets.prices import fetch_event_prices
from polymarket_model.weather.openmeteo import fetch_daily_extreme
from polymarket_model.model import (
    PredictiveDistribution,
    evaluate_event,
    assert_bins_cover_support,
)


def main() -> None:
    configure_logging()
    events = discover_weather_events()
    print(f"discovered {len(events)} active F-unit weather events")

    target = next(
        (e for e in events if e.city.lower().startswith("nyc") and e.kind == "high" and e.target_date_local.day == 8),
        None,
    )
    if target is None and events:
        target = events[0]
    if target is None:
        print("no events to test against")
        return

    ok, reason = assert_bins_cover_support(target.bins)
    print(f"event: {target.title}")
    print(f"  station={target.station_id}  date={target.target_date_local}  unit={target.unit}")
    print(f"  bins cover support: {ok} ({reason})")

    ex = fetch_daily_extreme(target.station_id, target.target_date_local, target.kind, unit=target.unit)
    dist = PredictiveDistribution.from_ensemble(ex)
    out = evaluate_event(target, dist)
    prices = fetch_event_prices(target, with_book=False)
    print(f"  ensemble: model={ex.model} members={ex.n_members} lead_hours={ex.lead_hours}")
    print(f"  model: sum_of_bin_probs={out.sum_of_bin_probs:.4f}  outside={out.outside_bin_mass:.4f}  qc={out.passes_qc}")
    print(f"  market: sum_of_mids={prices.sum_of_mids:.4f}  qc={prices.passes_qc}")
    print()
    print(f"  {'bin':<22}  {'model_p':>8}  {'market':>7}  {'edge':>9}")
    for bp, pp in zip(out.bin_probs, prices.prices, strict=True):
        market = pp.midpoint if pp.midpoint is not None else float("nan")
        edge = bp.p - market if pp.midpoint is not None else float("nan")
        print(f"  {bp.bin.label:<22}  {bp.p:>8.4f}  {market:>7.4f}  {edge:>+9.4f}")


if __name__ == "__main__":
    main()
