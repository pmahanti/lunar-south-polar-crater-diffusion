# Data

## `catalog_v0.csv` — Sprint 1 v0 stratified south polar crater catalog

Per-crater metadata for 88 lunar south polar craters in the 1–5 km diameter
band, stratified across eight 0.5 km diameter bins. Built from the Robbins
(2019) global lunar crater database. This catalog is the input to the LOLA
profile-extraction phase (Sprint 1 Phase 2).

## Source

Robbins, S. J. (2019). *A new global database of lunar impact craters >1–2 km:
1. Crater locations and sizes, comparisons with published databases, and global
analysis.* JGR-Planets, 124, 871–892. doi:10.1029/2018JE005592.

The Robbins database catalogs ~1.3 million lunar impact craters down to ~1–2 km
diameter, derived primarily from LROC WAC mosaics (with NAC supplements at high
latitudes). The local working copy is the GeoPackage conversion of the
published CSV at:

```
C:/Users/prasu/Documents/KPLO_SDC_python_work/lunar_crater_database.gpkg
```

Columns used: `CRATER_ID`, `LAT_CIRC_IMG`, `LON_CIRC_IMG`, `DIAM_CIRC_IMG`
(circular-fit lat / lon / diameter — Robbins's recommended primary fields).

## Filtering and sampling

Reproducible build: `python data/build_catalog_v0.py` (writes
`data/catalog_v0.csv`). Source GPKG path is configurable via `--gpkg`.

- **Latitude filter:** `LAT_CIRC_IMG < -75°`
- **Diameter filter:** `DIAM_CIRC_IMG ∈ [1.0, 5.0]` km
- **Bins:** eight 0.5 km bins — `[1.0, 1.5), [1.5, 2.0), ..., [4.5, 5.0]` (last bin closed on the right)
- **Sample size:** 11 craters per bin → 88 craters total
- **Random seed:** 42 (`numpy.random.default_rng(42)`)

### Population per bin (after lat / diameter filter, before sampling)

| Bin (km)      | Count  |
|---------------|--------|
| [1.0, 1.5)    | 13,274 |
| [1.5, 2.0)    | 6,965  |
| [2.0, 2.5)    | 3,786  |
| [2.5, 3.0)    | 2,273  |
| [3.0, 3.5)    | 1,516  |
| [3.5, 4.0)    | 974    |
| [4.0, 4.5)    | 621    |
| [4.5, 5.0)    | 485    |
| **Total**     | **29,894** |

Every bin is well-populated (>>11), so the stratified sample is uniform 11 per
bin. The size-frequency distribution drops off as expected.

## Schema (`catalog_v0.csv`)

| Column             | Type    | Description                                                                                  |
|--------------------|---------|----------------------------------------------------------------------------------------------|
| `crater_id`        | string  | Robbins `CRATER_ID` (e.g. `10-1-088622`). Stable join key against the source DB.            |
| `lat`              | float   | `LAT_CIRC_IMG`, degrees (south negative).                                                    |
| `lon`              | float   | `LON_CIRC_IMG`, degrees east, 0–360 convention (Robbins primary).                            |
| `diameter_km`      | float   | `DIAM_CIRC_IMG`, km, circular fit.                                                           |
| `depth_km`         | float   | **Empty in v0.** Robbins (2019) does not publish per-crater depths; populated in Phase 2 from LOLA.   |
| `is_extreme_polar` | bool    | `lat < -85°`. Convenience flag for downstream sub-filtering / sensitivity studies.           |
| `qc_status`        | enum    | `pending` / `accepted` / `rejected` / `flagged` — see "QC workflow" below. v0 ships with all `pending`. |
| `qc_notes`         | string  | Free text; populated during Quickmap visual QC. Empty by default.                            |

### QC workflow

`qc_status` semantics for the upcoming visual QC pass (Quickmap, Prasun):

- **`pending`** — not yet reviewed (every row in v0).
- **`accepted`** — clean simple crater, suitable for profile extraction.
- **`rejected`** — disqualifying issue: secondary cluster, chain crater,
  significant overlap with another crater that breaks azimuthal symmetry, or
  incorrect catalog entry.
- **`flagged`** — keep but note caveat (e.g. partial PSR shadowing in ROI,
  edge-of-DEM proximity, mild asymmetry). Profile extraction proceeds; result
  carries the flag forward.

## Polar-coverage caveats from Robbins (2019) methodology

Robbins flags reduced completeness near the poles, driven by the same imaging
conditions that motivate this whole project:

1. **Illumination geometry.** WAC base imagery is acquired at very high solar
   incidence at the poles. Long shadows obscure rim morphology; PSR interiors
   are not imaged at all in the WAC base. Crater detection therefore relies on
   shadow boundaries rather than full rim circumscription, which biases against
   shallow / degraded craters and reduces completeness at small diameters.
2. **Diameter-of-completeness drops poleward.** Robbins notes the global
   completeness limit is ~1–2 km; in the polar regions (lat > |75°|) the
   reliable lower bound is closer to **~2 km**. The `[1.0, 1.5)` and
   `[1.5, 2.0)` bins in this catalog are therefore expected to under-represent
   the true crater population.
3. **PSR interiors and PSR-floor craters are systematically missed in the WAC
   base.** Some are recovered via NAC supplements; ShadowCam-only PSR craters
   (per Pokorny et al. 2025 LPSC) are out of scope for this catalog.
4. **Circular vs elliptical fit.** We use `LAT/LON/DIAM_CIRC_IMG` (3-point
   circular fit) following Robbins's primary recommendation. Elliptical fits
   exist for craters with ≥5 rim points; not used in v0 to keep the metric set
   minimal.
5. **Crater-ID lineage.** A `CRATER_ID` of the form `XX-Y-NNNNNN` encodes the
   diameter rank tier (XX) and ID within that tier; IDs are stable across
   Robbins releases and serve as the canonical join key.

These caveats motivate downstream sensitivity checks (e.g. excluding the
smallest two bins for diffusion-state regression robustness) but do not affect
v0 catalog construction.

## Reproducibility

- Seed: 42 (NumPy `default_rng`)
- Source GPKG hash and ingest provenance are tracked outside this repo;
  Robbins's published CSV is the canonical primary.
- Re-run: `python data/build_catalog_v0.py [--gpkg PATH] [--out PATH]`. Output
  is deterministic given the same source GPKG.

## Public redistribution

The Robbins (2019) database is publicly redistributable under standard
JGR-Planets supplementary-material terms; the per-crater rows we surface here
(<100 craters) are derivative metadata, not bulk redistribution. Cite Robbins
(2019) when using `catalog_v0.csv` downstream.

The full Robbins GPKG (~1.9 GB) is **not** committed to this repo; see
`.gitignore`. Place a local copy at the path declared in `build_catalog_v0.py`
or pass `--gpkg`.

## Citations

- Robbins, S. J. (2019). A new global database of lunar impact craters >1–2 km.
  *JGR-Planets*, 124, 871–892. doi:10.1029/2018JE005592.

## Status

- `catalog_v0.csv` — built, awaiting visual QC pass.
- Phase 2 (LOLA polar DEM access + per-crater clipping) — not started.
