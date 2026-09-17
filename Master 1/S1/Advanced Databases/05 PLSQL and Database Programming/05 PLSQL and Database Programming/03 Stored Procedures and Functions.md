### Sources
* *Based on Images: 6, 11*

# Stored Procedures and Functions

## 1. Stored Procedures
A block of code saved in the database that can encapsulate reusable business logic.

**Parameters:**
1. **`IN`:** Pass data **into** the procedure. This is the default mode.
2. **`OUT`:** The procedure sends data **back** to the caller.
3. **`INOUT`:** The parameter is passed in, modified, and returned.

**Syntax:**
```sql
DELIMITER //

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

## 2. SQL Functions (UDF)
Unlike procedures, functions **return a single scalar value** and can be used inline in SQL in DBMSs that support stored functions in that context.

**Syntax:**
```sql
CREATE FUNCTION myFunc(p_id INT) RETURNS INT
BEGIN
    RETURN p_id * 10;
END
```

### Deterministic vs. Non-Deterministic
* **`DETERMINISTIC`:** The same input under the same relevant database state produces the same result. A pure mathematical function such as `SQRT(4)` is deterministic.
* **`NOT DETERMINISTIC`:** The result can vary between calls, for example `NOW()` or `RAND()`.

### SQL Data-Access Classifications
MySQL-style routine declarations can also describe how a routine interacts with data:

* `NO SQL`: contains no SQL data access.
* `CONTAINS SQL`: contains SQL statements but does not read or modify SQL data in the declared sense.
* `READS SQL DATA`: reads database data.
* `MODIFIES SQL DATA`: modifies database data.

The exact restrictions and required declarations depend on the DBMS and configuration.

## 3. Function Restrictions and Result Handling

A stored function is intended to return a scalar result through `RETURN`. A procedure is generally preferred when the operation needs multiple `OUT`/`INOUT` outputs, result sets, or complex transactional work.

A query such as:

```sql
SELECT * FROM Employees;
```

is not the same as:

```sql
SELECT COUNT(*) INTO v_count FROM Employees;
```

The first produces a result set, whereas the second assigns one scalar value to a variable. Whether a stored function can execute particular SQL statements or return result sets is DBMS-specific, so do not generalize a restriction from one procedural engine to all others.

## 4. Determinism and Binary Logging / Replication

In MySQL, stored functions used while binary logging is enabled are subject to additional safety checks because a function that produces different results on different servers can lead to replication divergence.

For example, a non-deterministic operation may produce different results if independently evaluated on source and replica servers. MySQL therefore requires routine characteristics and, depending on server settings and operation, may raise an error such as **Error 1418** when a function does not declare appropriate characteristics.

Typical approaches are:

1. Accurately declare a routine `DETERMINISTIC` only when it really is deterministic.
2. Use an appropriate SQL-data-access characteristic such as `READS SQL DATA` when applicable.
3. Administratively configure `log_bin_trust_function_creators` when the deployment explicitly accepts the associated trust trade-off.

Never mark a non-deterministic or data-modifying routine as deterministic merely to bypass a warning.
