---
tags: [concept, architecture, exceptions]
type: concept
status: complete
related:
  - [[03 - Java Foundations/02 - Exception Handling]]
  - [[05 - Software Architecture/10 - Layered Architecture]]
---

# Exception Translation

## What it is

**Exception translation** is converting a low-level exception (e.g., `SQLException`) into a higher-level, domain-specific exception (e.g., `DuplicateEmailException`) at the layer boundary.

```java
// In the repository (low-level)
public void save(Intern intern) {
    try {
        // JDBC insert
    } catch (SQLException e) {
        if (e.getErrorCode() == 1) {  // ORA-00001: unique constraint violated
            throw new DuplicateEmailException(intern.getEmail(), e);
        }
        throw new DataAccessException("Failed to save intern", e);
    }
}

// In the controller (high-level)
try {
    internService.createIntern(cmd);
} catch (DuplicateEmailException e) {
    showError("This email is already registered.");
} catch (DataAccessException e) {
    showError("Database error. Please try again.");
}
```

## Why it matters

- **Decoupling** — the controller doesn't know about `SQLException` or Oracle error codes.
- **User-friendliness** — the controller can show "This email is already registered" instead of "ORA-00001: unique constraint (SYS_C001234) violated."
- **Security** — internal DB structure (constraint names, table names) is not leaked to the user.
- **Testability** — the service layer can be tested by asserting that it throws `DuplicateEmailException`, without needing a real DB.

## Spring's exception translation

Spring JDBC translates `SQLException` to a hierarchy of `DataAccessException` subclasses:
- `DataIntegrityViolationException` (unique constraint, FK violation)
- `DuplicateKeyException` (subclass of the above)
- `DataAccessException` (root)

Spring uses `SQLErrorCodeSQLExceptionTranslator` to map vendor-specific error codes to Spring exceptions. You write code against `DataAccessException`, not `SQLException`.

## The project's exception handling

```java
// oracleConnector catches SQLException and shows a JOptionPane
} catch (SQLException e) {
    JOptionPane.showMessageDialog(null, "Failed to insert intern: " + e.getMessage());
}
```

`e.getMessage()` for an Oracle unique violation returns something like `"ORA-00001: unique constraint (INTERN_MANEGEMENT.SYS_C001234) violated"`. This is shown to the user — leaking the schema name and constraint name.

## The fix

```java
// Repository: translate SQLException to domain exceptions
public class OracleInternRepository implements InternRepository {
    public void save(Intern intern) {
        try (Connection conn = dataSource.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            // ...
            ps.executeUpdate();
        } catch (SQLException e) {
            throw translate(e, intern);
        }
    }

    private RuntimeException translate(SQLException e, Intern intern) {
        switch (e.getErrorCode()) {
            case 1:    // ORA-00001
                return new DuplicateEmailException(intern.getEmail(), e);
            case 2291: // ORA-02291: FK violation
                return new InvalidReferenceException(e);
            case 12899: // ORA-12899: value too large
                return new FieldTooLongException(e);
            default:
                return new DataAccessException("Database error", e);
        }
    }
}

// Controller: catch domain exceptions, show user-friendly messages
try {
    internService.createIntern(cmd);
    showSuccess("Intern created.");
} catch (DuplicateEmailException e) {
    showError("This email is already registered.");
} catch (FieldTooLongException e) {
    showError("One of the fields is too long.");
} catch (ValidationException e) {
    showError(e.getMessage());
}
```

## Common pitfalls

- **Catching and swallowing** — `catch (SQLException e) {}` loses information. At minimum, log and rethrow.
- **Catching too broad** — `catch (Exception e)` catches everything including `NullPointerException`. Catch specific exceptions.
- **Not preserving the cause** — `throw new MyException("msg")` loses the original. Always pass the cause: `throw new MyException("msg", e)`.
- **Showing raw exception messages to users** — leaks internals. Translate to user-friendly messages.

## Further reading

- *Effective Java* (Bloch), Item 73 (throw exceptions appropriate to the abstraction).
- Spring `DataAccessException` hierarchy.
