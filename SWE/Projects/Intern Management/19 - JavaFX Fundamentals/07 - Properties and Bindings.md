---
tags: [concept, javafx, properties, bindings]
type: concept
status: complete
related:
  - [[06 - Design Patterns/11 - Observer Pattern]]
---

# Properties and Bindings

## What it is

JavaFX **Properties** are observable values. When a property changes, listeners are notified. **Bindings** establish relationships between properties.

## Property types

```java
StringProperty name = new SimpleStringProperty("Alice");
IntegerProperty age = new SimpleIntegerProperty(22);
BooleanProperty valid = new SimpleBooleanProperty(false);
DoubleProperty price = new SimpleDoubleProperty(9.99);
ObjectProperty<Intern> selected = new SimpleObjectProperty<>();
```

## Listeners

```java
name.addListener((obs, oldVal, newVal) -> {
    System.out.println("Name changed: " + oldVal + " → " + newVal);
});

name.set("Bob");  // prints: Name changed: Alice → Bob
```

## Bindings

```java
StringProperty name = new SimpleStringProperty("Alice");
StringProperty greeting = new SimpleStringProperty();

greeting.bind(Bindings.concat("Hello, ", name, "!"));
System.out.println(greeting.get());  // Hello, Alice!

name.set("Bob");
System.out.println(greeting.get());  // Hello, Bob!
```

`greeting` is automatically updated when `name` changes.

## Bidirectional binding

```java
StringProperty a = new SimpleStringProperty("Alice");
StringProperty b = new SimpleStringProperty();
a.bindBidirectional(b);
System.out.println(b.get());  // Alice

b.set("Bob");
System.out.println(a.get());  // Bob
```

Changes propagate both ways.

## UI binding

```java
@FXML private TextField nameField;

StringProperty name = new SimpleStringProperty();
name.bindBidirectional(nameField.textProperty());
// Now `name` and the TextField's text are in sync.
```

## Computed properties

```java
BooleanProperty hasInput = new SimpleBooleanProperty();
hasInput.bind(name.isNotEmpty().and(email.isNotEmpty()));

Button submit = new Button("Submit");
submit.disableProperty().bind(hasInput.not());
// Submit is disabled until both name and email are non-empty.
```

## Why this matters

- **Reactive UI** — the UI updates automatically when data changes.
- **No manual update code** — no `if (changed) { updateLabel(); updateButton(); }`.
- **MVVM** — the ViewModel exposes properties; the View binds to them.

## Project Connection

The project uses almost no bindings. Controllers manually read fields, manually update labels, manually enable/disable buttons. The fix: expose properties on a ViewModel; bind the FXML to them.

## Further reading

- JavaFX Properties tutorial.
