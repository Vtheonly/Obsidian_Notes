# The Unified Mental Model

> The central argument of the vault. Read this first.

## What you already know

You have probably studied OOP, SQL, UML, design patterns, and databases as separate subjects. Each came with its own vocabulary, its own textbooks, its own exam. You learned them in parallel and stored them in separate mental boxes.

## Why this layer exists

That separation is artificial. It was created by curricula and bookshelves, not by the problems themselves. The problems of software design and the problems of database engineering are not two problems. They are **the same problem** viewed at two different layers of concreteness:

> *Given a messy reality, produce a constrained model that behaves correctly under use, change, concurrency, and failure.*

Whether you call the model an *object model* or a *data model* is a question of which side of the disk you are standing on. The forces — abstraction, identity, dependency, constraint, trade-off — are identical.

## What is genuinely new here

The single claim that organizes this vault:

> **Software design and database engineering are the same discipline applied at different layers. The same five forces appear at every layer; only the vocabulary changes.**

The five forces:

| Force | In OOP / LLD | In databases |
|---|---|---|
| **Dependency** | imports, references, DI, coupling | foreign keys, joins, schema dependencies |
| **Abstraction** | interface, abstract class, role | view, materialized view, logical schema |
| **Identity** | object reference, `equals`/`hashCode` | primary key, surrogate key, OID |
| **Constraint** | invariant, precondition, assertion | `NOT NULL`, `CHECK`, FK, unique, trigger |
| **Trade-off** | "no free lunch" in design | "no free lunch" in query plans and isolation |

If you internalize these five, every later chapter is a variation on a theme you already know.

## The unification rule

> **Unify repetition, not knowledge.**

Two cases:

1. **Same concept, different vocabulary.** Teach the concept once, then map the vocabulary.
   - Example: *dependency* in UML, *coupling* in OOP, *foreign key* in SQL, *join dependency* in relational theory. Same idea, four vocabularies. The vault teaches *dependency* once.

2. **Genuinely different concept.** Teach it in full. Do not abbreviate.
   - Example: *BCNF decomposition*, *MVCC snapshot isolation*, *ARIES recovery*. These are not "the dependency idea again." They are real, hard, specific. The vault teaches each completely.

The test for which case applies:

> *If I removed this topic, would the reader infer it from a unifying principle, or would they actually lose knowledge?*

If they would lose knowledge, the topic stays — in full.

## How to read the vault

Every chapter opens with:

> **What you already know.** A short recall of the prior layer. If you can already recite it, skip.

And closes with:

> **What is genuinely new here.** The delta you must take away. Usually one paragraph.

In between, the chapter applies the five forces to one new layer of the chain and advances the Banking case study by one step.

## The one habit to build

When you encounter any new concept in any chapter, ask:

> *What do I already understand about this? What is genuinely new here?*

If the answer is "nothing is new, this is just X wearing a new hat" — good. Link it to X and move on. If the answer is "this is genuinely new" — slow down and learn it for real.

This habit is what makes the curriculum fast without making it shallow.

## Where this goes next

- [[02-The-Continuous-Chain]] — the full pipeline you will traverse, layer by layer.
- [[03-Dependency-As-Root-Concept]] — the single most-reused idea in the vault.
- [[00-Banking-Case-Study]] — the anchor problem every chapter advances.
