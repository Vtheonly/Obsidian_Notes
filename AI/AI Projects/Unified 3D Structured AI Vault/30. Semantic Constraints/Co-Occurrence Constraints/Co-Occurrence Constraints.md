---
tags: [constraints, semantic, co-occurrence]
---

# Co-Occurrence Constraints

> **Definition.** Constraints on which elements must (or must not) co-occur.

## Examples

- Kitchen contains sink + stove + fridge.
- Bathroom contains toilet + sink + (shower or bathtub).
- Bedroom contains bed.
- Living room contains seating.

- Bathroom not adjacent to kitchen.
- Bedroom not directly accessible from outside.

## Enforcement

- Per-room checks (does this kitchen have a sink?).
- Per-pair checks (is this bathroom adjacent to this kitchen?).

## Hard vs Soft

- Hard: code compliance (e.g. bathroom must have a toilet).
- Soft: cultural preferences (e.g. kitchen adjacent to dining).

See [[Semantic Constraints]], [[Semantic Validation]].

## Related Concepts

- [[Semantic Constraints]]
- [[Semantic Validation]]
- [[Type Constraints]]
