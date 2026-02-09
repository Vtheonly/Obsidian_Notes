# Master Class: Functions & Stored Procedures (SQL Procedural)

**Course Context:** Bases de Données Avancées (Master 1)
**Sources:** *Source 20 (SQL Procedural), Source 15 (Corrigé TD4)*

---

## Part 1: The Concept of Procedural SQL

### 1.1 Why do we need it?
Standard SQL (`SELECT`, `INSERT`, `UPDATE`) is **Declarative**: you tell the database *what* you want, not *how* to do it step-by-step.
**Procedural SQL** extends SQL by adding programming structures found in languages like C or Java:
*   Variables and assignment.
*   Conditional Logic (`IF`, `CASE`).
*   Loops (`WHILE`, `LOOP`, `REPEAT`).
*   Error Handling (Exceptions).

### 1.2 The "Delimiter" Problem
In standard SQL, the semicolon `;` marks the end of a command.
Inside a procedure, we write many lines of code ending in `;`. To prevent MySQL from executing the procedure halfway through while we are defining it, we must change the delimiter temporarily.

**Standard Pattern:**
```sql
DELIMITER $  -- Change end-marker to $
-- Define the Procedure here
-- Use ; inside the procedure normally
END $        -- End the definition with $
DELIMITER ;  -- Change back to ;
```

---

## Part 2: Variables & Scope

**Source 20 (Section 3)** defines two distinct types of variables. Confusing them is a common exam mistake.

| Feature | **Local Variables** (`DECLARE`) | **Session Variables** (`@var`) |
| :--- | :--- | :--- |
| **Scope** | Exist **only** inside the `BEGIN...END` block. | Exist for the entire connection session (globally). |
| **Declaration** | `DECLARE v_nom VARCHAR(20);` | No declaration needed. Just assignment. |
| **Syntax** | `v_nom` (No @ sign) | `@v_nom` (Must have @) |
| **Usage** | Used for internal calculations. | Used to pass values between procedures or from the shell. |

**Assignment Syntax:**
```sql
SET v_count = 10;
-- OR
SELECT COUNT(*) INTO v_count FROM Pilote;
```

---

## Part 3: Stored Procedures vs. Functions

**Source 20 (Section 1.3)** outlines the key differences.

### 3.1 Stored Procedures
*   **Purpose:** Execute a series of actions (business logic, updates, complex transactions).
*   **Return Values:** Can return **multiple** values using `OUT` or `INOUT` parameters.
*   **Invocation:** Called using `CALL ProcedureName()`.
*   **Parameter Modes:**
    *   `IN`: Pass value *into* procedure (Read-only inside).
    *   `OUT`: Pass value *out* of procedure (Write-only inside, starts NULL).
    *   `INOUT`: Pass value in, modify it, pass it back out.

**Syntax:**
```sql
CREATE PROCEDURE myProc(IN p_id INT, OUT p_result VARCHAR(50))
BEGIN
    -- Logic
END
```

### 3.2 Stored Functions
*   **Purpose:** Calculate and return a **single value**.
*   **Return Values:** Must have a `RETURNS type` clause and a `RETURN value` statement.
*   **Invocation:** Used inside SQL statements like a variable: `SELECT myFunction(col) FROM Table`.
*   **Restriction:** Generally cannot contain statements that return a result set (like a `SELECT *` without `INTO`).

**Syntax:**
```sql
CREATE FUNCTION myFunc(p_id INT) RETURNS INT
BEGIN
    RETURN p_id * 10;
END
```

---

## Part 4: Cursors (The "Row-by-Row" Processor)

**Source 20 (Section 2)** explains that standard SQL works on *sets* of rows. If you need to process rows one by one (like a `for` loop in Java), you use a **Cursor**.

### The 4-Step Lifecycle
1.  **DECLARE:** Define the query. `DECLARE cur CURSOR FOR SELECT...`
2.  **OPEN:** Execute the query and load results into memory. `OPEN cur;`
3.  **FETCH:** Get the next row into variables. `FETCH cur INTO v_a, v_b;`
4.  **CLOSE:** Free memory. `CLOSE cur;`

