# Triggers as Constraints

> When `CHECK` cannot express the rule, the database gives you one escape hatch: triggers. Use them sparingly, document them loudly, and never let them become the first tool you reach for. Triggers are constraints of last resort.

## What you already know

From [[02-Domain-Check-Constraints]]: declarative constraints (`NOT NULL`, `CHECK`, `UNIQUE`, `EXCLUDE`) enforce invariants at the row level — cheaply, inline, and discoverably. Their limitation: they cannot look at other rows, other tables, or the current time. From [[02-Encapsulation]]: invariants belong at the layer that can enforce them universally. The database is universal for *its* rows; a trigger extends that universality to rules CHECK cannot reach. From [[08-Trade-offs-Everywhere]]: every choice is a trade-off. Triggers trade declarative simplicity for procedural power — and the cost is paid in debugging, performance, and surprise.

## Why this layer exists

Some invariants cannot be expressed per-row. The Banking system has three:

1. **Closed accounts cannot transact.** A new `ledger_entries` row should be rejected if its `account_id` refers to an account with `status = 'CLOSED'`. CHECK cannot look at another table.
2. **Every transfer's two ledger entries must sum to zero.** This is a multi-row invariant across a transaction.
3. **A frozen account cannot send (only receive).** The rule depends on the account's status *and* the direction of the entry.

For these, the choices are:

- **Application code** — visible, testable, bypassable by any other client.
- **Database trigger** — invisible, universal, harder to test.
- **Both (defense in depth)** — application for friendly errors; trigger as the safety net.

This layer exists because the database is the only universal enforcement point. If the invariant must hold for every client forever, the trigger is the only tool that delivers that.

## What is genuinely new here

The new idea is **the trigger as defense-in-depth** — the same invariant enforced in *three* places: object invariant in code, CHECK constraint in schema (where possible), and trigger in DB (where CHECK cannot reach). This redundancy is not waste; it is *layers of protection against different failure modes*.

## Concepts

### What a trigger is

A trigger is a function the database executes automatically when a specified event occurs on a specified table. The components:

- **Event** — `INSERT`, `UPDATE`, `DELETE`, or `TRUNCATE`.
- **Timing** — `BEFORE` (can modify or cancel the row), `AFTER` (runs after the row is written), or `INSTEAD OF` (for views).
- **Granularity** — `FOR EACH ROW` (fires per row) or `FOR EACH STATEMENT` (fires once per statement).
- **Condition** — optional `WHEN` clause (PostgreSQL) restricting when the trigger fires.
- **Function** — the procedural code (PL/pgSQL in PostgreSQL, PL/SQL in Oracle, T-SQL in SQL Server).

### What a trigger can do that CHECK cannot

| Rule | CHECK | Trigger |
|---|---|---|
| `balance >= 0` | Yes | Yes (but slower) |
| `status IN ('A','B')` | Yes | Yes |
| `iban` is unique among active accounts | Yes (partial UNIQUE) | Yes |
| A new ledger entry's account must not be CLOSED | No (cross-table) | Yes |
| The two entries of a transfer must sum to zero | No (cross-row) | Yes (with deferred constraint) |
| Balance equals the sum of ledger entries | No (aggregate) | Yes (but expensive) |
| A withdrawal cannot happen on a weekend | No (time-dependent) | Yes |
| Audit log entry must be written on every status change | No (side-effect) | Yes |

The right-hand column is where triggers earn their keep. The left-hand column is where they should not be used.

### BEFORE vs AFTER

- `BEFORE` triggers can modify the row being inserted (`NEW.balance := NEW.balance + adjustment`) or cancel the operation (`RETURN NULL`).
- `AFTER` triggers cannot modify the row but can write to other tables (audit logs, notifications, derived data).

The pattern: use `BEFORE` for validation and row adjustment; use `AFTER` for side effects.

### Statement-level vs row-level

- `FOR EACH ROW` fires once per row affected by the statement.
- `FOR EACH STATEMENT` fires once for the whole statement, regardless of how many rows it touched.

A `DELETE FROM accounts WHERE status = 'CLOSED'` that affects 1000 rows fires a row-level trigger 1000 times but a statement-level trigger once. Use statement-level when the rule is about the operation, not the individual rows.

### Deferred constraint triggers

