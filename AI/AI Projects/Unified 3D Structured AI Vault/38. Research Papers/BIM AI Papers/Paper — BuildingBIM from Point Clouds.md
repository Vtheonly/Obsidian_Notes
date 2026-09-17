---
tags: [paper, bim, scan-to-bim, illustrative]
---

# Paper — BuildingBIM from Point Clouds (Illustrative Summary)

## Problem

Automated "scan-to-BIM": convert a point cloud of a building into a BIM (IFC) model.

## Input

A point cloud of a building (interior or exterior, possibly with color and normals).

## Output

A BIM (IFC) model with walls, slabs, doors, windows, rooms, and their relationships.

## 3D Representation

Point cloud (input) + BIM (output).

## Structural Representation

BIM hierarchy (site → building → storey → space → element) + BIM relations (containment, connectivity).

## Tree Representation

The IFC spatial containment tree.

## Graph Representation

The IFC connectivity graph (door connects spaces, wall bounds spaces).

## BIM Representation

Full IFC: entities, properties, relationships, materials.

## Geometry Representation

Point cloud (input). Output: parametric geometry (extrusions, sweeps) per IFC element.

## How Is Structure Represented?

Explicitly as IFC entities and relationships.

## How Is Structure Learned?

The element types (wall, slab, door) are learned from labeled point clouds. The containment and connectivity are inferred from geometry.

## Where Does Structural Information Enter?

In the output structure (IFC entities and relationships).

## Where Does 3D Information Enter?

In the input (point cloud) and in the geometric attributes of output elements.

## Training Objective

Per-point segmentation loss + element detection loss + relationship prediction loss.

## Loss Functions

Cross-entropy (segmentation) + detection loss + relation classification.

## Generation Process

1. Segment point cloud (per-point class).
2. Cluster points into elements.
3. Fit primitives (planes, boxes).
4. Classify elements (wall, slab, etc.).
5. Build spatial hierarchy (rooms, storeys).
6. Predict relationships (containment, connectivity).
7. Output IFC.

## Constraints

Implicit (geometric fitting constrains element shapes).

## Validation

Compare generated BIM to ground-truth BIM (if available).

## Verification

N/A (typically).

## Search

N/A.

## Repair

N/A.

## Failure Modes

- Misclassification (a wall classified as a slab).
- Missing elements (a window not detected).
- Wrong hierarchy (a room assigned to wrong storey).
- Wrong relationships (a door not connected to the right spaces).

## What Is Guaranteed?

Nothing structural (the output IFC may be invalid).

## What Is Merely Probabilistic?

Everything (types, hierarchy, relationships are all probabilistic).

## Main Contribution

End-to-end scan-to-BIM with learned segmentation, classification, and relationship prediction.

## Limitations

- No structural / topological / semantic verification.
- No constraint enforcement during generation.
- Limited to detected element types.
- Geometry may not match IFC parametric definitions exactly.

## Related Concepts

- [[BIM Generation]]
- [[3D Reconstruction]]
- [[Semantic Segmentation]]
- [[Scene Graph Generation]]
- [[Geometric Validation]]
- [[Topological Validation]]
- [[Semantic Validation]]
- [[BIM Validation]]

## My Interpretation

Scan-to-BIM papers typically produce plausible BIM but not verifiable BIM. The pipeline is segmentation → clustering → fitting → classification → assembly. Each stage introduces errors that propagate. A constrained or verified version would enforce constraints at each stage and validate the final BIM. This is exactly the [[Open Problem — Verifiable BIM Generation]].
