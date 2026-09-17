---
tags: [concept, concurrency, reactive, reactor]
type: concept
status: complete
related:
  - [[18 - Java Concurrency/01 - CompletableFuture]]
---

# Reactive Programming

## What it is

**Reactive programming** is an async, event-driven paradigm where you compose streams of events. Java's main reactive libraries are **Project Reactor** (`Mono<T>`, `Flux<T>`) and **RxJava** (`Observable<T>`, `Flowable<T>`).

## Example (Reactor)

```java
Mono<Intern> internMono = repository.findById(123);
Mono<Theme> themeMono = internMono.flatMap(intern -> themeRepository.findById(intern.getThemeId()));
Mono<InternDetail> detailMono = Mono.zip(internMono, themeMono, (i, t) -> new InternDetail(i, t));

detailMono.subscribe(detail -> {
    Platform.runLater(() -> display(detail));
});
```

## Why

- **Backpressure** — the consumer tells the producer how fast to emit. Prevents overload.
- **Composition** — chain operations (map, filter, flatMap, zip).
- **Non-blocking** — never blocks a thread; I/O is async.
- **Streams** — handle 0, 1, or N elements uniformly.

## When to use

- **High-concurrency I/O** — thousands of concurrent HTTP/DB calls.
- **Event-driven** — UI events, message queues.
- **Streaming** — real-time data feeds.

## When NOT to use

- **Simple CRUD** — `CompletableFuture` is simpler.
- **CPU-bound work** — reactive doesn't add parallelism.
- **Beginners** — reactive has a steep learning curve.

## R2DBC (Reactive Relational Database Connectivity)

R2DBC is the reactive equivalent of JDBC. Non-blocking DB access.

```java
DatabaseClient client = DatabaseClient.create(connectionFactory);
Mono<Intern> intern = client.sql("SELECT * FROM interns WHERE intern_id = :id")
    .bind("id", 123)
    .map((row, meta) -> new Intern(row.get("intern_id", Long.class), ...))
    .one();
```

## Project Connection

For a desktop app with JavaFX, reactive is overkill. The JavaFX `Task` / `Service` API is simpler. Reactive would be useful if the app evolves to a high-throughput server.

## Further reading

- *Reactive Programming with Reactor* (Obriský).
- Project Reactor reference.
