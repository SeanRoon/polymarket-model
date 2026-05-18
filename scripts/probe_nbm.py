"""Probe NBM QMD GRIB2 to confirm Tmax/Tmin percentile field layout.

Run from project root:
    PYTHONUTF8=1 uv run python scripts/probe_nbm.py

Goal: validate that NBM QMD carries Tmax/Tmin at percentiles 10/25/50/75/90 with
sensible values at KLAX and KMIA. If this fails or the schema differs we stop
and reassess before touching production code.

Herbie ships a built-in NBM template but it hard-codes the deterministic 'core'
product. We register a sibling 'nbm_qmd' template that points at the probabilistic
'qmd' product on the same AWS bucket.
"""
from __future__ import annotations

import sys
import traceback
from datetime import UTC, datetime, timedelta


KLAX = (33.9425, -118.4081)
KMIA = (25.7959, -80.2870)


def _register_qmd_template() -> None:
    """Inject an `nbm_qmd` template into herbie.models that swaps 'core' -> 'qmd'."""
    import herbie.models
    from herbie.models.nbm import nbm as _NBM_BASE

    class nbm_qmd(_NBM_BASE):
        def template(self):
            _NBM_BASE.template(self)
            self.DESCRIPTION = "National Blend of Models (Probabilistic QMD)"
            self.SOURCES = {
                "aws": (
                    "https://noaa-nbm-grib2-pds.s3.amazonaws.com/"
                    f"blend.{self.date:%Y%m%d}/{self.date:%H}/qmd/"
                    f"blend.t{self.date:%H}z.qmd.f{self.fxx:03d}.{self.product}.grib2"
                ),
                "nomads": (
                    "https://nomads.ncep.noaa.gov/pub/data/nccf/com/blend/prod/"
                    f"blend.{self.date:%Y%m%d}/{self.date:%H}/qmd/"
                    f"blend.t{self.date:%H}z.qmd.f{self.fxx:03d}.{self.product}.grib2"
                ),
            }

    herbie.models.nbm_qmd = nbm_qmd


def main() -> int:
    _register_qmd_template()
    from herbie import Herbie

    # NBM QMD is published at 00/06/12/18 UTC (6-hourly). Empirically, upload
    # finishes 6-8h after cycle time. Apply a 10h safety margin.
    now = datetime.now(UTC).replace(minute=0, second=0, microsecond=0)
    deadline = now - timedelta(hours=10)
    cycle_hour = (deadline.hour // 6) * 6
    cycle = deadline.replace(hour=cycle_hour)
    fxx = 24
    print(f"Probing NBM QMD cycle={cycle.isoformat()} fxx={fxx}")

    try:
        H = Herbie(cycle.strftime("%Y-%m-%d %H:%M"), model="nbm_qmd", product="co", fxx=fxx)
    except Exception:
        traceback.print_exc()
        return 1

    print(f"  grib URL: {H.grib}")
    print(f"  idx URL : {H.idx}")
    if H.grib is None:
        print("File not found at any source — try an earlier cycle/lead.")
        return 1

    try:
        inv = H.inventory()
    except Exception:
        traceback.print_exc()
        return 2

    print(f"\nTotal GRIB2 messages: {len(inv)}")
    print("Columns:", list(inv.columns))

    # Show TMAX/TMIN/MAXT/MINT/TMP rows.
    mask = inv["variable"].astype(str).str.contains("TMAX|TMIN|TMP|MAXT|MINT", regex=True, na=False)
    candidates = inv[mask]
    print(f"\nTMAX/TMIN/TMP candidate rows: {len(candidates)}")
    cols = [c for c in ("variable", "level", "forecast_time", "search_this") if c in candidates.columns]
    print(candidates[cols].head(60).to_string())

    # Pull a slice that should include TMAX/TMIN percentile messages.
    print("\nLoading filtered xarray (TMAX|TMIN|MAXT|MINT)...")
    try:
        ds = H.xarray("(TMAX|TMIN|MAXT|MINT)")
    except Exception:
        traceback.print_exc()
        return 3

    print("\nDataset(s):")
    if isinstance(ds, list):
        for i, d in enumerate(ds):
            print(f"-- dataset {i} --")
            print(d)
            print()
    else:
        print(ds)

    # Spot-check at KLAX/KMIA.
    print("\nNearest-grid lookup:")
    target = ds[0] if isinstance(ds, list) else ds
    for name, (lat, lon) in (("KLAX", KLAX), ("KMIA", KMIA)):
        print(f"\n{name} ({lat}, {lon}):")
        try:
            pt = target.herbie.nearest_points(points=[(lat, lon)])
            print(pt)
        except Exception:
            traceback.print_exc()

    return 0


if __name__ == "__main__":
    sys.exit(main())
