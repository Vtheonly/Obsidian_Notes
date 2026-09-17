---
tags: [concept, cs-foundations, os, threads]
type: concept
status: complete
prerequisites:
  - [[02 - CS Foundations/08 - Memory and Pointers]]
related:
  - [[18 - Java Concurrency/09 - Threads and Runnable]]
  - [[19 - JavaFX Fundamentals/03 - JavaFX Application Thread]]
  - [[10 - Transactions and Concurrency/03 - Connection Is Not Thread-Safe]]
---

# Processes and Threads (OS View)

## What it is

A **process** is an instance of a running program. The OS gives each process its own address space, file descriptors, and security context.

A **thread** is a unit of execution *within* a process. Threads in the same process share the heap, file descriptors, and security context — but each has its own stack and program counter.

## Why it exists

Without threads, a program can do only one thing at a time. If it waits for I/O, the entire program blocks. Threads let a program overlap I/O with computation: while thread 1 waits for the database, thread 2 renders the UI.

The OS scheduler preemptively switches between threads, giving each a slice of CPU time. On multi-core machines, threads genuinely run in parallel.

## Why this matters for the project

JavaFX (like every GUI toolkit) has a **single dedicated thread** for UI work — the *JavaFX Application Thread*. GUI toolkits are not thread-safe by design. Allowing two threads to mutate the scene graph simultaneously would corrupt rendering state. The contract: **only the Application Thread may touch UI nodes**.

When you call `oracleConnector.searchIntern()` from a button's `onAction` handler, that handler runs on the Application Thread. The DB call blocks for hundreds of ms. During that time, the UI cannot repaint, cannot process other clicks, cannot respond to resize. The OS marks the app as "Not Responding."

This is the project's #1 UI/UX bug. The fix: run DB calls on a *different* thread — a background worker — and post the result back to the Application Thread when done. See [[21 - JavaFX Concurrency/06 - Why UI Thread Matters]].

## Thread lifecycle (OS view)

| State | Meaning |
|---|---|
| New | Created but not started. |
| Runnable | Ready to run, waiting for a CPU slice. |
| Running | Currently executing on a CPU. |
| Blocked | Waiting for a resource (I/O, lock, sleep). |
| Terminated | Finished execution. |

Java's `Thread.State` enum: `NEW`, `RUNNABLE`, `BLOCKED`, `WAITING`, `TIMED_WAITING`, `TERMINATED`.

## Why JDBC Connections are not thread-safe

A JDBC `Connection` holds socket state, server-side session state, and transaction state. If two threads use the same connection simultaneously:

- Thread A starts a transaction.
- Thread B autocommits its own update, which silently commits A's transaction.
- Thread A's rollback fails because there's nothing to roll back.

Oracle's driver serializes execution on a single connection (it locks internally), so you don't get *corruption* — you get *mysterious transaction bugs*. Either way, the connection is broken for concurrent use. See [[10 - Transactions and Concurrency/03 - Connection Is Not Thread-Safe]].

The project's `static Connection` shared across the entire app is therefore a concurrency landmine. The fix is a connection pool (HikariCP) that gives each thread its own connection.

## Thread vs process trade-offs

| Property | Threads | Processes |
|---|---|---|
| Creation cost | Cheap (~50 µs) | Expensive (~1 ms) |
| Memory | Shared heap (efficient) | Separate address spaces (heavy) |
| Communication | Direct memory access | IPC (pipes, sockets, shared memory) |
| Isolation | None (one thread can crash all) | Strong (OS-enforced) |
| Failure mode | One thread's bug crashes the process | One process crash doesn't affect others |

## Common pitfalls

- Assuming single-threaded execution. Most "weird" GUI bugs come from code that assumed only one thread would touch state.
- Sharing mutable state without synchronization. Two threads incrementing a counter produce lost updates.
- Blocking the UI thread. Any blocking call (DB, file, network, `Thread.sleep`) on the UI thread freezes the UI.
- Calling UI methods from background threads. JavaFX scene-graph methods throw `IllegalStateException` if called off the Application Thread. Use `Platform.runLater()`.

## Project Connection

- Every `oracleConnector` call from a controller blocks the JavaFX Application Thread. See [[21 - JavaFX Concurrency/06 - Why UI Thread Matters]].
- The single `static Connection` is shared across whatever threads happen to call it. See [[10 - Transactions and Concurrency/03 - Connection Is Not Thread-Safe]].
- The `static String labelText` shared between controllers is a single-threaded race (two clicks faster than the new window's `initialize()` runs).

## Further reading

- *Operating System Concepts* (Silberschatz), Chapters 4–5.
- *Java Concurrency in Practice* (Goetz), Chapter 1.
- JLS §17 (Threads and Locks).
