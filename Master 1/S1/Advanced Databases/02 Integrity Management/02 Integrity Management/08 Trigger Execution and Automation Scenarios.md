# 4. Trigger Execution and Automation Scenarios

Triggers are powerful blocks of procedural code attached to tables. They provide the ability to implement **Dynamic Integrity Constraints**—rules that require real-time context to evaluate.

## 1. Anatomy of a Trigger Execution
A trigger relies on specific contextual keywords to understand what is happening to the data.

### The Pseudo-Records: `NEW` and `OLD`
These are temporary memory structures holding the state of the row being manipulated.
*   **`INSERT` Operations:** Only `NEW` exists. It holds the values the user is trying to insert.
*   **`DELETE` Operations:** Only `OLD` exists. It holds the values of the row that is about to be destroyed.
*   **`UPDATE` Operations:** Both exist. `OLD` holds the current database value. `NEW` holds the proposed incoming value.

### The `FOR EACH ROW` Clause
In SQL, an `UPDATE` statement might affect 1,000 rows at once. By specifying `FOR EACH ROW`, the trigger will execute 1,000 separate times—once for every individual row modified. This allows row-level validation.

## 2. Common Trigger Scenarios

### Scenario A: The Audit Trail (Historization)
A common requirement in finance and security is to track every time a record is deleted, recording *what* was deleted and *when*.

```sql
DELIMITER //
CREATE TRIGGER save_deleted_client
AFTER DELETE ON Clients
FOR EACH ROW
BEGIN
    -- OLD captures the exact state of the row right before deletion
    INSERT INTO Clients_Audit (client_id, name, deleted_at)
    VALUES (OLD.id, OLD.name, NOW());
END //
DELIMITER ;
```

### Scenario B: Complex Cross-Table Automation
Triggers can reach out and touch other tables. For example, if an e-commerce order is marked as 'cancelled', the inventory should be automatically restocked.

```sql
DELIMITER //
CREATE TRIGGER handle_order_cancellation
BEFORE UPDATE ON Orders
FOR EACH ROW
BEGIN
    -- Check if the status is changing from something else TO 'cancelled'
    IF NEW.status = 'cancelled' AND OLD.status != 'cancelled' THEN
        -- Go to the Products table and add the inventory back
        UPDATE Products 
        SET stock_quantity = stock_quantity + OLD.quantity 
        WHERE id = OLD.product_id;
    END IF;
END //
DELIMITER ;
```

## 3. Best Practices for Triggers
*   **Keep them fast:** Triggers run synchronously with the query. If an `INSERT` triggers a massive calculation, the user's `INSERT` query will hang until the calculation finishes.
*   **Avoid cascading triggers:** Do not have Trigger A update Table B, which fires Trigger B to update Table C. This creates invisible spaghetti code that is a nightmare to debug.
*   **Visibility:** Use `SHOW TRIGGERS;` or `SHOW CREATE TRIGGER trigger_name;` to review the active background logic in your database, as triggers do not show up in normal table definitions.
