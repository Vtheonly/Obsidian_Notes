---
tags: [concept, database, sql, ddl, dml]
type: concept
status: complete
prerequisites:
  - [[08 - Relational DB Foundations/14 - SQL Basics]]
related:
  - [[10 - Transactions and Concurrency/01 - ACID Properties]]
  - [[14 - Schema Evolution/05 - Flyway]]
---

# DDL vs DML vs DCL vs TCL

## What it is

SQL statements are grouped by what they operate on:

**DDL - Data Definition Language.** Defines the schema.

```sql
CREATE TABLE intern (
    intern_id   NUMBER(10) PRIMARY KEY,
    name        VARCHAR2(100 CHAR) NOT NULL,
    is_accepted VARCHAR2(10) DEFAULT 'Pending'
        CHECK (is_accepted IN ('Accepted','Rejected','Pending'))
);
ALTER  TABLE intern ADD (start_date DATE);
DROP   TABLE intern;
TRUNCATE TABLE intern;  -- DDL-like, but really DML under the hood in Oracle
```

DDL in Oracle issues an **implicit COMMIT before and after** the statement. This surprises people: you cannot roll back a `CREATE TABLE` even if you wrap it in a transaction.

**DML - Data Manipulation Language.** Reads and changes rows.

```sql
SELECT * FROM intern;
INSERT INTO intern(intern_id, name) VALUES (1, 'Alice');
UPDATE intern SET is_accepted = 'Accepted' WHERE intern_id = 1;
DELETE FROM intern WHERE intern_id = 1;
```

DML is transactional - changes are visible only after `COMMIT`.

**DCL - Data Control Language.** Grants and revokes privileges.

```sql
GRANT  SELECT, INSERT ON intern TO app_user;
REVOKE DELETE              ON intern FROM app_user;
```

**TCL - Transaction Control Language.** Manages transactions.

```sql
COMMIT;
ROLLBACK;
SAVEPOINT before_insert;
ROLLBACK TO before_insert;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

## Why it matters

The implicit commit on DDL is the #1 reason migration tools like [[14 - Schema Evolution/05 - Flyway]] split migrations into separately-committed steps. It is also why you cannot atomically "create a table and insert into it" - the create commits before the insert runs.

## Trade-offs

- DDL is "free" to commit in Oracle, but in PostgreSQL many DDL statements (e.g., `CREATE INDEX CONCURRENTLY`) cannot run inside a transaction at all.
- `TRUNCATE` is fast (resets the high-water mark) but cannot be rolled back in some engines and bypasses FK triggers.

## Project Connection

The project's `insertion.sql` mixes DDL (`CREATE TABLE`) with DML (`INSERT` for sample data) in the same script. Because each `CREATE TABLE` commits, the sample inserts run in autocommit mode and cannot be undone if something later fails. Worse, the `DROP.sql` script uses dynamic `EXECUTE IMMEDIATE 'DROP TABLE ...'` which also commits each drop.

## Common pitfalls

- Expecting `ROLLBACK` to undo a `CREATE TABLE` - it can't.
- Running DDL mid-transaction and silently committing partial DML work.
- Confusing `DELETE` (DML, transactional, fires triggers) with `TRUNCATE` (DDL-ish, non-transactional in Oracle, doesn't fire row triggers).

## Further reading

- Oracle Docs, "SQL Statements".
- [[14 - Schema Evolution/05 - Flyway]]
