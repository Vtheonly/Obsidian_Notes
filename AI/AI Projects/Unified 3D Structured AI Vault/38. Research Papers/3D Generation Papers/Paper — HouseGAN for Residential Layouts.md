---
tags: [paper, 3d-generation, layout]
---

# Paper — HouseGAN for Residential Layouts (Illustrative Summary)

## Problem

Generating residential floor plans automatically from constraints (number of rooms, room types, adjacency requirements).

## Input

A bubble diagram: nodes = rooms (with type), edges = adjacency constraints.

## Output

A floor plan: a set of room rectangles with positions, sizes, and types.

## 3D Representation

2D (floor plan). 3D is not directly produced; the paper is 2D layout generation.

## Structural Representation

A graph (the bubble diagram) + a layout (set of rectangles with relations).

## Tree Representation

N/A.

## Graph Representation

Bubble diagram: nodes = rooms (with type), edges = adjacency constraints.

## BIM Representation

N/A (output is 2D rectangles, not IFC).

## Geometry Representation

Rectangles (axis-aligned).

## How Is Structure Represented?

The bubble diagram is an explicit graph given as input. The output is a layout where adjacency constraints should be satisfied.

## How Is Structure Learned?

The graph is given (not learned). The model learns to produce layouts that satisfy the graph.

## Where Does Structural Information Enter?

In the generator's conditioning: the bubble diagram is encoded and conditions the layout generation.

## Where Does 3D Information Enter?

N/A.

## Training Objective

Adversarial loss (GAN) + reconstruction loss.

## Loss Functions

GAN loss + L1 on layout.

## Generation Process

Graph-conditioned GAN: encode bubble diagram → generate layout.

## Constraints

Soft: the model prefers layouts that satisfy adjacency constraints. Hard constraints are not enforced.

## Validation

Implicit (visual inspection).

## Verification

N/A.

## Search

N/A.

## Repair

N/A.

## Failure Modes

- Adjacency constraints not satisfied.
- Rooms overlapping.
- Rooms with unrealistic aspect ratios.

## What Is Guaranteed?

Nothing (no hard guarantee).

## What Is Merely Probabilistic?

Everything (adjacency, sizes, positions are all probabilistic).

## Main Contribution

A GAN that generates residential floor plans conditioned on a bubble diagram.

## Limitations

- 2D only (not 3D, not BIM).
- No hard constraints.
- No verification.
- Limited to residential layouts.

## Related Concepts

- [[3D Generative Models]]
- [[Spatial Constraints]]
- [[Adjacency Constraints]]
- [[Scene Graph Fundamentals]]
- [[Layout Rewriting]]

## My Interpretation

This paper illustrates the "plausible but not verifiable" trap: the GAN produces layouts that look right but may violate adjacency constraints. A structure-aware / constrained version would enforce the bubble diagram as a hard constraint. For BIM generation, this means: don't just condition on structure; constrain generation by structure.
