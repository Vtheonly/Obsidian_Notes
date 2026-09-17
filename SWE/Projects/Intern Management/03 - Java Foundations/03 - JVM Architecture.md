---
tags: [concept, java, jvm]
type: concept
status: complete
related:
  - [[03 - Java Foundations/14 - The static Keyword]]
---

# JVM Architecture

## What it is

The Java Virtual Machine is the runtime engine that executes Java bytecode. It has three main subsystems:

1. **Class Loader Subsystem** — loads `.class` files into memory (loading, linking, initialization).
2. **Runtime Data Areas** — method area, heap, JVM stacks, PC registers, native method stacks.
3. **Execution Engine** — interpreter + JIT compiler (HotSpot) + garbage collector.

## Runtime data areas

| Area | Per-thread? | Stores |
|---|---|---|
| Method area (Metaspace in Java 8+) | Shared | Class metadata, static fields, method bytecode |
| Heap | Shared | All objects, arrays |
| JVM stack | Per-thread | Method frames (local vars, return address) |
| PC register | Per-thread | Address of current instruction |
| Native method stack | Per-thread | Frames for native (JNI) calls |

## Why this matters

- **`static` fields live in the method area** — one copy per class, shared across all instances and threads. This is why `static String labelText` is a single shared slot.
- **Objects live on the heap** — garbage collected when no references remain.
- **Local variables live on the stack** — thread-local, automatically freed on method return.
- **The JIT compiler** optimizes hot code — methods called frequently get compiled to native code. This is why micro-benchmarks need warmup.

## Common pitfalls

- Assuming `static` means "constant" — it means "one per class," not "immutable."
- Assuming objects on the heap are thread-safe — they're shared, so they require synchronization.
- Forgetting that the method area is shared — `static` mutable state is a concurrency hazard.

## Project Connection

- `oracleConnector.connection` is a `static` field in the method area. Every thread that calls any `oracleConnector` method uses the same `Connection` object (which lives on the heap). See [[10 - Transactions and Concurrency/03 - Connection Is Not Thread-Safe]].
- `toolkit.RANDOM` is `static final SecureRandom` — `SecureRandom` is thread-safe, so this is fine.
- `insertionInternController.labelText` is `static String` — shared mutable state. Race condition.

## Further reading

- *Java Performance* (Scott Oaks).
- JLS §12 (Execution).
- JVM Specification.
