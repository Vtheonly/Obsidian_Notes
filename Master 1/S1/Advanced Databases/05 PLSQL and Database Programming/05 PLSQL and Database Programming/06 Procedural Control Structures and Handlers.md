# 6. Procedural Control Structures and Handlers

To write complex Stored Procedures, you must utilize control structures (IF, CASE, loops) and advanced error handlers.

## 1. Variables and Scope
Unlike declarative SQL, procedural SQL allows you to maintain state.

### Local Variables
Local variables are declared inside a procedural block and exist only within their scope.

```sql
DECLARE total_revenue DECIMAL(10,2) DEFAULT 0.00;
SET total_revenue = 500.50;
SELECT SUM(amount) INTO total_revenue FROM Orders;
```

### Session Variables in MySQL
MySQL session variables use the `@name` form and live for the current connection rather than only the current `BEGIN...END` block.

```sql
SET @x = 10;
SELECT @x;
```

| Feature | Local variable | MySQL session variable |
| :--- | :--- | :--- |
| Declaration | `DECLARE v INT;` | No `DECLARE` required |
| Syntax | `v` | `@v` |
| Scope | Procedural block | Current session/connection |
| Typical use | Internal calculations | Passing values between statements/calls |

### `SET` vs `SELECT ... INTO`

```sql
SET total_revenue = 500.50;

SELECT SUM(amount)
INTO total_revenue
FROM Orders;
```

A `SELECT ... INTO` expression used for scalar assignment must respect the expected result cardinality. A zero-row or multi-row result can raise a condition depending on the DBMS and exact statement, so a query should be written to guarantee one scalar result when that is required. Aggregate functions such as `COUNT(*)` normally provide one result row.

## 2. Conditional Logic

### IF / THEN / ELSE
```sql
IF total_revenue > 10000 THEN
    SET status = 'VIP';
ELSEIF total_revenue > 5000 THEN
    SET status = 'Gold';
ELSE
    SET status = 'Standard';
END IF;
```

### CASE
Useful for several distinct conditions:

```sql
CASE
    WHEN age < 18 THEN SET category = 'Minor';
    WHEN age BETWEEN 18 AND 65 THEN SET category = 'Adult';
    ELSE SET category = 'Senior';
END CASE;
```

The exact `CASE` statement syntax differs between procedural dialects; distinguish a procedural `CASE` statement from the SQL expression `CASE WHEN ... END` used inside a query.

## 3. Loops

### WHILE
Executes while its condition remains true.

```sql
WHILE counter < 10 DO
    SET counter = counter + 1;
END WHILE;
```

### REPEAT ... UNTIL
Executes its body at least once and stops when the `UNTIL` condition becomes true.

```sql
REPEAT
    SET counter = counter + 1;
UNTIL counter >= 10
END REPEAT;
```

### LOOP with LEAVE
An open-ended loop that must be terminated explicitly.

```sql
my_loop: LOOP
    SET counter = counter + 1;
    IF counter >= 10 THEN
        LEAVE my_loop;
    END IF;
END LOOP my_loop;
```

### ITERATE
`ITERATE` skips the remainder of the current loop iteration and starts the next iteration.

```sql
read_loop: LOOP
    SET counter = counter + 1;
    IF counter = 5 THEN
        ITERATE read_loop;
    END IF;
    -- Other work
END LOOP read_loop;
```

## 4. Advanced Error Handling Mechanics
A robust stored procedure uses `DECLARE ... HANDLER` to manage exceptions.

### Handler Declaration Order
In MySQL-style procedural code, declare variables first, then cursors/conditions as required by the dialect, and declare handlers before executable statements.

```sql
DECLARE finished INT DEFAULT 0;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
```

### `CONTINUE` vs `EXIT`
* **`EXIT HANDLER`:** Stops execution of the handler's containing block after handling the condition. It is useful for critical failures, often together with a rollback or error result.
* **`CONTINUE HANDLER`:** Handles the condition and then continues with the next statement after the one that raised it. It is especially useful for cursor end-of-data flags.

### Common Conditions
* `SQLWARNING`: warning conditions.
* `NOT FOUND`: commonly used for cursor exhaustion or no-data situations.
* `SQLEXCEPTION`: SQL errors not classified as warnings or `NOT FOUND`.
* Specific `SQLSTATE`: catches a particular condition.

## 5. Raising and Re-Throwing Errors

### `SIGNAL`
`SIGNAL` raises a new condition and can expose a clear message to the caller.

```sql
SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Custom Error Message';
```

### `RESIGNAL`
`RESIGNAL` is used inside exception handling to propagate an error after performing local handling such as logging or cleanup.

## 6. SQLSTATE Codes

SQLSTATE uses five-character condition codes. Common examples include:

| SQLSTATE | Meaning / Typical Use |
| :--- | :--- |
| `00000` | Success |
| `01000` | General warning |
| `02000` | No data / not found |
| `23000` | Integrity constraint violation |
| `45000` | Generic user-defined exception |

The exact vendor error code and behavior may provide more detail than the SQLSTATE class alone.

## 7. Robust Transaction + Handler Pattern

```sql
BEGIN
    DECLARE exit_flag INT DEFAULT 0;

    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        SET exit_flag = 1;

    START TRANSACTION;

    UPDATE accounts ...;

    IF exit_flag = 1 THEN
        ROLLBACK;
        SELECT 'Transaction Failed';
    ELSE
        COMMIT;
        SELECT 'Success';
    END IF;
END;
```

The exact handler architecture is DBMS-specific, but the general pattern is to make the failure state explicit, stop subsequent business logic when necessary, and ensure the transaction does not leave partial work committed.

## 8. Typical Sources of Errors

1. **Constraint violations:** duplicate primary keys, invalid foreign keys, failed checks.
2. **Data errors:** division by zero, invalid conversions, invalid dates or numeric values.
3. **Business errors:** domain rules implemented by the application or procedure, such as an insufficient account balance.
