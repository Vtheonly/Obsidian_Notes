---
tags: [constraints, geometric]
---

# Geometric Constraints

> **Definition.** Constraints on geometric properties: distances, angles, areas, volumes, alignment, containment, manifoldness.

## Sub-Categories

- **Distance and angle**: wall thickness, room dimensions, corner angles.
- **Alignment**: walls parallel to axes, columns on grid, beams level.
- **Containment**: object inside parent.
- **Manifoldness**: mesh is watertight, orientable.

See [[Distance and Angle]], [[Alignment]], [[Containment]].

## Examples

- Wall thickness in [0.10, 0.30] m.
- Room area in [9, 100] m².
- Corner angles = 90° (for rectangular rooms).
- Walls vertical (normal aligned with Z axis within 1°).
- Mesh watertight (every edge has exactly 2 faces).

## Enforcement

- **Hard**: solver-based, post-validation.
- **Soft**: loss term.

See [[Hard Constraints]], [[Soft Constraints]].

## Related Concepts

- [[Distance and Angle]]
- [[Alignment]]
- [[Containment]]
- [[Hard Constraints]]
- [[Geometric Validation]]
