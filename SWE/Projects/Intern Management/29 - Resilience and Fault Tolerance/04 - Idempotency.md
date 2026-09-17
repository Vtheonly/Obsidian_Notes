---
tags: [concept, resilience, idempotency]
type: concept
status: complete
related:
  - [[29 - Resilience and Fault Tolerance/06 - Retry with Backoff]]
---

# Idempotency

## What it is

An operation is **idempotent** if calling it multiple times has the same effect as calling it once.

## Examples

- **Idempotent**: `x = 5` (setting a value). `DELETE FROM interns WHERE id = 123` (deleting — second call is a no-op). HTTP PUT.
- **NOT idempotent**: `x = x + 1` (incrementing). `INSERT INTO interns (...)` (second call creates a duplicate). HTTP POST.

## Why it matters for retries

If an operation fails after partially completing, retrying it could cause side effects:
- Insert twice → duplicate row.
- Charge twice → double charge.
- Send email twice → duplicate email.

If the operation is idempotent, retrying is safe.

## Making operations idempotent

### 1. Use a unique key
```sql
INSERT INTO interns (id, name) VALUES (?, ?)
ON CONFLICT (id) DO NOTHING;
-- Second call is a no-op (PostgreSQL syntax).
```

### 2. Use an idempotency key
Client sends a unique key with each request. Server tracks keys:
```java
if (processedKeys.contains(key)) return previousResult;
// process
processedKeys.add(key);
return result;
```

### 3. Use natural keys
If the operation is "set the intern's status to Accepted," it's inherently idempotent — calling it twice leaves the status as Accepted.

## Project Connection

The project's `MAX(id)+1` insert is NOT idempotent — retrying creates a duplicate (or a PK violation, depending on timing). With IDENTITY columns, the insert is still not idempotent (each call creates a new row).

For critical operations (accept/reject intern), the operation IS idempotent — setting status to "Accepted" twice is fine.

For email sending, use an idempotency key to prevent duplicate emails on retry.

## Further reading

- *Designing Data-Intensive Applications* (Kleppmann), Chapter 11.
