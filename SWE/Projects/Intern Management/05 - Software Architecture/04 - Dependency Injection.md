---
tags: [concept, di, ioc]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/07 - Dependency Inversion Principle (DIP)]]
  - [[04 - OOD and SOLID/04 - Composition Root]]
  - [[05 - Software Architecture/09 - Inversion of Control]]
---

# Dependency Injection (DI)

> "Don't call us, we'll call you." — Hollywood Principle

## What it is

**Dependency Injection** is a technique where an object receives its dependencies from an external source, rather than creating them itself. The object declares what it needs (via constructor, setter, or field); a **container** (or test code) provides it.

```java
// Without DI: the class creates its own dependencies (tightly coupled)
public class LoginController {
    private OracleConnector connector = new OracleConnector();  // hard dependency
}

// With DI: the class declares its dependencies (loosely coupled)
public class LoginController {
    private final AuthService authService;

    public LoginController(AuthService authService) {  // injected
        this.authService = authService;
    }
}
```

## Three types of DI

### 1. Constructor injection (preferred)
```java
public class LoginController {
    private final AuthService authService;

    public LoginController(AuthService authService) {
        this.authService = authService;
    }
}
```
Pros: dependencies are clear; fields can be `final`; impossible to use the object half-constructed.
Cons: long constructor parameter lists for many dependencies.

### 2. Setter injection
```java
public class LoginController {
    private AuthService authService;

    public void setAuthService(AuthService authService) {
        this.authService = authService;
    }
}
```
Pros: optional dependencies; reconfigurable.
Cons: not `final`; possible to forget to call the setter.

### 3. Field injection (avoid)
```java
public class LoginController {
    @Inject private AuthService authService;  // injected via reflection
}
```
Pros: concise.
Cons: not `final`; requires reflection; hides dependencies; untestable without a container.

**Use constructor injection. Reserve setter injection for optional dependencies. Avoid field injection.**

## DI containers

A DI container (Spring, Guice, Dagger) automates the wiring:
1. You register your classes (via annotations like `@Component`, `@Service`, `@Repository` or via configuration).
2. The container inspects constructors and resolves dependencies.
3. The container creates and injects instances.

### Spring example
```java
@Service
public class InternService {
    private final InternRepository repository;
    public InternService(InternRepository repository) {
        this.repository = repository;
    }
}

@Repository
public class OracleInternRepository implements InternRepository { ... }

@SpringBootApplication
public class App {
    public static void main(String[] args) {
        SpringApplication.run(App.class, args);
    }
}
```
Spring scans for `@Service` and `@Repository`, sees that `InternService` needs an `InternRepository`, finds `OracleInternRepository`, and wires them.

### Manual DI (no container)
For a JavaFX desktop app, manual DI in the composition root is often simpler than Spring:

```java
public class App extends Application {
    @Override
    public void start(Stage stage) {
        HikariDataSource ds = createDataSource();
        InternRepository internRepo = new OracleInternRepository(ds);
        WorkerUserRepository userRepo = new OracleWorkerUserRepository(ds);
        AuthService auth = new AuthService(userRepo, new Argon2PasswordEncoder());
        InternService internService = new InternService(internRepo, new AuditService(ds));
        NavigationController nav = new NavigationController(stage, auth, internService);
        nav.showLogin();
    }
}
```

## Why DI matters

- **Testability** — inject mocks in tests. No need to launch the real DB.
- **Decoupling** — classes depend on interfaces, not concretions.
- **Flexibility** — swap implementations without touching consumers.
- **Clarity** — dependencies are explicit in the constructor signature.
- **Lifecyle management** — the container handles singletons, request-scoped, etc.

## "new is glue" (Mark Seemann)

Every `new` keyword creates a hard dependency. The composition root is where `new` is allowed. Everywhere else, inject.

## Common pitfalls

- **Service locator anti-pattern** — a global registry that hands out dependencies. Hides dependencies, makes testing harder.
- **Circular dependencies** — A depends on B, B depends on A. The container can't resolve this. Redesign.
- **Field injection** — looks clean but hides dependencies. Use constructor injection.
- **DI everywhere** — injecting a `String` or a `int` is overkill. Use configuration, not DI.

## Project Connection

The project has zero DI. Every class creates its own dependencies (`new oracleConnector()`, `static` initializers). The fix: introduce a composition root in `main.java` and constructor-inject dependencies.

## Further reading

- *Dependency Injection in .NET* (Seemann) — applies to Java too.
- Spring Framework documentation.
- *Clean Architecture* (Martin), Chapter 11 (DIP).
