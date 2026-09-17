---
tags: [concept, database, indexing, function-based]
type: concept
status: complete
prerequisites:
  - [[11 - DB Performance and Indexing/01 - B-Tree Index]]
---

# Function-Based Index

## What it is

A **function-based index** indexes the result of a function or expression.

```sql
CREATE INDEX idx_users_upper_name ON users(UPPER(full_name));

-- Now this query uses the index:
SELECT * FROM users WHERE UPPER(full_name) = 'ALICE';
-- Without the index, this would be a full table scan (UPPER() is applied to every row).
```

## Why it exists

Without a function-based index, any function on a column in the WHERE clause prevents index usage:
```sql
SELECT * FROM users WHERE UPPER(full_name) = 'ALICE';  -- full scan, can't use idx on full_name
```

The function-based index pre-computes `UPPER(full_name)` and indexes it.

## Common use cases

- **Case-insensitive search**: `CREATE INDEX idx_upper_name ON users(UPPER(name));`
- **Computed columns**: `CREATE INDEX idx_total ON orders(unit_price * quantity);`
- **Substring**: `CREATE INDEX idx_email_domain ON users(SUBSTR(email, INSTR(email, '@')+1));`

## Project Connection

The advanced redesign uses:
```sql
CREATE INDEX idx_users_fn_upper ON users(UPPER(full_name));
CREATE INDEX idx_interns_fn_upper ON interns(UPPER(name)) LOCAL;
```

These make case-insensitive name searches fast — `WHERE UPPER(name) LIKE 'ALI%'` uses the index.

## Common pitfalls

- **The query must use the exact same expression** as the index. `UPPER(name)` vs `upper(name)` (case in the function name doesn't matter, but `UPPER(name)` vs `LOWER(name)` does).
- **Deterministic functions only** — the function must always return the same output for the same input. `SYSDATE` or `RANDOM` can't be indexed.

## Further reading

- Oracle Database SQL Tuning Guide — Function-Based Indexes.
