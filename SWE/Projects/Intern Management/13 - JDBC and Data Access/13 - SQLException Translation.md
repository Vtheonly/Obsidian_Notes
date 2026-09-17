---
tags: [concept, jdbc, exceptions, translation]
type: concept
status: complete
related:
  - [[05 - Software Architecture/06 - Exception Translation]]
  - [[13 - JDBC and Data Access/14 - Spring JDBC (JdbcTemplate)]]
---

# SQLException Translation

## What it is

Converting low-level `SQLException` (with vendor-specific error codes) into domain-specific exceptions (`DuplicateEmailException`, `NotFoundException`).

## Why

- **Decoupling** — the service layer doesn't know about Oracle error codes.
- **User-friendliness** — "This email is already registered" vs. "ORA-00001: unique constraint violated."
- **Security** — don't leak schema/structure via error messages.

## Manual translation

```java
public void save(Intern intern) {
    try (Connection conn = dataSource.getConnection();
         PreparedStatement ps = conn.prepareStatement(sql)) {
        // ...
        ps.executeUpdate();
    } catch (SQLException e) {
        switch (e.getErrorCode()) {
            case 1:    // ORA-00001: unique constraint
                throw new DuplicateEmailException(intern.getEmail(), e);
            case 2291: // ORA-02291: FK violation
                throw new InvalidReferenceException(e);
            case 12899: // ORA-12899: value too large
                throw new FieldTooLongException(e);
            default:
                throw new DataAccessException("Database error", e);
        }
    }
}
```

## Spring's translation

Spring's `SQLErrorCodeSQLExceptionTranslator` does this automatically:
```java
// In a Spring @Repository:
@Repository
public class InternRepository {
    // JdbcTemplate catches SQLException, translates to DataAccessException
}

// Service catches Spring exceptions:
try {
    internService.createIntern(cmd);
} catch (DuplicateKeyException e) {
    showError("This email is already registered.");
} catch (DataIntegrityViolationException e) {
    showError("Data integrity error.");
}
```

## The exception hierarchy

```
DataAccessException (root)
├── NonTransientDataAccessException
│   ├── DataIntegrityViolationException
│   │   └── DuplicateKeyException
│   └── ...
├── TransientDataAccessException
│   ├── ConcurrencyFailureException
│   │   └── OptimisticLockingFailureException
│   └── ...
```

## Project Connection

The project shows `e.getMessage()` to the user — leaks Oracle error codes and constraint names. The fix: translate `SQLException` to domain exceptions at the repository boundary.

## Further reading

- Spring `DataAccessException` hierarchy.
