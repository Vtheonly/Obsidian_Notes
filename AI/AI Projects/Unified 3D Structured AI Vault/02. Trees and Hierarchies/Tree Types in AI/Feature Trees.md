---
tags: [trees, cad, feature-tree]
---

# Feature Trees

> A **feature tree** is the construction history of a CAD model, expressed as a tree of parametric operations (sketch, extrude, cut, fillet, pattern).

## Example

```
Sketch(profile)
  - Extrude(depth=0.5)
      - Cut(sketch2, depth=0.2)
          - Fillet(edges=[1,2,3], radius=0.02)
              - Pattern(count=5, axis=X)
```

## Why Feature Trees Matter

- They are the **canonical editable representation** of a CAD model.
- They are a **program**: change a parameter and the geometry re-evaluates.
- They are a **tree** — see [[CAD and Parametric Modeling]].
- They are a natural target for [[Tree Generation]]: generate the program, not the mesh.

## Connection to Other Trees

| Tree type        | Nodes                       | Edges                 |
| ---------------- | --------------------------- | --------------------- |
| AST              | Code constructs             | Syntactic containment |
| Expression tree  | Math operators / operands   | Evaluation order      |
| Feature tree     | CAD operations              | Construction history  |
| BIM hierarchy    | Spatial entities            | Containment           |

All four are [[What Is Tree Aware AI|tree-aware]] targets.

## Related Concepts

- [[CAD and Parametric Modeling]]
- [[Constructive Solid Geometry]]
- [[Tree Generation]]
- [[Program Induction]]
