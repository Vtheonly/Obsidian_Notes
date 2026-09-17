# 4. Wide Column Physical Layout and JSONiq Context

To understand the Wide-Column Store (like Cassandra or HBase), we must look past the conceptual table representation and examine how data is mapped to disk as a multi-dimensional nested hash map.

## 1. The Multi-Dimensional Map
In a relational database, a table is a 2D array: Rows and Columns. If a column has no data, it still occupies space as a `NULL`.
In a Wide-Column store, the schema is radically different. The database is fundamentally a 4-dimensional map:
`[Row Key] -> [Column Family] -> [Column Name] -> [Timestamp] = Value`

### Breaking down the Slides' Example:
Imagine we store user data: `user_123` is the `Row Key`.

```json
"user_123": {
    "Users_Family": {
        "name": {
            "1698000001": "Ali"
        },
        "email": {
            "1698000002": "ali@mail.com"
        },
        "age": {
            "1698000003": 28
        }
    }
}
```

**Why this layout matters:**
1.  **Sparsity:** Notice `user_456` in the slides does not have an `email` or `age`, but *does* have a `city`. Because the structure is a nested dictionary, the missing columns literally do not exist on the disk. There are no `NULL` placeholders wasting space.
2.  **Version Control at the Cell Level:** Because the final key is a `Timestamp`, the database can hold multiple versions of the exact same cell (e.g., changing "Ali" to "Ali B."). The query simply fetches the one with the highest timestamp (Last Write Wins).

## 2. A Brief Note on JSONiq
While Cypher is the standard for Graph databases, the slides briefly mention **JSONiq** in the curriculum plan. 
*   **What is it?** JSONiq is a query language designed explicitly to query and manipulate JSON documents, similar to how XQuery works for XML. 
*   **Purpose:** While MongoDB has its own JSON-based syntax (e.g., `db.collection.find()`), JSONiq aims to be a standardized, declarative language (like SQL) but built natively for the hierarchical, nested, and schema-less nature of JSON data. It allows for complex iterative filtering, let clauses, and nested grouping that native database drivers often make cumbersome.
