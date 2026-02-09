
**Context Schema:**
*   `Compagnie (comp, nrue, rue, ville, nomComp)`
*   `Pilote (brevet, nom, nbHVol, comp, nbqualif, grade)`
*   `TypeAvion (typa, nomtype)`
*   `Qualifications (brevet, typa, dateexpiration)`

---

### Exercise 1: Function `EffectifsHeure`

**Source:** TD N°4 BDA : MySQL Procédural - Exercice 1
**Question:** Write a function `EffectifsHeure(comp, heures)` that returns the number of pilots for a given company who have more flight hours than the parameter. If `comp` is NULL, count across all companies.

#### 1. Solution
```sql
DELIMITER $

CREATE FUNCTION EffectifsHeure(
    pcomp VARCHAR(4),
    pheuresVol DECIMAL(7,2)
) 
RETURNS SMALLINT
DETERMINISTIC -- Added for MySQL strict mode compatibility
READS SQL DATA
BEGIN
    DECLARE resultat SMALLINT;

    IF (pcomp IS NULL) THEN
        SELECT COUNT(*) INTO resultat 
        FROM Pilote 
        WHERE nbHVol > pheuresVol;
    ELSE
        SELECT COUNT(*) INTO resultat 
        FROM Pilote 
        WHERE nbHVol > pheuresVol
          AND comp = pcomp;
    END IF;

    RETURN resultat;
END $

DELIMITER ;
```

#### 2. Reasoning
*   **Function vs Procedure:** The requirement asks to "return" a value based on calculation, which fits a scalar **Function**.
*   **Conditional Logic:** We need an `IF` block to handle the specific case where the company parameter is `NULL`.
*   **`SELECT ... INTO`**: This is the standard way to store a query result into a variable inside a block.

#### 3. Detailed Explanation
*   **`DELIMITER $`**: Standard SQL uses `;` to end statements. Inside a function body, we use `;` for individual lines. To tell MySQL "don't run this yet, wait for the end", we change the delimiter to `$` (or `//`).
*   **Parameters:** Defined as `IN` by default for functions.
*   **`DETERMINISTIC` / `READS SQL DATA`**: In newer MySQL versions, you must declare the nature of the function for binary logging safety. `READS SQL DATA` tells the engine this function queries tables but doesn't modify them.
*   **Usage:** You can call this in a SELECT statement: `SELECT EffectifsHeure('AF', 500);`.

---

### Exercise 2: Procedure `PlusExperimente`

**Source:** TD N°4 BDA : MySQL Procédural - Exercice 2
**Question:** Write a procedure `PlusExperimente(comp, nom, heures)` that returns (via OUT parameters) the name and hours of the most experienced pilot for a company. If `comp` is NULL, find the most experienced pilot overall and return their name and *company code*.

#### 1. Solution
```sql
DELIMITER $

CREATE PROCEDURE PlusExperimente(
    INOUT pcomp VARCHAR(4),
    OUT pnom VARCHAR(15),
    OUT pheuresVol DECIMAL(7,2)
)
BEGIN
    -- Case 1: A specific company is provided
    IF (pcomp IS NOT NULL) THEN
        SELECT nom, nbHVol INTO pnom, pheuresVol
        FROM Pilote
        WHERE comp = pcomp
        ORDER BY nbHVol DESC
        LIMIT 1;
    
    -- Case 2: No company provided (NULL)
    ELSE
        SELECT nom, nbHVol, comp INTO pnom, pheuresVol, pcomp
        FROM Pilote
        ORDER BY nbHVol DESC
        LIMIT 1;
    END IF;
END $

DELIMITER ;
```

#### 2. Reasoning
*   **INOUT Parameter:** `pcomp` is used as an input filter, but in the second case (NULL), it must calculate the company of the best pilot and return it. Thus, it must be `INOUT`.
*   **Ordering:** To find the "most experienced", we sort by `nbHVol DESC` and take the first row (`LIMIT 1`).

