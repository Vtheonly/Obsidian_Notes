---
tags: [concept, database, oracle, security, data-redaction]
type: concept
status: complete
prerequisites:
  - [[12 - Advanced Database Features/16 - VPD - Virtual Private Database]]
related:
  - [[12 - Advanced Database Features/15 - Triggers]]
  - [[08 - Relational DB Foundations/17 - Schemas and Users in Oracle]]
---

# Data Redaction

## What it is

**Data Redaction** (via `DBMS_REDACT`) masks sensitive column values **at query time**, based on the user's session. The original data is stored unmasked; the redacted version is returned to queries. The user sees `***-**-****` instead of `123-45-6789`; the DBA sees `123-45-6789`.

Unlike VPD (which filters **rows**), Data Redaction masks **columns**. Unlike encryption (which protects data at rest), Data Redaction protects data **in transit to the client**.

```sql
BEGIN
    DBMS_REDACT.ADD_POLICY(
        object_schema  => 'APP_OWNER',
        object_name    => 'WORKER_USER',
        column_name    => 'PASSWORD_HASH',
        policy_name    => 'redact_password_hash',
        function_type  => DBMS_REDACT.FULL,
        function_parameters => NULL,           -- replace with NULL
        expression     => 'SYS_CONTEXT(''USERENV'',''SESSION_USER'') != ''APP_ADMIN'''
    );
END;
/
```

Now any non-admin user querying `worker_user.password_hash` gets NULL instead of the actual hash.

## Redaction function types

- **`FULL`** - always redact. Replace the value with a fixed value (NULL, 0, blank).
- **`NULLIFY`** (12c+) - replace with NULL.
- **`PARTIAL`** - redact part of the value. E.g., `123-45-6789` -> `***-**-6789`.
- **`REGEXP`** - redact based on a regular expression.
- **`RANDOM`** - replace with a random value of the same type.

```sql
-- Partial: redact the SSN except the last 4 digits
DBMS_REDACT.ADD_POLICY(
    ...
    function_type      => DBMS_REDACT.PARTIAL,
    function_parameters => 'DBMS_REDACT.REDACT_US_SSN_LEADING, 1, 5'
);
```

## The expression

The `expression` parameter is a SQL predicate that determines when redaction applies:

```sql
expression => 'SYS_CONTEXT(''USERENV'',''SESSION_USER'') != ''APP_ADMIN'''
```

Redaction applies when the expression is true. Common patterns:

- "Redact for everyone except the `HR_ADMIN` role."
- "Redact for users whose `CLIENT_IDENTIFIER` is not in the audit list."
- "Redact only when connecting from outside the corporate subnet" (using `SYS_CONTEXT('USERENV','IP_ADDRESS')`).

## Why Data Redaction

- **Defense in depth**. Even if an attacker gets SQL\*Plus access, they see masked data.
- **Compliance**. GDPR, HIPAA, PCI-DSS require masking of PII/PHI/card data for non-privileged users.
- **Logging safety**. Application logs that accidentally dump query results show masked values.
- **Demo / test environments**. Real data, masked, for training and UAT.

Compare to application-side masking, where every DAO must remember to mask - one missed path leaks the data.

## What Data Redaction does NOT do

- It does **not** encrypt the data at rest. The columns are stored in plaintext. Use **Transparent Data Encryption (TDE)** for at-rest protection.
- It does **not** prevent users with `EXEMPT REDACTION POLICY` from seeing the data. Grant this privilege only to DBAs.
- It does **not** protect against `INSERT` or `UPDATE` - users can still write sensitive data; they just can't read it back. (Use [[08 - Relational DB Foundations/02 - Constraints]] and CHECK for write-side protection.)

## Project Connection

The project stores `password_hash` as **plaintext** (`'rootroot'` - see [[01 - Code Walkthrough/04 - SQL Scripts]]). Even hashing it properly would leave the hashes visible to anyone with `SELECT` access - and password hashes are sensitive (they can be brute-forced offline).

The reviews' redesign proposes Data Redaction on `password_hash`:

```sql
BEGIN
    DBMS_REDACT.ADD_POLICY(
        object_schema  => 'APP_OWNER',
        object_name    => 'WORKER_USER',
        column_name    => 'PASSWORD_HASH',
        policy_name    => 'redact_password_hash',
        function_type  => DBMS_REDACT.FULL,
        function_parameters => NULL,
        expression     => '1=1'   -- redact for everyone; the app never needs to read it back
    );
END;
/
```

The app never needs to `SELECT password_hash` and read it back; it needs to `SELECT password_hash WHERE username = ?` and compare in-memory. With redaction set to `FULL` returning NULL, even that comparison breaks - so the policy should either:
- Redact only for non-app sessions (via `CLIENT_IDENTIFIER`).
- Use a dedicated `verify_password` stored procedure that does the comparison inside the database.

## Common pitfalls

- Redacting a column the app needs to read - the app breaks silently (it gets NULL instead of the hash, and the login fails).
- Forgetting that redaction applies to all query paths - including exports, replication, and trace files. (Mostly true; some admin paths are exempt.)
- Not testing with the actual application user - the DBA sees the unredacted data and thinks everything's fine.

## Trade-offs

- **Security vs. usability**: redaction protects data but breaks queries that need the value.
- **At-rest vs. in-transit**: Data Redaction protects in-transit; TDE protects at-rest. Use both.

## Further reading

- Oracle Docs, "DBMS_REDACT", "Data Redaction".
- [[12 - Advanced Database Features/16 - VPD - Virtual Private Database]]
