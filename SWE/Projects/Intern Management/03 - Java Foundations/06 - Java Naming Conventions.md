---
tags: [concept, java, conventions, clean-code]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/02 - Clean Code Principles]]
---

# Java Naming Conventions

## The rules (JLS §6.2, Java Community conventions)

| Element | Convention | Example |
|---|---|---|
| Class / Interface | PascalCase, noun | `Intern`, `InternRepository`, `Runnable` |
| Method | camelCase, verb | `findById`, `save`, `isPending` |
| Variable | camelCase, noun | `internName`, `resultSet` |
| Constant | UPPER_SNAKE_CASE | `MAX_POOL_SIZE`, `DEFAULT_TIMEOUT` |
| Package | lowercase, dot-separated | `com.example.internmanagement` |
| Module | lowercase, dot-separated | `com.example.internmanagement` |
| Generic type parameter | single uppercase | `T`, `E`, `K`, `V` |
| Enum constant | UPPER_SNAKE_CASE | `PENDING`, `ACCEPTED` |
| Annotation | PascalCase | `@Override`, `@FXML` |

## Why it matters

- **Readability** — PascalCase for classes, camelCase for methods is universal in the Java ecosystem. Violating it makes code look "wrong" to any Java developer.
- **Tooling** — IDEs, static analyzers, Spring's component scanner treat lowercase class names as suspicious.
- **Refactoring** — automated rename tools may refuse to rename lowercase classes.
- **First impression** — recruiters and reviewers form an opinion in seconds. Lowercase class names signal "beginner."

## The project's violations

| File | Should be |
|---|---|
| `main.java` | `Main.java` or `InternManagementApp.java` |
| `oracleConnector.java` | `OracleConnector.java` (then split into `OracleInternRepository`, etc.) |
| `toolkit.java` | `Toolkit.java` (then split into `PasswordHasher`, `PasswordGenerator`, `RecordFormatter`) |
| `loginController.java` | `LoginController.java` |
| `insertionInternController.java` | `InternManagementController.java` or `InsertInternController.java` |
| `insertionUserController.java` | `UserManagementController.java` |
| `updateInternController.java` | `UpdateInternController.java` |
| `updateUserController.java` | `UpdateUserController.java` |
| `chiefDecisionController.java` | `ChiefDecisionController.java` |
| `DataPreprocessor.java` | (delete — dead code) |

Plus misspellings:
- `Intern_Mnagement_app` (artifactId) — should be `InternManagementApp`.
- `intern_manegement_app` (package) — should be `internmanagement`.
- `intern_mnagement_app` (module) — should be `internmanagement`.
- `requstes.sql` — should be `requests.sql`.
- FXML misspellings: `Serach`, `Accepte`, `Refuse`, `Departement`, `Describtion`, `Loaction`, `Paasword`, `Reciver`, `Statitics`.

## Fix

Use IntelliJ's "Rename Package" + "Rename Module" refactor. Update the GitHub repo name. Do this **first**, before any other refactoring, to avoid merge conflicts later.

## Further reading

- JLS §6.2 (Names and Identifiers).
- *Clean Code* (Martin), Chapter 2 (Meaningful Names).
- Google Java Style Guide.
