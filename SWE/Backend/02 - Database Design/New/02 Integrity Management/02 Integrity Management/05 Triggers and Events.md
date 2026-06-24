###  Sources
*   *Based on Image: 10*

### 1. Definition
A **Trigger** is a named database object that is associated with a table, and that activates when a particular event occurs for the table.

### 2. Structure & Timing
*   **Timing:**
    *   `BEFORE`: Activates before the data hits the disk. Great for **Validation** (checking constraints) or formatting data.
    *   `AFTER`: Activates after the change is successful. Great for **Logging** (Audit trails) or updating stats in other tables.
*   **Events:** `INSERT`, `UPDATE`, `DELETE`.

### 3. Context Variables (`NEW` and `OLD`)
Inside the trigger, you have access to the data rows:

| Event | `OLD` (Previous Value) | `NEW` (Proposed Value) |
| :--- | :--- | :--- |
| **INSERT** | `NULL` (Didn't exist) | Available |
| **UPDATE** | Available | Available |
| **DELETE** | Available | `NULL` (Gone) |

**Example (Audit Trigger):**
```sql
CREATE TRIGGER Before_Update_Employee
BEFORE UPDATE ON employees
FOR EACH ROW
BEGIN
    IF NEW.salary < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Salary cannot be negative';
    END IF;
    
    -- Log change
    INSERT INTO salary_history (emp_id, old_sal, new_sal)
    VALUES (OLD.id, OLD.salary, NEW.salary);
END;
```

---