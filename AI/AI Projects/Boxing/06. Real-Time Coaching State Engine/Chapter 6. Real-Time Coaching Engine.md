---
title: Chapter 6 — The Real-Time Coaching State Engine
tags: [boxing, ai, hfsm, state-machine, coaching, feedback, adaptive-learning]
---

# Chapter 6: The Real-Time Coaching State Engine

## 6.1 Hierarchical Finite State Machines

The coaching engine should use explicit state rather than a loose collection of independent rules.

Top-level states:

1. Tracking acquisition
2. Calibration/framing validation
3. Neutral guard
4. Punch initiation
5. Dynamic strike tracking
6. Terminal evaluation
7. Guard recovery
8. Post-round summary

Each state can own smaller sub-state machines for punch class, punch phase, and technique checks.

A transition should require kinematic evidence, sufficient confidence, and a minimum dwell time.

## 6.2 Temporal Hysteresis

State chattering occurs when a value repeatedly crosses one threshold.

Use:

- enter threshold
- exit threshold
- confirmation window

Example:

warning enters only when a metric exceeds a high boundary for several frames, then remains active until the metric passes a lower boundary for several frames.

This prevents rapidly alternating voice and visual cues.

## 6.3 Real-Time Coaching Intervention Engine

Multiple technical errors can happen in the same repetition. Do not voice every error.

Priority order can emphasize:

1. core defensive/guard issues
2. stance and structural issues
3. trajectory issues
4. subtle timing inefficiencies

Only the highest-priority active issue should normally be spoken immediately.

Secondary errors can be displayed visually and stored for post-round analysis.

Use an audio refractory interval so the coach does not talk continuously.

## 6.4 Drill Progression and Adaptive Curricula

Track skill state for:

- stance
- jab
- cross
- hook
- slip
- other learned movements

An exponentially weighted moving average can estimate recent skill trend.

Example progression:

stance control
→ jab
→ jab-cross
→ combination
→ defense transitions
→ reaction drills
→ randomized training

The Markov Decision Process framing is useful for future adaptive systems, but the first implementation can use deterministic progression rules.

## 6.5 Real-Time Feedback Semantics

Bad feedback:

Technique incorrect.

Better feedback:

Rear hand dropped during jab extension.

The coach should distinguish:

- positive feedback
- corrective feedback
- wrong-sequence feedback
- input-quality/framing warnings

Never issue a confident joint-level correction when the affected keypoint is visually unreliable.

## Core Connections

- [[05. Biomechanical Modeling and Sequence Comparison/Chapter 5. Biomechanical Modeling]]
- [[07. Edge Inference Runtime and Optimization/Chapter 7. Edge Runtime and Optimization]]
- [[08. End-to-End System Synthesis and Verification/Chapter 8. System Synthesis and Verification]]
- [[readme|Final Technical Report — Real-Time AI Boxing Coach]]
