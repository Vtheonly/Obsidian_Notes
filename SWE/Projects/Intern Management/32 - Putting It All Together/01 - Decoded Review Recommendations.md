---
tags: [concept, rebuild, recommendations]
type: concept
status: complete
---

# Decoded Review Recommendations

> Every recommendation from the reviews, with a link to the note that explains it.

## Critical (14 issues)

| Recommendation | Why | Vault note |
|---|---|---|
| Remove committed JavaFX SDK (99 MB) | Binary blobs in git | [[24 - Build and Tooling/04 - Maven]] |
| Delete hardcoded `system/rootroot` | Principle of Least Privilege | [[17 - Application Security/09 - Secrets Management]] |
| Replace unsalted SHA-256 with Argon2id | Password security | [[15 - Cryptography and Password Security/01 - Argon2id]] |
| Introduce HikariCP | Connection pool | [[11 - DB Performance and Indexing/15 - HikariCP]] |
| Remove `JOptionPane` from DAO | Separation of Concerns | [[05 - Software Architecture/15 - Separation of Concerns]] |
| Replace `MAX(id)+1` with IDENTITY | Race condition | [[12 - Advanced Database Features/12 - Sequences and IDENTITY Columns]] |
| Fix `value == ""` bug | `==` vs `equals` | [[03 - Java Foundations/13 - String comparison (== vs equals)]] |
| Fix `HashMap` iteration order | Undefined behavior | [[03 - Java Foundations/01 - Collections Framework]] |
| Fix mixed Swing + JavaFX | Toolkit mixing | [[05 - Software Architecture/15 - Separation of Concerns]] |
| Fix module/package typo | JPMS | [[24 - Build and Tooling/02 - JPMS Modules]] |
| Move DB calls off FX thread | UI freeze | [[21 - JavaFX Concurrency/06 - Why UI Thread Matters]] |
| Fix static `Connection` shared across threads | Thread safety | [[10 - Transactions and Concurrency/03 - Connection Is Not Thread-Safe]] |
| Fix SQL injection in `getMaxId` | SQL injection | [[17 - Application Security/08 - SQL Injection Prevention]] |
| Fix `is_accepted` CHECK violation | Schema/code mismatch | [[04 - OOD and SOLID/18 - Replace Magic Strings with Enums]] |

## High (23 issues) — selected

| Recommendation | Why | Vault note |
|---|---|---|
| Introduce Repository pattern | Decoupling | [[05 - Software Architecture/14 - Repository Pattern]] |
| Introduce service layer | Separation | [[05 - Software Architecture/16 - Service Layer Pattern]] |
| Introduce domain model | Type safety | [[04 - OOD and SOLID/01 - Anemic Domain Model]] |
| Dependency injection | DIP | [[05 - Software Architecture/04 - Dependency Injection]] |
| Replace TitledPane-in-VBox with TableView | Virtualization | [[22 - JavaFX Advanced Controls/08 - TableView]] |
| Add empty/loading/error states | UX | [[23 - JavaFX UX and Polish/04 - Empty Loading Error States]] |
| Add transactions (auto-commit off) | ACID | [[10 - Transactions and Concurrency/01 - ACID Properties]] |
| Add FK indexes | Performance + locking | [[11 - DB Performance and Indexing/16 - Indexing Foreign Keys]] |
| Fix N+1 in search | Performance | [[11 - DB Performance and Indexing/18 - N+1 Query Problem]] |
| Use Flyway for migrations | Schema versioning | [[14 - Schema Evolution/05 - Flyway]] |
| Add audit columns | Compliance | [[14 - Schema Evolution/01 - Audit Columns]] |
| Add soft delete | Recovery | [[14 - Schema Evolution/09 - Soft Delete Pattern]] |
| Add input validation | Security | [[17 - Application Security/05 - Input Validation]] |
| Add rate limiting on login | Brute force | [[16 - Authentication and Authorization/03 - Brute Force Protection]] |
| Use Bean Validation | Declarative validation | [[17 - Application Security/01 - Bean Validation (JSR-380)]] |
| Add session management | Auth | [[16 - Authentication and Authorization/10 - Session Management]] |
| Add SLF4J + Logback logging | Observability | [[28 - Observability/07 - SLF4J and Logback]] |
| Add Micrometer metrics | Observability | [[28 - Observability/05 - Micrometer]] |
| Add audit log | Compliance | [[28 - Observability/01 - Audit Logging]] |
| Add Resilience4j (retry/circuit breaker) | Resilience | [[29 - Resilience and Fault Tolerance/05 - Resilience4j]] |
| Add Caffeine cache | Performance | [[11 - DB Performance and Indexing/06 - Caffeine Cache]] (cross-ref [[11 - DB Performance and Indexing/06 - Caffeine Cache]]) |
| Add tests | Quality | [[27 - Testing/00 - MOC - Testing]] |
| Add CI/CD | DevOps | [[26 - CI-CD/00 - MOC - CI-CD]] |

