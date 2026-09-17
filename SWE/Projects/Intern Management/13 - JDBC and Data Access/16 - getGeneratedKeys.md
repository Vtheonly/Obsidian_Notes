---
tags: [concept, jdbc, generated-keys]
type: concept
status: complete
related:
  - [[12 - Advanced Database Features/12 - Sequences and IDENTITY Columns]]
---

# getGeneratedKeys

## What it is

After an INSERT into a table with an auto-generated key (IDENTITY, sequence), `getGeneratedKeys()` retrieves the generated key.

## Usage

```java
String sql = "INSERT INTO interns (name, age) VALUES (?, ?)";
try (PreparedStatement ps = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
    ps.setString(1, "Alice");
    ps.setInt(2, 22);
    ps.executeUpdate();
    try (ResultSet keys = ps.getGeneratedKeys()) {
        if (keys.next()) {
            long id = keys.getLong(1);
            System.out.println("Generated ID: " + id);
        }
    }
}
```

## Why it matters

- **No second query** — you don't need `SELECT MAX(id)` (which is a race condition).
- **Atomic** — the key is returned with the INSERT.
- **Works with sequences and IDENTITY columns.**

## Project Connection

The project uses `MAX(id)+1` to generate IDs (race condition). The fix: IDENTITY columns + `RETURN_GENERATED_KEYS`.

## Further reading

- JDBC `Statement.RETURN_GENERATED_KEYS` documentation.
