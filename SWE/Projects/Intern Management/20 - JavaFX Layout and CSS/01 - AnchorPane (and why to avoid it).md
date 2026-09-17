---
tags: [concept, javafx, layout, anchorpane]
type: concept
status: complete
---

# AnchorPane (and why to avoid it)

## What it is

`AnchorPane` anchors children to its edges. You set `layoutX`, `layoutY`, `AnchorPane.leftAnchor`, etc.

```xml
<AnchorPane>
    <TextField layoutX="48.0" layoutY="54.0"/>
    <Button text="Login" layoutX="150.0" layoutY="100.0"/>
</AnchorPane>
```

## Why the project uses it

It's the default in Scene Builder's preview — you drag a control, it gets absolute coordinates. Easy for beginners.

## Why it's bad

### 1. Not responsive
Absolute coordinates don't adapt to:
- Different window sizes (resizing shows empty space).
- Different DPI (4K displays make the UI tiny; 13" laptops make it huge).
- Different font sizes (accessibility).

### 2. Fragile
Add a new field, and you have to manually adjust the coordinates of everything below it.

### 3. Not maintainable
Reading `layoutX="48.0" layoutY="54.0"` tells you nothing about the intent. Was 48 chosen for a reason, or arbitrary?

### 4. Not composable
You can't extract a reusable component — its coordinates are tied to its parent's size.

## The alternative: layout panes

Use **layout panes** that compute positions based on rules:
- `BorderPane` — top/left/center/right/bottom regions.
- `GridPane` — rows and columns.
- `VBox` / `HBox` — vertical / horizontal stacks.
- `StackPane` — overlay.
- `FlowPane` — wrap.

These adapt to window size, font size, DPI automatically.

## Project Connection

**Every** FXML file in the project uses `AnchorPane` with `layoutX`/`layoutY`. The fix: replace with `BorderPane` (top-level), `GridPane` (forms), `VBox`/`HBox` (linear).

See [[20 - JavaFX Layout and CSS/02 - BorderPane]], [[20 - JavaFX Layout and CSS/05 - GridPane]], [[20 - JavaFX Layout and CSS/09 - VBox and HBox]].

## Further reading

- JavaFX Layout Panes tutorial.