## Medium (31 issues) — selected

| Recommendation | Vault note |
|---|---|
| Replace inline CSS with stylesheet | [[20 - JavaFX Layout and CSS/03 - CSS in JavaFX]] |
| Add design tokens | [[20 - JavaFX Layout and CSS/04 - Design Tokens (CSS Variables)]] |
| Add inline form validation | [[23 - JavaFX UX and Polish/06 - Inline Form Validation]] |
| Add accessibility (a11y) | [[23 - JavaFX UX and Polish/01 - Accessibility (a11y)]] |
| Add i18n | [[23 - JavaFX UX and Polish/07 - Internationalization (i18n)]] |
| Replace Glow effect | [[20 - JavaFX Layout and CSS/01 - AnchorPane (and why to avoid it)]] |
| Use single-Stage navigation | [[20 - JavaFX Layout and CSS/07 - Single-Stage Navigation]] |
| Add FileChooser for PDF | [[23 - JavaFX UX and Polish/05 - FileChooser]] |
| Replace HTMLWorker with OpenHTMLtoPDF | [[31 - Enterprise Java/07 - OpenHTMLtoPDF]] |
| Add Dockerfile | [[25 - Docker and Deployment/03 - Dockerfile]] |
| Add static analysis (SpotBugs, PMD, Checkstyle) | [[24 - Build and Tooling/07 - Static Analysis (SpotBugs, PMD, Checkstyle, Sonar)]] |
| Add OWASP Dependency-Check | [[24 - Build and Tooling/05 - OWASP Dependency-Check]] |
| Add JaCoCo coverage | [[24 - Build and Tooling/03 - JaCoCo Coverage]] |
| Bump Java 20 → 21 LTS | [[03 - Java Foundations/04 - Java 21 LTS Features]] |
| Bump ojdbc8 → ojdbc11 23.x | [[17 - Application Security/04 - Dependency Vulnerabilities (CVEs)]] |
| Replace `javax.mail` with `jakarta.mail` | [[31 - Enterprise Java/03 - Jakarta Mail]] |
| Fix quoted identifiers | [[08 - Relational DB Foundations/11 - Quoted Identifiers in Oracle]] |
| Add `SELECT *` → explicit columns | [[08 - Relational DB Foundations/14 - SQL Basics]] |
| Add batch operations | [[11 - DB Performance and Indexing/03 - Batch Operations]] |
| Add pagination | [[11 - DB Performance and Indexing/19 - Pagination]] |
| Add least-privilege DB user | [[16 - Authentication and Authorization/08 - Principle of Least Privilege]] |
| Add encryption at rest (TDE) | [[15 - Cryptography and Password Security/09 - Symmetric Encryption (AES)]] |
| Add encryption in transit (TLS) | [[15 - Cryptography and Password Security/10 - TLS and HTTPS]] |
| Add health check endpoint | [[28 - Observability/03 - Health Check Endpoints]] |
| Add password reset flow | [[16 - Authentication and Authorization/07 - Password Reset Flows]] |
| Add Docker healthcheck | [[25 - Docker and Deployment/04 - Healthchecks]] |
| Add Docker secrets | [[25 - Docker and Deployment/02 - Docker Secrets]] |
| Add GitHub Actions CI | [[26 - CI-CD/03 - GitHub Actions]] |
| Add Testcontainers | [[27 - Testing/08 - Testcontainers]] |
| Add TestFX | [[27 - Testing/07 - TestFX]] |
| Add structured logging (JSON) | [[28 - Observability/07 - SLF4J and Logback]] |

## Low (17 issues)

- Fix misspellings (`Mnagement`, `requstes`, `Serach`, etc.).
- Fix lowercase class names.
- Remove dead code (`DataPreprocessor`, `isHashEqual`).
- Remove dead schema tables.
- Remove TODO comments.
- Add `.gitignore` for `*.swp`, `document_now.pdf`, `.idea/`.
- Add LICENSE (MIT).
- Add `.editorconfig`.
- Rewrite README.
- Use `mvn` wrapper.
- Consistent brace style.
- Add Javadoc to public APIs.

## Coverage check

Every recommendation from the four review documents is explained in at least one vault note. If you finish the vault and still don't understand a recommendation, it's a gap — let me know.
