---
tags: [concept, ioc, di]
type: concept
status: complete
related:
  - [[05 - Software Architecture/04 - Dependency Injection]]
  - [[04 - OOD and SOLID/07 - Dependency Inversion Principle (DIP)]]
---

# Inversion of Control (IoC)

> "Don't call us, we'll call you." — Hollywood Principle

## What it is

**Inversion of Control** is a broader principle than DI. In traditional programming, your code calls framework/library code. In IoC, the framework calls your code. The control flow is inverted.

## Examples

### Traditional (you call the framework)
```java
public class App {
    public static void main(String[] args) {
        Connection conn = DriverManager.getConnection(...);
        ResultSet rs = conn.createStatement().executeQuery("SELECT ...");
        while (rs.next()) {
            System.out.println(rs.getString(1));
        }
        conn.close();
    }
}
```

### IoC (the framework calls you)
```java
@SpringBootApplication
public class App {
    public static void main(String[] args) {
        SpringApplication.run(App.class, args);  // framework takes over
    }
}

@RestController
public class InternController {
    @GetMapping("/interns")
    public List<Intern> list() {  // framework calls this when /interns is hit
        return internService.findAll();
    }
}
```

The framework (Spring) handles startup, HTTP routing, dependency wiring, lifecycle. Your code just declares what should happen.

## Forms of IoC

1. **Dependency Injection** — the framework injects dependencies. (Most common form.)
2. **Template Method** — the framework defines an algorithm skeleton; you override specific steps.
3. **Event-driven** — you register handlers; the framework calls them when events occur.
4. **Lifecycle callbacks** — `@PostConstruct`, `@PreDestroy`; the framework calls them at the right time.

## Why it matters

- **Decoupling** — your code doesn't know about the framework's internals.
- **Reuse** — the framework handles common concerns (routing, transactions, security).
- **Testability** — your code is plain POJOs, testable in isolation.

## Project Connection

The project has no IoC. `main.java` calls JavaFX (`Application.launch`), but after that, every class is procedural — it directly calls `oracleConnector`, directly creates `Stage`s, directly handles everything. There's no framework managing lifecycle or dependencies.

## Common pitfalls

- **"IoC container" vs "IoC"** — IoC is the principle; an IoC container (Spring, Guice) is a tool that implements DI, which is one form of IoC.
- **Framework lock-in** — heavy IoC framework use can make your code hard to test without the framework. Use plain POJOs where possible.
- **Over-inversion** — don't invert control for the sake of it. Invert when the framework genuinely manages lifecycle or routing.

## Further reading

- Fowler, "Inversion of Control Containers and the Dependency Injection pattern" (martinfowler.com, 2004).
