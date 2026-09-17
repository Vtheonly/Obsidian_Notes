---
tags: [synthetic, rgb, depth, bim]
---

# Synthetic RGB / Depth / BIM

> **Definition.** Generate synthetic datasets of buildings that include RGB images, depth maps, and BIM models, all consistent with each other.

## Why It Matters

Real BIM-annotated data is scarce. Synthetic data can:

- Train perception models (depth, segmentation, detection).
- Train BIM generation models.
- Test algorithms on edge cases (rare room layouts, unusual structures).
- Enable domain randomization.

## Pipeline

```
Procedural or neural building generator
  ↓
BIM model
  ↓
Render from virtual cameras
  ↓
RGB images + depth maps + segmentation masks + camera poses
  ↓
(BIM, RGB, depth, masks) tuples for training
```

## Tools

- **Blender / BlenderProc**: render photorealistic scenes from BIM.
- **Unity / Unreal**: real-time rendering, interactive scenes.
- **Habitat-Sim**: indoor scenes for embodied AI.
- **Custom**: combine IFC + rendering pipeline.

## Domain Randomization

Vary textures, lighting, object placement to make models robust to real-world variations.

## Sim-to-Real

Train on synthetic, transfer to real. Works best when:

- synthetic is photorealistic,
- domain gap is minimized,
- fine-tuning on small real data is used.

See [[Datasets and Synthetic Data]], [[Domain Randomization]], [[Sim to Real]].

## Related Concepts

- [[Datasets and Synthetic Data]]
- [[Domain Randomization]]
- [[Sim to Real]]
- [[BIM Generation]]
