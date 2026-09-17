---
tags: [foundations, pipeline]
---

# Raw Data to Verified Structure Pipeline

```mermaid
mindmap
  root((Pipeline))
    Raw Data
      Images
      Depth Maps
      Point Clouds
      CAD Files
      Text
    Perception
      Segmentation
      Detection
      Pose Estimation
      Depth Estimation
    Representation
      Points
      Voxels
      Meshes
      Scene Graphs
      BIM
    Structure Discovery
      Clustering
      Motif Mining
      Grammar Induction
    Hierarchy
      Site
      Building
      Storey
      Room
      Element
    Graph
      Adjacency
      Connectivity
      Containment
      Support
    Geometry
      Distances
      Angles
      Volumes
      Normals
    BIM
      IFC Entities
      Property Sets
      Relations
    Generation
      Tree Generation
      Diffusion
      Autoregressive
    Transformation
      Layout Rewriting
      Style Transfer
    Merging
      Registration
      Alignment
      Conflict Resolution
    Validation
      Geometric
      Topological
      Spatial
      Structural
      Semantic
    Verification
      Formal Proof
      Physics Simulation
      SMT Solver
    Repair
      Localized Fix
      Subtree Regeneration
      Backtracking
```

Each stage consumes the output of the previous and adds new structure. Failures cascade: a bad segmentation produces a bad scene graph, which produces a bad BIM, which fails validation.

## Key Insight

The pipeline is **not** linear. Validation can feed back to perception (re-segment), to discovery (re-cluster), to generation (regenerate), or to repair (rewrite subtree). The strongest systems close this loop.

See [[Generate Validate Repair]], [[Cross Representation Consistency]].

## Related Concepts

- [[Central Research Question]]
- [[Cross Representation Consistency]]
- [[Generate Validate Repair]]
