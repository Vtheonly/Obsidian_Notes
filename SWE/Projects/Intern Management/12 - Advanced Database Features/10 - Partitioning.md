---
tags: [concept, database, partitioning, advanced]
type: concept
status: complete
related:
  - [[12 - Advanced Database Features/06 - Materialized Views]]
---

# Partitioning

## What it is

**Partitioning** splits a large table into smaller, manageable pieces (partitions). Each partition is stored separately but queried as one table.

## Types

### Range partitioning
Rows are assigned to partitions based on a range of values.
```sql
CREATE TABLE interns (
    intern_id NUMBER, start_date DATE, ...
)
PARTITION BY RANGE (start_date) (
    PARTITION p_2024 VALUES LESS THAN (TO_DATE('2025-01-01', 'YYYY-MM-DD')),
    PARTITION p_2025 VALUES LESS THAN (TO_DATE('2026-01-01', 'YYYY-MM-DD')),
    PARTITION p_2026 VALUES LESS THAN (TO_DATE('2027-01-01', 'YYYY-MM-DD'))
);
```

### Interval partitioning (Oracle 11g+)
Like range, but Oracle automatically creates new partitions.
```sql
PARTITION BY RANGE (start_date) INTERVAL (NUMTOYMINTERVAL(1, 'MONTH')) (
    PARTITION p_initial VALUES LESS THAN (TO_DATE('2026-01-01', 'YYYY-MM-DD'))
);
```
A row with `start_date = '2026-06-15'` causes Oracle to auto-create a June 2026 partition.

### List partitioning
Rows assigned by a discrete value.
```sql
PARTITION BY LIST (department_id) (
    PARTITION p_dept1 VALUES (1, 2, 3),
    PARTITION p_dept2 VALUES (4, 5, 6),
    PARTITION p_other VALUES (DEFAULT)
);
```

### Hash partitioning
Rows assigned by a hash function. Distributes evenly.
```sql
PARTITION BY HASH (intern_id) PARTITIONS 4;
```

### Composite
Combine types — e.g., range-hash.
```sql
PARTITION BY RANGE (start_date)
    SUBPARTITION BY HASH (intern_id) SUBPARTITIONS 4 (
    PARTITION p_2026 VALUES LESS THAN (...),
    ...
);
```

## Benefits

### Partition pruning
Queries with a partition-key filter skip irrelevant partitions:
```sql
SELECT * FROM interns WHERE start_date BETWEEN '2026-06-01' AND '2026-06-30';
-- Only scans the June 2026 partition. Not the entire table.
```

### Partition exchange
Swap a partition with a standalone table — fast data load/archive:
```sql
ALTER TABLE interns EXCHANGE PARTITION p_2024 WITH TABLE interns_archive_2024;
```

### Partition-wise joins
Joining two partitioned tables on the partition key can join partition-by-partition, in parallel.

### Maintenance
- Drop old data: `ALTER TABLE interns DROP PARTITION p_2020;` (instant, vs. `DELETE` which is slow).
- Rebuild stats per partition.
- Compress old partitions.

## Trade-offs

- **Partitioning is an Enterprise Edition feature** — not in XE.
- **Composite PK required** — the partition key must be part of the PK. So `interns` PK becomes `(intern_id, start_date)`.
- **Foreign keys to partitioned tables** must include the partition key. So `intern_assignments` FK to `interns` is `(intern_id, intern_start_date)`.

## Project Connection

The advanced redesign uses interval partitioning on `interns.start_date` (monthly) and `audit_logs.timestamp` (30-day). This:
- Makes time-based queries fast (pruning).
- Allows dropping old partitions instead of DELETE.
- Isolates concurrent writes to different partitions (less contention).

```sql
CREATE TABLE interns (
    intern_id NUMBER(10) GENERATED ALWAYS AS IDENTITY,
    start_date DATE NOT NULL,
    ...
    CONSTRAINT pk_interns PRIMARY KEY (intern_id, start_date)
)
PARTITION BY RANGE (start_date) INTERVAL (NUMTOYMINTERVAL(1, 'MONTH')) (
    PARTITION p_historic VALUES LESS THAN (TO_DATE('2026-01-01', 'YYYY-MM-DD'))
);
```

## Further reading

- Oracle Database VLDB and Partitioning Guide.
