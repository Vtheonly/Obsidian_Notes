# 02 — Database Design · Master Index

> [!INFO] About This Vault
> A comprehensive, progressively-ordered study vault on relational database design — from foundational terminology through relational algebra, keys, relationships, ER modeling, normalization, SQL joins, views, the modern data ecosystem, and worked exercises. The vault is organized so that each chapter builds on the one before it.

## How to Navigate

- Read chapters in numeric order (01 → 12) for a complete curriculum.
- Each chapter folder is self-contained and can be studied independently.
- Wikilinks (`[[...]]`) connect related concepts across chapters.
- The **Exercises** chapter at the end consolidates practice material.

---

## Chapter Map

### 01 — Foundations
Database essentials: what a database is, the relational model, RDBMS, SQL basics, naming, design process, integrity, terminology, atomicity.

- [[01 - Introduction to Database Design]]
- [[02 - What is a Database]]
- [[03 - What is a Relational Database]]
- [[04 - RDBMS]]
- [[05 - Introduction to SQL]]
- [[06 - Naming Conventions]]
- [[07 - What is Database Design]]
- [[08 - Data Integrity]]
- [[09 - Database Terms]]
- [[10 - More Database Terms]]
- [[11 - Atomic Values]]

### 02 — Relational Algebra
The formal mathematical foundation: operators (σ, π, ρ, ⋈, ÷, ∪, ∩, −), set vs. bag semantics, advanced functions, and the SQL↔algebra mapping.

- [[01 - Relational Model Fundamentals]]
- [[02 - Relational Algebra Operators]]
- [[03 - Advanced Relational Algebra Functions]]
- [[04 - SQL to Algebra Mapping Cheat Sheet]]

### 03 — Keys & Constraints
The taxonomy of keys (superkey, candidate, primary, alternate, foreign, surrogate, natural, simple, composite, compound), constraints, and lookup tables.

- [[01 - Introduction to Keys]]
- [[02 - Superkey and Candidate Key]]
- [[03 - Primary Key and Alternate Key]]
- [[04 - Surrogate Key and Natural Key]]
- [[05 - Surrogate vs Natural Keys Decision Guide]]
- [[06 - Foreign Key]]
- [[07 - NOT NULL Foreign Key]]
- [[08 - Foreign Key Constraints]]
- [[09 - Simple, Composite, and Compound Key]]
- [[10 - Lookup Table]]
- [[11 - Primary Key Index]]
- [[12 - Review and Key Points]]

### 04 — Indexes
Database index internals: clustered vs. nonclustered, composite indexes, B-tree structure, design guidelines.

- [[01 - Indexes]]

### 05 — Relationships
The three relationship types (1:1, 1:N, M:N), their design patterns, parent/child table dynamics, and how to choose between them.

- [[01 - Relationships Overview]]
- [[02 - One-to-One Relationships]]
- [[03 - One-to-Many Relationships]]
- [[04 - Many-to-Many Relationships]]
- [[05 - Designing One-to-One Relationships]]
- [[06 - Designing One-to-Many Relationships]]
- [[07 - Designing Many-to-Many Relationships]]
- [[08 - Parent Tables and Child Tables]]
- [[09 - Summary of Relationships]]

### 06 — ER Modeling
Entity-Relationship diagrams, Crow's Foot notation, cardinality, modality, advanced attribute normalization, and complex ER-to-relational translations.

- [[01 - Introduction to ER Modeling]]
- [[02 - Cardinality]]
- [[03 - Modality]]
- [[04 - Advanced ER Concepts and Attribute Normalization]]
- [[05 - Complex ER to Relational Translations]]

### 07 — Normalization
Functional dependencies, anomalies, and the normal forms (1NF, 2NF, 3NF, BCNF).

- [[01 - Introduction to Database Normalization]]
- [[02 - Functional Dependencies]]
- [[03 - Anatomy of Database Anomalies]]
- [[04 - 1NF First Normal Form]]
- [[05 - 2NF Second Normal Form]]
- [[06 - 3NF Third Normal Form]]

### 08 — Data Types
SQL data type reference: numeric, string, date/time, boolean, binary, with selection guidelines.

- [[01 - Data Types]]

