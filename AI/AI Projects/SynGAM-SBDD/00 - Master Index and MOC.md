# SynGAM-SBDD

> [!abstract] Project
> **Formal Academic Title:** Structure-Based Molecular Generation via Reaction-Graph-Aware Decoding with Retrosynthetic Guarantees  
> **Short Codename:** **SynGAM-SBDD** — *Synthesis-Graph-Aware Module for Structure-Based Drug Design*  
> **Plain-English Pitch:** Design 3D molecules directly inside protein pockets while constraining generation to real chemical building blocks and validated reaction pathways, so synthesizability is part of the generation process rather than a post-hoc filter.

## 1. Project Identity

### Formal Academic Title

**Structure-Based Molecular Generation via Reaction-Graph-Aware Decoding with Retrosynthetic Guarantees**

### Short Project Codename

**SynGAM-SBDD**  
*Synthesis-Graph-Aware Module for Structure-Based Drug Design*

### Core Thesis Idea

Current structure-based drug-design systems can optimize molecules for geometric fit and predicted binding properties while leaving chemical synthesis as a downstream problem. SynGAM-SBDD explores a different formulation:

> Treat molecular generation as **structured decoding over a reaction grammar**, while simultaneously conditioning generation on the continuous 3D geometry of a protein binding pocket.

The central analogy is to **TAMER** for handwritten mathematical expression recognition: rather than generating an unconstrained flat sequence, the model incorporates structural constraints during decoding.

---

# 2. The TAMER Analogy

TAMER demonstrated the value of structure-aware recognition for handwritten mathematical expressions.

The important conceptual transfer is:

| Mathematical Expression Recognition | SynGAM-SBDD |
|---|---|
| Handwritten mathematical expression | Protein binding pocket |
| LaTeX output | Designed molecular structure |
| Mathematical syntax | Chemical reaction grammar |
| Expression tree / structured representation | Reaction graph / synthesis tree |
| Tree-aware decoding | Reaction-graph-aware decoding |
| Valid LaTeX structure | Valid synthesis pathway |

The key hypothesis is that the chemical analogue of a syntax tree is not merely the molecular atom-and-bond graph.

For this project, the more useful structural object is the **retrosynthetic / reaction graph** describing how the molecule can be assembled from starting materials through chemically valid transformations.

---

# 3. The Core Problem

## 3.1 Geometry Alone Is Not Enough

Many 3D molecular generative approaches formulate drug design primarily as a geometric generation problem.

The model receives a protein pocket and generates atoms, bonds, coordinates, or molecular fragments that occupy the pocket.

This can produce molecules that appear attractive according to computational objectives such as:

- pocket complementarity,
- docking score,
- predicted binding affinity,
- geometric fit,
- hydrogen-bond interactions.

However, a molecule that scores well computationally is not automatically a molecule that a chemist can readily synthesize.

This creates a gap:

**3D plausibility ≠ synthetic accessibility.**

## 3.2 The Synthesizability Wall

A generated molecule may subsequently fail because:

- no practical retrosynthetic route can be found,
- required intermediates are unavailable,
- reaction conditions are incompatible,
- functional groups interfere with one another,
- proposed transformations have poor precedent,
- the molecule contains chemically difficult or unstable structures,
- the generated structure falls outside the domain represented by available reaction templates.

Therefore, synthesizability should not necessarily be treated only as a final filtering step.

The central question becomes:

> **Can the generative process itself be constrained by the chemistry required to construct the molecule?**

---

# 4. The Central Technical Pivot

## From Atom Generation to Reaction-Structured Generation

The initial intuition was to introduce a graph-aware module that prevents invalid atom-to-atom connections.

That is useful, but insufficient.

An atom-level graph constraint can enforce local chemical validity such as valence and bond compatibility. It does not, by itself, guarantee that the resulting molecule has a practical synthesis.

The project therefore moves one level higher.

### Atom-Level Representation

The model asks:

> Can atom A connect to atom B?

### Reaction-Level Representation

The model asks:

> Can these chemically functionalized building blocks be connected using a known reaction class, under a valid reaction template, to produce the desired intermediate?

