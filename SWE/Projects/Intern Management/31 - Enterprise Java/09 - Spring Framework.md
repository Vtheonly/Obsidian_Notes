---
tags: [concept, enterprise, spring, framework]
type: concept
status: complete
related:
  - [[05 - Software Architecture/04 - Dependency Injection]]
  - [[16 - Authentication and Authorization/11 - Spring Security]]
---

# Spring Framework

## What it is

**Spring** is the most popular Java application framework. It provides:
- **DI container** (`@Component`, `@Autowired`).
- **AOP** (`@Transactional`, `@Security`).
- **JDBC** (`JdbcTemplate`).
- **ORM** (Spring Data JPA).
- **Web** (Spring MVC, Spring WebFlux).
- **Security** (Spring Security).
- **Boot** (auto-configuration, starters).

## Spring Boot

Spring Boot is opinionated Spring — auto-configures sensible defaults, embedded server, production-ready features.

```java
@SpringBootApplication
public class App {
    public static void main(String[] args) {
        SpringApplication.run(App.class, args);
    }
}

@Service
public class InternService {
    private final InternRepository repo;
    public InternService(InternRepository repo) { this.repo = repo; }  // auto-injected
}

@Repository
public interface InternRepository extends JpaRepository<Intern, Long> { }  // auto-implemented
```

## Why Spring for the project

The project is a JavaFX desktop app, not a web app. Spring Boot is overkill. But:
- **Spring DI** — useful for wiring up services and repositories.
- **Spring JDBC** — `JdbcTemplate` simplifies DB access.
- **Spring Security** — for auth (if the app evolves to a server).

For a desktop app, consider:
- **Manual DI** (composition root in `main.java`) — simplest.
- **Guice** — lightweight DI.
- **Spring** — full-featured, but heavy.

## Spring profiles

```java
@Service
@Profile("dev")
public class DevEmailService implements EmailService { ... }

@Service
@Profile("prod")
public class SmtpEmailService implements EmailService { ... }
```

`SPRING_PROFILES_ACTIVE=dev` selects the dev profile.

## application.yml

```yaml
spring:
  datasource:
    url: ${DB_URL}
    username: ${DB_USER}
    password: ${DB_PASSWORD}
  flyway:
    enabled: true
logging:
  level:
    com.example: DEBUG
```

Externalized, environment-specific config.

## Project Connection

For the desktop app, manual DI in `main.java` is sufficient. If the app evolves to a REST API, Spring Boot is the natural choice.

## Further reading

- Spring Framework documentation.
- Spring Boot reference.
