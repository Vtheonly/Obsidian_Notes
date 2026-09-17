---
tags: [concept, database, oracle, plsql]
type: concept
status: complete
related:
  - [[08 - Relational DB Foundations/14 - SQL Basics]]
  - [[12 - Advanced Database Features/15 - Triggers]]
---

# PL/SQL Basics

## What it is

**PL/SQL** (Procedural Language/SQL) is Oracle's procedural extension to SQL. It adds variables, control structures (if/else, loops), exceptions, procedures, functions, packages, and triggers.

## Anonymous block

```sql
DECLARE
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count FROM interns WHERE status = 'Pending';
    IF v_count > 0 THEN
        DBMS_OUTPUT.PUT_LINE('Pending interns: ' || v_count);
    ELSE
        DBMS_OUTPUT.PUT_LINE('No pending interns.');
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
END;
/
```

- `DECLARE` (optional) — variable declarations.
- `BEGIN ... END;` — the body.
- `EXCEPTION` (optional) — error handling.
- `/` — block terminator (in SQL*Plus, SQL Developer).

## Procedures and functions

```sql
CREATE OR REPLACE PROCEDURE accept_intern(p_intern_id IN NUMBER, p_chief_id IN NUMBER) AS
BEGIN
    UPDATE interns SET status = 'Accepted', decided_by = p_chief_id, decided_at = SYSTIMESTAMP
    WHERE intern_id = p_intern_id AND status = 'Pending';
    IF SQL%ROWCOUNT = 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Intern not found or not pending');
    END IF;
    COMMIT;
END accept_intern;
/

CREATE OR REPLACE FUNCTION count_pending(p_dept_id IN NUMBER) RETURN NUMBER AS
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count FROM interns WHERE department_id = p_dept_id AND status = 'Pending';
    RETURN v_count;
END count_pending;
/
```

## Packages

A package groups related procedures, functions, types, and variables.

```sql
CREATE OR REPLACE PACKAGE intern_pkg AS
    PROCEDURE accept_intern(p_intern_id IN NUMBER, p_chief_id IN NUMBER);
    FUNCTION count_pending(p_dept_id IN NUMBER) RETURN NUMBER;
END intern_pkg;
/

CREATE OR REPLACE PACKAGE BODY intern_pkg AS
    PROCEDURE accept_intern(p_intern_id IN NUMBER, p_chief_id IN NUMBER) AS
    BEGIN
        -- implementation
    END;
    FUNCTION count_pending(p_dept_id IN NUMBER) RETURN NUMBER AS
        v_count NUMBER;
    BEGIN
        -- implementation
        RETURN v_count;
    END;
END intern_pkg;
/
```

## PL/SQL collections

```sql
TYPE number_list IS TABLE OF NUMBER INDEX BY PLS_INTEGER;
v_ids number_list;
v_ids(1) := 123;
```

## FORALL (bulk DML)

```sql
FORALL i IN 1..v_ids.COUNT
    UPDATE interns SET status = 'Accepted' WHERE intern_id = v_ids(i);
```

Much faster than row-by-row updates.

## Project Connection

The project uses PL/SQL in `DROP.sql` (anonymous block to drop tables) and `insertion.sql` (anonymous block to drop tables idempotently). The advanced redesign uses PL/SQL for:
- VPD security packages (`sec_context_pkg`).
- Triggers (`trg_interns_updated` to maintain `updated_at`).
- Audit logging.

## Common pitfalls

- **Slow row-by-row processing** — use `FORALL` / `BULK COLLECT` for bulk operations.
- **Exceptions swallowed** — `WHEN OTHERS THEN NULL` hides bugs. At minimum log.
- **Implicit conversions** — `v_count := 'abc'` may silently convert. Use typed variables.

## Further reading

- *Oracle PL/SQL Programming* (Feuerstein).
- Oracle Database PL/SQL Language Reference.
