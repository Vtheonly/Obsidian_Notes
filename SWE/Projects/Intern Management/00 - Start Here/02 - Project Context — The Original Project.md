---
tags: [moc, start-here, project-context]
type: case-study
status: complete
---

# Project Context — The Original Project

> This note establishes the shared context for the entire vault. Read it first — every other note assumes you know what is described here.

## The Repository

- **URL:** `https://github.com/Vtheonly/JavaFX_Intern_Mnagement`
- **Stack:** JavaFX 21 + Oracle XE (19c/21c) + Maven
- **Functional scope:** authentication with role-based routing, CRUD over four entities (intern, worker_user, theme, department), chief-of-department accept/reject workflow, PDF report generation, email sending (claimed, not implemented).
- ** LOC:** ~2,400 lines of application code, 6 FXML views, 3 SQL scripts, 1 docker-compose for Oracle.

## The Verdict

Multiple independent professional code reviews conclude the same thing: **the project is structurally unsalvageable in its current form.** It must be refactored — not patched — before it can be shown on a résumé as an example of professional work.

The verdict is harsh but quantified. The codebase violates every SOLID principle, ships hardcoded credentials for the Oracle **`system`** (SYSDBA-privileged) account in source control, uses unsalted SHA-256 for passwords (crackable in seconds on a consumer GPU), performs every database call on the JavaFX Application Thread (UI freezes on every query), ships the 99 MB JavaFX SDK as binary blobs in git, mixes Swing `JOptionPane` dialogs into a JavaFX app, has zero tests, and builds SQL by string concatenation.

## The Issue Breakdown

| Severity | Count | Meaning |
|---|---|---|
| Critical | 14 | Actively dangerous: data loss, security breach, or app-wide breakage |
| High | 23 | Will block any production deployment; fundamental design flaws |
| Medium | 31 | Significant quality/maintainability problems; accumulate technical debt |
| Low | 17 | Code smell, style, or minor inconsistency |
| **Total** | **85** | Across architecture, security, DB, UI/UX, build, testing, observability |

## The Five "Must-Fix-Before-Anything-Else" Items

These are the items that make the project look like a beginner wrote it. The vault teaches the prerequisites for each.

1. **Remove the committed JavaFX SDK (99 MB) from git history** — binary blobs, Windows-only DLLs in a cross-platform project, redundant with the Maven JavaFX dependency. → Learn: [[24 - Build and Tooling/00 - MOC - Build and Tooling]]
2. **Delete the hardcoded `system/rootroot` database credentials** — using Oracle's `system` account (which can `DROP DATABASE`) as the application user is a critical security violation. → Learn: [[17 - Application Security/09 - Secrets Management]], [[16 - Authentication and Authorization/08 - Principle of Least Privilege]]
3. **Replace unsalted SHA-256 with bcrypt/argon2id** — the `salt` column exists in the schema but is never used. Plain SHA-256 is rainbow-table-crackable in milliseconds per hash. → Learn: [[15 - Cryptography and Password Security/00 - MOC - Cryptography]]
4. **Introduce a connection pool (HikariCP/Oracle UCP)** — the current single static `Connection` shared across the entire app is not thread-safe, leaks on close, and prevents any meaningful concurrency. → Learn: [[11 - DB Performance and Indexing/15 - HikariCP]], [[11 - DB Performance and Indexing/09 - Connection Pooling]]
5. **Stop mixing Swing `JOptionPane` into JavaFX** — every database error pops a Swing dialog from inside the data-access layer, which means the DAO cannot be unit-tested, cannot run headless, and visually breaks on macOS/Linux. → Learn: [[05 - Software Architecture/15 - Separation of Concerns]], [[05 - Software Architecture/17 - Smart UI Anti-Pattern]]

## The Anti-Patterns Identified

This vault exists to teach you why each of these is bad, what principle it violates, and how to fix it. Notes that decode each anti-pattern are linked.

