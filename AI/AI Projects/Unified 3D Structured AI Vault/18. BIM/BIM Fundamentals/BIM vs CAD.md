---
tags: [bim, cad]
---

# BIM vs CAD

| Aspect            | CAD                                   | BIM                                          |
| ----------------- | ------------------------------------- | -------------------------------------------- |
| Focus             | Geometry (lines, surfaces, solids).   | Whole-building information.                  |
| Elements          | Geometric primitives.                  | Typed objects (wall, door, slab).            |
| Properties        | Few / ad-hoc.                          | Rich (fire rating, U-value, manufacturer).   |
| Relationships     | Implicit (geometric only).             | Explicit (typed relations).                  |
| Hierarchy         | Implicit (layers, blocks).             | Explicit (spatial containment).              |
| Materials         | Visual only.                           | Structural, thermal, acoustic.               |
| Domain info       | None.                                  | Schedules, costs, code compliance.           |
| Use               | Drawing, detailing, fabrication.       | Whole lifecycle (design, construction, FM).  |

## Why It Matters

CAD gives you geometry. BIM gives you geometry *plus* everything else needed to design, build, operate, and decommission a building.

For AI: BIM is a *structured* representation; CAD is mostly *geometric*. Tree-aware and structure-aware methods apply naturally to BIM; CAD requires more inference.

See [[BIM Fundamentals]], [[BIM vs Mesh]], [[CAD and Parametric Modeling]].

## Related Concepts

- [[BIM Fundamentals]]
- [[BIM vs Mesh]]
- [[CAD and Parametric Modeling]]
- [[CAD to BIM]]
