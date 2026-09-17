---
tags: [pattern, creational, abstract-factory]
type: concept
status: complete
related:
  - [[06 - Design Patterns/08 - Factory Pattern]]
---

# Abstract Factory Pattern

## What it is

> "Provide an interface for creating families of related or dependent objects without specifying their concrete classes." — GoF

An **abstract factory** creates *families* of related objects. Each concrete factory produces a consistent family.

```java
public interface ThemeFactory {
    Button createButton();
    TextField createTextField();
    Label createLabel();
}

public class DarkThemeFactory implements ThemeFactory {
    public Button createButton() { return new DarkButton(); }
    public TextField createTextField() { return new DarkTextField(); }
    // ...
}

public class LightThemeFactory implements ThemeFactory {
    public Button createButton() { return new LightButton(); }
    // ...
}
```

The client uses `ThemeFactory` without knowing whether it's dark or light. All components from one factory are consistent.

## Difference from Factory Method

- **Factory Method** — creates one type of object. Decoupling is the goal.
- **Abstract Factory** — creates a *family* of related objects. Consistency is the goal.

## When to use

- When you need families of related objects (themes, database dialects, platform-specific UIs).
- When the family must be consistent (don't mix dark buttons with light text fields).

## When NOT to use

- When you only need one type of object (use Factory Method).
- When the family has only one member.

## Project Connection

The project could use Abstract Factory for theming (dark/light JavaFX themes), but it's not a priority. The reviews don't recommend it.

## Further reading

- *Design Patterns* (GoF), Abstract Factory.
