---
tags: [merging, semantic-alignment]
---

# Semantic Alignment

> **Definition.** Match elements from two BIM models based on their semantic content (type, properties), not just geometry.

## Why It's Needed

Two BIM models of the same building may:

- use different element types (one says `IfcWall`, the other says `IfcWallStandardCase`),
- have different property sets (one has `FireRating`, the other doesn't),
- have different element names ("Wall_01" vs "W-A1"),
- have slightly different geometries.

Pure geometric matching may miss the correspondence. Semantic alignment matches by:

- type (with type hierarchy),
- properties,
- name (with string similarity),
- material,
- placement.

## Algorithm

1. For each element in model A, compute a feature vector (type, properties, geometry, position).
2. For each element in model B, compute the same.
3. Match (e.g. with Hungarian algorithm on a similarity matrix).
4. Validate matches (e.g. with geometric consistency).

## Conflicts

After matching, two corresponding elements may have:

- different geometries (which one is correct?),
- different properties (which value?),
- different materials (which?).

See [[Conflict Detection]], [[Conflict Resolution]].

## Related Concepts

- [[BIM Merging]]
- [[Registration]]
- [[Conflict Detection]]
- [[Conflict Resolution]]
