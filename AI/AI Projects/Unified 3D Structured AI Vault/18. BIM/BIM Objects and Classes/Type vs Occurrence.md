---
tags: [bim, type, occurrence]
---

# Type vs Occurrence

> IFC separates the **type** (definition of a class of objects) from **occurrences** (instances of that type).

## Example

```
IfcDoorType "WoodenDoor_900x2100"
    - FireRating: F30
    - Material: Oak
    - Default dimensions: 900 x 2100 mm

IfcDoor #100 (occurrence of WoodenDoor_900x2100)
    - Placement: at room A
    - Geometry: standard

IfcDoor #101 (another occurrence)
    - Placement: at room B
    - Geometry: standard
```

The type defines shared properties; the occurrence defines its placement and instance-specific data.

## Why It Matters

- Reduces redundancy: 100 doors of the same type share one type definition.
- Enables consistency: change the type, all occurrences update.
- Supports generation: generate types first, then place occurrences.

## In Tree-Aware AI

A tree-aware BIM generator can:

1. Predict types (what types of walls/doors/windows exist?).
2. Predict occurrences (how many of each, where?).

See [[Tree Based BIM]], [[BIM Generation]].

## Related Concepts

- [[BIM Objects]]
- [[BIM Element Classes]]
- [[IFC Entity Relationships]]
