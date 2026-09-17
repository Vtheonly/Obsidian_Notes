---
tags: [bim, fundamentals]
---

# BIM Fundamentals

> **Definition.** *Building Information Modeling (BIM)* is a structured representation of a building that combines geometry, semantics, properties, relationships, hierarchy, spatial containment, and domain information.

## What BIM Adds Over a Mesh

A mesh is geometry only. A BIM model adds:

| Aspect              | Mesh  | BIM   |
| ------------------- | ----- | ----- |
| Geometry            | Yes   | Yes   |
| Semantics (types)   | No    | Yes   |
| Properties          | No    | Yes   |
| Relationships       | No    | Yes   |
| Hierarchy           | No    | Yes   |
| Spatial containment | No    | Yes   |
| Materials           | No    | Yes   |
| Domain information  | No    | Yes   |

See [[BIM vs CAD]], [[BIM vs Mesh]], [[What BIM Adds]].

## IFC

The standard open format for BIM is **IFC** (Industry Foundation Classes), maintained by buildingSMART. See [[IFC Overview]], [[IFC Entity Relationships]], [[IFC Spatial Structure]].

## Spatial Hierarchy

```
IfcSite
  - IfcBuilding
      - IfcBuildingStorey
          - IfcSpace
              - IfcElement (IfcWall, IfcSlab, IfcDoor, IfcWindow, ...)
```

See [[Building Hierarchies]], [[BIM Hierarchies]], [[IFC Spatial Structure]].

## Relationships

IFC defines relationships through `IfcRel*` entities:

- `IfcRelContainedInSpatialStructure`: element → space.
- `IfcRelAggregates`: whole → parts.
- `IfcRelConnectsElements`: element ↔ element.
- `IfcRelDefinesByType`: element → type.
- `IfcRelAssociatesMaterial`: element → material.

See [[IFC Entity Relationships]], [[BIM Relationships]].

## Properties

Each element has:

- **Property sets** (`IfcPropertySet`): key-value attributes (fire rating, U-value, manufacturer).
- **Quantity sets** (`IfcElementQuantity`): measurable quantities (area, volume, weight).
- **Material layer sets**: material composition (e.g. a wall with brick + insulation + drywall).

See [[Property Sets]], [[Quantity Sets]], [[Material Layer Sets]].

## In This Vault

BIM is the canonical example of a representation that simultaneously encodes:

- geometry,
- semantics,
- properties,
- relationships,
- hierarchy,
- spatial containment,
- domain information.

It is the natural target for [[BIM Generation]] and the natural subject of [[BIM Validation]] and [[BIM Merging]].

## Related Concepts

- [[BIM vs CAD]]
- [[BIM vs Mesh]]
- [[What BIM Adds]]
- [[IFC Overview]]
- [[Building Hierarchies]]
- [[BIM Hierarchies]]
- [[BIM Generation]]
- [[BIM Validation]]
- [[BIM Merging]]
