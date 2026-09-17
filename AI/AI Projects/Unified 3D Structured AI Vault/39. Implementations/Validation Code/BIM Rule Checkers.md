---
tags: [implementation, validation, bim]
---

# BIM Rule Checkers

Reference for BIM-specific validators using IfcOpenShell.

```python
import ifcopenshell

def every_space_has_a_door(model):
    spaces = model.by_type("IfcSpace")
    doors = model.by_type("IfcDoor")
    issues = []
    for space in spaces:
        # Trace space boundaries to doors
        # (simplified; real check is more involved)
        boundaries = space.BoundedBy
        if not boundaries:
            issues.append(f"Space {space.GlobalId} has no boundaries")
    return issues

def every_element_contained_in_space(model):
    elements = model.by_type("IfcElement")
    issues = []
    for elem in elements:
        contained_in = elem.ContainedInStructure
        if not contained_in:
            issues.append(f"Element {elem.GlobalId} not contained in any space")
    return issues

def corridor_width_at_least(model, min_width=1.2):
    # Check all IfcSpace with name containing "corridor"
    corridors = [s for s in model.by_type("IfcSpace")
                 if s.Name and "corridor" in s.Name.lower()]
    issues = []
    for c in corridors:
        # Compute width from geometry (simplified)
        # ...
        pass
    return issues

def run_all_checks(model):
    issues = []
    issues += every_space_has_a_door(model)
    issues += every_element_contained_in_space(model)
    issues += corridor_width_at_least(model)
    return issues
```

See [[BIM Validation]], [[Rule Based Verification]].

## Related Concepts

- [[BIM Validation]]
- [[Rule Based Verification]]
- [[Geometric Checkers Library]]
