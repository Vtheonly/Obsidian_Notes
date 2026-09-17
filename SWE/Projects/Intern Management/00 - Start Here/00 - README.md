---
tags: [moc, root, start-here]
type: moc
status: complete
---

# JavaFX Intern Management — Learning Vault

> A complete, first-principles learning roadmap built around a real JavaFX + Oracle
> project and the **85 issues** that professional code reviews identified in it.
> The goal: by the end, you can rebuild the project from scratch using modern best
> practices and defend every architectural decision in a senior engineering interview.

## What This Vault Is

The project at `github.com/Vtheonly/JavaFX_Intern_Mnagement` was "vibe coded" until
it compiled. Multiple professional reviews then dissected it across architecture,
security, database, UI/UX, build, testing, and observability — finding 14 critical,
23 high, 31 medium, and 17 low issues. This vault teaches the engineering principles
behind every recommendation, criticism, and refactoring suggestion.

The vault is **not** a line-by-line documentation of the existing code. The existing
code is a case study in what *not* to do. Instead, the vault teaches the *concepts*
the reviewers assume you already know — from Big-O and the Java Memory Model to
Argon2id, HikariCP, virtualized TableViews, Flyway migrations, Oracle VPD, and the
12-Factor App.

## How to Use This Vault

1. **Start with** [[00 - Start Here/02 - Project Context — The Original Project]].
2. **Then read** [[00 - Start Here/01 - Learning Path — The Roadmap]].
3. **Follow the MOCs.** Every chapter folder has a `MOC - <topic>.md` index.
4. **Follow the wikilinks.** Notes cross-link aggressively.
5. **Don't skip the foundations.** The project has real bugs from misunderstanding
   `==` on Strings, `HashMap` iteration order, `static`, and Big-O.

## Vault Structure (32 chapters)

| # | Chapter | What it teaches |
|---|---|---|
| 00 | [[00 - Start Here/02 - Project Context — The Original Project|Start: Project Context]] | The 85 issues and the five "must-fix" items |
| 00 | [[00 - Start Here/01 - Learning Path — The Roadmap|Start: Learning Path]] | The sequenced roadmap |
| 01 | [[01 - Code Walkthrough/00 - MOC - Code Walkthrough|Code Walkthrough]] | What the actual source code does, file by file |
| 02 | [[02 - CS Foundations/00 - MOC - CS Foundations|CS Foundations]] | Big-O, data structures, OS threads, memory |
| 03 | [[03 - Java Foundations/00 - MOC - Java|Java Foundations]] | JVM, types, exceptions, `static`, records, JPMS |
| 04 | [[04 - OOD and SOLID/00 - MOC - OOD|OOD & SOLID]] | Encapsulation, SOLID, DRY/KISS/YAGNI |
| 05 | [[05 - Software Architecture/00 - MOC - Architecture|Software Architecture]] | Layered, Clean, Hexagonal, Repository, DI |
| 06 | [[06 - Design Patterns/00 - MOC - Design Patterns|Design Patterns]] | GoF + Repository + DI + Plug-in |
| 07 | [[07 - Refactoring Techniques/00 - MOC - Refactoring|Refactoring]] | Extract Class, Replace Conditional, etc. |
| 08 | [[08 - Relational DB Foundations/00 - MOC - Databases|Relational DB]] | Relational model, SQL, keys, joins |
| 09 | [[09 - Normalization/00 - MOC - Normalization|Normalization]] | 1NF–BCNF, denormalization |
| 10 | [[10 - Transactions and Concurrency/00 - MOC - Transactions|Transactions]] | ACID, isolation levels, MVCC, locking |
| 11 | [[11 - DB Performance and Indexing/00 - MOC - DB Performance|DB Performance]] | B-tree, bitmap, N+1, HikariCP, Caffeine |
| 12 | [[12 - Advanced Database Features/00 - MOC - Advanced DB|Advanced DB]] | Partitioning, MVs, VPD, redaction, IOT |
| 13 | [[13 - JDBC and Data Access/00 - MOC - JDBC|JDBC & Data Access]] | DataSource, PreparedStatement, RowMapper |
| 14 | [[14 - Schema Evolution/00 - MOC - Schema Evolution|Schema Evolution]] | Soft delete, audit columns, Flyway, Liquibase |
| 15 | [[15 - Cryptography and Password Security/00 - MOC - Cryptography|Cryptography]] | Hashing vs encryption, salt, BCrypt, Argon2id |
| 16 | [[16 - Authentication and Authorization/00 - MOC - Auth|Auth & Authz]] | Sessions, RBAC, rate limiting, Spring Security |
| 17 | [[17 - Application Security/00 - MOC - Security|App Security]] | OWASP Top 10, input validation, secrets, GDPR |
| 18 | [[18 - Java Concurrency/00 - MOC - Concurrency|Java Concurrency]] | Threads, ExecutorService, JMM, virtual threads |
| 19 | [[03 - Java Foundations/00 - MOC - Java|JavaFX Fundamentals]] | Stage, Scene, FXML, Application Thread |
| 20 | [[03 - Java Foundations/00 - MOC - Java|JavaFX Layout & CSS]] | Panes, CSS, design tokens, navigation |
| 21 | [[03 - Java Foundations/00 - MOC - Java|JavaFX Concurrency]] | Task, Service, Platform.runLater |
| 22 | [[03 - Java Foundations/00 - MOC - Java|JavaFX Controls]] | TableView, virtualization, FilteredList |
| 23 | [[03 - Java Foundations/00 - MOC - Java|JavaFX UX & Polish]] | Empty/loading/error, a11y, i18n |
| 24 | [[24 - Build and Tooling/00 - MOC - Build and Tooling|Build & Tooling]] | Maven, JPMS, jlink, jpackage, static analysis |
| 25 | [[25 - Docker and Deployment/00 - MOC - Docker|Docker & Deployment]] | Dockerfiles, Compose, secrets, healthchecks |
| 26 | [[26 - CI-CD/00 - MOC - CI-CD|CI/CD]] | GitHub Actions, Jenkins, release workflows |
| 27 | [[27 - Testing/00 - MOC - Testing|Testing]] | JUnit 5, Mockito, Testcontainers, TestFX |
| 28 | [[28 - Observability/00 - MOC - Observability|Observability]] | SLF4J, Logback, Micrometer, Prometheus, audit |
| 29 | [[29 - Resilience and Fault Tolerance/00 - MOC - Resilience|Resilience]] | Retry, circuit breaker, bulkhead, Resilience4j |
| 30 | [[30 - Caching/00 - MOC - Caching|Caching]] | Caffeine, Redis, cache-aside, stampede |
| 31 | [[31 - Enterprise Java/00 - MOC - Enterprise Java|Enterprise Java]] | SPI, Jakarta Mail, OpenHTMLtoPDF, Quartz |
| 32 | [[32 - Putting It All Together/00 - MOC - Rebuild|Putting It All Together]] | Target architecture, refactoring roadmap |
| 33 | [[33 - Appendix/02 - Glossary|Appendix]] | Glossary, bibliography, concept index |

## Conventions

- YAML frontmatter on every note: `tags`, `type`, `status`, `prerequisites`, `related`.
- `type: moc` = Map of Content (chapter index).
- `type: concept` / `case-study` / `pattern` for individual notes.
- Wikilinks `[[like this]]` heavily used.
- Each note ends with **Common Pitfalls**, **Trade-offs**, **Project Connection**.
