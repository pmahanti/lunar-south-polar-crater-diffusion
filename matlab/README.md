# MATLAB

## Role in this project

Independent cross-check for the 1D radial topographic-diffusion solver.

Prasun maintains a MATLAB implementation of the same explicit finite-difference
scheme used by the Python solver in this repo. On disagreement between the
Python forward solver and Cratermaker's `apply_diffusion` (the primary
validator), the MATLAB version serves as a third reference.

## Decoupling rule (locked)

Python and MATLAB never call each other. All exchange is file-based:

- Python writes inputs (initial profile, kappa schedule, time array) to
  `results/exchange/python_to_matlab/` as `.csv` or `.npy`.
- MATLAB reads those, writes its forward-diffused profiles to
  `results/exchange/matlab_to_python/` as `.csv` or `.mat`.

Rationale: the two implementations stay genuinely independent only if neither
can call the other. Any cross-language bridge erodes the value of the
cross-check.

## MATLAB version

R2024a or later assumed. No toolbox dependencies expected for the 1D
diffusion cross-check (base + finite-difference utilities). Mapping Toolbox
and Image Processing Toolbox may be needed later for the LOLA DEM-handling
cross-check, but are not required for the solver comparison.

## Status

No MATLAB scripts checked in yet. Prasun adds them when the existing 1D radial
diffusion code is migrated into this repo for the cross-check phase
(scheduled around Sprint 1 Phase 4-6).
