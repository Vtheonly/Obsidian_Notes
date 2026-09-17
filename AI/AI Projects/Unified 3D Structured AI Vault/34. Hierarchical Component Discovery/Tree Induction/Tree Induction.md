---
tags: [discovery, tree-induction]
---

# Tree Induction

> **Definition.** Build a tree structure that explains the data, by recursively partitioning or composing.

## Methods

- **Decision tree learning**: recursively split data on features.
- **Hierarchical clustering**: recursively merge similar items.
- **Grammar induction**: recursively learn production rules.
- **Recursive component discovery**: recursively discover and abstract components.

## Why It Matters

Trees are the natural structure for hierarchical data. Inducing a tree from raw data is a fundamental operation in:

- Building hierarchy reconstruction.
- BIM structure inference.
- Scene graph construction.
- Program synthesis.

## In Buildings

Given a flat list of elements (walls, doors, slabs), induce a tree:

```
Building
  - Storey 1
      - Room A
          - Wall, Wall, Wall, Wall
          - Door
          - Window
      - Room B
          - ...
  - Storey 2
      - ...
```

The tree is **induced** from the elements' geometry, adjacency, and containment.

See [[Recursive Component Discovery]], [[Grammar Induction]], [[Hierarchical Clustering]].

## Related Concepts

- [[Recursive Component Discovery]]
- [[Grammar Induction]]
- [[Hierarchical Clustering]]
- [[Building Hierarchies]]
