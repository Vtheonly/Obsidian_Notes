---
tags: [concept, concurrency, threads, java]
type: concept
status: complete
prerequisites:
  - [[02 - CS Foundations/10 - Processes and Threads (OS view)]]
---

# Threads and Runnable

## Creating a thread

```java
// Option 1: extend Thread
class MyThread extends Thread {
    public void run() { System.out.println("Hello"); }
}
new MyThread().start();

// Option 2: implement Runnable (preferred)
Runnable task = () -> System.out.println("Hello");
new Thread(task).start();

// Option 3: with a name
new Thread(task, "worker-1").start();
```

## Thread lifecycle

- `NEW` — created, not started.
- `RUNNABLE` — started, eligible to run.
- `BLOCKED` — waiting for a monitor lock.
- `WAITING` — waiting indefinitely (`Object.wait()`, `Thread.join()`).
- `TIMED_WAITING` — waiting for a duration (`Thread.sleep(ms)`).
- `TERMINATED` — finished.

## Daemon threads

```java
Thread t = new Thread(task);
t.setDaemon(true);  // JVM exits even if t is running
t.start();
```

Daemon threads are background workers — the JVM doesn't wait for them on exit. Use for non-critical tasks (logging, monitoring).

## Why not to use `new Thread()` directly

- **No pool** — unbounded thread creation exhausts resources.
- **No reuse** — each thread is created and destroyed (expensive).
- **No queueing** — no way to limit concurrency.

Use `ExecutorService` instead. See [[18 - Java Concurrency/03 - ExecutorService]].

## Project Connection

The project creates no threads explicitly — everything runs on the JavaFX Application Thread. The fix: use `ExecutorService` for background DB work.

## Further reading

- *Java Concurrency in Practice* (Goetz), Chapter 1.
