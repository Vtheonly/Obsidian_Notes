---
tags: [concept, database, audit, columns]
type: concept
status: complete
related:
  - [[14 - Schema Evolution/09 - Soft Delete Pattern]]
  - [[28 - Observability/01 - Audit Logging]]
---

# Audit Columns

## What it is

Every table should have audit columns tracking when and by whom records were created/modified:

```sql
CREATE TABLE interns (
    intern_id NUMBER PRIMARY KEY,
    name VARCHAR2(100),
    ...
    created_at TIMESTAMP WITH LOCAL TIME ZONE DEFAULT SYSTIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH LOCAL TIME ZONE,
    created_by VARCHAR2(50),
    updated_by VARCHAR2(50),
    deleted_at TIMESTAMP WITH LOCAL TIME ZONE
);
```

## Why

- **Traceability** — "who changed this, and when?"
- **Compliance** — GDPR Article 30, SOC 2 CC7.2 require records of processing.
- **Debugging** — "this intern's status changed yesterday; who changed it?"
- **Soft delete** — `deleted_at` is an audit column.

## Maintaining audit columns

### Via triggers
```sql
CREATE OR REPLACE TRIGGER trg_interns_updated
BEFORE UPDATE ON interns
FOR EACH ROW
BEGIN
    :new.updated_at := SYSTIMESTAMP;
    :new.updated_by := SYS_CONTEXT('USERENV', 'SESSION_USER');
END;
```

### Via JPA/Hibernate
```java
@Entity
@EntityListeners(AuditListener.class)
public class Intern {
    @CreatedDate
    private Instant createdAt;

    @LastModifiedDate
    private Instant updatedAt;

    @CreatedBy
    private String createdBy;

    @LastModifiedBy
    private String updatedBy;
}
```

### Via application code
```java
intern.setUpdatedAt(Instant.now());
intern.setUpdatedBy(currentUser.getUsername());
repository.save(intern);
```

## Project Connection

The project has **no audit columns**. You can't tell who created an intern, when, or who last modified it. The fix: add `created_at`, `updated_at`, `created_by`, `updated_by`, `deleted_at` to every table. Maintain via triggers or application code.

For full audit history (every change, not just the last), see [[28 - Observability/01 - Audit Logging]] and the `audit_logs` table.

## Further reading

- Spring Data Auditing documentation.