The second formulation is closer to the actual synthesis problem.

---

# 5. Reaction Graph as the Chemical Grammar

The proposed structured representation is a **reaction graph / synthesis tree / reaction DAG**.

### Nodes

Nodes represent:

- purchasable or catalogued chemical building blocks,
- synthesized intermediates,
- the current molecular intermediate.

### Edges

Edges represent:

- validated reaction classes,
- reaction templates,
- chemically compatible transformations.

Examples include:

- amide coupling,
- Suzuki-Miyaura cross-coupling,
- reductive amination,
- Buchwald-Hartwig coupling,
- alkylation,
- acylation.

The exact reaction vocabulary should ultimately be determined by the available reaction datasets and the scope selected for the thesis.

---

# 6. System Architecture

~~~text
                  3D PROTEIN POCKET
                         |
                         v
             +-------------------------+
             | SE(3)-Equivariant       |
             | Pocket Encoder          |
             |                         |
             | - Geometry              |
             | - Chemical environment |
             | - H-bond features       |
             | - Electrostatics        |
             +------------+------------+
                          |
                          v
              Continuous 3D Condition
                          |
                          v
             +-------------------------+
             | Reaction-Graph-Aware    |
             | Module (RGAM)           |
             |                         |
             | - Select reaction type  |
             | - Track reaction state  |
             | - Mask invalid actions  |
             | - Select building block |
             +------------+------------+
                          |
                          v
             Selected Block + Reaction
                          |
                          v
             +-------------------------+
             | Equivariant 3D Pose     |
             | & Torsion Module        |
             |                         |
             | - Rigid transform       |
             | - Coordinates           |
             | - Torsions              |
             | - Pocket collision check|
             +------------+------------+
                          |
                          v
             +-------------------------+
             | Structured Molecular    |
             | Output                  |
             |                         |
             | 1. Molecular structure  |
             | 2. 3D conformation     |
             | 3. Reaction graph       |
             | 4. Synthetic route     |
             +-------------------------+
~~~

---

# 7. Generation Process

## Step 1 — Encode the Protein Pocket

Input:

- protein structure,
- binding-pocket coordinates,
- atom types,
- local chemical environment,
- optional electrostatic or pharmacophoric features.

An **SE(3)-equivariant** neural architecture encodes the pocket so that transformations of the coordinate system are handled consistently.

The encoder produces a continuous representation of the spatial environment in which the ligand must be generated.

---

## Step 2 — Determine Valid Chemical Actions

The Reaction-Graph-Aware Module maintains the state of the growing molecule.

It observes:

- available functional handles,
- current reaction history,
- molecular scaffold,
- already-used building blocks,
- compatibility constraints.

The module then masks reaction actions that are not valid for the current state.

Conceptually:

$$
\mathcal{A}_t^{valid}
=
\{a \in \mathcal{A}: a \text{ is chemically compatible with state } S_t\}
$$

The generator samples only from:

$$
a_t \sim p(a_t \mid S_t, P)
$$

where:

- $S_t$ is the current synthesis state,
- $P$ is the encoded protein pocket,
- $a_t$ is the next reaction/building-block action.

---

# 8. Building-Block Selection

Instead of generating arbitrary atoms, the system retrieves or samples from a defined library of chemical building blocks.

Potential sources include commercial/catalogue-derived building blocks or public fragment libraries, subject to licensing and dataset availability.

The building-block representation may use:

- molecular fingerprints,
- graph neural embeddings,
- learned molecular embeddings,
- reaction-aware embeddings,
- 3D-aware embeddings.

The model then selects a candidate compatible with the current reaction state and the pocket-conditioned objective.

---

# 9. Continuous 3D Placement

Discrete chemical decisions are combined with continuous geometric generation.

Once a building block and reaction are selected, the geometric module predicts how the newly added component should be positioned.

Possible predicted variables include:

- translation $t \in \mathbb{R}^3$,
- rotation $R \in SO(3)$,
- torsional degrees of freedom,
- local conformational parameters.

The rigid-body transformation can be expressed as:

$$
x' = Rx + t
$$

with $R \in SO(3)$.

The objective is to position the newly generated structure so that it:

