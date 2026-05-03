# Data

## Source

NASA Planetary Data System (PDS) Imaging Node — ShadowCam archive.

## Product Level

ShadowCam EDR (Experiment Data Record) and CDR (Calibrated Data Record) products. CDR preferred for evaluation; EDR may be used for noise characterization studies.

## Test Region

Shackleton crater floor, lunar south pole. Selected for:
- Well-characterized PSR with multiple published studies (Mahanti et al. 2024 PSJ; Mahanti et al. 2024 LPSC)
- Multiple ShadowCam observations across a range of secondary illumination conditions
- Public availability of all relevant frames

## Frame Selection Target

20–50 ShadowCam frames covering Shackleton floor under varying secondary illumination geometries.

## Public Redistribution

ShadowCam data is NASA public domain. However, raw and calibrated frames are NOT committed to this repository due to file size. Use `download.py` to retrieve frames from the PDS archive.

## Scope Decision (Sprint 1, final)

Only PDS-public ShadowCam products are in scope for this repo. Internal/team-restricted frames are out of scope for Sprint 1. This decision is final for the sprint.

## Citations

When using this data, cite:
- Robinson, M. S. et al. (2023). ShadowCam instrument and investigation overview. *Journal of Astronomy and Space Sciences*, 40(4), 149–171.
- Humm, D. C. et al. (2023). Calibration of ShadowCam. *Journal of Astronomy and Space Sciences*, 40(4), 173–197.

## Status

`download.py` skeleton committed May 3. Implementation scheduled for May 6.
