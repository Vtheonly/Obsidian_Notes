---
tags: [exercise, generation, repair]
---

# Exercise — Generate Validate Repair

## Problem

You have a BIM generator that produces valid IFC 80% of the time. The other 20% have these issues:

- 10%: a door is not connected to any space.
- 5%: a wall has no geometry.
- 5%: a room has no door.

Design a generate-validate-repair loop that:

(a) Detects each issue.
(b) Localizes the error.
(c) Repairs it.
(d) Re-validates.

## Required Background

- Generate-validate-repair: see [[Generate Validate Repair]].
- Validation types: see [[BIM Validation]], [[Topological Validation]], [[Geometric Validation]], [[Semantic Validation]].

## Correct Answers

### (a) Detection

- **Door not connected**: topological check. For each `IfcDoor`, trace its `IfcRelConnectsElements` to spaces. If less than 2 spaces, flag.
- **Wall has no geometry**: geometric check. For each `IfcWall`, check `Representation` is not null and has valid geometry.
- **Room has no door**: topological check. For each `IfcSpace`, check that at least one `IfcDoor` connects it to another space.

### (b) Localization

- For each violation, record:
  - which entity (GlobalId),
  - which property / relation is missing,
  - which validator caught it.

### (c) Repair

- **Door not connected**:
  - Find the two spaces the door should connect (based on geometry: which spaces does the door's geometry lie between?).
  - Add `IfcRelConnectsElements` between the door and each space.
- **Wall has no geometry**:
  - Infer geometry from the wall's placement and parameters (length, height, thickness).
  - Generate the representation and attach it.
- **Room has no door**:
  - Find a suitable wall in the room (one that is shared with another room or corridor).
  - Add a door to that wall (create opening, fill with door, connect to both spaces).

### (d) Re-validation

After repair, run all validators again. If new issues appear (e.g. the added door now has a geometry conflict), repair those too. Loop until no issues remain (or a max iteration count is reached).

## Pseudocode

```python
def generate_validate_repair(generator, input, max_iter=10):
    output = generator(input)
    for i in range(max_iter):
        issues = validate(output)
        if not issues:
            return output
        for issue in issues:
            repair(output, issue)
    return output  # may still have issues
```

## Common Mistakes

- Repairing one issue and breaking another (e.g. adding a door creates a geometry conflict).
- Not re-validating after repair (assuming the repair worked).
- Letting the loop run forever (need a max iteration count).

## Edge Cases

- Some issues cannot be repaired automatically (e.g. a completely wrong building topology). Flag for human review.
- Multiple issues may interact (fixing one requires fixing another first).

## Implementation Considerations

- Log all repairs for auditing.
- Use a priority queue (fix hard violations before soft).
- Consider backtracking: if a repair makes things worse, undo and try a different repair.

## Related Concepts

- [[Generate Validate Repair]]
- [[BIM Validation]]
- [[Topological Validation]]
- [[Geometric Validation]]
- [[Semantic Validation]]
- [[Iterative Refinement]]
