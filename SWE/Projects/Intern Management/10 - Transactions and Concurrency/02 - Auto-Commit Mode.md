---
tags: [concept, database, transactions, jdbc]
type: concept
status: complete
prerequisites:
  - [[10 - Transactions and Concurrency/01 - ACID Properties]]
related:
  - [[10 - Transactions and Concurrency/13 - Savepoints and Nested Transactions]]
  - [[13 - JDBC and Data Access/04 - DataSource vs DriverManager]]
---

# Auto-Commit Mode

## What it is

**Auto-commit** is the JDBC default in which every SQL statement is wrapped in its own transaction: the statement runs, the transaction commits, locks release. There is no way to group statements into a single atomic unit.

```java
Connection conn = dataSource.getConnection();
// conn.getAutoCommit() == true   // the default
PreparedStatement ps = conn.prepareStatement("INSERT INTO intern ...");
ps.executeUpdate();   // <-- COMMIT happens here, immediately
ps.close();
conn.close();
```

To get a real transaction, you turn auto-commit **off**:

```java
conn.setAutoCommit(false);
// ... multiple statements ...
conn.commit();       // or conn.rollback();
```

## Why the default is `true`

JDBC's auto-commit default is `true` for historical reasons: simple CRUD apps (one statement per request) "just work" without transaction code. For anything non-trivial - any time two writes must succeed or fail together - auto-commit is wrong.

Oracle SQL\*Plus also defaults to auto-commit OFF (the opposite of JDBC), which surprises people moving between the two. JDBC drivers for other databases (PostgreSQL, MySQL) follow JDBC's `true` default.

## What auto-commit costs you

1. **No atomicity** - if your business operation is "insert intern, insert audit log, update department count," auto-commit makes them three independent transactions. A failure between steps 2 and 3 leaves you with an intern and an audit log but a wrong count.
2. **No batch optimization** - each statement is a round-trip with its own commit. Oracle's commit cost (writing the redo log and signaling LGWR) is ~1ms; 100 statements = 100ms of pure commit overhead.
3. **No consistent reads across statements** - in `READ COMMITTED` (Oracle's default), each statement sees a fresh snapshot. Auto-commit means each statement is its own snapshot, so two statements in the "same" operation can see different data.

## The fix

```java
public void transferIntern(long internId, long oldDeptId, long newDeptId) {
    try (Connection c = dataSource.getConnection()) {
        c.setAutoCommit(false);
        try {
            try (PreparedStatement u1 = c.prepareStatement(
                    "UPDATE intern SET department_id=? WHERE intern_id=?")) {
                u1.setLong(1, newDeptId);
                u1.setLong(2, internId);
                u1.executeUpdate();
            }
            try (PreparedStatement u2 = c.prepareStatement(
                    "INSERT INTO audit_log(...) VALUES(...)")) {
                // ...
                u2.executeUpdate();
            }
            c.commit();
        } catch (SQLException e) {
            c.rollback();
            throw new DataAccessException("transfer failed", e);
        }
    } catch (SQLException e) {
        throw new DataAccessException(e);
    }
}
```

The pattern: `setAutoCommit(false)` immediately after `getConnection()`, `commit()` on success, `rollback()` on any exception, and always close the connection via try-with-resources.

## Spring's Default

Spring's `JdbcTemplate` and `@Transactional` set auto-commit to `false` automatically inside a transactional method. Outside a `@Transactional` boundary, it falls back to auto-commit. **Always** annotate service methods with `@Transactional`.

## Project Connection

`oracleConnector` does:

```java
private static Connection connection = DriverManager.getConnection(...);
// never calls setAutoCommit(false)
// every executeUpdate commits immediately
```

So the project has **no multi-statement transactions at all**. The `MAX(id)+1` pattern - which is two statements (a SELECT, then an INSERT) - is therefore an unprotected read-then-write race. See [[10 - Transactions and Concurrency/01 - ACID Properties]].

## Common pitfalls

- Forgetting that the default is `true`. Read the JDBC spec, then forget it - always set it explicitly.
- Setting `setAutoCommit(false)` and then never calling `commit()` - the transaction rolls back when the connection closes, silently losing work.
- Setting `setAutoCommit(false)` on a pooled connection and **returning it to the pool without resetting** - the next user inherits a transaction in progress. HikariCP resets this for you; raw pools may not.
- Mixing DDL (which auto-commits in Oracle) into a transaction - the DDL commits everything before it.

## Further reading

- Oracle Docs, "JDBC Developer's Guide", "Transaction Control".
- [[10 - Transactions and Concurrency/01 - ACID Properties]]
