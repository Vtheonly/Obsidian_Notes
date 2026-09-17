---
tags: [papers, template]
---

# Paper Analysis Template

> Every paper note in this vault MUST follow this template. Copy it verbatim and fill in each section.

## Template

```markdown
# Paper Name

## Problem

(What problem does the paper address? Why is it important?)

## Input

(What does the system take as input? Images? Point clouds? Text? BIM?)

## Output

(What does the system produce? Trees? Graphs? Meshes? BIM?)

## 3D Representation

(How is 3D content represented? Point cloud? Voxel? Mesh? SDF? NeRF? BIM?)

## Structural Representation

(How is structure represented? Tree? Graph? Scene graph? Grammar?)

## Tree Representation

(If trees are used, what kind? AST? BIM hierarchy? Parse tree?)

## Graph Representation

(If graphs are used, what are the nodes and edges?)

## BIM Representation

(If BIM is involved, which entities and relationships?)

## Geometry Representation

(How is geometry represented? Parametric? Mesh? Implicit?)

## How Is Structure Represented?

(Explicit data structure? Implicit in embeddings? Both?)

## How Is Structure Learned?

(Learned from data? Given by a parser? Hard-coded?)

## Where Does Structural Information Enter?

(Input embeddings? Attention? Constraints? Decoder?)

## Where Does 3D Information Enter?

(3D features? 3D attention? 3D losses? 3D constraints?)

## Training Objective

(What is the model trained to optimize?)

## Loss Functions

(Per-token cross-entropy? Structured loss? Geometric loss? Multi-task?)

## Generation Process

(Autoregressive? Diffusion? Tree decoder? Search?)

## Constraints

(Are constraints enforced? How? Hard or soft?)

## Validation

(Is there a validator? What does it check?)

## Verification

(Is there a verifier? Formal? Neural? Physics-based?)

## Search

(Is there a search procedure? Beam? MCTS? Backtracking?)

## Repair

(Is there a repair loop? How does it work?)

## Failure Modes

(When does the system fail? What kinds of errors are possible?)

## What Is Guaranteed?

(What properties are guaranteed by construction / by verification?)

## What Is Merely Probabilistic?

(What properties are only preferred statistically?)

## Main Contribution

(What is the paper's main contribution?)

## Limitations

(What does the paper NOT do? What are the open problems?)

## Related Concepts

(Link to vault notes: [[...]])

## My Interpretation

(Your own reading. What did you learn? What surprised you? What would you do differently?)
```

## How to Use

1. Create a new file under `38. Research Papers/<category>/Paper — <short name>.md`.
2. Copy the template above.
3. Fill in every section.
4. If a section doesn't apply, write "N/A" and explain why.

## Why This Template

The template forces you to ask the **central questions** of this vault:

- What structure does the paper represent?
- How is that structure discovered?
- How is it learned?
- How does the structure influence the model?
- Is the structure explicit or implicit?
- Is generation constrained?
- Are invalid structures possible?
- How are errors detected?
- How are errors localized?
- How are errors repaired?
- Are multiple hypotheses searched?
- How do geometry and semantics remain consistent?
- How do different representations remain synchronized?
- What is actually guaranteed?
- What is merely learned as a statistical pattern?

See [[08. Research Papers MOC]].

## Related Concepts

- [[08. Research Papers MOC]]
- [[Learning vs Representing vs Using vs Constraining Structure]]
- [[Hard Guarantees vs Statistical Preferences]]
