---
tags: [concept, javafx, layout, stackpane, flowpane]
type: concept
status: complete
---

# StackPane and FlowPane

## StackPane

Overlays children (z-axis). Useful for:
- Loading overlay.
- Empty/error state on top of a table.
- Centered content.

```xml
<StackPane>
    <TableView fx:id="tableView"/>
    <ProgressIndicator fx:id="loading" visible="false"/>
    <VBox fx:id="emptyState" visible="false" alignment="CENTER">
        <Label text="No results found"/>
    </VBox>
</StackPane>
```

Toggle visibility to switch between states.

## FlowPane

Wraps children like text. When a row is full, wraps to the next.

```xml
<FlowPane hgap="10" vgap="10">
    <Button text="Tag 1"/>
    <Button text="Tag 2"/>
    <Button text="Tag 3"/>
    <!-- wraps when window is too narrow -->
</FlowPane>
```

## When to use

- **StackPane** — overlays, state switching, centered content.
- **FlowPane** — tag clouds, chip lists, dynamic button groups.

## Project Connection

The fix uses `StackPane` for the StatusView (loading/empty/error states overlaid on the table). See [[23 - JavaFX UX and Polish/04 - Empty Loading Error States]].

## Further reading

- JavaFX `StackPane` and `FlowPane` documentation.
