---
tags: [image-to-3d, multi-view]
---

# Multi-View to 3D

> **Definition.** Reconstruct 3D from multiple images of the same scene.

See [[Multi-View Stereo]] for the canonical algorithm.

## Pipeline

```
Multiple RGB images (with poses)
  ↓
SfM (camera poses + sparse cloud)
  ↓
MVS (dense cloud or mesh)
  ↓
Surface reconstruction
  ↓
Mesh / point cloud
```

## Strengths

- 3D consistency is enforced (multi-view loss).
- Scales to large scenes (aerial, urban).

## Limitations

- Requires many images with good overlap.
- Sensitive to texture / lighting.
- Fails on reflective / transparent surfaces.

## In Buildings

Multi-view reconstruction is the basis for **scan-to-BIM**:

1. Scan building exterior / interior with camera or laser scanner.
2. Reconstruct mesh.
3. Segment mesh into elements.
4. Fit primitives.
5. Build IFC.

See [[Multi-View Stereo]], [[3D Reconstruction]], [[BuildingBIM from Point Clouds]].

## Related Concepts

- [[Multi-View Stereo]]
- [[3D Reconstruction]]
- [[Single Image to 3D]]
