---
tags: [pattern, structural, composite]
type: concept
status: complete
related:
  - [[19 - JavaFX Fundamentals/00 - MOC - JavaFX]]
---

# Composite Pattern

> "Compose objects into tree structures to represent part-whole hierarchies. Composite lets clients treat individual objects and compositions of objects uniformly." — GoF

## What it is

A **composite** is a tree structure where leaf nodes and container nodes implement the same interface. Clients treat them uniformly.

```java
public interface Shape {
    void draw();
}

public class Circle implements Shape {  // leaf
    public void draw() { /* draw circle */ }
}

public class Group implements Shape {  // composite
    private List<Shape> children = new ArrayList<>();
    public void add(Shape s) { children.add(s); }
    public void draw() { children.forEach(Shape::draw); }  // delegates to children
}
```

`Group` can contain `Circle`s, other `Group`s, or any `Shape`. Calling `draw()` on a group draws all its children recursively.

## JavaFX scene graph is a Composite

```java
// Node is the interface
// Parent (subclass of Node) has children
// Group, Pane, Region are Parents
// Button, Label, TextField are leaf Nodes

Parent root = new VBox(
    new Label("Name:"),
    new HBox(
        new TextField(),
        new Button("OK")
    )
);
```

A `VBox` contains a `Label` and an `HBox`. The `HBox` contains a `TextField` and a `Button`. Calling `root.layout()` lays out the entire tree recursively.

## Why it exists

- **Uniform treatment** — the client doesn't care if a node is a leaf or a container.
- **Recursive structure** — trees are natural for UIs, file systems, org charts.
- **Extensibility** — add new leaf types without changing the composite.

## When to use

- Tree structures (UI, file system, org chart).
- When leaves and containers should be treated the same way.

## Project Connection

The project uses JavaFX's composite scene graph, but doesn't compose its own UIs into reusable components. The fix: extract reusable components (e.g., `StatusView`, `ValidatedTextField`) that can be composed into larger views.

## Further reading

- *Design Patterns* (GoF), Composite.
