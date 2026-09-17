---
tags: [concept, javafx, state-machine, ux]
type: concept
status: complete
prerequisites:
  - [[21 - JavaFX Concurrency/04 - Task (javafx.concurrent)]]
  - [[02 - CS Foundations/11 - State Machines]]
related:
  - [[23 - JavaFX UX and Polish/04 - Empty Loading Error States]]
---

# UI State Machine Pattern

## What it is

Every async view has 4 states:
- **LOADING** — spinner visible, table hidden.
- **EMPTY** — "no results" message, table hidden.
- **ERROR** — error message + retry button, table hidden.
- **PRESENTING** — table visible with data.

The UI State Machine pattern explicitly manages these states.

## Implementation

```java
private enum UIState { LOADING, EMPTY, ERROR, PRESENTING }

@FXML private StackPane root;
@FXML private ProgressIndicator loadingIndicator;
@FXML private VBox emptyState;
@FXML private VBox errorState;
@FXML private Label errorDetail;
@FXML private TableView<Intern> tableView;

private void setState(UIState state) {
    switch (state) {
        case LOADING:
            loadingIndicator.setVisible(true);
            emptyState.setVisible(false);
            errorState.setVisible(false);
            tableView.setVisible(false);
            break;
        case EMPTY:
            loadingIndicator.setVisible(false);
            emptyState.setVisible(true);
            errorState.setVisible(false);
            tableView.setVisible(false);
            break;
        case ERROR:
            loadingIndicator.setVisible(false);
            emptyState.setVisible(false);
            errorState.setVisible(true);
            tableView.setVisible(false);
            break;
        case PRESENTING:
            loadingIndicator.setVisible(false);
            emptyState.setVisible(false);
            errorState.setVisible(false);
            tableView.setVisible(true);
            break;
    }
}
```

## FXML structure

```xml
<StackPane fx:id="root">
    <TableView fx:id="tableView" visible="false"/>
    <ProgressIndicator fx:id="loadingIndicator" visible="false"/>
    <VBox fx:id="emptyState" visible="false" alignment="CENTER">
        <Label text="No results found"/>
    </VBox>
    <VBox fx:id="errorState" visible="false" alignment="CENTER">
        <Label fx:id="errorDetail"/>
        <Button text="Retry" onAction="#handleRetry"/>
    </VBox>
</StackPane>
```

## Wiring to a Service

```java
service.setOnScheduled(e -> setState(UIState.LOADING));
service.setOnSucceeded(e -> {
    List<Intern> data = service.getValue();
    if (data.isEmpty()) {
        setState(UIState.EMPTY);
    } else {
        tableView.getItems().setAll(data);
        setState(UIState.PRESENTING);
    }
});
service.setOnFailed(e -> {
    errorDetail.setText(service.getException().getMessage());
    setState(UIState.ERROR);
});
```

## Why this matters

- **Clear UX** — the user always knows what's happening.
- **No "frozen" states** — the loading indicator shows the app is working.
- **Recovery** — the error state offers a retry button.
- **Encourages async** — the state machine only makes sense if work is async.

## Project Connection

The project has no state management — empty results show an empty VBox, errors show a `JOptionPane`, loading shows nothing. The fix: StatusView component with the 4-state machine.

## Further reading

- Nielsen Norman Group — Empty States.
