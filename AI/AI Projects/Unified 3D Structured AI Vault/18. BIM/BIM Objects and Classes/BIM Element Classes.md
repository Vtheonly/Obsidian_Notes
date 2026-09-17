---
tags: [bim, classes]
---

# BIM Element Classes

> IFC defines a hierarchy of element classes. Each class has standard attributes, properties, and relationships.

## Major Classes

- **IfcWall**: vertical barriers.
- **IfcSlab**: horizontal planes (floors, roofs).
- **IfcColumn**: vertical load-bearing elements.
- **IfcBeam**: horizontal load-bearing elements.
- **IfcDoor**: openings that allow passage.
- **IfcWindow**: openings that allow light.
- **IfcRoof**: top cover of a building.
- **IfcStair**: vertical circulation.
- **IfcRailing**: protective barriers.
- **IfcFurnishingElement**: furniture, fixtures.

## Subclasses

Each major class has subclasses:

- `IfcWall` → `IfcWallStandardCase`, `IfcWallElementedCase`, `IfcWallArbitrary`.
- `IfcDoor` → `IfcDoorStandardCase`.

## Properties per Class

Each class has a predefined property set:

- `Pset_WallCommon` for walls.
- `Pset_DoorCommon` for doors.
- `Pset_SlabCommon` for slabs.

See [[BIM Objects]], [[IFC Property Sets]].

## Related Concepts

- [[BIM Objects]]
- [[Type vs Occurrence]]
- [[IFC Property Sets]]
