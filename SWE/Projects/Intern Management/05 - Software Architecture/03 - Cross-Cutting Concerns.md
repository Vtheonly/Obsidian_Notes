---
tags: [concept, architecture, cross-cutting]
type: concept
status: complete
related:
  - [[05 - Software Architecture/10 - Layered Architecture]]
  - [[06 - Design Patterns/07 - Decorator Pattern]]
---

# Cross-Cutting Concerns

## What it is

A **cross-cutting concern** is a requirement that affects multiple layers or modules. Logging, security, transactions, caching, monitoring — these don't fit neatly into one layer; they cut across the whole application.

## Examples

- **Logging** — every layer logs.
- **Security** — every service method checks authorization.
- **Transactions** — every service method starts/commits a transaction.
- **Caching** — every repository call might be cached.
- **Error handling** — every controller catches exceptions and shows alerts.
- **Auditing** — every mutation is logged.
- **Metrics** — every method is timed.

## The problem

If you implement these inline:
```java
public Intern createIntern(Intern intern) {
    log.info("Creating intern: {}", intern);
    authz.check(Permission.CREATE_INTERN);
    metrics.start("createIntern");
    try {
        transaction.begin();
        Intern saved = repository.save(intern);
        audit.log("CREATE", saved);
        transaction.commit();
        return saved;
    } catch (Exception e) {
        transaction.rollback();
        log.error("Failed", e);
        metrics.error("createIntern");
        throw e;
    } finally {
        metrics.stop("createIntern");
    }
}
```

The business logic is buried in cross-cutting concerns. Every method looks like this. DRY violation, readability nightmare.

## Solutions

### 1. Decorator pattern
Wrap the service in a decorator that adds the concern:
```java
public class LoggingInternService implements InternService {
    private final InternService delegate;
    public Intern createIntern(Intern intern) {
        log.info("Creating intern: {}", intern);
        return delegate.createIntern(intern);
    }
}

InternService service = new LoggingInternService(
    new TransactionalInternService(
        new CachingInternService(
            new InternServiceImpl(repository)
        )
    )
);
```

### 2. AOP (Aspect-Oriented Programming)
Define aspects (annotations like `@Transactional`, `@Logged`, `@Cached`) that are applied at runtime:
```java
@Transactional
@Logged
public Intern createIntern(Intern intern) {
    return repository.save(intern);  // no boilerplate
}
```

Spring AOP weaves the aspects into the method at runtime.

### 3. Pipeline / Middleware
Compose functions:
```java
InternService createIntern = withLogging(withTransactions(withAuthz(baseService::createIntern)));
```

### 4. Functional wrappers
```java
public <T> T withMetrics(String name, Supplier<T> supplier) {
    long start = System.nanoTime();
    try {
        return supplier.get();
    } finally {
        metrics.record(name, System.nanoTime() - start);
    }
}

Intern saved = withMetrics("createIntern", () -> repository.save(intern));
```

## Spring's approach

Spring uses AOP for transactions (`@Transactional`), security (`@PreAuthorize`), caching (`@Cacheable`), and JMX (`@ManagedAttribute`). You annotate, Spring weaves.

## Project Connection

The project has zero cross-cutting concern handling. No logging (just `System.out.println`), no security (just `if (roleId == 4)`), no transactions (auto-commit), no caching, no metrics. The fix introduces these via decorators or AOP.

## Common pitfalls

- **Inline cross-cutting logic** — every method has the same logging/transaction boilerplate. Extract.
- **AOP overuse** — aspects everywhere, hard to debug. Use sparingly.
- **Hidden behavior** — AOP can make code behave in surprising ways (the annotation does something invisible). Document clearly.

## Further reading

- *AspectJ in Action* (Laddad).
- Spring AOP documentation.
