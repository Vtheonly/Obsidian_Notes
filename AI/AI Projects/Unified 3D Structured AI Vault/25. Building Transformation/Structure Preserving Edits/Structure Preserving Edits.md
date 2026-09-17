---
tags: [building, transformation, structure-preserving]
---

# Structure-Preserving Edits

> Edits that modify a building's appearance or attributes while preserving its structure (topology, hierarchy, semantics).

## Examples

- Change material of a wall (keep geometry, keep type).
- Change fire rating of a door (keep everything else).
- Change surface finish (paint, texture).
- Swap a window type for another (same dimensions, different properties).

## Why It Matters

Structure-preserving edits are "safe" — they cannot break topology, hierarchy, or semantics. This makes them ideal for:

- Iterative design exploration.
- What-if analysis (what if all walls had a higher fire rating?).
- Style transfer at the attribute level.

## Constraints

- Topology unchanged.
- Hierarchy unchanged.
- Element types unchanged.
- Geometry unchanged (or within tolerance).
- Only attributes change.

## Validation

After a structure-preserving edit:

- Re-validate semantics (attributes are still meaningful).
- Re-validate geometry (still manifold, still consistent).
- Re-validate physics (still structurally sound).

See [[Building Transformation]], [[Layout Rewriting]], [[Semantic Validation]].

## Related Concepts

- [[Building Transformation]]
- [[Layout Rewriting]]
- [[Semantic Validation]]
