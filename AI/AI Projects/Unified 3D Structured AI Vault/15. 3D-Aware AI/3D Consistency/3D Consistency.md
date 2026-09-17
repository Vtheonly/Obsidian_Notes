---
tags: [3d, consistency]
---

# 3D Consistency

> **Definition.** A 3D-aware model produces outputs that are consistent across viewpoints, scales, and time.

## Types of Consistency

| Type                  | Property                                                       |
| --------------------- | -------------------------------------------------------------- |
| Multi-view consistency| The same 3D structure appears the same from all viewpoints.    |
| Scale consistency     | The scale of the 3D structure matches the real world (or a chosen unit). |
| Temporal consistency  | The 3D structure evolves smoothly over time (videos).          |
| Geometric consistency | Distances, angles, sizes satisfy geometric constraints.        |
| Topological consistency | Adjacency, connectivity, containment are correct.            |
| Semantic consistency  | Types, attributes, roles are correct.                          |

## Why It Matters

Without 3D consistency, a generator produces "hallucinated" 3D that looks plausible but isn't real:

- different views disagree,
- scale is wrong (a 10 m room becomes 100 m),
- topology is wrong (a closed room has a hole).

## Mechanisms to Enforce Consistency

- **3D representations**: voxels, meshes, neural fields — geometry is explicit.
- **Multi-view loss**: photometric consistency across views.
- **Geometric constraints**: parallelism, orthogonality, support.
- **Validation**: post-hoc geometric, topological, semantic checks.
- **Cross-representation sync**: keep mesh, scene graph, BIM consistent.

See [[What Is 3D Aware AI]], [[Cross Representation Consistency]], [[Consistency]].

## Related Concepts

- [[What Is 3D Aware AI]]
- [[Cross Representation Consistency]]
- [[Consistency]]
- [[3D Aware Generation]]
