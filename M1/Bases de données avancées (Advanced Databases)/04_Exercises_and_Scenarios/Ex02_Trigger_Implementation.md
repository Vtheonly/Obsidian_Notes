
# Exercise 2: Implementing Business Logic with Triggers

## Scenario A: The "Freezing" Account
**Goal:** We have a table `Accounts` (ID, Balance, Status). If the status is 'FROZEN', no money can be withdrawn (Balance cannot decrease).

**Analysis:**
1.  **Operation:** `UPDATE` on Accounts.
2.  **Timing:** `BEFORE` (We want to prevent the change).
3.  **Condition:** `NEW.Balance < OLD.Balance` AND `OLD.Status = 'FROZEN'`.

**SQL Solution:**
```sql
CREATE TRIGGER Block_Frozen_Withdrawal
BEFORE UPDATE ON Accounts
FOR EACH ROW
BEGIN
    -- Check if money is leaving AND account is frozen
    IF NEW.Balance < OLD.Balance AND OLD.Status = 'FROZEN' THEN
       SIGNAL SQLSTATE '45000' 
       SET MESSAGE_TEXT = 'Cannot withdraw from a frozen account.';
    END IF;
END;
```

---

## Scenario B: Automatic Audit Log
**Goal:** Every time an employee's salary is changed, save the old salary, new salary, and date into a table `Salary_History`.

**Analysis:**
1.  **Operation:** `UPDATE` on Employees.
2.  **Timing:** `AFTER` (The change is valid, now we record it).
3.  **Condition:** Only if `NEW.Salary != OLD.Salary`.

**SQL Solution:**
```sql
CREATE TRIGGER Audit_Salary_Change
AFTER UPDATE ON Employees
FOR EACH ROW
BEGIN
    IF NEW.Salary <> OLD.Salary THEN
        INSERT INTO Salary_History (Emp_ID, Old_Sal, New_Sal, Change_Date)
        VALUES (OLD.ID, OLD.Salary, NEW.Salary, NOW());
    END IF;
END;
```

## Essential Tip for Exams
*   Always check if the value *actually changed* (`IF NEW <> OLD`). Otherwise, "dummy updates" (updating a row with same values) will fill up your log table with useless duplicates.
