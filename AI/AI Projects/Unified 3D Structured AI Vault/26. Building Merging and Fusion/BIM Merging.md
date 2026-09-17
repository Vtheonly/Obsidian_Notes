---
tags: [merging, bim]
---

# BIM Merging

> **Definition.** Merging two BIM models into one. Not just mesh merging — semantic, topological, and hierarchy alignment are required.

See [[BIM Merging Overview]] and the [[26. Building Merging and Fusion]] subnotes for the full treatment.

## Quick Map

```mermaid
mindmap
  root((BIM Merging))
    Registration
      Coordinate alignment
      Pose graph
      ICP
    Semantic Alignment
      Type matching
      Property matching
      Material matching
    Conflict Detection
      Geometric
      Semantic
      Topological
      Metadata
      Hierarchy
    Conflict Resolution
      Priority
      Latest wins
      Manual review
      Solver
      Merge attributes
    Cross Representation Sync
      Mesh
      Scene graph
      Tree
      Properties
```

## Why Merging Is Hard

Two BIM models of the same building can disagree on:

- coordinate systems,
- element types,
- property values,
- connectivity,
- hierarchy.

A naive mesh-merge would produce duplicate elements and contradictions. BIM merging requires semantic alignment, conflict detection, and conflict resolution.

See [[Registration]], [[Semantic Alignment]], [[Conflict Detection]], [[Conflict Resolution]].

## Related Concepts

- [[Registration]]
- [[Semantic Alignment]]
- [[Conflict Detection]]
- [[Conflict Resolution]]
- [[Cross Representation Consistency]]
