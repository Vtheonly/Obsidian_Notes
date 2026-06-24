# Indexes

An index is a data structure that improves the speed of data retrieval operations on a database table at the cost of additional storage and slower write operations. Indexes work by maintaining a sorted or organized representation of selected column values along with pointers to the actual row locations, allowing the database engine to locate specific rows without scanning the entire table. Understanding when and how to create indexes is critical for designing databases that perform well under load. See [[21 - Primary Key Index]] for the specific case of indexes created automatically on primary keys.

## The Analogy: Book Index and Phone Book

A nonclustered index is analogous to the index at the back of a book. The index lists topics in sorted order and tells you which page to turn to. You find the topic quickly without reading the entire book, then go directly to the referenced page. The data (the book's content) is stored separately from the index, and the index merely points to where the data is located.

A clustered index is analogous to a phone book. The phone book itself is sorted alphabetically by name, and the data (the phone number) is right there next to the name. You do not need to look up a page number and then go somewhere else -- the data is stored in the sorted order of the index. This is why a phone book can only be sorted one way: the physical arrangement of the data is the index.

## Clustered Indexes

A clustered index determines the physical storage order of the rows in a table. Because the data rows themselves are stored in the sorted order defined by the clustered index, a table can have only one clustered index. The clustered index is typically created on the primary key column by default in most database systems, though this default can be overridden.

When a query searches for a row using the clustered index key (e.g., `WHERE user_id = 72`), the database can navigate directly to the correct location in the sorted data without scanning from the beginning. This is known as an **index seek**, and it is dramatically faster than a **table scan** (reading every row sequentially) for large tables.

```sql
-- Most RDBMS create a clustered index on the primary key automatically
CREATE TABLE users (
    user_id INT PRIMARY KEY,       -- clustered index created on user_id
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100)
);
```

### When the clustered index is used

The clustered index is most effective when queries filter on the primary key or when a range of values is needed. For example, `WHERE user_id BETWEEN 50 AND 100` benefits from the clustered index because the rows are stored in `user_id` order, so the database can jump to the start of the range and read sequentially.

## Nonclustered Indexes

A nonclustered index is a separate structure from the table data. It stores the indexed column values in sorted order along with pointers (row locators) to the actual data rows. A table can have multiple nonclustered indexes, because each one is an independent structure that does not affect the physical storage order of the data.

When a query uses a nonclustered index, the database first searches the index structure to find the matching values and their row locators, then retrieves the actual data rows using those locators. This two-step process is still much faster than a full table scan for selective queries, but slower than a clustered index seek for the same column.

```sql
-- Create a nonclustered index on the email column
CREATE INDEX idx_users_email ON users(email);
```

### When to create nonclustered indexes

Create nonclustered indexes on columns that are frequently used in `WHERE` clauses, `JOIN` conditions, or `ORDER BY` clauses but are not already covered by the clustered index. For example, if users frequently search for records by `email`, a nonclustered index on `email` allows the database to locate matching rows without scanning the entire table.

```sql
-- A query that benefits from the nonclustered index on email
SELECT first_name, last_name, email
FROM users
WHERE email = 'alice@example.com';
```

Without the index, the database must examine every row in the `users` table (a table scan) to find the one with the matching email. With the index, the database navigates the sorted index structure and goes directly to the matching row.

## Composite Indexes

A composite index (also called a multi-column index or concatenated index) is an index built on two or more columns. The order of columns in a composite index matters significantly, because the index sorts by the first column first, then by the second column within each first-column value, and so on.

```sql
-- Create a composite index on last_name then first_name
CREATE INDEX idx_users_name ON users(last_name, first_name);
```

### Column order and the leftmost prefix rule

A composite index on `(last_name, first_name)` can efficiently serve queries that filter on:

- Both `last_name` and `first_name`: `WHERE last_name = 'Curry' AND first_name = 'Caleb'`
- Only `last_name`: `WHERE last_name = 'Curry'`

The index cannot efficiently serve queries that filter on only `first_name` without `last_name`, because the index is sorted by `last_name` first. Searching for `WHERE first_name = 'Caleb'` would still require scanning a large portion of the index. This principle is known as the **leftmost prefix rule**: a composite index can be used for any leftmost prefix of its columns, but not for columns in the middle or end alone.

### Designing composite indexes

When designing composite indexes, place the most selective or most frequently queried column first. If you commonly query by `last_name` alone and also by `last_name` plus `first_name`, a single composite index `(last_name, first_name)` serves both patterns, eliminating the need for a separate index on `last_name`.

## Index Overhead

Indexes are not free. Every index adds storage overhead (the index structure occupies disk space) and write overhead (every `INSERT`, `UPDATE`, or `DELETE` must also update all affected indexes). For a table with heavy write activity and multiple indexes, the cost of maintaining indexes during write operations can be significant.

Consider the trade-offs:

| Operation | Without Index | With Index |
|---|---|---|
| SELECT (filtered) | Table scan (slow for large tables) | Index seek (fast) |
| INSERT | Write row only | Write row + update each index |
| UPDATE (indexed column) | Modify row | Modify row + update affected indexes |
| DELETE | Remove row | Remove row + update affected indexes |

Create indexes selectively on columns that are actually used in queries. Do not index every column, as this would maximize read performance for arbitrary queries but severely degrade write performance. Monitor query patterns and create indexes to support the most common and performance-critical queries.

## Indexes and Joins

Indexes are particularly important for join operations. When two tables are joined on a common column (typically a primary key and foreign key), the database needs to quickly locate matching rows in both tables. An index on the join columns enables the database to use an index seek rather than a table scan for each row being matched.

```sql
-- Join between users and comments benefits from indexes on join columns
SELECT u.first_name, u.last_name, c.content
FROM users u
JOIN comments c ON u.user_id = c.user_id
WHERE u.last_name = 'Curry';
```

In this query, an index on `comments.user_id` (the foreign key) allows the database to quickly find all comments by a given user. An index on `users.user_id` (the primary key, usually clustered) allows the database to quickly locate each user row. Both indexes contribute to efficient join processing.

## B-Tree Structure Overview

Most database indexes are implemented using a B-tree (balanced tree) structure. A B-tree maintains sorted data and allows searches, insertions, and deletions in logarithmic time. The tree consists of a root node, intermediate nodes, and leaf nodes. Each node contains key values and pointers to child nodes (or to data rows in the case of leaf nodes).

For a nonclustered index, the leaf nodes contain the indexed column values and row locators (pointers to the actual data rows). For a clustered index, the leaf nodes are the data rows themselves, stored in sorted order. The B-tree structure ensures that the index remains balanced after insertions and deletions, maintaining consistent query performance regardless of data growth.

## Index Creation Examples

```sql
-- Clustered index (often created automatically with PRIMARY KEY)
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    total DECIMAL(10,2)
);

-- Nonclustered index on a frequently queried column
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- Composite index for multi-column queries
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Unique index to enforce uniqueness (like an alternate key)
CREATE UNIQUE INDEX idx_orders_date_total ON orders(order_date, total);
```

## Index Design Guidelines

1. **Index the primary key**: This is typically done automatically by the RDBMS
2. **Index foreign key columns**: Foreign keys are used in joins and benefit from indexes
3. **Index columns used in WHERE clauses**: Any column frequently filtered on should be indexed
4. **Consider composite indexes for multi-column filters**: One composite index can replace multiple single-column indexes for common query patterns
5. **Avoid over-indexing**: Each index adds write overhead; index only what you need
6. **Monitor and adjust**: Use query execution plans to identify slow queries and determine which indexes would help

Cross-reference: [[21 - Primary Key Index]], [[27 - Foreign Key]]
