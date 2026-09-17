---
tags: [merging, conflict-resolution]
---

# Conflict Resolution

> **Definition.** Resolve conflicts between two BIM models during merging.

## Strategies

| Strategy        | When to use                                                |
| --------------- | ---------------------------------------------------------- |
| Priority        | One model is authoritative; the other yields on conflicts. |
| Latest-wins     | Most recently updated element wins.                         |
| Manual review   | High-stakes conflicts (structural, safety).                |
| Solver          | Use a constraint solver to find a consistent resolution.   |
| Merge attributes| Combine property sets from both.                           |
| Geometric union | Take the union of geometries (when overlapping is OK).     |

## Example

Two BIM models of the same building, both with a wall W:

- A: W has `FireRating = F60`, thickness = 0.20 m.
- B: W has `FireRating = F90`, thickness = 0.15 m.

Resolution:

- If A is authoritative: use F60, 0.20 m.
- If B is more recent: use F90, 0.15 m.
- If structural engineer says F90 required: use F90, but with thickness 0.20 m (combining).
- If can't decide: flag for manual review.

## Cross-Representation Impact

Resolving a conflict in the BIM model must propagate to:

- the mesh (geometry changes),
- the scene graph (relations may change),
- the tree (hierarchy may change),
- the properties (attributes change).

See [[Cross Representation Consistency]], [[BIM Merging]].

## Related Concepts

- [[BIM Merging]]
- [[Conflict Detection]]
- [[Semantic Alignment]]
- [[Cross Representation Consistency]]
