---
tags: [concept, design-patterns, gof]
type: concept
status: complete
related:
  - [[06 - Design Patterns/12 - Pattern Catalog Overview]]
---

# What Are Design Patterns?

> "Each pattern describes a problem which occurs over and over again in our environment, and then describes the core of the solution to that problem, in such a way that you can use this solution a million times over, without ever doing it the same way twice." — Christopher Alexander, *A Pattern Language*, 1977

## What it is

A **design pattern** is a reusable solution to a commonly occurring problem in software design. It's not a finished design — it's a template for solving a problem that can be adapted to many situations.

## The Gang of Four

In 1994, Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides ("Gang of Four" or GoF) published *Design Patterns: Elements of Reusable Object-Oriented Software*. They cataloged 23 patterns in three categories:

- **Creational** — object creation (5 patterns).
- **Structural** — object composition (7 patterns).
- **Behavioral** — object interaction (11 patterns).

## Why patterns exist

- **Shared vocabulary** — instead of "let's create an object that wraps another object and adds behavior," you say "Decorator pattern." Engineers understand immediately.
- **Proven solutions** — patterns have been refined over decades. They capture hard-won knowledge.
- **Common mistakes** — patterns document not just the solution, but the trade-offs and pitfalls.

## Pattern structure

Most pattern descriptions follow this template:
- **Name** — the pattern's name (e.g., "Strategy").
- **Intent** — one sentence describing what it does.
- **Motivation** — a scenario where the pattern applies.
- **Structure** — a UML diagram.
- **Participants** — the classes and objects involved.
- **Collaborations** — how they interact.
- **Consequences** — trade-offs.
- **Implementation** — practical tips.
- **Related patterns** — connections to other patterns.

## When to use patterns

- **When the problem fits** — don't force a pattern. Use it when the problem genuinely matches.
- **When the team knows the pattern** — patterns are vocabulary; if the team doesn't know them, they're noise.
- **When the complexity is justified** — a 3-line function doesn't need the Strategy pattern.

## When NOT to use patterns

- **YAGNI** — don't add patterns "for the future."
- **Simplicity first** — if a simple solution works, use it.
- **Pattern obsession** — "I just learned the Visitor pattern, let me use it everywhere." Don't.

## Project Connection

The project uses **zero** patterns correctly. The `oracleConnector` static utility is the worst form of Singleton (static mutable state). Every other pattern is absent. The reviews identify 13+ patterns that should be applied.

## Further reading

- *Design Patterns* (GoF, 1994) — the book.
- *Head First Design Patterns* (Freeman & Robson) — friendlier introduction.
- refactoring.guru — interactive catalog with examples.
