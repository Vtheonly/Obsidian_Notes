---
tags: [concept, database, oracle, types]
type: concept
status: complete
related:
  - [[02 - CS Foundations/06 - Floating Point and Numeric Precision]]
  - [[02 - CS Foundations/03 - Character Encoding (Unicode, UTF-8)]]
---

# Oracle Data Types

## Numeric

| Type | Description |
|---|---|
| `NUMBER(p, s)` | Decimal number with precision `p` (1-38 digits) and scale `s` (digits after decimal). Exact. |
| `NUMBER` (no args) | Unlimited precision floating-point (decimal). |
| `NUMBER(10)` | 10-digit integer (scale 0). Use for IDs. |
| `NUMBER(3)` | 3-digit integer. Use for age. |
| `BINARY_FLOAT` | 32-bit IEEE float. |
| `BINARY_DOUBLE` | 64-bit IEEE double. |

**Always use `NUMBER` for money, IDs, and counts.** Never use `BINARY_FLOAT`/`BINARY_DOUBLE` for money (floating-point errors).

## String

| Type | Description |
|---|---|
| `VARCHAR2(n BYTE)` | Variable-length string, max `n` bytes. |
| `VARCHAR2(n CHAR)` | Variable-length string, max `n` characters (multibyte-safe). |
| `CHAR(n)` | Fixed-length, padded with spaces. Rarely useful. |
| `NCHAR` / `NVARCHAR2` | Unicode (National Character Set). |
| `CLOB` | Character Large Object (up to 128 TB). Use for long text. |

**Always use `VARCHAR2(n CHAR)` for strings.** The `CHAR` semantics ensure multibyte characters fit.

## Date/Time

| Type | Description |
|---|---|
| `DATE` | Date + time (second precision). No timezone. |
| `TIMESTAMP` | Date + time + fractional seconds. No timezone. |
| `TIMESTAMP WITH TIME ZONE` | Timestamp + timezone offset. |
| `TIMESTAMP WITH LOCAL TIME ZONE` | Stored in DB timezone, displayed in session timezone. |
| `INTERVAL YEAR TO MONTH` | A period of years and months. |
| `INTERVAL DAY TO SECOND` | A period of days, hours, minutes, seconds. |

**Use `TIMESTAMP WITH LOCAL TIME ZONE` for audit columns** — it normalizes to DB time but displays in user time.

## LOB

| Type | Description |
|---|---|
| `CLOB` | Character LOB. |
| `NCLOB` | National Character Set LOB. |
| `BLOB` | Binary LOB (images, PDFs). |
| `BFILE` | Pointer to an external file. |

Oracle 11g+ has **SecureFiles LOBs** (high-performance, compressed, deduplicated, encrypted) vs the older **BasicFiles LOBs**.

## Other

| Type | Description |
|---|---|
| `ROWID` | Physical row address (base 64). |
| `UROWID` | Universal rowid (for index-organized tables). |
| `XMLTYPE` | XML data. |
| `JSON` | JSON data (Oracle 21c+). |
| `RAW(n)` | Raw binary, max 2000 bytes. |
| `LONG` / `LONG RAW` | Deprecated. Use CLOB/BLOB. |

## Project Connection

The project's schema uses:
- `NUMBER(10)` for IDs — correct.
- `NUMBER(3)` for age — correct.
- `VARCHAR2(n CHAR)` — correct (character semantics).
- `DATE` for `start_date` — OK but lacks timezone. The advanced redesign uses `TIMESTAMP WITH LOCAL TIME ZONE` for `created_at`/`updated_at`/`deleted_at`.
- `VARCHAR2(255)` for `password_hash` — generous enough for hex-encoded SHA-256 (64 chars), BCrypt (60 chars), or Argon2id (~100 chars).
- No CLOBs — the `theme.description` column should be a CLOB (SecureFiles in the redesign).

The `requstes.sql` schema incorrectly uses `VARCHAR2(255)` for primary keys — strings as IDs. The fix: `NUMBER(10)` IDs everywhere.

## Further reading

- Oracle Database SQL Language Reference — Data Types.
