---
tags: [constraints, structural]
---

# Structural Constraints

> **Definition.** Constraints on the *structural* behavior of a building: load paths, support, stability.

## Examples

- Every beam has at least 2 supports.
- Every column reaches the foundation.
- Every slab has at least 3 supports.
- Columns in a multi-storey building are aligned vertically.
- Lateral load resistance in both directions (bracing or shear walls).

## Hard vs Soft

- **Hard**: enforced during generation (constraint solver).
- **Soft**: preferred statistically (loss shaping).

See [[Hard Constraints]], [[Soft Constraints]], [[Constraint Solvers]].

## In Generation

A structural-aware BIM generator must:

- predict support relations (column supports beam),
- check load paths,
- ensure lateral stability.

A structural validator checks these post-generation.

See [[Structural Validation]], [[Physics Based Verification]].

## Related Concepts

- [[Hard Constraints]]
- [[Soft Constraints]]
- [[Constraint Solvers]]
- [[Structural Validation]]
