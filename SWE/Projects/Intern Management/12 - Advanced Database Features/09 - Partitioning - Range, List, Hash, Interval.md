---
tags: [concept, database, oracle, partitioning]
type: concept
status: complete
prerequisites:
  - [[11 - DB Performance and Indexing/02 - B-tree Indexes]]
related:
  - [[12 - Advanced Database Features/01 - Audit Logs]]
  - [[14 - Schema Evolution/01 - Audit Columns]]
---

# Partitioning - Range, List, Hash, Interval

## What it is

**Partitioning** splits one logical table into multiple physical segments (partitions), each stored separately. Queries that touch one partition don't read the others; queries that touch all partitions parallelize across them. It's the standard technique for tables over ~10M rows.

Oracle supports four partitioning strategies:

### Range

Each partition holds rows where the partition key falls in a range.

```sql
CREATE TABLE audit_log (
    id         NUMBER GENERATED ALWAYS AS IDENTITY,
    log_time   TIMESTAMP NOT NULL,
    action     VARCHAR2(50),
    payload    CLOB
)
PARTITION BY RANGE (log_time) (
    PARTITION p_2024_01 VALUES LESS THAN (TO_DATE('2024-02-01','YYYY-MM-DD')),
    PARTITION p_2024_02 VALUES LESS THAN (TO_DATE('2024-03-01','YYYY-MM-DD')),
    PARTITION p_2024_03 VALUES LESS THAN (TO_DATE('2024-04-01','YYYY-MM-DD')),
    PARTITION p_future VALUES LESS THAN (MAXVALUE)
);
```

Classic for time-series data. Old partitions can be archived/dropped without affecting new data.

### List

Each partition holds rows matching a discrete value.

```sql
CREATE TABLE intern
PARTITION BY LIST (department_region) (
    PARTITION p_east VALUES ('NY', 'Boston', 'Miami'),
    PARTITION p_west VALUES ('LA', 'SF', 'Seattle'),
    PARTITION p_other VALUES (DEFAULT)
);
```

Good for categorical keys like region, country, status.

### Hash

Each partition holds rows whose partition key hashes to that partition.

```sql
CREATE TABLE intern
PARTITION BY HASH (intern_id)
PARTITIONS 8;
```

Good for distributing load evenly when no natural range/list exists. No partition pruning by value (you can't say "give me partition 3"), but parallel scans work.

### Interval (the modern range)

**Interval partitioning** creates range partitions **automatically** as data arrives, instead of requiring you to pre-create them.

```sql
CREATE TABLE intern (
    intern_id   NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name        VARCHAR2(100),
    start_date  DATE NOT NULL,
    ...
)
PARTITION BY RANGE (start_date)
INTERVAL (NUMTOYMINTERVAL(1, 'MONTH'))
(
    PARTITION p_initial VALUES LESS THAN (TO_DATE('2024-01-01','YYYY-MM-DD'))
);
```

When a row arrives with `start_date = '2024-02-15'`, Oracle automatically creates a partition for February 2024. No DBA intervention needed.

The reviews' redesign uses **interval partitioning by 30-day intervals** on the `audit_logs` table:

```sql
PARTITION BY RANGE (created_at)
INTERVAL (NUMTODSINTERVAL(30, 'DAY'))
(
    PARTITION p_initial VALUES LESS THAN (TIMESTAMP '2024-01-01 00:00:00')
);
```

## Subpartitioning

You can combine: range on top, hash or list below.

```sql
PARTITION BY RANGE (log_time)
INTERVAL (NUMTODSINTERVAL(1, 'DAY'))
SUBPARTITION BY HASH (id) SUBPARTITIONS 4
```

Each day's partition is further split into 4 hash subpartitions - useful for parallel scans.

## Why partition

1. **Partition pruning** - `WHERE log_time >= DATE '2024-02-01'` skips all other partitions. A 5-year audit log with daily partitions scans 1 day, not 1825.
2. **Partition exchange** - swap a partition with a standalone table in O(1). Use for data loads and archiving.
3. **Parallel query** - each partition can be scanned by a different parallel slave.
4. **Maintenance** - drop a month's data with `ALTER TABLE ... DROP PARTITION` (DDL, near-instant) instead of `DELETE` (DML, slow, generates undo/redo).

## When NOT to partition

- Tables under 10M rows - the overhead exceeds the benefit.
- When the partition key isn't in most queries - you can't prune, and you've added overhead.
- When you'd partition on a column that changes often - row movement between partitions is expensive.

## Project Connection

The project doesn't partition anything. The redesign proposes interval partitioning on `intern.start_date` (so interns can be archived by cohort) and on `audit_logs.created_at` (so old audit data can be dropped cheaply). See [[12 - Advanced Database Features/01 - Audit Logs]].

## Common pitfalls

- Forgetting to include the partition key in the PK / UNIQUE constraint. Oracle requires the partition key to be a subset of every unique constraint.
- Choosing a partition key that's not in your queries - no pruning, all partitions scanned.
- Interval partitioning with too-fine a granularity (e.g., hourly) - you end up with thousands of partitions; the data dictionary slows down.

## Trade-offs

- **Partition pruning vs. global indexes**: a global index spans all partitions; it enables lookups but defeats pruning. A local index is per-partition; it enables pruning but can't enforce global uniqueness (without the partition key).
- **Range vs. interval**: range is explicit (you manage partitions); interval is automatic (Oracle creates them).
- **Hash vs. list**: hash distributes evenly but doesn't prune by value; list prunes by value but can be uneven.

## Further reading

- Oracle Docs, "Partitioning Concepts".
- [[12 - Advanced Database Features/01 - Audit Logs]]
