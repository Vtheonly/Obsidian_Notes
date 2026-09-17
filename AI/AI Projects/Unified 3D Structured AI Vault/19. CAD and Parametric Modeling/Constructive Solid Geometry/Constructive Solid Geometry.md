---
tags: [cad, csg]
---

# Constructive Solid Geometry (CSG)

> **Definition.** *CSG* represents a solid as a tree of boolean operations on primitives.

## Primitives

- **Box**: dimensions, position.
- **Sphere**: radius, center.
- **Cylinder**: radius, height, axis.
- **Cone**: radius, height, axis.
- **Torus**: major radius, minor radius.

## Operations

- **Union** (∪): combine two solids.
- **Intersection** (∩): keep only the overlapping part.
- **Difference** (−): subtract one solid from another.

## CSG Tree

```
Union
  - Difference
      - Box(1, 1, 1)
      - Cylinder(r=0.2, h=1.5)
  - Sphere(r=0.5)
```

Each leaf is a primitive; each internal node is a boolean operation. The tree is a program that builds the solid.

## Why CSG Is Interesting

- **Tree-structured**: naturally fits tree-aware AI.
- **Editable**: change a primitive's parameter; the whole tree re-evaluates.
- **Boolean ops are formal**: easy to verify (no self-intersection, watertight by construction).
- **Compact**: small program, complex geometry.

## In AI

CSG trees are a natural target for [[Tree Generation]] and [[Program Induction]]. The model predicts the tree structure (operations, primitives, parameters).

See [[Feature Trees]], [[Tree Generation]], [[Program Induction]].

## Related Concepts

- [[Feature Trees]]
- [[Tree Generation]]
- [[Program Induction]]
- [[Surfaces and Solids]]
