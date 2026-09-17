---
tags: [concept, database, transactions, savepoints]
type: concept
status: complete
prerequisites:
  - [[10 - Transactions and Concurrency/01 - ACID Properties]]
---

# Savepoints and Nested Transactions

## What it is

A **savepoint** is a marker within a transaction. You can roll back to a savepoint (partial rollback) without rolling back the entire transaction.

```sql
BEGIN;
INSERT INTO interns ...;
SAVEPOINT after_intern;
INSERT INTO assignments ...;
-- assignment fails
ROLLBACK TO SAVEPOINT after_intern;  -- undo only the assignment, keep the intern
INSERT INTO audit_logs ...;
COMMIT;
```

## JDBC savepoints

```java
Connection conn = dataSource.getConnection();
conn.setAutoCommit(false);
try {
    internRepository.save(conn, intern);

    Savepoint sp = conn.setSavepoint("after_intern");
    try {
        assignmentRepository.save(conn, assignment);
    } catch (SQLException e) {
        conn.rollback(sp);  // partial rollback
        // continue — intern is still saved
    }

    auditRepository.log(conn, "CREATE", intern);
    conn.commit();
} catch (SQLException e) {
    conn.rollback();
}
```

## When to use

- **Partial success** — "insert the intern even if the email notification fails."
- **Retry within a transaction** — "try this approach; if it fails, roll back to the savepoint and try another."

## Spring nested transactions

Spring's `Propagation.NESTED` uses savepoints:
```java
@Transactional
public void createIntern(Intern intern) {
    internRepository.save(intern);
    try {
        notificationService.notify(intern);  // @Transactional(propagation = NESTED)
    } catch (NotificationFailedException e) {
        // notification rolled back, intern stays
    }
}
```

## Project Connection

The project has no transactions, hence no savepoints. The fix: explicit transactions with savepoints for partial-success operations.

## Further reading

- JDBC `Connection.setSavepoint` documentation.
- Spring `@Transactional` propagation types.
