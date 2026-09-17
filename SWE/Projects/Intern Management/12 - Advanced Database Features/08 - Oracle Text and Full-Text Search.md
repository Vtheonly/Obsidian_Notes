---
tags: [concept, database, oracle-text, search]
type: concept
status: complete
related:
  - [[31 - Enterprise Java/01 - Apache Lucene]]
---

# Oracle Text and Full-Text Search

## What it is

**Oracle Text** is Oracle's full-text search engine. It indexes text content (CLOBs, documents) and supports `CONTAINS` queries — much more powerful than `LIKE`.

## Why `LIKE` is bad for search

```sql
SELECT * FROM interns WHERE name LIKE '%ali%';
```

- Leading wildcard (`%ali`) prevents index usage — full scan.
- No relevance ranking.
- No stemming (run ≠ running).
- No synonyms.
- No typo tolerance.

## Oracle Text

```sql
-- Create a context index
CREATE INDEX idx_interns_name_ctx ON interns(name) INDEXTYPE IS CTXSYS.CONTEXT;

-- Search
SELECT * FROM interns WHERE CONTAINS(name, 'ali', 1) > 0;
-- Returns rows where 'name' contains 'ali' (or 'Alice', 'Alison' — stemmed).
```

Features:
- **Relevance ranking** — `SCORE(1)` returns a relevance score.
- **Stemming** — `run` matches `running`, `ran`.
- **Fuzzy matching** — `?ali` matches typos.
- **Boolean** — `ali AND bob`, `ali OR bob`, `ali NOT bob`.
- **Phrase** — `"ali smith"` matches the phrase.

## Alternatives

- **Apache Lucene** (embedded in Java) — see [[31 - Enterprise Java/01 - Apache Lucene]].
- **Elasticsearch** — distributed, scalable full-text search.
- **PostgreSQL `tsvector` / `tsquery`** — built-in full-text search.

## Project Connection

The project uses `LIKE '%name%'` for search — slow and limited. The fix could be Oracle Text (if staying on Oracle) or Apache Lucene (embedded in the Java app) for in-memory full-text search.

For the intern management app (a few thousand interns), a simple B-tree index on `UPPER(name)` with `WHERE UPPER(name) LIKE 'ALI%'` (no leading wildcard) is probably sufficient. Oracle Text is overkill.

## Further reading

- Oracle Text Application Developer's Guide.
