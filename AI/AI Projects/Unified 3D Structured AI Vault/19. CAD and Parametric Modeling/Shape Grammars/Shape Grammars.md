---
tags: [cad, grammar, shape-grammar]
---

# Shape Grammars

> **Definition.** A *shape grammar* is a production system that generates shapes by recursively applying rules to a starting shape.

## Structure

- **Vocabulary**: a set of shapes (terminals and non-terminals).
- **Rules**: productions of the form `LHS → RHS`, where LHS and RHS are shapes.
- **Starting shape**: the initial shape.

## Example (Building Grammar)

```
Start: Building footprint rectangle.
Rule 1: Building → split into floors.
Rule 2: Floor → split into rooms.
Rule 3: Wall with length > 3m → Wall + Window.
Rule 4: Wall between bedroom and bathroom → Wall + Door.
```

Apply rules recursively to generate a complete building.

## Famous Examples

- **Palladian grammar** (Stiny and Mitchell): generates Palladian villas.
- **City grammar** (Duarte): generates urban layouts.
- **Building grammar** (Wonka et al.): CGA shape, used in Esri CityEngine.

## Why It Matters

- **Procedural generation**: produces large, varied buildings from small rule sets.
- **Tree-structured**: rule application creates a derivation tree.
- **Easy to constrain**: rules can enforce domain constraints (e.g. every room has a door).
- **Easy to validate**: check that all rules are satisfied.

## Connection to AI

Shape grammars are a formal analog of generative models. AI can:

- **Learn** grammars from data (grammar induction). See [[Grammar Induction]].
- **Use** grammars as constraints. See [[Grammar Constrained Generation]].
- **Generate** by sampling rules. See [[Procedural]].

See [[Grammar Induction]], [[Grammar Constrained Generation]], [[Procedural]].

## Related Concepts

- [[Grammar Induction]]
- [[Grammar Constrained Generation]]
- [[Procedural]]
- [[Rule Based]]