PostgreSQL constraint triggers can be `DEFERRABLE INITIALLY DEFERRED` — they fire at commit time rather than statement time. This is essential for multi-row invariants like "the two entries of a transfer must sum to zero," because the transfer is only consistent once both entries are written.

### The rule: prefer CHECK, use triggers sparingly, document them loudly

The discipline:

1. Try to express the rule as a CHECK or UNIQUE. If yes, stop.
2. If the rule is cross-row, cross-table, or time-dependent, consider a trigger.
3. Before writing the trigger, ask: *can the application enforce this well enough?* If the database is the only client (rare), the application may suffice.
4. If the trigger is necessary, document it in three places:
   - The schema (with a `COMMENT ON TRIGGER`).
   - The application's domain model documentation.
   - The migration that creates it.

Undocumented triggers are the source of the worst debugging sessions in databases.

## Banking application

### Trigger 1: closed accounts cannot transact

```sql
-- PostgreSQL: trigger enforcing invariant 8 of the Banking case study

CREATE OR REPLACE FUNCTION enforce_open_account_for_ledger()
RETURNS TRIGGER AS $$
BEGIN
    -- Cross-table check: the account referenced by this new ledger entry
    -- must NOT be CLOSED. CHECK cannot do this.
    IF EXISTS (
        SELECT 1 FROM accounts
        WHERE id = NEW.account_id
          AND status = 'CLOSED'
    ) THEN
        RAISE EXCEPTION 'Account % is closed; ledger entries are not allowed',
            NEW.account_id
            USING ERRCODE = 'check_violation';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_ledger_no_closed_account
BEFORE INSERT OR UPDATE ON ledger_entries
FOR EACH ROW
EXECUTE FUNCTION enforce_open_account_for_ledger();
```

This trigger fires before every insert into `ledger_entries`. It rejects the insert if the account is closed. It is the database-level enforcement of invariant 8 from [[00-Banking-Case-Study]].

### Trigger 2: audit log on account status change

```sql
-- PostgreSQL: AFTER trigger that writes an audit row on every status change

CREATE TABLE audit_log (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    table_name   TEXT NOT NULL,
    row_id       BIGINT NOT NULL,
    changed_from TEXT,
    changed_to   TEXT,
    changed_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    changed_by   TEXT  -- application-supplied via SET LOCAL app.user
);

CREATE OR REPLACE FUNCTION audit_account_status()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status IS DISTINCT FROM NEW.status THEN
        INSERT INTO audit_log (table_name, row_id, changed_from, changed_to)
        VALUES ('accounts', NEW.id, OLD.status, NEW.status);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_audit_account_status
AFTER UPDATE OF status ON accounts
FOR EACH ROW
WHEN (OLD.status IS DISTINCT FROM NEW.status)
EXECUTE FUNCTION audit_account_status();
```

This is the auditability invariant (invariant 6 of [[00-Banking-Case-Study]]). The trigger fires only when `status` actually changes (the `WHEN` clause and the `OF status` qualifier together make it efficient).

### Trigger 3: double-entry must balance (deferred)

```sql
-- PostgreSQL: deferred constraint trigger enforcing the double-entry rule

CREATE OR REPLACE FUNCTION enforce_transfer_balances()
RETURNS TRIGGER AS $$
BEGIN
    -- This trigger fires at commit time on transfers. It checks that
    -- the two ledger entries associated with the transfer sum to zero.
    IF NEW.status = 'COMPLETED' THEN
        IF NOT EXISTS (
            SELECT 1
            FROM ledger_entries le
            WHERE le.transfer_id = NEW.id
            GROUP BY le.transfer_id
            HAVING SUM(le.amount) = 0
               AND COUNT(*) = 2
        ) THEN
            RAISE EXCEPTION 'Transfer % does not have a balanced pair of ledger entries',
                NEW.id;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE CONSTRAINT TRIGGER trg_transfer_balanced
AFTER UPDATE ON transfers
FOR EACH ROW
DEFERRABLE INITIALLY DEFERRED
EXECUTE FUNCTION enforce_transfer_balances();
```

The `DEFERRABLE INITIALLY DEFERRED` clause means the check runs at commit, after both ledger entries have been written. Without it, the trigger would fire mid-transaction when only one entry existed and fail.

### Defense in depth — the application layer

The same invariants are checked in the `TransferService` Java code:

