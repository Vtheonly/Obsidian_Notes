---
tags: [concept, javafx, events]
type: concept
status: complete
---

# Events and Event Handlers

## What it is

JavaFX events are objects that represent user interactions (mouse, keyboard) or programmatic notifications. Event handlers respond to events.

## Event types

| Event | Trigger |
|---|---|
| `ActionEvent` | Button click, Enter in TextField |
| `MouseEvent` | Click, move, enter, exit, drag |
| `KeyEvent` | Key press, release, type |
| `WindowEvent` | Window show, close, hide |
| `DragEvent` | Drag and drop |

## Registering handlers

### FXML
```xml
<Button text="Login" onAction="#onLoginClick"/>
<TextField onKeyTyped="#onKeyTyped"/>
```

### Java
```java
button.setOnAction(event -> { ... });
button.setOnMouseClicked(event -> { ... });
textField.setOnKeyTyped(event -> { ... });
```

### addEventHandler (with event filter)
```java
node.addEventHandler(MouseEvent.MOUSE_CLICKED, event -> { ... });
node.addEventFilter(MouseEvent.MOUSE_CLICKED, event -> {
    // runs during the capture phase (before the target handler)
});
```

## Event propagation

Events travel through the scene graph in two phases:
1. **Capture** (top-down) — from root to target. Event filters run.
2. **Bubbling** (bottom-up) — from target to root. Event handlers run.

Use a filter to intercept events before they reach the target (e.g., global key handling).

## Consuming events

```java
button.setOnAction(event -> {
    doSomething();
    event.consume();  // stop propagation
});
```

## Project Connection

The project uses `onAction="#method"` in FXML — correct. But many buttons have no handler (Email tab's Send, Cancel buttons). The fix: either implement or remove.

## Further reading

- JavaFX Events documentation.
