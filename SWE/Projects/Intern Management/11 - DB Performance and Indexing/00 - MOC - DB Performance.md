---
tags: [moc, database, performance, indexing]
type: moc
status: complete
---

# MOC — DB Performance and Indexing

## Notes (read in order)

1. [[11 - DB Performance and Indexing/01 - B-Tree Index]] — the default index type.
2. [[11 - DB Performance and Indexing/04 - Bitmap Index]] — for low-cardinality columns.
3. [[11 - DB Performance and Indexing/12 - Function-Based Index]] — for `UPPER(name)` queries.
4. [[11 - DB Performance and Indexing/08 - Composite and Covering Indexes]] — multi-column indexes.
5. [[11 - DB Performance and Indexing/16 - Indexing Foreign Keys]] — critical for concurrency.
6. [[11 - DB Performance and Indexing/18 - N+1 Query Problem]] — the project's search bug.
7. [[11 - DB Performance and Indexing/11 - EXPLAIN Plan]] — reading execution plans.
8. [[11 - DB Performance and Indexing/09 - Connection Pooling]] — why pools exist.
9. [[11 - DB Performance and Indexing/15 - HikariCP]] — the recommended pool.
10. [[11 - DB Performance and Indexing/06 - Caffeine Cache]] — in-process caching.
11. [[11 - DB Performance and Indexing/03 - Batch Operations]] — addBatch, executeBatch.
12. [[11 - DB Performance and Indexing/19 - Pagination]] — OFFSET/FETCH, keyset pagination.
