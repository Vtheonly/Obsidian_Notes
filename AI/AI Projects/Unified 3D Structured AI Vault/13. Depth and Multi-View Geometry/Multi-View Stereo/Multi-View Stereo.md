---
tags: [3d, depth, mvs]
---

# Multi-View Stereo (MVS)

> **Definition.** Reconstruct 3D geometry from multiple images taken from different viewpoints.

## Pipeline

1. **Structure from Motion** (SfM): estimate camera poses and a sparse point cloud.
2. **Dense matching**: for each image, match pixels to other images.
3. **Depth map fusion**: fuse per-view depth maps into a single 3D model.
4. **Mesh reconstruction**: Poisson, Delaunay.

## Algorithms

- **COLMAP**: classic SfM + MVS pipeline.
- **MVSNet**: deep MVS with cost volume.
- **PatchmatchNet**: learning-based patchmatch.

## Output

- Dense point cloud or mesh.

## Use Cases

- Aerial surveying.
- Building exterior reconstruction.
- Cultural heritage digitization.

## Limitations

- Requires many images with good overlap.
- Sensitive to texture and lighting.
- Fails on reflective / transparent surfaces.

See [[Stereo Depth]], [[3D Reconstruction]].

## Related Concepts

- [[Stereo Depth]]
- [[3D Reconstruction]]
- [[Camera Models]]
