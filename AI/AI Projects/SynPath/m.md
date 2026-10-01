---
title: "SynPath-3D Canonical Project Map"
tags: [synpath3d, moc, architecture, canonical]
status: canonical
---

# SynPath-3D Canonical Project Map

This file replaces the former large working specification with a contradiction-free project map.

## Authoritative source

The canonical architecture is defined in:

[[SynPath-3D Technical Specification & System Architecture/0. 1. Master Architectural Overhaul and Canonical Revision]]

and its component notes under:

[[SynPath-3D Technical Specification & System Architecture/1. 1. Overall System Architecture and Modular Decomposition]]

## Canonical model

~~~text
3–5 POCKET CONFORMERS
        ↓
SELF-SUPERVISED 6-LAYER EQUIFORMER-LIGHT
        ↓
HENF + CPDF
        ↓
HANDLE-CENTERED SPATIAL PLANNER
        ↓
24-CLASS LEGAL REACTION
        ↓
263-D CONTINUOUS SYNTHON TARGET
        ↓
REACTION-FILTERED TOP-128 ANN RETRIEVAL
        ↓
IN-POCKET CROSS-ATTENTION RE-RANKING
        ↓
COMPLIANT PoE + ENERGY-GUIDED TORUS FLOW
        ↓
PHYSICAL + SYNTHETIC VALIDATION
        ↓
PRUNED SubTB GFlowNet ALIGNMENT
~~~

## Canonical training curriculum

**Stage 0:** structural self-supervision over a large leakage-controlled PDB-derived corpus.

**Stage 1:** experimental 3D grounding plus synthetic-route chemistry/retrieval supervision.

**Stage 2:** pruned SubTB alignment over legal/retrieved actions with entropy regularization and hard physical/synthetic validity gates.

## Retired production mechanisms

The following are not production architecture:

- independent Gaussian sidechain torsion perturbation as receptor dynamics;
- 3D-RISM-only runtime solvation;
- fixed M=5 TIF anchors;
- flat 75k synthon softmax;
- DPDA stack execution;
- rigid-only PoE with no compliance;
- mandatory DLS clash correction;
- mandatory MMFF94s generation minimization;
- unconstrained full-action SubTB.

These mechanisms may be discussed as theory, historical alternatives or ablations in explicitly labeled notes.

## Project-wide invariants

1. Receptor flexibility is represented by correlated conformer ensembles.
2. HENF is the runtime hydration representation.
3. CPDF is the runtime pharmacophore target field.
4. Catalog selection is hierarchical retrieval.
5. Reaction legality is finite-state handle-mask logic.
6. Geometry is compliant PoE plus torus flow.
7. Steric guidance is inside the flow field.
8. Stage 2 uses pruned SubTB support.
9. Physical and synthesis validity are hard gates.
10. Empirical values are benchmarked rather than assumed.

The technical-specification vault is the source of truth for implementation.
