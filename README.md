# Lunar South Polar Crater Diffusion

Topographic profile and diffusion-state catalog for lunar south polar craters in the 1–5 km diameter range. Built with a profile-fit inverse model (not depth-to-diameter proxy), validated against published forward solvers.

## Status

**Sprint 1 in progress** (May 3–14, 2026, possible extension to May 17).
v0.1.0 release targeted for end of sprint.

## Motivation

Topographic diffusion is a primary mechanism of lunar landscape evolution and a quantitative proxy for relative crater age (Fassett & Thomson 2014; Fassett et al. 2022). Existing diffusion-state catalogs are concentrated on lunar mare; the south polar region — where Artemis-era exploration is focused — has not been systematically characterized.

This repository delivers:

- A reproducible catalog of 80–90 south polar craters (1–5 km diameter, lat < -75°) sourced from the Robbins (2019) global lunar crater database
- Per-crater topographic profiles extracted from LOLA polar DEMs
- Chebyshev polynomial coefficient features per profile (Mahanti et al. 2014 representation)
- Inverse-model degradation state K per crater, fit by iterative forward marching against an initial-shape model
- Forward diffusion solver in Python, cross-validated against Cratermaker (Minton group)

The dataset itself is the primary Sprint 1 deliverable. ML regression linking Chebyshev coefficients to K is deferred to Sprint 2. Anomalous diffusion exploration is deferred to Sprint 3+.

## Approach

### Data
- **Crater catalog:** Robbins (2019), filtered to lat < -75° and D ∈ [1.0, 5.0] km, stratified across 0.5 km diameter bins (random seed 42)
- **Topography:** LOLA polar DEM, per-crater clipping with a 2.5× diameter window
- **Profile extraction:** azimuth-averaged 1D radial profile per crater (FT2014 convention); multi-azimuth as Sprint 2 sensitivity check

### Forward diffusion model
- 1D radial heat equation on a uniform polar grid, explicit finite differences
- Implementation in Python (`src/diffusion/forward_pm.py`)
- Validation harness: mass conservation, analytical Gaussian solution σ²(t) = σ₀² + 2κt, agreement with Cratermaker `apply_diffusion` on test craters

### Inverse model
- Iterative forward-marching algorithm: starting from initial-shape model z_init(r, D), apply diffusion in dK steps and find K minimizing ‖z_current − z_obs‖₂
- Initial-shape model: parabolic profile, d/D = 0.21 (Pike 1977 / FT2014 convention)
- Visibility limit Kv flagging per FT2014; craters with best_K > Kv are flagged in the dataset

### Feature extraction
- Chebyshev polynomial fit to each radial profile (Mahanti et al. 2014 representation)
- Coefficients persisted alongside K labels in the catalog CSV

## Repository Structure

- `src/` — Python implementation (forward and inverse models, profile extraction, Chebyshev fitting)
- `matlab/` — Reference forward-model implementation and validation scripts
- `data/` — Catalog provenance, crater list, processed profiles (small files committed; large DEMs via download script)
- `notebooks/` — Exploration, validation, and figure generation
- `results/` — Output figures, validation tables, processed dataset

## Citation Context

This work builds on:

- Fassett, C. I., & Thomson, B. J. (2014). Crater degradation on the lunar maria: Topographic diffusion and the rate of erosion on the Moon. *JGR-Planets*, 119, 2255–2271. doi:10.1002/2014JE004698
- Fassett, C. I., Beyer, R. A., Deutsch, A. N., Hirabayashi, M., Leight, C., Mahanti, P., Nypaver, C. A., Thomson, B. J., & Minton, D. A. (2022). Topographic diffusion revisited: Small crater lifetime on the Moon and implications for volatile exploration. *JGR-Planets*, 127. doi:10.1029/2022JE007510
- Mahanti, P., Robinson, M., Humm, D., & Stopar, J. (2014). A standardized approach for quantitative characterization of impact crater topography. *Icarus*, 241, 114–129
- Robbins, S. J. (2019). A new global database of lunar impact craters >1–2 km. *JGR-Planets*

The forward-model validation uses Cratermaker (Minton group, github.com/MintonGroup/cratermaker), supported by NASA LDAP grants #80NSSC21K1719 and #80NSSC25K7050.

## License

Code: MIT. Data products: NASA public domain (Robbins catalog, LOLA DEMs). Cratermaker is a GPL-3.0 dependency used as a library only; no Cratermaker source is redistributed in this repo.

## Author

Prasun Mahanti — Co-Investigator, Lunar Reconnaissance Orbiter Camera (LROC); Principal Investigator, ShadowCam (KPLO mission); Associate Research Scientist, Intuitive Machines. Co-author on Fassett et al. 2022.
