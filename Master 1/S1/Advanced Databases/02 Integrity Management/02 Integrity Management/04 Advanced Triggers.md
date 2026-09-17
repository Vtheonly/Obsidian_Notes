# Master Class: Database Triggers (Déclencheurs)

**Course Context:** Bases de Données Avancées (Master 1)
**Sources:** *Source 20 (SQL Procedural), Source 18 (Gestion de l'intégrité), Source 15 (Corrigé TD4)*

---

## Part 1: Theoretical Foundations

### 1.1 What is a Trigger?
According to **Source 18 (Slide 43)** and **Source 20 (Section 4.1)**, a Trigger (Déclencheur) is a specialized stored procedure that is **automatically executed** by the DBMS in response to a specific event on a table.

Unlike a standard procedure, **you do not call a trigger manually**. It waits for its configured event.

### 1.2 The Event-Condition-Action Model
Triggers follow the **Event-Condition-Action (ECA)** logic:
1. **Event:** `INSERT`, `UPDATE`, or `DELETE` activates the trigger.
2. **Timing:** The trigger runs `BEFORE` or `AFTER` the data modification according to the DBMS semantics.
3. **Condition:** Optional logic determines whether the action should run.
4. **Action:** Procedural SQL performs validation, correction, auditing, or propagation.

### 1.3 Key Variables: `NEW` and `OLD`
Inside a row-level trigger, you have access to two pseudo-rows that hold the data involved in the modification:

| Pseudo-row | Description | Available In |
| :--- | :--- | :--- |
| **`NEW`** | The new version of the row being inserted or updated. | `INSERT`, `UPDATE` |
| **`OLD`** | The original version of the row before modification. | `UPDATE`, `DELETE` |

> [!TIP] Access Syntax
> Use dot notation such as `NEW.column_name` or `OLD.column_name`.

---

## Part 2: Syntax and Creation

### 2.1 Standard Row-Level Structure
```sql
CREATE TRIGGER TriggerName
{ BEFORE | AFTER } { INSERT | UPDATE | DELETE }
ON TableName
FOR EACH ROW
BEGIN
    -- Business Logic
END;
```

### 2.2 BEFORE vs. AFTER

* **BEFORE:** Used for validation, normalization, blocking an operation, or modifying incoming `NEW` values where the DBMS permits it.
* **AFTER:** Used after the modification succeeds, commonly for audit logging, maintaining counters, or updating related tables.

An `AFTER` trigger should not be presented as an editable stage for the already-written triggering row; exact mutability rules are DBMS-specific.

---

## Part 3: Use Cases & Scenarios (Dynamic Integrity)

Triggers are useful when ordinary static constraints are not enough, especially for state-dependent or cross-table rules.

### 3.1 Complex Validation
* *Static:* `CHECK (age > 18)`
* *Dynamic:* "A pilot cannot be promoted to 'Captain' unless they have flown 1000 hours."

### 3.2 Denormalization Maintenance
A trigger can maintain a cached aggregate such as `Total_Sales` or a qualification counter in another table after the underlying child rows change.

### 3.3 Auditing
A trigger can record who changed what and when in an audit table.

### 3.4 Emulating a Cross-Table Foreign-Key Rule
If a target DBMS does not provide a native foreign key for a particular situation, a trigger can check that a referenced parent exists and reject the child write when it does not:

```sql
CREATE TRIGGER Check_Customer_Exists
BEFORE INSERT ON Orders
FOR EACH ROW
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM Customers WHERE ID = NEW.CustomerID
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Referenced customer does not exist';
    END IF;
END;
```

> [!IMPORTANT]
> When a native foreign key can express the rule, prefer the declarative foreign key because the DBMS can enforce and optimize it as a schema-level integrity constraint. Trigger-based emulation is mainly useful when the rule cannot be represented directly or the engine lacks the required feature.

---

## Part 4: Solved Exercises (Deep Dive)

**Context Schema:**
* `Pilote (brevet, nom, nbHVol, comp, nbqualif, grade)`
* `Qualifications (brevet, typa, dateexpiration)`

### Exercise 7: Automatic Counter Decrement (`AFTER DELETE`)

```sql
DELIMITER $

CREATE TRIGGER TrigDelQualif
AFTER DELETE ON Qualifications
FOR EACH ROW
BEGIN
    UPDATE Pilote
    SET nbqualif = COALESCE(nbqualif, 1) - 1
    WHERE brevet = OLD.brevet;
END $

DELIMITER ;
```

**Reasoning:**
1. `AFTER DELETE` updates the count only after the deletion succeeds.
2. `OLD.brevet` identifies the pilot that owned the deleted qualification.
3. `COALESCE(nbqualif, 1)` illustrates defensive handling when the stored counter is unexpectedly `NULL`; in a well-designed schema, the counter should normally be `NOT NULL`.

### Exercise 8: Automatic Counter Increment (`AFTER INSERT`)

```sql
DELIMITER $

CREATE TRIGGER TrigInsQualif
AFTER INSERT ON Qualifications
FOR EACH ROW
BEGIN
    UPDATE Pilote
    SET nbqualif = COALESCE(nbqualif, 0) + 1
    WHERE brevet = NEW.brevet;
END $

DELIMITER ;
```

Use `NEW.brevet` because the new qualification row contains the pilot identifier.

### Exercise 9: Handling Updates (`AFTER UPDATE`)

When a qualification is transferred from Pilot A to Pilot B, adjust both counters. If another column such as `dateexpiration` changes but `brevet` does not, no counter adjustment is needed.

```sql
DELIMITER $

CREATE TRIGGER TrigUpdQualif
AFTER UPDATE ON Qualifications
FOR EACH ROW
BEGIN
    IF OLD.brevet <> NEW.brevet THEN
        UPDATE Pilote
        SET nbqualif = COALESCE(nbqualif, 1) - 1
        WHERE brevet = OLD.brevet;

        UPDATE Pilote
        SET nbqualif = COALESCE(nbqualif, 0) + 1
        WHERE brevet = NEW.brevet;
    END IF;
END $

DELIMITER ;
```

If `OLD.brevet = NEW.brevet`, decrementing and incrementing the same pilot would produce no logical change but would create unnecessary writes. The explicit condition avoids that work.

### Exercise 10: Complex Data Correction (`BEFORE INSERT`)

Rules:
* `CDB`: 1000–4000 hours.
* `COPI`: 100–1000 hours.
* `INST`: at least 3000 hours.

A defensive trigger should also account explicitly for `NULL` flight hours because comparisons with `NULL` evaluate to `UNKNOWN`.

```sql
DELIMITER $

CREATE TRIGGER TrigInsGrade
BEFORE INSERT ON Pilote
FOR EACH ROW
BEGIN
    IF NEW.grade = 'CDB' AND (
        NEW.nbHVol IS NULL OR NEW.nbHVol < 1000 OR NEW.nbHVol > 4000
    ) THEN
        SET NEW.grade = NULL;
    END IF;

    IF NEW.grade = 'COPI' AND (
        NEW.nbHVol IS NULL OR NEW.nbHVol < 100 OR NEW.nbHVol > 1000
    ) THEN
        SET NEW.grade = NULL;
    END IF;

    IF NEW.grade = 'INST' AND (
        NEW.nbHVol IS NULL OR NEW.nbHVol < 3000
    ) THEN
        SET NEW.grade = NULL;
    END IF;
END $

DELIMITER ;
```

### Exercise 11: Blocking Transactions (`SIGNAL SQLSTATE`)

```sql
DELIMITER $

CREATE TRIGGER CheckMaxQualif
BEFORE INSERT ON Qualifications
FOR EACH ROW
BEGIN
    DECLARE current_count INT DEFAULT 0;

    SELECT COALESCE(nbqualif, 0) INTO current_count
    FROM Pilote
    WHERE brevet = NEW.brevet;

    IF current_count >= 3 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Error: This pilot already has 3 qualifications.';
    END IF;
END $

DELIMITER ;
```

### Legacy Workaround
Older engines without `SIGNAL` sometimes used an intentional constraint violation to force the statement to fail, for example inserting `NULL` into a known `NOT NULL` column of a dedicated dummy/error table. The table and column must actually exist; using a nonexistent object simply produces a different database error and is not a clean demonstration of the pattern.

---

## Part 5: Managing Triggers

### 5.1 Dropping Triggers
```sql
DROP TRIGGER IF EXISTS TriggerName;
```

> [!NOTE] Dependency
> Dropping a table may also remove associated triggers according to the DBMS's dependency rules.

### 5.2 Restrictions
1. **No explicit transaction boundary:** A trigger executes within the transaction that fired it; explicit `START TRANSACTION`, `COMMIT`, and `ROLLBACK` are prohibited in many procedural trigger implementations.
2. **Recursion/Cascades:** Trigger A may modify a table that fires Trigger B. Long chains are difficult to debug and maintain.
3. **Self-referencing tables:** Some DBMSs restrict querying or changing the table currently undergoing a row-level trigger. Exact restrictions are engine-specific.
4. **Performance:** Trigger logic is synchronous with the original operation, so expensive work increases the latency of the triggering statement.

---

## Summary Checklist for Exams

1. **`NEW` vs `OLD`:** `INSERT` → `NEW`; `DELETE` → `OLD`; `UPDATE` → both.
2. **Timing:** Use `BEFORE` when validation/correction must happen before the write; use `AFTER` when logic depends on a successful modification.
3. **Row scope:** `FOR EACH ROW` executes once per affected row.
4. **Blocking:** `SIGNAL SQLSTATE '45000'` can abort a user-defined condition in MySQL-style procedural SQL.
5. **Avoid unnecessary writes:** Compare `OLD` and `NEW` before maintaining derived counters.
6. **Prefer native constraints:** Use a foreign key instead of trigger emulation when the DBMS can express the relationship declaratively.
