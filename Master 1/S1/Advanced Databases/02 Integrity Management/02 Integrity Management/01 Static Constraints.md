

# Static Integrity Constraints

Rules defined at the schema level (`CREATE TABLE`) that are checked before data is written.

## 1. Entity Integrity (Row Identity)
*   **PRIMARY KEY:** Unique identifier for a row. Every participating column is `NOT NULL`, and the key is enforced for uniqueness. A table can have only one primary key.
*   **UNIQUE:** Ensures no duplicates across one column or a combination of columns. A table can have multiple `UNIQUE` constraints. `NULL` handling is DBMS-dependent; in systems such as PostgreSQL and MySQL, multiple `NULL` values are generally permitted unless the column is also `NOT NULL`.
*   **NOT NULL:** Ensures a column cannot be left empty (`NULL`) and forces the application to provide a value for that column when the row is created or modified.

## 2. Domain Integrity (Value Validity)
*   **CHECK:** A Boolean expression that must not evaluate to `FALSE`.
    *   *Example:* `CHECK (Salary > 0)`
    *   *Example:* `CHECK (Status IN ('Active', 'Inactive'))`

### Three-Valued Logic and `NULL`
A common exam trap is the interaction between `CHECK` and `NULL` values. SQL uses three-valued logic: `TRUE`, `FALSE`, and `UNKNOWN`.

For example:
```sql
CHECK (Salary > 0)
```

If `Salary` is `NULL`, the expression `NULL > 0` evaluates to `UNKNOWN`, not `FALSE`. A standard `CHECK` constraint rejects `FALSE`, but normally accepts `TRUE` or `UNKNOWN`. Therefore, a `CHECK` such as `Salary > 0` does **not** by itself prevent `NULL` salaries. To reject both negative values and missing values, use:

```sql
Salary DECIMAL(10,2) NOT NULL CHECK (Salary > 0)
```

### Scope Limitation of `CHECK`
A standard row-level `CHECK` is intended to validate the row being inserted or updated. It should not be used as a substitute for cross-table or aggregate business rules such as:

> The total salary of all employees in department `HR` must not exceed 1,000,000.

Such rules require a broader mechanism, typically an assertion where supported, a trigger, or explicit transactional validation.

## 3. Complete Implementation Example
```sql
CREATE TABLE Students (
    ID INT PRIMARY KEY,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Age INT CHECK (Age >= 18),
    Status VARCHAR(20) DEFAULT 'Active'
        CHECK (Status IN ('Active', 'Inactive', 'Suspended'))
);
```

## 4. Constraints as a Database-Level Safety Boundary
Static constraints are enforced by the DBMS rather than by one specific application. This means a second application, script, or administrative session cannot bypass the rule simply by using different application code. The constraint therefore acts as a persistent integrity boundary around the schema.

## 5. Naming and Managing Constraints
Explicit constraint names are strongly recommended because they make later administration predictable:

```sql
CREATE TABLE Students (
    ID INT,
    CONSTRAINT pk_students PRIMARY KEY (ID),
    CONSTRAINT chk_student_age CHECK (Age >= 18)
);
```

Named constraints can later be identified and removed with `ALTER TABLE`. When a constraint was not explicitly named, its generated name can be found through the DBMS metadata catalog, such as `information_schema.TABLE_CONSTRAINTS` in MySQL.
