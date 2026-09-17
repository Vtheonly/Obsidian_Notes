---
tags: [concept, ux, keyboard, shortcuts, mnemonics]
type: concept
status: complete
related:
  - [[23 - JavaFX UX and Polish/01 - Accessibility (a11y)]]
---

# Keyboard Shortcuts and Mnemonics

## Mnemonics

```xml
<Button text="_Save"/>     <!-- Alt+S -->
<Button text="_Cancel"/>   <!-- Alt+C -->
<Menu text="_File">        <!-- Alt+F -->
    <MenuItem text="_Open"/>  <!-- then O -->
</Menu>
```

The `_` prefix (with `mnemonicParsing="true"`) makes the next character an Alt+key shortcut.

## Keyboard shortcuts (accelerators)

```java
MenuItem saveItem = new MenuItem("Save");
saveItem.setAccelerator(new KeyCodeCombination(KeyCode.S, KeyCombination.CONTROL_DOWN));
// Ctrl+S (Cmd+S on macOS)
```

## Common shortcuts

| Shortcut | Action |
|---|---|
| Ctrl+N | New |
| Ctrl+S | Save |
| Ctrl+F | Search |
| Ctrl+P | Print |
| Ctrl+W | Close |
| Ctrl+Q | Quit |
| F5 | Refresh |
| Esc | Cancel / close dialog |
| Enter | Confirm |

## Global key handlers

```java
scene.setOnKeyPressed(e -> {
    if (e.isControlDown() && e.getCode() == KeyCode.S) {
        handleSave();
        e.consume();
    }
});
```

## Why this matters

- **Power users** — keyboard is faster than mouse.
- **Accessibility** — keyboard-only users can navigate.
- **Professional** — every desktop app supports standard shortcuts.

## Project Connection

The project has no keyboard shortcuts. `mnemonicParsing="false"` on buttons. The fix: enable mnemonics, add Ctrl+S (save), Ctrl+F (search), F5 (refresh), Esc (cancel).

## Further reading

- JavaFX Mnemonics and Accelerators.
