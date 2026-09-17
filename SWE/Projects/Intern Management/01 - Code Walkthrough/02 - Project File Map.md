---
tags: [case-study, code-walkthrough, inventory]
type: case-study
status: complete
related:
  - "[[00 - Start Here/02 - Project Context — The Original Project]]"
---

# Project File Map

> Every file in `github.com/Vtheonly/JavaFX_Intern_Mnagement` and its role.

## Source tree

```
JavaFX_Intern_Mnagement/
├── README.md                              213 lines — claims features that don't exist
├── _.swp                                    12 KB   — Vim swap file (committed)
├── document_now.pdf                         836 B   — generated PDF (committed)
├── mvnw, mvnw.cmd                                   — Maven wrapper
├── pom.xml                                 194 lines — Maven build (typos, old deps, Java 20)
├── javafx-sdk-22/                          ~99 MB   — JavaFX SDK binary blob (anti-pattern)
│
└── src/
    ├── main/
    │   ├── docker-compose.yml               27 lines — Oracle XE (wrong mount path)
    │   ├── java/
    │   │   ├── module-info.java             13 lines — JPMS (module ≠ package typo)
    │   │   └── com/example/intern_manegement_app/
    │   │       ├── main.java                21 lines — JavaFX Application entry
    │   │       ├── oracleConnector.java    940 lines — God Class DAO
    │   │       ├── toolkit.java            160 lines — parsing, SHA-256, password gen
    │   │       ├── DataPreprocessor.java   125 lines — dead duplicate
    │   │       ├── loginController.java     72 lines — login flow
    │   │       ├── insertionInternController.java  376 lines — secretary view
    │   │       ├── insertionUserController.java   444 lines — admin view
    │   │       ├── updateInternController.java      81 lines — update intern form
    │   │       ├── updateUserController.java       105 lines — update worker_user form
    │   │       └── chiefDecisionController.java    147 lines — chief view
    │   ├── resources/
    │   │   ├── style.css                     0 lines — empty
    │   │   └── com/example/intern_manegement_app/
    │   │       ├── login_page.fxml          45 lines
    │   │       ├── intern_insertion.fxml   269 lines
    │   │       ├── user_insertion.fxml     293 lines
    │   │       ├── decision_Intern.fxml     88 lines
    │   │       ├── update_intern.fxml      100 lines
    │   │       ├── update_worker_user.fxml 113 lines
    │   │       └── sonatrach-logo.png
    │   └── sql/
    │       ├── insertion.sql               283 lines — main schema
    │       ├── requstes.sql                114 lines — legacy schema (typo)
    │       └── DROP.sql                     58 lines — PL/SQL drop-all
    └── test/  (does not exist — zero tests despite JUnit in pom.xml)
```

## File-by-file responsibility summary

| File | LOC | Role |
|---|---|---|
| `main.java` | 21 | JavaFX entry point. Loads `login_page.fxml`. |
| `oracleConnector.java` | 940 | God Class. Static Connection, all CRUD, login, search, update, delete, getMaxId, getNameById, getSelectableOptions, bulk accept/reject. ~30 `JOptionPane` calls. |
| `toolkit.java` | 160 | Static utilities: `parseText`, `formatString`, `preProcess`, `generatePassword`, `hashIt` (unsalted SHA-256), `isHashEqual` (dead+buggy). |
| `DataPreprocessor.java` | 125 | Dead duplicate of `toolkit.preProcess` with a `main()` test harness. Uses Java text blocks. |
| `loginController.java` | 72 | Login button. 3 redundant queries. Opens new `Stage` per role. |
| `insertionInternController.java` | 376 | Secretary view. Insert/search interns, TitledPane pool, PDF (deprecated `HTMLWorker`), email tab (no handler). |
| `insertionUserController.java` | 444 | Admin view. CRUD for workers, themes, departments. Two `PieChart`s with hardcoded data. |
| `chiefDecisionController.java` | 147 | Chief view. Search interns, accept/reject individually or bulk. |
| `updateInternController.java` | 81 | Update intern form, fed by `sendConstraint()`. |
| `updateUserController.java` | 105 | Update worker_user form. Displays password_hash in the password field. |
| `module-info.java` | 13 | JPMS descriptor. Module name `intern_mnagement_app` ≠ package `intern_manegement_app`. |
| 6 FXML files | 908 total | Absolute positioning, inline styles, Glow effect, empty `style.css`. |
| 3 SQL files | 455 total | Two conflicting schemas; Java only matches `insertion.sql`. |
| `pom.xml` | 194 | JavaFX 21.0.1, ojdbc8 19.8, pdfbox 2.0.24 (unused), openpdf 1.3.29, javax.mail 1.6.2 (unused), junit 5.10 (no tests). Java 20 (non-LTS). |
| `docker-compose.yml` | 27 | Oracle XE, port 1521, password `rootroot`, mounts `./sql-scripts` (wrong path). |

## Where to look first

If you only have 30 minutes to understand the project's problems:

1. `oracleConnector.java` lines 11–30 (hardcoded credentials + static Connection).
2. `oracleConnector.java` any insert/update/delete method (JOptionPane + dynamic SQL).
3. `toolkit.java` lines 100–130 (`hashIt` unsalted SHA-256 + `parseText` string surgery).
4. `insertionInternController.java` `addToPool` (TitledPane + UI tree walking).
5. Any FXML file (absolute positioning + inline styles + Glow effect).

You now understand 80% of what the reviews complain about.
