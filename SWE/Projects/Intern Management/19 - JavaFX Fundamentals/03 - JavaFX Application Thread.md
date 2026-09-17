---
tags: [concept, javafx, thread, application-thread]
type: concept
status: complete
prerequisites:
  - [[02 - CS Foundations/10 - Processes and Threads (OS view)]]
related:
  - [[21 - JavaFX Concurrency/06 - Why UI Thread Matters]]
  - [[18 - Java Concurrency/05 - Java Memory Model]]
---

# JavaFX Application Thread

## The rule

> **Only the JavaFX Application Thread may modify the scene graph.**

JavaFX, like every GUI toolkit, is single-threaded for UI work. The scene graph (all UI nodes) is not thread-safe. Allowing concurrent modification would corrupt rendering state.

## Why single-threaded?

Thread-safe UI toolkits are extremely hard to build (every method would need locks; deadlock risk; performance overhead). Single-threaded is simpler and fast enough — the UI thread does only quick work (rendering, event handling); heavy work goes to background threads.

## The pulse mechanism

The JavaFX runtime runs a "pulse" ~60 times per second. Each pulse:
1. Processes events (mouse, keyboard).
2. Runs animations.
3. Lays out the scene graph.
4. Renders to the screen.

If the Application Thread is blocked (e.g., on a DB call), pulses don't run — the UI freezes.

## What runs on the Application Thread

- `Application.start()`.
- Event handlers (`onAction`, `setOnMouseClicked`).
- `initialize()` of controllers.
- Animations.
- `Platform.runLater()` callbacks.

## What should NOT run on the Application Thread

- DB calls (use `Task` / `Service`).
- Network calls.
- File I/O.
- Long computations.
- `Thread.sleep()`.

## `Platform.runLater()`

To update the UI from a background thread:
```java
new Thread(() -> {
    List<Intern> results = repository.findByName(name);  // background thread
    Platform.runLater(() -> {                            // marshal to UI thread
        tableView.getItems().setAll(results);
    });
}).start();
```

`Platform.runLater(Runnable)` schedules the `Runnable` to run on the Application Thread.

## The "Not Responding" problem

If the Application Thread blocks for > 250 ms, the OS marks the app as "Not Responding":
- Windows: title bar shows "(Not Responding)".
- macOS: rainbow beachball.
- Linux: grayed-out window.

The user assumes the app crashed.

## Project Connection

**Every** `oracleConnector` call from a controller runs on the Application Thread. Search, insert, update, delete — all block the UI. The fix: wrap every DB call in a `Task` and run it on a background thread. See [[21 - JavaFX Concurrency/00 - MOC - JavaFX Concurrency]].

## Further reading

- JavaFX Concurrency documentation.
