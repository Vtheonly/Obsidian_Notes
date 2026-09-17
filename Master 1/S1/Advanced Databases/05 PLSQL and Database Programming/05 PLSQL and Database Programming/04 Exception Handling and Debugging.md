###  Sources
*   *Based on Images: 7, 9*

### 1. Sources of Errors
1.  **Constraint Violations:** Duplicate Primary Key, Foreign Key mismatch.
2.  **Data Errors:** Division by zero, Invalid type conversion.
3.  **Logical/Business Errors:** "Balance insufficient" (defined by your code).

### 2. Declaring Handlers
You can define what the procedure does when an error occurs.

**Syntax:**
```sql
DECLARE [Action] HANDLER FOR [Condition] [Statement];
```

**Actions:**
*   **`CONTINUE`:** Log the error or set a flag, but continue executing the next line of code.
*   **`EXIT`:** Stop the procedure immediately (and perhaps Rollback).

**Conditions:**
*   `SQLWARNING`: Catches warnings (01...).
*   `NOT FOUND`: Catches cursor ends (02...).
*   `SQLEXCEPTION`: Catches errors (>02...).
*   `SQLSTATE 'xxxxx'`: Catches a specific error code.

### 3. Raising Errors (`SIGNAL`)
You can stop execution and throw a custom error to the application.

*   **`SIGNAL`:** Raises a new error.
    ```sql
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Custom Error Message';
    ```
*   **`RESIGNAL`:** Used inside a Handler. It catches an error, does something (like logging), and then throws the error again so the caller knows it failed.

### 4. SQLSTATE Codes
Standardized 5-character codes.
*   `00000`: Success.
*   `01000`: General Warning.
*   `02000`: Not Found (No data).
*   `23000`: Integrity Constraint Violation (Duplicate Key).
*   `45000`: Generic User-Defined Exception (Used for `SIGNAL`).

> [!PRO TIP] Procedure Structure with Handlers
> Always declare handlers at the *top* of your `BEGIN...END` block, after variable declarations but before any logic.

```sql
BEGIN
    DECLARE exit_flag INT DEFAULT 0;
    
    -- 1. Declare Variables
    -- 2. Declare Handlers
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET exit_flag = 1;
    
    -- 3. Start Transaction
    START TRANSACTION;
    
    -- 4. Logic
    UPDATE accounts...;
    
    -- 5. Check Errors
    IF exit_flag = 1 THEN
        ROLLBACK;
        SELECT 'Transaction Failed';
    ELSE
        COMMIT;
        SELECT 'Success';
    END IF;
END;
```