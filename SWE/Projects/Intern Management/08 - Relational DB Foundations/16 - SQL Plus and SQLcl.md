---
tags: [concept, database, oracle, tooling]
type: concept
status: complete
prerequisites:
  - [[08 - Relational DB Foundations/14 - SQL Basics]]
related:
  - [[13 - JDBC and Data Access/04 - DataSource vs DriverManager]]
---

# SQL*Plus and SQLcl

## What it is

**SQL\*Plus** is Oracle's original command-line client - shipped since v5 (1986). It is austere: line-based editor, no history, no autocompletion. But it is **guaranteed to be present** on every Oracle installation and works over a bare SSH session.

**SQLcl** is the modern successor (free, Java-based). Same command set as SQL\*Plus, plus:
- Inline editing with arrow keys.
- `INFO` command (richer than `DESC`).
- Output as JSON, CSV, XML, INSERT statements.
- Autocompletion.
- A JavaScript engine for scripting.

```bash
# SQL*Plus
sqlplus username/password@//localhost:1521/XEPDB1

# SQLcl
sql username/password@//localhost:1521/XEPDB1
```

## Why it matters

A surprising amount of database work happens at a command line: verifying a migration ran, dumping a row for a bug report, granting a role, killing a session. Knowing the tool means you don't need a GUI to do basic ops, and your runbooks work on any server.

## Useful commands

```
SHOW  USER
SHOW  CON_NAME                  -- current container (CDB/PDB)
ALTER SESSION SET CURRENT_SCHEMA = app_owner;
DESC  intern                    -- describe columns
SET   PAGESIZE 100 LINESIZE 200
SET   SQLFORMAT ANSICONSOLE     -- SQLcl only
SELECT table_name FROM user_tables;
@path/to/script.sql             -- run a script file
@path/to/script.sql &1 &2       -- with substitution variables
SPOOL intern_report.txt         -- tee output to a file
SPOOL OFF
SET  TIMING ON                  -- print elapsed time after each statement
```

## Substitution variables

```sql
-- Accept a value at runtime
ACCEPT dept_id NUMBER PROMPT 'Department ID: '
SELECT * FROM intern WHERE department_id = &dept_id;
```

`&var` substitutes literally; `&&var` defines and reuses. Useful for ad-hoc scripts; **never** use for production queries with user input - that's SQL injection.

## Project Connection

The project's `insertion.sql` and `DROP.sql` are written for SQL\*Plus:

```sql
-- DROP.sql uses PL/SQL block with EXECUTE IMMEDIATE
BEGIN
  FOR r IN (SELECT table_name FROM user_tables) LOOP
    EXECUTE IMMEDIATE 'DROP TABLE "' || r.table_name || '" CASCADE CONSTRAINTS';
  END LOOP;
END;
/
```

The trailing `/` is **required** in SQL\*Plus to execute a PL/SQL block - JDBC doesn't need it. This is one reason the project can't just `jdbc.execute(new String(Files.readAllBytes(Paths.get("insertion.sql"))))` - the script has SQL\*Plus-specific syntax.

## Common pitfalls

- Forgetting the `/` after a PL/SQL block - SQL\*Plus sits waiting for more input.
- Using `&` substitution in scripts you mean to run from JDBC - the `&` is SQL\*Plus syntax, not SQL.
- Not setting `LINESIZE` - long rows wrap at 80 columns and become unreadable.
- Using SQL\*Plus formatting (`COLUMN ... FORMAT A20`) in scripts that other tools run - it's a SQL\*Plus command, not SQL.

## Trade-offs

- **SQL\*Plus**: tiny, ubiquitous, ugly. Use for runbooks, container startup scripts.
- **SQLcl**: bigger, needs Java, much nicer. Use for ad-hoc queries and exports.
- **SQL Developer / DBeaver**: GUIs. Use for browsing, but every GUI op should be reproducible as a script.

## Further reading

- Oracle Docs, "SQL\*Plus User's Guide and Reference".
- Jeff Smith's blog (SQLcl product manager).
- [[08 - Relational DB Foundations/03 - DDL vs DML vs DCL vs TCL]]
