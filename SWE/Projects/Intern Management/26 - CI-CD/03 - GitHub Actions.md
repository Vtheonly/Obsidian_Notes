---
tags: [concept, ci-cd, github-actions]
type: concept
status: complete
related:
  - [[26 - CI-CD/02 - Continuous Integration]]
---

# GitHub Actions

## What it is

**GitHub Actions** is GitHub's CI/CD service. Workflows are defined in `.github/workflows/*.yml`.

## Basic workflow

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: 'temurin'
          cache: maven
      - name: Build
        run: mvn clean verify
      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: target/site/jacoco/
```

## Services (for integration tests)

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      oracle:
        image: gvenzl/oracle-xe:21-slim
        ports: ['1521:1521']
        env:
          ORACLE_PASSWORD: test
        options: >-
          --health-cmd "healthcheck.sh"
          --health-interval 15s
          --health-timeout 10s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: 'temurin'
      - name: Wait for Oracle
        run: |
          while ! nc -z localhost 1521; do sleep 1; done
          sleep 30  # Oracle needs time to initialize
      - name: Run tests
        run: mvn test
        env:
          DB_URL: jdbc:oracle:thin:@localhost:1521/XE
          DB_USER: system
          DB_PASSWORD: test
```

## Matrix builds

```yaml
strategy:
  matrix:
    java: [21, 22]
    os: [ubuntu-latest, windows-latest, macos-latest]
steps:
  - uses: actions/setup-java@v4
    with:
      java-version: ${{ matrix.java }}
```

Runs the build on multiple Java versions and OSes.

## Caching

```yaml
- uses: actions/setup-java@v4
  with:
    java-version: '21'
    cache: maven
```

Caches `~/.m2/repository` — faster builds.

## Secrets

```yaml
- name: Deploy
  run: mvn deploy
  env:
    MAVEN_USERNAME: ${{ secrets.MAVEN_USERNAME }}
    MAVEN_PASSWORD: ${{ secrets.MAVEN_PASSWORD }}
```

Secrets are set in the repo settings.

## Project Connection

The fix adds `.github/workflows/ci.yml` with:
1. Build on push/PR.
2. Java 21.
3. Maven verify (compile + test + SpotBugs + Checkstyle + JaCoCo + OWASP Dependency-Check).
4. Testcontainers for integration tests.
5. Docker image build.
6. jpackage installer on tag.

## Further reading

- GitHub Actions documentation.
