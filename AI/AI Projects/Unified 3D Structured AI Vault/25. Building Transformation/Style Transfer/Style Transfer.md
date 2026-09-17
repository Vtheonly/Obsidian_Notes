---
tags: [building, transformation, style]
---

# Building Style Transfer

> Transform a building from one architectural style to another while preserving structure.

## Examples

- Modern → Classical.
- Brutalist → Minimalist.
- Residential → Commercial.
- 2D-only vs 3D-consistent.

## Approaches

- **2D image transfer**: render views, transfer style per view, then 3D-consistent fusion. (Risk: 3D inconsistency.)
- **3D style transfer**: transfer style on mesh / point cloud directly.
- **Latent transfer**: encode building into a latent; interpolate in latent space.

## Constraints

- Preserve topology (don't add/remove rooms).
- Preserve semantics (walls remain walls).
- Preserve structural validity (load paths remain).

See [[Building Transformation]], [[3D Consistency]], [[Structure Preserving Edits]].

## Related Concepts

- [[Building Transformation]]
- [[Layout Rewriting]]
- [[Structure Preserving Edits]]
- [[3D Consistency]]
