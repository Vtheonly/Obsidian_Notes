---
title: Chapter 8 — End-to-End System Synthesis and Verification
tags: [boxing, ai, system-design, profiling, verification, benchmarking, failure-modes]
---

# Chapter 8: End-to-End System Synthesis and Verification

## 8.1 Complete Pipeline

CameraX / YUV
→ frame selection and ROI
→ RTMPose-S
→ One Euro filtering and confidence handling
→ body-relative normalization
→ kinematic features
→ ST-GCN
→ Tiny Temporal Transformer
→ movement and phase understanding
→ DTW and reference distribution
→ biomechanical evaluation
→ HFSM coaching state
→ visual/audio feedback
→ session analytics

Each stage should have one clearly defined responsibility.

## 8.2 Frame Budget

At 15 FPS:

budget ≈ 66.7 ms per processing cycle

Initial planning budget:

| Stage | Planning target |
|---|---:|
| Capture/conversion | 8–10 ms |
| Pose inference | 35–40 ms |
| Conditioning | 1–2 ms |
| Temporal models | 6–8 ms |
| Kinematics/comparison | 4–5 ms |
| State/UI decision | 3–4 ms |
| Remaining | headroom |

These are planning values, not measured Galaxy A30s results.

## 8.3 Diagnostic Profiling

Record:

- median latency
- P95 latency
- P99 latency
- effective pose FPS
- dropped frames
- model memory
- process RSS
- battery drain
- thermal rise
- thermal-throttling onset
- movement recognition accuracy
- phase recognition accuracy
- technique-error detection accuracy

Measure both each stage and the full pipeline.

## 8.4 Failure Modes

| Failure | Trigger | Response |
|---|---|---|
| Framing violation | head/feet leave frame | framing guidance; suppress unsafe critique |
| Low confidence | occlusion/blur | suppress affected feedback |
| Hand identity ambiguity | cross-body overlap | temporal tracking/context |
| Low lighting | poor image quality | lighting warning |
| Multiple people | background person | primary-person lock |
| Thermal overload | sustained temperature | reduce inference cadence |
| Stale frames | analyzer backlog | keep-latest strategy |
| State chatter | threshold oscillation | hysteresis + dwell |

## 8.5 Verification Matrix

### Stance

Test:

- correct stance
- narrow stance
- excessive width
- foot crossing
- guard asymmetry
- torso lean

### Punches

Test:

- jab
- cross
- lead hook
- rear hook
- uppercuts
- phase boundaries

### Combinations

Test:

- correct sequence
- wrong order
- missing movement
- extra movement
- timing variations

### Robustness

Test:

- different lighting
- different camera distances
- different heights
- different body proportions
- different clothes
- slow and fast execution
- partial occlusion
- background interference

## 8.6 Acceptance Criteria

The system must demonstrate:

1. reliable body tracking
2. stable keypoint streams
3. useful movement recognition
4. phase-aware analysis
5. specific coaching feedback
6. real-time responsiveness
7. graceful low-confidence behavior
8. repeatable physical-device benchmarks

Skeleton display alone is not a successful implementation.

## 8.7 First Implementation Slice

Camera
→ RTMPose-S
→ filtering
→ normalization
→ live skeleton
→ stance evaluation
→ jab detection
→ basic phase analysis
→ specific feedback

After this becomes reliable, expand into combinations, teacher-student motion modeling, free shadowboxing, reaction drills, and adaptive curricula.

## Core Connections

- [[01. Mathematical and Theoretical Foundations/Chapter 1. Foundations]]
- [[02. Mobile Vision and Real-Time Pose Estimation/Chapter 2. Mobile Vision and Pose]]
- [[05. Biomechanical Modeling and Sequence Comparison/Chapter 5. Biomechanical Modeling]]
- [[06. Real-Time Coaching State Engine/Chapter 6. Real-Time Coaching Engine]]
- [[07. Edge Inference Runtime and Optimization/Chapter 7. Edge Runtime and Optimization]]
- [[readme|Final Technical Report — Real-Time AI Boxing Coach]]
