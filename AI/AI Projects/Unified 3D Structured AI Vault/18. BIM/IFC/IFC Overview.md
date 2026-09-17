---
tags: [bim, ifc]
---

# IFC Overview

> **Definition.** *IFC* (Industry Foundation Classes) is the open international standard for BIM data, maintained by buildingSMART. It is an object-oriented data model encoded in EXPRESS schema and serialized as STEP-21 (`.ifc`), ifcXML, or ifcJSON.

## Versions

- IFC2x3: widely supported, stable.
- IFC4: added more features, better geometry.
- IFC4.3: infrastructure (roads, bridges, rails).
- IFC5 (in development): more domains.

## Schema

IFC is defined by an EXPRESS schema. Key entities:

- `IfcRoot` (base): has GlobalId, OwnerHistory, Name, Description.
- `IfcObjectDefinition`: `IfcObject`, `IfcContext`, `IfcProcess`, etc.
- `IfcObject`: `IfcProduct` (physical things), `IfcGroup`, etc.
- `IfcProduct`: `IfcElement` (walls, slabs, ...), `IfcSpatialStructureElement` (sites, buildings, storeys, spaces).
- `IfcRelationship`: `IfcRelDecomposes`, `IfcRelConnects`, `IfcRelDefines`, `IfcRelAssociates`, `IfcRelAssigns`.
- `IfcRepresentation`: shape representations (Brep, swept solid, mapped).

## File Structure

A typical `.ifc` file:

```
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(...);
FILE_NAME(...);
FILE_SCHEMA(('IFC4'));
ENDSEC;
DATA;
#1 = IFCPROJECT(...);
#2 = IFCBUILDING(...);
...
#100 = IFCWALL(...);
#101 = IFCRELCONTAINEDINSPATIALSTRUCTURE(...);
ENDSEC;
END-ISO-10303-21;
```

## In This Vault

IFC is the canonical structured 3D representation. Tree-aware AI operates on its hierarchy; structure-aware AI operates on its relationships; BIM validation operates on its schema.

See [[IFC Entity Relationships]], [[IFC Spatial Structure]], [[IFC Property Sets]], [[BIM Fundamentals]].

## Related Concepts

- [[IFC Entity Relationships]]
- [[IFC Spatial Structure]]
- [[IFC Property Sets]]
- [[BIM Fundamentals]]
- [[BIM Validation]]
