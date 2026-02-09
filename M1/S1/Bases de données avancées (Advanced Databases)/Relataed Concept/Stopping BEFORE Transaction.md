Here is an explanation of what happens to your data if a crash (power loss, network failure, or application error) occurs at different stages of an SQL transaction.

To understand this, you must understand the **ACID** rule of databases, specifically **Atomicity** (All or Nothing).

Here is the breakdown of the three specific scenarios you asked about:

---

### 1. Stopping BEFORE Commit (The "Draft" Phase)
**Scenario:** You ran `START TRANSACTION`, executed several `INSERT` or `UPDATE` queries, but the connection was lost or the system crashed **before** the `COMMIT` command reached the database.

*   **What happens?** The database performs an **Automatic Rollback**.
*   **The Result:** None of your changes are saved. The database looks exactly as it did before you started.
*   **Why:** Until you say `COMMIT`, the changes exist only in temporary memory (or temporary log files). If the connection dies, the database treats the transaction as "abandoned" and discards it to ensure data safety.
*   **Analogy:** You are typing a long email. You type 5 paragraphs, but your computer crashes **before** you click "Send." When you restart, the email is gone.

### 2. Stopping AT / DURING Commit (The "Critical Moment")
**Scenario:** You issued the `COMMIT` command. The crash happens exactly at that split second—while the database is trying to write the changes to the hard drive.

*   **What happens?** This depends entirely on the **Transaction Log (Write-Ahead Log)**.
    *   **Case A (Crash just before log write):** If the crash happens before the "Commit Record" is safely written to the transaction log, the database treats it as if it never happened. **Result: Rolled Back (Data Lost).**
    *   **Case B (Crash just after log write):** If the crash happens immediately after the "Commit Record" hits the disk, but before the database confirms success to you. **Result: Rolled Forward (Data Saved).**
*   **The Mechanism:** When the database restarts, it looks at its logs.
    *   If it sees a "Commit" entry for your ID, it "Re-does" the changes to make sure they are there.
    *   If it does *not* see a "Commit" entry, it "Un-does" (Rolls back) any partial changes.
*   **Analogy:** You click "Pay Now" on a banking app. The screen spins. Then your phone dies.
    *   *Case A:* The bank server didn't get the signal before the crash. Money stays in your account.
    *   *Case B:* The bank server recorded the signal, but your phone died before showing "Success." The money is gone/transferred.

### 3. Stopping AT / DURING Rollback (The "Cleanup" Phase)
**Scenario:** You realized you made a mistake (or an error occurred), and the `ROLLBACK` command was issued. The system crashes *while* the database is busy undoing your changes.

*   **What happens?** The result is exactly the same as a successful Rollback.
*   **The Result:** The changes are gone. The data is restored to its original state.
*   **Why:** The goal of a rollback is to revert changes. If the system crashes halfway through reverting, when it restarts, the recovery process sees that the transaction was never committed. It simply finishes the job of wiping out those changes.
*   **Analogy:** You decide to delete a file. You click "Delete." The progress bar gets to 50% and the computer crashes. When you restart, the computer sees the file is corrupted/incomplete and finishes deleting it (or marks the space as free). The result is the same: the file is gone.

---

### Summary Comparison Table

| Scenario | Status of Data | Technical Action on Restart |
| :--- | :--- | :--- |
| **Stop BEFORE Commit** | **Not Saved** | Database sees an incomplete transaction and performs an **Implicit Rollback**. |
| **Stop DURING Commit** | **It Depends** | **If Log is written:** Database "Rolls Forward" (Saves data).<br>**If Log is missing:** Database "Rolls Back" (Discards data). |
| **Stop DURING Rollback**| **Not Saved** | The goal was to destroy the changes. The crash just pauses the destruction; the restart completes it. |

**The Golden Rule:** In SQL, data is considered "Safe" only after the `COMMIT` command has successfully returned a confirmation message to your application.