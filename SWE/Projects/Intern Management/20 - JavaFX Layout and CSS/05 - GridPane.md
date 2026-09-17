---
tags: [concept, javafx, layout, gridpane]
type: concept
status: complete
---

# GridPane

## What it is

`GridPane` lays out children in a grid of rows and columns.

## Usage

```xml
<GridPane hgap="10" vgap="10">
    <columnConstraints>
        <ColumnConstraints percentWidth="30" halignment="RIGHT"/>
        <ColumnConstraints percentWidth="70"/>
    </columnConstraints>

    <Label text="Name:" GridPane.rowIndex="0" GridPane.columnIndex="0"/>
    <TextField fx:id="nameField" GridPane.rowIndex="0" GridPane.columnIndex="1"/>

    <Label text="Email:" GridPane.rowIndex="1" GridPane.columnIndex="0"/>
    <TextField fx:id="emailField" GridPane.rowIndex="1" GridPane.columnIndex="1"/>
</GridPane>
```

## ColumnConstraints

```xml
<ColumnConstraints percentWidth="30"/>  <!-- 30% of grid width -->
<ColumnConstraints percentWidth="70"/>
```

Or with fixed/min/max:
```xml
<ColumnConstraints minWidth="100" prefWidth="200" maxWidth="400" hgrow="ALWAYS"/>
```

## RowConstraints

```xml
<RowConstraints minHeight="30" vgrow="ALWAYS"/>
```

## Spanning

```xml
<Button text="Submit" GridPane.rowIndex="3" GridPane.columnIndex="0"
        GridPane.columnSpan="2"/>  <!-- spans 2 columns -->
```

## Alignment

```xml
<Label text="Name:" GridPane.halignment="RIGHT" GridPane.valignment="CENTER"/>
```

## When to use

- **Forms** — label on left, field on right.
- **Tabular layouts** (but `TableView` is better for data).

## Project Connection

The fix uses `GridPane` with percentage-based `ColumnConstraints` for forms:
```xml
<GridPane hgap="15" vgap="15">
    <columnConstraints>
        <ColumnConstraints percentWidth="30" halignment="RIGHT"/>
        <ColumnConstraints percentWidth="70"/>
    </columnConstraints>
    <!-- form fields -->
</GridPane>
```

The form adapts to window resize — labels stay right-aligned, fields fill.

## Further reading

- JavaFX `GridPane` documentation.