> [!TIP] The "Done" Handler
> To stop the loop, you must declare a "Handler". When `FETCH` runs out of rows, MySQL raises a `NOT FOUND` warning. We catch this to set a flag variable to stop the loop.

---

## Part 5: Solved Exercises (Deep Dive)

We will use the **Airline Database** context:
*   `Compagnie (comp, ...)`
*   `Pilote (brevet, nom, nbHVol, comp, ...)`

### Exercise 1: Scalar Function (`EffectifsHeure`)
**Goal:** Return the number of pilots in a company having more than `X` flight hours. If company is NULL, count all pilots.

**Solution:**
```sql
DELIMITER $

CREATE FUNCTION EffectifsHeure(
    pcomp VARCHAR(4),
    pheuresVol DECIMAL(7,2)
) 
RETURNS SMALLINT
DETERMINISTIC READS SQL DATA -- Good practice for function safety
BEGIN
    DECLARE resultat SMALLINT;

    -- Logic: Check if we filter by company or take all
    IF (pcomp IS NULL) THEN
        SELECT COUNT(*) INTO resultat 
        FROM Pilote 
        WHERE nbHVol > pheuresVol;
    ELSE
        SELECT COUNT(*) INTO resultat 
        FROM Pilote 
        WHERE nbHVol > pheuresVol AND comp = pcomp;
    END IF;

    RETURN resultat;
END $
DELIMITER ;
```
**Explanation:**
1.  **`RETURNS SMALLINT`**: Functions must declare the data type they return.
2.  **`SELECT ... INTO`**: We calculate the count and store it immediately in the local variable `resultat`.
3.  **`IF/ELSE`**: Handles the requirement "If comp is NULL, count all".

---

### Exercise 2: Procedure with INOUT (`PlusExperimente`)
**Goal:** Find the most experienced pilot.
*   Input: Company code.
*   Output: Pilot Name, Hours.
*   Special Logic: If Input Company is NULL, find the best pilot across *all* companies and return their Company Code in the input variable.

**Solution:**
```sql
DELIMITER $

CREATE PROCEDURE PlusExperimente(
    INOUT pcomp VARCHAR(4),      -- INOUT: Can receive 'AF' or NULL, and return 'AF' or 'SING'
    OUT pnom VARCHAR(15),        -- OUT: Returns name
    OUT pheuresVol DECIMAL(7,2)  -- OUT: Returns hours
)
BEGIN
    IF (pcomp IS NOT NULL) THEN
        -- Case 1: Search specific company
        SELECT nom, nbHVol INTO pnom, pheuresVol
        FROM Pilote
        WHERE comp = pcomp
        ORDER BY nbHVol DESC
        LIMIT 1; -- Take the top 1
    ELSE
        -- Case 2: Search global. We must also update pcomp.
        SELECT nom, nbHVol, comp INTO pnom, pheuresVol, pcomp
        FROM Pilote
        ORDER BY nbHVol DESC
        LIMIT 1;
    END IF;
END $
DELIMITER ;
```
**Explanation:**
*   **`INOUT pcomp`**: This is crucial. It acts as a filter initially. If it's NULL, the procedure fills it with the company of the winner.
*   **`ORDER BY ... DESC LIMIT 1`**: The standard SQL way to find "The most experienced" (Max) without using a complex subquery.

---

### Exercise 4: Recursion (Factorial)
**Goal:** Write a recursive function for $n!$.

**Solution:**
```sql
DELIMITER $
CREATE FUNCTION factorielle(n INT) RETURNS INT
DETERMINISTIC
BEGIN
    IF n <= 1 THEN
        RETURN 1;
    ELSE
        RETURN n * factorielle(n - 1); -- Recursive Call
    END IF;
END $
DELIMITER ;
```
> [!WARNING] MySQL Limitation
> As noted in **Source 15**, older MySQL versions (and default configs) disallow recursive functions (`Error 1424`). To make this work in a procedure, you must set `SET max_sp_recursion_depth = 255;`.

