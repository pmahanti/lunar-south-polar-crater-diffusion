# Claude Code Conventions for lunar-south-polar-crater-diffusion

## Project
Public dataset of south polar lunar craters (1–5 km diameter, lat < −75°) with per-crater LOLA-derived topographic profiles, Chebyshev coefficients, and inverse-model topographic-diffusion state K. Extends Fassett & Thomson 2014 and Fassett et al. 2022 to the south pole, where the diffusion regime may differ.

- **Sprint 1 (May 3 → May 14, possible extension to May 16/17):** ship dataset CSV + reproducible processing code + validation figure. **No ML in Sprint 1.**
- **Sprint 2:** ML regression (Chebyshev coefficients → K). Frame against Chen et al. 2025 (image+morphology fusion).
- **Sprint 3+:** anomalous diffusion exploration (slope-dependent first, fractional-time/space second). Standalone paper.

## Project Owner
Prasun Mahanti. LROC Co-I, ShadowCam PI, IM Associate Research Scientist. Co-author on Fassett et al. 2022 — this project is natural follow-on to that work, not competition. Domain depth (Chebyshev representation, calibration knowledge, mission ConOps) is the moat; don't dilute by chasing AI-flavored work that anyone could do.

## Coding Style
- Python 3.11
- Type hints on public functions
- Black formatting, ruff linting
- Docstrings: NumPy style
- Sprint 1 has no ML; scientific-Python stack only (numpy, scipy, pandas, matplotlib, rasterio/GDAL for LOLA)
- Sprint 2 ML: scikit-learn first; only escalate to PyTorch if a tabular regressor is genuinely insufficient

## Architecture Decisions (locked)

### Crater catalog
- **Source:** Robbins (2019) global lunar crater database
- **Filter:** lat < −75°, diameter ∈ [1.0, 5.0] km
- **Sample:** 80–90 craters, stratified evenly across 0.5 km diameter bins, random seed 42
- **Columns:** `crater_id, lat, lon, diameter_km, depth_km, is_extreme_polar (lat < −85°), qc_status, qc_notes`
- Visual QC (Quickmap) flags overlapping/secondary/chain craters

### Profile extraction
- Azimuth-averaged 1D radial profile per crater from LOLA polar DEM (matches FT2014)
- Multi-azimuth profiles deferred to Sprint 2 sensitivity check

### Forward diffusion model
- **Workhorse:** Reimplement 1D radial diffusion in Python, ~50–100 lines, finite-differences, explicit scheme on uniform polar grid
- **Validator:** Minton's Cratermaker `apply_diffusion` (forward only). Prasun is co-author with Minton on F2022.
- **Cross-check:** Prasun has a MATLAB version of the same 1D solver — useful third reference if Python and Cratermaker disagree
- **DO NOT** use Cratermaker's `measure_degradation_state` — it relies on a depth-to-diameter proxy (DepthCount). 1–5 km polar craters are not simple bowl-shaped cones; full profile-fit is required.
- **License note:** Cratermaker is GPL-3.0. Using as a dependency (not redistributing source) is fine for this MIT-licensed code.

### Inverse model
- Iterative forward-marching: start from initial-shape model `z_init(r, D)`, apply diffusion in dK steps, find K minimizing ‖z_current − z_obs‖₂
- **Initial shape:** parabolic, d/D = 0.21 per Pike 1977 / FT2014 convention
- **Visibility limit:** Kv per FT2014; flag craters where `best_K > Kv`

### Validation tests (forward solver)
- Mass conservation
- Analytical Gaussian diffusion solution σ²(t) = σ₀² + 2κt
- Agreement with Cratermaker on 5 test craters

### Chebyshev representation
- Per Mahanti et al. 2014 *Icarus*. Prasun's own published method.

## Compute
- **Sprint 1:** local CPU sufficient (no GPU work)
- **Sprint 2+ (ML):** Google Colab Pro (T4/V100) available
- **W&B entity:** `pmahanti-lroc-personal` (recorded; login deferred to Sprint 2)
- **W&B project:** TBD on first ML run — likely `polar-crater-diffusion`. Not used in Sprint 1 (forward/inverse solver runs are not standard ML training; W&B is overkill).

