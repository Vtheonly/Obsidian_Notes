---
tags: [bim, objects]
---

# BIM Objects

> A *BIM object* is a typed entity with geometry, properties, relationships, and material assignment.

## Examples

| Type             | Subclasses                                            |
| ---------------- | ----------------------------------------------------- |
| IfcWall          | IfcWallStandardCase, IfcWallElementedCase.            |
| IfcSlab          | Floor, Roof, Landing.                                 |
| IfcColumn        | IfcColumnStandardCase.                                |
| IfcBeam          | IfcBeamStandardCase.                                  |
| IfcDoor          | + DoorType, DoorStyle.                                |
| IfcWindow        | + WindowType, WindowStyle.                            |
| IfcRoof          | Flat, Pitched, Hip.                                   |
| IfcStair         | + StairFlightType.                                    |

## Anatomy

```
IfcWall
  - GlobalId (unique identifier)
  - Name, Description
  - ObjectPlacement (position in parent frame)
  - Representation (geometry)
  - RelDefinesByType → IfcWallType
  - RelDefinesByProperties → IfcPropertySet
  - RelAssociatesMaterial → IfcMaterialLayerSet
  - RelContainedInSpatialStructure → IfcSpace
```

See [[BIM Element Classes]], [[Type vs Occurrence]].

## Related Concepts

- [[BIM Element Classes]]
- [[Type vs Occurrence]]
- [[IFC Overview]]
