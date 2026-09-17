---
tags: [concept, di, composition-root]
type: concept
status: complete
related:
  - [[05 - Software Architecture/04 - Dependency Injection]]
  - [[04 - OOD and SOLID/07 - Dependency Inversion Principle (DIP)]]
---

# Composition Root

## What it is

The **composition root** is the single place in your application where you wire up dependencies — where you say "create an `OracleInternRepository` with this `DataSource`, create an `InternService` with this repository, create an `InternSearchController` with this service."

> "new is glue." — Mark Seemann

Every `new` keyword creates a hard dependency. The composition root is where those `new`s are allowed. Everywhere else, dependencies are **injected**.

## Why it matters

- **Single place** — all wiring is in one place, easy to understand and change.
- **No hidden dependencies** — every class declares its dependencies via constructor; the composition root satisfies them.
- **Testability** — in tests, you build a different composition root (with mocks).

## Example

```java
// main.java — the composition root
public class InternManagementApp extends Application {
    @Override
    public void start(Stage stage) {
        // Wire up dependencies
        HikariDataSource dataSource = createDataSource();
        InternRepository internRepo = new OracleInternRepository(dataSource);
        WorkerUserRepository userRepo = new OracleWorkerUserRepository(dataSource);
        AuthService authService = new AuthService(userRepo, new Argon2PasswordEncoder());
        InternService internService = new InternService(internRepo);
        NavigationController nav = new NavigationController(stage, authService, internService);

        nav.showLogin();
    }

    private HikariDataSource createDataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(System.getenv("DB_URL"));
        // ...
        return new HikariDataSource(config);
    }
}
```

Every other class receives its dependencies via constructor — no `new` inside services or controllers.

## With a DI container

For larger apps, use a DI container (Spring, Guice, Dagger):
```java
// Spring Boot
@SpringBootApplication
public class InternManagementApp {
    public static void main(String[] args) {
        SpringApplication.run(InternManagementApp.class, args);
    }
}

@Service
public class InternService {
    private final InternRepository repository;
    public InternService(InternRepository repository) {  // Spring injects
        this.repository = repository;
    }
}
```

The container scans for `@Service`, `@Repository`, `@Component` annotations and wires them automatically.

## Common pitfalls

- **`new` outside the composition root** — every `new` is a hidden dependency. Inject instead.
- **Static factory methods called from anywhere** — same as `new`. Inject the factory.
- **`ServiceLocator` pattern** — a global registry that hands out dependencies. Anti-pattern; hides dependencies.
- **Circular dependencies** — A depends on B, B depends on A. The container can't wire this. Redesign.

## Project Connection

The project has no composition root. Every class constructs its own dependencies (`new oracleConnector()` in controllers, `static` initializers everywhere). The fix: introduce a composition root in `main.java` that wires everything up.

See [[05 - Software Architecture/04 - Dependency Injection]].
