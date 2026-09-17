---
tags: [concept, javafx, filterlist, sortedlist, search]
type: concept
status: complete
prerequisites:
  - [[22 - JavaFX Advanced Controls/08 - TableView]]
---

# FilteredList and SortedList

## What it is

`FilteredList<T>` and `SortedList<T>` are observable wrappers that filter/sort a source list, live. Combined with `TableView`, they enable live search and column-click sorting.

## Live search

```java
ObservableList<Intern> source = FXCollections.observableArrayList();
FilteredList<Intern> filtered = new FilteredList<>(source, p -> true);  // show all initially

// Bind the filter to a search field
searchField.textProperty().addListener((obs, old, query) -> {
    filtered.setPredicate(intern -> {
        if (query == null || query.isEmpty()) return true;
        String lower = query.toLowerCase();
        return intern.getName().toLowerCase().contains(lower)
            || intern.getEmail().toLowerCase().contains(lower);
    });
});

// Bind to table
tableView.setItems(filtered);
```

As the user types, the table filters live — no search button needed.

## Sorting

```java
SortedList<Intern> sorted = new SortedList<>(filtered);
sorted.comparatorProperty().bind(tableView.comparatorProperty());
tableView.setItems(sorted);
```

Now clicking a column header sorts the (filtered) list.

## Composition

```
source (all interns)
  → filtered (matches search)
    → sorted (by clicked column)
      → tableView
```

All three are observable. Change the source, the filter, or the sort — the table updates.

## Why this matters

- **No re-query** — filtering is in-memory, instant.
- **Live** — the filter updates as you type.
- **Composable** — filter + sort + table binding.

## Project Connection

The project's search does a DB query per keystroke (if it were live) or per button click. With `FilteredList`, load all interns once, filter in-memory. Much faster for reasonable dataset sizes.

For very large datasets (>100,000), use server-side pagination instead.

## Further reading

- JavaFX `FilteredList` and `SortedList` documentation.
