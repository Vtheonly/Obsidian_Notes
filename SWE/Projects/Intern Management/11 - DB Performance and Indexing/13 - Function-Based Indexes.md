---
tags: [concept, database, performance, indexing, function-based]
type: concept
status: complete
prerequisites:
  - [[11 - DB Performance and Indexing/02 - B-tree Indexes]]
related:
  - [[11 - DB Performance and Indexing/07 - Composite Indexes]]
  - [[08 - Relational DB Foundations/08 - Oracle Data Types]]
---

# Function-Based Indexes

## What it is

A **function-based index (FBI)** is a B-tree (or bitmap) index on the result of a function or expression, rather than on a bare column. The function is precomputed at insert/update time and stored in the index; queries that use the same function can use the index.

## The problem it solves

Without an FBI:

```sql
SELECT * FROM intern WHERE LOWER(name) = 'alice';
SELECT * FROM intern WHERE TRUNC(start_date) = DATE '2024-01-15';
SELECT * FROM intern WHERE UPPER(email) = 'ALICE@EXAMPLE.COM';
```

The `LOWER(name)` predicate cannot use `idx_intern_name` - the index is on `name` (as stored), not on `LOWER(name)`. Oracle falls back to a full table scan.

## The FBI fix

```sql
CREATE INDEX idx_intern_name_lower  ON intern(LOWER(name));
CREATE INDEX idx_intern_start_trunc ON intern(TRUNC(start_date));
CREATE INDEX idx_intern_email_upper ON intern(UPPER(email));
```

Now `WHERE LOWER(name) = 'alice'` uses `idx_intern_name_lower`. The function is computed **once** at write time and stored; reads are as fast as a regular B-tree lookup.

## Case-insensitive lookups

The canonical use case. Oracle stores `VARCHAR2` case-sensitively; if users type `Alice`, `alice`, `ALICE` interchangeably, you need a case-insensitive index:

```sql
CREATE INDEX idx_intern_name_ci ON intern(NLSSORT(name, 'NLS_SORT=BINARY_CI'));
-- then query:
SELECT * FROM intern WHERE NLSSORT(name, 'NLS_SORT=BINARY_CI') = NLSSORT('alice', 'NLS_SORT=BINARY_CI');
```

For a simpler case-insensitive equality (no locale-aware sorting):

```sql
CREATE INDEX idx_intern_name_ci ON intern(LOWER(name));
SELECT * FROM intern WHERE LOWER(name) = LOWER(?);
```

## Expressions, not just functions

FBIs work on arbitrary expressions:

```sql
CREATE INDEX idx_intern_age_plus_5 ON intern(age + 5);
CREATE INDEX idx_intern_total      ON intern(salary + bonus);
```

## Determinism requirement

The function must be **deterministic** - same input, same output. You cannot index `SYSDATE`, `USER`, `DBMS_RANDOM`, or anything that depends on time or session state. Oracle enforces this for built-ins; for user functions, you must declare `DETERMINISTIC`:

```sql
CREATE OR REPLACE FUNCTION mask_email(p_email VARCHAR2)
RETURN VARCHAR2 DETERMINISTIC IS
BEGIN
    RETURN REGEXP_REPLACE(p_email, '.*@', '***@');
END;
/

CREATE INDEX idx_intern_email_masked ON intern(mask_email(email));
```

## Project Connection

The project's `searchIntern` uses `LIKE '%' || ? || '%'` - a leading wildcard that **cannot** use any index. Even a function-based index won't help (the substring is not a fixed prefix). For substring search, use Oracle Text (`CONTEXT` index) or accept the full scan.

But for the many `WHERE UPPER(name) = UPPER(?)` style lookups the project does, an FBI is the right answer. The redesign adds:

```sql
CREATE INDEX idx_intern_name_ci ON intern(LOWER(name));
CREATE INDEX idx_intern_email_ci ON intern(LOWER(email));
```

## Common pitfalls

- Querying with a different function than the index - `WHERE UPPER(name) = 'ALICE'` won't use `idx_intern_name_lower` (which is on `LOWER`).
- Indexing a non-deterministic function - silent wrong results.
- Forgetting that the FBI's stored value goes stale if the underlying data changes outside the index maintenance path (e.g., direct-path loads that bypass index maintenance).
- Adding an FBI for a one-off query - the write cost may exceed the read savings.

## Further reading

- Oracle Docs, "Function-Based Indexes".
- [[11 - DB Performance and Indexing/02 - B-tree Indexes]]
