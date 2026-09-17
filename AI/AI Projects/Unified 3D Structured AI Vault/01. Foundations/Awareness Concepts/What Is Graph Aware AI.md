---
tags: [foundations, awareness, graph-aware]
---

# What Is Graph-Aware AI

> **Definition.** A model is *graph-aware* if it represents or exploits arbitrary pairwise (or higher-arity) relationships between elements, not just hierarchical parent-child ones.

A tree is a special case of a graph. Graph-awareness allows:

- cycles,
- many-to-many relations,
- asymmetric or symmetric relations,
- typed edges (e.g. `adjacent-to`, `supports`, `connected-to`).

## Why Buildings Are Not Trees

Real buildings contain relationships that cannot be represented in a pure tree:

- A wall is adjacent to two rooms at once.
- A door connects two rooms.
- A beam is supported by two columns.
- Two pipes intersect.

A pure containment tree (building → floor → room → wall → window) cannot represent these. You need a graph alongside the tree.

See [[Why Buildings Are Not Purely Trees]], [[Combining Trees Graphs and Geometry]].

## What Information Makes the Model Aware?

- The **nodes** (objects, elements).
- The **edges** (typed relationships).
- The **edge attributes** (e.g. distance, contact area, direction).
- The **node attributes** (e.g. type, position, dimensions).

## Where Does It Enter?

- Graph neural networks (message passing along edges).
- Graph attention (attention weighted by edge type).
- Graph constraints (e.g. door must connect exactly two rooms).
- Graph decoders (predict nodes and edges).
- Scene-graph generation (image → objects + predicates).

See [[Graph Neural Networks]], [[Graph Attention]], [[Scene Graph Fundamentals]].

## Related Concepts

- [[What Is Tree Aware AI]]
- [[What Is Spatially Aware AI]]
- [[What Is Topology Aware AI]]
- [[Why Buildings Are Not Purely Trees]]
- [[Scene Graph Fundamentals]]
