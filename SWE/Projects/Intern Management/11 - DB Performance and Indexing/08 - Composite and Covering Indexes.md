---
tags: [concept, database, indexing, composite, covering]
type: concept
status: complete
prerequisites:
  - [[11 - DB Performance and Indexing/01 - B-Tree Index]]
---

# Composite and Covering Indexes

## Composite index

An index on multiple columns:
```sql
CREATE INDEX idx_interns_dept_status ON interns(department_id, status);
```

Best for queries that filter on both columns:
```sql
SELECT * FROM interns WHERE department_id = 5 AND status = 'Pending';
```

## Column order matters

The index is sorted by the first column, then the second, etc. The index helps:
- `WHERE department_id = 5` ✓ (uses the index)
- `WHERE department_id = 5 AND status = 'Pending'` ✓
- `WHERE status = 'Pending'` ✗ (can't use the index — status is not the leading column)

Rule of thumb: **most selective column first** (or the column always queried).

## Covering index

A **covering index** includes all columns the query needs, so the query can be answered from the index alone (no table access).

```sql
-- Query
SELECT intern_id, name, email FROM interns WHERE department_id = 5;

-- Covering index
CREATE INDEX idx_interns_dept_covering ON interns(department_id, intern_id, name, email);
```

The index has all 4 columns. The query reads only the index, not the table. Much faster.

## Oracle "INCLUDING" clause (12c+)

```sql
CREATE INDEX idx_interns_dept ON interns(department_id) INCLUDING (name, email);
```

The `INCLUDING` columns are stored in the index but not used for sorting. They're there only for covering.

## Trade-offs

- **Faster reads** — covering indexes eliminate table access.
- **Slower writes** — every index must be updated on INSERT/UPDATE/DELETE.
- **More storage** — indexes take space.

Don't index every column — pick the queries that matter.

## Project Connection

The project has no composite or covering indexes. The advanced redesign uses:
```sql
CREATE INDEX idx_interns_dept_status ON interns(department_id, status);
```

For the dashboard's "pending interns by department" query.

## Further reading

- *SQL Performance Explained* (Markus Winand).
