---
tags: [case-study, code-walkthrough, javafx, controller]
type: case-study
status: complete
---

# insertionUserController.java (444 lines)

## What it does

Admin view. Tabs: Manage_User, Manage_theme, Manage_Departement (note trailing space and misspelling), Statitics (misspelled).
- Three SplitPanes for CRUD forms (worker, theme, department), each with `Glow` effect.
- HBox with password `TextField` (not PasswordField) + Button → `makePassword()`.
- Two `PieChart`s with **hardcoded** data.

## Hardcoded PieChart data

```java
ObservableList<PieChart.Data> themeChartData =
    FXCollections.observableArrayList(
        new PieChart.Data("Department 3", 33),
        new PieChart.Data("Department 2", 20),
        new PieChart.Data("Department 1", 17),
        new PieChart.Data("Department 1", 30)  // duplicate key!
    );
theme_chart.setData(themeChartData);
```

### What's wrong
1. **Data is hardcoded, not from DB** — the chart shows the same numbers every time, regardless of actual intern counts.
2. **Duplicate key "Department 1"** appears twice (17 and 30). The second overwrites the first in `ObservableList`. No validation.
3. **Magic numbers 33/20/17/30** — no source, no explanation.
4. **No labels** on the chart — no percentage, no count, no tooltip.

### Fix
Query the DB: `SELECT d.department_name, COUNT(*) FROM interns i JOIN departments d ON i.department_id = d.department_id GROUP BY d.department_name`. Use a Materialized View for `O(1)` dashboard queries. See [[12 - Advanced Database Features/06 - Materialized Views]].

## `insertWorkerUserController` — wrong key

```java
insertParameters.put("department", "");  // BUG: should be "department_id"
```

This passes an empty string under the key `"department"` to `insertWorkerUser`. The DAO iterates the map and tries to insert into a `department` column that doesn't exist → SQL error.

## `insertThemeController` and `insertDepartmentController`

Near-identical to `insertWorkerUserController`. Copy-paste × 3. DRY violation.

### Fix
Extract a generic `CrudRepository<T, ID>` interface + `AbstractJdbcRepository<T, ID>` template. Each entity provides only a `RowMapper<T>` and table metadata. See [[05 - Software Architecture/14 - Repository Pattern]] and [[06 - Design Patterns/18 - Template Method Pattern]].

## `makePassword()`

```java
public void makePassword() {
    password.setText(toolkit.generatePassword());
}
```

Calls `toolkit.generatePassword()` (8-char ASCII) and sets the password field. See [[01 - Code Walkthrough/12 - toolkit java and DataPreprocessor java]].

## Three `addToXPool` methods

`addToWorkerUserPool`, `addToThemePool`, `addToDepartmentPool` — copy-pasted three times with only the entity name differing. Same TitledPane-in-VBox anti-pattern, same UI tree walking, same inline CSS.

### Fix
Extract a generic `ResultListPanel<T>` component that takes a `Function<T, String>` formatter and a `Function<T, Node>` actions factory. See [[06 - Design Patterns/17 - Strategy Pattern]] and [[22 - JavaFX Advanced Controls/02 - Custom Cell Factories]].
