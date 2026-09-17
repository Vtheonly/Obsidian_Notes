---
tags: [concept, javafx, platform-runlater]
type: concept
status: complete
prerequisites:
  - [[19 - JavaFX Fundamentals/03 - JavaFX Application Thread]]
  - [[18 - Java Concurrency/05 - Java Memory Model]]
related:
  - [[21 - JavaFX Concurrency/06 - Why UI Thread Matters]]
---

# Platform.runLater

## What it is

`Platform.runLater(Runnable)` schedules a `Runnable` to run on the JavaFX Application Thread. Use it to update the UI from a background thread.

## Why

Only the Application Thread may touch the scene graph. If a background thread tries to update a `Label` or `TableView`, it throws `IllegalStateException: Not on FX application thread`.

## Usage

```java
new Thread(() -> {
    List<Intern> results = repository.findByName(name);  // background

    Platform.runLater(() -> {
        tableView.getItems().setAll(results);  // UI thread
        loadingIndicator.setVisible(false);
    });
}).start();
```

## When NOT to use

- **From the Application Thread itself** — unnecessary overhead. Just call the code directly.
- **For high-frequency updates** — `runLater` coalesces; many calls may be batched. For high-frequency updates, use `Task`'s `updateValue` / `updateProgress` (which throttle).

## Throttling

If you call `runLater` from a tight loop, the Application Thread can be overwhelmed. Throttle:

```java
private long lastUpdate = 0;
void onUpdate(Intern intern) {
    long now = System.currentTimeMillis();
    if (now - lastUpdate < 100) return;  // throttle to 10/sec
    lastUpdate = now;
    Platform.runLater(() -> tableView.getItems().add(intern));
}
```

## Alternatives

- `Task.updateValue(V)` — for JavaFX `Task`, throttled automatically.
- `Service` — reusable `Task`.
- `AnimationTimer` — for 60 FPS updates.

## Project Connection

The project doesn't use `Platform.runLater` (it's single-threaded). The fix uses it (or `Task`/`Service`) for all background-to-UI updates.

## Further reading

- JavaFX `Platform` documentation.
