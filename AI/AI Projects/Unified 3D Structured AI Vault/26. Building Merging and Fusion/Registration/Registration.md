---
tags: [merging, registration]
---

# Registration

> **Definition.** *Registration* aligns two or more 3D models into a common coordinate frame.

## Types

- **Point cloud registration**: align two point clouds (ICP, feature-based).
- **Mesh registration**: align two meshes.
- **BIM registration**: align two BIM models (with semantic alignment).

## ICP (Iterative Closest Point)

Standard algorithm:

1. For each point in source, find closest point in target.
2. Compute optimal transform (rotation + translation) minimizing point-to-point distances.
3. Apply transform.
4. Repeat until convergence.

Variants:

- Point-to-plane ICP (use surface normals).
- Generalized ICP (plane-to-plane).
- Robust ICP (reject outliers).

## Feature-Based Registration

1. Detect features (SIFT, FPFH) in both models.
2. Match features.
3. Compute transform from matches (RANSAC for robustness).
4. Refine with ICP.

## BIM Registration

BIM models have semantic content (types, properties) that point clouds lack. Registration can use:

- Geometric alignment (mesh-based).
- Semantic matching (match walls to walls, doors to doors).
- Hybrid.

See [[BIM Merging]], [[Coordinate Frames]], [[Transformations]].

## Related Concepts

- [[BIM Merging]]
- [[Coordinate Frames]]
- [[Transformations]]
- [[Semantic Alignment]]
