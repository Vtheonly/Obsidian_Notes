---
tags: [cad, feature-tree]
---

# Feature Trees

See [[Feature Trees]] (canonical).

A feature tree is the construction history of a CAD model, expressed as a tree of operations. Each node is an operation; edges represent data flow.

## Why Feature Trees Are Trees

- Each operation has a single output (a solid or surface).
- Operations compose: the output of one becomes the input of the next.
- Branches arise when an operation takes multiple inputs (e.g. a boolean union of two solids).

## Example

```
Sketch(circle, radius=0.5)
    - Extrude(depth=1.0)
        - Cut(Sketch(rectangle, 0.2 × 0.3), depth=0.5)
            - Fillet(edges=[1,2,3], radius=0.05)
                - Pattern(count=5, axis=X, pitch=0.6)
```

## Connection to Other Trees

| Tree type        | Nodes                       | Edges                 |
| ---------------- | --------------------------- | --------------------- |
| AST              | Code constructs             | Syntactic containment |
| Expression tree  | Math operators / operands   | Evaluation order      |
| Feature tree     | CAD operations              | Construction history  |
| BIM hierarchy    | Spatial entities            | Containment           |

All are [[What Is Tree Aware AI|tree-aware]] targets.

## Program Synthesis View

A feature tree **is a program**. Generating a CAD model = synthesizing a program that builds it. See [[Program Induction]].

## Related Concepts

- [[CAD Fundamentals]]
- [[Constructive Solid Geometry]]
- [[Program Induction]]
- [[Tree Generation]]
- [[What Is Tree Aware AI]]
