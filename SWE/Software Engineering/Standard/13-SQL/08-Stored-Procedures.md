# Stored Procedures

> Putting logic in the database. PL/pgSQL (PostgreSQL), PL/SQL (Oracle), T-SQL (SQL Server) — every major database has a procedural language that runs inside the DBMS. The question is not *can* you put logic there, but *should* you. The answer is: sometimes, deliberately, and not by default.

## What you already know

From [[03-Triggers-As-Constraints]]: the database can run procedural code via triggers — and the trade-off is hidden logic, performance cost, and debugging difficulty. From [[04-Abstraction-and-Models]]: an abstraction reduces or inverts a dependency. A stored procedure is an abstraction over the schema; callers depend on the procedure, not on the tables. From [[06-Coupling-and-Cohesion]]: putting business logic in the database couples the application to the database — every change requires a migration. From [[08-Trade-offs-Everywhere]]: the choice between logic-in-app and logic-in-DB is one of the deepest trade-offs in database engineering.

## Why this layer exists

Some operations are awkward to express in pure SQL:

- A transfer requires several statements, conditional logic, and an idempotency check. Encapsulating it as a single callable reduces round-trips and centralizes the logic.
- A batch job (daily interest accrual, statement generation) needs loops, conditionals, and exception handling.
- A complex validation that depends on multiple tables is faster if it runs where the data lives.

Stored procedures exist to give the database a procedural layer for these cases. The question is when to use them — and when not to.

## What is genuinely new here

The new idea is **logic as a schema object**. A stored procedure is a function: it has a name, parameters, a body, and a return value. It is created with DDL, versioned with migrations, and called from SQL or from the application. The database becomes not just a data store but a *compute location*.

## Concepts

### Functions vs procedures

PostgreSQL historically had only *functions* (`CREATE FUNCTION`); PostgreSQL 11 added *procedures* (`CREATE PROCEDURE`). The difference:

