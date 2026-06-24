# Foreign Key Constraints

Foreign key constraints define what happens to child rows when the parent row they reference is modified or deleted. These constraints are essential for maintaining referential integrity automatically, so the database engine handles cascading changes rather than requiring application code to manually keep related tables in sync. Without foreign key constraints, deleting or updating a parent row could leave child rows pointing to nonexistent data, producing orphaned references and corrupted relationships. See [[06 - Foreign Key]] for the basic foreign key concept and [[08 - Data Integrity]] for the broader context of data integrity.

## The ON DELETE and ON UPDATE Clauses

When defining a foreign key in SQL, you specify the constraint behavior using the `ON DELETE` and `ON UPDATE` clauses. These clauses determine the action the database takes on child rows when the referenced parent row is deleted or when the parent's primary key value is updated.

```sql
CREATE TABLE comments (
    comment_id INT PRIMARY KEY,
    user_id INT,
    content TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
```

The `ON DELETE` clause specifies behavior when a parent row is deleted, and the `ON UPDATE` clause specifies behavior when a parent primary key is updated. Each clause accepts one of several action types.

## Constraint Action Types

### RESTRICT (and NO ACTION)

The `RESTRICT` action prevents the operation on the parent row if any child rows reference it. If you attempt to delete a user who has comments, the database rejects the deletion and raises an error. The parent row remains unchanged, and all child rows continue to reference it normally.

`NO ACTION` behaves identically to `RESTRICT` in most relational database management systems (including MySQL). The distinction between the two exists in the SQL standard but has no practical difference in most implementations. Both reject the parent operation when child references exist.

```sql
-- This will fail if any comments reference user_id 504
DELETE FROM users WHERE user_id = 504;
-- ERROR: Cannot delete or update a parent row: a foreign key constraint fails
```

`RESTRICT` is the safest default because it prevents accidental data loss. However, it requires the application to handle child rows explicitly before deleting or updating the parent.

### CASCADE

The `CASCADE` action propagates the parent operation to all child rows. With `ON DELETE CASCADE`, deleting a parent row automatically deletes all child rows that reference it. With `ON UPDATE CASCADE`, updating the parent's primary key automatically updates the foreign key values in all child rows to match.

```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```

With this configuration, deleting user 504 would automatically delete all orders placed by user 504. Updating user 504's primary key to 508 would automatically change the `user_id` in all corresponding order rows from 504 to 508.

`CASCADE` is appropriate when child rows have no independent meaning without their parent. For example, if order line items are meaningless without the order itself, `ON DELETE CASCADE` ensures that deleting an order also removes its line items.

### SET NULL

The `SET NULL` action sets the foreign key column in all child rows to `NULL` when the parent row is deleted or updated. The child rows themselves remain in the table, but they no longer reference any parent row.

```sql
CREATE TABLE comments (
    comment_id INT PRIMARY KEY,
    user_id INT,
    content TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE SET NULL
        ON UPDATE SET NULL
);
```

With `ON DELETE SET NULL`, deleting user 504 would set `user_id` to `NULL` in all comments that previously referenced user 504. The comments still exist but are no longer associated with any user. This is useful when you want to preserve child records even after the parent is removed.

**Important restriction:** You cannot use `SET NULL` on a foreign key column that has the `NOT NULL` constraint. If the column is declared `NOT NULL`, the database cannot set it to null, and the operation will fail with an error. See [[07 - NOT NULL Foreign Key]] for more on this interaction.

### SET DEFAULT

The `SET DEFAULT` action sets the foreign key column to its default value (as defined by the `DEFAULT` constraint on the column) when the parent is deleted or updated. This action is supported by the SQL standard but is not implemented in all database systems. MySQL, for example, recognizes the syntax but treats it as equivalent to `RESTRICT`. Check your specific RDBMS documentation for support.

## Choosing the Right Constraint

| Scenario | Recommended Action | Rationale |
|---|---|---|
| Child rows are meaningless without parent | `CASCADE` | Deleting parent should remove children |
| Child rows should survive parent deletion | `SET NULL` | Preserve children with no parent link |
| Parent deletion must be handled explicitly | `RESTRICT` | Force application to manage children first |
| Primary key updates should propagate | `CASCADE` | Keep references in sync automatically |
| Primary key should never change | `RESTRICT` | Prevent updates to parent primary key |

The combination of constraints you choose depends on the specific business rules. A common pattern is `ON DELETE RESTRICT` with `ON UPDATE CASCADE`: this prevents accidental deletion of parent rows with dependents while ensuring that any (rare) primary key updates propagate correctly.

## Composite Foreign Key Constraints

When a foreign key consists of multiple columns (a composite foreign key), the same constraint actions apply to the entire set of columns as a unit. You cannot specify different actions for individual columns within the same composite foreign key. The constraint treats the combination as a single reference.

Cross-reference: [[06 - Foreign Key]], [[07 - NOT NULL Foreign Key]], [[08 - Data Integrity]]
