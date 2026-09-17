---
tags: [research, roadmap]
---

# Roadmap — Phased Research Plan

## Phase 1 — Foundations (Months 1-3)

- Study [[Foundations]]: awareness concepts, structure spectrum.
- Study [[Trees and Hierarchies]]: fundamentals, building/BIM hierarchies.
- Set up tooling: IFC parsing, rendering, validation.

## Phase 2 — Discovery (Months 4-6)

- Implement clustering methods (HDBSCAN, hierarchical).
- Implement motif discovery (subtree, subgraph).
- Implement recursive component discovery.
- Apply to a corpus of buildings.

## Phase 3 — Generation (Months 7-12)

- Implement tree-based BIM generator.
- Implement constrained BIM generator.
- Implement generate-validate-repair loop.
- Evaluate on quality, diversity, validity.

## Phase 4 — Verification (Months 13-18)

- Implement geometric, topological, semantic validators.
- Implement formal verification for critical properties.
- Integrate verification into generation loop.

## Phase 5 — Hybrid Systems (Months 19-24)

- Implement neural + formal hybrid generation.
- Implement verifiable generation.
- Scale to whole buildings.

## Milestones

- M3: Discovery pipeline producing meaningful motifs.
- M6: Tree-based BIM generator producing valid BIM.
- M12: Constrained generator with verifiable properties.
- M18: Hybrid system producing verifiably valid BIM.
- M24: Deployment-ready system.

See [[Open Problem — Verifiable BIM Generation]], [[Open Problem — Neural Formal Hybrid Generation]].

## Related Concepts

- [[Open Problem — Verifiable BIM Generation]]
- [[Open Problem — Neural Formal Hybrid Generation]]
- [[Open Problem — Recursive Discovery of Building Motifs]]
