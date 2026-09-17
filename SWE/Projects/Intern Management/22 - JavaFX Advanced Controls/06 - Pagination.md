---
tags: [concept, javafx, pagination, controls]
type: concept
status: complete
related:
  - [[11 - DB Performance and Indexing/19 - Pagination]]
---

# Pagination Control

## What it is

`Pagination` is a JavaFX control that splits content into pages with navigation buttons.

## Usage

```java
Pagination pagination = new Pagination(totalPages, 0);
pagination.setPageFactory(pageIndex -> {
    List<Intern> page = repository.findPage(pageIndex, PAGE_SIZE);
    TableView<Intern> table = buildTable(page);
    return table;
});
```

The `setPageFactory` returns the node for each page. The user clicks "Next" / "Previous" / page numbers; the factory is called.

## When to use

- **Very large datasets** (> 10,000 rows) where loading all into memory is wasteful.
- **Server-side pagination** — each page is a separate DB query.

For smaller datasets, `TableView` with virtualization handles everything without pagination.

## Project Connection

For the intern app (likely < 10,000 interns), `TableView` with virtualization is sufficient — no pagination needed. If the dataset grows, add `Pagination` with keyset queries.

## Further reading

- JavaFX `Pagination` documentation.
