---
tags: [bim-generation]
---

# BIM Generation (Canonical)

> **Definition.** Generating a BIM model (geometry + semantics + properties + relationships + hierarchy) from inputs (text, image, partial BIM, sketch, etc.).

## Approaches

| Approach         | Strengths                                  | Weaknesses                              |
| ---------------- | ------------------------------------------ | --------------------------------------- |
| Autoregressive   | Sequential conditioning; natural for BIM.  | Slow; error accumulation.               |
| Tree-based       | Natural fit for hierarchy; easy to constrain. | Custom architecture needed.             |
| Diffusion-based  | High quality; diverse.                     | Unstructured; hard to constrain.        |
| Constrained      | Always valid.                              | Over-constrains diversity.              |

## Hybrid Strategy

Combine multiple approaches:

1. Tree-based generator predicts the spatial hierarchy.
2. Autoregressive generator fills elements per node.
3. Diffusion generates per-element geometry.
4. Constraint validator checks the result.
5. Repair loop fixes violations.

See [[Autoregressive BIM]], [[Tree Based BIM]], [[Diffusion BIM]], [[Constrained BIM]].

## Why BIM Generation Is Hard

BIM is simultaneously:

- a tree (containment),
- a graph (relations),
- a collection of geometry,
- a set of properties,
- a set of materials,
- a code-compliant specification.

A BIM generator must produce all of these consistently. A generator that produces only geometry is **not** a BIM generator.

## Related Concepts

- [[Autoregressive BIM]]
- [[Tree Based BIM]]
- [[Diffusion BIM]]
- [[Constrained BIM]]
- [[BIM Validation]]
- [[BIM Fundamentals]]
