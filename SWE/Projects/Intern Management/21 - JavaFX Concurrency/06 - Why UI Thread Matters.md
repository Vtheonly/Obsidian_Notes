---
tags: [concept, javafx, concurrency, ui-thread]
type: concept
status: complete
prerequisites:
  - [[19 - JavaFX Fundamentals/03 - JavaFX Application Thread]]
related:
  - [[18 - Java Concurrency/03 - ExecutorService]]
---

# Why the UI Thread Matters

## The 16 ms rule

JavaFX aims for 60 FPS — one frame every ~16 ms. If the Application Thread takes longer than 16 ms on any pulse, the UI drops frames.

If it takes longer than ~250 ms, the OS marks the app as "Not Responding."

## What blocks the UI thread

- **JDBC calls** — 10 ms to 10 seconds depending on query and network.
- **File I/O** — disk reads.
- **Network calls** — HTTP, SMTP.
- **Heavy computation** — sorting 1M items, rendering PDFs.
- **`Thread.sleep()`** — obviously.

## The project's blocking

Every `oracleConnector` call from a controller blocks the UI thread:
- Login — 4 queries × ~50 ms = 200 ms. UI freezes.
- Search — 1 query + N follow-up queries. For 100 results, ~1 sec.
- Insert — ~100 ms.
- Update — ~100 ms.
- Delete — ~100 ms.
- PDF generation — ~1-5 sec.

The UI is non-responsive during each.

## The 250 ms budget

A good rule: **anything that might take > 250 ms should run on a background thread.**

In practice, **any** I/O should be background — you don't know if it'll be fast.

## The fix

Wrap every DB / file / network call in a `Task`:

```java
@FXML
public void handleSearch() {
    Task<List<Intern>> task = new Task<>() {
        @Override
        protected List<Intern> call() throws Exception {
            return repository.findByName(searchField.getText());
        }
    };

    task.setOnSucceeded(e -> tableView.getItems().setAll(task.getValue()));
    task.setOnFailed(e -> showError(task.getException()));

    loadingIndicator.setVisible(true);
    new Thread(task).start();
}
```

The DB call runs on a background thread. The UI stays responsive. The result updates the UI on the Application Thread (via `setOnSucceeded`).

## Further reading

- JavaFX Concurrency tutorial.
