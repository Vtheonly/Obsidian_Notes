---
tags: [concept, javafx, propertyvaluefactory, binding]
type: concept
status: complete
prerequisites:
  - [[22 - JavaFX Advanced Controls/08 - TableView]]
  - [[19 - JavaFX Fundamentals/07 - Properties and Bindings]]
---

# PropertyValueFactory

## What it is

`PropertyValueFactory<S, T>` is a convenience class that maps a `TableColumn` to a property of the row object by name.

```java
TableColumn<Intern, String> colName = new TableColumn<>("Name");
colName.setCellValueFactory(new PropertyValueFactory<>("name"));
```

This tells the column: "for each `Intern`, call `nameProperty()` (or `getName()`) and use the result as the cell value."

## How it works

For `PropertyValueFactory<>("name")` on an `Intern`:
1. Look for `nameProperty()` — if it returns an `ObservableValue<String>`, use that (enables live updates).
2. Else look for `getName()` — use the return value (no live updates).
3. Else look for the `name` field — use reflection (last resort).

## For records

Java records use accessor methods like `name()`, not `getName()`. `PropertyValueFactory` doesn't find these by default (in older JavaFX). Workarounds:

### Option 1: Use a lambda
```java
colName.setCellValueFactory(cell -> new SimpleObjectProperty<>(cell.getValue().name()));
```

### Option 2: JavaFX 19+ supports records
JavaFX 19+ `PropertyValueFactory` recognizes record accessors. Check your version.

### Option 3: Use JavaFX properties in the model
```java
public class Intern {
    private final StringProperty name = new SimpleStringProperty();
    public StringProperty nameProperty() { return name; }
    public String getName() { return name.get(); }
}
```
`PropertyValueFactory` finds `nameProperty()` — live updates work.

## Why live updates matter

If the `Intern`'s name changes and the cell is bound to `nameProperty()`, the cell updates automatically. If it's bound to `getName()` (a snapshot), the cell shows the old value until the table is refreshed.

## Project Connection

The fix uses `Intern` records. For `PropertyValueFactory` compatibility, either:
- Use a lambda (`cell -> new SimpleObjectProperty<>(cell.getValue().name())`).
- Or use JavaFX 19+ which supports records.
- Or use JavaFX property classes instead of records.

## Further reading

- JavaFX `PropertyValueFactory` documentation.
