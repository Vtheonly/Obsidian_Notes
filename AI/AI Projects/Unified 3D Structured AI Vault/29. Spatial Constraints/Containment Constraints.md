---
tags: [constraints, spatial, containment]
---

# Containment Constraints (Spatial)

> **Definition.** Spatial constraints that one element is contained in another.

See [[Containment]] for the geometric version; here we emphasize the spatial hierarchy aspect.

## Examples

- Each element in exactly one space.
- Each space in exactly one storey.
- Each storey in exactly one building.
- Each building in exactly one site.

## Enforcement

- Maintain containment tree.
- Check at each generation step.

See [[Containment Relationships]], [[Spatial Validation]].

## Related Concepts

- [[Containment Relationships]]
- [[Spatial Validation]]
- [[Containment]]
