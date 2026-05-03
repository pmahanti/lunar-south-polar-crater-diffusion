"""Download ShadowCam frames from the NASA PDS archive.

Skeleton committed May 3, 2026. Full implementation scheduled for May 6.

Plan:
- Pull a curated list of ShadowCam EDR/CDR products covering Shackleton crater floor
  from the PDS Imaging Node ShadowCam archive.
- Save under data/raw/ (gitignored). CDR products preferred; EDR retained for noise
  characterization.
- Verify checksums against PDS labels before declaring a frame usable.

PDS archive root (ShadowCam):
    https://pds.lroc.asu.edu/data/  # TODO: confirm exact ShadowCam path on May 6
"""

# TODO(May 6): implement frame list resolution from PDS index
# TODO(May 6): implement download with retry + checksum verification
# TODO(May 6): emit a manifest (frame_id, geometry, illumination conditions) to data/manifest.csv


def main() -> None:
    raise NotImplementedError("Scheduled for May 6 (data pipeline day).")


if __name__ == "__main__":
    main()