### 09 — Joins
The complete join family — algebraic and SQL — including inner, outer (left/right/full), self joins, the division operator, subquery operators (ANY/ALL/SOME), aggregation nuances, and comprehensive cheatsheets.

- [[01 - Relational Algebra - The Join Family]]
- [[02 - Introduction to Joins]]
- [[03 - Inner Join]]
- [[04 - Inner Join on 3 Tables]]
- [[05 - Outer Joins Explained]]
- [[06 - Outer Join Across 3 Tables]]
- [[07 - JOIN with NOT NULL Columns]]
- [[08 - Auto-Join, Self-Reference, and Self Join]]
- [[09 - Alias]]
- [[10 - The Division Operator]]
- [[11 - Advanced Querying - Joins and Subqueries]]
- [[12 - Advanced Subquery Operators - ANY, ALL, SOME]]
- [[13 - Aggregation Nuances and Subquery Optimization]]
- [[14 - Comprehensive Guide to Joins]]
- [[15 - Comprehensive SQL Join Cheatsheet]]

### 10 — Views
Virtual tables for security, simplification, and data independence; updatable views and `WITH CHECK OPTION`.

- [[01 - Views Fundamentals]]
- [[02 - Updatable Views and Check Options]]

### 11 — Database Classifications & Ecosystem
The broader database landscape: DBMS architectures, data independence, the modern data ecosystem, specialized models, and NoSQL storage internals.

- [[01 - Database Classifications and Architectures]]
- [[02 - DBMS Architecture and Models]]
- [[03 - Deep Dive on Data Independence and Architectures]]
- [[04 - The Modern Data Ecosystem]]
- [[05 - Specialized Database Models Deep Dive]]
- [[06 - NoSQL Internal Storage Mechanics]]
- [[07 - Wide Column Physical Layout and JSONiq Context]]

### 12 — Exercises
Worked problems and practice drills spanning set operations, joins, algebra↔SQL translation, advanced theory, and 30+ progressive practice exercises.

- [[01 - Set Operations vs Joins]]
- [[02 - Master Guide to SQL Joins]]
- [[03 - SQL Syntax Rules and Best Practices]]
- [[04 - Relational Algebra to SQL - 20 Query Examples]]
- [[05 - Advanced Database Theory]]
- [[06 - Practice Exercises]]

---

## Recommended Reading Paths

### A. Complete Beginner (Start Here)
01 → 03 → 05 → 06 → 07 → 08 → 09 → 10

### B. SQL Practitioner Reviewer
02 → 09 → 10 → 12

### C. Exam Prep (Theory + Drill)
02 → 03 → 06 → 07 → 09 → 11 → 12

### D. Architecture / Systems Focus
04 (RDBMS in 01) → 11

---

## Conventions Used in This Vault

- **Headings**: Each note has exactly one `# H1` title at the top, followed by `## H2` sections.
- **Callouts**: Obsidian callouts (`> [!INFO]`, `> [!TIP]`, `> [!WARNING]`, `> [!ERROR]`, `> [!NOTE]`, `> [!IMPORTANT]`) highlight key insights and pitfalls.
- **Diagrams**: Mermaid blocks (` ```mermaid `) render ER diagrams, flowcharts, and join visualizations.
- **Math**: KaTeX inline (`$...$`) and block (`$$...$$`) notation for relational algebra symbols (σ, π, ⋈, ÷).
- **Code**: SQL examples use ` ```sql ` fenced blocks.
- **Wikilinks**: `[[Note Name]]` for cross-references; Obsidian resolves them by filename across the whole vault.

## Source Acknowledgement

This vault was consolidated from an earlier, more fragmented version that combined:
- A "New/" structure with 5 chapter folders (Relational Algebra, Joins, Views, Ecosystem, Exercises) plus root-level advanced notes.
- An "Old/" structure of 51 numbered notes (0–50) covering the foundational curriculum.

All content from both structures has been preserved. Duplicates were merged (Best-of-Both synthesis), the `Old/` folder was fully absorbed into the proper chapters, and niche topics (Indexes, Data Types, Keys & Constraints, Relationships, ER Modeling, Normalization) were given their own dedicated folders for clarity. Wikilinks were remapped to the new filenames so navigation works seamlessly inside Obsidian.
