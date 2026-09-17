---
tags: [concept, javafx, tableview, controls]
type: concept
status: complete
related:
  - [[22 - JavaFX Advanced Controls/10 - Virtualization (how it works)]]
  - [[22 - JavaFX Advanced Controls/02 - Custom Cell Factories]]
---

# TableView

## What it is

`TableView<T>` is a virtualized, sortable, editable table. It's the correct control for tabular data — replacing the project's TitledPane-in-VBox anti-pattern.

## Basic usage

```java
@FXML private TableView<Intern> tableView;
@FXML private TableColumn<Intern, Long> colId;
@FXML private TableColumn<Intern, String> colName;
@FXML private TableColumn<Intern, String> colEmail;

private final ObservableList<Intern> data = FXCollections.observableArrayList();

@Override
public void initialize(URL url, ResourceBundle rb) {
    colId.setCellValueFactory(new PropertyValueFactory<>("internId"));
    colName.setCellValueFactory(new PropertyValueFactory<>("name"));
    colEmail.setCellValueFactory(new PropertyValueFactory<>("email"));
    tableView.setItems(data);
}

@FXML
public void handleSearch() {
    data.setAll(repository.findByName(searchField.getText()));
}
```

## Features

- **Sorting** — click a column header to sort. `tableView.setSortPolicy(...)` for custom sorting.
- **Column reordering** — drag columns.
- **Column resizing** — drag column borders. `CONSTRAINED_RESIZE_POLICY` auto-fills width.
- **Selection** — `tableView.getSelectionModel().getSelectedItem()`.
- **Editing** — `colName.setCellFactory(TextFieldTableCell.forTableColumn())`.
- **Context menu** — `tableView.setContextMenu(...)`.
- **Row factory** — `tableView.setRowFactory(...)` for per-row styling.

## Selection

```java
tableView.getSelectionModel().selectedItemProperty().addListener((obs, old, selected) -> {
    if (selected != null) {
        showDetail(selected);
    }
});

// Multi-selection
tableView.getSelectionModel().setSelectionMode(SelectionMode.MULTIPLE);
List<Intern> selected = tableView.getSelectionModel().getSelectedItems();
```

## Constrained resize policy

```xml
<TableView>
    <columnResizePolicy>
        <TableView fx:constant="CONSTRAINED_RESIZE_POLICY"/>
    </columnResizePolicy>
</TableView>
```

Columns auto-resize to fill the table width.

## Project Connection

The project uses `VBox` + `TitledPane` for search results. 1000 interns = 1000 TitledPanes, each a heavy graphical node. Memory explosion, scroll lag.

The fix: `TableView<Intern>`. 1000 interns = ~20 visible cells (virtualized). Memory and performance are constant.

## Further reading

- JavaFX `TableView` documentation.
