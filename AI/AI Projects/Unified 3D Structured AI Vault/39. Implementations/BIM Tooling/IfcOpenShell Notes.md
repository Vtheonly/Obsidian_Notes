---
tags: [implementation, bim, ifcopenshell]
---

# IfcOpenShell Notes

Practical notes on using IfcOpenShell.

## Common Operations

- `model.by_type("IfcWall")` — get all walls.
- `wall.Representation` — get geometry.
- `wall.ContainedInStructure` — get parent space.
- `wall.IsDefinedBy` — get property sets.
- `wall.HasAssociations` — get material associations.

## Gotchas

- IFC uses `GlobalId` (a 22-character string) as unique identifier; not an integer.
- Many-to-many relationships go through `IfcRel*` objects.
- Geometry is stored as `IfcShapeRepresentation` and requires interpretation.
- Some attributes are optional and may be `None`.

## Performance

- For large models, use `model.by_type` once and cache results.
- Avoid walking the full relationship graph repeatedly.

## Extensions

- `ifcopenshell.geom` — create geometry (tessellated meshes).
- `ifcopenshell.api` — create/modify IFC programmatically.

See [[IFC Parsing With IfcOpenShell]], [[IFC Overview]].

## Related Concepts

- [[IFC Parsing With IfcOpenShell]]
- [[IFC Overview]]
