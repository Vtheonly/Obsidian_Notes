---
tags: [validation, structural]
---

# Structural Validation

> **Definition.** *Structural validation* checks that the building's structure can support its loads: load paths are continuous, columns sit on beams, beams sit on columns or walls, slabs are supported, etc.

## Checks

| Check                       | Description                                                            |
| --------------------------- | --------------------------------------------------------------------- |
| Load path continuity        | Every load has a continuous path to the foundation.                   |
| Support count               | Beams have at least 2 supports; slabs have at least 3 supports.       |
| Column alignment            | Columns in a multi-storey building are aligned vertically.            |
| Slab-to-column ratio        | Slab is not too large for the columns supporting it.                  |
| Wall-to-slab connection     | Load-bearing walls connect to slabs above and below.                  |
| Lateral stability           | Building has bracing or shear walls in both directions.               |

## Algorithms

- **Graph analysis**: build a support graph (A supports B); check connectivity to foundation.
- **Static equilibrium**: solve $\sum F = 0, \sum M = 0$ under expected loads.
- **Finite element analysis** (FEA): full simulation if a coarse check passes.

## When It Catches Errors

- Beams with only one support.
- Columns that don't reach the foundation.
- Slabs with insufficient support.
- Missing lateral bracing.

## When It Misses

- Wrong material strength (requires FEA with material properties).
- Construction defects (not visible in model).

See [[Physics Based Verification]], [[Geometric Validation]].

## Related Concepts

- [[Physics Based Verification]]
- [[Geometric Validation]]
- [[Structural Constraints]]
