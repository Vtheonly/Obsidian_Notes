# Dynamic Integrity: Triggers & Stored Procedures

## 1. The Need for Dynamic Constraints
Static constraints (PK, FK, CHECK) are declarative. However, sometimes business logic depends on:
1. **State changes:** Comparing the *new* value vs. the *old* value (e.g., "Salary cannot decrease").
2. **Complex validation:** Checking data across multiple tables or enforcing rules that depend on more than the current row.
3. **Auditing:** Logging who changed what and when.
4. **Automatic propagation:** Updating counters, inventory, or denormalized values after a successful change.

This is where **Triggers** come in.

---

## 2. Anatomy of a Trigger
A trigger is a database object containing procedural logic that fires automatically when its configured event occurs.

### Syntax Structure
```sql
CREATE TRIGGER trigger_name
{BEFORE | AFTER} {INSERT | UPDATE | DELETE}
ON table_name
FOR EACH ROW
BEGIN
    -- Trigger Logic Here
END;
```

### The ECA Model
Triggers are naturally described using **Event–Condition–Action**:

* **Event:** `INSERT`, `UPDATE`, or `DELETE` activates the trigger.
* **Condition:** Optional logic determines whether the action should run.
* **Action:** Procedural SQL performs validation, correction, logging, or propagation.

### Key Concepts
| Concept | Description |
| :--- | :--- |
| **Timing** | `BEFORE`: validation/correction before the row is written. `AFTER`: logic that depends on a successful modification, such as auditing or updating related tables. |
| **Event** | `INSERT`, `UPDATE`, `DELETE`. |
| **Scope** | `FOR EACH ROW`: the trigger executes once for every affected row. Some DBMSs also support statement-level triggers, which execute once per statement and do not expose row-specific `NEW`/`OLD` values. |
| **Variables** | `NEW`: the incoming row for `INSERT`/`UPDATE`. `OLD`: the previous row for `UPDATE`/`DELETE`. |

> [!TIP] When to use `NEW` vs `OLD`?
> * `INSERT`: only `NEW` is available.
> * `DELETE`: only `OLD` is available.
> * `UPDATE`: both are available; `OLD` is the previous state and `NEW` is the proposed state.

---

## 3. BEFORE vs. AFTER

### `BEFORE`
Use a `BEFORE` trigger when the row must be validated, normalized, rejected, or adjusted before persistence.

```sql
IF (NEW.age < 18) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User is too young';
END IF;
```

In MySQL-style triggers, a `BEFORE` trigger can modify writable `NEW` fields, for example:

```sql
SET NEW.email = LOWER(NEW.email);
```

### `AFTER`
Use an `AFTER` trigger when the triggering modification has succeeded and another action should follow it, for example recording history or maintaining a counter in another table.

```sql
INSERT INTO salary_history (emp_id, old_sal, new_sal)
VALUES (OLD.id, OLD.salary, NEW.salary);
```

`NEW` is not a general-purpose editable buffer in an `AFTER` trigger because the triggering row has already been processed.

---

## 4. Procedural SQL Elements Used by Triggers
Triggers commonly use the same procedural building blocks as stored procedures.

### Variables and Queries
```sql
DECLARE total_sales INT DEFAULT 0;
SET total_sales = 100;
SELECT COUNT(*) INTO total_sales FROM Orders;
```

When using `SELECT ... INTO`, the query must be designed so that the result cardinality is appropriate for a scalar assignment. Aggregates such as `COUNT(*)` naturally produce one row; a plain multi-row query requires a cursor instead.

### Control Flow
```sql
IF (NEW.age < 18) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User is too young';
END IF;

WHILE (x < 10) DO
    SET x = x + 1;
END WHILE;
```

### Cursors
Used when a query returns multiple rows and you need to process them one by one.
1. **Declare:** `DECLARE cursor_name CURSOR FOR SELECT ...`
2. **Open:** `OPEN cursor_name;`
3. **Fetch:** `FETCH cursor_name INTO variable_list;`
4. **Close:** `CLOSE cursor_name;`

> [!INFO] Handlers
> A `CONTINUE HANDLER FOR NOT FOUND` is commonly used to set a flag when `FETCH` reaches the end of a cursor result set.

---

## 5. Common Dynamic-Integrity Patterns

### Audit Trail
```sql
CREATE TRIGGER save_deleted_client
AFTER DELETE ON Clients
FOR EACH ROW
BEGIN
    INSERT INTO Clients_Audit (client_id, name, deleted_at)
    VALUES (OLD.id, OLD.name, NOW());
END;
```

### Cross-Table Automation
```sql
CREATE TRIGGER handle_order_cancellation
BEFORE UPDATE ON Orders
FOR EACH ROW
BEGIN
    IF NEW.status = 'cancelled' AND OLD.status <> 'cancelled' THEN
        UPDATE Products
        SET stock_quantity = stock_quantity + OLD.quantity
        WHERE id = OLD.product_id;
    END IF;
END;
```

### Denormalized Counter Maintenance
A trigger can maintain a cached count or aggregate in another table after a successful child insertion/deletion. The write should be kept simple because triggers execute synchronously as part of the original operation.

---

## 6. Trigger Restrictions and Design Risks

1. **No explicit transaction boundaries:** A trigger runs inside the transaction that fired it. Explicit `START TRANSACTION`, `COMMIT`, and `ROLLBACK` statements are therefore not appropriate inside a trigger body in systems that prohibit them.
2. **Recursive/cascading behavior:** A trigger that modifies another table may fire additional triggers. Long trigger chains are hard to reason about and debug.
3. **Self-referencing table access:** Some DBMSs restrict querying or modifying the table currently being changed by a row-level trigger. The exact restriction is DBMS-specific; Oracle, for example, has mutating-table restrictions in relevant trigger contexts.
4. **Performance:** Trigger work is synchronous. A large query or expensive calculation inside a trigger increases the latency of the original `INSERT`, `UPDATE`, or `DELETE`.

---

## 7. Example: The "Pilot Qualification" Trigger (From TD4)
**Scenario:** A pilot cannot acquire a qualification if they already have 3 qualifications.

```sql
DELIMITER $$

CREATE TRIGGER Check_Pilot_Qualif
BEFORE INSERT ON Qualifications
FOR EACH ROW
BEGIN
    DECLARE count_qualif INT DEFAULT 0;

    SELECT COUNT(*) INTO count_qualif
    FROM Qualifications
    WHERE pilot_id = NEW.pilot_id;

    IF (count_qualif >= 3) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Pilot cannot have more than 3 qualifications.';
    END IF;
END $$

DELIMITER ;
```

### Explanation
1. `BEFORE INSERT` checks the condition before the new qualification is accepted.
2. `DECLARE` creates a local scalar variable.
3. `SELECT ... INTO` stores the calculated count.
4. `NEW.pilot_id` identifies the row currently being inserted.
5. `SIGNAL SQLSTATE '45000'` raises a user-defined exception and aborts the statement.
