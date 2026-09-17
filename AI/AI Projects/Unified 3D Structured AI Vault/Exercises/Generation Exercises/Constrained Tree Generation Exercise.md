---
tags: [exercise, generation, constrained, tree]
---

# Exercise — Constrained Tree Generation

## Problem

You are generating a small BIM hierarchy with constraints:

- The root must be `IfcBuilding`.
- The root must have at least 1 and at most 5 `IfcBuildingStorey` children.
- Each `IfcBuildingStorey` must have at least 1 `IfcSpace` child.
- Each `IfcSpace` must have at least 3 `IfcWall` children.
- Each `IfcWall` may have 0 or more `IfcWindow` / `IfcDoor` children.

(a) Describe how to enforce these constraints during tree generation.
(b) What is the minimum valid tree?
(c) What goes wrong if you generate freely and validate afterward?

## Required Background

- Tree generation: see [[Tree Generation]], [[Tree Decoding]].
- Constrained generation: see [[Constrained Decoding]], [[Tree and Graph Constrained Generation]].

## Correct Answers

### (a) Enforcing Constraints During Generation

At each step of tree generation, the decoder must:

1. **Pick an open node** (a node that can still have children).
2. **Determine valid child types** based on the parent's type and the current state:
   - If parent is `IfcBuilding`: valid child types = `IfcBuildingStorey` (only).
   - If parent is `IfcBuildingStorey`: valid child types = `IfcSpace` (only).
   - If parent is `IfcSpace`: valid child types = `IfcWall` (only).
   - If parent is `IfcWall`: valid child types = `IfcWindow`, `IfcDoor`, or stop.
3. **Determine valid count of children** based on constraints:
   - `IfcBuilding`: 1 to 5 storeys.
   - `IfcBuildingStorey`: ≥ 1 space.
   - `IfcSpace`: ≥ 3 walls.
   - `IfcWall`: ≥ 0 windows/doors.
4. **Mask out invalid predictions** in the decoder's logits.

This is constrained tree decoding: the output is always a valid tree by construction.

### (b) Minimum Valid Tree

```
IfcBuilding
  - IfcBuildingStorey
      - IfcSpace
          - IfcWall
          - IfcWall
          - IfcWall
```

(1 building, 1 storey, 1 space, 3 walls, no windows/doors.)

### (c) What Goes Wrong with Generate-Then-Validate

If you generate freely (no constraints) and validate afterward:

- The model may produce an `IfcBuilding` with 0 storeys (invalid).
- The model may produce an `IfcSpace` with 1 wall (invalid).
- The model may produce a wall as a child of a storey (wrong hierarchy).
- The validator catches these, but you've wasted computation on invalid samples.
- You may need many resamples to get a valid sample.

Constrained generation avoids this by preventing invalid outputs at each step.

## Common Mistakes

- Forgetting to mask out invalid child types (the model may predict a `IfcWall` as a child of `IfcBuilding`).
- Forgetting count constraints (the model may stop too early).
- Confusing "valid by construction" with "valid by checking".

## Edge Cases

- Some constraints depend on context (e.g. a "fire-rated" wall must have a fire-rated door). These require looking beyond the immediate parent.
- Cross-tree constraints (e.g. total window count ≤ 10) are harder to enforce locally.

## Implementation Considerations

Implement constrained tree decoding by:

1. Maintaining a partial tree state.
2. Computing valid actions at each step.
3. Masking the decoder's logits.
4. Sampling from the masked distribution.

## Related Concepts

- [[Tree Generation]]
- [[Tree Decoding]]
- [[Constrained Decoding]]
- [[Tree and Graph Constrained Generation]]
- [[Constrained BIM]]
- [[Hard Guarantees vs Statistical Preferences]]
