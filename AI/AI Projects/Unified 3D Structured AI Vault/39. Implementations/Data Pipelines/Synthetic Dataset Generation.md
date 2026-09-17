---
tags: [implementation, synthetic]
---

# Synthetic Dataset Generation

## Pipeline

1. Generate building model (procedural or neural).
2. Render from virtual cameras.
3. Save (building, RGB, depth, masks, poses) tuples.

## Tools

- **BlenderProc**: Python wrapper around Blender for synthetic data.
- **Habitat-Sim**: indoor scenes for embodied AI.
- **Unity / Unreal**: real-time rendering.

## Example (BlenderProc)

```python
import bpyproc as bproc

bproc.init()
objects = bproc.loader.load_obj("building.obj")
bproc.camera.add_camera_pose(...)
bproc.camera.set_resolution(640, 480)
data = bproc.renderer.render()
```

## In AI

Synthetic data trains:

- Depth estimation.
- Object detection.
- Semantic segmentation.
- BIM generation.

See [[Synthetic Generators]], [[Domain Randomization]], [[Sim to Real]].

## Related Concepts

- [[Synthetic Generators]]
- [[Domain Randomization]]
- [[Sim to Real]]
