---
tags: [discovery, grammar-induction]
---

# Grammar Induction

> **Definition.** Learn a grammar (production rules) from a set of examples.

## Why It Matters

A grammar is a compact description of a set of structures. If we can induce a grammar from data, we have:

- a compact representation,
- a generator (sample from the grammar),
- a recognizer (parse new examples),
- a basis for constraints.

## Methods

- **ADIOS**: pattern discovery in sequences.
- **EMILE**: grammar induction from text.
- **Tree substitution grammar induction**: learn tree patterns.
- **Neural grammar induction**: learn soft rules with neural networks.

## In Buildings

Induce a shape grammar from a corpus of buildings:

```
Building → split into Storeys
Storey → split into Rooms
Room → Walls + Door + Windows
Wall (length > 3m) → Wall + Window
Wall (between bedroom and bathroom) → Wall + Door
...
```

The induced grammar captures recurring design patterns.

## Connection to Other Discovery

Grammar induction is a form of [[Recursive Component Discovery]] where each production rule is a discovered component.

See [[Recursive Component Discovery]], [[Shape Grammars]], [[Grammar Constrained Generation]].

## Related Concepts

- [[Recursive Component Discovery]]
- [[Shape Grammars]]
- [[Grammar Constrained Generation]]
- [[Program Induction]]
- [[Minimum Description Length]]
