---
tags: [discovery, program-induction]
---

# Program Induction

> **Definition.** Infer a program (typically from input-output examples or from a target structure).

## Why It Matters

A program is the most compact structured representation. Examples:

- A CAD feature tree is a program that builds geometry.
- A shape grammar derivation is a program.
- An AST is a program.

Inducing a program from data = finding the most compact program that explains the data.

## Methods

- **Program synthesis**: search over program space (e.g. with symbolic regression, inductive logic programming).
- **Neural program synthesis**: a neural network generates the program.
- **Library learning**: discover reusable subroutines (which are components).

## In Buildings

Program induction for buildings:

- Given a building, find a CAD program that builds it.
- Given a corpus, find a library of reusable building blocks.
- Given a partial building, complete the program.

## Connection to Discovery

Program induction is the most general form of [[Recursive Component Discovery]]: each subroutine is a discovered component, and the program is the composition.

See [[Recursive Component Discovery]], [[Feature Trees]], [[Grammar Induction]].

## Related Concepts

- [[Recursive Component Discovery]]
- [[Feature Trees]]
- [[Grammar Induction]]
- [[Minimum Description Length]]
