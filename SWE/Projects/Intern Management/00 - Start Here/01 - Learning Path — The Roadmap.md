---
tags: [moc, start-here, learning-path]
type: moc
status: complete
---

# Learning Path — The Roadmap

> The vault is a learning roadmap, not a reference book. Read top to bottom the first time. The order is intentional: every chapter assumes you have read its prerequisites.

## The Big Picture

```
[ Foundations ]
  CS  →  Java  →  OOD/SOLID  →  Architecture  →  Design Patterns
                                                      │
                                                      ▼
[ Databases ]                            [ Concurrency ]
  Relational Model  →  Transactions  →     Java Threads  →  JavaFX
  Indexing  →  Advanced  →  JDBC            Concurrency       UI
                                                      │
                                                      ▼
[ Security ]                  [ Build & Test ]      [ JavaFX ]
  Crypto  →  Auth  →  App     Maven → Testing     Layout/Controls
  Security                   Docker/Observability   UX/Polish
                                                      │
                                                      ▼
                                          [ Putting It All Together ]
                                            Target Architecture
                                            Refactoring Roadmap
```

## Phase 1 — Foundations (Weeks 1–3)

| Chapter | Why first | Time |
|---|---|---|
| [[02 - CS Foundations/00 - MOC - CS Foundations|01 CS Foundations]] | Without Big-O, you cannot reason about why `MAX(id)+1` is bad. Without OS thread concepts, the JavaFX Application Thread discussion is opaque. | 4–6 hrs |
| [[03 - Java Foundations/00 - MOC - Java|02 Java Foundations]] | The review identifies real bugs from misunderstanding `static`, `==` on Strings, `HashMap` iteration order, and `try-with-resources`. You must understand these before reading any architecture note. | 6–8 hrs |
| [[04 - OOD and SOLID/00 - MOC - OOD|03 OOD & SOLID]] | Every architectural critique in the review is grounded in SOLID. Without SRP, OCP, DIP, "God Class" is just an insult, not a diagnosis. | 4–6 hrs |

## Phase 2 — Architecture and Patterns (Weeks 3–4)

| Chapter | Why now | Time |
|---|---|---|
| [[05 - Software Architecture/00 - MOC - Architecture|04 Software Architecture]] | The #1 critical issue in the project is "no architecture." Layered architecture, Repository pattern, DI, and the Smart UI anti-pattern all live here. | 5–7 hrs |
| [[06 - Design Patterns/00 - MOC - Design Patterns|05 Design Patterns]] | The review identifies 13 patterns that should be applied. Learn what they are, when to use them, and when they are overkill. | 6–8 hrs |

## Phase 3 — Databases (Weeks 5–7)

| Chapter | Why this order | Time |
|---|---|---|
| [[08 - Relational DB Foundations/00 - MOC - Databases|06 Relational DB Foundations]] | You cannot understand why `VARCHAR2(255)` PKs are bad without normalization. You cannot understand why double-quoted identifiers are bad without Oracle's case-folding rules. | 6–8 hrs |
| [[10 - Transactions and Concurrency/00 - MOC - Transactions|07 Transactions & Concurrency]] | The project has no transactions. ACID, isolation levels, MVCC, deadlocks — all prerequisites for any later discussion of repository implementation. | 4–5 hrs |
| [[11 - DB Performance and Indexing/00 - MOC - DB Performance|08 DB Performance & Indexing]] | N+1 queries, missing FK indexes, no connection pool, no cache. HikariCP and Caffeine both live here. | 5–7 hrs |
| [[12 - Advanced Database Features/00 - MOC - Advanced DB|09 Advanced DB Features]] | The advanced schema redesign uses partitioning, materialized views, VPD, redaction, IOT, sequences. These are the "masterclass-grade" recommendations. | 6–8 hrs |
| [[13 - JDBC and Data Access/00 - MOC - JDBC|10 JDBC & Data Access]] | PreparedStatement, DataSource, RowMapper — the actual Java-side of database access. | 3–4 hrs |
| [[14 - Schema Evolution/00 - MOC - Schema Evolution|11 Schema Design & Evolution]] | Soft delete, audit columns, Flyway, Liquibase. How schemas evolve safely over time. | 3–4 hrs |

## Phase 4 — Security (Week 8)