- occupies useful pocket volume,
- preserves chemically meaningful geometry,
- avoids severe protein clashes,
- maintains favorable interactions,
- remains compatible with the discrete synthesis state.

---

# 10. Dual-Stream Formulation

The core architecture therefore has two interacting streams.

### Discrete Stream

**Reaction grammar**

Controls:

- reaction type,
- building-block identity,
- functional-group compatibility,
- synthesis state,
- reaction sequence.

### Continuous Stream

**3D geometry**

Controls:

- molecular placement,
- orientation,
- torsion,
- pocket interaction,
- spatial compatibility.

The central research question is whether combining these streams produces molecules with a better joint trade-off between:

**binding/pocket quality + chemical validity + synthetic accessibility.**

---

# 11. Output

The intended output is not merely a molecular graph.

For each generated candidate:

### 1. Molecular Structure

A chemically valid molecular graph.

### 2. 3D Conformation

A pocket-conditioned 3D ligand pose.

### 3. Reaction Graph

The sequence of building blocks and reaction transformations used to construct the molecule.

### 4. Synthetic Route

A machine-readable and human-readable description of the proposed synthesis.

Conceptually:

~~~text
Building Block A
        |
        | Reaction 1
        v
Intermediate AB
        |
        | Reaction 2
        v
Building Block C
        |
        | Reaction 3
        v
Final Candidate
~~~

---

# 12. Why the Reaction Constraint Matters

The central claim of the project is not simply:

> "Our model generates valid molecules."

It is stronger:

> **The model incorporates synthesis constraints into generation instead of discovering synthesizability only after generation.**

This distinction is important.

### Post-Hoc Filtering

~~~text
Generate molecule
       |
       v
Check chemistry
       |
       v
Check retrosynthesis
       |
       v
Reject many candidates
~~~

### Structure-Aware Generation

~~~text
Protein pocket
      |
      v
Choose valid chemical action
      |
      v
Choose compatible building block
      |
      v
Place in 3D
      |
      v
Update reaction state
      |
      v
Repeat
      |
      v
Candidate + synthesis route
~~~

The second formulation makes chemical feasibility part of the search space itself.

---

# 13. Research Hypothesis

### Primary Hypothesis

A structure-based molecular generator that jointly models:

1. protein-pocket geometry,
2. discrete reaction grammar,
3. building-block selection,
4. continuous 3D placement,

can generate candidates with a better joint balance between binding-related objectives and synthetic accessibility than geometry-focused molecular generators without reaction-aware generation.

### Secondary Hypothesis

Reaction-aware structured decoding can reduce the proportion of generated candidates requiring extensive post-generation chemical repair or rejection.

---

# 14. Evaluation Framework

The evaluation should compare SynGAM-SBDD against appropriate structure-based molecular generation baselines.

Potential baselines include models such as:

- TargetDiff,
- DiffSBDD,
- other publicly available SBDD generative models appropriate to the final experimental setup.

The exact baseline set should be selected after reviewing the current literature and ensuring that comparisons use compatible datasets and evaluation protocols.

## Metrics

### A. Molecular Validity

Measure:

- valence validity,
- bond validity,
- sanitization success,
- structural validity.

### B. Synthetic Accessibility

Evaluate using appropriate retrosynthesis tools and metrics, potentially including:

- AiZynthFinder,
- Retro* / RetroStar-style systems,
- route existence,
- route length,
- reaction-template validity,
- building-block availability.

### C. Pocket Interaction

Potential metrics:

- docking score,
- pose quality,
- protein-ligand clashes,
- interaction recovery,
- hydrogen-bond interactions.

Possible tools include:

- AutoDock Vina,
- GNINA,
- other validated docking pipelines.

### D. Molecular Strain / Geometry

Potential measurements:

- force-field energy,
- bond-length deviations,
- angle deviations,
- torsional strain,
- conformational stability.

RDKit/MMFF-style evaluation may be considered where appropriate.

### E. Diversity

Measure whether reaction constraints collapse the generator into a narrow region of chemical space.

Possible metrics:

- molecular uniqueness,
- scaffold diversity,
- fingerprint diversity,
- reaction diversity,
- building-block diversity.

