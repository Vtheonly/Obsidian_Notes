---
tags: [concept, concurrency, completablefuture, async]
type: concept
status: complete
prerequisites:
  - [[18 - Java Concurrency/03 - ExecutorService]]
---

# CompletableFuture

## What it is

`CompletableFuture<T>` is Java's promise/future — an async computation that produces a `T`.

## Basic usage

```java
CompletableFuture<Intern> future = CompletableFuture.supplyAsync(() -> {
    return repository.findById(123);  // runs on ForkJoinPool
}, dbExecutor);

future.thenAccept(intern -> {
    Platform.runLater(() -> display(intern));  // runs on dbExecutor, marshal to FX thread
});

future.exceptionally(ex -> {
    log.error("Failed", ex);
    return null;
});
```

## Composition

```java
CompletableFuture<Intern> internFuture = CompletableFuture.supplyAsync(() -> repo.findById(123), dbExecutor);
CompletableFuture<Theme> themeFuture = internFuture.thenCompose(intern ->
    CompletableFuture.supplyAsync(() -> themeRepo.findById(intern.getThemeId()), dbExecutor)
);
CompletableFuture<String> nameFuture = themeFuture.thenApply(Theme::getName);

nameFuture.thenAccept(name -> Platform.runLater(() -> label.setText(name)));
```

Like a monad — chain async operations without nested callbacks.

## Combining

```java
CompletableFuture<Intern> internF = ...;
CompletableFuture<List<Assignment>> assignmentsF = ...;

CompletableFuture.allOf(internF, assignmentsF)
    .thenRun(() -> {
        Intern intern = internF.join();
        List<Assignment> assignments = assignmentsF.join();
        // both done
    });
```

## Error handling

```java
future
    .exceptionally(ex -> {
        log.error("Failed", ex);
        return defaultValue;
    })
    .thenAccept(value -> display(value));
```

## Why over raw `Future`

- `Future.get()` blocks. `CompletableFuture` lets you register callbacks.
- Composition — chain async operations.
- Error handling — `exceptionally`, `handle`.

## Project Connection

For background DB work in JavaFX, `Task` (JavaFX-specific) is often simpler than `CompletableFuture`. But `CompletableFuture` is useful for composing multiple async operations (e.g., fetch intern, then fetch theme, then fetch assignments).

## Further reading

- *Modern Java in Action* (Urma, Fusco, Mycroft), Chapter 15.
