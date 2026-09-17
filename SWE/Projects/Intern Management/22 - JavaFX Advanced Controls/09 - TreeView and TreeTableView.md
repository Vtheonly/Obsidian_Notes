---
tags: [concept, javafx, treeview, treetableview]
type: concept
status: complete
---

# TreeView and TreeTableView

## What it is

- `TreeView<T>` — hierarchical list (expand/collapse).
- `TreeTableView<T>` — hierarchical table.

## Use cases

- File system browser.
- Org chart (employee → manager → manager's manager).
- Department → themes → interns hierarchy.

## Example

```java
TreeView<String> tree = new TreeView<>();
TreeItem<String> root = new TreeItem<>("Departments");
root.setExpanded(true);

for (Department dept : departments) {
    TreeItem<String> deptNode = new TreeItem<>(dept.getName());
    for (Theme theme : dept.getThemes()) {
        deptNode.getChildren().add(new TreeItem<>(theme.getName()));
    }
    root.getChildren().add(deptNode);
}

tree.setRoot(root);
```

## Project Connection

The project doesn't use trees. A tree view could show the department → theme → intern hierarchy. Useful for navigation.

## Further reading

- JavaFX `TreeView` documentation.
