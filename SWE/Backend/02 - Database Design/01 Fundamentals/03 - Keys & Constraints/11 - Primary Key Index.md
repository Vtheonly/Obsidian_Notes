# Primary Key Index

When a primary key is defined on a table, the database automatically creates an index for it. This index is a data structure that allows the database to locate rows by their primary key value without scanning the entire table. Understanding how primary key indexes work is essential for writing efficient queries and designing databases that perform well at scale.

## What Is an Index?

An index in a database is analogous to the index at the back of a book. If you want to find information about a specific topic in a book, you can flip to the index, look up the topic, find the page number, and go directly to that page. This is vastly faster than reading through every page of the book sequentially until you find what you are looking for. A database index works the same way: it stores a sorted mapping of key values to the physical locations of the corresponding rows, enabling rapid lookup.

Without an index, the database must perform a **full table scan** to find rows matching a query condition. This means examining every single row in the table, one by one, checking whether it satisfies the search criteria. For a small table with a few hundred rows, this is acceptable. For a table with millions or billions of rows, a full table scan is catastrophically slow.

## How Primary Key Indexes Work

When you declare a primary key, the database creates a unique index on the primary key column or columns. This index is typically implemented as a **B-tree** (balanced tree), a data structure that maintains sorted data and allows searches, insertions, and deletions in logarithmic time.

### B-Tree Structure (Simplified)

A B-tree is organized as a hierarchy of nodes. The top of the tree is the **root node**. Below the root are **intermediate nodes**, and at the bottom are **leaf nodes** that contain pointers to the actual data rows.

```
                    [Root: 50]
                   /          \
          [Leaf: 25, 50]    [Leaf: 75, 100]
```

When the database searches for a row with primary key value 75, it starts at the root node. The root contains values that divide the key space into ranges. By comparing the search key (75) with the values in the root, the database determines which branch to follow. It then moves to the appropriate child node and repeats the process until it reaches a leaf node containing the pointer to the actual row.

This process has a time complexity of O(log n), meaning the number of steps grows logarithmically with the number of rows. For a table with 1,000,000 rows, a B-tree lookup might require only about 20 node visits, compared to scanning all 1,000,000 rows without an index.

### Step-by-Step Lookup Example

Consider a users table with 10 million rows, indexed by `user_id` as the primary key. You execute:

```sql
SELECT * FROM users WHERE user_id = 8675309;
```

Without an index, the database starts at row 1, checks if user_id equals 8675309, moves to row 2, checks again, and continues until it finds the matching row. In the worst case, it reads all 10 million rows.

With the primary key B-tree index, the database navigates the tree:

1. Start at the root node, which contains range boundaries like [0, 5000000, 10000000].
2. Since 8675309 is between 5000000 and 10000000, follow the right branch.
3. At the next level, narrower ranges like [5000000, 7500000, 10000000] direct the search further.
4. Continue descending through intermediate nodes until reaching the leaf node containing the pointer to the row with user_id = 8675309.
5. Follow the pointer to retrieve the actual row data.

Instead of 10 million comparisons, the database performs approximately 23 comparisons (log base 2 of 10 million). This is an improvement of several orders of magnitude.

## Why Indexes Matter for Keys

Primary key indexes are crucial because keys are used in three of the most common database operations:

**SELECT with WHERE clauses.** Queries that filter by primary key are extremely common. The index allows these queries to execute in logarithmic time rather than linear time.

```sql
SELECT * FROM users WHERE user_id = 42;
```

**JOIN operations.** Joins combine rows from two tables based on a related column, typically a primary key and a foreign key. Without an index on the primary key, every row in the parent table would need to be scanned for each row in the child table, resulting in a Cartesian product-level cost.

```sql
SELECT u.username, c.content
FROM users u
JOIN comments c ON u.user_id = c.user_id;
```

**Foreign key enforcement.** When inserting or deleting rows with foreign keys, the database must verify that the referenced primary key exists (for inserts) or that no foreign keys reference a row being deleted. The index makes these checks efficient.

## Primary Key Index Characteristics

- **Unique**: The primary key index enforces uniqueness. No two rows can have the same primary key value.
- **Automatic**: Most relational database management systems automatically create an index when you define a primary key.
- **Clustered or non-clustered**: Depending on the RDBMS, the primary key index may be clustered (the table's physical storage is ordered by the primary key) or non-clustered (the index is a separate structure pointing to the data). In MySQL's InnoDB, the primary key is the clustered index by default.
- **Not null**: The primary key index enforces the NOT NULL constraint. No row can have a null primary key value.

## Impact on Write Performance

While indexes dramatically improve read performance, they add overhead to write operations. Every INSERT, UPDATE, or DELETE that modifies a primary key column requires the database to update the index as well. This means maintaining the B-tree structure: inserting new nodes, rebalancing the tree, and ensuring it remains sorted. For most applications, this overhead is negligible compared to the read performance gains, but it is a factor to consider for write-heavy workloads.

## See Also

- [[01 - Introduction to Keys]] - Overview of keys and their role in database design
- [[10 - Lookup Table]] - How lookup tables use keys for data integrity
- [[01 - Indexes]] - Advanced index types and configurations