#### 3. Detailed Explanation
*   **Why a Procedure?** Unlike functions, procedures can return multiple values via `OUT` parameters.
*   **Error Handling (Implicit):** The exercise mentions "If multiple pilots have the same experience, show an error". In standard SQL without specific handlers, `SELECT INTO` failing (too many rows) or `LIMIT 1` handles the retrieval. To explicitly throw an error for duplicates, we would need to check `COUNT(*)` first. The solution provided assumes `LIMIT 1` is sufficient to pick *one* winner.

---

### Exercise 4: Recursive Factorial (Limitations)

**Source:** TD N°4 BDA : MySQL Procédural - Exercice 4
**Question:** Write a recursive SQL function to calculate the factorial of `n`. Test it.

#### 1. Solution
```sql
DELIMITER $

CREATE FUNCTION factorielle(n INT) RETURNS INT
NO SQL
BEGIN
    IF n <= 1 THEN
        RETURN 1;
    ELSE
        RETURN n * factorielle(n - 1);
    END IF;
END $

DELIMITER ;

-- Test
SELECT factorielle(5);
```

#### 2. Reasoning
The logic is standard recursion: $n! = n \times (n-1)!$, with a base case of $1! = 1$.

#### 3. Detailed Explanation
*   **MySQL Limitation:** Historically (and in the version context of this TD, likely MySQL 5.0/5.1), **Stored Functions could not be recursive**. Attempting to call `factorielle` inside `factorielle` would trigger: `ERROR 1424 (HY000): Recursive stored routines are not allowed`.
*   **Modern MySQL (8.0+):** Recursive Common Table Expressions (CTEs) or setting `max_sp_recursion_depth` allows recursion in *procedures*, but functions remain restricted in many configurations. The correction notes this limitation explicitly.

---

### Exercise 5: Cursors (Sum of Hours)

**Source:** TD N°4 BDA : MySQL Procédural - Exercice 5
**Question:** Write a procedure calculating the sum of flight hours for all pilots of company 'AF' using a **cursor**.

#### 1. Solution
```sql
DELIMITER $

CREATE PROCEDURE total_hvol_AF()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_nbHv DECIMAL(7,2);
    DECLARE v_tot DECIMAL(8,2) DEFAULT 0;
    
    -- 1. Declare Cursor
    DECLARE curs1 CURSOR FOR 
        SELECT nbHVol FROM Pilote WHERE comp = 'AF';
        
    -- 2. Declare Handler for End of Data
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- 3. Open Cursor
    OPEN curs1;

    -- 4. Loop
    read_loop: LOOP
        FETCH curs1 INTO v_nbHv;
        
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        SET v_tot = v_tot + v_nbHv;
    END LOOP;

    -- 5. Close Cursor
    CLOSE curs1;

    -- 6. Display Result
    SELECT v_tot AS 'Total Heures AF';
END $

DELIMITER ;
```

#### 2. Reasoning
A cursor allows row-by-row processing.
1.  **Declare:** Define the query (`SELECT nbHVol...`).
2.  **Handler:** Define what happens when the cursor runs out of rows (SQLSTATE '02000' / NOT FOUND).
3.  **Fetch:** Grab the current row's value into a variable.
4.  **Accumulate:** Add to `v_tot`.

#### 3. Detailed Explanation
*   **`DECLARE` Order:** In MySQL, variables must be declared *before* cursors, and cursors *before* handlers. Violating this order causes syntax errors.
*   **The Loop:** The `FETCH` moves the pointer. When it tries to fetch past the last row, the `NOT FOUND` handler fires, setting `done = TRUE`, triggering the `LEAVE` command.

---

### Exercise 6: Cursor for Updates

**Source:** TD N°4 BDA : MySQL Procédural - Exercice 6
**Question:** Use a cursor to:
1.  Add 100 hours to 'AF' pilots.
2.  Remove 100 hours from 'SING' pilots.
3.  Delete pilots from other companies.
**Requirement:** Use **Row Locking**.

