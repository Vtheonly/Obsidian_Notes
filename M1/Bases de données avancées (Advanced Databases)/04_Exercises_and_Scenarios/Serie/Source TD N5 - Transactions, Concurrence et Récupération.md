Here is the complete processing for the source **TD N°5 : Transactions, Concurrence et Récupération**.

This TD focuses on the theoretical and practical aspects of transaction management (ACID properties), concurrency control (Isolation levels, anomalies), and database recovery (Logs).

---

# Source: TD N°5 - Transactions, Concurrence et Récupération

**Context:**
*   Theoretical exercises on ACID properties.
*   Scenarios involving bank accounts (`Comptes`), products (`Produits`), and university registrations.
*   Log analysis for crash recovery.

---

### Exercise 1: ACID Properties

**Source:** TD 5 - Exercice 1
**Questions:**
1.  Define ACID.
2.  Real-life examples.
3.  Why banking needs strict Atomic/Durability.

#### 1. Solution
*   **A - Atomicité (Atomicity):** "All or Nothing". A transaction is an indivisible unit. Either all operations succeed, or none are applied.
*   **C - Cohérence (Consistency):** The transaction takes the database from one valid state to another, respecting all integrity constraints (primary keys, checks, etc.).
*   **I - Isolation:** Transactions executing concurrently should not interfere with each other. Intermediate states are invisible to others.
*   **D - Durabilité (Durability):** Once a transaction is committed (validated), the changes are permanent, even in the event of a power failure or crash.

*   **Real-life Example (Coffee Machine):**
    *   Atomic: You insert a coin and press a button. You get coffee + change, OR you get your coin back. You never lose the coin without getting coffee.
*   **Banking Necessity:** If a transfer of 100 DA from Ali to Sara crashes after debiting Ali but before crediting Sara, money vanishes. Atomicity ensures this doesn't happen. Durability ensures that if the system says "Transfer Done", the money is truly in Sara's account even if the server explodes 1 second later.

#### 2. Reasoning
These are the four fundamental pillars of relational database reliability.

#### 3. Detailed Explanation
*   **Atomicity** is usually implemented via **Rollback** segments or Undo Logs. If an error occurs, the DB reverses all previous steps of the transaction.
*   **Isolation** is handled by **Locking** (verrouillage) and **MVCC** (Multi-Version Concurrency Control).
*   **Durability** is achieved via **Write-Ahead Logging (WAL)**. The log entry is written to the hard drive *before* the confirmation is sent to the user.

---

### Exercise 2: Transactions SQL

**Source:** TD 5 - Exercice 2
**Context:** Table `Comptes(id, titulaire, solde)`. Ali (500), Sara (300). Transfer 100 from Ali to Sara.

#### 1. Solution
**Q1. SQL Commands:**
```sql
START TRANSACTION; -- or BEGIN
UPDATE Comptes SET solde = solde - 100 WHERE id = 1; -- Ali
UPDATE Comptes SET solde = solde + 100 WHERE id = 2; -- Sara
COMMIT;
```

**Q2. Crash Scenario:**
If a power failure occurs after the first update but before the second (and before commit), the database is in an inconsistent state (Ali=400, Sara=300, 100 vanished).

**Q3. SGBD Reaction:**
Upon restart, the SGBD detects via its logs that the transaction was active but never received a `COMMIT`. It automatically performs a **ROLLBACK** (Undo) on the modification to Ali's account. The state reverts to Ali=500, Sara=300.

#### 2. Reasoning
The explicit `COMMIT` is the "save point". Anything before that is provisional.

#### 3. Detailed Explanation
This illustrates the "A" (Atomicity) in ACID. The transaction is a logical unit of work. The SGBD guarantees that partial updates are never visible permanently.

---

### Exercise 3: Concurrency Problems

**Source:** TD 5 - Exercice 3
**Context:** Two transactions T1 and T2 on `Produits(id, stock)`.
*   T1: Decrement stock by 10.
*   T2: Read stock.

#### 1. Solution
**Q1. Dirty Read (Lecture Sale):**
*   T1 updates stock (100 -> 90).
*   T2 reads stock (90).
*   T1 fails and does **ROLLBACK** (stock -> 100).
*   *Result:* T2 has worked with a value (90) that "never existed".

**Q2. Lost Update (Perte de mise à jour):**
*   T1 reads stock (100).
*   T2 reads stock (100).
*   T1 updates (100 - 10 = 90) and commits.
*   T2 updates (100 - 5 = 95) and commits.
*   *Result:* The update from T1 is overwritten. Final stock is 95, should be 85.

**Q3. Solution:**
Use **Locking** (Pessimistic) or higher isolation levels (like Repeatable Read or Serializable). T1 should lock the row before reading if it intends to update (`SELECT ... FOR UPDATE`).

#### 2. Reasoning
Concurrency anomalies occur when transactions interleave their operations without sufficient isolation.

#### 3. Detailed Explanation
*   **Dirty Read** happens in `READ UNCOMMITTED` isolation level.
*   **Lost Update** is a classic race condition. To fix it, T2 must be forced to wait until T1 finishes, or T2 must detect that the row changed before committing (Optimistic Locking).

