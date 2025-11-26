

# Static Integrity Constraints

Rules defined at the schema level (`CREATE TABLE`) that are checked **before** data is written.

## 1. Entity Integrity (Row Identity)
*   **PRIMARY KEY:** Unique identifier for a row. Cannot be NULL.
*   **UNIQUE:** Ensures no duplicates in a column.
*   **NOT NULL:** Ensures a column cannot be left empty.

## 2. Domain Integrity (Value Validity)
*   **CHECK:** A Boolean expression that must be true.
    *   *Example:* `CHECK (Salary > 0)`
    *   *Example:* `CHECK (Status IN ('Active', 'Inactive'))`

## Implementation Example
```sql
CREATE TABLE Students (
    ID INT PRIMARY KEY,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Age INT CHECK (Age >= 18)
);
```
