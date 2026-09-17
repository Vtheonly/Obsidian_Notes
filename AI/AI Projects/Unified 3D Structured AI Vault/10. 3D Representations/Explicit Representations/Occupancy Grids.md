---
tags: [3d, representations, occupancy]
---

# Occupancy Grids

> An *occupancy grid* is a voxel grid where each voxel stores a binary (or probabilistic) value: is the voxel occupied by matter?

## Use Cases

- Robot navigation: which cells are free?
- Building scanning: which cells are inside walls?
- Collision checking: does the robot's path intersect obstacles?

## Probabilistic Occupancy

Each cell stores $P(\text{occupied})$. Updated by Bayesian filtering as new sensor readings arrive.

## Resolution Trade-off

- Coarse: fast, but misses thin structures (walls).
- Fine: detailed, but expensive (memory $O(n^3)$).

## Conversion

- To mesh: Marching Cubes on the occupancy field.
- To SDF: convert binary to signed distance.
- To BIM: segment occupied regions; fit primitives.

See [[Voxels]], [[TSDF]], [[SDF]].

## Related Concepts

- [[Voxels]]
- [[TSDF]]
- [[SDF]]
