---
title: "SynPath-3D Technical Specification & System Architecture — Introduction"
tags: [synpath3d, architecture, canonical]
status: canonical
---

# SynPath-3D Technical Specification & System Architecture

This directory is the authoritative engineering specification for SynPath-3D.

## Canonical flow

\`\`\`text
Pocket ensemble
  ↓
Self-supervised Equiformer-Light
  ↓
HENF + CPDF
  ↓
Spatial planning
  ↓
24-class legal reaction
  ↓
263-D target prediction
  ↓
Top-128 catalog retrieval
  ↓
Contextual re-ranking
  ↓
Compliant PoE + energy-guided torus flow
  ↓
Physical / synthetic validation
  ↓
Pruned SubTB GFlowNet alignment
\`\`\`

## No longer canonical

- fixed M=5 TIF anchors;
- flat 75k synthon softmax;
- DPDA stack execution;
- 3D-RISM-only runtime solvation;
- independent Gaussian sidechain-noise receptor conditioning;
- mandatory DLS clash correction;
- mandatory MMFF94s generation cleanup.

Legacy material may remain for teaching and ablation context. It does not override the canonical component notes.
