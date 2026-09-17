---
tags: [exercise, bim, validation]
---

# Exercise — BIM Validation

## Problem

You are given a BIM model with the following potential issues. For each, identify:

- which validation type catches it (geometric / topological / spatial / structural / semantic),
- whether it's a hard or soft violation.

Issues:

1. A wall's geometry extends outside its storey's bounding box.
2. A door is not connected to any space.
3. A "kitchen" room has no sink.
4. A column does not reach the foundation.
5. Two rooms overlap.
6. A "fire-rated" door has no `FireRating` property.
7. A corridor is 0.8 m wide.
8. A wall's geometry is not watertight.

## Required Background

- Validation types: see [[Geometric Validation]], [[Topological Validation]], [[Spatial Validation]], [[Structural Validation]], [[Semantic Validation]], [[BIM Validation]].
- Hard vs soft: see [[Hard Guarantees vs Statistical Preferences]].

## Correct Answers

| # | Issue                                                  | Validation Type      | Hard/Soft        |
| - | ------------------------------------------------------ | -------------------- | ---------------- |
| 1 | Wall extends outside storey.                           | Spatial / Geometric  | Hard (containment violation). |
| 2 | Door not connected to any space.                       | Topological          | Hard (door must connect 2 spaces). |
| 3 | Kitchen has no sink.                                   | Semantic             | Soft (cultural norm) or hard (code in some jurisdictions). |
| 4 | Column doesn't reach foundation.                       | Structural           | Hard (load path broken). |
| 5 | Two rooms overlap.                                     | Spatial / Geometric  | Hard (non-overlap rule). |
| 6 | Fire-rated door missing `FireRating`.                  | Semantic             | Hard (attribute required). |
| 7 | Corridor is 0.8 m wide (min 1.2 m).                    | Code compliance      | Hard (code violation). |
| 8 | Wall geometry not watertight.                          | Geometric            | Hard (mesh must be closed for B-rep). |

## Step-by-Step Reasoning

1. **Wall outside storey**: containment constraint violated. The wall's geometry must be inside its parent storey. Hard.

2. **Door not connected**: a door must connect exactly two spaces (topological invariant). Hard.

3. **Kitchen without sink**: semantic expectation. Cultural norm in many places; some building codes require a sink in a kitchen. Depends on jurisdiction.

4. **Column not reaching foundation**: structural load path broken. Hard.

5. **Overlapping rooms**: spatial non-overlap rule violated. Hard.

6. **Fire-rated door missing FireRating**: the attribute is required for the door's semantic role. Hard.

7. **Narrow corridor**: code compliance (typically corridors ≥ 1.2 m). Hard.

8. **Non-watertight wall geometry**: B-rep requires closed surfaces. Hard.

## Common Mistakes

- Treating semantic rules as soft when they are hard (e.g. fire-rating attributes).
- Treating cultural norms as hard when they are soft (e.g. kitchen-dining adjacency).
- Forgetting that code compliance is hard.

## Edge Cases

- A "kitchen" without a sink in a studio apartment (sink may be in a combined space).
- A column that reaches a beam (which then reaches the foundation): structural path is indirect but valid.

## Implementation Considerations

A BIM validator should run all checks and report violations with severity (hard / soft). Hard violations must be fixed; soft violations are warnings.

## Related Concepts

- [[Geometric Validation]]
- [[Topological Validation]]
- [[Spatial Validation]]
- [[Structural Validation]]
- [[Semantic Validation]]
- [[BIM Validation]]
- [[Hard Guarantees vs Statistical Preferences]]