#### 1. Solution
```sql
DELIMITER $

CREATE PROCEDURE Gestion_Pilotes_Curs()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_brevet VARCHAR(6);
    DECLARE v_comp VARCHAR(4);
    
    -- Declare cursor with FOR UPDATE to lock rows
    DECLARE cur_pilote CURSOR FOR 
        SELECT brevet, comp FROM Pilote FOR UPDATE;
        
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur_pilote;

    read_loop: LOOP
        FETCH cur_pilote INTO v_brevet, v_comp;
        
        IF done THEN
            LEAVE read_loop;
        END IF;

        IF v_comp = 'AF' THEN
            UPDATE Pilote SET nbHVol = nbHVol + 100 WHERE brevet = v_brevet;
        ELSEIF v_comp = 'SING' THEN
            UPDATE Pilote SET nbHVol = nbHVol - 100 WHERE brevet = v_brevet;
        ELSE
            DELETE FROM Pilote WHERE brevet = v_brevet;
        END IF;
        
    END LOOP;

    CLOSE cur_pilote;
    COMMIT; -- Commit transaction to release locks
END $

DELIMITER ;
```

#### 2. Reasoning
*   **`FOR UPDATE`**: This clause in the cursor declaration locks the selected rows. Other transactions cannot modify them until this transaction commits.
*   **Logic:** We iterate through every pilot, check their company variable, and execute the corresponding DML (`UPDATE` or `DELETE`) using the primary key (`brevet`).

#### 3. Detailed Explanation
*   **Performance Note:** Doing updates row-by-row (RBAR - Row By Agonizing Row) is generally slower than set-based SQL (e.g., `UPDATE Pilote SET ... WHERE comp='AF'`). Cursors are used here for educational purposes to demonstrate procedural logic and locking.
*   **Safety:** The `FOR UPDATE` ensures data consistency. If another process tried to delete an 'AF' pilot while this procedure was running, it would wait.

---

### Exercise 7: Trigger `TrigDelQualif`

**Source:** TD N°4 BDA : MySQL Procédural - Exercice 7
**Question:** When a qualification is deleted, decrement the `nbqualif` counter in the `Pilote` table for the corresponding pilot.

#### 1. Solution
```sql
DELIMITER $

CREATE TRIGGER TrigDelQualif
AFTER DELETE ON Qualifications
FOR EACH ROW
BEGIN
    UPDATE Pilote 
    SET nbqualif = nbqualif - 1
    WHERE brevet = OLD.brevet;
END $

DELIMITER ;
```

#### 2. Reasoning
*   **Event:** `AFTER DELETE` on table `Qualifications`.
*   **Reference:** `OLD.brevet` refers to the pilot ID of the row that was just deleted.
*   **Action:** Simple arithmetic update on the parent table.

#### 3. Detailed Explanation
This is a classic **Denormalization Maintenance** trigger. The database stores a calculated value (`nbqualif`) physically in the `Pilote` table for performance (to avoid doing `COUNT(*)` every time). The trigger ensures this calculated value stays in sync with the actual data.

---

### Exercise 8: Trigger `TrigInsQualif`

**Source:** TD N°4 BDA : MySQL Procédural - Exercice 8
**Question:** When a qualification is inserted, increment the `nbqualif` counter.

#### 1. Solution
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

#### 2. Reasoning
*   **Event:** `AFTER INSERT`.
*   **Reference:** `NEW.brevet` refers to the new data being inserted.
*   **Action:** Increment counter.

---

### Exercise 9: Trigger `TrigUpdQualif`

**Source:** TD N°4 BDA : MySQL Procédural - Exercice 9
**Question:** Handle the update of a qualification (e.g., transferring a qualification from one pilot to another).

#### 1. Solution
```sql
DELIMITER $

CREATE TRIGGER TrigUpdQualif
AFTER UPDATE ON Qualifications
FOR EACH ROW
BEGIN
    -- Decrement for the old pilot
    UPDATE Pilote 
    SET nbqualif = nbqualif - 1
    WHERE brevet = OLD.brevet;

    -- Increment for the new pilot
    UPDATE Pilote 
    SET nbqualif = nbqualif + 1
    WHERE brevet = NEW.brevet;
END $

DELIMITER ;
```

#### 2. Reasoning
If we change the `brevet` in the `Qualifications` table (transferring the cert), the count must decrease for the old owner (`OLD.brevet`) and increase for the new owner (`NEW.brevet`).

