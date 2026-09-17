---
tags: [hybrid, overview]
---

# Neural + Formal Hybrid Systems (Canonical)

> **Definition.** Systems that combine neural generation with formal representations, constraints, verification, search, and repair.

## Components

```mermaid
mindmap
  root((Neural Formal Hybrid))
    Neural Generation
      Diffusion
      Autoregressive
      Tree Decoder
      Graph Decoder
    Structural Representation
      Trees
      Graphs
      Scene Graphs
      BIM
    Geometry
      Meshes
      Voxels
      SDF
      Point Clouds
    Hard Constraints
      Grammar
      Schema
      Geometric
      Topological
      Semantic
    Verification
      Formal
      Neural
      Physics
      Hybrid
    Search
      Backtracking
      MCTS
      Beam
    Repair
      Localized
      Subtree Regeneration
      Iterative Refinement
```

## Why Hybrid

- Neural alone: plausible but not verifiable.
- Formal alone: verifiable but not scalable / not flexible.
- Hybrid: plausible + verifiable + scalable.

## Open Question

> Can hybrid systems produce outputs that are **both** plausible **and** verifiably valid?

This is the central research question of [[Neural + Formal Hybrid Systems]]. See [[Verifiable Generation]], [[Open Problem — Neural Formal Hybrid Generation]].

## Related Concepts

- [[Verifiable Generation]]
- [[Guided Search]]
- [[Differentiable Solvers]]
- [[Formal Verification]]
- [[Neural Verification]]
- [[Generate Validate Repair]]
