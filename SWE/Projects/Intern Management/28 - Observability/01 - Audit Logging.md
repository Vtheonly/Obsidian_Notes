---
tags: [concept, observability, audit, compliance]
type: concept
status: complete
related:
  - [[14 - Schema Evolution/01 - Audit Columns]]
  - [[12 - Advanced Database Features/15 - Triggers]]
---

# Audit Logging

## What it is

**Audit logging** records every mutation (create, update, delete) for compliance and debugging. Unlike application logs (for developers), audit logs are for auditors, security teams, and compliance.

## What to log

- **Who** — user ID, username, role.
- **What** — action (CREATE, UPDATE, DELETE), entity type, entity ID.
- **When** — timestamp.
- **Before/after** — the old and new state (for UPDATE).
- **Where** — IP address, session ID.
- **Why** — reason (if available, e.g., "user requested deletion").

## Schema

```sql
CREATE TABLE audit_logs (
    audit_id NUMBER(19) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    timestamp TIMESTAMP WITH LOCAL TIME ZONE DEFAULT SYSTIMESTAMP NOT NULL,
    changed_by_user VARCHAR2(50) NOT NULL,
    action_type VARCHAR2(20) NOT NULL,  -- INSERT, UPDATE, DELETE
    table_name VARCHAR2(50) NOT NULL,
    record_id NUMBER(10) NOT NULL,
    old_state CLOB,  -- JSON snapshot before
    new_state CLOB   -- JSON snapshot after
);
```

## Implementation

### Application-level

```java
public class AuditService {
    private final ThreadLocal<String> currentUser = ThreadLocal.withInitial(() -> "SYSTEM");

    public void setCurrentUser(String username) { currentUser.set(username); }

    public void log(String action, String table, long recordId, Object oldState, Object newState) {
        AuditLog log = new AuditLog(
            currentUser.get(),
            action,
            table,
            recordId,
            toJson(oldState),
            toJson(newState)
        );
        auditRepository.save(log);
    }
}
```

### Database-level (triggers)

```sql
CREATE TRIGGER audit_intern_update
AFTER UPDATE ON interns
FOR EACH ROW
BEGIN
    INSERT INTO audit_logs (changed_by_user, action_type, table_name, record_id, old_state, new_state)
    VALUES (SYS_CONTEXT('USERENV', 'SESSION_USER'), 'UPDATE', 'interns', :old.intern_id,
            JSON_OBJECT(...), JSON_OBJECT(...));
END;
```

Triggers catch every change, even from direct SQL. But they're invisible to the app (harder to debug).

## Why

- **Compliance** — GDPR Article 30, SOC 2 CC7.2 require audit trails.
- **Security** — "who changed this intern's status?"
- **Debugging** — "the intern says their status changed; let me check the audit log."
- **Non-repudiation** — the user can't deny making a change.

## Project Connection

The project has no audit logging. Every change overwrites the previous state; there's no history.

The fix:
- `audit_logs` table (partitioned, as in the advanced redesign).
- `AuditService` called by every service method that mutates.
- An "Audit Log" view for admins.
- The audit log is append-only (no UPDATE, no DELETE).

## Further reading

- GDPR Article 30.
- SOC 2 CC7.2.
