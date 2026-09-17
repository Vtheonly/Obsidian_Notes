---
tags: [concept, security, least-privilege]
type: concept
status: complete
related:
  - [[16 - Authentication and Authorization/09 - RBAC (Role-Based Access Control)]]
  - [[17 - Application Security/09 - Secrets Management]]
---

# Principle of Least Privilege

> "Every module, every user, every process should have the least privilege necessary to do its job." — Saltzer & Schroeder, 1975

## What it means

Give an entity (user, service, process) only the permissions it needs — nothing more.

## Application

### Database user
The app should connect as a user with only the permissions it needs:
```sql
CREATE USER intern_app IDENTIFIED BY ...;
GRANT SELECT, INSERT, UPDATE, DELETE ON interns TO intern_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON users TO intern_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON themes TO intern_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON departments TO intern_app;
GRANT SELECT, INSERT ON audit_logs TO intern_app;
-- NO DROP, NO ALTER, NO GRANT, NO SYSDBA
```

If the app is compromised (e.g., SQL injection), the attacker can only do what `intern_app` can do — not `DROP DATABASE`.

### Application user
Users should have only the role they need:
- A secretary can create interns, not delete users.
- A chief can accept/reject interns, not create users.
- An admin can do everything.

### Service account
A microservice should have only the permissions it needs to call other services.

## The project's violation

The project connects as **`system`** — Oracle's SYSDBA-privileged account. `system` can:
- `DROP DATABASE`.
- `ALTER SYSTEM`.
- Access any table in any schema.
- Bypass all security controls.

If the app is compromised (and with SQL injection, it can be), the attacker has full DB control.

## The fix

```sql
CREATE USER intern_app IDENTIFIED BY securepassword;
GRANT CREATE SESSION TO intern_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON interns TO intern_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON users TO intern_app;
-- ... etc.

-- Or use a role:
CREATE ROLE intern_app_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON interns TO intern_app_role;
GRANT intern_app_role TO intern_app;
```

Then connect as `intern_app`, not `system`.

## Further reading

- Saltzer & Schroeder, "The Protection of Information in Computer Systems" (1975).
- NIST SP 800-53 (AC-6 Least Privilege).
