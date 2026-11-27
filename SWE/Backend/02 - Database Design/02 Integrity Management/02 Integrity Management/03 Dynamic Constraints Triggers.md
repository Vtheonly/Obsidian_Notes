# Dynamic Integrity: Triggers & Stored Procedures

## 1. The Need for Dynamic Constraints
Static constraints (PK, FK, CHECK) are declarative. However, sometimes business logic depends on:
1.  **State changes:** Comparing the *new* value vs. the *old* value (e.g., "Salary cannot decrease").
2.  **Complex validation:** Checking data across multiple tables.
3.  **Auditing:** Logging who changed what and when.

This is where **Triggers** come in.

---

## 2. Anatomy of a Trigger
A trigger is a PL/SQL block stored in the database that fires automatically when an event occurs.

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

### Key Concepts
| Concept | Description |
| :--- | :--- |
| **Timing** | `BEFORE`: Used for validation or modifying data *before* it hits the disk. <br> `AFTER`: Used for auditing, logging, or cascading updates to other tables. |
| **Event** | `INSERT`, `UPDATE`, `DELETE`. |
| **Scope** | `FOR EACH ROW`: The trigger fires once for every row affected. |
| **Variables** | `NEW`: Represents the value *about to be* inserted/updated. <br> `OLD`: Represents the value *before* the update/delete. |

> [!TIP] When to use NEW vs OLD?
> *   **INSERT:** Only `NEW` exists.
> *   **DELETE:** Only `OLD` exists.
> *   **UPDATE:** Both exist. `OLD` is the previous value, `NEW` is the incoming value.

---

## 3. Procedural SQL (PL/SQL) Elements
To write triggers (and Stored Procedures), you need procedural logic.

### Variables
```sql
DECLARE total_sales INT DEFAULT 0;
SET total_sales = 100;
-- Or extracting from DB
SELECT count(*) INTO total_sales FROM Orders;
```

### Control Flow
```sql
-- IF Statement
IF (NEW.age < 18) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User is too young';
END IF;

-- LOOPS
WHILE (x < 10) DO
    SET x = x + 1;
END WHILE;
```

### Cursors
Used when a query returns multiple rows and you need to process them one by one.
1.  **Declare:** `DECLARE cursor_name CURSOR FOR SELECT ...`
2.  **Open:** `OPEN cursor_name;`
3.  **Fetch:** `FETCH cursor_name INTO variable_list;`
4.  **Close:** `CLOSE cursor_name;`

> [!INFO] Handlers
> You need a `CONTINUE HANDLER` to stop the loop when the cursor runs out of data (NOT FOUND).

### Complete Example: `Process_Completed_Order` (Cursor + Handler)
A real trigger (`AFTER UPDATE ON Orders`) combining a `CURSOR`, a `CONTINUE HANDLER FOR NOT FOUND`, a `LOOP`/`LEAVE` control structure, and `Inventory` updates — it only runs when an order's status transitions to `'Completed'`:

```sql
DELIMITER $$

CREATE TRIGGER Process_Completed_Order
AFTER UPDATE ON Orders
FOR EACH ROW
BEGIN
    -- Declare loop control flags and row variables
    DECLARE finished INT DEFAULT 0;
    DECLARE item_id INT;
    DECLARE qty INT;
    
    -- 1. Declare the Cursor
    DECLARE cursor_items CURSOR FOR 
        SELECT ProductID, Quantity 
        FROM Order_Items 
        WHERE OrderID = NEW.ID;
        
    -- 2. Declare a Continue Handler to catch when cursor rows are exhausted
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
    
    -- Trigger logic: only run if status changed to 'Completed'
    IF (NEW.Status = 'Completed' AND OLD.Status <> 'Completed') THEN
        
        -- 3. Open the Cursor
        OPEN cursor_items;
        
        -- 4. Loop and Fetch data
        process_loop: LOOP
            FETCH cursor_items INTO item_id, qty;
            
            -- Exit the loop if the handler flipped the finish flag
            IF finished = 1 THEN 
                LEAVE process_loop;
            END IF;
            
            -- Business logic: update stock for each item in the order
            UPDATE Inventory 
            SET StockLevel = StockLevel - qty 
            WHERE ProductID = item_id;
            
        END LOOP process_loop;
        
        -- 5. Close the Cursor to free up database memory
        CLOSE cursor_items;
        
    END IF;
END $$

DELIMITER ;
```

---

## 4. Example: The "Pilot Qualification" Trigger (From TD4)
**Scenario:** A pilot cannot acquire a qualification if they already have 3 qualifications.

```sql
DELIMITER $$

CREATE TRIGGER Check_Pilot_Qualif
BEFORE INSERT ON Qualifications
FOR EACH ROW
BEGIN
    -- 1. Declare a variable to hold the count
    DECLARE count_qualif INT;

    -- 2. Count existing qualifications for this pilot
    SELECT COUNT(*) INTO count_qualif 
    FROM Qualifications 
    WHERE pilot_id = NEW.pilot_id;

    -- 3. Check condition
    IF (count_qualif >= 3) THEN
        -- 4. Block the insertion with an error
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Error: Pilot cannot have more than 3 qualifications.';
    END IF;
END $$

DELIMITER ;
```

### Explanation of the Code
1.  **`BEFORE INSERT`**: We must check *before* adding the data. If we used `AFTER`, the bad data would already be in the table.
2.  **`DECLARE`**: Creates a local variable `count_qualif` to store our calculation.
3.  **`SELECT ... INTO`**: Runs a query and puts the result into our variable. Note we use `NEW.pilot_id` to check the pilot currently being processed.
4.  **`SIGNAL SQLSTATE`**: This is how you throw an exception in MySQL. It aborts the transaction and prevents the insert.



