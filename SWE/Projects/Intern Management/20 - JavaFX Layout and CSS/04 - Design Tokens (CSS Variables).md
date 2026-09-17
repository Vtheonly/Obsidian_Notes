---
tags: [concept, javafx, css, design-tokens]
type: concept
status: complete
prerequisites:
  - [[20 - JavaFX Layout and CSS/03 - CSS in JavaFX]]
---

# Design Tokens (CSS Variables)

## What it is

**Design tokens** are named values (colors, fonts, spacing) that ensure consistency across the UI. In JavaFX CSS, you define them as variables on `.root`.

```css
.root {
    /* Colors */
    -color-primary: #0F766E;
    -color-primary-hover: #115E59;
    -color-danger: #EF4444;
    -color-success: #10B981;
    -color-surface: #FFFFFF;
    -color-text: #1E293B;
    -color-text-muted: #94A3B8;
    -color-border: #CBD5E1;

    /* Typography */
    -fx-font-family: "Segoe UI", "Helvetica Neue", sans-serif;
    -fx-font-size: 13px;

    /* Spacing */
    -spacing-xs: 4px;
    -spacing-sm: 8px;
    -spacing-md: 16px;
    -spacing-lg: 24px;

    /* Radius */
    -radius-sm: 4px;
    -radius-md: 6px;
    -radius-lg: 8px;
}
```

## Using tokens

```css
.button-primary {
    -fx-background-color: -color-primary;
    -fx-text-fill: -color-text;
    -fx-padding: -spacing-sm -spacing-md;
    -fx-background-radius: -radius-md;
}

.button-primary:hover {
    -fx-background-color: -color-primary-hover;
}
```

## Why tokens

- **Consistency** — every "primary" button is the same color.
- **Theming** — change one variable, the whole UI updates.
- **Dark mode** — define a `.dark` class with different tokens.
- **Maintainability** — no magic hex values scattered around.

## Dark/light theme switching

```java
scene.getRoot().getStyleClass().add("dark");  // toggle
```

```css
.root { -color-surface: #FFFFFF; -color-text: #1E293B; }
.root.dark { -color-surface: #1E293B; -color-text: #F8FAFC; }
```

## Project Connection

The project has no design tokens — every color is an inline hex literal. The fix: define tokens in `style.css`, use `styleClass` everywhere, never inline styles.

## Further reading

- Design Tokens W3C Community Group.
- Material Design Design Tokens.
