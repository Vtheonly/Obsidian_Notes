---
tags: [concept, testing, pyramid]
type: concept
status: complete
---

# Test Pyramid

## The pyramid

```
        /\
       /E2E\         few, slow, whole-system
      /------\
     /Integ.   \      some, medium, real dependencies
    /-----------\
   /   Unit      \    many, fast, isolated
  /----------------\
```

- **Unit tests (70%)** — fast (< 100 ms each), isolated (mocked dependencies), test one class/method.
- **Integration tests (20%)** — medium speed, real dependencies (DB via Testcontainers), test multiple components.
- **E2E tests (10%)** — slow, full system (browser, DB, API), test user flows.

## Why the pyramid shape

- **Fast feedback** — unit tests run in seconds; E2E in minutes.
- **Cost** — E2E tests are expensive to write and maintain.
- **Brittleness** — E2E tests break on any change; unit tests break only on relevant changes.

## Inverted pyramid (anti-pattern)

Most E2E, few unit tests. Slow, brittle, hard to localize failures.

## Project Connection

The project has **zero tests**. The fix:
1. Unit tests for `PasswordHasher`, `Validator`, `DecisionStatus`, service logic (with mocked repositories).
2. Integration tests for repositories (with Testcontainers Oracle).
3. UI tests for critical flows (login, search, accept) with TestFX.

Target: 70/20/10.

## Further reading

- *Succeeding with Agile* (Cohn), test pyramid.
- Google Testing Blog — "Test Sizes".
