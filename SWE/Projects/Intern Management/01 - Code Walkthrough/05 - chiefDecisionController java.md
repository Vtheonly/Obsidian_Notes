---
tags: [case-study, code-walkthrough, javafx, controller]
type: case-study
status: complete
---

# chiefDecisionController.java (147 lines)

## What it does

Chief of Department view. SplitPane:
- Left: ButtonBar (`Accepte All`, `Refuse All`, `Search` — misspellings) + GridPane form (`fullNameField`, `themeChoiceBox`, `startDatePicker` — latter two unused).
- Right: ScrollPane → VBox `ResultPool` — same TitledPane-in-VBox pattern.

## `acceptedAll` and `rejectedAll`

```java
public void acceptedAll() {
    oracleConnector.setAllInternsAccepted();
}
public void rejectedAll() {
    oracleConnector.setAllInternsRejected();
}
```

Bulk update with **no confirmation dialog**. One click → all interns marked Accepted/Rejected. No undo.

### What's wrong
1. **No confirmation** — destructive bulk operation with no "Are you sure?".
2. **No undo** — once clicked, the change is permanent (no soft delete, no audit log).
3. **No filtering** — "Accept All" accepts ALL interns in the DB, not just the search results.
4. **No transaction** — `setAllInternsAccepted` does `UPDATE interns SET status='Accepted'` (no WHERE). If it fails halfway, some interns are Accepted and some are Pending.

### Fix
- Confirmation dialog: `Alert(AlertType.CONFIRMATION).showAndWait()`.
- Apply only to the current search filter, not all interns.
- Wrap in a transaction.
- Log to `audit_logs` with the chief's user ID, timestamp, and before/after state.

## `searchIntern` — same N+1

Same as `insertionInternController.searchIntern`: `oracleConnector.searchIntern` then `getNameById` per row. 100 interns = 101 queries.

## `addToPool` — `parseText` called twice

```java
String innerLabelText = innerLabel.getText();
Map<String, String> params1 = parseText(innerLabelText);
String internId = params1.get("Intern ID");
Map<String, String> params2 = parseText(innerLabelText);  // redundant!
String name = params2.get("Name");
```

Parses the same string twice. Could parse once and access both keys.

## `oracleConnector Connection = new oracleConnector();`

```java
private oracleConnector Connection = new oracleConnector();
```

Instantiates a class with only static methods and no instance state. The instance is never used (every method is called statically via `oracleConnector.method()`). Wasteful allocation, signals the author doesn't understand `static`.

### Fix
Remove the line. Call `oracleConnector.method()` directly. Better: inject a `ChiefDecisionService` via constructor. See [[05 - Software Architecture/04 - Dependency Injection]].
