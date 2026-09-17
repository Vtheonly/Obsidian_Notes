# Exercise Index

> How to use the exercises in this vault.

## Why exercises

Reading is not learning. Reading is the *first* exposure; exercises are where concepts become skills. The vault is not a reference to be skimmed — it is a curriculum to be practiced.

## How the exercises are organized

Four exercise files, each focused on a different part of the continuous chain:

1. **[[01-OOP-LLD-Exercises]]** — OOP, SOLID, patterns, UML, LLD. The "design half" of the vault.
2. **[[02-SQL-Normalization-Exercises]]** — Relational theory, normalization, schema design, SQL. The "data modeling half."
3. **[[03-Transactions-Concurrency-Exercises]]** — Transactions, isolation, MVCC, recovery, distributed systems. The "correctness under failure half."
4. **[[04-End-To-End-Capstone]]** — One problem, end-to-end, through every layer. The integration test.

## How to use each exercise

Each exercise has:

- **Problem statement** — what you are asked to do.
- **Hints** — small nudges if you are stuck. Read these *after* you have attempted the problem.
- **Solution** — a worked solution with reasoning. Read this *after* you have completed your own attempt, even if your attempt was wrong.
- **What this exercise teaches** — the concept being exercised, with back-links to the relevant chapter.

The workflow:

1. Attempt the problem without reading hints or solutions.
2. If stuck, read the hints and try again.
3. Compare your solution to the worked solution.
4. Identify the gap — what did you miss? Re-read the relevant chapter.
5. Move on. Come back in a week and try again without notes.

## The capstone

[[04-End-To-End-Capstone]] is the most important exercise. It asks you to take a single problem (a different one from the Banking anchor — to avoid copying the vault's own solution) and carry it through every layer:

- Requirements
- Use cases
- Domain concepts
- Responsibilities
- Classes
- UML
- LLD
- Code
- ER model
- Schema
- Normalization
- SQL
- Indexes
- Transactions
- Concurrency
- Query optimization

If you can complete the capstone, you have internalized the unified mental model. If you get stuck at any layer, that is the layer to revisit.

## The rule of deliberate practice

Do not read the solution before attempting. The act of struggling with the problem is where learning happens. Reading the solution first turns the exercise into a reading task, which teaches nothing.

If a problem feels easy, you are not pushing yourself — pick a harder one or add constraints (e.g., "solve this without using a Repository pattern").

If a problem feels impossible, you have found a gap in your understanding — read the linked chapter and come back.

## Where to start

- New to OOP/design? Start with [[01-OOP-LLD-Exercises]].
- New to databases? Start with [[02-SQL-Normalization-Exercises]].
- Comfortable with both, want the hard stuff? Jump to [[03-Transactions-Concurrency-Exercises]].
- Want the integration test? Go straight to [[04-End-To-End-Capstone]].

## Cross-references

- All exercises reference back to the Banking case study: [[00-Banking-Case-Study]]
- The capstone uses a *different* domain (a library system) so you cannot copy the vault's solution.
