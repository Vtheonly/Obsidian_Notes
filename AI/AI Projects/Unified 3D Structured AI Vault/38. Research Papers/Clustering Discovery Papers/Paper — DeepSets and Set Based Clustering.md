---
tags: [paper, clustering, sets, illustrative]
---

# Paper — DeepSets and Set-Based Clustering (Illustrative Summary)

## Problem

How to do machine learning on sets (unordered collections) in a way that is invariant to permutation.

## Input

A set of feature vectors $\{x_1, x_2, \dots, x_n\}$.

## Output

- A single vector (set encoding), or
- Per-element predictions, or
- Cluster assignments.

## 3D Representation

Sets are common in 3D (point clouds are sets of points).

## Structural Representation

Sets have no internal structure (by definition). However, set-based methods can be extended to structured outputs (graphs, trees).

## Tree Representation

N/A.

## Graph Representation

N/A (sets have no edges).

## BIM Representation

N/A.

## Geometry Representation

Sets of points / vectors.

## How Is Structure Represented?

No structure (sets are unstructured). This is the *opposite* of structure-aware.

## How Is Structure Learned?

N/A.

## Where Does Structural Information Enter?

N/A.

## Where Does 3D Information Enter?

In point clouds (sets of 3D points).

## Training Objective

Task-dependent (classification, regression, clustering).

## Loss Functions

Task-dependent.

## Generation Process

For set generation: sample elements one by one (autoregressive) or all at once (normalizing flow).

## Constraints

None (sets are unconstrained).

## Validation

N/A.

## Verification

N/A.

## Search

N/A.

## Repair

N/A.

## Failure Modes

- Permutation sensitivity (if the model is not properly permutation-invariant).
- Variable size (handling sets of different sizes).

## What Is Guaranteed?

Permutation invariance (if the model is correct).

## What Is Merely Probabilistic?

The actual set predictions.

## Main Contribution

A general framework for permutation-invariant learning on sets: $f(X) = \rho(\sum_{x \in X} \phi(x))$.

## Limitations

- No structure (sets are flat).
- Cannot model relations between elements.

## Related Concepts

- [[Point Clouds]]
- [[Embedding Based Clustering]]
- [[Deep Clustering]]
- [[What Is Structure Aware AI]] (contrast: sets are NOT structure-aware)

## My Interpretation

DeepSets is the canonical example of an *unstructured* representation. It is the baseline against which structure-aware methods should be compared. For buildings, treating elements as a set loses all adjacency, containment, and connectivity — which is why structure-aware methods (graphs, trees) outperform set-based methods on building tasks.
