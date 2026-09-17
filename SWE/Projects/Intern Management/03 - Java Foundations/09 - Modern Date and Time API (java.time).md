---
tags: [concept, java, date-time]
type: concept
status: complete
related:
  - [[08 - Relational DB Foundations/08 - Oracle Data Types]]
---

# Modern Date and Time API (java.time)

## What it is

Java 8 (2014) introduced `java.time` (JSR 310), replacing the legacy `java.util.Date` and `java.util.Calendar`. `java.time` is immutable, thread-safe, and well-designed.

## Core classes

| Class | Represents | Example |
|---|---|---|
| `LocalDate` | Date without time or timezone | 2026-07-13 |
| `LocalTime` | Time without date | 14:30:00 |
| `LocalDateTime` | Date + time without timezone | 2026-07-13T14:30:00 |
| `ZonedDateTime` | Date + time + timezone | 2026-07-13T14:30:00+01:00[Africa/Algiers] |
| `Instant` | Point on the UTC timeline | 2026-07-13T13:30:00Z |
| `Duration` | Time-based amount (hours, minutes, seconds) | PT1H30M |
| `Period` | Date-based amount (years, months, days) | P1Y2M3D |
| `DateTimeFormatter` | Formatting and parsing | yyyy-MM-dd |

## Why it's better than `Date`

- **Immutable** — no `setYear()` method that mutates the object. Thread-safe.
- **Type-safe** — `LocalDate` is a date, `LocalTime` is a time, `Instant` is a moment. No confusion.
- **Timezone-aware** — `ZonedDateTime` handles DST, offset, and zone rules.
- **Parseable** — `LocalDate.parse("2026-07-13")` works. `Date.parse("...")` is deprecated.

## JDBC mapping

| SQL type | Java type |
|---|---|
| `DATE` | `java.sql.Date` → `LocalDate` via `toLocalDate()` |
| `TIME` | `java.sql.Time` → `LocalTime` via `toLocalTime()` |
| `TIMESTAMP` | `java.sql.Timestamp` → `LocalDateTime` via `toLocalDateTime()` |
| `TIMESTAMP WITH TIME ZONE` | `OffsetDateTime` (via `ResultSet.getObject(col, OffsetDateTime.class)`) |

## Common pitfalls

- Using `java.util.Date` — use `java.time.*`.
- Using `SimpleDateFormat` — not thread-safe. Use `DateTimeFormatter` (thread-safe).
- Forgetting that `LocalDateTime` has no timezone — use `ZonedDateTime` or `Instant` for moments.
- Storing `LocalDateTime` in the DB when you mean a moment — store `Instant` or `OffsetDateTime`.

## Project Connection

- `oracleConnector.searchIntern` does `LocalDate.parse(value)` for date filters — no try/catch. `DateTimeParseException` propagates.
- `insertionInternController` overwrites `start_date`/`end_date` to `null` with TODO comments — the date is validated but discarded.
- The advanced schema uses `TIMESTAMP WITH LOCAL TIME ZONE` for `created_at`/`updated_at`/`deleted_at` — correct for audit columns (stores in DB timezone, displays in session timezone).
- `oracleConnector.searchIntern` does `Date.valueOf(LocalDate.parse(value))` — converts `String` → `LocalDate` → `java.sql.Date`. Correct but fragile.

### Fix

```java
private Intern mapRowToIntern(ResultSet rs) throws SQLException {
    Date sqlDate = rs.getDate("start_date");
    LocalDate start = (sqlDate != null) ? sqlDate.toLocalDate() : null;
    return new Intern(
        rs.getLong("intern_id"),
        rs.getString("name"),
        rs.getInt("age"),
        rs.getString("email"),
        rs.getString("university"),
        rs.getString("phone_number"),
        start,
        DecisionStatus.valueOf(rs.getString("status").toUpperCase()),
        rs.getObject("theme_id", Integer.class)  // handles null
    );
}
```

## Further reading

- *Java 8 in Action* (Urma, Fusco, Mycroft), Chapter 5.
- `java.time` package documentation.
