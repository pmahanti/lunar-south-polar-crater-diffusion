# MATLAB Validation

Radiometric and SNR validation of denoised outputs against the ShadowCam calibration pipeline. These scripts encode domain-specific checks that complement standard ML metrics (PSNR, SSIM).

## Scripts (to be added May 9)

- `snr_analysis.m` — Per-frame SNR estimation before/after denoising
- `radiometric_consistency.m` — Verify denoised radiance values remain within calibration tolerance
- `bright_unit_contrast.m` — PSR-specific check: preservation of bright/dark unit contrast on PSR walls

## Inputs

Denoised outputs from `../results/denoised/` (`.mat` or `.npy` format).

## Outputs

Validation figures to `../results/figures/matlab/`.

## MATLAB Version

R2024a or later. Requires Mapping Toolbox and Image Processing Toolbox.
