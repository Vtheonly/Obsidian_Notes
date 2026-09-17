---
tags: [concept, rebuild, phase-1]
type: concept
status: complete
related:
  - [[]]
---

# Phase 1 — Characterization Tests (8-12 hours)

> Goal: capture the current behavior in tests before refactoring.

## Tasks

### 1. Set up testing infrastructure
- JUnit 5 + Mockito + Testcontainers in `pom.xml`.
- `src/test/java/` directory.
- JaCoCo plugin.
- SpotBugs, PMD, Checkstyle (with `failOnViolation=false` initially — just collect data).

### 2. Integration tests for `oracleConnector`
- Testcontainers Oracle XE container.
- Seed with `insertion.sql` data.
- Test every public method of `oracleConnector`.
- Even the buggy ones — lock in current behavior.

### 3. Characterization tests for `toolkit`
- `hashIt` — given "password", produces a specific Base64 hash.
- `parseText` — given a specific input, produces a specific Map.
- `formatString` — given a Map, produces a specific string.
- `generatePassword` — verify length and charset.
- Lock in current behavior, including bugs.

### 4. TestFX UI tests
- TestFX + monocle (headless).
- Test login flow, search, insert.
- These will break during Phase 2 refactor — that's OK, update them.

### 5. JaCoCo
- Initial coverage ~20-30%.
- Target 60% by Phase 3, 80% after.

## After Phase 1

You have a safety net. When you refactor in Phase 2, tests tell you if you broke behavior. Bugs are documented (the tests assert the buggy behavior; you can fix them later and update the tests).

## Why this comes before refactor

Without tests, you can't safely refactor. You'd be flying blind. With characterization tests, you can refactor with confidence — if a test breaks, you changed behavior.

## Further reading

- [[07 - Refactoring Techniques/02 - Characterization Tests]] (cross-ref [[07 - Refactoring Techniques/02 - Characterization Tests]]).
