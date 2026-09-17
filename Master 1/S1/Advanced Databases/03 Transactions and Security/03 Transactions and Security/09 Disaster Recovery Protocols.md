# 7. Disaster Recovery Protocols

A DBMS must guarantee that once a transaction says `COMMIT`, the data is permanently safe, even if someone unplugs the server a millisecond later. This relies on three core pillars: The WAL, Checkpoints, and Backups.

## 1. Write-Ahead Logging WAL Detailed Workflow
Writing directly to database files on a hard drive is slow because data is scattered randomly across the disk. To guarantee speed and safety, the DBMS uses the WAL.

1.  **The Log File:** This is a continuous, append-only file. Writing to it is incredibly fast.
2.  **The Rule:** The DBMS must write the *intent* of the modification to the WAL **before** it actually modifies the physical database pages.
3.  **The Memory Buffer:** Data modifications happen in fast RAM (Buffer Pool). Eventually, these modified memory pages are flushed to the slow hard drive.

### The Crash Scenario:
Imagine T1 transfers money, says `COMMIT`, the DBMS writes this to the WAL, but before the RAM flushes the actual database files to the disk, the power fails.

Upon reboot, the DBMS goes into **Recovery Mode**:
1.  It reads the WAL from the last known good state.
2.  **REDO Phase (Roll Forward):** It finds T1 in the log with a `COMMIT` tag, but sees the data file is missing the change. It *re-executes* T1 from the log to restore the committed state.
3.  **UNDO Phase (Roll Back):** It finds T2 in the log with some `UPDATE` statements, but no `COMMIT` tag (T2 was interrupted). The DBMS actively reverses any partial writes T2 might have made to ensure consistency.

## 2. Checkpoints
If a database runs for a year, the WAL becomes enormous. Rebooting and reading a year's worth of logs would take days.
*   Periodically, the DBMS pauses briefly.
*   It forces all modified RAM pages to the physical disk.
*   It writes a **Checkpoint** marker in the WAL.
*   If a crash happens, the DBMS only needs to read the WAL starting from the most recent Checkpoint, discarding everything before it as safely written.

## 3. High Availability Redundancy
For mission-critical systems, WAL and Checkpoints are not enough (what if the hard drive itself burns?). 
*   **Replication:** The Master server constantly streams its WAL entries to a Slave server. The Slave plays the WAL entries on its own disk.
*   **Failover:** If the Master dies, a load balancer instantly redirects all user traffic to the Slave, which becomes the new Master, ensuring zero downtime.
