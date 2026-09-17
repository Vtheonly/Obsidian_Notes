---
tags: [concept, rebuild, phase-0]
type: concept
status: complete
related:
  - [[]]
---

# Phase 0 — Hygiene (4-6 hours)

> Goal: make the repo clonable, buildable, and presentable. No code changes, just cleanup.

## Tasks

### 1. Purge JavaFX SDK from git history
```bash
git filter-repo --invert-paths --path javafx-sdk-22/ --force
```
Add `javafx-sdk-22/` to `.gitignore`.

### 2. Delete `_.swp` and `document_now.pdf`
Add to `.gitignore`:
```
*.swp
*.swo
document_now.pdf
*.pdf
.idea/
*.iml
```

### 3. Fix package/module typo
- Rename `com.example.intern_manegement_app` → `com.example.internmanagement`.
- Rename module in `module-info.java`.
- Update all FXML `fx:controller` attributes.
- Update all imports.
- Update `pom.xml` (`artifactId`, `mainClass`).
- Rename the GitHub repo.

### 4. Rename class files to PascalCase
- `main` → `InternManagementApp`
- `oracleConnector` → (will be split in Phase 2; for now, `OracleConnector`)
- `toolkit` → (will be split in Phase 2; for now, `Toolkit`)
- Controllers → `LoginController`, `InsertionInternController`, etc.
- Delete `DataPreprocessor.java`.

### 5. Rewrite README
- One-paragraph elevator pitch.
- Architecture diagram (Mermaid).
- Prerequisites (JDK 21+, Docker, Maven).
- `docker compose up` + `mvn javafx:run` quickstart.
- Screenshots.
- "What's intentionally simplified" section.
- License.

### 6. Add LICENSE (MIT)
Use `github.com/license` to generate.

### 7. Add `.editorconfig`, Checkstyle config
```ini
# .editorconfig
root = true
[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 4
```

### 8. Bump pom.xml
- Java 21 LTS (`<maven.compiler.release>21</maven.compiler.release>`).
- JavaFX 21.0.4.
- `ojdbc11` 23.5.0.24.7.
- `jakarta.mail-api` 2.1.3 + `org.eclipse.angus:jakarta.mail` 2.0.3.
- `pdfbox` 3.0.x.
- `openpdf` 2.0.x.
- Add `versions-maven-plugin` for `mvn versions:display-dependency-updates`.

## After Phase 0

The repo is clonable, builds cleanly, has no embarrassing typos, and the README explains how to run it. Still has all the architectural and security issues — those come in later phases.

## Further reading

- See [[24 - Build and Tooling/00 - MOC - Build and Tooling]].
