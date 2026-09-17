---
tags: [case-study, code-walkthrough, documentation]
type: case-study
status: complete
---

# README and Hidden Features

## README.md (213 lines)

### What it claims
- "The system displays..." (future tense throughout).
- "Security Measures: RBAC, Reverse Engineering Protection (Obfuscation), Password Hashing."
- References `EmailService` and `ReportService` classes that **don't exist**.
- Mentions "No Results Found" display (not implemented).
- Documents role IDs: 4=Manager, 5=Chief, <4=Secretary; 1/2/3 sub-levels.

### What's wrong
1. **Future tense** — written as a spec, not as documentation.
2. **No build instructions** — no `mvn javafx:run`, no `docker compose up`.
3. **No prerequisites** — no JDK version, no Maven version, no Docker requirement.
4. **No architecture diagram** — no Mermaid, no PNG.
5. **No screenshots.**
6. **No contributor guide.**
7. **No license.**
8. **Claims features that don't exist**:
   - "Reverse Engineering Protection (Obfuscation)" — no ProGuard/obfuscation config in `pom.xml`.
   - `EmailService` class — doesn't exist. The email tab's Button has no `onAction`.
   - `ReportService` class — doesn't exist. The report tab uses `makePDF()` directly in the controller.
   - "No Results Found" display — not implemented. Empty VBox is shown.
9. **Inconsistent role naming** — README calls role 4 "Manager" but `oracleConnector.isAdmin` calls it "Admin".
10. **No mention of which SQL file to run.**

### Fix
Rewrite README with:
1. One-paragraph elevator pitch.
2. Architecture diagram (Mermaid).
3. Prerequisites (JDK 21+, Docker, Maven).
4. `docker compose up` + `mvn javafx:run` quickstart.
5. Screenshots.
6. "What's intentionally simplified" section (be honest).
7. License (MIT).

See [[24 - Build and Tooling/00 - MOC - Build and Tooling]].

## Hidden / Dead Features

### Email tab (intern_insertion.fxml)
- `TextField` + `HTMLEditor` + `Button text="Send"` with **no `onAction`**.
- `javax.mail` declared in `pom.xml` and `requires java.mail` in `module-info.java`.
- **No `EmailService` class exists. No `javax.mail` imports anywhere. No email-sending code.**
- The email feature is declared in pom/FXML/README but **never implemented**.

### Report tab → PDF
- `HTMLEditor fx:id="PDF_INPUT"` + `Button text="Serach" onAction="#makePDF"`.
- `makePDF` uses `com.lowagie.text.HTMLWorker` (deprecated since 2010).
- Writes to `document_now.pdf` in CWD (no FileChooser).
- `pdfbox` dependency declared but **not used** (the code uses `openpdf`).

### `PrintButton` in insertionInternController
- Created in `addToPool`.
- `setOnAction` commented out: `// PrintButton.setOnAction(event ->{})`.
- Dead button — clicking does nothing.

### Cancel buttons in update FXMLs
- `cancelButton="true"` but **no `onAction`**.
- Pressing Esc does nothing.

### `startDatePicker` in chiefDecisionController
- Declared in `decision_Intern.fxml`.
- **Not `@FXML`-injected in `chiefDecisionController`** — silent dead UI element.

### `startDatePicker` in updateInternController
- `@FXML`-injected.
- **Never read or set** — dead injection.

### Dead schema tables
`profile`, `function_and_menu`, `function_and_menu_profile`, `responsible_theme`, `department_theme`, `theme_intern`, `responsible` — defined in `insertion.sql`, never queried by any Java code.

### Dead branch in `getIdByName`
```java
if (tableName.equals("responsible")) { ... }
```
Unreachable — `tableName` is reassigned earlier in the switch.

### `"worker_user_user"` case in `getIdByName` switch
Never called by any controller. Pseudo-table name (not a real table).

### `toolkit.isHashEqual`
Dead method — never called anywhere.

### `DataPreprocessor.java`
Entire class is a dead duplicate of `toolkit.preProcess`.

### Commented-out code
- `// oracleConnector.updateTheme(...)` in `insertionUserController`.
- `// PrintButton.setOnAction(event ->{})` in `insertionInternController`.
- `// connection.commit(); // Uncomment if auto-commit is disabled` in `oracleConnector`.

### TODOs in production code
- `// TODO make a string to text-date`
- `// TODO make a reference to the user id`
- `// TODO add a print functionality`
- `// todo : put "addtopools" this into a separate class`

## The lesson

Every dead feature, dead table, dead method, and TODO is a liability. Reviewers see them and assume:
- The author doesn't finish what they start.
- The author doesn't understand what `static` means (instantiating `oracleConnector`).
- The author doesn't read their own code (Cancel buttons with no action).
- The author doesn't test (email tab that does nothing, sample users that can't log in).

**YAGNI** — You Aren't Gonna Need It. Delete dead code. Implement claimed features or remove them from the README. See [[04 - OOD and SOLID/25 - YAGNI (You Aren't Gonna Need It)]].
