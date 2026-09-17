---
tags: [concept, database, spring, transactions]
type: concept
status: complete
prerequisites:
  - [[10 - Transactions and Concurrency/01 - ACID Properties]]
---

# Transaction Propagation (Spring)

## What it is

Spring's `@Transactional(propagation = ...)` defines how a method behaves when called from within an existing transaction.

## Propagation types

| Type | Behavior |
|---|---|
| **REQUIRED** (default) | Use the existing transaction; if none, create one. |
| **REQUIRES_NEW** | Suspend the existing transaction; create a new one. |
| **NESTED** | Use the existing transaction; create a savepoint. |
| **SUPPORTS** | Use the existing transaction; if none, run without one. |
| **NOT_SUPPORTED** | Suspend the existing transaction; run without one. |
| **MANDATORY** | Use the existing transaction; if none, throw. |
| **NEVER** | Run without a transaction; if one exists, throw. |

## Examples

### REQUIRED (most common)
```java
@Transactional
public void createIntern(Intern intern) {
    internRepository.save(intern);  // @Transactional(REQUIRED) — same transaction
    auditService.log("CREATE", intern);  // @Transactional(REQUIRED) — same transaction
}
```
If any method fails, the whole transaction rolls back.

### REQUIRES_NEW
```java
@Transactional
public void createIntern(Intern intern) {
    internRepository.save(intern);
    try {
        notificationService.send(intern);  // @Transactional(REQUIRES_NEW)
    } catch (Exception e) {
        // notification failed, but intern is still saved
    }
}
```
The notification runs in a separate transaction. If it fails, the outer transaction continues.

### NESTED
```java
@Transactional
public void createIntern(Intern intern) {
    internRepository.save(intern);
    try {
        assignmentService.assign(intern, theme);  // @Transactional(NESTED)
    } catch (Exception e) {
        // assignment rolled back to savepoint, intern stays
    }
}
```

## When to use

- **REQUIRED** — default. Most use cases.
- **REQUIRES_NEW** — for operations that must succeed/fail independently (e.g., audit logging that must persist even if the main operation fails).
- **NESTED** — for partial rollback within the same transaction.

## Project Connection

The project has no transactions. The fix introduces Spring `@Transactional(REQUIRED)` on service methods.

## Further reading

- Spring Framework documentation — Transaction Management.
