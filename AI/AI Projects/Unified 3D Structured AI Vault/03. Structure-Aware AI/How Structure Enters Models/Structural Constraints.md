---
tags: [structure-aware, constraints]
---

# Structural Constraints

> **Definition.** *Structural constraints* restrict the model's output space so that structurally invalid outputs cannot be produced.

## Mechanisms

- **Grammar mask**: at each decoding step, only tokens that continue a valid grammar prefix are scored. Others are set to $-\infty$.
- **Schema validator**: candidates are checked against a schema (JSON schema, IFC schema, XML DTD) and rejected if invalid.
- **Tree decoder**: each step attaches a node to an existing parent; output is a tree by construction.
- **Graph decoder**: each step adds a node or edge to a partial graph; structural invariants are checked before acceptance.
- **Constraint solver**: a solver (SMT, CP) is queried at each step to determine which next actions are feasible.

## Strength

Hard guarantee on the constrained property.

## Limitation

- Only the property *explicitly constrained* is guaranteed.
- Computational cost (mask computation, solver calls).
- May over-restrict the model, reducing diversity.

See [[Hard Guarantees vs Statistical Preferences]], [[Constrained Decoding]].

## Related Concepts

- [[How Structure Enters Models]]
- [[Constrained Decoding]]
- [[Grammar Constrained Generation]]
- [[Schema Constrained Generation]]
- [[Hard Guarantees vs Statistical Preferences]]