### F. Joint Utility

A central experiment should investigate the trade-off between:

$$
\text{Pocket Quality}
\quad \leftrightarrow \quad
\text{Synthetic Accessibility}
$$

rather than optimizing only one metric.

---

# 15. Critical Scientific Caveat

The project should **not** claim that selecting commercial building blocks and known reaction templates automatically guarantees that the final synthesis will succeed in a laboratory.

A computationally valid reaction graph is not equivalent to an experimentally validated synthesis.

Therefore, the strongest defensible wording is:

> **synthetic feasibility by construction under the defined reaction grammar and building-block constraints**

rather than:

> **100% guaranteed laboratory synthesis**

This distinction is important for a Master's thesis and should remain explicit throughout the project.

---

# 16. Dataset Strategy

Potential components include:

### Protein-Ligand Structures

**CrossDocked2020** or another suitable public protein-ligand benchmark.

### Reaction Data

A public reaction dataset suitable for:

- reaction-template extraction,
- reaction classification,
- reaction-center identification,
- retrosynthesis modelling.

### Building Blocks

A public or legally accessible building-block library should be used for the reproducible research version.

Commercial databases such as Enamine REAL can be discussed as motivation or future deployment targets, but the thesis implementation must respect licensing, access, redistribution, and reproducibility constraints.

---

# 17. Major Ideas Rejected

## Rejected: Pure Atom-Level GAM

A graph-aware module operating only on atom connectivity is insufficient.

It can enforce:

- valence,
- bond compatibility,
- graph validity.

But it does not necessarily encode:

- reaction feasibility,
- reagent requirements,
- protecting-group logic,
- reaction compatibility,
- retrosynthetic accessibility.

Therefore, the project moved from an **atom-level GAM** to a **reaction-graph-aware module**.

---

## Rejected: Pure 3D Generation

Generating atoms or fragments solely according to spatial fit leaves synthesis as a downstream problem.

This project instead treats 3D geometry as one stream of the generator rather than the entire representation.

---

## Rejected: Pure Retrosynthesis After Generation

A generate-first, retrosynthesize-later pipeline may waste substantial computation on candidates that cannot satisfy the desired synthesis constraints.

The proposed research direction instead investigates whether retrosynthetic structure can participate directly in generation.

---

# 18. The Core Novelty

The project is built around the intersection of three representations:

$$
\boxed{
\text{Protein Geometry}
+
\text{Reaction Grammar}
+
\text{Molecular 3D Geometry}
}
$$

The intended contribution is a generative framework in which:

- the protein pocket provides the spatial condition,
- the reaction graph provides the discrete chemical structure,
- the equivariant geometric model provides continuous 3D placement.

This is the conceptual heart of **SynGAM-SBDD**.

---

# 19. Master's Thesis Scope

The project should remain experimentally defensible.

A realistic Master's implementation can begin with a constrained reaction vocabulary rather than attempting to model all of organic chemistry.

For example:

1. select a limited set of common reaction classes;
2. construct a clean reaction-template grammar;
3. define compatible functional handles;
4. build a building-block library;
5. implement reaction-aware candidate generation;
6. add 3D pocket conditioning;
7. evaluate against structure-based baselines;
8. perform ablations to determine the contribution of the reaction grammar.

The thesis does not need to solve all of drug discovery.

It needs to demonstrate that **structured chemical generation changes the properties of SBDD candidates in a measurable way.**

---

# 20. Core Experiments

## Experiment 1 — Chemistry Constraint Ablation

Compare:

- unconstrained generation,
- atom-level validity constraints,
- reaction-graph constraints.

Measure chemical validity and synthetic accessibility.

## Experiment 2 — 3D Conditioning Ablation

Compare:

- reaction-aware generation without pocket conditioning,
- reaction-aware generation with pocket conditioning.

Measure pocket interaction and docking-related metrics.

## Experiment 3 — Joint Model

Compare the full model against each ablation.

Question:

> Does combining discrete reaction structure with continuous 3D geometry provide a measurable advantage?

## Experiment 4 — Diversity / Constraint Trade-off

