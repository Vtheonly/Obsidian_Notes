---
tags: [concept, javafx, service, concurrency]
type: concept
status: complete
prerequisites:
  - [[21 - JavaFX Concurrency/04 - Task (javafx.concurrent)]]
---

# Service (javafx.concurrent)

## What it is

`javafx.concurrent.Service<T>` is a reusable `Task` factory. A `Task` is one-shot; a `Service` can be started, cancelled, and restarted.

## Why Service

- **Reusable** — `service.restart()` cancels the current run and starts a new one.
- **State tracking** — `service.stateProperty()` (READY, SCHEDULED, RUNNING, SUCCEEDED, FAILED, CANCELLED).
- **Bind to UI** — bind a loading indicator to `service.runningProperty()`.

## Usage

```java
public class InternSearchService extends Service<List<Intern>> {
    private final InternRepository repository;
    private String nameFilter;

    public InternSearchService(InternRepository repository) {
        this.repository = repository;
    }

    public void setNameFilter(String name) {
        this.nameFilter = name;
    }

    @Override
    protected Task<List<Intern>> createTask() {
        return new Task<>() {
            @Override
            protected List<Intern> call() throws Exception {
                return repository.findByName(nameFilter);
            }
        };
    }
}

// Usage:
InternSearchService service = new InternSearchService(repository);
service.setOnSucceeded(e -> tableView.getItems().setAll(service.getValue()));
service.setOnFailed(e -> showError(service.getException()));

// In the search button handler:
service.setNameFilter(searchField.getText());
service.restart();
```

## Reset vs Restart

- `reset()` — back to READY (clears last result).
- `restart()` — cancel + reset + start.

## When to use Service vs Task

- **Task** — one-shot background work (load this intern, save this form).
- **Service** — reusable, restartable work (search with different filters, periodic refresh).

## Project Connection

The fix uses `Service` for search (reusable with different filters) and `Task` for one-shot operations (insert, update, delete).

## Further reading

- JavaFX `Service` documentation.
