"""One-off: purge PRELIMINARY (mid-morning) CLI rows from data/resolutions.parquet.

Background (2026-07-23): `fetch-resolution` stored same-day 7 AM preliminary CLIs as
final for the three live stations whose NWS offices (KEWX -> KAUS/KSAT, KBOU -> KDEN)
publish before the ~13:00 UTC resolve run. Those "highs" are the overnight max, 15-25F
below the real afternoon high (verified vs Kalshi settlements), which poisoned the bias
correction (KAUS/high +9.4F, KDEN/high +13.6F) and every downstream eval/paper number
for the live cities. See data/reports/model-watch.md 2026-07-23.

This removes the poisoned rows so the (now preliminary-aware) `fetch-resolution` can
re-fetch a genuine FINAL where one is still in the live CLI version stack (recent days),
and simply leaves older days UNRESOLVED (honestly missing) rather than wrong.

A row is poisoned if its raw_text carries the AM "VALID AS OF" marker. As a cross-check
we also report rows fetched the SAME local day they are valid for (lag 0), which is the
structural signature of the same bug.

Usage:
    uv run python scripts/purge_preliminary_resolutions.py            # dry run (report only)
    uv run python scripts/purge_preliminary_resolutions.py --apply    # rewrite the parquet
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from polymarket_model.weather.nws import _PRELIMINARY_RE

RESOLUTIONS = Path("data") / "resolutions.parquet"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Rewrite the parquet (default: dry run).")
    ap.add_argument("--path", default=str(RESOLUTIONS))
    args = ap.parse_args()

    df = pd.read_parquet(args.path)
    n0 = len(df)

    prelim = df["raw_text"].fillna("").map(lambda t: bool(_PRELIMINARY_RE.search(t)))
    valid_d = pd.to_datetime(df["valid_date_local"]).dt.date
    fetch_d = pd.to_datetime(df["fetched_at_utc"]).dt.date
    lag0 = (pd.to_datetime(fetch_d) - pd.to_datetime(valid_d)).dt.days == 0

    poisoned = prelim | lag0
    bad = df[poisoned]

    print(f"total rows: {n0}")
    print(f"flagged preliminary (AM VALID marker): {int(prelim.sum())}")
    print(f"flagged same-day fetch (lag 0):        {int(lag0.sum())}")
    print(f"union to purge:                        {int(poisoned.sum())}")
    print()
    print("by station/kind:")
    print(bad.groupby(["station_id", "kind"]).size().to_string())

    if not args.apply:
        print("\nDRY RUN — pass --apply to rewrite. Then run `polymarket fetch-resolution`")
        print("with the preliminary-aware parser to re-fetch finals where still available.")
        return

    keep = df[~poisoned].reset_index(drop=True)
    keep.to_parquet(args.path, index=False)
    print(f"\nPURGED {n0 - len(keep)} rows; wrote {len(keep)} to {args.path}")


if __name__ == "__main__":
    main()
