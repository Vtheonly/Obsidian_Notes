---
tags: [concept, javafx, platform-runlater, patterns]
type: concept
status: complete
prerequisites:
  - [[19 - JavaFX Fundamentals/06 - Platform.runLater]]
  - [[21 - JavaFX Concurrency/04 - Task (javafx.concurrent)]]
---

# Platform.runLater Patterns

## When to use

Use `Platform.runLater()` when you need to update the UI from a background thread, and you're not using `Task` (which handles this for you).

## Pattern 1: Single update after background work

```java
new Thread(() -> {
    List<Intern> results = repository.findByName(name);
    Platform.runLater(() -> tableView.getItems().setAll(results));
}).start();
```

## Pattern 2: Partial updates during background work

```java
new Thread(() -> {
    try (ResultSet rs = ...) {
        while (rs.next()) {
            Intern intern = mapRow(rs);
            Platform.runLater(() -> tableView.getItems().add(intern));
        }
    }
}).start();
```

⚠️ For high-frequency updates, throttle (don't call `runLater` per row — batch).

## Pattern 3: Error handling

```java
new Thread(() -> {
    try {
        List<Intern> results = repository.findByName(name);
        Platform.runLater(() -> tableView.getItems().setAll(results));
    } catch (SQLException e) {
        Platform.runLater(() -> showError(e));
    }
}).start();
```

## Pattern 4: Final cleanup

```java
new Thread(() -> {
    try {
        // work
        Platform.runLater(() -> {
            loadingIndicator.setVisible(false);
            tableView.getItems().setAll(results);
        });
    } catch (Exception e) {
        Platform.runLater(() -> {
            loadingIndicator.setVisible(false);
            showError(e);
        });
    }
}).start();
```

Always hide the loading indicator in both success and failure.

## When NOT to use Platform.runLater

- **Inside a `Task`** — use `updateValue`, `updateProgress`, `updateMessage` instead. They throttle automatically.
- **On the Application Thread** — just call the code directly.
- **For high-frequency updates** — throttle manually:
```java
private long lastUpdate = 0;
void onUpdate(Intern intern) {
    long now = System.currentTimeMillis();
    if (now - lastUpdate < 100) return;
    lastUpdate = now;
    Platform.runLater(() -> tableView.getItems().add(intern));
}
```

## Project Connection

The project never uses `Platform.runLater` (no background threads). The fix uses it (or `Task` callbacks, which handle it internally).

## Further reading

- JavaFX `Platform` documentation.
