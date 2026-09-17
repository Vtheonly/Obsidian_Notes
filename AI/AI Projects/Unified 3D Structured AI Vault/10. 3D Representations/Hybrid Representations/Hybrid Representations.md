---
tags: [3d, representations, hybrid]
---

# Hybrid Representations

> A *hybrid representation* combines multiple representations to get the strengths of each.

## Common Combinations

| Hybrid                          | Components                          | Use case                                |
| ------------------------------- | ----------------------------------- | --------------------------------------- |
| Mesh + texture                  | Mesh, image                         | Rendering.                              |
| Mesh + scene graph              | Mesh, graph                         | Scene understanding.                    |
| Point cloud + BIM               | Points, IFC                         | Scan-to-BIM.                            |
| Voxel + mesh                    | Voxels, mesh                        | Reconstruction + rendering.             |
| NeRF + scene graph              | Radiance field, graph               | Editable novel views.                   |
| Tree + graph + geometry         | Containment, relations, mesh        | Full building model (BIM-like).         |

## Why Hybrid

No single representation captures everything:

- **Geometry** needs explicit shapes (mesh, SDF, points).
- **Topology** needs graphs.
- **Hierarchy** needs trees.
- **Semantics** needs labels.
- **Appearance** needs images or radiance fields.

A complete building representation is hybrid by necessity. See [[Combining Trees Graphs and Geometry]].

## Consistency Challenge

Multiple representations must stay synchronized. See [[Cross Representation Consistency]].

## Research Direction

A unified differentiable representation that *is* all of these at once is an open problem. See [[Neural Representation Learning]], [[Neural + Formal Hybrid Systems]].

## Related Concepts

- [[3D Representations]]
- [[Representation Comparison]]
- [[Cross Representation Consistency]]
- [[Combining Trees Graphs and Geometry]]
