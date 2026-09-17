---
tags: [concept, database, compression, advanced]
type: concept
status: complete
related:
  - [[12 - Advanced Database Features/11 - SecureFiles LOBs]]
---

# Table Compression

## What it is

**Table compression** reduces storage by deduplicating repeated values within data blocks.

## Oracle compression types

| Type | Syntax | When |
|---|---|---|
| Basic | `COMPRESS` | OLTP, read-heavy. Older. |
| Advanced Row | `ROW STORE COMPRESS ADVANCED` | OLTP, mixed read/write. |
| Hybrid Columnar (HAC) | `COLUMN STORE COMPRESS FOR OLTP` / `QUERY HIGH` | Exadata, data warehouse. |

## How it works

Oracle's advanced compression deduplicates repeated values within a data block:
```
Block:
  Row 1: dept=1, status='Pending', ...
  Row 2: dept=1, status='Pending', ...
  Row 3: dept=1, status='Accepted', ...

Compressed:
  Symbol table: dept=1 → symbol A, status='Pending' → symbol B, status='Accepted' → symbol C
  Row 1: A, B, ...
  Row 2: A, B, ...
  Row 3: A, C, ...
```

Repeated values are stored once; rows reference them by symbol.

## Benefits

- **Storage** — 2-4x compression for typical data.
- **I/O** — fewer disk reads (more rows per block).
- **Buffer cache** — more rows fit in memory.
- **Network** — less data transferred.

## Trade-offs

- **CPU** — compression/decompression takes CPU. Small overhead on reads, more on writes.
- **Best for low-entropy data** — columns with few distinct values compress well (status, department_id). High-entropy columns (UUIDs, hashes) don't compress.

## Project Connection

The advanced redesign uses `ROW STORE COMPRESS ADVANCED` on:
- `departments`
- `users`
- `interns`
- `intern_assignments`
- `audit_logs`

These tables have low-cardinality columns (status, department_id, role_id) that compress well. The historic partition of `interns` is also compressed.

```sql
CREATE TABLE interns (...) ROW STORE COMPRESS ADVANCED
PARTITION BY RANGE (start_date) INTERVAL (...) (
    PARTITION p_historic VALUES LESS THAN (...) ROW STORE COMPRESS ADVANCED
);
```

## Further reading

- Oracle Database Administrator's Guide — Table Compression.
