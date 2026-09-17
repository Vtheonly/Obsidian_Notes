---
tags: [foundations, spectrum, structure]
---

# Learning vs Representing vs Using vs Constraining Structure

> **The seven distinctions.** Learning a structure is not representing it. Representing it is not using it. Using it is not constraining it. Constraining it is not validating it. Validating it is not verifying it. Verifying it is not repairing it.

This distinction appears in every paper in this vault. A model that "is structure-aware" could be doing any one (or several) of these things, and the differences matter enormously.

## The Distinction Matrix

| Stage         | What is happening                                                        | What you can say                                                       |
| ------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| Learning      | The model fits parameters so its outputs *tend to* have structure.       | "Outputs *usually* have structure" (statistical).                      |
| Representing  | Structure is *stored* explicitly (embeddings, edges, masks).             | "The model *knows* the structure" (informational).                     |
| Using         | Structure influences attention, loss, or scoring.                        | "The model *prefers* structured outputs" (statistical).                 |
| Constraining  | Structure restricts the output space (grammar mask, schema).             | "Invalid outputs are *impossible*" (hard).                              |
| Validating    | An external checker tests whether the output satisfies the structure.    | "Invalid outputs are *detectable*" (post-hoc).                          |
| Verifying     | A formal prover/solver certifies the output satisfies a property.        | "The output is *proven* correct" (formal).                              |
| Repairing     | Invalid parts are localized and rewritten, then re-checked.              | "Invalid outputs are *recoverable*" (interactive).                      |

## Why This Matters

A paper that "is structure-aware" might mean any of:

- It *learns* a tree-structured latent (no guarantee).
- It *represents* the tree explicitly (no guarantee).
- It *uses* tree positional encodings (no guarantee).
- It *constrains* decoding with a grammar mask (hard guarantee on syntax, not on semantics).
- It *validates* with a parser (hard guarantee *if* you trust the validator).
- It *verifies* with an SMT solver (formal guarantee on the property checked).
- It *repairs* invalid subtrees (iterative recovery).

The guarantee you get depends on which stage the paper actually implements.

## Cross-Reference

- [[Hard Guarantees vs Statistical Preferences]]
- [[The Awareness Spectrum]]
- [[Validating vs Verifying vs Repairing Structure]]
- [[Explicit Structure vs Implicit Structure]]

## Example

Suppose a paper claims "tree-aware code generation". Ask:

1. Is the AST *learned* by the model or *parsed* from a reference?
2. Is the AST *represented* in the input (e.g. as parent pointers) or only *implicit* in token sequences?
3. Is the AST *used* in attention (e.g. tree mask) or only in the loss?
4. Is generation *constrained* by a grammar (so syntactically invalid code is impossible)?
5. Is the output *validated* by a parser and rejected if invalid?
6. Is the output *verified* by a type checker or symbolic executor?
7. Are invalid subtrees *repaired* by a localized rewrite?

See [[Paper Analysis Template]] — these questions are baked into the template.

## Related Concepts

- [[The Awareness Spectrum]]
- [[Validating vs Verifying vs Repairing Structure]]
- [[Hard Guarantees vs Statistical Preferences]]
- [[Explicit Structure vs Implicit Structure]]
- [[Paper Analysis Template]]
