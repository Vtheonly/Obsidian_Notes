---
tags: [concept, resilience, bulkhead]
type: concept
status: complete
---

# Bulkhead Pattern

## What it is

A **bulkhead** limits concurrent calls to a service. If the service is slow, only N calls are in flight; the rest fail fast (or queue).

## Why

- **Isolation** — one slow service doesn't consume all threads.
- **Resource protection** — the DB pool isn't exhausted by one slow query type.
- **Cascade prevention** — a failure in one part doesn't bring down everything.

## Analogy

Ship bulkheads — compartments that can flood without sinking the ship. If one compartment floods, the others stay dry.

## Implementation (Resilience4j)

```java
BulkheadConfig config = BulkheadConfig.custom()
    .maxConcurrentCalls(10)              // max 10 concurrent
    .maxWaitDuration(Duration.ofMillis(100))
    .build();
Bulkhead bulkhead = Bulkhead.of("db", config);

T result = bulkhead.executeSupplier(() -> repository.findById(id));
```

If 10 calls are in flight, the 11th waits 100 ms, then fails.

## Semaphore vs Thread Pool

- **Semaphore bulkhead** (Resilience4j default) — limits concurrent calls on any thread.
- **Thread pool bulkhead** — dedicates a thread pool to each service. Stronger isolation.

## Project Connection

Without a bulkhead, a slow DB query consumes a connection from the pool indefinitely. With `maxConcurrentCalls=10`, only 10 queries run at once; the 11th fails fast.

## Further reading

- *Release It!* (Nygard).
- Resilience4j Bulkhead documentation.
