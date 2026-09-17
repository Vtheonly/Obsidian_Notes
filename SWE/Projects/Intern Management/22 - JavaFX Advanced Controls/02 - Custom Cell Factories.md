---
tags: [concept, javafx, cell-factory, controls]
type: concept
status: complete
prerequisites:
  - [[22 - JavaFX Advanced Controls/08 - TableView]]
  - [[22 - JavaFX Advanced Controls/10 - Virtualization (how it works)]]
---

# Custom Cell Factories

## What it is

A **cell factory** creates (or recycles) the cells in a `TableColumn` or `ListView`. The default cell shows text; a custom cell can show buttons, badges, images, etc.

## Example: status badge

```java
public class StatusBadgeCell extends TableCell<Intern, DecisionStatus> {
    @Override
    protected void updateItem(DecisionStatus status, boolean empty) {
        super.updateItem(status, empty);
        if (empty || status == null) {
            setGraphic(null);
            setText(null);
        } else {
            Label badge = new Label(status.name());
            badge.getStyleClass().addAll("badge", "badge-" + status.name().toLowerCase());
            setGraphic(badge);
            setText(null);
        }
    }
}

// Usage
colStatus.setCellFactory(col -> new StatusBadgeCell());
```

CSS:
```css
.badge { -fx-padding: 4 8; -fx-background-radius: 12; -fx-font-size: 11; -fx-font-weight: bold; }
.badge-pending { -fx-background-color: #FEF3C7; -fx-text-fill: #92400E; }
.badge-accepted { -fx-background-color: #DCFCE7; -fx-text-fill: #166534; }
.badge-rejected { -fx-background-color: #FEE2E2; -fx-text-fill: #991B1B; }
```

## Example: action buttons

```java
public class ActionCell extends TableCell<Intern, Void> {
    private final Button editButton = new Button("Edit");
    private final Button deleteButton = new Button("Delete");

    public ActionCell(InternService service) {
        editButton.setOnAction(e -> {
            Intern intern = getTableView().getItems().get(getIndex());
            // open edit dialog
        });
        deleteButton.setOnAction(e -> {
            Intern intern = getTableView().getItems().get(getIndex());
            service.delete(intern.getId());
        });
    }

    @Override
    protected void updateItem(Void item, boolean empty) {
        super.updateItem(item, empty);
        if (empty) {
            setGraphic(null);
        } else {
            setGraphic(new HBox(5, editButton, deleteButton));
        }
    }
}

// Usage
colActions.setCellFactory(col -> new ActionCell(internService));
```

## Project Connection

The project builds action buttons by walking the scene graph (`DeleteButton.getParent().getParent()...`). The fix: a custom cell factory that holds the `Intern` directly via `getTableView().getItems().get(getIndex())`. No tree walking.

## Common pitfalls

- **Not handling `empty`** — stale cells show old data.
- **Creating nodes in `updateItem`** — slow; create once in the constructor, just update content in `updateItem`.
- **Not calling `super.updateItem`** — broken cell state.

## Further reading

- JavaFX Cell Factories tutorial.
