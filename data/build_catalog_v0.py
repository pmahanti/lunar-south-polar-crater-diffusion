"""Build Sprint 1 v0 stratified south polar crater catalog from Robbins (2018).

Filters the Robbins (2018) global lunar crater database to lat < -75 deg and
diameter in [1.0, 5.0] km, bins by 0.5 km diameter, and stratified-samples
``PER_BIN`` craters per bin with ``SEED``.

Source GPKG is the full Robbins CSV ingested into a GeoPackage; columns of
interest are ``CRATER_ID``, ``LAT_CIRC_IMG``, ``LON_CIRC_IMG``, ``DIAM_CIRC_IMG``
(km, circular fit). Robbins (2018) does NOT publish per-crater depths, so the
``depth_km`` column in the output is left blank for population during a later
LOLA-DEM phase.
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

DEFAULT_GPKG = Path(
    r"C:/Users/prasu/Documents/KPLO_SDC_python_work/lunar_crater_database.gpkg"
)
TABLE = "lunar_crater_database"
LAT_MAX_DEG = -75.0
EXTREME_POLAR_LAT_DEG = -85.0
DIAM_MIN_KM = 1.0
DIAM_MAX_KM = 5.0
BIN_EDGES_KM = np.arange(1.0, 5.0001, 0.5)  # 1.0, 1.5, ..., 5.0 -> 8 bins
PER_BIN = 11  # 11 * 8 = 88 craters, in the 80-90 target band
SEED = 42


def load_band(gpkg: Path) -> pd.DataFrame:
    """Pull all Robbins craters in the south polar diameter band into memory."""
    query = (
        "SELECT CRATER_ID, LAT_CIRC_IMG AS lat, LON_CIRC_IMG AS lon, "
        f"DIAM_CIRC_IMG AS diameter_km, CRATER_NAME FROM {TABLE} "
        "WHERE LAT_CIRC_IMG < ? AND DIAM_CIRC_IMG BETWEEN ? AND ?"
    )
    with sqlite3.connect(str(gpkg)) as conn:
        return pd.read_sql_query(
            query, conn, params=(LAT_MAX_DEG, DIAM_MIN_KM, DIAM_MAX_KM)
        )


def per_bin_counts(df: pd.DataFrame) -> pd.Series:
    """Count craters in each 0.5 km diameter bin (right edge inclusive on last)."""
    intervals = pd.cut(
        df["diameter_km"],
        bins=BIN_EDGES_KM,
        right=False,
        include_lowest=True,
    )
    # last bin: extend to include the upper edge (5.0 km)
    last_lo = BIN_EDGES_KM[-2]
    last_hi = BIN_EDGES_KM[-1]
    last_mask = df["diameter_km"] == last_hi
    if last_mask.any():
        intervals = intervals.cat.add_categories([])  # no-op, kept for symmetry
        intervals.loc[last_mask] = pd.Interval(last_lo, last_hi, closed="left")
    return intervals.value_counts().sort_index()


def _bin_mask(df: pd.DataFrame, lo: float, hi: float, is_last: bool) -> pd.Series:
    if is_last:
        return (df["diameter_km"] >= lo) & (df["diameter_km"] <= hi)
    return (df["diameter_km"] >= lo) & (df["diameter_km"] < hi)


def stratified_sample(df: pd.DataFrame, per_bin: int, seed: int) -> pd.DataFrame:
    """Sample ``per_bin`` craters from each 0.5 km bin (or fewer if short)."""
    rng = np.random.default_rng(seed)
    parts = []
    for i, (lo, hi) in enumerate(zip(BIN_EDGES_KM[:-1], BIN_EDGES_KM[1:])):
        is_last = i == len(BIN_EDGES_KM) - 2
        bin_df = df.loc[_bin_mask(df, lo, hi, is_last)]
        n = min(per_bin, len(bin_df))
        idx = rng.choice(bin_df.index.to_numpy(), size=n, replace=False)
        parts.append(bin_df.loc[idx])
    return pd.concat(parts).sort_values("diameter_km").reset_index(drop=True)


def build_output(sample: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "crater_id": sample["CRATER_ID"],
            "lat": sample["lat"],
            "lon": sample["lon"],
            "diameter_km": sample["diameter_km"],
            "depth_km": pd.NA,
            "is_extreme_polar": sample["lat"] < EXTREME_POLAR_LAT_DEG,
            "qc_status": "pending",
            "qc_notes": "",
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gpkg", type=Path, default=DEFAULT_GPKG)
    parser.add_argument(
        "--out", type=Path, default=Path("data/catalog_v0.csv")
    )
    args = parser.parse_args()

    df = load_band(args.gpkg)
    print(
        f"Robbins south polar band (lat<{LAT_MAX_DEG}, "
        f"D in [{DIAM_MIN_KM}, {DIAM_MAX_KM}] km): {len(df)} craters"
    )
    print("Per-bin counts (0.5 km, left-closed; last bin includes 5.0):")
    for interval, n in per_bin_counts(df).items():
        print(f"  [{interval.left:.1f}, {interval.right:.1f}) : {n}")

    sample = stratified_sample(df, PER_BIN, SEED)
    print(
        f"\nStratified sample: {len(sample)} craters "
        f"(seed={SEED}, target={PER_BIN} per bin)"
    )

    out = build_output(sample)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, index=False)
    print(f"Wrote {args.out} ({len(out)} rows)")


if __name__ == "__main__":
    main()
