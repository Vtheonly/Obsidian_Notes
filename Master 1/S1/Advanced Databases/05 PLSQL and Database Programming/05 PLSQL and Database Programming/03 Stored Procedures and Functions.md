###  Sources
*   *Based on Images: 6, 11*

### 1. Stored Procedures
A block of code saved in the database that can encapsulate business logic.

**Parameters:**
1.  **`IN`:** Pass data **into** the procedure. (Default).
2.  **`OUT`:** The procedure sends data **back** to the caller.
3.  **`INOUT`:** The variable is passed in, modified, and sent back.

**Syntax:**
```sql
DELIMITER //  -- Change delimiter so ; doesn't end the creation early

CREATE PROCEDURE ProcessOrder (IN orderId INT, OUT total DECIMAL(10,2))
BEGIN
    SELECT SUM(price) INTO total 
    FROM order_items 
    WHERE order_id = orderId;
END //

DELIMITER ;
```

**Calling it:**
```sql
CALL ProcessOrder(101, @myTotal);
SELECT @myTotal;
```

---

### 2. SQL Functions (UDF)
Unlike procedures, functions **must** return a single value and can be used inline in SQL (`SELECT MyFunc(col)...`).

**Deterministic vs. Non-Deterministic:**
*   **DETERMINISTIC:** Same Input = Same Output. (e.g., `SQRT(4)` is always 2).
*   **NOT DETERMINISTIC:** Output varies. (e.g., `NOW()` changes every second, `RAND()` changes every call).

#### The Binary Log Problem (Replication)
If you use **Non-Deterministic** functions in an `INSERT`/`UPDATE`, and that query is replicated to a Slave server:
*   The Master might generate `RAND() = 0.5`.
*   The Slave might generate `RAND() = 0.9`.
*   **Result:** Data inconsistency.

**Solution:**
1.  Mark functions as `DETERMINISTIC` if they are.
2.  If you must use non-deterministic logic, enable `SET GLOBAL log_bin_trust_function_creators = 1;` in MySQL to bypass the safety check (use with caution).

---