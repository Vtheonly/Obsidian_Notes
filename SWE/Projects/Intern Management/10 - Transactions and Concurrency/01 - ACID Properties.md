---
tags: [concept, database, transactions, acid]
type: concept
status: complete
related:
  - [[10 - Transactions and Concurrency/05 - Isolation Levels]]
  - [[05 - Software Architecture/18 - Unit of Work Pattern]]
---

# ACID Properties

## The four properties

A **transaction** is a unit of work that satisfies ACID:

### Atomicity
**All or nothing.** Either all operations in the transaction succeed, or none do. If any operation fails, the entire transaction rolls back.

### Consistency
**Valid state to valid state.** The transaction brings the database from one valid state to another. Constraints (PK, FK, CHECK, UNIQUE) are enforced. If a transaction would violate a constraint, it rolls back.

### Isolation
**Concurrent transactions don't interfere.** Two transactions running in parallel produce the same result as if they ran sequentially. (In practice, full isolation is expensive; databases offer multiple isolation levels — see [[10 - Transactions and Concurrency/05 - Isolation Levels]].)

### Durability
**Committed data survives crashes.** Once a transaction commits, the data is written to disk (or a redo log) and survives power loss, OS crash, or DB crash.

## The transaction lifecycle

```sql
BEGIN TRANSACTION;
-- or in Oracle: SET TRANSACTION ...
INSERT INTO interns ...;
UPDATE themes ...;
DELETE FROM old_assignments ...;
COMMIT;  -- or ROLLBACK;
```

If the connection drops before COMMIT, the DB rolls back automatically.

## Auto-commit

By default, JDBC connections are in **auto-commit** mode: every statement is its own transaction, committed immediately. To group multiple statements:

```java
conn.setAutoCommit(false);
try {
    // multiple statements
    conn.commit();
} catch (SQLException e) {
    conn.rollback();
}
```

## Project Connection

The project has **no transactions** — auto-commit is on for every operation. Multi-step operations (insert intern + insert assignment) are not atomic. If the second insert fails, the first is already committed — inconsistent state.

The fix:
```java
try (Connection conn = dataSource.getConnection()) {
    conn.setAutoCommit(false);
    try {
        internRepository.save(conn, intern);
        assignmentRepository.save(conn, assignment);
        auditRepository.log(conn, "CREATE", intern);
        conn.commit();
    } catch (SQLException e) {
        conn.rollback();
        throw e;
    }
}
```

Or with Spring `@Transactional`:
```java
@Transactional
public void createIntern(Intern intern) {
    internRepository.save(intern);
    assignmentRepository.save(assignment);
    auditRepository.log("CREATE", intern);
}
```

## Further reading

- Gray & Reuter, *Transaction Processing* (1993).
- *Designing Data-Intensive Applications* (Kleppmann), Chapter 7.
