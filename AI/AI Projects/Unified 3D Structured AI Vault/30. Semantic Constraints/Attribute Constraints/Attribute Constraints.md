---
tags: [constraints, semantic, attributes]
---

# Attribute Constraints

> **Definition.** Constraints on the values of element attributes.

## Examples

- `FireRating` ∈ {F30, F60, F90, F120}.
- `LoadBearing` ∈ {TRUE, FALSE}.
- `ThermalTransmittance` (U-value) ≤ 0.3 W/(m²·K) for exterior walls.
- `AcousticRating` (STC) ≥ 50 for walls between dwellings.
- `IsExternal` ∈ {TRUE, FALSE}.

## Enforcement

- Type checking (attribute is of correct type).
- Range checking (value within bounds).
- Cross-attribute checking (e.g. if `IsExternal = TRUE` then `ThermalTransmittance` ≤ threshold).

See [[Semantic Constraints]], [[Semantic Validation]], [[Property Sets]].

## Related Concepts

- [[Semantic Constraints]]
- [[Semantic Validation]]
- [[Property Sets]]
