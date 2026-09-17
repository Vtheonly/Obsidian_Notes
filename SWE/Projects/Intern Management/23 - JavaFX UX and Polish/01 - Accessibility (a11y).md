---
tags: [concept, ux, accessibility, a11y, wcag]
type: concept
status: complete
related:
  - [[23 - JavaFX UX and Polish/08 - Keyboard Shortcuts and Mnemonics]]
---

# Accessibility (a11y)

## Why

- **Legal** — WCAG 2.1 AA is required in many jurisdictions (EAA, Section 508).
- **Moral** — visually impaired users deserve to use your app.
- **Practical** — keyboard power users prefer keyboard nav.

## JavaFX a11y features

### accessibleText
```java
searchField.setAccessibleText("Search interns by name");
```
Screen readers (NVDA, VoiceOver) read this when the field is focused.

### accessibleHelp
```java
submitButton.setAccessibleHelp("Click to save the intern record");
```

### Mnemonics
```xml
<Button text="_Save"/>
```
`_S` makes Alt+S activate the button. Set `mnemonicParsing="true"` (default in some controls).

### Keyboard navigation
- Tab — move focus.
- Shift+Tab — reverse.
- Enter — activate button.
- Esc — close dialog.

JavaFX handles this by default if you don't override.

### Focus traversal
```java
field.setFocusTraversable(true);
```

### High contrast
```css
.root { -fx-background-color: black; -fx-text-fill: white; }
```
Or use the OS's high-contrast mode (JavaFX respects it on Windows).

### Color-independent
Don't rely on color alone to convey meaning:
```java
// Bad: green = accepted, red = rejected (colorblind users can't tell)
// Good: green "Accepted" badge, red "Rejected" badge (text + color)
```

## Testing

- **NVDA** (Windows) — free screen reader.
- **VoiceOver** (macOS) — built-in.
- **JavaFX Accessibility Scanner** (Oracle).
- Keyboard-only testing — unplug the mouse.

## Project Connection

The project has zero accessibility:
- No `accessibleText`.
- `mnemonicParsing="false"` on buttons (disables Alt+key).
- Status indicated by color alone (`-fx-text-fill: green`).
- No keyboard shortcuts.

The fix: add `accessibleText`, enable mnemonics, use text+color badges, test with NVDA.

## Further reading

- WCAG 2.1 (w3.org).
- JavaFX Accessibility documentation.
