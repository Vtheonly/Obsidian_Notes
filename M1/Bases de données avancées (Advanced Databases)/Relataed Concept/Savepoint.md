Based on **Source 20 (SQL PROCEDURAL.pdf, Section 3.11.4, Page 11-12)**, here is the explanation of **Savepoints**.

Think of a **Savepoint** as a **"Bookmark"** or a **"Checkpoint"** inside a transaction. It allows you to save your progress temporarily so that if an error occurs later, you don't have to restart the *entire* transaction from zero—you can just go back to the bookmark.

### 1. The Syntax ("On" and "Back")

According to the document, there are two main commands:

*   **Creating a Bookmark ("ON"):**
    To creates a savepoint at the current moment.
    ```sql
    SAVEPOINT my_marker;
    ```

*   **Jumping Back ("Rollback To"):**
    To undo everything done *after* the marker, but keep everything done *before* it.
    ```sql
    ROLLBACK TO SAVEPOINT my_marker;
    ```

---

### 2. How it works (The Timeline)

Imagine a transaction with 3 steps. Here is how Savepoints allow you to jump back to specific moments.

**The Script:**
```sql
START TRANSACTION;

-- Step 1: Insert a Pilot (This is good)
INSERT INTO Pilote VALUES ('PL-100', 'Mario', ...);

-- CREATE SAVEPOINT A (We are happy with Step 1)
SAVEPOINT checkpoint_A;

-- Step 2: Update Salaries (This is risky)
UPDATE Pilote SET salaire = salaire * 2;

-- CREATE SAVEPOINT B (We tried step 2)
SAVEPOINT checkpoint_B;

-- Step 3: Delete a Company (This is a mistake!)
DELETE FROM Compagnie WHERE comp = 'AF';
```

**The Scenarios (Jumping):**

1.  **Scenario: "Undo only Step 3"**
    *   Command: `ROLLBACK TO SAVEPOINT checkpoint_B;`
    *   **Result:** The DELETE is cancelled. The UPDATE (Step 2) and INSERT (Step 1) are still there. The transaction is still open.

2.  **Scenario: "Undo Step 2 and Step 3"**
    *   Command: `ROLLBACK TO SAVEPOINT checkpoint_A;`
    *   **Result:** The DELETE and UPDATE are cancelled. The INSERT (Step 1) is still there.

3.  **Scenario: "Undo Everything"**
    *   Command: `ROLLBACK;` (No savepoint name)
    *   **Result:** Everything is gone. Steps 1, 2, and 3 are cancelled.

---

### 3. "Off and On" (Lifecycle of a Savepoint)

*   **ON (Alive):** A savepoint exists as soon as you type `SAVEPOINT Name;`.
*   **OFF (Dead):** A savepoint disappears (is destroyed) in three cases:
    1.  **Commit:** If you type `COMMIT`, the transaction ends, and all savepoints are deleted.
    2.  **Full Rollback:** If you type `ROLLBACK` (without a name), the transaction ends, and savepoints are deleted.
    3.  **Overwriting:** If you type `ROLLBACK TO SAVEPOINT A`, any savepoints created *after* A (like B or C) are destroyed because you went back in time before they existed.

### 4. Example from Course (Source 20, Page 12)

The document provides a specific example using the `Compagnie` table to illustrate this:

```sql
BEGIN;
    -- Operation 1: Insert 'Easy Jet'
    INSERT INTO Compagnie VALUES (... 'Easy Jet');

    SAVEPOINT P1; -- Bookmark 1

    -- Operation 2: Update address to 'Blagnac'
    UPDATE Compagnie SET city = 'Blagnac' ...;

    SAVEPOINT P2; -- Bookmark 2

    -- Operation 3: Delete a company
    DELETE FROM Compagnie WHERE comp = 'C1';

    -- CHOICES:
    -- 1. To keep everything except the DELETE:
    -- ROLLBACK TO SAVEPOINT P2;
    
    -- 2. To keep only the INSERT (undo Update and Delete):
    -- ROLLBACK TO SAVEPOINT P1;

    -- 3. To save whatever is currently active:
    COMMIT; 
END;
```