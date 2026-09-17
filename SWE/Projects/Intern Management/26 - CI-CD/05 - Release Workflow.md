---
tags: [concept, ci-cd, release]
type: concept
status: complete
---

# Release Workflow

## What it is

A **release workflow** publishes a versioned artifact (JAR, Docker image, installer) when you tag a release.

## Semantic versioning

`MAJOR.MINOR.PATCH`:
- `MAJOR` — breaking changes.
- `MINOR` — new features, backward-compatible.
- `PATCH` — bug fixes.

Examples: `1.0.0`, `1.1.0`, `1.1.1`, `2.0.0`.

## GitHub release workflow

```yaml
name: Release

on:
  push:
    tags: ['v*']

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: 'temurin'
          cache: maven

      - name: Build
        run: mvn clean package -DskipTests

      - name: Build installer
        run: |
          jlink --module-path target/modules:$JAVA_HOME/jmods                 --add-modules com.example.internmanagement                 --output target/custom-runtime                 --strip-debug --no-man-pages --no-header-files
          jpackage --type deb --input target --name intern-management                    --main-jar intern-management-1.0.0.jar                    --runtime-image target/custom-runtime

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            target/intern-management-1.0.0.jar
            target/intern-management_1.0.0-1_amd64.deb
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Tagging

```bash
git tag v1.0.0
git push origin v1.0.0
```

This triggers the workflow, which builds and publishes the release.

## Conventional commits

```
feat: add intern search
fix: correct age validation
docs: update README
chore: bump dependencies
BREAKING CHANGE: rename Intern to InternRecord
```

Tools (semantic-release) can auto-generate versions and changelogs from commit messages.

## Project Connection

The project has no releases. The fix: tag-based release workflow, GitHub Releases with JAR + installer artifacts.

## Further reading

- semver.org.
- conventionalcommits.org.
