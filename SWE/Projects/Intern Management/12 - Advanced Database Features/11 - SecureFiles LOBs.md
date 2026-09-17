---
tags: [concept, database, lobs, securefiles]
type: concept
status: complete
related:
  - [[12 - Advanced Database Features/14 - Table Compression]]
---

# SecureFiles LOBs

## What it is

**SecureFiles** is Oracle's modern LOB storage (introduced in 11g), replacing the older **BasicFiles**. SecureFiles supports compression, deduplication, encryption, and caching.

## Syntax

```sql
CREATE TABLE themes (
    theme_id NUMBER PRIMARY KEY,
    theme_name VARCHAR2(150),
    description CLOB
) LOB (description) STORE AS SECUREFILE db_lob_theme_desc (
    COMPRESS HIGH
    CACHE
);
```

- `COMPRESS HIGH` — compress the LOB data.
- `CACHE` — keep frequently-accessed LOBs in the buffer cache.
- `DEDUPLICATE` — deduplicate identical LOBs.
- `ENCRYPT` — encrypt at rest (requires TDE).

## Why it's better than BasicFiles

| Feature | BasicFiles | SecureFiles |
|---|---|---|
| Compression | No | Yes |
| Deduplication | No | Yes |
| Encryption | Manual | Built-in |
| Performance | Slower | Faster |
| Max size | 4 GB (traditional) | 128 TB |

## When to use

- **Large text** — descriptions, comments, documents.
- **Binary data** — images, PDFs (BLOB).
- **When you need compression or encryption**.

## Project Connection

The advanced redesign stores `themes.description` as a SecureFiles CLOB:

```sql
CREATE TABLE themes (
    theme_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    theme_name VARCHAR2(150) NOT NULL,
    description CLOB,
    ...
) LOB (description) STORE AS SECUREFILE db_lob_theme_desc (COMPRESS HIGH CACHE);
```

With `CACHE`, frequently-read theme descriptions stay in the buffer pool — no disk reads.

## Further reading

- Oracle Database SecureFiles and Large Objects Developer's Guide.
