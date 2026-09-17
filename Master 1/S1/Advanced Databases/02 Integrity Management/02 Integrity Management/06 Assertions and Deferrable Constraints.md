# Assertions and Deferrable Constraints

While basic `CHECK` constraints and `FOREIGN KEY` constraints are excellent for simple rules, they possess limitations. Advanced integrity management involves cross-table constraints and timing deferments.

## 1. Standard Constraints Limitations
A `CHECK` constraint is typically evaluated against values from the row being inserted or updated.
*   *Example:* `CHECK (Salary > 0)`

However, what if the business rule requires data from multiple tables?
*   *Example Rule:* "The total sum of salaries in department 'HR' cannot exceed $1,000,000."

This is a global, cross-row rule and cannot be expressed as an ordinary single-row `CHECK` constraint.

## 2. Assertions (`CREATE ASSERTION`)
An **Assertion** is a standalone, schema-level integrity constraint. It is independent of any specific table and expresses a rule that the entire database instance must satisfy.

### Syntax
```sql
CREATE ASSERTION Assertion_Name CHECK ( condition );
```

### Example
Ensure that no employee makes more money than their direct manager:
```sql
CREATE ASSERTION check_salary_hierarchy CHECK (
    NOT EXISTS (
        SELECT 1
        FROM Employee E
        JOIN Manager M ON E.ManagerID = M.ManagerID
        WHERE E.Salary > M.Salary
    )
);
```

> [!WARNING] Performance and Portability
> `CREATE ASSERTION` is part of the SQL standard, but support is absent from many commonly used DBMSs, including MySQL and PostgreSQL. A global assertion could require evaluating a cross-table condition whenever any referenced table changes, so implementations commonly replace it with carefully designed **triggers** or explicit validation inside **stored procedures/transactions**.

## 3. Deferrable Constraints
By default, many constraints are checked immediately after the statement that modifies the data. Deferrable constraints allow supported DBMSs to postpone validation until a later point, normally the end of the transaction.

### The Cyclic Dependency Problem
Imagine two tables, `Department` and `Employee`.
*   `Department` has a Foreign Key `ManagerID` referencing `Employee(ID)`. (Every department must have a manager.)
*   `Employee` has a Foreign Key `DeptID` referencing `Department(ID)`. (Every employee must belong to a department.)

How do you create a new Department and its Manager at the same time?
1. If you insert the Department first, it fails because the Manager does not exist yet.
2. If you insert the Manager first, it fails because the Department does not exist yet.

### The Solution: `DEFERRABLE`
The purpose of deferral is to permit temporarily incomplete references inside one transaction. The DBMS checks the constraints when the transaction reaches the configured validation point, commonly `COMMIT`.

### Mode Configurations
When creating the constraint, you attach deferrable properties:
1. **`NOT DEFERRABLE`:** The constraint is not deferrable and is checked immediately.
2. **`DEFERRABLE INITIALLY IMMEDIATE`:** The constraint is deferrable but is checked immediately by default; a transaction/session can switch it to deferred mode where supported.
3. **`DEFERRABLE INITIALLY DEFERRED`:** The constraint starts in deferred mode and is checked when the transaction is committed.

### Example Solution
```sql
ALTER TABLE Department
ADD CONSTRAINT fk_mgr FOREIGN KEY (ManagerID) REFERENCES Employee(ID)
DEFERRABLE INITIALLY DEFERRED;
```

Now, the transaction works in a DBMS that supports this syntax:
```sql
BEGIN TRANSACTION;
-- These references are temporarily incomplete, but validation is deferred:
INSERT INTO Department (ID, Name, ManagerID) VALUES (10, 'IT', 99);
INSERT INTO Employee (ID, Name, DeptID) VALUES (99, 'Alice', 10);
-- Constraint validation occurs at COMMIT.
COMMIT;
```

## 4. Commit-Time Validation Flow
A deferred constraint is not permanently ignored. The sequence is:

1. Begin the transaction.
2. Perform statements that temporarily violate the deferred rule.
3. Complete the missing referenced rows or otherwise restore the invariant.
4. `COMMIT` triggers the deferred validation.
5. If validation succeeds, the transaction commits. If it fails, the transaction cannot successfully commit and must be corrected or rolled back.

> [!IMPORTANT]
> Deferrability is DBMS-specific. MySQL, for example, does not support general `DEFERRABLE` foreign keys in the same way as PostgreSQL or Oracle, so the exact syntax and available modes depend on the engine.
