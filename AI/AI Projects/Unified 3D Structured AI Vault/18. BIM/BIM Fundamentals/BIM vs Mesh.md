---
tags: [bim, mesh]
---

# BIM vs Mesh

| Aspect          | Mesh                              | BIM                                                |
| --------------- | --------------------------------- | -------------------------------------------------- |
| Geometry        | Triangles.                        | Parametric geometry (extrusions, sweeps, CSG).     |
| Semantics       | None (unless segmented).          | Element type, name, classification.                |
| Properties      | None.                             | Property sets, quantity sets.                      |
| Relationships   | None.                             | Containment, connectivity, type, material.         |
| Hierarchy       | None.                             | Site → Building → Storey → Space → Element.        |
| Editability     | Hard (low-level edits).           | Easy (change a property; geometry re-evaluates).   |
| File size       | Small (vertices + faces).         | Large (lots of metadata).                          |
| Use             | Visualization, rendering.         | Design, construction, FM.                          |

## Why It Matters

A mesh is the *output* of geometry. A BIM model is the *source* — the geometry is derived from the parametric definition.

For AI: a mesh is unstructured; BIM is highly structured. Tree-aware / structure-aware methods target BIM directly.

See [[BIM Fundamentals]], [[BIM vs CAD]], [[Meshes]].

## Related Concepts

- [[BIM Fundamentals]]
- [[BIM vs CAD]]
- [[Meshes]]
- [[3D Representations]]
