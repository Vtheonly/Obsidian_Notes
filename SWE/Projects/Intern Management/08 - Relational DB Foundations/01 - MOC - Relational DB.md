---
tags: [moc, database, relational-model, sql]
type: moc
status: complete
---

# MOC - Relational DB Foundations

> Codd's relational model is the substrate everything in the project sits on.
> The two conflicting schemas (insertion.sql vs requstes.sql), the `MAX(id)+1`
> race condition, the quoted identifiers, and the CHECK constraint violation
> all live here. Master the model and most of the project's bugs become obvious.

## Notes (read in order)

### The model
1. [[08 - Relational DB Foundations/18 - The Relational Model]] - Codd, tuples, relations, domains.
2. [[08 - Relational DB Foundations/14 - SQL Basics]] - the language that manipulates relations.
3. [[08 - Relational DB Foundations/03 - DDL vs DML vs DCL vs TCL]] - four families of statements.

### Structure
4. [[08 - Relational DB Foundations/07 - Keys - Primary, Foreign, Candidate, Surrogate]] - identifying rows.
5. [[08 - Relational DB Foundations/02 - Constraints]] - CHECK, NOT NULL, UNIQUE, FK.
6. [[08 - Relational DB Foundations/06 - Joins]] - INNER, LEFT, RIGHT, FULL, CROSS, NATURAL.

### Oracle specifics
7. [[08 - Relational DB Foundations/08 - Oracle Data Types]] - NUMBER, VARCHAR2, DATE, CLOB, RAW.
8. [[08 - Relational DB Foundations/16 - SQL Plus and SQLcl]] - the command-line clients.
9. [[08 - Relational DB Foundations/12 - Quoted Identifiers]] - why `"intern"` is a footgun.
10. [[08 - Relational DB Foundations/17 - Schemas and Users in Oracle]] - a schema IS a user.
