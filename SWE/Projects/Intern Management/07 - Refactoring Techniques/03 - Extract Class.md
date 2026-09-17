---
tags: [concept, refactoring, extract-class]
type: concept
status: complete
related:
  - [[07 - Refactoring Techniques/12 - What Is Refactoring]]
  - [[04 - OOD and SOLID/10 - God Class (God Object)]]
---

# Extract Class

## What it is

**Extract Class** is the refactoring that splits a class with multiple responsibilities into multiple classes, each with one responsibility.

## When to use

- The class has multiple unrelated responsibilities (SRP violation).
- The class is too large (> 300-500 LOC).
- The class has "personality splits" — some methods use one group of fields, others use a different group.

## Steps

1. Identify a cohesive cluster of fields and methods.
2. Create a new class.
3. Move the fields to the new class (use IDE refactoring).
4. Move the methods to the new class.
5. Have the original class hold a reference to the new class.
6. Update callers (if the methods were public, the original class may need to delegate).
7. Run tests after each step.

## Example: splitting `oracleConnector`

```java
// Before: 940-line God Class
public class oracleConnector {
    private static Connection connection;
    public static boolean login(...) { ... }
    public static void insertIntern(...) { ... }
    public static List<Map<String,Object>> searchIntern(...) { ... }
    public static int getMaxId(...) { ... }
    // ... 25 more methods
}

// After: 4 classes
public class ConnectionManager {  // responsibility: pool lifecycle
    private final HikariDataSource dataSource;
    public Connection getConnection() { return dataSource.getConnection(); }
}

public class OracleInternRepository implements InternRepository {  // responsibility: intern CRUD
    private final DataSource dataSource;
    public void save(Intern intern) { ... }
    public Optional<Intern> findById(long id) { ... }
}

public class AuthService {  // responsibility: authentication
    private final UserRepository users;
    private final PasswordEncoder encoder;
    public Optional<AuthenticatedUser> authenticate(String username, char[] password) { ... }
}

public class InternIdGenerator {  // responsibility: ID generation (replaced by IDENTITY columns)
    // ... or just delete this class and use Oracle IDENTITY
}
```

## Common pitfalls

- **Extracting too much** — splitting a cohesive class into many tiny classes that always change together.
- **Extracting too little** — leaving the original class still too big.
- **Forgetting to update callers** — after extraction, callers may need to use the new class.

## Further reading

- *Refactoring* (Fowler), "Extract Class".
