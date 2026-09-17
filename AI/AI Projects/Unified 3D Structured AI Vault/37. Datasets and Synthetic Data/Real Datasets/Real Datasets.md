---
tags: [datasets, real]
---

# Real Datasets

> Real-world datasets for training and evaluating 3D / BIM / structure-aware AI.

## Building / Architecture

- **CubiCasa5K**: 5000 floor plans.
- **LIFULL HOME's floor plan dataset**: 5M floor plans.
- **RPLAN**: 80K floor plans.
- **Structural3D**: structural engineering data.
- **ScanNet**: 1500 RGB-D scans of indoor scenes.
- **Matterport3D**: 90 large-scale building scans.
- **Gibson Environment**: 572 building scans.

## Point Clouds

- **ScanNet**: indoor.
- **Semantic3D**: outdoor.
- **KITTI**: autonomous driving scenes.
- **S3DIS**: Stanford large-scale indoor spaces.

## BIM-Specific

- **BIMViewSet**: IFC models with annotations.
- **BIMtools datasets**: various IFC test files.
- **IfcOpenShell test files**: IFC samples.

## Why It Matters

Real datasets:

- Ground models in real distributions.
- Provide evaluation benchmarks.
- Reveal data-specific challenges (noise, missing data, label imbalance).

## Limitations

- Limited scale (annotating BIM is expensive).
- Domain-specific (a residential dataset may not transfer to hospitals).
- Privacy, licensing.

See [[Synthetic Generators]], [[Domain Randomization]], [[Sim to Real]].

## Related Concepts

- [[Synthetic Generators]]
- [[Domain Randomization]]
- [[Sim to Real]]
