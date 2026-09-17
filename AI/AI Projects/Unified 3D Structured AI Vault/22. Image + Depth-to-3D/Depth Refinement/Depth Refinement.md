---
tags: [image-depth, refinement]
---

# Depth Refinement

> **Definition.** Improve a raw depth map (from sensor or monocular estimation) for downstream 3D tasks.

## Why Refinement Is Needed

- Sensor noise (especially RGB-D cameras).
- Missing data (transparent surfaces).
- Multi-view inconsistency.
- Quantization (depth resolution).

## Methods

- **Bilateral filtering**: edge-preserving smoothing.
- **Joint bilateral**: use the RGB image to guide filtering.
- **Deep refinement**: a network predicts a refined depth from raw depth + RGB.
- **Multi-view fusion**: fuse multiple depth maps into a consistent TSDF.

## Multi-View Consistency

For multiple views of the same scene:

1. Estimate poses (SfM).
2. Back-project each depth map to 3D.
3. Check consistency: do corresponding pixels in different views give the same 3D point?
4. Average / fuse consistent estimates; reject outliers.

See [[Consistency]], [[TSDF Fusion]].

## Related Concepts

- [[Image Plus Depth to 3D]]
- [[Consistency]]
- [[TSDF Fusion]]
