---
tags: [implementation, point-cloud, voxel]
---

# Point Cloud Loading and Voxelization

## Loading Point Clouds

```python
import numpy as np
import open3d as o3d

pcd = o3d.io.read_point_cloud("scan.ply")
points = np.asarray(pcd.points)
colors = np.asarray(pcd.colors)
normals = np.asarray(pcd.normals)
```

## Voxelization

```python
# Voxel grid
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(
    pcd, voxel_size=0.05
)
voxels = voxel_grid.get_voxels()
```

## Custom Voxelization

```python
def voxelize(points, voxel_size):
    indices = (points // voxel_size).astype(int)
    grid = {}
    for i, idx in enumerate(indices):
        key = tuple(idx)
        if key not in grid:
            grid[key] = []
        grid[key].append(i)
    return grid
```

## In AI

- Convert point clouds to voxel grids for 3D CNNs.
- Compute features per voxel (occupancy, density, color).
- Use sparse voxels for large scenes.

See [[Point Clouds]], [[Voxels]], [[Feature Extraction]].

## Related Concepts

- [[Point Clouds]]
- [[Voxels]]
- [[Feature Extraction]]
