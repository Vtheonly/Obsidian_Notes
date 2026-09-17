---
tags: [concept, database, relational-model]
type: concept
status: complete
related:
  - [[08 - Relational DB Foundations/14 - SQL Basics]]
  - [[08 - Relational DB Foundations/07 - Keys - Primary, Foreign, Candidate, Surrogate]]
  - [[09 - Normalization/09 - What Is Normalization]]
---

# The Relational Model

## What it is

The **relational model** was introduced by Edgar F. Codd in 1970 ("A Relational Model of Data for Large Shared Data Banks"). It represents all data as **relations** - mathematical sets of tuples - and manipulates them with operations drawn from relational algebra: selection, projection, join, union, difference.

A **relation** has:
- A **heading**: a set of attributes, each with a name and a domain (type).
- A **body**: a set of tuples, each one row of values matching the heading.
- No duplicate tuples (sets, not bags).
- No intrinsic ordering of rows or columns.

SQL is an imperfect implementation of this model: tables allow duplicate rows, columns have an order, and NULL breaks the two-valued logic. The model is the ideal; SQL is the practical approximation.

## Why it exists

Before Codd, data was stored in hierarchical or network databases (IMS, CODASYL) where access paths were hardcoded into the data. To answer a new question, you often had to rewrite the storage. Codd's insight: separate the **logical** representation (relations) from the **physical** storage, and let a query optimizer choose access paths. That separation is why SQL "just works" 55 years later.

## The three integrity rules

1. **Entity integrity** - every relation has a primary key; PK columns cannot be NULL.
2. **Referential integrity** - every foreign key value either matches a PK in the referenced table or is NULL.
3. **Domain integrity** - every value falls in its declared domain (enforced by type + CHECK constraints).

## Project Connection

The project's `intern` table is a relation in name only. It has a declared PK (`intern_id`), but the Java layer generates IDs via `MAX(id)+1`, which **bypasses entity integrity under concurrency** - two threads can compute the same max and both insert, producing a duplicate PK or one failed insert. See [[10 - Transactions and Concurrency/01 - ACID Properties]].

## Common pitfalls

- Confusing the relation (the abstract set) with the table (the SQL storage that can have duplicates and NULLs).
- Thinking rows have an order - they don't, unless you add `ORDER BY`.
- Believing NULL means "zero" or "empty string" - it means "unknown."

## Further reading

- Codd, "A Relational Model of Data for Large Shared Data Banks," CACM 1970.
- Date, *An Introduction to Database Systems*, 8th ed.
- [[08 - Relational DB Foundations/14 - SQL Basics]]
