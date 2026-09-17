---
tags: [validation, bim]
---

# BIM Validation

> **Definition.** *BIM validation* checks that a BIM model satisfies the IFC schema, domain rules, and project-specific requirements.

## Levels

1. **Schema validation**: the model is a valid IFC file (entities, attributes, relationships match the IFC schema).
2. **Model checking**: the model satisfies domain rules (e.g. "every space has at least one door").
3. **Model coordination**: multiple discipline models (architectural, structural, MEP) are consistent with each other (no clashes).
4. **Code compliance**: the model satisfies building codes (e.g. minimum corridor width, maximum travel distance to exit).

## Tools

- **IfcOpenShell**: parse and inspect IFC.
- **Solibri Model Checker**: rule-based BIM validation.
- **BIMcollab**: clash detection and issue tracking.
- **Custom validators**: encode project-specific rules.

## Common Rules

- Every `IfcSpace` is contained in exactly one `IfcBuildingStorey`.
- Every `IfcDoor` connects two `IfcSpace`s.
- Every `IfcWall` has a `Representation`.
- Corridors have width ≥ 1.2 m.
- Travel distance from any point to an exit ≤ 30 m.
- No clashes between structural, mechanical, and plumbing elements.

## When It Catches Errors

- Missing mandatory attributes.
- Wrong relationship cardinalities.
- Code violations.
- Clashes between disciplines.

## When It Misses

- Geometric errors not encoded as rules.
- Semantic errors not encoded as rules.
- Structural insufficiency (requires FEA).

See [[Geometric Validation]], [[Semantic Validation]], [[Rule Based Verification]].

## Related Concepts

- [[Model Checking]]
- [[Rule Based Verification]]
- [[IFC Entity Relationships]]
- [[Geometric Validation]]
- [[Semantic Validation]]
