---
tags: [3d, depth, consistency]
---

# Multi-View Consistency

> **Definition.** A property of multi-view 3D outputs: the same 3D structure must be consistent across all views.

## Geometric Consistency

A 3D point $p$ projected into two views gives image points $p_1, p_2$ satisfying the **epipolar constraint**:

$$p_2^T F p_1 = 0$$

where $F$ is the fundamental matrix.

## Photometric Consistency

The same 3D point should have the same color in all views (under Lambertian assumption):

$$I_1(p_1) \approx I_2(p_2)$$

Violations indicate non-Lambertian surfaces, occlusions, or errors.

## Depth Consistency

A 3D point's depth should be the same when reconstructed from different view pairs. Depth maps from different views should agree where they overlap.

## In Generation

A 3D-aware generator produces outputs that are multi-view consistent. A 2D generator (e.g. naive image diffusion) does not — it can produce inconsistent views of the "same" object.

See [[3D Consistency]], [[What Is 3D Aware AI]], [[3D-Aware AI]].

## Related Concepts

- [[Multi-View Stereo]]
- [[3D Consistency]]
- [[What Is 3D Aware AI]]
