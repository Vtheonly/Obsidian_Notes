---
tags: [concept, concurrency, structured]
type: concept
status: complete
prerequisites:
  - [[18 - Java Concurrency/01 - CompletableFuture]]
  - [[18 - Java Concurrency/04 - Java 21 Virtual Threads]]
---

# Structured Concurrency (JEP 453, Java 21 preview)

## What it is

**Structured concurrency** treats concurrent tasks as a single unit — if any fails, all are cancelled. Like structured programming (if/else, for) but for concurrency.

## The problem without it

```java
Future<Intern> internF = executor.submit(() -> fetchIntern());
Future<Theme> themeF = executor.submit(() -> fetchTheme());
Future<List<Assignment>> assignmentsF = executor.submit(() -> fetchAssignments());

Intern intern = internF.get();  // blocks
Theme theme = themeF.get();     // blocks
List<Assignment> assignments = assignmentsF.get();  // blocks
```

If `fetchTheme` fails, `fetchIntern` and `fetchAssignments` keep running — wasted work, leaked resources.

## With structured concurrency (Java 21 preview)

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Subtask<Intern> internT = scope.fork(() -> fetchIntern());
    Subtask<Theme> themeT = scope.fork(() -> fetchTheme());
    Subtask<List<Assignment>> assignmentsT = scope.fork(() -> fetchAssignments());

    scope.join();              // wait for all
    scope.throwIfFailed();     // throw if any failed

    Intern intern = internT.get();
    Theme theme = themeT.get();
    List<Assignment> assignments = assignmentsT.get();
    // all succeeded
}
```

If any subtask fails, the others are cancelled automatically. The scope's `close()` ensures all subtasks are done before continuing.

## Why it matters

- **No leaks** — all subtasks complete before the scope exits.
- **Error propagation** — failures cancel siblings.
- **Readability** — concurrent code reads like sequential code.

## Project Connection

For fetching an intern with their theme and assignments, structured concurrency is cleaner than chained `CompletableFuture`:

```java
InternDetail detail = fetchInternDetail(internId);
// fetchInternDetail uses structured concurrency to fetch all three in parallel
```

## Status

Structured concurrency is a **preview feature** in Java 21. Stabilized in later versions. Check your Java version.

## Further reading

- JEP 453 (Structured Concurrency).
