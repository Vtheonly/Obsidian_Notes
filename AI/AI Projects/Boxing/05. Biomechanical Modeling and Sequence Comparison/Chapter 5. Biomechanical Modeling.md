---
title: Chapter 5 — Biomechanical Modeling and Sequence Comparison
tags: [boxing, ai, biomechanics, dtw, scoring, motion-reference]
---

# Chapter 5: Biomechanical Modeling and Sequence Comparison

## 5.1 Kinetic Chains of Boxing

A strike is a coordinated sequence across the body rather than an isolated arm action.

Useful chain abstraction:

foot/base
→ knee and hip
→ pelvis
→ torso
→ shoulder/scapula
→ elbow
→ hand

Study the temporal relationship of segment angular velocities rather than assuming one universal fixed timing.

### 5.1.1 Kinetic Chain Evaluation

The system can investigate:

- arm-only initiation
- insufficient lower-body contribution
- unstable base
- excessive torso compensation
- poor recovery
- guard-hand drop

### 5.1.2 Punch Phase Decomposition

Five useful phases:

1. Preparation
2. Initiation
3. Acceleration
4. Peak extension
5. Retraction/recovery

The state engine can use wrist velocity, acceleration, articulation, trajectory, guard position, and recovery direction to identify these phases.

## 5.2 Dynamic Time Warping

### 5.2.1 Dynamic Programming

Two similar punches can have different durations.

DTW finds a monotonic alignment path minimizing cumulative local distance.

D(i,j) = cost(i,j) + min(
    D(i-1,j),
    D(i,j-1),
    D(i-1,j-1)
)

This lets a slower repetition be compared to a faster reference without imposing rigid one-to-one frame correspondence.

A mobile implementation should reuse memory efficiently and avoid unnecessary allocation.

### 5.2.2 Sakoe-Chiba Band

Constrain the alignment with:

|i - j| <= R

This reduces computation and prevents pathological temporal stretching.

The radius R should be tuned from the real dataset.

## 5.3 Multi-Reference Distribution Modeling

A single reference punch is too rigid.

Build references from many athletes and repetitions covering:

- different body proportions
- orthodox and southpaw
- multiple speeds
- different camera distances
- legitimate stylistic variation

For aligned phase tau:

x_ref(tau) ~ Gaussian(mu(tau), Sigma(tau))

Evaluate a user point using Mahalanobis distance:

D_M = sqrt((x - mu)^T Sigma^-1 (x - mu))

High-variance dimensions are penalized less; highly consistent technical dimensions are penalized more.

## 5.4 Decomposed Biomechanical Scoring

Avoid a mysterious single percentage.

Recommended components:

1. trajectory accuracy
2. kinetic timing and velocity
3. guard discipline
4. stance stability
5. temporal rhythm and recovery

A trajectory score can be derived from accumulated reference-distribution distance.

The output should explain the reason for a low component score.

Example:

Trajectory: strong
Guard discipline: weak
Stance stability: strong
Recovery: moderate

This produces actionable coaching instead of a black-box number.

## 5.5 Expert Annotation

Reference distributions require expert-defined technical meaning.

The dataset should label events such as:

- rear hand drop
- elbow flare
- excessive lean
- poor recovery
- foot crossing
- weak base
- inefficient trajectory

Statistical similarity alone is not a substitute for expert knowledge.

## Core Connections

- [[03. Signal Conditioning, Normalization, and Kinematics/Chapter 3. Conditioning and Kinematics]]
- [[04. Spatial-Temporal Deep Learning Architectures/Chapter 4. Spatial-Temporal Deep Learning]]
- [[06. Real-Time Coaching State Engine/Chapter 6. Real-Time Coaching Engine]]
