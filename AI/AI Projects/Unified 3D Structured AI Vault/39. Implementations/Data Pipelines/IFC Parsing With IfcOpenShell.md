---
tags: [implementation, ifc, ifcopenshell]
---

# IFC Parsing With IfcOpenShell

> **IfcOpenShell** is an open-source library for parsing, inspecting, and creating IFC files.

## Installation

```bash
pip install ifcopenshell
```

## Reading an IFC File

```python
import ifcopenshell

model = ifcopenshell.open("building.ifc")

# Get all walls
walls = model.by_type("IfcWall")
for wall in walls:
    print(wall.GlobalId, wall.Name)

# Get containment hierarchy
for storey in model.by_type("IfcBuildingStorey"):
    elements = [r.RelatedElements for r in storey.ContainsElements]
    print(storey.Name, elements)
```

## Inspecting Relationships

```python
# For each door, find the two spaces it connects
for door in model.by_type("IfcDoor"):
    fills = door.FillsOpenings
    for fill in fills:
        opening = fill.RelatingOpeningElement
        # ... trace to spaces
```

## Writing an IFC File

```python
from ifcopenshell.api import run

model = ifcopenshell.api.run("create.file")
project = run("root.create_entity", model, ifc_class="IfcProject")
# ... add buildings, storeys, walls, etc.
model.write("output.ifc")
```

## Use in AI

IfcOpenShell is the standard library for:

- Loading BIM models for ML.
- Extracting scene graphs from BIM.
- Validating generated BIM.
- Converting BIM to other formats.

See [[IfcOpenShell Notes]], [[IFC Overview]].

## Related Concepts

- [[IfcOpenShell Notes]]
- [[IFC Overview]]
- [[Point Cloud Loading and Voxelization]]
