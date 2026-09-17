---
tags: [concept, testing, testcontainers, integration]
type: concept
status: complete
related:
  - [[27 - Testing/02 - JUnit 5]]
---

# Testcontainers

## What it is

**Testcontainers** spins up real Docker containers (Oracle, PostgreSQL, Redis, etc.) for integration tests. Each test gets a clean, real environment.

## Maven dependency

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers</artifactId>
    <version>1.19.3</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>oracle-xe</artifactId>
    <version>1.19.3</version>
    <scope>test</scope>
</dependency>
```

## Usage

```java
class InternRepositoryIT {
    private static OracleContainer oracle;
    private static InternRepository repository;

    @BeforeAll
    static void setUp() {
        oracle = new OracleContainer("gvenzl/oracle-xe:21-slim");
        oracle.start();

        HikariDataSource ds = new HikariDataSource(new HikariConfig());
        ds.setJdbcUrl(oracle.getJdbcUrl());
        ds.setUsername(oracle.getUsername());
        ds.setPassword(oracle.getPassword());

        repository = new OracleInternRepository(ds);

        // Run migrations
        Flyway.configure().dataSource(ds).load().migrate();
    }

    @AfterAll
    static void tearDown() {
        oracle.stop();
    }

    @Test
    void shouldSaveAndFind() {
        Intern intern = new Intern("Alice", 22, "alice@example.com");
        repository.save(intern);

        Optional<Intern> found = repository.findById(intern.getId());
        assertTrue(found.isPresent());
        assertEquals("Alice", found.get().getName());
    }
}
```

## Why

- **Real DB** — catches SQL dialect issues, constraint violations, type mismatches that mocks miss.
- **Isolated** — each test class gets a fresh DB.
- **Reproducible** — same DB version every time.
- **CI-friendly** — Docker is available on all CI runners.

## Trade-offs

- **Slow** — container startup takes ~30 sec. Use `@Testcontainers` + shared container pattern.
- **Requires Docker** — on developer machines and CI.

## Project Connection

The project's `oracleConnector` is untestable (static, no DI). After refactoring to `OracleInternRepository` with injected `DataSource`, Testcontainers enables real DB integration tests.

## Further reading

- Testcontainers documentation.