| Anti-Pattern | Where it appears | Vault chapter |
|---|---|---|
| Smart UI / God Class | `oracleConnector.java` (940 LOC, 6+ responsibilities) | [[05 - Software Architecture/17 - Smart UI Anti-Pattern]] |
| Static global state for view transitions | `static String labelText` in two controllers | [[04 - OOD and SOLID/21 - Static Utility Anti-Pattern]] |
| Anemic domain model (no domain objects, just `Map<String,Object>`) | everywhere | [[04 - OOD and SOLID/01 - Anemic Domain Model]] |
| Hardcoded credentials | `oracleConnector.java` lines 14–16 | [[17 - Application Security/09 - Secrets Management]] |
| Unsalted SHA-256 password hashing | `toolkit.hashIt()` | [[15 - Cryptography and Password Security/12 - Why Hashing ≠ Encryption]] |
| SQL string concatenation | `oracleConnector.searchIntern()` | [[17 - Application Security/08 - SQL Injection Prevention]] |
| `MAX(id)+1` for new IDs (race condition) | every insert | [[12 - Advanced Database Features/12 - Sequences and IDENTITY Columns]] |
| N+1 query problem | `searchIntern` calls `getNameById` per row | [[11 - DB Performance and Indexing/18 - N+1 Query Problem]] |
| Blocking the JavaFX Application Thread | every controller event handler | [[21 - JavaFX Concurrency/06 - Why UI Thread Matters]] |
| Absolute positioning (AnchorPane + layoutX/Y) | every FXML file | [[20 - JavaFX Layout and CSS/01 - AnchorPane (and why to avoid it)]] |
| Un-virtualized lists (TitledPane in VBox) | `chiefDecisionController.addToPool()` | [[22 - JavaFX Advanced Controls/10 - Virtualization (how it works)]] |
| String serialization of records (`Map.toString()` → Label → parse back) | `toolkit.parseText` | [[04 - OOD and SOLID/01 - Anemic Domain Model]] |
| Mixed Swing + JavaFX | `JOptionPane.showMessageDialog` in DAO | [[05 - Software Architecture/15 - Separation of Concerns]] |
| No transactions (auto-commit everywhere) | all `oracleConnector` write methods | [[10 - Transactions and Concurrency/01 - ACID Properties]] |
| Hard delete (no soft delete, no audit) | all four `delete*` methods | [[14 - Schema Evolution/09 - Soft Delete Pattern]] |

## The Modern Technologies Recommended

Every recommendation in the reviews maps to a chapter in this vault.

| Recommendation | What it is | Vault chapter |
|---|---|---|
| HikariCP | JDBC connection pool | [[11 - DB Performance and Indexing/15 - HikariCP]] |
| Argon2id | Password hashing function (PHC winner) | [[15 - Cryptography and Password Security/01 - Argon2id]] |
| Flyway / Liquibase | Database migration tools | [[14 - Schema Evolution/05 - Flyway]] |
| Java SPI (`ServiceLoader`) | Plugin architecture | [[31 - Enterprise Java/04 - Java SPI (ServiceLoader)]] |
| Virtualized TableViews | JavaFX TableView cell recycling | [[22 - JavaFX Advanced Controls/08 - TableView]] |
| Prepared Statements | JDBC parameterized queries | [[13 - JDBC and Data Access/09 - PreparedStatement]] |
| Repository Pattern | Data access abstraction | [[05 - Software Architecture/14 - Repository Pattern]] |
| Dependency Injection | Inversion of control for dependencies | [[05 - Software Architecture/04 - Dependency Injection]] |
| MVC/MVP/MVVM | UI architectural patterns | [[05 - Software Architecture/10 - Layered Architecture]] |
| Connection Pooling | Reuse JDBC connections | [[11 - DB Performance and Indexing/09 - Connection Pooling]] |
| Database Indexing | B-tree, bitmap, function-based | [[11 - DB Performance and Indexing/01 - B-Tree Index]] |
| Database Normalization | 1NF–BCNF | [[09 - Normalization/00 - MOC - Normalization]] |
| Transaction Isolation | ACID isolation levels | [[10 - Transactions and Concurrency/05 - Isolation Levels]] |
| Caffeine Cache | In-process Java cache | [[11 - DB Performance and Indexing/06 - Caffeine Cache]] |
| JavaFX Application Thread | UI rendering thread | [[19 - JavaFX Fundamentals/03 - JavaFX Application Thread]] |
| `ExecutorService` | Java thread pool | [[18 - Java Concurrency/03 - ExecutorService]] |
| Secure Authentication | Sessions, RBAC, rate limiting | [[16 - Authentication and Authorization/00 - MOC - Auth]] |

## What This Vault Does NOT Do

- **It does not document the existing code line-by-line.** The existing code is a case study in what not to do. We explain it briefly when needed, then teach the correct approach.
- **It does not preserve the original code's organization.** The original code has no real organization; we reorganize concepts by logical learning sequence.
- **It does not only teach enough to understand the project.** It teaches enough to understand every review recommendation, every alternative, and how to rebuild the project from scratch using modern best practices.

## How to Proceed

Go to → [[Learning Path — The Roadmap]]

If you want a specific topic, browse the [[00 - Start Here/00 - README|chapter index]] or open a chapter MOC directly.
