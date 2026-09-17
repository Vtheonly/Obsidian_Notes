# The Unified Vault — Software Design & Database Engineering

> One interconnected system of knowledge. Learn the shared concept once; reuse it everywhere.

This vault does not contain separate courses on OOP, UML, LLD, SQL, databases, or transactions. It contains **one continuous mental model** that runs from a raw requirement all the way down to a B-tree lookup on a disk page, with every layer explaining *why it exists*, *what problem it solves*, and *how it connects to the layer above and below*.

## How to read this vault

1. Start at [[00-Map-of-Content]] — that is the master index.
2. Read [[01-Unified-Mental-Model]] first. It is short and it is the lens for everything that follows.
3. Read [[02-The-Continuous-Chain]] to see the full pipeline you will traverse.
4. Read [[03-Dependency-As-Root-Concept]] — this single concept recurs in OOP, SOLID, UML, schema design, foreign keys, and query plans. If you internalize it, half the vault is implicit.
5. Then walk the chapters in order. Each one opens by recalling what you already know and naming only what is *genuinely new*.

## What this vault is not

- Not a list of definitions to memorize.
- Not five textbooks stitched together.
- Not a patterns cheat sheet.
- Not a SQL tutorial.

## What this vault is

A single argument: software design and database engineering are **the same problem at different layers**, and the same handful of concepts (dependency, abstraction, identity, composition, constraint, trade-off) reappear at every layer wearing different vocabulary.

If you finish this vault and can answer, for any software problem:

> *What are the requirements? What are the domain concepts? What objects and responsibilities exist? How should they collaborate? What should the class design look like? What data must persist? How should that data be modeled? What constraints must hold? What SQL represents the operations? How will the database execute it? What happens under concurrency or failure? What can be optimized? What trade-offs am I making?*

…then the vault has done its job.

## The anchor case

The vault uses one continuous end-to-end case study: a **Banking / Ledger system**. Every chapter applies its concepts to the same system, so you watch a single problem progress from requirements → use cases → domain model → classes → UML → LLD → code → ER model → schema → normalization → SQL → indexes → transactions → concurrency → query optimization → distributed concerns.

The anchor lives at [[00-Banking-Case-Study]]. Read it once; you will be sent back to it from every chapter.

## Conventions

- `[[Wiki-Links]]` link concepts across the vault. Follow them when a term is unfamiliar.
- Code is Java unless a snippet is explicitly SQL, relational algebra, or pseudocode.
- SQL is generic ANSI SQL unless a PostgreSQL-specific feature is shown (always labeled).
- Diagrams are Mermaid — they render in Obsidian, GitHub, and most Markdown previewers.
- Each note opens with a `## What you already know` block. If you can recall it without reading, skip it.
- Each note closes with `## What is genuinely new here` — the only thing you must take away.

## A note on the rule that drives everything

> **Unify repetition, not knowledge.**

If a topic is shared (e.g., "dependency"), the vault teaches it once and reuses it. If a topic is genuinely specific (e.g., BCNF decomposition, ARIES recovery, MVCC snapshot isolation), the vault teaches it in full. Unification is a teaching strategy, not a deletion strategy.

Continue to [[00-Map-of-Content]].
