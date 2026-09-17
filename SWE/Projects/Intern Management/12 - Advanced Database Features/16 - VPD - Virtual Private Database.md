---
tags: [concept, database, oracle, security, vpd]
type: concept
status: complete
prerequisites:
  - [[08 - Relational DB Foundations/17 - Schemas and Users in Oracle]]
related:
  - [[12 - Advanced Database Features/03 - Data Redaction]]
  - [[12 - Advanced Database Features/15 - Triggers]]
---

# VPD - Virtual Private Database

## What it is

**Virtual Private Database (VPD)**, implemented via the `DBMS_RLS` package, attaches a **WHERE clause** to every query against a table, automatically, based on the current session. The user writes `SELECT * FROM intern` and the database silently rewrites it to `SELECT * FROM intern WHERE department_id = :current_user_dept`.

The filter is **invisible to the user** and **impossible to bypass** - it's applied at the parse stage, before execution. Even `SELECT *` is filtered.

## How it works

1. A **policy function** (PL/SQL function) returns a predicate string, e.g. `'department_id = 5'`.
2. A **policy** (registered via `DBMS_RLS.ADD_POLICY`) binds the function to a table, for a given statement type.
3. When the user runs a query, Oracle calls the function, gets the predicate, and appends it to the query.

```sql
-- 1. The policy function
CREATE OR REPLACE FUNCTION intern_policy_fn(
    schema_name VARCHAR2, table_name VARCHAR2
) RETURN VARCHAR2 IS
    v_dept_id NUMBER;
BEGIN
    -- Look up the current user's department
    SELECT department_id INTO v_dept_id
    FROM   worker_user WHERE username = SYS_CONTEXT('USERENV', 'SESSION_USER');
    RETURN 'department_id = ' || v_dept_id;
END;
/

-- 2. Register the policy
BEGIN
    DBMS_RLS.ADD_POLICY(
        object_schema   => 'APP_OWNER',
        object_name     => 'INTERN',
        policy_name     => 'intern_dept_isolation',
        function_schema => 'APP_OWNER',
        policy_function => 'intern_policy_fn',
        statement_types => 'SELECT, INSERT, UPDATE, DELETE'
    );
END;
/
```

Now any query on `intern` by a non-admin user gets `AND department_id = <their dept>` appended.

## Why VPD

- **Cannot be bypassed by the application**. The policy is in the database; even if the app forgets the WHERE clause, the DB adds it.
- **Cannot be bypassed by SQL\*Plus**. A DBA who connects directly is still subject to the policy (unless they're exempted via `EXEMPT ACCESS POLICY` privilege - grant carefully).
- **Centralized**. The rule lives in one function; every query automatically uses it.

Compare to application-enforced security, where every DAO method must remember to add the WHERE clause - one missed method is a data leak.

## Use cases

- **Multi-tenant isolation** - tenant A's users see only tenant A's rows.
- **Department isolation** - users see only their department's interns.
- **Compliance** - "only HR users see salary columns" (combined with [[12 - Advanced Database Features/03 - Data Redaction]] for column masking).
- **GDPR** - EU users' data is visible only to EU-region sessions.

## Performance considerations

- The policy function runs **once per query** (cached for the cursor lifetime by default).
- The appended predicate must be **indexable** - if `department_id` is unindexed, every VPD-filtered query full-scans. See [[11 - DB Performance and Indexing/17 - Missing Indexes on Foreign Keys]].
- For complex predicates, consider a **context** (`DBMS_SESSION.SET_CONTEXT`) populated at login; the policy function reads the context cheaply.

## Exemption

The `EXEMPT ACCESS POLICY` system privilege bypasses all VPD policies. Grant it only to schema-owning DBA accounts, never to the app user.

## Project Connection

The project has **no row-level security at all**. Any logged-in user (or anyone with SQL\*Plus access) can `SELECT * FROM intern` and see every department's interns. The reviews' redesign proposes a VPD policy that limits each user to their department:

```sql
BEGIN
    DBMS_RLS.ADD_POLICY(
        object_schema   => 'APP_OWNER',
        object_name     => 'INTERN',
        policy_name     => 'intern_dept_isolation',
        function_schema => 'APP_OWNER',
        policy_function => 'intern_dept_policy_fn',
        statement_types => 'SELECT, UPDATE, DELETE'
    );
END;
/
```

Admins get the `EXEMPT ACCESS POLICY` privilege; regular users see only their department.

## Common pitfalls

- Forgetting that VPD applies to **all** queries, including those in stored procedures and triggers - a trigger that inserts into the VPD-protected table may fail the policy.
- The policy function returning NULL (no filter) when it should return a restrictive predicate - silently turns off security.
- Not indexing the predicate column - every query full-scans.
- Granting `EXEMPT ACCESS POLICY` too broadly - bypasses all security.

## Trade-offs

- **Security vs. complexity**: VPD is more secure but adds a layer of indirection that's hard to debug.
- **Centralization vs. visibility**: the policy is invisible to the application; a developer reading the SQL doesn't see the filter.

## Further reading

- Oracle Docs, "DBMS_RLS", "Virtual Private Database".
- [[12 - Advanced Database Features/03 - Data Redaction]]
