---
tags: [exercise, 3d, voxels, meshes]
---

# Exercise — Voxel vs Mesh Trade-Off

## Problem

You are building a 3D-aware AI system for indoor scene understanding. You have two representation options:

- **Voxels** at $128^3$ resolution.
- **Mesh** with 50,000 triangles.

(a) Compute the memory cost of each (assume 4 bytes per voxel, 12 bytes per vertex + 4 bytes per triangle for indices, with 25,000 vertices).
(b) Discuss the trade-offs for: editing, generation, validation, BIM conversion.
(c) Which would you choose for: (i) generating building exteriors, (ii) editing a single wall, (iii) running a 3D CNN for semantic segmentation?

## Required Background

- Voxels: regular 3D grid; memory $O(n^3)$. See [[Voxels]].
- Meshes: vertices + faces; memory $O(V + F)$. See [[Meshes]].
- See [[Representation Comparison]].

## Correct Answers

### (a) Memory Cost

**Voxels**: $128^3 \times 4$ bytes $= 2{,}097{,}152 \times 4 = 8{,}388{,}608$ bytes $\approx 8.4$ MB.

**Mesh**: vertices $25{,}000 \times 12 = 300{,}000$ bytes; faces $50{,}000 \times 4 = 200{,}000$ bytes. Total $\approx 500$ KB.

Mesh is ~17× smaller.

### (b) Trade-offs

| Aspect            | Voxels                | Mesh                          |
| ----------------- | --------------------- | ----------------------------- |
| Editing           | Hard (grid cells).    | Easy (move vertices).         |
| Generation        | Easy (3D CNN).        | Hard (variable topology).     |
| Validation        | Easy (occupancy).     | Medium (manifoldness).        |
| BIM conversion    | Medium (segment + fit).| Medium (segment + fit).       |
| Resolution        | Limited by grid.      | High (adaptive).              |
| Topology          | Implicit.             | Explicit (surface).           |
| Semantics         | Per-voxel label.      | Per-face label.               |

### (c) Choices

(i) **Generating building exteriors**: Mesh. High resolution needed; mesh is more memory-efficient.

(ii) **Editing a single wall**: Mesh. Easy to move vertices; voxels would require updating many cells.

(iii) **Running a 3D CNN for semantic segmentation**: Voxels. 3D CNNs work naturally on voxel grids; meshes require special architectures.

## Common Mistakes

- Choosing voxels for high-resolution needs (memory blows up).
- Choosing mesh for 3D CNNs (architectures are more complex).
- Forgetting that both can be converted to each other (with loss).

## Edge Cases

- Sparse voxels (octrees) can compete with meshes on memory for sparse scenes.
- Subdivision surfaces can give meshes adaptive resolution.

## Implementation Considerations

- For BIM conversion, the choice between voxels and mesh matters less than the segmentation step that follows.
- Hybrid: voxels for perception, mesh for editing.

## Related Concepts

- [[Voxels]]
- [[Meshes]]
- [[Representation Comparison]]
- [[3D Representations]]
