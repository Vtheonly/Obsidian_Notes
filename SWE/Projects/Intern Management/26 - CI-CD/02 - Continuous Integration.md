---
tags: [concept, ci-cd, ci]
type: concept
status: complete
---

# Continuous Integration (CI)

## What it is

**CI** is the practice of integrating code into a shared branch frequently (multiple times per day), with automated builds and tests.

## The CI loop

1. Developer pushes to a branch.
2. CI server detects the push.
3. CI builds the code.
4. CI runs tests.
5. CI runs quality checks (static analysis, coverage).
6. CI reports success/failure.
7. If green, the branch can be merged.

## Why

- **Catch bugs early** — a bug introduced today is found today, not next month.
- **Always-green main** — main is always deployable.
- **Confidence** — automated tests catch regressions.
- **Fast feedback** — developers know in minutes if their change broke something.

## Without CI

- "It works on my machine."
- Integration hell — merging a long-lived branch breaks everything.
- Manual testing — slow, error-prone.
- Fear of refactoring — no safety net.

## The project's CI status

The project has **no CI**. No `.github/workflows/`, no Jenkinsfile, no `.gitlab-ci.yml`. The README doesn't mention how to build. Anyone cloning the repo has to figure out `mvn javafx:run` themselves.

## The fix

A GitHub Actions workflow that:
1. Checks out the code.
2. Sets up Java 21.
3. Runs `mvn verify` (compile + test + static analysis).
4. Builds a Docker image.
5. Publishes a jpackage installer on tag.

See [[26 - CI-CD/03 - GitHub Actions]].

## Further reading

- *Continuous Delivery* (Humble & Farley).
