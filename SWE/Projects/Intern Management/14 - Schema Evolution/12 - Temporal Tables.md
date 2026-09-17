---
tags: [concept, database, schema-evolution, temporal-tables]
type: concept
status: complete
prerequisites:
  - [[14 - Schema Evolution/01 - Audit Columns]]
related:
  - [[12 - Advanced Database Features/01 - Audit Logs]]
  - [[12 - Advanced Database Features/09 - Partitioning - Range, List, Hash, Interval]]
---

# Temporal Tables

## What it is

A **temporal table** (also called a **system-versioned table** or **history table**) keeps **every version** of every row, with the time range during which each version was current. You can query the table "as of" any point in time.

The SQL:2011 standard introduced `FOR SYSTEM_TIME AS OF` syntax, supported by SQL Server (2016+), PostgreSQL (with `temporal_tables` extension), MariaDB, and DB2. **Oracle does not have native system-versioned tables** in this syntax - but it has **Flashback Data Archive** (FDA), which is equivalent.

## SQL:2011 syntax (on supporting databases)

```sql
CREATE TABLE intern (
    intern_id   NUMBER,
    name        VARCHAR2(100),
    is_accepted VARCHAR2(10),
    sys_start   TIMESTAMP GENERATED ALWAYS AS ROW START NOT NULL,
    sys_end     TIMESTAMP GENERATED ALWAYS AS ROW END NOT NULL,
    PERIOD FOR SYSTEM_TIME (sys_start, sys_end)
)
WITH SYSTEM VERSIONING;

-- Insert/update/delete as usual; the database maintains history automatically.

-- Query the current state
SELECT * FROM intern;

-- Query as of a point in time
SELECT * FROM intern FOR SYSTEM_TIME AS OF TIMESTAMP '2024-03-01 10:00:00';

-- Query all versions ever
SELECT * FROM intern FOR SYSTEM_TIME FROM TIMESTAMP '2024-01-01 00:00:00'
                                  TO   TIMESTAMP '2024-04-01 00:00:00';
```

The database stores a "current" table and a "history" table (or partitions). On UPDATE/DELETE, the old version is moved to history with its `sys_end` set to "now"; the new version is inserted into current with `sys_start` = "now".

## Oracle's Flashback Data Archive

Oracle's FDA (a.k.a. Total Recall) gives the same capability:

```sql
-- Create a flashback archive (a repository for historical data)
CREATE FLASHBACK ARCHIVE DEFAULT fla1
    TABLESPACE users
    QUOTA 10G
    RETENTION 1 YEAR;

-- Attach it to a table
ALTER TABLE intern FLASHBACK ARCHIVE fla1;
```

Now every change to `intern` is automatically archived for 1 year. Query as of a point in time:

```sql
SELECT * FROM intern AS OF TIMESTAMP (SYSTIMESTAMP - INTERVAL '1' DAY);
```

Or see all versions of a row:

```sql
SELECT * FROM intern
VERSIONS BETWEEN TIMESTAMP (SYSTIMESTAMP - INTERVAL '7' DAY) AND SYSTIMESTAMP
WHERE intern_id = 42;
```

FDA is **transactional** - it stores the undo in a dedicated archive, not in the undo tablespace, so it survives long after the undo retention expires.

## Why temporal tables exist

- **Compliance** - "show me the state of this account on March 15." SOX, GDPR (right to be informed), and HIPAA all require historical queries.
- **Audit** - "what did this row look like before the bug?"
- **Forensics** - "when did this value change, and to what?"
- **Time-travel queries** - "what was the intern count per department last quarter?"

Temporal tables answer these without a custom audit log. The database does the work; you write the query.

## When to use vs. a custom audit log

| Aspect | Temporal table | Custom audit log |
|---|---|---|
| Setup | One DDL statement | Custom table + triggers |
| Storage | Automatic (compressed history) | Manual |
| Query | `AS OF` / `VERSIONS BETWEEN` | SQL on the audit table |
| Attribution | Limited (DB user, SCN) | Full (any columns you want) |
| Schema evolution | Hard (history is frozen) | Easy (JSON snapshots) |
| License | FDA is an EE option (extra cost) | Free |

For most apps, a custom [[12 - Advanced Database Features/01 - Audit Logs]] table with JSON snapshots is more flexible and free. For compliance-driven apps (financial, healthcare), temporal tables are the gold standard.

## Project Connection

The project has neither temporal tables nor an audit log. The redesign proposes a custom `audit_logs` table (see [[12 - Advanced Database Features/01 - Audit Logs]]) with JSON before/after snapshots, populated by triggers. This is the right choice for the project's scope and license (XE doesn't include FDA).

If the project later needs point-in-time queries on `intern`, the team can either:

- Migrate to Enterprise Edition with FDA.
- Use the `audit_logs` table's `after_snapshot` columns to reconstruct state.

## Common pitfalls

- Forgetting that temporal tables grow without bound - retention policies are essential.
- Expecting temporal queries to be as fast as current-state queries - they scan history, which is larger.
- Using FDA on XE - it's an EE feature; XE doesn't include it.
- Confusing `valid time` (when the fact was true in the real world) with `system time` (when the database knew about it). SQL:2011 supports both; most apps only need system time.

## Further reading

- SQL:2011 standard, "Temporal Tables".
- Oracle Docs, "Flashback Data Archive".
- [[14 - Schema Evolution/01 - Audit Columns]]
- [[12 - Advanced Database Features/01 - Audit Logs]]
