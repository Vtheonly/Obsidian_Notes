---
tags: [concept, javafx, responsive, layout]
type: concept
status: complete
---

# Responsive Layouts

## What it is

A responsive layout adapts to different window sizes, DPIs, and font sizes.

## Techniques

### 1. Use layout panes (not AnchorPane)
`BorderPane`, `GridPane`, `VBox`, `HBox` compute positions dynamically.

### 2. Percentage-based sizing
```xml
<ColumnConstraints percentWidth="30"/>
<ColumnConstraints percentWidth="70"/>
```

### 3. Grow / shrink
```xml
<TextField HBox.hgrow="ALWAYS"/>  <!-- fills available width -->
<Region HBox.hgrow="ALWAYS"/>     <!-- spacer -->
```

### 4. Bind to parent size
```java
label.prefWidthProperty().bind(parent.widthProperty());
```

### 5. Constrained resize policy (TableView)
```xml
<TableView>
    <columnResizePolicy><TableView fx:constant="CONSTRAINED_RESIZE_POLICY"/></columnResizePolicy>
</TableView>
```
Columns auto-resize to fill the table width.

### 6. Min/max width
```xml
<TextField minWidth="200" maxWidth="500"/>
```

### 7. Window size listeners
```java
stage.widthProperty().addListener((obs, old, newW) -> {
    if (newW.doubleValue() < 600) {
        sidebar.setVisible(false);
    } else {
        sidebar.setVisible(true);
    }
});
```

### 8. CSS media queries (limited)
JavaFX CSS doesn't support media queries directly, but you can toggle stylesheets based on size:
```java
scene.widthProperty().addListener((obs, o, n) -> {
    if (n.doubleValue() < 768) {
        scene.getStylesheets().setAll(mobileCss);
    } else {
        scene.getStylesheets().setAll(desktopCss);
    }
});
```

## Project Connection

The project uses `AnchorPane` with absolute coordinates — nothing is responsive. The fix: layout panes, percentage sizing, grow/shrink.

## Further reading

- JavaFX Layout tutorial.
