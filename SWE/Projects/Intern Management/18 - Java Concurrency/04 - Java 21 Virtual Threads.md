---
tags: [concept, concurrency, virtual-threads, loom]
type: concept
status: complete
prerequisites:
  - [[18 - Java Concurrency/03 - ExecutorService]]
---

# Java 21 Virtual Threads

## What it is

**Virtual threads** (Project Loom, JEP 444, Java 21) are lightweight threads managed by the JVM, not the OS. Millions can run on a single JVM.

## Platform vs virtual threads

| | Platform thread | Virtual thread |
|---|---|---|
| Created by | OS | JVM |
| Cost | ~1 MB stack, ~50 µs to create | ~few KB stack, ~1 µs to create |
| Max count | Thousands | Millions |
| Scheduling | OS scheduler | JVM scheduler (ForkJoinPool) |
| Blocking | Blocks the OS thread | "Parks" — doesn't block the OS thread |

## When virtual threads shine

Virtual threads are best for **I/O-bound** work (DB calls, HTTP requests, file I/O). When a virtual thread blocks on I/O, the JVM "parks" it and runs another virtual thread on the same OS thread.

```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 10_000).forEach(i ->
        executor.submit(() -> {
            Thread.sleep(Duration.ofSeconds(1));
            return fetchFromDb(i);
        })
    );
}
// 10,000 concurrent I/O operations, using only a few OS threads.
```

## When virtual threads DON'T help

- **CPU-bound work** — virtual threads don't add parallelism (still limited by CPU cores).
- **Code that uses `synchronized` for a long time** — virtual threads "pin" the OS thread inside `synchronized`. Use `ReentrantLock` instead (Java 21 workaround; fixed in Java 24).

## Project Connection

For the JavaFX app's background DB work, virtual threads are ideal:

```java
private final ExecutorService dbExecutor = Executors.newVirtualThreadPerTaskExecutor();

public void search(String name) {
    dbExecutor.submit(() -> {
        List<Intern> results = repository.findByName(name);  // I/O — virtual thread parks
        Platform.runLater(() -> tableView.getItems().setAll(results));
    });
}
```

You can submit thousands of concurrent searches without exhausting OS threads.

## Further reading

- JEP 444 (Virtual Threads).
- Inside Java — Virtual Threads.
