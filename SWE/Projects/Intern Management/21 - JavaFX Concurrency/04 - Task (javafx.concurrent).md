---
tags: [concept, javafx, task, concurrency]
type: concept
status: complete
prerequisites:
  - [[21 - JavaFX Concurrency/06 - Why UI Thread Matters]]
  - [[18 - Java Concurrency/03 - ExecutorService]]
---

# Task (javafx.concurrent)

## What it is

`javafx.concurrent.Task<T>` is a JavaFX-aware `FutureTask`. It runs background work and safely updates the UI on completion.

## Basic usage

```java
Task<List<Intern>> task = new Task<>() {
    @Override
    protected List<Intern> call() throws Exception {
        // Runs on a background thread.
        // Do NOT touch the UI here.
        return repository.findByName(name);
    }
};

task.setOnScheduled(e -> loadingIndicator.setVisible(true));
task.setOnSucceeded(e -> {
    loadingIndicator.setVisible(false);
    tableView.getItems().setAll(task.getValue());
});
task.setOnFailed(e -> {
    loadingIndicator.setVisible(false);
    showError(task.getException());
});

Thread thread = new Thread(task);
thread.setDaemon(true);
thread.start();
```

## Why Task (not raw Thread)

- **Thread-safe UI updates** — `setOnSucceeded`, `setOnFailed` run on the Application Thread.
- **Lifecycle callbacks** — Scheduled, Running, Succeeded, Failed, Cancelled.
- **Progress** — `updateProgress(workDone, max)`, `updateMessage(msg)` (for status display).
- **Cancellation** — `task.cancel()` cooperatively cancels; check `isCancelled()` in `call()`.

## Progress

```java
Task<Void> importTask = new Task<>() {
    @Override
    protected Void call() throws Exception {
        List<Intern> interns = parseCsv(file);
        for (int i = 0; i < interns.size(); i++) {
            if (isCancelled()) break;
            repository.save(interns.get(i));
            updateProgress(i + 1, interns.size());
            updateMessage("Imported " + (i + 1) + " of " + interns.size());
        }
        return null;
    }
};

progressBar.progressProperty().bind(importTask.progressProperty());
statusLabel.textProperty().bind(importTask.messageProperty());
```

## Partial results

```java
Task<ObservableList<Intern>> task = new Task<>() {
    @Override
    protected ObservableList<Intern> call() throws Exception {
        ObservableList<Intern> results = FXCollections.observableArrayList();
        try (ResultSet rs = ...) {
            while (rs.next()) {
                if (isCancelled()) break;
                Intern intern = mapRow(rs);
                Platform.runLater(() -> results.add(intern));  // partial update
            }
        }
        return results;
    }
};
```

Use `Platform.runLater` for partial UI updates (or `updateValue` in JavaFX 8+).

## Common pitfalls

- **Touching the UI in `call()`** — throws `IllegalStateException`. Use `setOnSucceeded`.
- **Not setting `setDaemon(true)`** — the thread keeps the JVM alive on exit.
- **Catching exceptions in `call()`** — let them propagate; `setOnFailed` handles them.
- **Creating a new `Thread` per task** — use an `ExecutorService` for reuse.

## Project Connection

The project has zero `Task` usage — all DB work is on the UI thread. The fix: every DB call wrapped in a `Task`.

## Further reading

- JavaFX `Task` documentation.