---

### Exercise 5: Basic Cursor (Summing Hours)
**Goal:** Calculate total flight hours for company 'AF' using a cursor (instead of `SUM()`).

**Solution:**
```sql
DELIMITER $

CREATE PROCEDURE total_hvol_AF()
BEGIN
    -- 1. Variables
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_nbHv DECIMAL(7,2);
    DECLARE v_tot DECIMAL(8,2) DEFAULT 0;
    
    -- 2. Cursor Declaration (The Query)
    DECLARE curs1 CURSOR FOR 
        SELECT nbHVol FROM Pilote WHERE comp = 'AF';
        
    -- 3. Handler (The "Stop" Signal)
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- 4. Open
    OPEN curs1;

    -- 5. Loop
    read_loop: LOOP
        FETCH curs1 INTO v_nbHv; -- Get one row
        
        IF done THEN
            LEAVE read_loop; -- Break loop if empty
        END IF;
        
        SET v_tot = v_tot + v_nbHv; -- Accumulate
    END LOOP;

    CLOSE curs1;

    -- 6. Result
    SELECT v_tot AS 'Total Heures AF';
END $
DELIMITER ;
```
**Key logic:** The `FETCH` moves the pointer. When it fails, `done` becomes TRUE. The `IF done` check prevents adding the last value twice or adding NULL.

---

### Exercise 6: Cursor with Locking (`FOR UPDATE`)
**Goal:** Iterate through pilots.
*   If Company = 'AF': Add 100 hours.
*   If Company = 'SING': Remove 100 hours.
*   Others: Delete pilot.
*   **Requirement:** Lock the rows while processing.

**Solution:**
```sql
DELIMITER $

CREATE PROCEDURE Gestion_Pilotes()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE v_brevet VARCHAR(6);
    DECLARE v_comp VARCHAR(4);
    
    -- IMPORTANT: "FOR UPDATE" locks the selected rows
    DECLARE cur_pilote CURSOR FOR 
        SELECT brevet, comp FROM Pilote FOR UPDATE;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    START TRANSACTION; -- Optional but good for wrapping the logic
    
    OPEN cur_pilote;

    loop_pilote: LOOP
        FETCH cur_pilote INTO v_brevet, v_comp;
        IF done = 1 THEN LEAVE loop_pilote; END IF;

        -- Business Logic Branching
        IF v_comp = 'AF' THEN
            UPDATE Pilote SET nbHVol = nbHVol + 100 WHERE brevet = v_brevet;
        ELSEIF v_comp = 'SING' THEN
            UPDATE Pilote SET nbHVol = nbHVol - 100 WHERE brevet = v_brevet;
        ELSE
            DELETE FROM Pilote WHERE brevet = v_brevet;
        END IF;
        
    END LOOP;

    CLOSE cur_pilote;
    COMMIT; -- Release locks
END $
DELIMITER ;
```
**Explanation:**
*   **`FOR UPDATE`**: In the cursor definition, this ensures that no other transaction can modify these pilots while this procedure is running. This prevents concurrency errors (Lost Updates).
*   **Logic:** We read `comp` into a variable (`v_comp`) and decide the action based on that variable. We use the Primary Key (`v_brevet`) to target the `UPDATE`/`DELETE` precisely.

---

## Summary Checklist for Exams

1.  **Delimiters:** Don't forget `DELIMITER $` before creating objects.
2.  **Parameters:** Remember `IN`, `OUT`, `INOUT` are for Procedures only.
3.  **Cursors:** Remember the order: Variables -> Cursor -> Handler.
4.  **Assignment:** Use `SET var = val` or `SELECT col INTO var`.
5.  **Strict Mode:** Functions usually need `DETERMINISTIC` or `READS SQL DATA` flags in newer MySQL versions.