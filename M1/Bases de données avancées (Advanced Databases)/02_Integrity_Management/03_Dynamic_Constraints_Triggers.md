
# Dynamic Integrity: Triggers

**Definition:** Procedural code that fires automatically in response to database events.

## Key Components
1.  **Timing:**
    *   `BEFORE`: Used for **Validation** (Check logic, abort if invalid).
    *   `AFTER`: Used for **Auditing/Logging** (Record the change) or **Cascading** (Update summary tables).
2.  **Context Variables:**
    *   `NEW`: Access the value *being inserted/updated*. (Available in INSERT/UPDATE).
    *   `OLD`: Access the value *before the change*. (Available in UPDATE/DELETE).

## Syntax Structure
```sql
CREATE TRIGGER Check_Price
BEFORE INSERT ON Products
FOR EACH ROW
BEGIN
    IF NEW.Price < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Price cannot be negative';
    END IF;
END;
```

## Static vs Dynamic
*   **Static (CHECK):** Simple rules (A > B).
*   **Dynamic (Trigger):** Complex rules involving other tables, history, or complex logic (e.g., "Cannot increase salary by more than 10%").