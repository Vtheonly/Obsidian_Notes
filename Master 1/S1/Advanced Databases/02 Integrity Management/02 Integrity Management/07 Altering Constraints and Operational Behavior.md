# 3. Altering Constraints and Operational Behavior

While static constraints are usually defined during the `CREATE TABLE` phase, databases evolve. You will frequently need to add, modify, or remove constraints on live tables using the `ALTER TABLE` command.

## 1. Managing Constraints Post-Creation

To modify a constraint, you normally replace it rather than editing its definition in place: **DROP** the old constraint and **ADD** the corrected constraint.

### Dropping a Constraint
To drop a constraint, you must know its name. If you did not explicitly name it during creation, the DBMS auto-generated a name (which you can find by querying the information schema or another DBMS-specific catalog).

```sql
-- Dropping a CHECK constraint
ALTER TABLE Students DROP CONSTRAINT check_note;

-- Dropping a FOREIGN KEY constraint in MySQL syntax
ALTER TABLE Orders DROP FOREIGN KEY fk_customer_id;
```

### Adding a Constraint
When adding a constraint, it is a best practice to explicitly name it using the `CONSTRAINT` keyword. This makes future modifications significantly easier.

```sql
-- Adding a CHECK constraint
ALTER TABLE Students
ADD CONSTRAINT check_email
CHECK (email LIKE '%_@__%.__%');

-- Adding a UNIQUE constraint
ALTER TABLE Students
ADD CONSTRAINT unique_nin
UNIQUE (national_id_number);
```

> [!WARNING] Existing Data and Operational Impact
> When a constraint is added to an existing table, the DBMS generally has to validate the existing data before the operation can succeed. The exact scan, locking behavior, validation strategy, and whether the operation blocks concurrent work are **DBMS- and version-dependent**. On a large production table this can therefore be an expensive DDL operation.

If even one existing row violates the new constraint, the `ALTER TABLE` operation fails and the new constraint is not successfully established.

## 2. Advanced Foreign Key Behaviors
Understanding exactly how Foreign Keys restrict data is crucial for preventing orphaned data.

### Visualizing CASCADE vs SET NULL

Imagine a `Departments` table (Parent) and an `Employees` table (Child). Department 10 is "IT". Alice and Bob work in IT.

**Scenario: We DELETE Department 10.**

*   **If `ON DELETE CASCADE`:** The DBMS removes Department 10 and propagates the delete to the dependent `Employees` rows. This maintains referential consistency but can affect many records unexpectedly.
*   **If `ON DELETE SET NULL`:** The DBMS removes Department 10 and sets Alice and Bob's `department_id` to `NULL`. The employees remain but are now unassigned. This requires the child FK column to permit `NULL`.
*   **If `ON DELETE RESTRICT`:** The DBMS blocks the deletion while dependent employees exist. The application must first reassign or delete the dependent rows.

## 3. Operational Checklist
Before changing a constraint on a live table:

1. Identify the exact constraint name and owning table.
2. Check whether current rows already satisfy the new rule.
3. Check whether application queries depend on the existing constraint behavior.
4. Consider the size of the table and the DBMS-specific locking/validation strategy.
5. Prefer explicit names for future constraints so administration is deterministic.
