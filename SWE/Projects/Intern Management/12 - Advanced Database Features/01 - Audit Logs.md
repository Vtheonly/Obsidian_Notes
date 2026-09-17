---
tags: [concept, database, oracle, audit, pattern]
type: concept
status: complete
prerequisites:
  - [[12 - Advanced Database Features/15 - Triggers]]
related:
  - [[12 - Advanced Database Features/11 - SecureFiles LOBs]]
  - [[12 - Advanced Database Features/09 - Partitioning - Range, List, Hash, Interval]]
  - [[14 - Schema Evolution/01 - Audit Columns]]
---

# Audit Logs

## What it is

An **audit log** records every change to a table - who changed what, when, and the before/after values. It's the foundation for compliance (SOX, GDPR, HIPAA), debugging ("when did this intern's status change?"), and security forensics.

## The audit_logs table pattern

```sql
CREATE TABLE audit_logs (
    id              NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    table_name      VARCHAR2(128)  NOT NULL,
    operation       VARCHAR2(10)   NOT NULL,    -- INSERT/UPDATE/DELETE
    row_pk          VARCHAR2(4000) NOT NULL,    -- the changed row's PK as a string
    changed_by      VARCHAR2(100)  NOT NULL,
    changed_at      TIMESTAMP      DEFAULT SYSTIMESTAMP NOT NULL,
    before_snapshot CLOB,                       -- JSON of old row, NULL for INSERT
    after_snapshot  CLOB                        -- JSON of new row, NULL for DELETE
)
LOB (before_snapshot) STORE AS SECUREFILE (COMPRESS HIGH CACHE),
LOB (after_snapshot)  STORE AS SECUREFILE (COMPRESS HIGH CACHE)
PARTITION BY RANGE (changed_at)
INTERVAL (NUMTODSINTERVAL(30, 'DAY'))
(
    PARTITION p_initial VALUES LESS THAN (TIMESTAMP '2024-01-01 00:00:00')
)
ROW STORE COMPRESS ADVANCED;
```

Key design choices:

- **`before_snapshot` and `after_snapshot` as CLOB JSON** - captures the full row, schema-evolution-safe. Adding a column doesn't break old audit entries.
- **`SECUREFILE COMPRESS HIGH`** - JSON is highly repetitive; compression shrinks it 5-10x.
- **Interval partitioning by 30 days** - old partitions can be archived or dropped with `ALTER TABLE ... DROP PARTITION` (DDL, near-instant).
- **`ROW STORE COMPRESS ADVANCED`** - further compresses the non-LOB columns.
- **`row_pk` as `VARCHAR2(4000)`** - works for any table's PK, simple or composite (concatenated).

## Populating the audit log

Two main strategies:

### 1. Trigger-based (DB-enforced)

A compound trigger on each audited table captures `:OLD` and `:NEW`, serializes them to JSON, and bulk-inserts into `audit_logs` in the `AFTER STATEMENT` section. See [[12 - Advanced Database Features/15 - Triggers]].

Pros: cannot be bypassed by the application.
Cons: trigger overhead on every DML; complex PL/SQL.

### 2. Application-side (service-layer-enforced)

The service layer explicitly writes to `audit_logs` as part of each operation:

```java
@Transactional
public void updateInternStatus(long id, String newStatus, String user) {
    Intern before = repo.findById(id).orElseThrow();
    String beforeJson = toJson(before);
    before.setStatus(newStatus);
    repo.save(before);
    String afterJson = toJson(before);
    auditLog.record("INTERN", "UPDATE", String.valueOf(id), user, beforeJson, afterJson);
}
```

Pros: simple, testable, no PL/SQL.
Cons: bypassed by direct DB access (DBA, ad-hoc SQL).

Most production systems use **both**: the application-side audit for rich context (the user's intent, the request ID) and the trigger-based audit for defense in depth.

## Querying the audit log

```sql
-- Who changed intern 42's status, and when?
SELECT changed_by, changed_at,
       JSON_VALUE(before_snapshot, '$.is_accepted') AS before_status,
       JSON_VALUE(after_snapshot,  '$.is_accepted') AS after_status
FROM   audit_logs
WHERE  table_name = 'INTERN'
  AND  row_pk = '42'
ORDER  BY changed_at;
```

Oracle 21c supports JSONPath natively; earlier versions use `JSON_VALUE` (12c+) or `JSON_TABLE`.

## Why partition by 30 days

- **Pruning** - queries on recent data touch only the current partition.
- **Archiving** - `ALTER TABLE audit_logs EXCHANGE PARTITION p_2023_01 WITH TABLE audit_archive_2023_01` swaps a month out in O(1). Then drop or move the archive table.
- **Compliance** - "retain 7 years" becomes "keep 84 partitions, drop the 85th."

## Project Connection

The project has **no audit log at all**. There's no `created_at`, no `updated_at`, no `deleted_at`, no history. See [[14 - Schema Evolution/01 - Audit Columns]]. The reviews' redesign proposes the `audit_logs` table above, populated by compound triggers on `intern`, `worker_user`, `department`, and `theme`.

## Common pitfalls

- Storing the snapshot as columns instead of JSON - every schema change breaks old audit entries.
- Forgetting to redact sensitive columns from the snapshot - the audit log now stores plaintext passwords forever. See [[12 - Advanced Database Features/03 - Data Redaction]].
- Not partitioning - the audit log grows unbounded; queries slow to a crawl.
- Writing audit entries in the same transaction as the change - a trigger failure rolls back the change. (Usually desired, but not always.)
- Writing audit entries in an autonomous transaction - decouples from the change, but loses atomicity: a rollback leaves a phantom audit entry.

## Trade-offs

- **Trigger vs. application-side**: triggers are harder to bypass but harder to test.
- **Same transaction vs. autonomous**: same transaction is atomic; autonomous survives rollbacks but can lie.
- **JSON vs. columns**: JSON is schema-flexible; columns are queryable.

## Further reading

- Oracle Docs, "Flashback Data Archive" (a built-in alternative).
- [[12 - Advanced Database Features/15 - Triggers]]
- [[14 - Schema Evolution/01 - Audit Columns]]
