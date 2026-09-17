---
tags: [concept, javafx, css, styling]
type: concept
status: complete
---

# CSS in JavaFX

## What it is

JavaFX supports CSS styling via `-fx-` properties. CSS separates style from structure.

## Loading a stylesheet

```java
Scene scene = new Scene(root);
scene.getStylesheets().add(getClass().getResource("style.css").toExternalForm());
```

Or in FXML:
```xml
<VBox stylesheets="@style.css">
```

## CSS selectors

```css
/* Type selector */
.label { -fx-text-fill: #333; }

/* Class selector */
.button-primary { -fx-background-color: #0F766E; }

/* ID selector */
#usernameField { -fx-border-color: red; }

/* Combined */
.button-primary:hover { -fx-background-color: #115E59; }
```

## `-fx-` properties

JavaFX CSS uses `-fx-` prefixed properties:
- `-fx-background-color`
- `-fx-text-fill`
- `-fx-font-size`, `-fx-font-weight`, `-fx-font-family`
- `-fx-border-color`, `-fx-border-width`, `-fx-border-radius`
- `-fx-background-radius`
- `-fx-padding`
- `-fx-spacing`

## Pseudo-classes

```css
.button:hover { ... }
.button:pressed { ... }
.button:disabled { ... }
.button:focused { ... }
.table-row-cell:selected { ... }
.table-row-cell:empty { ... }
```

## The project's CSS problem

`style.css` is **empty**. All styling is inline:
```xml
<Label style="-fx-text-fill: green;"/>
<Button style="-fx-background-color: #F8981C;"/>
```

Problems:
- **No reuse** — change the brand color, find-and-replace across every FXML.
- **No theming** — can't switch light/dark.
- **No consistency** — each form has slightly different padding.
- **Inconsistent colors** — the hex values drift between files.

## The fix

`style.css` with design tokens (CSS variables):
```css
.root {
    -color-primary: #0F766E;
    -color-primary-hover: #115E59;
    -color-danger: #EF4444;
    -color-success: #10B981;
    -color-surface: #1E293B;
    -color-text: #F8FAFC;
    -color-text-muted: #94A3B8;
    -color-border: #334155;
}

.label { -fx-text-fill: -color-text; }

.button-primary {
    -fx-background-color: -color-primary;
    -fx-text-fill: white;
}
.button-primary:hover { -fx-background-color: -color-primary-hover; }

.badge-accepted { -fx-background-color: rgba(16, 185, 129, 0.15); -fx-text-fill: -color-success; }
.badge-pending { -fx-background-color: rgba(245, 158, 11, 0.15); -fx-text-fill: #F59E0B; }
.badge-rejected { -fx-background-color: rgba(239, 68, 68, 0.15); -fx-text-fill: -color-danger; }
```

FXML uses class names:
```xml
<Label styleClass="badge-accepted" text="Accepted"/>
<Button styleClass="button-primary" text="Save"/>
```

## Further reading

- JavaFX CSS Reference Guide.
