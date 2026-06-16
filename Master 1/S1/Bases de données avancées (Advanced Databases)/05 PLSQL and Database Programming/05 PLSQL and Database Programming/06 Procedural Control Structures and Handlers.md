# 6. Procedural Control Structures and Handlers

To write complex Stored Procedures, you must utilize control structures (IF, Loops) and advanced error handlers.

## 1. Variables and Flow Control
Unlike declarative SQL, procedural SQL allows you to maintain state.

### Variables
You must declare variables at the very beginning of a `BEGIN...END` block.
```sql
DECLARE total_revenue DECIMAL(10,2) DEFAULT 0.00;
-- Assigning values
SET total_revenue = 500.50;
-- Or assigning via a query
SELECT SUM(amount) INTO total_revenue FROM Orders;
```

### Conditional Logic
*   **IF / THEN / ELSE:**
    ```sql
    IF total_revenue > 10000 THEN
        SET status = 'VIP';
    ELSEIF total_revenue > 5000 THEN
        SET status = 'Gold';
    ELSE
        SET status = 'Standard';
    END IF;
    ```
*   **CASE:** Useful for multiple distinct conditions.
    ```sql
    CASE 
        WHEN age < 18 THEN SET category = 'Minor';
        WHEN age BETWEEN 18 AND 65 THEN SET category = 'Adult';
        ELSE SET category = 'Senior';
    END CASE;
    ```

### Loops
*   **WHILE Loop:** Executes as long as a condition is true.
    ```sql
    WHILE counter < 10 DO
        SET counter = counter + 1;
    END WHILE;
    ```
*   **LOOP with LEAVE:** An infinite loop that must be manually broken.
    ```sql
    my_loop: LOOP
        SET counter = counter + 1;
        IF counter >= 10 THEN
            LEAVE my_loop; -- This is the equivalent of 'break'
        END IF;
    END LOOP my_loop;
    ```

## 2. Advanced Error Handling Mechanics
A robust stored procedure uses `DECLARE ... HANDLER` to manage exceptions.

### `CONTINUE` vs `EXIT`
*   **`EXIT HANDLER`:** Immediately stops the execution of the entire `BEGIN...END` block. It is best practice to use this for critical errors alongside a `ROLLBACK` to ensure partial transactions are destroyed.
*   **`CONTINUE HANDLER`:** Catches the error, executes a specific instruction (like setting a flag to NULL), and then forces the procedure to move to the very next line of code.

### The `NOT FOUND` Handler
When writing loops that fetch data row-by-row (using Cursors) or when doing a `SELECT ... INTO`, the database throws an error if it runs out of rows. You *must* catch this using a `NOT FOUND` continue handler so the procedure knows to exit the loop cleanly rather than crashing.

```sql
DECLARE finished INT DEFAULT 0;
-- When the database runs out of rows, it will change 'finished' to 1
DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
```