| Aspect | Function | Procedure |
|---|---|---|
| Return value | Required (can be `void`) | None |
| Called from SQL | Yes (`SELECT my_func()`) | No (must use `CALL my_proc()`) |
| Transaction control | Cannot commit/rollback (runs in caller's transaction) | Can commit/rollback (own transaction control) |
| Use case | Computation, transformation, query | Multi-statement operations, batches |

The SQL standard distinguishes them; PostgreSQL follows the standard. Most other databases (Oracle, SQL Server) have had both for years.

### PL/pgSQL — the structure

PL/pgSQL is a block-structured language. The basic block:

```sql
CREATE OR REPLACE FUNCTION transfer(
    p_from BIGINT, p_to BIGINT, p_amount NUMERIC(18,2), p_idem TEXT
) RETURNS BIGINT AS $$
DECLARE
    v_transfer_id BIGINT;
    v_was_inserted BOOLEAN;
BEGIN
    -- 1. Idempotent insert of the transfer row
    INSERT INTO transfers (from_account_id, to_account_id, amount, status, idempotency_key)
    VALUES (p_from, p_to, p_amount, 'PENDING', p_idem)
    ON CONFLICT (idempotency_key) DO UPDATE
    SET status = transfers.status
    RETURNING id, (xmax = 0) INTO v_transfer_id, v_was_inserted;

    -- 2. If this is a retry, return the existing transfer id
    IF NOT v_was_inserted THEN
        RETURN v_transfer_id;
    END IF;

    -- 3. Debit and credit
    UPDATE accounts SET balance = balance - p_amount
    WHERE id = p_from AND status = 'ACTIVE'
      AND balance - p_amount >= -overdraft_limit;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Debit failed for account %', p_from;
    END IF;

    UPDATE accounts SET balance = balance + p_amount
    WHERE id = p_to AND status IN ('ACTIVE','FROZEN');
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Credit failed for account %', p_to;
    END IF;

    -- 4. Ledger entries
    INSERT INTO ledger_entries (account_id, transfer_id, amount, idempotency_key)
    VALUES
        (p_from, v_transfer_id, -p_amount, p_idem || '-debit'),
        (p_to,   v_transfer_id,  p_amount, p_idem || '-credit')
    ON CONFLICT (idempotency_key) DO NOTHING;

    -- 5. Mark complete
    UPDATE transfers SET status = 'COMPLETED', completed_at = now()
    WHERE id = v_transfer_id;

    RETURN v_transfer_id;
END;
$$ LANGUAGE plpgsql;
```

Components:

- `DECLARE` — local variables.
- `BEGIN ... END;` — the body.
- `INTO` — captures the result of a `SELECT` or `RETURNING` into a variable.
- `IF ... THEN ... END IF;` — conditional.
- `LOOP ... EXIT WHEN ...; END LOOP;` — iteration.
- `RAISE EXCEPTION` — raises an error and aborts the function (and the transaction, unless caught).
- `EXCEPTION WHEN ... THEN ...` — exception handler (uses a savepoint internally).

### When stored procedures are right

| Situation | Why a procedure fits |
|---|---|
| Encapsulating a multi-statement transaction | One call from the application, one round-trip, atomic |
| Reducing round-trips for chatty operations | Each SQL statement is a network call; a procedure is one call |
| Complex validation that depends on much data | Running it in the DB avoids shipping the data over the network |
| Batch jobs (interest accrual, statement generation) | Run overnight, in the database, with no client involvement |
| Operations called from many clients (Java service, Python script, BI tool) | Define once, call from anywhere |
| Security: callers should not have direct table access | Grant EXECUTE on the procedure; revoke SELECT on the tables |

### When stored procedures are wrong

| Situation | Why a procedure is the wrong choice |
|---|---|
| Business logic that changes often | Each change is a migration; deployment is coupled to the DB |
| Logic that needs to be tested | PL/pgSQL is hard to unit test; Java/Python have proper test frameworks |
| Logic that needs versioning | Multiple versions of a function require multiple names or schemas |
| Logic that needs to be shared with non-DB clients | A REST endpoint is more portable than a stored procedure |
| Logic that depends on external services | Stored procedures should not make HTTP calls (though they can, via extensions) |
| Logic that needs complex error handling | PL/pgSQL's exception handling is basic compared to Java's |

### The architectural trade-off

The deepest trade-off: **logic in the DB couples you to the DB.**

- **Pro**: the logic runs where the data lives. No data transfer. Atomicity is free (the procedure runs in one transaction).
- **Con**: the logic is now in the database. To change it, you need a migration. To test it, you need a running database. To version it, you need to manage function signatures. To move to a different database, you rewrite the logic. To scale the application tier independently of the database tier, you cannot — the logic is on the wrong tier.

For most OLTP applications, the right answer is: **keep business logic in the application tier; use stored procedures only for performance-critical encapsulation or for batch jobs.**

For data-warehouse-style workloads, the answer tilts toward procedures: the data is large, the queries are heavy, and the application tier is mostly a coordinator.

## Banking application

### The transfer procedure (in the DB)

```sql
-- PostgreSQL: transfer as a stored procedure
CREATE OR REPLACE PROCEDURE transfer(
    p_from BIGINT, p_to BIGINT, p_amount NUMERIC(18,2), p_idem TEXT
) LANGUAGE plpgsql AS $$
DECLARE
    v_transfer_id BIGINT;
    v_was_inserted BOOLEAN;
BEGIN
    -- The procedure manages its own transaction
    -- (Procedures can COMMIT/ROLLBACK; functions cannot.)

    INSERT INTO transfers (from_account_id, to_account_id, amount, status, idempotency_key)
    VALUES (p_from, p_to, p_amount, 'PENDING', p_idem)
    ON CONFLICT (idempotency_key) DO UPDATE
    SET status = transfers.status
    RETURNING id, (xmax = 0) INTO v_transfer_id, v_was_inserted;

    IF NOT v_was_inserted THEN
        -- Already processed; nothing to do.
        RETURN;
    END IF;

    -- Debit
    UPDATE accounts SET balance = balance - p_amount
    WHERE id = p_from AND status = 'ACTIVE'
      AND balance - p_amount >= -overdraft_limit;
    IF NOT FOUND THEN
        UPDATE transfers SET status = 'FAILED' WHERE id = v_transfer_id;
        COMMIT;
        RAISE EXCEPTION 'Debit failed for account %', p_from;
    END IF;

    -- Credit
    UPDATE accounts SET balance = balance + p_amount
    WHERE id = p_to AND status IN ('ACTIVE','FROZEN');
    IF NOT FOUND THEN
        UPDATE transfers SET status = 'FAILED' WHERE id = v_transfer_id;
        COMMIT;
        RAISE EXCEPTION 'Credit failed for account %', p_to;
    END IF;

    -- Ledger entries
    INSERT INTO ledger_entries (account_id, transfer_id, amount, idempotency_key)
    VALUES
        (p_from, v_transfer_id, -p_amount, p_idem || '-debit'),
        (p_to,   v_transfer_id,  p_amount, p_idem || '-credit')
    ON CONFLICT (idempotency_key) DO NOTHING;

    -- Complete
    UPDATE transfers SET status = 'COMPLETED', completed_at = now()
    WHERE id = v_transfer_id;

    COMMIT;
END;
$$;

-- Call from SQL
CALL transfer(1, 2, 100.00, 'abc-123');
```

### The transfer service (in the application)

The same logic, in Java, using the patterns from [[04-Unit-of-Work]]:

```java
@Transactional(isolation = Isolation.SERIALIZABLE)
public Long transfer(TransferRequest req) {
    // 1. Idempotent insert
    TransferId id = transfers.insertOrReturnExisting(req);
    if (id.alreadyExisted()) return id.value();

    // 2. Debit
    Account src = accounts.findById(req.fromAccountId());
    if (src.status() != ACTIVE || src.balance().subtract(req.amount()).compareTo(src.overdraftLimit().negate()) < 0) {
        transfers.markFailed(id);
        throw new InsufficientFundsException(src.id());
    }
    accounts.debit(src.id(), req.amount());

    // 3. Credit
    Account dst = accounts.findById(req.toAccountId());
    if (dst.status() == CLOSED) {
        transfers.markFailed(id);
        throw new AccountClosedException(dst.id());
    }
    accounts.credit(dst.id(), req.amount());

    // 4. Ledger entries
    ledgerEntries.insertDebitCredit(id, src, dst, req.amount(), req.idempotencyKey());

    // 5. Complete
    transfers.markComplete(id);

    return id.value();
}
```

### Which to choose?

| Aspect | Stored procedure | Application service |
|---|---|---|
| Performance | One round-trip; runs in DB | Multiple round-trips (or batched) |
| Atomicity | Free (single transaction) | Requires `@Transactional` |
| Testability | Hard (needs DB) | Easy (mock the repository) |
| Versioning | Migration per change | Code deploy per change |
| Coupling | Couples logic to DB | Couples logic to language |
| Reuse | Callable from any client | Callable only from Java |
| Debugging | Limited tooling | Full IDE support |
| Scaling | Cannot scale independently of DB | Scales with application tier |

The vault's recommendation: **default to the application service. Use a stored procedure only when**:

1. The operation is called from many clients (Java, Python, BI tools) and the duplication cost is high.
2. The operation is performance-critical enough that round-trips matter (high call rate, low-latency requirement).
3. The operation is a batch job that runs entirely in the database (no application involvement needed).

For the Banking transfer: default to the application service. The performance difference is small (a few milliseconds of round-trip), and the testability gain is large. Reserve the procedure for batch jobs like daily interest accrual.

### Example: daily interest accrual (a good use of a procedure)

```sql
-- PostgreSQL: daily interest accrual as a stored procedure
-- This is a batch job that runs once per day. It iterates over savings accounts,
-- computes interest, and writes a ledger entry per account. Doing this in the
-- application would require fetching every savings account, computing in app code,
-- and writing back — many round-trips.

CREATE OR REPLACE PROCEDURE accrue_daily_interest() LANGUAGE plpgsql AS $$
DECLARE
    rec RECORD;
    v_interest NUMERIC(18,2);
BEGIN
    FOR rec IN
        SELECT sa.account_id, sa.interest_rate, a.balance
        FROM savings_accounts sa
        JOIN accounts a ON a.id = sa.account_id
        WHERE a.status = 'ACTIVE' AND a.balance > 0
    LOOP
        v_interest := ROUND(rec.balance * rec.interest_rate / 365, 2);
        IF v_interest <= 0 THEN
            CONTINUE;
        END IF;

        -- Update the account balance
        UPDATE accounts SET balance = balance + v_interest WHERE id = rec.account_id;

        -- Update the savings subtype
        UPDATE savings_accounts
        SET interest_accrued = interest_accrued + v_interest,
            last_accrual_at = now()
        WHERE account_id = rec.account_id;

        -- Write a ledger entry
        INSERT INTO ledger_entries (account_id, amount, idempotency_key)
        VALUES (rec.account_id, v_interest,
                'interest-' || rec.account_id || '-' || to_char(now(), 'YYYY-MM-DD'))
        ON CONFLICT (idempotency_key) DO NOTHING;
    END LOOP;

    COMMIT;
END;
$$;

-- Schedule it (PostgreSQL: pg_cron)
-- SELECT cron.schedule('daily_interest', '0 2 * * *', 'CALL accrue_daily_interest()');
```

This is a good use of a procedure: a batch job that runs entirely in the database, called from a scheduler, with no application involvement.

## What can go wrong

- **Business logic creeping into the DB.** Once a procedure exists, developers add to it. The procedure grows; testing becomes impossible; the database becomes the application.
- **Performance cliffs.** A procedure that loops over rows and runs a query per iteration is O(N × query cost). Use set-based SQL inside the procedure; avoid loops where possible.
- **Debugging difficulty.** PL/pgSQL has limited debugging tools compared to Java. Logs go to the database log, not the application log. Stack traces are less informative.
- **Versioning.** Changing a procedure's signature breaks every caller. Many teams resort to `transfer_v1`, `transfer_v2`, etc.
- **Migration risk.** A bad procedure update can break production instantly. There is no canary deploy for a stored procedure (without significant ceremony).
- **Hidden side effects.** A procedure that writes to multiple tables, sends notifications, and updates an audit log has side effects that callers cannot see from the call site.
- **Security.** A procedure running with `SECURITY DEFINER` runs as its owner, not as the caller. A flaw in the procedure is a privilege escalation.
- **Transaction surprises.** A procedure that calls `COMMIT` commits the caller's transaction too (in PostgreSQL 14+). Be explicit about transaction boundaries.

## Trade-offs

- **Logic in DB vs logic in app.** The deepest trade-off. Default to app; move to DB only with deliberate justification.
- **Function vs procedure.** Functions are composable (callable from SQL); procedures can manage their own transactions. Use functions for transformation; procedures for multi-statement operations.
- **Set-based vs procedural.** Set-based SQL is faster; procedural loops are clearer for some logic. Push toward set-based; use loops only when the logic cannot be expressed as a single statement.
- **Encapsulation vs testability.** A procedure encapsulates logic at the cost of testability. An application service is testable but requires multiple round-trips. Choose based on the call pattern.
- **`SECURITY DEFINER` vs `SECURITY INVOKER`.** `DEFINER` runs as the owner (more privileges); `INVOKER` runs as the caller (fewer privileges). Default to `INVOKER`; use `DEFINER` only when the procedure must perform privileged operations on behalf of unprivileged callers.
- **In-database scheduling vs external scheduler.** `pg_cron` runs in the database; an external scheduler (Airflow, Quartz) runs in the application tier. External is more flexible; in-database is simpler for database-only jobs.

## Forward links

- [[03-Triggers-As-Constraints]] — triggers and procedures share PL/pgSQL and the same trade-offs.
- [[04-Unit-of-Work]] — the application-layer alternative for transactional logic.
- [[06-Hibernate-JPA]] — the ORM perspective on stored procedures.
- [[00-ACID]] — procedures run inside transactions (or manage their own).
- [[04-MVCC]] — procedures see the same MVCC snapshots as their callers.
- [[09-Banking-SQL]] — the transfer as SQL, with the procedure as one option.
- [[05-Banking-Performance-Tuning]] — when procedures become a performance tool.
