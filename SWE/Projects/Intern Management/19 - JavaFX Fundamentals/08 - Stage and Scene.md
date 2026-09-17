---
tags: [concept, javafx, stage, scene]
type: concept
status: complete
---

# Stage and Scene

## Stage

A **Stage** is a window. It's the top-level container.

```java
Stage stage = new Stage();
stage.setTitle("My App");
stage.setScene(scene);
stage.show();
```

### Modality
- `Modality.NONE` — non-modal (default).
- `Modality.WINDOW_MODAL` — blocks the parent window.
- `Modality.APPLICATION_MODAL` — blocks the entire app.

```java
Stage dialog = new Stage();
dialog.initOwner(primaryStage);
dialog.initModality(Modality.APPLICATION_MODAL);
dialog.showAndWait();  // blocks until closed
```

## Scene

A **Scene** is the content of a Stage. It holds the scene graph root.

```java
Parent root = FXMLLoader.load(getClass().getResource("view.fxml"));
Scene scene = new Scene(root, 800, 600);
stage.setScene(scene);
```

## Single-Stage navigation (recommended)

The project opens a new Stage per view — clutters the taskbar, memory leaks. The fix: single Stage, swap Scenes (or swap the center of a BorderPane).

```java
// Instead of:
Stage adminStage = new Stage();
adminStage.setScene(new Scene(adminRoot));
adminStage.show();

// Do:
primaryStage.setScene(new Scene(adminRoot));
```

Or, with a StackPane as root:
```java
StackPane root = (StackPane) primaryStage.getScene().getRoot();
root.getChildren().setAll(adminRoot);
```

## Project Connection

The project opens new Stages for:
- Login → admin/chief/secretary view.
- Update intern dialog.
- Update user dialog.

Each is a separate window in the taskbar. The fix: single Stage, scene swap for main navigation; modal dialog for update forms.

## Further reading

- JavaFX `Stage` and `Scene` documentation.
