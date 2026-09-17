---
tags: [bim, ifc, properties]
---

# IFC Property Sets

> IFC stores key-value properties in `IfcPropertySet`, attached to elements via `IfcRelDefinesByProperties`.

## Structure

```
IfcWall #100
    - IfcRelDefinesByProperties    IfcPropertySet "Pset_WallCommon"
         - IfcPropertySingleProperty "FireRating" = "F90"
         - IfcPropertySingleProperty "LoadBearing" = TRUE
         - IfcPropertySingleProperty "ThermalTransmittance" = 0.3
         - ...
```

## Predefined vs Custom

- **Predefined property sets**: standardized by IFC (e.g. `Pset_WallCommon`, `Pset_DoorCommon`).
- **Custom property sets**: user-defined, for project-specific data.

## Quantity Sets

`IfcElementQuantity` stores measurable quantities:

- `IfcQuantityArea`: net area, gross area.
- `IfcQuantityVolume`: net volume, gross volume.
- `IfcQuantityLength`: length, perimeter.
- `IfcQuantityWeight`: weight.
- `IfcQuantityCount`: count.

## Material Layer Sets

A wall typically has multiple material layers:

```
IfcMaterialLayerSet
    - IfcMaterialLayer "Brick" (thickness 0.10)
    - IfcMaterialLayer "Insulation" (thickness 0.08)
    - IfcMaterialLayer "Air gap" (thickness 0.04)
    - IfcMaterialLayer "Drywall" (thickness 0.013)
```

Attached to the wall via `IfcRelAssociatesMaterial`.

See [[Property Sets]], [[Quantity Sets]], [[Material Layer Sets]].

## Related Concepts

- [[Property Sets]]
- [[Quantity Sets]]
- [[Material Layer Sets]]
- [[IFC Overview]]
