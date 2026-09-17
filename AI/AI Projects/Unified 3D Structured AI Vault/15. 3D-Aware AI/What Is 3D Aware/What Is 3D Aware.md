---
tags: [3d, awareness]
---

# What Is 3D-Aware (Recap)

This is a recap note pointing to the canonical definition. See [[What Is 3D Aware AI]] for the full content.

## Quick Recap

A model is **3D-aware** if it explicitly uses 3D geometric, spatial, or volumetric information.

Where it enters:

- 3D features (voxel, point, neural field).
- 3D attention (distance-weighted, ray-aware).
- 3D losses (Chamfer, IoU, normal consistency).
- 3D constraints (parallelism, orthogonality, support).
- 3D decoders (mesh, voxel, implicit).

Hard vs soft:

- Soft: a 2D diffusion model with depth preference.
- Hard: a 3D-aware decoder (e.g. voxel grid).
- Verified: multi-view consistency check.

See [[What Is 3D Aware AI]], [[3D Consistency]].

## Related Concepts

- [[What Is 3D Aware AI]]
- [[3D Consistency]]
- [[3D Generative Models]]
