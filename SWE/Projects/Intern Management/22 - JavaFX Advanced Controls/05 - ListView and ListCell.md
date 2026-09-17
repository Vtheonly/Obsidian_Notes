---
tags: [concept, javafx, listview, listcell]
type: concept
status: complete
related:
  - [[22 - JavaFX Advanced Controls/08 - TableView]]
---

# ListView and ListCell

## What it is

`ListView<T>` is a virtualized list (single column). Use when the data isn't tabular (e.g., a list of items with complex layouts).

## Basic usage

```java
ListView<Intern> listView = new ListView<>(FXCollections.observableArrayList(interns));
listView.setCellFactory(lv -> new InternListCell());
```

## Custom ListCell

```java
public class InternListCell extends ListCell<Intern> {
    private final HBox layout = new HBox(10);
    private final Label nameLabel = new Label();
    private final Label emailLabel = new Label();
    private final Button viewButton = new Button("View");

    public InternListCell() {
        layout.getChildren().addAll(nameLabel, emailLabel, viewButton);
        viewButton.setOnAction(e -> {
            Intern item = getItem();
            if (item != null) showDetail(item);
        });
    }

    @Override
    protected void updateItem(Intern intern, boolean empty) {
        super.updateItem(intern, empty);
        if (empty || intern == null) {
            setGraphic(null);
        } else {
            nameLabel.setText(intern.getName());
            emailLabel.setText(intern.getEmail());
            setGraphic(layout);
        }
    }
}
```

## ListView vs TableView

| | ListView | TableView |
|---|---|---|
| Columns | 1 | Many |
| Layout | Custom (HBox, VBox, anything) | Tabular |
| Sorting | Manual | Built-in (column click) |
| Editing | Manual | Built-in (cell factory) |
| Use case | Complex item layout | Tabular data |

## Project Connection

The project's TitledPane-in-VBox is closer to a `ListView` use case (complex per-item layout) than a `TableView`. But for intern search results, `TableView` is better — it's tabular data (name, email, status, actions).

Use `ListView` for the email list, notification list, or any non-tabular list.

## Further reading

- JavaFX `ListView` documentation.
