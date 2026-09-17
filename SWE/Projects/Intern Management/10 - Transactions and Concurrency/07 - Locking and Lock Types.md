---
tags: [concept, database, transactions, locking]
type: concept
status: complete
prerequisites:
  - [[10 - Transactions and Concurrency/01 - ACID Properties]]
related:
  - [[10 - Transactions and Concurrency/04 - Deadlocks]]
  - [[10 - Transactions and Concurrency/10 - Optimistic vs Pessimistic Concurrency]]
---

# Locking and Lock Types

## What it is

A **lock** is the database's mechanism for serializing access to a resource. Oracle's lock model:

- **Row-level (TX) locks** - acquired when an `INSERT`, `UPDATE`, `DELETE`, or `SELECT ... FOR UPDATE` modifies a row. One row, one lock - other rows in the same block are unaffected.
- **Table-level (TM) locks** - acquired on the table containing the locked rows, to prevent DDL that would invalidate the lock (e.g., `DROP TABLE` while a transaction is updating it).

Lock **modes** (Oracle's TM modes):

| Mode | Abbrev | Meaning |
|---|---|---|
| Row Share | RS | Intent to lock rows; others can do anything except `LOCK TABLE ... IN EXCLUSIVE MODE` |
| Row Exclusive | RX | Has locked rows; others can read but not exclusive-lock |
| Share | S | Allows other Share locks; no writes |
| Share Row Exclusive | SRX | One writer + readers |
| Exclusive | X | Only the holder can read/write; everyone else waits |

## `SELECT ... FOR UPDATE`

The pessimistic-locking primitive:

```sql
SELECT intern_id, name FROM intern
WHERE intern_id = 42
FOR UPDATE;          -- locks the row, waits if another tx holds the lock

-- or, fail fast instead of wait:
SELECT ... FOR UPDATE NOWAIT;       -- ORA-00054 if locked
SELECT ... FOR UPDATE WAIT 5;       -- wait up to 5 seconds
SELECT ... FOR UPDATE SKIP LOCKED;  -- skip locked rows (used in queue patterns)
```

`FOR UPDATE` is the right tool when you read a row, do some work in the application, and then update the row - it prevents another transaction from changing it in between.

## Locks vs latches vs mutexes

- **Locks** (enqueues) - user-visible, held for the duration of a transaction, can be detected and reported via `V$LOCK`.
- **Latches** - internal, short-lived, protect shared memory structures (e.g., the buffer cache hash table). Held for microseconds.
- **Mutexes** - similar to latches but lighter; replaced many latches in 10g+.

You rarely deal with latches and mutexes directly; they show up as "latch free" wait events in `V$SESSION_WAIT`.

## Detecting lock waits

```sql
SELECT s.sid, s.serial#, s.username, s.status,
       l.type, l.lmode, l.request, o.object_name
FROM   v$session  s
JOIN   v$lock     l ON s.sid = l.sid
LEFT   JOIN dba_objects o ON l.id1 = o.object_id
WHERE  s.type = 'USER' AND l.type = 'TM';
```

To kill a blocking session:

```sql
ALTER SYSTEM KILL SESSION 'sid,serial#' IMMEDIATE;
```

## Why it matters

Locks are the substrate of isolation. Without them, two transactions updating the same row would corrupt each other's writes (the "lost update" anomaly). With them, writes serialize - but if you lock too much, throughput collapses. The art is locking the minimum necessary.

## Project Connection

The project doesn't use `FOR UPDATE` at all. Updates look like:

```java
// search by name, display in UI, user edits, then:
String sql = "UPDATE "intern" SET is_accepted=? WHERE intern_id=?";
```

Between the search and the update (which can be minutes - the user is editing in a JavaFX form), another user could update the same intern. The second update wins; the first user's changes are lost. This is a classic **lost update** anomaly. The fix is either:

- Pessimistic: `SELECT ... FOR UPDATE` when loading the form.
- Optimistic: a `version` column checked in the `UPDATE`'s `WHERE` clause. See [[10 - Transactions and Concurrency/10 - Optimistic vs Pessimistic Concurrency]].

## Common pitfalls

- Locking too much - `LOCK TABLE ... IN EXCLUSIVE MODE` for what should be a row lock.
- Holding locks across user input - locks held for minutes will kill throughput.
- Forgetting that `SELECT` (without `FOR UPDATE`) takes **no locks** in Oracle (MVCC), so a "check then update" without `FOR UPDATE` is a race.
- Locking in a different order in two transactions - that's how you get deadlocks. See [[10 - Transactions and Concurrency/04 - Deadlocks]].

## Further reading

- Oracle Docs, "How Oracle Database Locks Data".
- [[10 - Transactions and Concurrency/04 - Deadlocks]]
