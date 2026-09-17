---
tags: [3d, representations, comparison]
---

# Representation Comparison

> Each 3D representation preserves some information and loses others. This note tabulates the trade-offs.

## Comparison Table

| Representation   | Geometry | Topology | Semantics | Hierarchy | Relations | Editable | Generatable | Validatable | BIM Convertible |
| ---------------- | -------- | -------- | --------- | --------- | --------- | -------- | ----------- | ----------- | --------------- |
| Point cloud      | Sampled  | None     | If labeled| No        | No        | Hard     | Yes         | Limited     | Hard            |
| Mesh             | Explicit | Surface  | If labeled| No        | No        | Medium   | Yes         | Yes         | Medium          |
| Voxel grid       | Discrete | Implicit | If labeled| No        | No        | Medium   | Yes         | Yes         | Medium          |
| Occupancy grid   | Discrete | Implicit | No        | No        | No        | Hard     | Yes         | Yes         | Hard            |
| TSDF             | Discrete | Implicit | No        | No        | No        | Hard     | Yes         | Yes         | Hard            |
| SDF              | Continuous| Implicit| No       | No        | No        | Medium   | Yes         | Yes         | Hard            |
| Neural field     | Continuous| Implicit| No       | No        | No        | Hard     | Yes         | Limited     | Hard            |
| Scene graph      | Implicit | Explicit | Yes       | Partial   | Yes       | Easy     | Yes         | Yes         | Easy            |
| Tree             | None     | Tree     | If labeled| Yes       | No        | Easy     | Yes         | Yes         | Medium          |
| BIM (IFC)        | Explicit | Explicit | Yes       | Yes       | Yes       | Easy     | Hard        | Yes         | Native          |
| CAD parametric   | Explicit | Implicit | Yes       | Feature tree | No    | Easy     | Hard        | Yes         | Medium          |
| CSG tree         | Implicit | Explicit | No        | Yes       | No        | Easy     | Yes         | Yes         | Medium          |

## Key Insight

- For **rendering**: mesh, NeRF.
- For **navigation / collision**: occupancy, TSDF.
- For **scene understanding**: scene graph + mesh.
- For **editing**: BIM, CAD, scene graph.
- For **generation**: depends on what you want — diffusion for mesh, tree decoder for BIM, neural field for novel views.
- For **validation**: BIM, scene graph, tree.
- For **BIM conversion**: scene graph, tree, CAD — these are already structured.

See [[3D Representations]], [[Cross Representation Consistency]].

## Related Concepts

- [[3D Representations]]
- [[Cross Representation Consistency]]
- [[Combining Trees Graphs and Geometry]]
