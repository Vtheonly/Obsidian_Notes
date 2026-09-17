---
tags: [concept, database, performance, indexing, foreign-keys]
type: concept
status: complete
prerequisites:
  - [[11 - DB Performance and Indexing/02 - B-tree Indexes]]
related:
  - [[08 - Relational DB Foundations/07 - Keys - Primary, Foreign, Candidate, Surrogate]]
  - [[10 - Transactions and Concurrency/04 - Deadlocks]]
---

# Missing Indexes on Foreign Keys

## What it is

When you declare a foreign key `FOREIGN KEY (department_id) REFERENCES department(department_id)`, Oracle creates an index on the **parent** (`department.department_id`) - it's the PK, already indexed. But Oracle does **not** create an index on the **child** (`intern.department_id`). That's on you.

## Why the missing index is a problem

### 1. Full table scan on child joins

```sql
SELECT i.name, d.department_name
FROM   intern i
JOIN   department d ON i.department_id = d.department_id
WHERE  d.department_id = 5;
```

Without an index on `intern.department_id`, Oracle must full-scan `intern` to find matching rows. With an index, it's a range scan.

### 2. Table lock on parent delete (the killer)

When you `DELETE FROM department WHERE department_id = 5`, Oracle needs to enforce the FK: either cascade the delete to `intern`, set `intern.department_id` to NULL, or block the delete. To do that, it must find all `intern` rows with `department_id = 5`.

If `intern.department_id` is **not** indexed, Oracle takes a **table-level Shared Row Exclusive lock** on `intern` for the duration of the transaction. That blocks all writes to `intern` - not just the matching rows.

If two such deletes run concurrently on different parent/child pairs, you get a **deadlock** - see [[10 - Transactions and Concurrency/04 - Deadlocks]].

### 3. Slow `ON DELETE SET NULL` and `ON DELETE CASCADE`

The same lock problem applies. The cascade must find every child row; without an index, that's a full scan plus a table lock.

## The fix

```sql
CREATE INDEX idx_intern_department  ON intern(department_id);
CREATE INDEX idx_intern_theme       ON intern(theme_id);
CREATE INDEX idx_user_department    ON worker_user(department_id);
CREATE INDEX idx_application_intern ON application(intern_id);
```

Index every FK column. Period. The cost is small (one B-tree per FK); the benefit is huge (no table locks on parent deletes, fast joins).

## How to find missing FK indexes

```sql
SELECT  c.table_name, c.constraint_name, cc.column_name
FROM    user_constraints c
JOIN    user_cons_columns cc ON c.constraint_name = cc.constraint_name
WHERE   c.constraint_type = 'R'   -- 'R' = Referential (FK)
AND     NOT EXISTS (
    SELECT 1
    FROM   user_ind_columns ic
    WHERE  ic.table_name  = c.table_name
    AND    ic.column_name = cc.column_name
    AND    ic.column_position = 1   -- first column of some index
);
```

Run this on any schema you inherit. The output is your "indexes to add" list.

## Project Connection

`insertion.sql` declares FKs:

```sql
FOREIGN KEY (theme_id)      REFERENCES theme,
FOREIGN KEY (department_id) REFERENCES department,
FOREIGN KEY (user_id)       REFERENCES worker_user
```

...and creates **zero indexes** on these FK columns. So:

- Every join between `intern` and `department` full-scans `intern`.
- Deleting a department locks the entire `intern` table.
- Deleting two departments from two sessions deadlocks.

The redesign adds indexes on every FK column. This is the single highest-impact change in the schema redesign.

## Common pitfalls

- Forgetting that the FK index must have the FK column as the **first** column (a composite index starting with a different column won't help).
- Assuming the FK index needs to be `UNIQUE` - it doesn't. FK columns can have duplicates (many interns in one department).
- Adding the FK index but forgetting to gather stats - the optimizer still chooses the full scan because it doesn't know the index exists.

## Further reading

- Oracle Docs, "How Oracle Database Locks Data", "Unindexed Foreign Keys".
- [[10 - Transactions and Concurrency/04 - Deadlocks]]
