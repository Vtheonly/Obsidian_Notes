---
tags: [concept, database, normalization, 1nf]
type: concept
status: complete
---

# First Normal Form (1NF)

## The rule

A table is in **1NF** if:
1. All columns contain **atomic** (indivisible) values.
2. Each row is unique (has a PK).
3. No repeating groups (no lists, arrays, or comma-separated values in a column).

## Violation

```sql
CREATE TABLE interns (
    intern_id NUMBER PRIMARY KEY,
    name VARCHAR2(100),
    themes VARCHAR2(500)  -- "AI, Web, Mobile" — violates 1NF
);
```

The `themes` column holds a comma-separated list. You can't query "find interns interested in Web" efficiently (need `LIKE '%Web%'`, which is O(N) and false-positive-prone).

## Fix

Create a junction table:
```sql
CREATE TABLE interns (
    intern_id NUMBER PRIMARY KEY,
    name VARCHAR2(100)
);

CREATE TABLE themes (
    theme_id NUMBER PRIMARY KEY,
    theme_name VARCHAR2(100)
);

CREATE TABLE intern_themes (  -- junction
    intern_id NUMBER REFERENCES interns(intern_id),
    theme_id NUMBER REFERENCES themes(theme_id),
    PRIMARY KEY (intern_id, theme_id)
);
```

Now "find interns interested in Web":
```sql
SELECT i.name FROM interns i
JOIN intern_themes it ON i.intern_id = it.intern_id
JOIN themes t ON it.theme_id = t.theme_id
WHERE t.theme_name = 'Web';
```

## Project Connection

The project's schema is in 1NF — no comma-separated lists. Good.

## Further reading

- *SQL Antipatterns* (Karwin), "Jaywalking" (comma-separated lists).
