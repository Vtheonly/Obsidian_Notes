---
tags: [concept, javafx, cancellation, tasks]
type: concept
status: complete
prerequisites:
  - [[21 - JavaFX Concurrency/04 - Task (javafx.concurrent)]]
---

# Cancelling Tasks

## Cooperative cancellation

Java thread cancellation is **cooperative** — you call `task.cancel()`, but the task must check `isCancelled()` and stop.

```java
Task<Void> task = new Task<>() {
    @Override
    protected Void call() throws Exception {
        for (int i = 0; i < items.size(); i++) {
            if (isCancelled()) break;  // check
            process(items.get(i));
            updateProgress(i, items.size());
        }
        return null;
    }
};
```

## Why cooperative

Java threads can be forcibly stopped (`Thread.stop()`), but it's **deprecated** — it can leave the app in an inconsistent state (locks held, objects half-updated). Cooperative cancellation is safe.

## Interrupting blocking calls

If the task is blocked on `Thread.sleep`, `wait`, or I/O, calling `task.cancel()` interrupts the thread, which throws `InterruptedException`:

```java
Task<Void> task = new Task<>() {
    @Override
    protected Void call() throws Exception {
        try {
            Thread.sleep(10000);  // cancel here throws InterruptedException
        } catch (InterruptedException e) {
            if (isCancelled()) {
                System.out.println("Cancelled");
                return null;
            }
            throw e;
        }
        return null;
    }
};
```

## JDBC cancellation

JDBC `Statement.cancel()` can cancel a running query:
```java
Task<List<Intern>> task = new Task<>() {
    private Statement stmt;
    @Override
    protected List<Intern> call() throws Exception {
        try (Connection conn = dataSource.getConnection()) {
            stmt = conn.createStatement();
            // check isCancelled() periodically
            ResultSet rs = stmt.executeQuery(sql);
            // ...
        }
    }

    @Override
    protected void cancelled() {
        try { if (stmt != null) stmt.cancel(); } catch (SQLException ignored) {}
    }
};
```

## UI for cancellation

```java
Button cancelButton = new Button("Cancel");
cancelButton.setOnAction(e -> task.cancel());
cancelButton.disableProperty().bind(task.stateProperty().isNotEqualTo(RUNNING));
```

## Project Connection

The project has no cancellation (no background work). The fix: long-running operations (bulk import, search) should be cancellable.

## Further reading

- JavaFX `Task` cancellation documentation.
- *Java Concurrency in Practice* (Goetz), Chapter 7.
