---
tags: [constraints, geometric, alignment]
---

# Alignment Constraints

> **Definition.** Constraints that certain elements are aligned: parallel, perpendicular, coaxial, coplanar, on-grid.

## Examples

- Walls parallel to building axes (X or Y).
- Columns on a regular grid.
- Beams level (horizontal).
- Beam axis aligned with column axis.
- Adjacent wall faces coplanar.

## Enforcement

- Compute alignment error (e.g. angle between element axis and target axis).
- Penalize / constrain.

## In Generation

Alignment-aware generation:

- Predict element orientations from a discrete set (e.g. 0°, 90°).
- Use grid constraints.

See [[Geometric Constraints]], [[Distance and Angle]].

## Related Concepts

- [[Geometric Constraints]]
- [[Distance and Angle]]
- [[Geometric Validation]]