| Chapter | Why now | Time |
|---|---|---|
| [[15 - Cryptography and Password Security/00 - MOC - Cryptography|12 Cryptography]] | Without understanding hash functions, salt, key stretching, and timing attacks, you cannot understand why unsalted SHA-256 is bad or why Argon2id is recommended. | 4–5 hrs |
| [[16 - Authentication and Authorization/00 - MOC - Auth|13 Auth & Authz]] | RBAC, sessions, brute-force protection, rate limiting. The project's auth is a textbook of what not to do. | 3–4 hrs |
| [[17 - Application Security/00 - MOC - Security|14 Application Security]] | OWASP Top 10, input validation, secrets management, GDPR. The capstone of the security chapters. | 3–4 hrs |

## Phase 5 — Concurrency and JavaFX (Weeks 9–11)

| Chapter | Why now | Time |
|---|---|---|
| [[18 - Java Concurrency/00 - MOC - Concurrency|15 Java Concurrency]] | You need threads, ExecutorService, and the Java Memory Model before tackling JavaFX concurrency. | 4–5 hrs |
| [[03 - Java Foundations/00 - MOC - Java|16 JavaFX Fundamentals]] | Stage, Scene, FXML, controllers, the Application Thread. The skeleton. | 3–4 hrs |
| [[03 - Java Foundations/00 - MOC - Java|17 JavaFX Layout & UI]] | Panes, CSS, design tokens, single-Stage navigation. | 3–4 hrs |
| [[03 - Java Foundations/00 - MOC - Java|18 JavaFX Concurrency]] | Task, Service, Platform.runLater, UI state machine. The core of "don't block the UI thread." | 3–4 hrs |
| [[03 - Java Foundations/00 - MOC - Java|19 JavaFX Controls]] | TableView, virtualization, cell factories, FilteredList. Replaces the TitledPane-in-VBox anti-pattern. | 4–5 hrs |
| [[03 - Java Foundations/00 - MOC - Java|20 JavaFX UX & Polish]] | Empty/loading/error states, accessibility, i18n. The polish layer. | 3–4 hrs |

## Phase 6 — Engineering Practices (Weeks 12–13)

| Chapter | Why now | Time |
|---|---|---|
| [[24 - Build and Tooling/00 - MOC - Build and Tooling|21 Build, Tooling, DevOps]] | Maven, Docker, CI, static analysis, jpackage. | 4–5 hrs |
| [[27 - Testing/00 - MOC - Testing|22 Testing]] | JUnit 5, Mockito, Testcontainers, TestFX. The project has zero tests. | 4–5 hrs |
| [[28 - Observability/00 - MOC - Observability|23 Observability]] | SLF4J, Logback, Micrometer, audit logs. Replaces `System.out.println`. | 3–4 hrs |
| [[29 - Resilience and Fault Tolerance/00 - MOC - Resilience|24 Resilience]] | Retry, circuit breaker, bulkhead, Resilience4j. Self-healing systems. | 3–4 hrs |

## Phase 7 — Enterprise & Capstone (Week 14)

| Chapter | Why last | Time |
|---|---|---|
| [[31 - Enterprise Java/00 - MOC - Enterprise Java|25 Enterprise Java]] | SPI, Jakarta Mail, OpenHTMLtoPDF, Quartz, multi-tenancy. Stretch goals. | 3–4 hrs |
| [[32 - Putting It All Together/00 - MOC - Rebuild|26 Putting It All Together]] | The target architecture, package structure, refactoring roadmap, and decoded review recommendations. | 5–6 hrs |

## How Long Will This Take?

- **Fast track** (you already know Java + SQL): 60–80 hours.
- **Realistic track** (you "vibe coded" the original): 120–160 hours.
- **Mastery track** (you want to rebuild the project from scratch afterwards): 200+ hours.

The goal is not speed. The goal is that, by the end, you can read every review comment and not only understand it but defend it in an interview.

## Reading Rules

1. **Never skip prerequisites.** If a note's `prerequisites:` list contains a note you haven't read, read that first.
2. **Read the MOC before the notes.** The MOC sets up the chapter's mental model.
3. **Follow wikilinks aggressively.** The first time you see a concept, click through. The second time, you should recognize it.
4. **Do the code examples.** Reading code is not the same as typing code. When a note shows a snippet, type it out, compile it, break it, fix it.
5. **Connect back to the project.** Every note has a "Project Connection" section at the end. Use it to anchor the abstract concept to the concrete bug in your code.

Continue → [[02 - CS Foundations/00 - MOC - CS Foundations]]
