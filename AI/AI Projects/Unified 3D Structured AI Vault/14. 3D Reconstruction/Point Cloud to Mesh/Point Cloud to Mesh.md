---
tags: [3d, reconstruction, mesh]
---

# Point Cloud to Mesh

> **Definition.** Reconstruct a mesh from a point cloud.

## Algorithms

- **Poisson reconstruction**: solve a Poisson equation to find an indicator function whose gradient matches the normals.
- **Ball-pivoting**: roll a ball over the points; triangles form when the ball touches three points.
- **Alpha shapes**: convex hull variant.
- **Delaunay triangulation**: tetrahedralize, then extract surface.

## Inputs

- Point cloud.
- (Optional) per-point normals.
- (Optional) confidence / weight per point.

## Output

- Triangle mesh.

## Trade-offs

| Algorithm             | Robustness to noise | Needs normals? | Output watertight? |
| --------------------- | ------------------- | -------------- | ------------------ |
| Poisson               | High                | Yes            | Yes                |
| Ball-pivoting         | Medium              | Yes            | No                 |
| Alpha shapes          | Low                 | No             | Yes                |
| Delaunay              | Low                 | No             | Yes                |

## Use Cases

- Scan-to-mesh for visualization.
- Mesh-based editing.
- Mesh-based rendering.

See [[3D Reconstruction]], [[Meshes]], [[TSDF Fusion]].

## Related Concepts

- [[3D Reconstruction]]
- [[TSDF Fusion]]
- [[Meshes]]
