---
tags: [concept, database, materialized-views, performance]
type: concept
status: complete
related:
  - [[12 - Advanced Database Features/10 - Partitioning]]
  - [[09 - Normalization/03 - Denormalization]]
---

# Materialized Views

## What it is

A **materialized view (MV)** is a pre-computed query result stored as a table. Unlike a regular view (which is just a saved query), an MV stores the actual data.

## When to use

- **Expensive aggregates** — `COUNT`, `SUM`, `AVG` over millions of rows.
- **Complex joins** — pre-compute the join.
- **Dashboard queries** — queries that run frequently but don't need real-time data.

## Creation

```sql
CREATE MATERIALIZED VIEW mv_dept_intern_metrics
BUILD IMMEDIATE
REFRESH FAST ON COMMIT
AS
SELECT department_id, status, COUNT(*) AS cnt
FROM interns
GROUP BY department_id, status;
```

- `BUILD IMMEDIATE` — populate the MV immediately (vs `BUILD DEFERRED` — populate later).
- `REFRESH FAST ON COMMIT` — incrementally update the MV whenever the base table changes (and commits).
- `REFRESH COMPLETE ON DEMAND` — rebuild the entire MV on demand (slower).
- `REFRESH FAST ON DEMAND` — incremental, but triggered manually.

## Materialized view log

`FAST REFRESH` requires a **materialized view log** on the base table — Oracle records changes (inserts, updates, deletes) so the MV can be updated incrementally.

```sql
CREATE MATERIALIZED VIEW LOG ON interns
WITH PRIMARY KEY, ROWID, (status, department_id) SEQUENCE;
```

## Query rewrite

Oracle can automatically rewrite a query to use the MV instead of the base table:
```sql
-- You write:
SELECT department_id, COUNT(*) FROM interns GROUP BY department_id;
-- Oracle rewrites to:
SELECT department_id, cnt FROM mv_dept_intern_metrics;
```

Enable with `QUERY REWRITE`:
```sql
ALTER SESSION SET query_rewrite_enabled = TRUE;
```

## Project Connection

The dashboard's PieChart currently uses hardcoded data. The fix:

```sql
CREATE MATERIALIZED VIEW LOG ON interns
WITH PRIMARY KEY, ROWID, (status, department_id) SEQUENCE;

CREATE MATERIALIZED VIEW mv_dept_intern_metrics
BUILD IMMEDIATE
REFRESH FAST ON COMMIT
AS
SELECT department_id, status, COUNT(*) AS status_count
FROM interns
GROUP BY department_id, status;
```

The dashboard queries `mv_dept_intern_metrics` (sub-millisecond) instead of scanning `interns` (seconds for millions of rows).

## Trade-offs

- **Faster reads** — pre-computed.
- **Slower writes** — every commit updates the MV.
- **Storage** — the MV takes space.
- **Staleness** — `ON COMMIT` is real-time; `ON DEMAND` can be stale.

## Further reading

- Oracle Database Data Warehousing Guide — Materialized Views.
