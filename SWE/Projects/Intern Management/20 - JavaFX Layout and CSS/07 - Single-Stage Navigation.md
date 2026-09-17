---
tags: [concept, javafx, navigation, single-stage]
type: concept
status: complete
related:
  - [[19 - JavaFX Fundamentals/08 - Stage and Scene]]
  - [[06 - Design Patterns/10 - Mediator Pattern]]
---

# Single-Stage Navigation

## The problem with multiple Stages

The project opens a new `Stage` per view:
- Login → close login Stage, open admin Stage.
- Click "Update" → open update Stage.

Problems:
- Multiple windows in the taskbar.
- Independent minimization, focus.
- Memory leaks (controllers retain references to closed Stages).
- Security (closed login window is still in memory).
- Inconsistent UX.

## The fix: single Stage + scene swap

```java
public class NavigationController {
    private final Stage stage;

    public void showLogin() {
        stage.setScene(loadScene("login.fxml"));
    }

    public void showAdminView() {
        stage.setScene(loadScene("admin.fxml"));
    }

    public void showInternSearch() {
        stage.setScene(loadScene("intern_search.fxml"));
    }

    private Scene loadScene(String fxml) {
        try {
            Parent root = FXMLLoader.load(getClass().getResource(fxml));
            return new Scene(root);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
```

## Or: single Scene + swap the center

```java
public class NavigationController {
    private final Stage stage;
    private final StackPane contentArea;  // center of BorderPane

    public void showView(String fxml) {
        Parent view = FXMLLoader.load(getClass().getResource(fxml));
        contentArea.getChildren().setAll(view);
    }
}
```

The `BorderPane` stays; only the center changes.

## Modal dialogs

For modal dialogs (update forms, confirmations), use a separate Stage with `APPLICATION_MODAL`:
```java
Stage dialog = new Stage();
dialog.initOwner(primaryStage);
dialog.initModality(Modality.APPLICATION_MODAL);
dialog.setScene(new Scene(FXMLLoader.load(...)));
dialog.showAndWait();  // blocks until closed
```

This is the only case where a new Stage is appropriate.

## Project Connection

The project opens new Stages for every view. The fix: `NavigationController` with single-Stage scene swap; modal dialogs for update forms.

## Further reading

- JavaFX Navigation patterns.
