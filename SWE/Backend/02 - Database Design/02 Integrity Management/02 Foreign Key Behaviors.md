

# Foreign Key Behaviors

**Concept:** **Declarative Referential Integrity (DRI)** ensures that a relationship between two tables remains valid. If `Order` references `Customer`, the Customer must exist. Formally, the database guarantees that the foreign key value must either reference a valid, existing parent row, or be set to `NULL`.

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDERS : places
    CUSTOMER {
        int customer_id PK
        string name
    }
    ORDERS {
        int order_id PK
        int customer_id FK
        double total_price
    }
```

## Foreign Key Violations (Parent-Child Relationship Lifecycle)
The parent table contains the primary key referenced by the child table. Referential integrity rules are triggered when:
1.  An application attempts to insert or update a child row with a foreign key value that does not exist in the parent table (**Child-side violation**).
2.  An application attempts to update the primary key of a parent row, or delete a parent row, while child rows are still linked to it (**Parent-side violation**).

## What happens when the Parent is Deleted or Updated?
You must define the behavior for the Child records. To handle parent-side deletions and updates, you define **referential actions** on the foreign key constraint — these actions apply to **both `ON DELETE` and `ON UPDATE`**, dictating how the database engine propagates changes to preserve integrity.

### 1. CASCADE
*   **Action:** Delete the child automatically.
*   **Use Case:** Strong composition. If a `Post` is deleted, its `Comments` should also be deleted.
*   **Performance Risk:** Deleting a single parent row can trigger a cascading delete across **millions of child rows**, locking multiple tables and causing significant performance overhead.

### 2. SET NULL
*   **Action:** Keep the child, but remove the link (Set FK to NULL).
*   **Use Case:** Loose association. If an `Employee` leaves, their `Tasks` should remain but be unassigned.
*   **Constraint Collision:** This action will fail with a database error if the child table's foreign key column is defined with a `NOT NULL` constraint.

### 3. RESTRICT (Default)
*   **Action:** Block the deletion (or update). Throw an error — the transaction is aborted with a foreign key violation error.
*   **Use Case:** Data protection. You cannot delete a `Category` if `Products` are still using it. This is the default option in most relational systems to prevent accidental data loss.

### 4. SET DEFAULT
*   **Action:** Change the FK to a specific default ID.
*   **Use Case:** Fallback. If a `Teacher` leaves, assign students to a "Substitute Teacher" ID.

## Database Engine Execution Flow
The following diagram illustrates the path the database engine takes when a user deletes a record from a parent table:

```mermaid
sequenceDiagram
    autonumber
    actor User as Client Application
    participant Engine as SQL Database Engine
    participant Parent as Parent Table (Customers)
    participant Child as Child Table (Orders)

    User->>Engine: DELETE FROM Customers WHERE ID = 101
    Note over Engine: Check System Catalog for FK Dependencies
    Engine->>Parent: Scan for row where ID = 101
    
    alt Parent row does not exist
        Engine-->>User: Success (0 rows affected)
    else Parent row exists
        Engine->>Child: Scan for Child Records referencing Customer_ID = 101
        
        alt No child records found
            Engine->>Parent: Delete row 101
            Engine-->>User: Success (Parent deleted)
        else Child records exist
            alt Constraint is RESTRICT (Default)
                Engine-->>User: Error! (Foreign Key Violation: Restrict blocks deletion)
            else Constraint is CASCADE
                Engine->>Child: Delete all rows where Customer_ID = 101
                Engine->>Parent: Delete row 101
                Engine-->>User: Success (Parent + Child records deleted)
            else Constraint is SET NULL
                Engine->>Child: Update child rows set Customer_ID = NULL where Customer_ID = 101
                Engine->>Parent: Delete row 101
                Engine-->>User: Success (Parent deleted, Child rows updated to NULL)
            end
        end
    end
```
