---
tags: [concept, ux, empty-state, loading, error]
type: concept
status: complete
related:
  - [[21 - JavaFX Concurrency/05 - UI State Machine Pattern]]
---

# Empty, Loading, and Error States

## The three states every async view must handle

### Loading state
Show a spinner or progress bar. Disable the search button. The user knows the app is working.

```xml
<StackPane>
    <TableView fx:id="tableView" visible="false"/>
    <ProgressIndicator fx:id="loading" visible="true"/>
</StackPane>
```

### Empty state
Show a helpful message and suggested actions.

```xml
<VBox fx:id="emptyState" alignment="CENTER" visible="false">
    <Label text="No interns found" styleClass="label-title"/>
    <Label text="Try adjusting your search filters." styleClass="label-muted"/>
    <Button text="Clear Filters" onAction="#handleClearFilters"/>
</VBox>
```

### Error state
Show the error and a retry button. Don't show raw stack traces.

```xml
<VBox fx:id="errorState" alignment="CENTER" visible="false">
    <Label text="Something went wrong" styleClass="label-error"/>
    <Label fx:id="errorDetail" styleClass="label-muted"/>
    <Button text="Retry" onAction="#handleRetry"/>
</VBox>
```

### Presenting state
The table (or list) is visible with data.

## Why this matters

- **Loading** — the user doesn't think the app froze.
- **Empty** — the user knows the search completed; they're not staring at a blank screen wondering.
- **Error** — the user knows what went wrong and can act (retry, contact support).

Without these states, the user sees:
- A blank screen during loading (looks frozen).
- A blank screen when no results (looks broken).
- A `JOptionPane` with `e.getMessage()` on error (looks unprofessional, leaks internals).

## Project Connection

The project has none of these states — empty VBox on no results, `JOptionPane` on error, nothing during loading. The fix: StatusView component with the 4-state machine.

## Further reading

- Nielsen Norman Group — Empty States.
