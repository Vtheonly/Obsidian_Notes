---
tags: [bim, properties]
---

# Property Sets

> A *property set* is a collection of key-value properties attached to an element. See [[IFC Property Sets]] for the IFC encoding.

## Standard vs Custom

- **Standard**: `Pset_WallCommon`, `Pset_DoorCommon`, etc. Predefined by IFC.
- **Custom**: user-defined for project-specific data.

## Common Properties

For walls:
- `FireRating`: e.g. "F90".
- `LoadBearing`: TRUE / FALSE.
- `ThermalTransmittance`: W/(m²·K).
- `AcousticRating`: dB.
- `IsExternal`: TRUE / FALSE.

For doors:
- `FireRating`.
- `SecurityRating`.
- `GlazingAreaFraction`.

## Use in AI

Property sets are node attributes in the BIM graph / tree. A generator must predict:

- the type of property set to attach,
- the values of each property.

A validator must check that property values are within expected ranges (e.g. fire rating is a valid string).

See [[IFC Property Sets]], [[Quantity Sets]], [[Material Layer Sets]].

## Related Concepts

- [[IFC Property Sets]]
- [[Quantity Sets]]
- [[Material Layer Sets]]
- [[BIM Objects]]
