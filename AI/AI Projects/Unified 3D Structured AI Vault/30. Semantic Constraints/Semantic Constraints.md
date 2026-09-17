---
tags: [constraints, semantic]
---

# Semantic Constraints

> **Definition.** Constraints on the *meaning* of elements: types, attributes, co-occurrence, roles.

## Sub-Categories

- **Type constraints**: a "door" has door geometry; a "wall" has wall geometry.
- **Co-occurrence constraints**: a kitchen has a sink, stove, fridge.
- **Attribute constraints**: a fire-rated door has fire-rating ≥ F30.

See [[Type Constraints]], [[Co-Occurrence Constraints]], [[Attribute Constraints]].

## Examples

- A "kitchen" room contains at least one sink, one stove, one fridge.
- A "bathroom" room contains at least one toilet, one sink.
- A "fire-rated" door has `FireRating` ≥ F30.
- A "load-bearing" wall has `LoadBearing` = TRUE.
- An "exterior" wall has `IsExternal` = TRUE.

## Enforcement

- Rule-based (logical predicates).
- Learned (classifier).

See [[Semantic Validation]], [[Rule Based Verification]].

## Related Concepts

- [[Type Constraints]]
- [[Co-Occurrence Constraints]]
- [[Attribute Constraints]]
- [[Semantic Validation]]
