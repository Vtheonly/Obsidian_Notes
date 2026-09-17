---
tags: [concept, concurrency, race-conditions]
type: concept
status: complete
prerequisites:
  - [[18 - Java Concurrency/05 - Java Memory Model]]
---

# Race Conditions

## What it is

A **race condition** occurs when the correctness of a program depends on the timing of thread execution.

## Example: counter

```java
class Counter {
    private int count = 0;
    public void increment() { count++; }
}
```

`count++` is three operations:
1. Read `count`.
2. Add 1.
3. Write `count`.

If two threads do this simultaneously:
```
Thread A: read count (0)
Thread B: read count (0)
Thread A: add 1 (1)
Thread B: add 1 (1)
Thread A: write count (1)
Thread B: write count (1)
Final count: 1 (should be 2)
```

Lost update.

## The project's race conditions

### 1. `MAX(id)+1`
```java
int newId = oracleConnector.getMaxId("intern", "intern_id") + 1;
oracleConnector.insertIntern(newId, ...);
```
Two concurrent inserts both read MAX=100, both compute 101, both insert → PK violation.

### 2. `static String labelText`
```java
// Click 1
labelText = internA.toString();
// Click 2 (before window opens)
labelText = internB.toString();  // overwrites
// Window 1 opens, reads labelText → sees internB
```

### 3. `static Connection`
Two threads using the same connection → transaction state corrupted.

## Fixes

### Counter
```java
AtomicInteger count = new AtomicInteger(0);
count.incrementAndGet();  // atomic
```

### MAX(id)+1
Use Oracle IDENTITY columns. The DB handles concurrency.

### static labelText
Pass data via controller setters. No shared state.

### static Connection
Use a connection pool. Each thread borrows its own.

## Further reading

- *Java Concurrency in Practice* (Goetz), Chapter 2.
