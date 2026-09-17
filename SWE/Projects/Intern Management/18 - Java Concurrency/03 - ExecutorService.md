---
tags: [concept, concurrency, executor-service, thread-pool]
type: concept
status: complete
related:
  - [[21 - JavaFX Concurrency/06 - Why UI Thread Matters]]
---

# ExecutorService

## What it is

`ExecutorService` is a thread pool — it manages a queue of tasks and a pool of worker threads. You submit tasks; the pool executes them.

## Why

- **Reuse threads** — no create/destroy overhead per task.
- **Limit concurrency** — too many threads exhaust resources.
- **Queue tasks** — submit faster than execute; queue holds the overflow.
- **Shutdown** — orderly shutdown of the pool.

## Common pools

```java
// Fixed pool — N threads
ExecutorService pool = Executors.newFixedThreadPool(4);

// Cached pool — grows as needed, reuses idle threads
ExecutorService pool = Executors.newCachedThreadPool();

// Single-threaded — tasks execute in order
ExecutorService pool = Executors.newSingleThreadExecutor();

// Scheduled — delayed or periodic tasks
ScheduledExecutorService pool = Executors.newScheduledThreadPool(2);
pool.scheduleAtFixedRate(task, 0, 1, TimeUnit.MINUTES);
```

## Submitting tasks

```java
// Runnable (no return)
pool.submit(() -> { System.out.println("Hello"); });

// Callable (returns a value)
Future<Integer> future = pool.submit(() -> {
    return 42;
});
Integer result = future.get();  // blocks until done

// CompletableFuture (async composition)
CompletableFuture<Integer> cf = CompletableFuture.supplyAsync(() -> 42, pool);
```

## Shutdown

```java
pool.shutdown();        // no new tasks; finish existing
pool.awaitTermination(60, TimeUnit.SECONDS);  // wait
// or
pool.shutdownNow();     // attempt to interrupt running tasks
```

Always shut down. An unshutdown pool keeps the JVM alive (unless daemon threads).

## Project Connection

The project runs all DB work on the JavaFX Application Thread. The fix:
```java
private final ExecutorService dbExecutor = Executors.newFixedThreadPool(4);

public void search(String name) {
    dbExecutor.submit(() -> {
        List<Intern> results = repository.findByName(name);
        Platform.runLater(() -> tableView.getItems().setAll(results));
    });
}
```

The DB call runs on a worker thread. The UI update marshals back to the JavaFX Application Thread via `Platform.runLater`.

## Java 21 virtual threads

```java
ExecutorService vtPool = Executors.newVirtualThreadPerTaskExecutor();
```

Virtual threads are cheap — you can have millions. Use for I/O-bound work (DB, HTTP). See [[18 - Java Concurrency/04 - Java 21 Virtual Threads]].

## Further reading

- *Java Concurrency in Practice* (Goetz), Chapter 6.
