---
tags: [concept, jdbc, java, data-access, batch]
type: concept
status: complete
prerequisites:
  - [[13 - JDBC and Data Access/09 - PreparedStatement]]
  - [[13 - JDBC and Data Access/18 - try-with-resources]]
related:
  - [[11 - DB Performance and Indexing/03 - Batch Operations]]
  - [[13 - JDBC and Data Access/15 - Spring JdbcTemplate]]
---

# Batch Operations in JDBC

## What it is

JDBC's batch API queues multiple INSERT/UPDATE/DELETE statements and sends them in one round-trip, instead of one round-trip per statement. For 1000 inserts, that's 1 round-trip instead of 1000.

## The API

```java
try (PreparedStatement ps = conn.prepareStatement(
        "INSERT INTO intern(name, is_accepted) VALUES (?, ?)")) {
    for (Intern i : interns) {
        ps.setString(1, i.getName());
        ps.setString(2, i.getStatus());
        ps.addBatch();           // queue, don't execute
    }
    int[] affected = ps.executeBatch();   // one round-trip
}
```

`addBatch()` queues the parameters; `executeBatch()` sends them all. The return value is an `int[]` of per-statement affected row counts.

## Chunking

Don't send 100,000 rows in one batch - you'll exhaust memory and undo space. Send in chunks:

```java
int chunkSize = 500;
for (int from = 0; from < interns.size(); from += chunkSize) {
    int to = Math.min(from + chunkSize, interns.size());
    try (PreparedStatement ps = conn.prepareStatement(SQL)) {
        for (Intern i : interns.subList(from, to)) {
            ps.setString(1, i.getName());
            ps.setString(2, i.getStatus());
            ps.addBatch();
        }
        ps.executeBatch();
    }
}
```

Or, with `executeBatch` mid-loop:

```java
int count = 0;
try (PreparedStatement ps = conn.prepareStatement(SQL)) {
    for (Intern i : interns) {
        ps.setString(1, i.getName());
        ps.setString(2, i.getStatus());
        ps.addBatch();
        if (++count % 500 == 0) {
            ps.executeBatch();
            ps.clearBatch();
        }
    }
    ps.executeBatch();   // flush the remainder
}
```

## Auto-commit and batches

Always `setAutoCommit(false)` before a batch. With auto-commit on, each `executeUpdate` (which `addBatch` does NOT call, but the underlying flush does) commits - defeating the batch benefit. More importantly, the whole batch should be one transaction:

```java
conn.setAutoCommit(false);
try (PreparedStatement ps = conn.prepareStatement(SQL)) {
    // ... addBatch loop ...
    ps.executeBatch();
    conn.commit();
} catch (SQLException e) {
    conn.rollback();
    throw e;
}
```

## Spring's `JdbcTemplate.batchUpdate`

Spring wraps the verbose pattern:

```java
jdbc.batchUpdate(INSERT, new BatchPreparedStatementSetter() {
    public void setValues(PreparedStatement ps, int i) throws SQLException {
        Intern in = interns.get(i);
        ps.setString(1, in.getName());
        ps.setString(2, in.getStatus());
    }
    public int getBatchSize() { return interns.size(); }
});
```

Or, with a `List` of parameter arrays:

```java
List<Object[]> batch = interns.stream()
    .map(i -> new Object[]{i.getName(), i.getStatus()})
    .toList();
jdbc.batchUpdate(INSERT, batch);   // Spring handles chunking
```

## Generated keys in batch

Retrieving generated keys from a batch is awkward in raw JDBC - the API exists (`prepareStatement(sql, RETURN_GENERATED_KEYS)` then `getGeneratedKeys` after `executeBatch`) but support varies by driver. Spring's `KeyHolder.getKeyList()` returns one map per row, but only works reliably for some drivers.

If you need keys, consider:

- Pre-fetching sequence values: `SELECT intern_seq.NEXTVAL FROM dual CONNECT BY LEVEL <= ?` to get N IDs in one round-trip, then use them in the batch INSERT.
- A subsequent `SELECT` to fetch the inserted rows by some natural key.

## Why it matters

For bulk loads, batch operations are the difference between "10 minutes" and "10 seconds". The per-statement overhead (parse, network, commit) dominates when each statement is small; batching amortizes it.

## Project Connection

The project inserts interns one at a time, no batching. For the seed data (`insertion.sql`'s sample inserts), this is fine - it's a one-time script. For a bulk-import feature (CSV upload, scheduled sync), it would be a problem.

The redesign's repository would expose:

```java
public void insertAll(List<Intern> interns) {
    jdbc.batchUpdate(INSERT, interns, 500, (ps, in) -> {
        ps.setString(1, in.getName());
        ps.setString(2, in.getStatus());
        ps.setLong(3, in.getDepartmentId());
    });
}
```

(Spring's `batchUpdate(sql, batchArgs, batchSize, parameterizedPreparedStatementSetter)`.)

## Common pitfalls

- Forgetting `setAutoCommit(false)` - each statement in the batch commits, killing the benefit.
- Not chunking - one giant batch exhausts memory and undo space.
- Calling `executeBatch` without `clearBatch` in a chunked loop - the previous chunk's statements accumulate.
- Mixing batch with `getGeneratedKeys` - works for some drivers, fails for others.

## Further reading

- Oracle Docs, "JDBC Developer's Guide", "Batch Updates".
- [[11 - DB Performance and Indexing/03 - Batch Operations]]
