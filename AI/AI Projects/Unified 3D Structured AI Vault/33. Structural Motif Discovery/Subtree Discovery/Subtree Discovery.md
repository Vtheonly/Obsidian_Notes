---
tags: [discovery, subtree]
---

# Subtree Discovery

> **Definition.** Discover recurring subtrees in a tree-structured representation (e.g. BIM hierarchy, AST).

## Examples

In a BIM hierarchy:

```
Building
  - Storey 1
      - Room A (kitchen)
          - Sink, Stove, Fridge
      - Room B (bathroom)
          - Toilet, Sink, Shower
  - Storey 2
      - Room C (kitchen)
          - Sink, Stove, Fridge    ← same subtree!
      - Room D (bathroom)
          - Toilet, Sink, Shower   ← same subtree!
```

The "kitchen" and "bathroom" subtrees are recurring.

## Methods

- **Frequent subtree mining** (FREQT, TreeFinder).
- **Embedded subtree mining** (allows descendants, not just direct children).
- **Approximate subtree mining** (allows small differences).
- **MDL-based**: find subtrees that compress the tree.

## Why It's Hard

- Subtree isomorphism is in P but expensive.
- Number of candidate subtrees is exponential.
- Approximate matching is fuzzy.

## Connection to Other Discovery

Subtree discovery is the **tree** analog of [[Subgraph Discovery]]. Together they cover tree and graph views.

See [[Structural Motif Discovery]], [[Subgraph Discovery]], [[Recursive Component Discovery]].

## Related Concepts

- [[Structural Motif Discovery]]
- [[Subgraph Discovery]]
- [[Recursive Component Discovery]]
