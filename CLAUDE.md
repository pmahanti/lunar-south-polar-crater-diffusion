# Claude Code Conventions for shadowcam-ssl-denoising

## Project Owner
Prasun Mahanti. Lunar research scientist with deep ShadowCam calibration background. The MATLAB validation pipeline is first-class — not optional, not an afterthought.

## Coding Style
- Python 3.11
- PyTorch + Lightning (not raw training loops)
- Type hints required on public functions
- Black formatting, ruff linting
- Docstrings: NumPy style

## Architecture Decisions (locked)
- **Method:** Neighbor2Neighbor primary, Noise2Void as fallback
- **Backbone:** Small U-Net (4 levels, base channels 32) — keep parameter count low so Colab T4 is sufficient
- **Loss:** L1 reconstruction + regularization term per N2N paper
- **Patch size:** 128x128 during training
- **Optimizer:** Adam, lr 1e-4, cosine schedule
- **Batch size:** 16 (adjust if OOM on Colab)

## Compute
- Primary: Google Colab Pro (T4/V100)
- Local dev: CPU-only is fine for scaffolding and tests
- W&B entity: `pmahanti-lroc-personal`
- W&B project: `shadowcam-ssl-denoising`

## Data
- ShadowCam EDR/CDR products from NASA PDS only
- Test region: Shackleton crater floor
- Data files NEVER committed to git (see .gitignore)
- Download via `data/download.py` (to be implemented May 6)

## MATLAB Integration
- MATLAB scripts live in `matlab/`
- Python writes denoised outputs as `.mat` or `.npy` files to `results/denoised/`
- MATLAB reads from `results/denoised/`, writes validation figures to `results/figures/matlab/`
- Do NOT attempt to call MATLAB from Python or vice versa — keep them decoupled
- MATLAB version: R2024a or later assumed

## Don't Touch
- The MATLAB scripts (Prasun writes those — they encode domain expertise)
- The README.md (Prasun owns the lunar-science framing)
- Any file in `paper/` if it appears later (Overleaf-synced)

## Sprint 1 Deadlines
- May 7: Working scaffold + smoke test on real data
- May 9: First trained model + evaluation
- May 11: README finalized
- May 13: v0.1.0 tagged
- May 14: Public release

## Reference Papers
- Lehtinen et al. 2018 — Noise2Noise
- Huang et al. 2021 — Neighbor2Neighbor (primary method)
- Krull et al. 2019 — Noise2Void (fallback)
- Robinson et al. 2023 — ShadowCam instrument paper
- Humm et al. 2023 — ShadowCam calibration
