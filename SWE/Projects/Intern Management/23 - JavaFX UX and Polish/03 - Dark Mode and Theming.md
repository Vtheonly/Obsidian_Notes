---
tags: [concept, ux, theming, dark-mode]
type: concept
status: complete
prerequisites:
  - [[20 - JavaFX Layout and CSS/04 - Design Tokens (CSS Variables)]]
---

# Dark Mode and Theming

## What it is

Allowing the user to switch between light and dark themes.

## Implementation

### CSS with theme classes
```css
.root {
    -color-bg: #FFFFFF;
    -color-text: #1E293B;
    -color-surface: #F8FAFC;
}

.root.dark {
    -color-bg: #0F172A;
    -color-text: #F8FAFC;
    -color-surface: #1E293B;
}

.label { -fx-text-fill: -color-text; }
```

### Toggle
```java
@FXML
public void toggleTheme() {
    Scene scene = ...;
    if (scene.getRoot().getStyleClass().contains("dark")) {
        scene.getRoot().getStyleClass().remove("dark");
    } else {
        scene.getRoot().getStyleClass().add("dark");
    }
}
```

### Persist preference
```java
Preferences prefs = Preferences.userNodeForPackage(App.class);
prefs.putBoolean("darkMode", true);
boolean dark = prefs.getBoolean("darkMode", false);
```

### Follow OS
```java
// JavaFX 19+: detect OS dark mode
boolean osDark = ... ;  // platform-specific
if (osDark) scene.getRoot().getStyleClass().add("dark");
```

## JavaFX built-in stylesheets

```java
// Application.setUserAgentStylesheet(Application.STYLESHEET_MODENA);  // default light
// There's no built-in dark, but community ones exist:
Application.setUserAgentStylesheet(getClass().getResource("modena-dark.css").toExternalForm());
```

## Project Connection

The project has no theming — hardcoded colors. The fix: design tokens (CSS variables), a `.dark` class, a Settings menu toggle, persisted preference.

## Further reading

- JavaFX CSS documentation.
- jmetro's JavaFX dark themes.
