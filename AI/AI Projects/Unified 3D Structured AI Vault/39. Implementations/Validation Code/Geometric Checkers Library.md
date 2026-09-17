---
tags: [implementation, validation, geometric]
---

# Geometric Checkers Library

A reference for common geometric validators.

```python
import numpy as np
import trimesh

def is_watertight(mesh):
    return mesh.is_watertight

def is_manifold(mesh):
    return mesh.is_watertight and len(mesh.euler_number) > 0

def no_self_intersection(mesh):
    return len(mesh.intersection(mesh).faces) == 0

def is_inside(point, mesh):
    return mesh.contains([point])[0]

def containment_ok(child_mesh, parent_mesh):
    # All vertices of child must be inside parent
    return all(is_inside(v, parent_mesh) for v in child_mesh.vertices)

def no_overlap(mesh_a, mesh_b):
    return len(mesh_a.intersection(mesh_b).faces) == 0

def vertical(normal, axis=np.array([0, 0, 1]), tol=1e-2):
    return abs(np.dot(normal, axis)) < tol

def horizontal(normal, axis=np.array([0, 0, 1]), tol=1e-2):
    return abs(np.dot(normal, axis) - 1) < tol
```

See [[Geometric Validation]], [[Validation Code]].

## Related Concepts

- [[Geometric Validation]]
- [[BIM Rule Checkers]]
- [[Topological Checkers]]
