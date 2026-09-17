---
tags: [concept, database, performance, batch]
type: concept
status: complete
related:
  - [[13 - JDBC and Data Access/09 - PreparedStatement]]
---

# Batch Operations

## What it is

**Batch operations** send multiple INSERT/UPDATE/DELETE statements in one network round-trip, instead of one round-trip per statement.

## JDBC batch

```java
try (PreparedStatement ps = conn.prepareStatement("INSERT INTO interns (name, age) VALUES (?, ?)")) {
    for (Intern intern : interns) {
        ps.setString(1, intern.getName());
        ps.setInt(2, intern.getAge());
        ps.addBatch();  // queue the statement
    }
    int[] results = ps.executeBatch();  // execute all at once
}
```

`executeBatch` returns an array of update counts (one per statement).

## Performance

- **Without batch**: N statements × ~10 ms round-trip = N × 10 ms.
- **With batch**: 1 round-trip for N statements = ~10 ms.

For 100 inserts:
- Without: 1000 ms.
- With: 10 ms.

100x faster.

## rewriteBatchedStatements

For MySQL, add `rewriteBatchedStatements=true` to the URL — the driver rewrites N separate INSERTs into one `INSERT ... VALUES (...), (...), (...)`. Even faster.

Oracle's driver has similar optimizations via `setDefaultExecuteBatch` and `setExecuteBatch`.

## Spring JdbcTemplate batch

```java
jdbcTemplate.batchUpdate(
    "INSERT INTO interns (name, age) VALUES (?, ?)",
    new BatchPreparedStatementSetter() {
        public void setValues(PreparedStatement ps, int i) throws SQLException {
            ps.setString(1, interns.get(i).getName());
            ps.setInt(2, interns.get(i).getAge());
        }
        public int getBatchSize() { return interns.size(); }
    }
);
```

## When to batch

- **Bulk imports** — CSV upload, data migration.
- **Bulk updates** — "accept all pending interns."
- **Bulk deletes** — cleanup jobs.

## When NOT to batch

- Single statements (no benefit).
- When you need generated keys per row (batch + `RETURN_GENERATED_KEYS` is awkward).

## Project Connection

The project's `setAllInternsAccepted` / `setAllInternsRejected` do a single `UPDATE` (efficient), but there's no batch insert path. Importing 100 interns from a CSV would be 100 separate INSERTs.

The fix: a `BatchImportService` using `addBatch` / `executeBatch`.

## Further reading

- JDBC `Statement.addBatch` documentation.
- Oracle JDBC batch documentation.
