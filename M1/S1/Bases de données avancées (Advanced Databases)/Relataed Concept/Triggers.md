# Master Class: Database Triggers (Déclencheurs)

**Course Context:** Bases de Données Avancées (Master 1)
**Sources:** *Source 20 (SQL Procedural), Source 18 (Gestion de l'intégrité), Source 15 (Corrigé TD4)*

---

## Part 1: Theoretical Foundations

### 1.1 What is a Trigger?
According to **Source 18 (Slide 43)** and **Source 20 (Section 4.1)**, a Trigger (Déclencheur) is a specialized stored procedure that is **automatically executed** (fired) by the DBMS in response to a specific event on a table.

Unlike standard procedures, **you never call a trigger manually**. It waits for an event to happen.

### 1.2 The Event Model (ECA Rule)
Triggers follow the **Event-Condition-Action** logic:
1.  **Event:** A modification command: `INSERT`, `UPDATE`, or `DELETE`.
2.  **Timing:** When to fire? `BEFORE` the modification hits the disk, or `AFTER` it is confirmed.
3.  **Action:** The SQL code to execute (validation, auditing, calculation).

### 1.3 Key Variables: `NEW` and `OLD`
Inside a trigger, you have access to two "pseudo-rows" that hold the data involved in the transaction (**Source 20, Section 4.4**):

| Pseudo-row | Description | Available In |
| :--- | :--- | :--- |
| **`NEW`** | The new version of the row being inserted or updated. | `INSERT`, `UPDATE` |
| **`OLD`** | The original version of the row before modification. | `UPDATE`, `DELETE` |

> [!TIP] Access Syntax
> You access columns using dot notation: `NEW.column_name` or `OLD.column_name`.

---

## Part 2: Syntax and Creation

### 2.1 The Standard Structure
Based on **Source 20 (Section 4.4)**:

```sql
CREATE TRIGGER TriggerName
{ BEFORE | AFTER } { INSERT | UPDATE | DELETE }
ON TableName
FOR EACH ROW
BEGIN
    -- Business Logic
    -- Use NEW.col and OLD.col here
END;
```

### 2.2 BEFORE vs. AFTER
*   **BEFORE:**
    *   Fires *before* the integrity checks and the physical write.
    *   **Use case:** Data validation, data cleaning (formatting), blocking invalid transactions.
    *   *Power:* You can change `NEW.value` here to fix data silently.
*   **AFTER:**
    *   Fires *after* the operation is successful.
    *   **Use case:** Logging (Audit), updating related tables (denormalization), cascading changes.
    *   *Limitation:* You cannot change `NEW.value` here (it's already written).

---

## Part 3: Use Cases & Scenarios (Dynamic Integrity)

**Source 18 (Slide 41)** defines triggers as "Dynamic Integrity Constraints". They are used where static constraints (like `CHECK` or `FOREIGN KEY`) are not enough.

### 3.1 Complex Validation
*   *Static:* `CHECK (age > 18)`
*   *Dynamic (Trigger):* "A pilot cannot be promoted to 'Captain' unless they have flown 1000 hours." (Requires logic).

### 3.2 Denormalization Maintenance
*   If you store a `Total_Sales` column in a `Store` table (for performance), you need a trigger on the `Sales` table to update that total every time a sale is made.

### 3.3 Auditing
*   Recording who changed what and when into a `Logs` table.

---

## Part 4: Solved Exercises (Deep Dive)

The following exercises are from **TD N°4 (MySQL Procedural)** and demonstrate advanced trigger logic.

**Context Schema:**
*   `Pilote (brevet, nom, nbHVol, comp, nbqualif, grade)`
*   `Qualifications (brevet, typa, dateexpiration)`

### Exercise 7: Automatic Counter Decrement (`AFTER DELETE`)
**Scenario:** The table `Pilote` has a column `nbqualif` which stores the count of qualifications a pilot holds. We must ensure this number stays accurate when a qualification is deleted.

**Solution:**
```sql
DELIMITER $

CREATE TRIGGER TrigDelQualif
AFTER DELETE ON Qualifications
FOR EACH ROW
BEGIN
    -- Logic: Find the pilot who owned this qualification and decrease their count
    UPDATE Pilote 
    SET nbqualif = nbqualif - 1
    WHERE brevet = OLD.brevet;
END $

DELIMITER ;
```
**Reasoning:**
1.  **Timing:** `AFTER` is appropriate because we only want to update the count if the deletion actually succeeded.
2.  **Event:** `DELETE`.
3.  **Reference:** We use `OLD.brevet` because the row in `Qualifications` is being removed; we need the ID that *used* to be there.

---

### Exercise 8: Automatic Counter Increment (`AFTER INSERT`)
**Scenario:** Conversely, when a new qualification is added, the pilot's count must increase.

**Solution:**
```sql
DELIMITER $

CREATE TRIGGER TrigInsQualif
AFTER INSERT ON Qualifications
FOR EACH ROW
BEGIN
    UPDATE Pilote 
    SET nbqualif = nbqualif + 1
    WHERE brevet = NEW.brevet;
END $

DELIMITER ;
```
**Reasoning:**
1.  **Reference:** We use `NEW.brevet` because this is the pilot ID associated with the newly inserted row.

---

### Exercise 9: Handling Updates (`AFTER UPDATE`)
**Scenario:** What if a qualification is transferred? (e.g., The `brevet` ID in the `Qualifications` table is changed from Pilot A to Pilot B).

**Solution:**
```sql
DELIMITER $

CREATE TRIGGER TrigUpdQualif
AFTER UPDATE ON Qualifications
FOR EACH ROW
BEGIN
    -- 1. Remove from the old pilot
    UPDATE Pilote 
    SET nbqualif = nbqualif - 1
    WHERE brevet = OLD.brevet;

    -- 2. Add to the new pilot
    UPDATE Pilote 
    SET nbqualif = nbqualif + 1
    WHERE brevet = NEW.brevet;
END $

DELIMITER ;
```
**Reasoning:**
*   An `UPDATE` is conceptually a DELETE of the old state and an INSERT of the new state.
*   If `OLD.brevet` is the same as `NEW.brevet`, the count performs `-1` then `+1`, resulting in no change (correct).
*   If they are different, the counts are adjusted correctly for both pilots.

---

### Exercise 10: Complex Data Correction (`BEFORE INSERT`)
**Scenario:** Enforce strict business rules for Pilot Grades based on flight hours (`nbHVol`).
*   **Rules:**
    *   `CDB`: Must have 1000-4000 hours.
    *   `COPI`: Must have 100-1000 hours.
    *   `INST`: Must have > 3000 hours.
*   **Requirement:** If the data inserted is invalid (e.g., a novice listed as 'CDB'), force the grade to `NULL` (or correct it) instead of crashing.

**Solution:**
```sql
DELIMITER $

CREATE TRIGGER TrigInsGrade
BEFORE INSERT ON Pilote
FOR EACH ROW
BEGIN
    -- Rule 1: Validate Commander (CDB)
    IF NEW.grade = 'CDB' AND (NEW.nbHVol NOT BETWEEN 1000 AND 4000) THEN
        SET NEW.grade = NULL; 
        -- Logic: "You claimed to be CDB but don't have the hours. Rejected."
    END IF;

    -- Rule 2: Validate Copilot (COPI)
    IF NEW.grade = 'COPI' AND (NEW.nbHVol NOT BETWEEN 100 AND 1000) THEN
        SET NEW.grade = NULL;
    END IF;

    -- Rule 3: Validate Instructor (INST)
    IF NEW.grade = 'INST' AND NEW.nbHVol < 3000 THEN
        SET NEW.grade = NULL;
    END IF;
END $

DELIMITER ;
```
**Reasoning:**
*   **Timing:** Must be `BEFORE`. We need to intercept the data (`NEW.grade`) and modify it *before* it is written to the database.
*   **Action:** Using `SET NEW.col = val` modifies the data in-flight.

---

### Exercise 11: Blocking Transactions (`SIGNAL SQLSTATE`)
**Scenario:** A pilot cannot have more than 3 qualifications. If a user tries to insert a 4th, block the transaction.

**Modern Solution (MySQL 5.5+):**
```sql
DELIMITER $

CREATE TRIGGER CheckMaxQualif
BEFORE INSERT ON Qualifications
FOR EACH ROW
BEGIN
    DECLARE current_count INT;

    -- Check current status
    SELECT nbqualif INTO current_count 
    FROM Pilote 
    WHERE brevet = NEW.brevet;

    -- Logic
    IF current_count >= 3 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Error: This pilot already has 3 qualifications.';
    END IF;
END $

DELIMITER ;
```

**Legacy Solution (Workaround for Older MySQL):**
*From Source 15 (Correction TD4)*
If `SIGNAL` is not available, you must force a standard SQL error, like inserting NULL into a NOT NULL column.
```sql
-- Inside Trigger Body
IF current_count >= 3 THEN
    -- Create a dummy table called 'Trace' with a non-null column
    INSERT INTO TRACE VALUES (NULL); 
    -- This causes a crash, rolling back the transaction.
END IF;
```

---

## Part 5: Managing Triggers

### 5.1 Dropping Triggers
```sql
DROP TRIGGER IF EXISTS TriggerName;
```
> [!NOTE] Dependency
> According to **Source 20**, if you drop a table, all associated triggers are automatically deleted.

### 5.2 Restrictions
1.  **No Transactions:** You cannot explicitly use `START TRANSACTION`, `COMMIT`, or `ROLLBACK` inside a trigger. The trigger becomes part of the transaction that fired it.
2.  **Recursion:** Be careful of updating the same table you are triggering on (Mutating Table Error), though MySQL handles some cases, infinite loops are possible (Update T1 -> Trigger Updates T1 -> Trigger Updates T1...).

---

## Summary Checklist for Exams

1.  **NEW vs OLD:**
    *   `INSERT`: Only **NEW**.
    *   `DELETE`: Only **OLD**.
    *   `UPDATE`: Both **NEW** and **OLD**.
2.  **Timing:**
    *   Use **BEFORE** to validate or modify data.
    *   Use **AFTER** to update *other* tables.
3.  **Blocking:** Use `SIGNAL SQLSTATE` to stop an operation.
4.  **Syntax:** Always remember `FOR EACH ROW`.
