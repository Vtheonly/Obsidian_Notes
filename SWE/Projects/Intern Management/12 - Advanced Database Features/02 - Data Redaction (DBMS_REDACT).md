---
tags: [concept, database, security, redaction]
type: concept
status: complete
related:
  - [[12 - Advanced Database Features/17 - Virtual Private Database (VPD)]]
  - [[17 - Application Security/07 - PII Protection]]
---

# Data Redaction (DBMS_REDACT)

## What it is

**Data Redaction** masks sensitive columns (phone, email, SSN) for certain users, at query time. The data on disk is unredacted; the masking happens as the rows are returned.

## Why it exists

- **PII protection** — support agents shouldn't see full phone numbers.
- **Compliance** — GDPR requires minimizing access to personal data.
- **Security by design** — applications don't need to implement masking; the DB does it.

## Implementation

```sql
BEGIN
    DBMS_REDACT.ADD_POLICY(
        object_schema       => 'SYSTEM',
        object_name         => 'interns',
        policy_name         => 'redact_intern_pii',
        column_name         => 'phone_number',
        expression          => 'SYS_CONTEXT(''USERENV'', ''SESSION_USER'') NOT IN (''SYS'', ''SYSTEM'')',
        function_type       => DBMS_REDACT.PARTIAL,
        function_parameters => 'VVVFVVVV',  -- mask all but last 4
        masking_character   => '*',
        enable              => TRUE
    );
END;
/
```

- `expression` — when to apply the policy. Here: for everyone except SYS and SYSTEM.
- `function_type` — `PARTIAL` (mask part), `FULL` (mask all), `RANDOM` (random value), `REGEXP` (regex-based).
- `function_parameters` — for `PARTIAL`: `VVVFVVVV` means "show 3, mask 1, show 5" (or similar, depends on data type).

## Effect

```sql
-- As SYS:
SELECT phone_number FROM interns;
-- Returns: +213770123456

-- As a regular user:
SELECT phone_number FROM interns;
-- Returns: +213********56
```

The data on disk is unchanged. Only the query result is masked.

## Why this is powerful

- **No app changes** — the app writes `SELECT phone_number FROM interns`; the DB masks it.
- **Centralized policy** — one place to manage masking rules.
- **Auditable** — policies are visible in `DBA_REDACTION_POLICIES`.

## Trade-offs

- **Enterprise Edition feature** — may not be in XE.
- **Performance** — small overhead per row.
- **Doesn't encrypt at rest** — the data on disk is unredacted. Use TDE for at-rest encryption.

## Project Connection

The advanced redesign redacts `phone_number` for non-admin users. Combined with VPD (row-level security), this provides defense in depth:
- VPD: users see only their department's rows.
- Redaction: even within their department, phone numbers are masked.

## Further reading

- Oracle Database Security Guide — Data Redaction.
