---
tags: [concept, database, performance, pagination]
type: concept
status: complete
related:
  - [[11 - DB Performance and Indexing/11 - EXPLAIN Plan]]
---

# Pagination

## What it is

**Pagination** returns query results in chunks (pages) instead of all at once. Essential for large result sets.

## OFFSET/FETCH (Oracle 12c+, standard SQL)

```sql
SELECT * FROM interns
ORDER BY intern_id
OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;
-- Skips 20 rows, returns 10. Page 3 (with 10 per page).
```

## ROWNUM (older Oracle)

```sql
SELECT * FROM (
    SELECT i.*, ROWNUM rn FROM interns i WHERE ROWNUM <= 30 ORDER BY intern_id
) WHERE rn > 20;
```

## Keyset (cursor) pagination

OFFSET is slow for large offsets — the DB scans and discards rows. Keyset pagination is faster:

```sql
-- First page
SELECT * FROM interns ORDER BY intern_id FETCH FIRST 10 ROWS ONLY;
-- Returns intern_ids 1-10.

-- Next page (use the last seen ID)
SELECT * FROM interns WHERE intern_id > 10 ORDER BY intern_id FETCH FIRST 10 ROWS ONLY;
-- Returns 11-20.
```

The DB uses the index to find `intern_id > 10` — O(log n) instead of O(n) for OFFSET.

## When to use which

- **OFFSET/FETCH** — simple, good for small offsets (< 1000).
- **Keyset** — fast for any offset, but requires an ordered unique column. Doesn't support "jump to page 50."

## UI pagination

JavaFX `Pagination` control:
```java
Pagination pagination = new Pagination(totalPages, 0);
pagination.setPageFactory(pageIndex -> {
    List<Intern> page = internService.findPage(pageIndex, 10);
    TableView<Intern> table = buildTable(page);
    return table;
});
```

## Project Connection

The project loads all search results into a VBox of TitledPanes — no pagination. For 1000+ interns, this is unusable.

The fix:
- Use `TableView` (virtualized) — handles 10,000+ rows without pagination.
- For very large datasets, add `Pagination` with keyset queries.

## Further reading

- *SQL Performance Explained* (Winand) — Pagination chapter.
