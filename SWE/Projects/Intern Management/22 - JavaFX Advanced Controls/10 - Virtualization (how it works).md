---
tags: [concept, javafx, virtualization, performance]
type: concept
status: complete
prerequisites:
  - [[22 - JavaFX Advanced Controls/08 - TableView]]
  - [[02 - CS Foundations/04 - Complexity Theory (Big-O)]]
---

# Virtualization (how it works)

## The problem

Without virtualization, a list of 10,000 items creates 10,000 UI nodes. Each node has:
- Layout calculations.
- Event handlers.
- Style computations.
- Memory (~1 KB per node, more for complex cells).

10,000 nodes = ~10 MB just for the list. Plus the layout time is O(n) per scroll.

## Virtualization

Virtualization creates **only the visible cells** (~20-30) and reuses them as you scroll.

```
Visible viewport: 800 px tall, 30 px per row → ~27 cells visible.

[Cell 1] [Cell 2] ... [Cell 27]  ← only these exist

As you scroll down:
- Cell 1 scrolls off the top.
- Cell 1 is reused for the new row at the bottom (its content is updated).
- Total cells: still 27.
```

## How JavaFX does it

`TableView` and `ListView` use a "cell recycling" mechanism:
1. The control creates enough cells to fill the viewport (~30).
2. As the user scrolls, cells that scroll off-screen are reused for new rows.
3. Each cell's `updateItem(T item, boolean empty)` is called to set its content.

## The `updateItem` contract

```java
public class InternCell extends TableCell<Intern, String> {
    @Override
    protected void updateItem(String value, boolean empty) {
        super.updateItem(value, empty);
        if (empty || value == null) {
            setText(null);
            setGraphic(null);
        } else {
            setText(value);
        }
    }
}
```

⚠️ **Critical**: always call `super.updateItem(item, empty)` first. Always handle the `empty` case (set text/graphic to null). Otherwise, cells show stale data when reused.

## Why this matters

- **Memory**: 10,000 items in a virtualized list use ~30 cells, not 10,000 nodes.
- **Performance**: scrolling is O(1) — only 30 cells update, not 10,000.
- **Startup**: instant (no need to create 10,000 nodes).

## The project's anti-pattern

The project's `addToPool` creates a new `TitledPane` (with labels, buttons, styles) per result. 1,000 results = 1,000 `TitledPane`s in a `VBox`. The VBox:
- Lays out all 1,000 children (O(n) per layout).
- Allocates memory for 1,000 nodes.
- Doesn't recycle — scrolling creates more nodes.

The fix: `TableView` with virtualization. Memory and layout are O(visible) = O(1).

## Further reading

- JavaFX Virtualization internals.
- "JavaFX TableView performance" articles.
