---
tags: [concept, javafx, layout, vbox, hbox]
type: concept
status: complete
---

# VBox and HBox

## VBox

Lays out children vertically (top to bottom).

```xml
<VBox spacing="10" alignment="CENTER">
    <Label text="Title"/>
    <TextField promptText="Search..."/>
    <Button text="Search"/>
</VBox>
```

- `spacing` — gap between children.
- `alignment` — overall alignment (CENTER, TOP_LEFT, etc.).
- `fillWidth` — if true, children expand to fill width.

## HBox

Lays out children horizontally (left to right).

```xml
<HBox spacing="10" alignment="CENTER_RIGHT">
    <Region HBox.hgrow="ALWAYS"/>  <!-- spacer -->
    <Button text="Cancel"/>
    <Button text="Submit"/>
</HBox>
```

- `HBox.hgrow="ALWAYS"` — child expands to fill space.
- `HBox.margin` — per-child margins.

## Common patterns

### Spacer
```xml
<HBox>
    <Label text="Left"/>
    <Region HBox.hgrow="ALWAYS"/>
    <Label text="Right"/>
</HBox>
```

### Button bar
```xml
<HBox spacing="10" alignment="CENTER_RIGHT">
    <Button text="Cancel" styleClass="button-secondary"/>
    <Button text="Save" styleClass="button-primary"/>
</HBox>
```

## When to use

- **VBox** — vertical stacks (form fields, list items, sidebar buttons).
- **HBox** — horizontal stacks (button bars, status indicators, form rows).

## Project Connection

The fix uses `VBox` for sidebars and form columns, `HBox` for button bars and form rows.

## Further reading

- JavaFX `VBox` and `HBox` documentation.
