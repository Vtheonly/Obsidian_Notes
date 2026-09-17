# 7. Disaster Recovery Protocols

A DBMS must preserve committed data and provide a recovery strategy for failures that range from transaction-level errors to complete site loss. The relevant mechanisms include WAL, checkpoints, backups, replication, and failover.

## 1. Write-Ahead Logging (WAL) Detailed Workflow

1. **The Log File:** A sequential log records changes and transaction events.
2. **The WAL Rule:** The relevant log record must be durable before the corresponding modified data page is written to permanent storage.
3. **The Buffer Pool:** Data pages may be changed in memory before being flushed to disk.

### Crash Scenario

If a transaction has a durable `COMMIT` record but some of its modified data pages were not yet persisted when the server failed, recovery can **REDO** the committed work. If another transaction was active without a durable commit, recovery can **UNDO** its incomplete work.

## 2. Checkpoints

If the log grows for a long time, scanning it from the beginning would make recovery expensive. Checkpoints record a known recovery position and reduce the amount of log that normally needs to be examined after a crash.

The exact checkpoint mechanism varies by DBMS; some systems flush many dirty pages, while others use more sophisticated incremental or fuzzy checkpoints.

## 3. Failure Classes

1. **Transaction failure:** Logical errors, constraint violations, or deadlock victims. Usually handled with statement/transaction rollback.
2. **System crash:** Power loss or operating-system failure destroys volatile memory. WAL-based REDO/UNDO restores a consistent database state.
3. **Media/disk failure:** Physical storage is damaged or lost. Backups and replication are required because WAL stored only on the failed medium is not enough.
4. **Site/catastrophic failure:** Fire, flood, or datacenter loss. Off-site or geographically separated backups/replicas are needed.

## 4. High Availability and Replication

Replication maintains one or more copies of database state on other servers. WAL records or equivalent change streams may be sent from a primary/source to replicas.

### Synchronous Replication

The primary waits for one or more replicas to durably acknowledge the required change before reporting success, depending on the system's exact commit policy.

**Trade-off:** Lower risk of losing recently committed transactions after a primary failure, but higher commit latency and dependence on replica availability/network latency.

### Asynchronous Replication

The primary reports success without waiting for replicas to confirm that the change is durable. Replicas may therefore lag behind the primary.

**Trade-off:** Lower commit latency and continued primary operation despite replica/network delays, but a sudden primary loss can leave a window of recently committed changes not yet present on the replica.

## 5. Failover

**Failover** is the controlled promotion of a replica to serve as the new primary after a primary failure.

A complete high-availability design must specify:

* how failure is detected;
* which replica is eligible for promotion;
* how clients are redirected;
* how replication consistency is verified;
* how the former primary is reintegrated after recovery.

A load balancer may help redirect traffic, but the exact failover orchestration is deployment-specific.
