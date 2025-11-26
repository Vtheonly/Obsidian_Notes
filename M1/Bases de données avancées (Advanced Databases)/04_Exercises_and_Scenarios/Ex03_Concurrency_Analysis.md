
# Exercise 3: Deadlock Analysis

## The Problem
Trace the following execution and explain what happens.
**Initial State:** Product A Stock = 10, Product B Stock = 10.

| Time | Transaction 1 (T1) | Transaction 2 (T2) |
| :--- | :--- | :--- |
| t1 | `BEGIN` | `BEGIN` |
| t2 | `UPDATE Products SET Stock=9 WHERE ID='A'` | |
| t3 | | `UPDATE Products SET Stock=9 WHERE ID='B'` |
| t4 | `UPDATE Products SET Stock=8 WHERE ID='B'` | |
| t5 | | `UPDATE Products SET Stock=8 WHERE ID='A'` |

---

## Detailed Step-by-Step Analysis

1.  **t2 (T1 acts):** T1 acquires an **Exclusive Lock (X)** on **Row A**.
    *   *State:* A is locked by T1.
2.  **t3 (T2 acts):** T2 acquires an **Exclusive Lock (X)** on **Row B**.
    *   *State:* B is locked by T2.
3.  **t4 (T1 acts):** T1 tries to update **Row B**.
    *   *Conflict:* Row B is currently locked by T2.
    *   *Result:* T1 goes into **WAIT** state. It pauses execution until T2 releases the lock.
4.  **t5 (T2 acts):** T2 tries to update **Row A**.
    *   *Conflict:* Row A is currently locked by T1.
    *   *Result:* T2 tries to wait for T1.

## The Conclusion: Deadlock
*   T1 is waiting for T2 (to free B).
*   T2 is waiting for T1 (to free A).
*   **Outcome:** The database deadlock detector will notice this cycle. It will pick a victim (e.g., T2), roll it back (undoing t3), and send an error message to User 2. T1 will then proceed to lock B and finish.

## Correct Answer Logic
To prevent this, both transactions should access resources in the **same order** (e.g., Alphabetical: Always lock A before B).
*   If T2 had tried to lock A first (at t3), it would have waited immediately.
*   T1 would have locked B (at t4) successfully.
*   T1 would commit.
*   T2 would wake up, lock A, lock B, and finish.