## Data
- **Sources:** Robbins (2019) catalog (CSV), LOLA polar DEM (PDS)
- Data files NEVER committed to git (see `.gitignore`)
- Public release target: dataset CSV + processing code on Zenodo with DOI (v0.1.0)
- ShadowCam data is **not** used in this project (Sprint 1 N2N project was abandoned; see `project_diary_2026-05-03.md`)

## MATLAB Integration
- MATLAB scripts live in `matlab/` if/when added by Prasun
- Python ↔ MATLAB stays decoupled — file-based handoff only, no cross-language calls
- MATLAB version: R2024a or later assumed
- Prasun's MATLAB 1D radial diffusion code is the third reference for forward-solver cross-check

## Don't Touch
- `README.md` — Prasun owns the lunar-science framing
- `paper/` if it appears later — Overleaf-synced
- MATLAB scripts in `matlab/` — Prasun writes those; they encode domain expertise

## Sprint 1 Phase Plan
| Phase | Task | Hours |
|---|---|---|
| 0 | Re-read FT2014, F2022, Cratermaker docs | 1.5 |
| 1 | Robbins south polar crater catalog → `data/catalog_v0.csv` | 0.75 |
| 2 | LOLA polar DEM access + per-crater clipping | 2 |
| 3 | Profile extraction (azimuth-averaged) | 1 |
| 4 | Forward model + Cratermaker validation | 3–4 |
| 5 | Inverse model (iterative forward marching) | 2 |
| 6 | Validation against Cratermaker on 5 test craters | 1 |
| 7 | Chebyshev fitting on profiles | 1 |
| 8 | ~~ML regression~~ — deferred to Sprint 2 | — |
| 9 | README + Zenodo release prep | 1.5 |
| | **Total** | **~14 hr** |

## Sprint 1 Deadlines
- **May 3:** Catalog generation (`data/catalog_v0.csv`)
- **May 4:** Re-read FT2014 + F2022; update this CLAUDE.md with any newly extracted architecture decisions; no code
- **Day 4–5:** Cratermaker install spike before forward-model implementation
- **May 14:** v0.1.0 ship target (dataset + code + validation figure on Zenodo)
- **May 16/17:** Hard extension cap

## Reference Papers
- **Fassett & Thomson 2014** *JGR-Planets* — original topographic-diffusion method on mare; size-independent κ ~5.5 m²/Myr
- **Fassett, Beyer, Deutsch, Hirabayashi, Leight, Mahanti, Nypaver, Thomson, Minton 2022** *JGR-Planets* — revisits FT2014; size-dependent κ; **Prasun is co-author**
- **Mahanti, Robinson, Humm, Stopar 2014** *Icarus* — Chebyshev representation of impact crater topography; **Prasun's method**
- **Robbins 2019** *JGR-Planets* — global lunar crater database; primary catalog source
- **Chen et al. 2025** *Icarus* — dual-branch CNN for lunar simple crater degradation grades; closest published competitor to Sprint 2 ML overlay
- **Pokorny, Mazarico, Robinson, Mahanti et al. 2025** LPSC — ML detection of PSR craters using ShadowCam; alternative polar catalog source if Robbins is sparse; **Prasun co-author**
- **Minton group, Cratermaker** `github.com/MintonGroup/cratermaker` — forward-diffusion solver used as validator

## Behavioral Notes (from project diary)
- **Decision discipline:** when in doubt, the answer is no, the decision stands, ship v0.1.0. Do not revisit foundational decisions mid-sprint.
- **Scope creep is the #1 sprint killer.** New ideas (second site, extreme polar expansion, second method) get logged as "Sprint N+1 candidates," not absorbed into the current sprint.
- **Sprint 1 ships dataset, not ML.** ML regression is Sprint 2. Anomalous diffusion is Sprint 3+.
- **Public visibility is the point.** Each deliverable: GitHub repo + LinkedIn post + (when justified) Zenodo DOI or preprint.

## Resuming in a Fresh Conversation
Share `project_diary_2026-05-03.md` (top-level) and this CLAUDE.md. Diary holds strategic context; CLAUDE.md is the operational handbook.
