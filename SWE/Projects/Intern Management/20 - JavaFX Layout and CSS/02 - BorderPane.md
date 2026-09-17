---
tags: [concept, javafx, layout, borderpane]
type: concept
status: complete
---

# BorderPane

## What it is

`BorderPane` divides the area into 5 regions: top, left, center, right, bottom.

```
┌─────────────────────────┐
│         TOP             │
├─────┬─────────────┬─────┤
│LEFT │   CENTER    │RIGHT│
│     │             │     │
├─────┴─────────────┴─────┤
│        BOTTOM           │
└─────────────────────────┘
```

## Usage

```xml
<BorderPane>
    <top>
        <MenuBar>...</MenuBar>
    </top>
    <left>
        <VBox styleClass="sidebar">...</VBox>
    </left>
    <center>
        <StackPane fx:id="contentArea"/>
    </center>
    <bottom>
        <HBox styleClass="status-bar">...</HBox>
    </bottom>
</BorderPane>
```

## Behavior

- `center` expands to fill available space.
- `top`/`bottom` take their preferred height.
- `left`/`right` take their preferred width.

## When to use

- **Top-level app layout** — menu bar on top, sidebar on left, content in center, status bar on bottom.
- **Master-detail** — list on left, detail in center.

## Project Connection

The fix replaces `AnchorPane` with `BorderPane` for the main app layout:
```xml
<BorderPane fx:controller="...MainLayoutController">
    <top><MenuBar>...</MenuBar></top>
    <left><VBox styleClass="sidebar">...</VBox></left>
    <center><StackPane fx:id="contentWorkspace"/></center>
</BorderPane>
```

The sidebar navigates; the center swaps views.

## Further reading

- JavaFX `BorderPane` documentation.
