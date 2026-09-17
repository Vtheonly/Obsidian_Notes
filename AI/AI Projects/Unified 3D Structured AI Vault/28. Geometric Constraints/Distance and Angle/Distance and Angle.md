---
tags: [constraints, geometric, distance]
---

# Distance and Angle Constraints

> **Definition.** Constraints on distances (lengths, sizes) and angles (corner angles, orientations).

## Examples

- Wall length in [0.5, 10] m.
- Wall thickness in [0.10, 0.30] m.
- Room area in [9, 100] m².
- Room aspect ratio in [0.5, 2.0].
- Corner angle = 90° ± 1°.
- Wall vertical: angle with Z axis ≤ 1°.
- Wall horizontal (for slab): angle with XY plane ≤ 1°.

## Enforcement

- Continuous constraints: solvers (SQP, interior point).
- Discrete constraints: integer programming.

## In Generation

A generator with distance/angle constraints:

- predicts parameters within bounds,
- checks at each step,
- repairs if out of bounds.

See [[Geometric Constraints]], [[Geometric Validation]].

## Related Concepts

- [[Geometric Constraints]]
- [[Alignment]]
- [[Geometric Validation]]
