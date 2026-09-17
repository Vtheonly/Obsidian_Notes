---
tags: [foundations, consistency]
---

# Cross-Representation Consistency

> **The deepest problem in this vault.** A building may simultaneously be represented as a point cloud, a mesh, a scene graph, a BIM model, a tree, a depth map, a set of semantic labels, and a CAD parametric model. How do all these representations stay synchronized?

## Why It Is Hard

Each representation captures a different aspect:

| Representation   | Captures                                       | Loses                          |
| ---------------- | ---------------------------------------------- | ------------------------------ |
| Point cloud      | Geometry (sampled)                             | Topology, semantics, hierarchy |
| Mesh             | Geometry + topology (surface)                  | Semantics, hierarchy           |
| Voxel grid       | Geometry (discrete) + occupancy                | Sharp features, semantics      |
| Scene graph      | Objects + relations                            | Continuous geometry            |
| Tree             | Hierarchy + containment                        | Graph relations, geometry      |
| BIM              | Geometry + semantics + relations + hierarchy   | Continuous appearance          |
| Depth map        | Projected geometry (per view)                  | 3D consistency, semantics      |
| Semantic labels  | Class per pixel / point / voxel                | Geometry, relations            |

If you change one representation, the others must follow:

- Remove a window from BIM → its geometry in the mesh must be filled, its semantic label must be removed, its scene-graph node must be deleted, its tree-leaf must be pruned.
- Reconstruct a wall from an image → its BIM representation must be created or updated, its tree position must be assigned, its scene-graph relations must be inferred.
- Discover a recurring window motif → the tree must be re-structured to use the new component, the BIM must reference the new type, the scene graph must update its relations.

## Consistency Strategies

1. **Single source of truth**: one representation is canonical; all others are *derived* and regenerated on change. Simple but expensive.
2. **Bidirectional sync**: every change is propagated to all representations. Powerful but conflict-prone.
3. **Event log**: changes are events; each representation consumes events and updates itself. Scalable but complex.
4. **Layered**: geometry layer → topology layer → semantics layer → hierarchy layer. Changes propagate upward only.
5. **Reconciliation**: representations are checked for consistency; inconsistencies trigger re-derivation.

## Failure Modes

- **Drift**: representations slowly diverge over many edits.
- **Conflict**: two representations disagree (e.g. mesh says wall is 0.20 m thick, BIM says 0.15 m).
- **Loss**: information present in one representation is lost in another (e.g. fire-rating in BIM but not in mesh).
- **Stale**: a representation was not updated after a change.

## Research Direction

A unified differentiable representation that *is* all of these at once (geometry + topology + semantics + hierarchy + relations) is an open problem. See [[Neural Representation Learning]], [[Neural + Formal Hybrid Systems]].

## Related Concepts

- [[Central Research Question]]
- [[Raw Data to Verified Structure Pipeline]]
- [[Building Merging]]
- [[Cross Representation Consistency]] (parent)
- [[Hybrid Representations]]
