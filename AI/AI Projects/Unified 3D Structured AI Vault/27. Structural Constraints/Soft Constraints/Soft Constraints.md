---
tags: [constraints, soft]
---

# Soft Constraints

> **Definition.** Constraints that are *preferred* but not enforced. Violations are penalized (in loss or scoring) but not impossible.

## Mechanisms

- **Loss term**: add a penalty for constraint violation.
- **Attention bias**: bias attention toward constraint-satisfying configurations.
- **Scoring**: lower the score of violating outputs.

## Examples

- "Prefer" doors to be near room centers.
- "Prefer" windows on exterior walls.
- "Prefer" kitchens adjacent to dining rooms.

## Trade-offs

- **Pro**: more flexibility, more diversity.
- **Con**: no guarantee; violations can occur.

See [[Hard Constraints]], [[Hard Guarantees vs Statistical Preferences]].

## Related Concepts

- [[Hard Constraints]]
- [[Hard Guarantees vs Statistical Preferences]]
- [[Structural Scoring]]
