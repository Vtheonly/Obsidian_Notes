
# Crash Recovery

How does the database survive a power failure?

## 1. The Log (Journal)
*   **Write-Ahead Logging (WAL):** The DB writes the change to a text log file *before* writing to the actual data file.
*   Sequential writing is fast.

## 2. Recovery Process
Upon restart after a crash:
1.  **REDO Phase:** Replay everything in the log that was Committed but not yet saved to the data file.
2.  **UNDO Phase:** Rollback everything in the log that was active (uncommitted) when the crash happened.

## 3. Checkpoints
*   Periodically, the DB saves all memory to disk.
*   Recovery only needs to start from the last Checkpoint, speeding up reboot time.