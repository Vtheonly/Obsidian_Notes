---
tags: [concept, rebuild, phase-3]
type: concept
status: complete
---

# Phase 3 — UI/UX Overhaul (16-24 hours)

> Goal: make the UI look like a 2025 commercial application, not a 2010 Swing port.

## Tasks

### 1. Write `style.css` with design tokens
```css
.root {
    -color-primary: #0F766E;
    -color-danger: #EF4444;
    -color-success: #10B981;
    -color-surface: #1E293B;
    -color-text: #F8FAFC;
    /* ... */
}
```

### 2. Replace AnchorPane with BorderPane + GridPane + VBox/HBox
- Top-level: `BorderPane` (top=menu, left=sidebar, center=content).
- Forms: `GridPane` with percentage-based `ColumnConstraints`.
- Linear: `VBox` / `HBox`.

### 3. Replace TitledPane-in-VBox with TableView<Intern>
- Virtualized, sortable, filterable.
- Custom cell factories for status badges and action buttons.
- `FilteredList` + `SortedList` for live search.

### 4. Define StatusView component
Loading / Empty / Error / Presenting states. Use on every async view.

### 5. Add inline form validation
- `TextField` focusedProperty listener.
- `.error` CSS class for red border.
- Inline `Label` for error message.
- Disable submit until valid.

### 6. Remove `<Glow/>` effect
Replace inline color literals with CSS classes.

### 7. Add menu bar + toolbar
File / Edit / View / Help. Keyboard shortcuts (Ctrl+N, Ctrl+F, Ctrl+S).

### 8. Add accessibility
- `mnemonicParsing="true"` + `text="_Save"`.
- `accessibleText` on every interactive control.
- Test with NVDA / VoiceOver.

### 9. Add i18n
- `messages.properties` (English).
- `messages_fr.properties` (French).
- `messages_ar.properties` (Arabic).
- `%key` in FXML.
- `nodeOrientation="RIGHT_TO_LEFT"` for Arabic.

### 10. Add Logout, About, Settings dialogs
Theme switch, language switch.

## After Phase 3

The UI is modern, responsive, accessible, and internationalized. Reviewers see a 2025 commercial app, not a student project.

## Further reading

- [[20 - JavaFX Layout and CSS/00 - MOC - JavaFX Layout]].
- [[23 - JavaFX UX and Polish/00 - MOC - JavaFX UX]].
