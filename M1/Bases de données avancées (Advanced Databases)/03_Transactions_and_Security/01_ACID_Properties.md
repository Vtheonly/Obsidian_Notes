
# Transaction Management: ACID

A **Transaction** is a logical unit of work (a set of SQL queries) that must be treated as a whole.

## The 4 Pillars (ACID)

### 1. Atomicity (Tout ou Rien)
*   Either all queries in the transaction succeed, or none do.
*   If a crash happens halfway, the DB performs a **Rollback**.

### 2. Consistency
*   The transaction moves the DB from one valid state to another valid state.
*   All constraints (Foreign Keys, Checks) must be satisfied at the end.

### 3. Isolation
*   Transactions running simultaneously should not interfere with each other.
*   (See `02_Concurrency_Control_and_Isolation` for details).

### 4. Durability
*   Once `COMMIT` is confirmed, the data is saved permanently, even if the power fails immediately after.
*   Achieved via **Write-Ahead Logging (WAL)**.
