---
tags: [constraints, hard]
---

# Hard Constraints

> **Definition.** Constraints that *cannot* be violated. Output is invalid if any hard constraint is violated.

## Mechanisms

- **Grammar mask**: next token must satisfy grammar.
- **Schema validator**: reject outputs that violate schema.
- **Solver**: reject outputs that violate solver-checked constraints.
- **Decoder shape**: tree/graph decoder that cannot emit invalid structures.

## Examples

- A door must connect exactly 2 spaces.
- A wall must be contained in a storey.
- A column must have a support below it.

## Trade-offs

- **Pro**: hard guarantee.
- **Con**: may over-restrict diversity.

See [[Soft Constraints]], [[Hard Guarantees vs Statistical Preferences]].

## Related Concepts

- [[Soft Constraints]]
- [[Hard Guarantees vs Statistical Preferences]]
- [[Constraint Solvers]]
