---
tags: [concept, database, denormalization]
type: concept
status: complete
prerequisites:
  - [[09 - Normalization/08 - Third Normal Form (3NF)]]
---

# Denormalization

## What it is

**Denormalization** is the deliberate violation of normal forms, usually for performance. You add redundancy to avoid expensive joins.

## When to denormalize

- **Read-heavy workloads** — if you read the same joined data 1000x more than you write it, denormalize.
- **Reporting / OLAP** — star schemas are deliberately denormalized.
- **Materialized views** — a denormalized snapshot that's auto-maintained.
- **Caching** — store computed results to avoid recomputing.

## Examples

### 1. Storing a count
```sql
-- Normalized: compute the count on demand
SELECT department_id, COUNT(*) FROM interns GROUP BY department_id;

-- Denormalized: store the count in departments
ALTER TABLE departments ADD COLUMN intern_count NUMBER;
-- Update via trigger or application logic whenever interns change.
```

### 2. Storing a name with the FK
```sql
-- Normalized
CREATE TABLE interns (intern_id, name, department_id REFERENCES departments);

-- Denormalized
CREATE TABLE interns (intern_id, name, department_id, department_name);
-- Faster reads (no JOIN), but update anomaly risk.
```

### 3. Materialized view
```sql
CREATE MATERIALIZED VIEW dept_intern_counts
REFRESH FAST ON COMMIT
AS SELECT department_id, COUNT(*) AS cnt FROM interns GROUP BY department_id;
```

## Trade-offs

| Pro | Con |
|---|---|
| Faster reads | Slower writes (update multiple places) |
| Fewer joins | Redundancy (more storage) |
| Simpler queries | Anomaly risk (must keep copies in sync) |

## When NOT to denormalize

- **Write-heavy workloads** — every write updates multiple places.
- **When the data changes often** — keeping copies in sync is expensive.
- **Small tables** — joins on small tables are cheap; denormalization isn't worth it.

## Project Connection

The advanced schema redesign uses denormalization via **materialized views**:
```sql
CREATE MATERIALIZED VIEW mv_dept_intern_metrics
REFRESH FAST ON COMMIT
AS SELECT department_id, status, COUNT(*) FROM interns GROUP BY department_id, status;
```

The dashboard queries the MV (fast) instead of scanning `interns` (slow). Oracle keeps the MV in sync on every commit — no application-level update logic.

See [[12 - Advanced Database Features/06 - Materialized Views]].

## Further reading

- *Refactoring Databases* (Ambler & Sadalage).