#### 3. Detailed Explanation
*   If `OLD.brevet` is the same as `NEW.brevet` (e.g., just updating the expiration date), the database executes `+1` and `-1` on the same row, resulting in no net change, which is correct.

---

### Exercise 10: Complex Validation Trigger (`TrigInsGrade`)

**Source:** TD N°4 BDA : MySQL Procédural - Exercice 10
**Question:** Enforce business rules on pilot grades based on flight hours during insertion:
*   1000 - 4000 hours: Can be 'CDB' (Commandant de Bord).
*   100 - 1000 hours: Can be 'COPI' (Copilote).
*   > 3000 hours: Can be 'INST' (Instructeur).
*   Force the correct grade or set to NULL if invalid.

#### 1. Solution
```sql
DELIMITER $

CREATE TRIGGER TrigInsGrade
BEFORE INSERT ON Pilote
FOR EACH ROW
BEGIN
    -- Check CDB Rule
    IF NEW.grade = 'CDB' AND (NEW.nbHVol NOT BETWEEN 1000 AND 4000) THEN
        SET NEW.grade = NULL; -- Or force logic: SET NEW.grade = 'COPI';
    END IF;

    -- Check COPI Rule
    IF NEW.grade = 'COPI' AND (NEW.nbHVol NOT BETWEEN 100 AND 1000) THEN
        SET NEW.grade = NULL;
    END IF;

    -- Check INST Rule
    IF NEW.grade = 'INST' AND NEW.nbHVol < 3000 THEN
        SET NEW.grade = NULL;
    END IF;
    
    -- The correction suggests forcing values based on hours rather than rejecting:
    -- Example logic from correction:
    -- IF (NEW.grade = 'CDB' AND NEW.nbHVol < 1000) THEN SET NEW.grade = 'COPI'; END IF;
END $

DELIMITER ;
```

#### 2. Reasoning
*   **Event:** `BEFORE INSERT`. This allows us to modify the data (`SET NEW.grade = ...`) *before* it is written to the disk.
*   **Logic:** We compare the `NEW.nbHVol` and `NEW.grade` against the rules. If they contradict, we override the grade.

#### 3. Detailed Explanation
Using `BEFORE` triggers for data cleaning is a powerful feature. Instead of rejecting the transaction with an error, the database "fixes" the data to comply with business rules.

---

### Exercise 11: Max 3 Qualifications Constraint

**Source:** TD N°4 BDA : MySQL Procédural - Exercice 11
**Question:** Ensure a pilot cannot have more than 3 qualifications. Since MySQL Triggers can't easily stop a transaction with a custom error message in older versions (before SIGNAL), use a workaround or `SIGNAL`.

#### 1. Solution (Modern MySQL with SIGNAL)
```sql
DELIMITER $

CREATE TRIGGER CheckMaxQualif
BEFORE INSERT ON Qualifications
FOR EACH ROW
BEGIN
    DECLARE count_qualif INT;

    SELECT nbqualif INTO count_qualif 
    FROM Pilote 
    WHERE brevet = NEW.brevet;

    IF count_qualif >= 3 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Pilot already has 3 qualifications.';
    END IF;
END $

DELIMITER ;
```

#### 1. Solution (Old MySQL Workaround - from Correction)
*Create a dummy table `Trace` to force an error.*
```sql
-- Trigger body
IF v_compteur >= 3 THEN
    -- Attempt to insert NULL into a NOT NULL column or table
    INSERT INTO TRACE VALUES (NULL); -- This crashes the transaction
END IF;
```

#### 2. Reasoning
*   **Constraint:** The rule is "Max 3".
*   **Check:** We check the current count in `Pilote`.
*   **Action:** If count is 3, the new insert (making it 4) must be blocked.
*   **Blocking:** `SIGNAL SQLSTATE` throws an exception, rolling back the insert.

#### 3. Detailed Explanation
This effectively implements a complex constraint that `CHECK` constraints (in older MySQL versions) could not handle because it involves a cross-table check (aggregating `Qualifications` or reading `Pilote`).