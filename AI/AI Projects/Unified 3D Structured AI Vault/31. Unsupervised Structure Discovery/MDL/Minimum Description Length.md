---
tags: [discovery, mdl]
---

# Minimum Description Length (MDL)

> **Definition.** *MDL* is a model selection principle: choose the model that minimizes the total description length of the data plus the model.

## Principle

Given data $D$ and a model $M$:

$$\text{Cost}(D, M) = L(D | M) + L(M)$$

where:

- $L(D | M)$ = length of encoding $D$ given $M$,
- $L(M)$ = length of encoding $M$ itself.

The best $M$ minimizes the total cost.

## Why It Matters

MDL provides a principled way to:

- Avoid over-fitting (a complex model that perfectly explains the data has high $L(M)$).
- Avoid under-fitting (a simple model that poorly explains the data has high $L(D | M)$).
- Decide whether to add a new component (does it reduce total cost?).

## In Discovery

A discovered component $c$ is worth keeping if:

$$L(D | \text{with } c) + L(c) < L(D | \text{without } c)$$

i.e. the cost saved by using $c$ (in $L(D | \text{with } c)$) exceeds the cost of describing $c$ (in $L(c)$).

## Application

- **Component discovery**: keep components that reduce total description length.
- **Grammar induction**: keep rules that reduce total description length.
- **Model selection**: pick the model with lowest total cost.

See [[Frequency vs Meaning]], [[Candidate Component Scoring]], [[Recursive Component Discovery]].

## Related Concepts

- [[Frequency vs Meaning]]
- [[Candidate Component Scoring]]
- [[Recursive Component Discovery]]
- [[Grammar Induction]]
- [[Program Induction]]