---

### Exercise 4: Isolation Levels

**Source:** TD 5 - Exercice 4
**Context:** Explain `READ UNCOMMITTED`, `READ COMMITTED`, `REPEATABLE READ`, `SERIALIZABLE`.

#### 1. Solution
**Q1. Differences:**
*   **READ UNCOMMITTED:** Lowest level. Can read non-committed data (Dirty Reads allowed). Fast but dangerous.
*   **READ COMMITTED:** Default in many DBs (Oracle, PostgreSQL). Only reads committed data. Prevents Dirty Reads but allows Non-Repeatable Reads (if T1 reads X twice, value might change).
*   **REPEATABLE READ:** Guarantees that if T1 reads X, it will see the same value for X throughout the transaction. Prevents Non-Repeatable Reads but allows Phantom Reads.
*   **SERIALIZABLE:** Highest level. Transactions execute as if they were sequential (one after another). No anomalies allowed.

**Q2. Scenarios:**
*   *Reporting on approximate stats (e.g., Likes on a post):* **Read Uncommitted** (Speed > Accuracy).
*   *Banking transfer:* **Read Committed** or **Repeatable Read**.
*   *Inventory management preventing negative stock:* **Serializable** (or strict locking).

#### 2. Reasoning
It's a trade-off between **Consistency** (Strict isolation) and **Performance** (Concurrency).

#### 3. Detailed Explanation
The standard SQL isolation levels are defined by which anomalies they *allow*:

| Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read |
| :--- | :---: | :---: | :---: |
| Read Uncommitted | Yes | Yes | Yes |
| Read Committed | No | Yes | Yes |
| Repeatable Read | No | No | Yes |
| Serializable | No | No | No |

---

### Exercise 5: Recovery (Récupération)

**Source:** TD 5 - Exercice 5
**Context:**
*   Log: `[Start T1, Write T1(id1, -200), Start T2, Write T2(id2, +200), Commit T1, CRASH]`
*   T2 did not commit.

#### 1. Solution
**Q1. SGBD Action (REDO/UNDO):**
*   **T1**: The log shows `COMMIT T1` before the crash. The SGBD must ensure T1's changes are applied. -> **REDO T1**.
*   **T2**: The log shows T2 started and wrote, but *never* committed. The SGBD must undo T2's partial changes. -> **UNDO T2**.

**Q2. Final State:**
*   Account `id=1` (modified by T1): Decreased by 200 (Saved).
*   Account `id=2` (modified by T2): Unchanged (Rolled back).

#### 2. Reasoning
This is the **ARIES** recovery algorithm principle.
*   **Winner (Gagnant):** Transaction with a COMMIT in the log. Must be replayed (Redo).
*   **Loser (Perdant):** Transaction active at crash time. Must be rolled back (Undo).

#### 3. Detailed Explanation
The recovery manager reads the log (usually backwards for Undo, forwards for Redo).
1.  It sees `Commit T1`. T1 is safe.
2.  It sees the crash happened while T2 was active. T2 is incomplete.
3.  **UNDO Phase**: It reverses `Write T2(id2, +200)` -> effectively doing `id2 = id2 - 200` (or restoring the "before image").
4.  **REDO Phase**: It reapplies `Write T1(id1, -200)` to ensure the disk reflects the change (in case the buffer wasn't flushed).

---

### Exercise 6: Case Study (University Registration)

**Source:** TD 5 - Exercice 6
**Context:** Registration involves 3 steps:
1.  Debit student account.
2.  Insert into `Inscriptions`.
3.  Decrement `Places_Disponibles` in `Cours`.

#### 1. Solution
**Q1. Transaction Model:**
```sql
BEGIN;
UPDATE Etudiants SET Solde = Solde - Frais WHERE ID = ...;
INSERT INTO Inscriptions VALUES (...);
UPDATE Cours SET Places = Places - 1 WHERE ID = ...;
COMMIT;
```

**Q2. Crash after Step 2:**
If the DB crashes after Step 2 (Insert) but before Step 3 (Update Cours) and before Commit:
*   The Atomicity property ensures **Rollback**.
*   The money is refunded (Step 1 undone).
*   The inscription line is removed (Step 2 undone).
*   The database returns to the state *before* the student tried to register.

**Q3. Guarantee:**
The system must guarantee **Consistency** (Constraints) and **Atomicity**.
Specifically, we need to ensure `Places > 0` (Check constraint) before decrementing. If places are 0, the transaction should assume a logical failure and Rollback itself.

#### 2. Reasoning
A multi-step business process must be wrapped in a single transaction to prevent partial data (e.g., Student paid but is not registered, or registered but course is full).

#### 3. Detailed Explanation
This scenario highlights the danger of "Inconsistent Analysis" or partial updates. Without transaction boundaries, a script running these 3 queries separately (autocommit on) would leave the database corrupted if a crash occurred in the middle. The student would have paid money but the course count wouldn't reflect their attendance.