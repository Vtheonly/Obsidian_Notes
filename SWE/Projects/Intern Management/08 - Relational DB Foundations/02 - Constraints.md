---
tags: [concept, database, constraints, ddl]
type: concept
status: complete
prerequisites:
  - [[08 - Relational DB Foundations/07 - Keys - Primary, Foreign, Candidate, Surrogate]]
related:
  - [[08 - Relational DB Foundations/03 - DDL vs DML vs DCL vs TCL]]
  - [[12 - Advanced Database Features/15 - Triggers]]
---

# Constraints

## What it is

A **constraint** is a declarative rule the database enforces on every row. There are five core constraint types in Oracle:

| Constraint | Meaning | Example |
|---|---|---|
| `NOT NULL` | Column cannot be NULL | `name VARCHAR2(100) NOT NULL` |
| `UNIQUE` | No two rows share a value (NULLs allowed, multiple) | `email VARCHAR2(255) UNIQUE` |
| `PRIMARY KEY` | `NOT NULL` + `UNIQUE` + identifies the row | `intern_id PRIMARY KEY` |
| `FOREIGN KEY` | Value must exist in referenced table | `department_id REFERENCES department` |
| `CHECK` | Custom boolean predicate | `CHECK (age >= 0)` |

Constraints are **declarative** - you state the rule once, the DB enforces it forever, on every INSERT, UPDATE, and (for FKs) DELETE.

## Why it matters

Constraints are the database's last line of defense. Application validation can be bypassed (a second app, a SQL*Plus session, a bug). A `CHECK` constraint catches bad data no matter how it got in.

Constraints are also **self-documenting** - the schema declares its own invariants.

## Example

```sql
CREATE TABLE intern (
    intern_id     NUMBER(10)     GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name          VARCHAR2(100)  NOT NULL,
    age           NUMBER(3)      CHECK (age BETWEEN 16 AND 99),
    email         VARCHAR2(255)  CONSTRAINT uq_intern_email UNIQUE,
    is_accepted   VARCHAR2(10)   DEFAULT 'Pending'
        CHECK (is_accepted IN ('Accepted','Rejected','Pending')),
    department_id NUMBER(10)     NOT NULL,
    CONSTRAINT fk_intern_department
        FOREIGN KEY (department_id) REFERENCES department(department_id)
        ON DELETE SET NULL
);
```

## Naming constraints

Always name constraints. Oracle's auto-generated names (`SYS_C001234`) are useless in error messages and in migration diffs.

```java
try (PreparedStatement ps = conn.prepareStatement(...)) {
    ps.executeUpdate();
} catch (SQLException e) {
    // Error message will contain "FK_INTERN_DEPARTMENT" not "SYS_C009812"
    if (e.getMessage().contains("FK_INTERN_DEPARTMENT")) { ... }
}
```

## Project Connection

`insertion.sql` does declare a CHECK constraint:

```sql
CHECK (is_accepted IN ('Accepted','Rejected','Pending'))
```

But the Java code does:

```java
data.put("IS_ACCEPTED", "hold");  // lowercase 'hold' - not in the allowed set
```

Result: **every intern insert fails** with `ORA-02290: check constraint violated`. The constraint is correct; the code is wrong. The fix is an `InternStatus` enum - see [[04 - OOD and SOLID/18 - Replace Magic Strings with Enums]].

## Trade-offs

- Constraints cost CPU on every write. For OLTP they're worth it; for bulk loads into a staging table, you might disable them and re-enable with `NOVALIDATE`.
- CHECK constraints cannot reference other rows or `SYSDATE` (no cross-row rules). Use [[12 - Advanced Database Features/15 - Triggers]] for those - reluctantly.

## Common pitfalls

- Adding a `CHECK (status = 'active')` and then forgetting `'Active'` vs `'active'` - case matters.
- Using `CHECK` to enforce business rules that change often - the schema becomes a release bottleneck.
- Declaring FKs without `ON DELETE` clauses - you get the default `RESTRICT`, which can block deletes.

## Further reading

- Oracle Docs, "Constraints".
- [[08 - Relational DB Foundations/07 - Keys - Primary, Foreign, Candidate, Surrogate]]
