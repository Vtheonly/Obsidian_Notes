---
tags: [concept, database, security, vpd, rls]
type: concept
status: complete
related:
  - [[12 - Advanced Database Features/02 - Data Redaction (DBMS_REDACT)]]
  - [[16 - Authentication and Authorization/08 - Principle of Least Privilege]]
---

# Virtual Private Database (VPD)

## What it is

**VPD** (also called Row-Level Security, RLS) is an Oracle feature that automatically appends a `WHERE` clause to every query on a table, based on the current user's context. Users see only the rows they're allowed to see — enforced by the DB, not the application.

## How it works

1. The application connects as a user.
2. A **policy function** runs, returning a predicate (e.g., `department_id = 5`).
3. Oracle appends the predicate to every query on the protected table:
   ```sql
   -- Application writes:
   SELECT * FROM interns;
   -- Oracle rewrites to:
   SELECT * FROM interns WHERE department_id = 5;
   ```

Even if the application has a SQL injection vulnerability, the user can't see other departments' rows — the DB enforces it.

## Implementation

```sql
-- 1. Create a security context package
CREATE OR REPLACE PACKAGE sec_context_pkg AS
    FUNCTION get_user_dept(p_schema VARCHAR2, p_obj VARCHAR2) RETURN VARCHAR2;
END;
/

CREATE OR REPLACE PACKAGE BODY sec_context_pkg AS
    FUNCTION get_user_dept(p_schema VARCHAR2, p_obj VARCHAR2) RETURN VARCHAR2 IS
        v_username VARCHAR2(100);
        v_role VARCHAR2(50);
        v_dept_id NUMBER;
    BEGIN
        v_username := SYS_CONTEXT('USERENV', 'SESSION_USER');
        IF v_username IN ('SYS', 'SYSTEM') THEN
            RETURN '1=1';  -- admins see everything
        END IF;

        SELECT r.role_name, u.department_id
        INTO v_role, v_dept_id
        FROM users u JOIN roles r ON u.role_id = r.role_id
        WHERE UPPER(u.username) = UPPER(v_username) AND u.deleted_at IS NULL;

        IF v_role IN ('Admin', 'Chief') THEN
            RETURN '1=1';  -- admins and chiefs see everything
        ELSE
            RETURN 'department_id = ' || v_dept_id;  -- users see only their dept
        END IF;
    END;
END;
/

-- 2. Register the policy
BEGIN
    DBMS_RLS.ADD_POLICY(
        object_schema   => 'SYSTEM',
        object_name     => 'interns',
        policy_name     => 'policy_restrict_intern_access',
        function_schema => 'SYSTEM',
        policy_function => 'sec_context_pkg.get_user_dept',
        statement_types => 'SELECT, UPDATE, DELETE',
        update_check    => TRUE,
        enable          => TRUE
    );
END;
/
```

## Why it's powerful

- **Enforced at the DB** — even if the app is compromised, the DB enforces the policy.
- **Transparent to the app** — the app writes `SELECT * FROM interns`; the DB handles the filtering.
- **Centralized** — one policy function, applied to all queries.

## Trade-offs

- **Enterprise Edition feature** — not in XE (may work in some versions, check).
- **Performance** — the policy function runs for every query. Cache the context.
- **Complexity** — debugging "why can't I see this row?" is hard (the predicate is invisible).

## Project Connection

The advanced redesign uses VPD so that:
- Standard users see only interns in their own department.
- Admins and chiefs see all interns.

Without VPD, the application would have to add `WHERE department_id = ?` to every query — easy to forget, easy to bypass with SQL injection.

## Further reading

- Oracle Database Security Guide — VPD.
