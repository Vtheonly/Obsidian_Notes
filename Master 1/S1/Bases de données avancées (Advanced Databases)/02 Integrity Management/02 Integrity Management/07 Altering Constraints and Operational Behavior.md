# 3. Altering Constraints and Operational Behavior

While static constraints are usually defined during the `CREATE TABLE` phase, databases evolve. You will frequently need to add, modify, or remove constraints on live tables using the `ALTER TABLE` command.

## 1. Managing Constraints Post-Creation

To modify a constraint, you cannot simply "edit" it. You must entirely **DROP** the old constraint and **ADD** a new one.

### Dropping a Constraint
To drop a constraint, you must know its name. If you did not explicitly name it during creation, the DBMS auto-generated a name (which you can find by querying the `information_schema.TABLE_CONSTRAINTS` table).

```sql
-- Dropping a CHECK constraint
ALTER TABLE Students DROP CONSTRAINT check_note;

-- Dropping a FOREIGN KEY constraint
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
> [!warning] Precaution
> When you add a constraint to an existing table, the DBMS will instantly scan all existing rows. If even one existing row violates the new constraint, the `ALTER TABLE` command will fail and the constraint will not be added.

## 2. Advanced Foreign Key Behaviors
Understanding exactly how Foreign Keys restrict data is crucial for preventing orphaned data.

### Visualizing CASCADE vs SET NULL

Imagine a `Departments` table (Parent) and an `Employees` table (Child). Department 10 is "IT". Alice and Bob work in IT.

**Scenario: We DELETE Department 10.**

*   **If `ON DELETE CASCADE`:** The DBMS destroys Department 10. It then actively searches the `Employees` table and completely deletes the records for Alice and Bob. This maintains perfect relational parity but is dangerous if unintended.
*   **If `ON DELETE SET NULL`:** The DBMS destroys Department 10. It searches the `Employees` table and changes the `department_id` for Alice and Bob from 10 to `NULL`. Alice and Bob still exist, but they are now unassigned.
*   **If `ON DELETE RESTRICT`:** The DBMS blocks the query. It returns an error: *"Cannot delete or update a parent row: a foreign key constraint fails"*. You must manually reassign or delete Alice and Bob before the database will allow you to delete Department 10.