```java
public TransferResult transfer(TransferRequest req) {
    Account src = accounts.findById(req.fromAccountId());
    if (src.status() == AccountStatus.CLOSED) {
        throw new AccountClosedException(src.id());
    }
    // ... continue with the transfer
}
```

Why both? The application gives the user a friendly error message ("This account is closed") before any database call. The trigger catches the case where:

- A migration script bypasses the application.
- A future microservice reuses the schema without re-implementing the rule.
- A maintenance query inserts a row directly.
- A race condition leaves a window where the account was closed after the application's check but before the insert.

The trigger is the *last line of defense*. It is also the *most expensive* line — every insert pays the trigger's cost. That cost is the price of universal enforcement.

## Code — what can go wrong with triggers

```sql
-- BAD: a trigger that calls a non-immutable function
CREATE OR REPLACE FUNCTION check_business_hours()
RETURNS TRIGGER AS $$
BEGIN
    IF EXTRACT(DOW FROM now()) IN (0, 6) THEN
        RAISE EXCEPTION 'No withdrawals on weekends';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

This trigger has three problems:

1. **Hidden dependency on time.** The same insert succeeds at 9 AM Monday and fails at 9 PM Saturday. Tests are non-deterministic.
2. **No documented business reason.** Why weekends? Is it regulatory? Internal policy? A trigger is a bad place to encode policy that may change.
3. **Performance.** `now()` is called per row.

The better design: encode business rules in the application (where they can be tested, configured, and changed without a migration) and reserve triggers for invariants the schema genuinely requires.

## What can go wrong

- **Hidden logic.** A junior developer inserts a row, gets a cryptic error from a trigger they did not know existed, and spends hours finding it. `COMMENT ON TRIGGER` and a clear naming convention (`trg_*`) help.
- **Performance cliffs.** A row-level trigger on a hot table that runs a subquery per row can turn a 10 ms insert into a 1000 ms insert. Always measure.
- **Ordering.** Multiple triggers on the same table fire in alphabetical order by name in PostgreSQL. If the order matters, name them so the alphabetical order is correct.
- **Cascading triggers.** A trigger on `accounts` updates `ledger_entries`, which has a trigger that updates `audit_log`, which has a trigger that writes a notification. A single user action can trigger a cascade of work that is invisible in the application's call graph.
- **Mutation inside triggers.** A `BEFORE` trigger that modifies `NEW` can change the values actually written, surprising the application. Document any `NEW` modification loudly.
- **Non-determinism.** Triggers that depend on `now()`, random functions, or external state make tests flaky and debugging hard.
- **Migrations that disable triggers.** `ALTER TABLE ... DISABLE TRIGGER ALL` is sometimes used in bulk loads. Forgetting to re-enable triggers leaves the schema unprotected. Always wrap such operations in a transaction that ends with `ENABLE TRIGGER`.
- **Triggers as a substitute for schema design.** A schema with many triggers enforcing rules CHECK could express is a schema that chose the harder path. Revisit those triggers and ask if a CHECK would do.

## Trade-offs

- **Universality vs visibility.** Triggers are universal (every write goes through them) but invisible (no caller sees them). The trade-off is fundamental: the more universal the enforcement, the less visible to any individual caller.
- **Correctness vs performance.** Every trigger adds work to every write. The trade-off is enforced correctness at the cost of throughput. For OLTP, this is usually worth it; for high-volume event ingestion, it may not be.
- **Defense in depth vs single-source-of-truth.** Enforcing an invariant in both code and DB is safer but creates two sources of truth. If they drift, the stricter one wins silently. Document both; keep them in sync.
- **Declarative vs procedural.** CHECK is declarative: you state the rule, the DB enforces it. Triggers are procedural: you write the enforcement. Declarative is more concise, more discoverable, and more optimizable. Procedural is more expressive.

## Forward links

- [[02-Domain-Check-Constraints]] — the preferred, declarative alternative.
- [[04-Banking-Schema]] — where each trigger sits in the full schema.
- [[08-Stored-Procedures]] — triggers and stored procedures share PL/pgSQL; the same trade-offs apply.
- [[00-ACID]] — triggers are part of the transaction; they can roll it back.
- [[04-MVCC]] — trigger-fired queries see the same MVCC snapshot as the triggering statement.
- [[08-Reading-EXPLAIN]] — trigger costs do not appear in EXPLAIN of the triggering statement; you must EXPLAIN ANALYZE the trigger function separately.
