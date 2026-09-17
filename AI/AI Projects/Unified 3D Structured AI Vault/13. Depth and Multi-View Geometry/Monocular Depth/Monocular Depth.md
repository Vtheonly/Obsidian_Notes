---
tags: [3d, depth, monocular]
---

# Monocular Depth Estimation

> **Definition.** Predict a per-pixel depth map from a single RGB image.

## Why Hard

The mapping from RGB to depth is ambiguous: many 3D scenes project to the same 2D image. The model must use learned priors.

## Architectures

- **MiDaS**: trained on multiple datasets, scale-invariant loss.
- **DPT**: Vision Transformer for monocular depth.
- **ZoeDepth**: metric depth (not just relative).

## Losses

- **Scale-invariant loss**: $\|d - d^*\|^2 - \lambda (\bar d - \bar d^*)^2$.
- **Gradient loss**: match image gradients.
- **SSILogo**: structural similarity.

## Output

- A depth map $Z(u, v)$ per pixel.
- Either relative (scale unknown) or metric (scale known).

## Limitations

- Ambiguous: same image can have multiple plausible depths.
- Scale ambiguity (for relative depth).
- Failure on out-of-distribution scenes.

## Connection to 3D

Monocular depth + camera intrinsics → back-project to a point cloud. See [[Back Projection]].

See [[Stereo Depth]], [[Multi-View Stereo]], [[Back Projection]].

## Related Concepts

- [[Stereo Depth]]
- [[Multi-View Stereo]]
- [[Back Projection]]
- [[Camera Models]]
