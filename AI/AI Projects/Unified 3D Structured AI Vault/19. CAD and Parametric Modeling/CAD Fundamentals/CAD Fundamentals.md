---
tags: [cad, fundamentals]
---

# CAD Fundamentals

> **Definition.** *Computer-Aided Design (CAD)* is the use of software to create, modify, and document geometric designs.

## What CAD Provides

- **Geometric primitives**: points, lines, arcs, splines, surfaces, solids.
- **Parametric modeling**: shapes defined by parameters and constraints.
- **Feature trees**: history of construction operations.
- **Constraints**: geometric (parallelism, tangency) and dimensional (length, angle).
- **Assemblies**: hierarchical composition of parts.

## CAD vs BIM

See [[BIM vs CAD]]. CAD focuses on geometry; BIM adds semantics, properties, relationships, hierarchy.

## Parametric Modeling

A parametric model defines shapes as functions of parameters:

```
width = 1.0
height = 2.0
rectangle(width, height) → extrude(thickness=0.1)
```

Change a parameter, the geometry re-evaluates. This makes CAD models editable and procedural.

## Feature Trees

See [[Feature Trees]]. A feature tree is the construction history:

```
Sketch(profile)
    - Extrude(depth=0.5)
      - Cut(sketch2, depth=0.2)
        - Fillet(edges, radius=0.02)
```

Each node is an operation; the tree is the program that builds the geometry.

## In This Vault

CAD is interesting because:

- **Feature trees are trees**: CAD models are tree-structured.
- **Parametric definitions are programs**: CAD is program synthesis.
- **Constraints are formal**: CAD uses constraint solvers.

CAD is therefore a natural domain for [[Tree Generation]], [[Program Induction]], [[Constrained Generation]].

See [[Feature Trees]], [[Constructive Solid Geometry]], [[Shape Grammars]], [[CAD to BIM]].

## Related Concepts

- [[Feature Trees]]
- [[Constructive Solid Geometry]]
- [[Shape Grammars]]
- [[CAD to BIM]]
- [[BIM vs CAD]]