Determine whether stronger reaction constraints improve feasibility at the cost of chemical diversity.

This is scientifically important because a constraint can solve one problem while introducing another.

---

# 21. Final Intended System

~~~text
                PROTEIN TARGET
                     |
                     v
             POCKET ENCODER
              SE(3)-EQUIVARIANT
                     |
          +----------+----------+
          |                     |
          v                     v
   3D GEOMETRY            REACTION STATE
          |                     |
          |              REACTION GRAMMAR
          |                     |
          +----------+----------+
                     |
                     v
          BUILDING-BLOCK SELECTOR
                     |
                     v
            3D POSE / TORSION
                     |
                     v
             UPDATE MOLECULE
                     |
                     v
              UPDATE RECIPE
                     |
                  repeat
                     |
                     v
        +-------------------------+
        | FINAL CANDIDATE         |
        |                         |
        | Molecular Graph         |
        | 3D Conformation        |
        | Reaction Graph          |
        | Synthetic Route         |
        +-------------------------+
~~~

---

# 22. Final Project Statement

**SynGAM-SBDD investigates whether structure-aware decoding can be transferred from mathematical expression recognition to structure-based molecular generation.**

Instead of treating drug design as unconstrained atom generation in a 3D protein pocket, the system represents chemical synthesis explicitly through a reaction graph.

The model combines:

- **SE(3)-equivariant protein-pocket encoding,**
- **reaction-graph-aware discrete generation,**
- **building-block selection,**
- **continuous 3D pose and torsion prediction,**
- **synthetic-route reconstruction.**

The goal is not simply to generate molecules that fit a protein pocket.

The goal is to generate molecules whose **3D geometry and chemical construction are modeled together**.

That makes the project a direct investigation of the following question:

> **Can a reaction-aware structural grammar make structure-based molecular generation more chemically actionable without sacrificing the geometric advantages of modern 3D generative models?**

---

# 23. Project Status

**Status:** Concept / Research Design

### Current Decisions

- [x] Use TAMER as the conceptual inspiration.
- [x] Move beyond atom-level graph validity.
- [x] Model synthesis through reaction structure.
- [x] Combine discrete chemistry with continuous 3D geometry.
- [x] Use an SE(3)-equivariant representation for the protein pocket.
- [x] Treat synthetic feasibility as a generation-time constraint.
- [ ] Finalize reaction vocabulary.
- [ ] Finalize reaction dataset.
- [ ] Finalize building-block dataset.
- [ ] Define exact model architecture.
- [ ] Define training objective.
- [ ] Define benchmark protocol.
- [ ] Implement baseline reproduction.
- [ ] Implement reaction-aware generator.
- [ ] Run ablations.
- [ ] Evaluate full model.

# 24. Working Terminology

| Term | Meaning |
|---|---|
| **SBDD** | Structure-Based Drug Design |
| **SynGAM** | Synthesis-Graph-Aware Module |
| **RGAM** | Reaction-Graph-Aware Module |
| **Reaction Grammar** | Formal set of allowed reaction transformations and compatibility rules |
| **Building Block** | Chemical component used as an input to the synthesis process |
| **Reaction Graph** | Graph representing the sequence of chemical transformations |
| **Pocket Encoder** | Network encoding the target protein binding pocket |
| **SE(3)-Equivariant** | Architecture whose representations transform consistently under 3D rotations and translations |
| **3D Pose** | Spatial placement and orientation of the generated ligand |
| **Retrosynthetic Feasibility** | Whether a molecule can be decomposed into plausible synthesis steps |

---

# 25. Important Claim Discipline

The following distinction should remain consistent in all future project documentation:

**Do claim:**
- reaction-constrained generation,
- validity under a defined reaction grammar,
- building-block-constrained generation,
- computational synthetic feasibility,
- joint optimization of geometry and synthesis structure.

**Do not claim without experimental evidence:**
- guaranteed laboratory synthesis,
- universal synthesizability,
- guaranteed binding,
- guaranteed biological activity,
- zero chemical risk,
- superiority over all existing SBDD models.

The thesis should demonstrate its claims experimentally rather than assuming them from the architecture.
