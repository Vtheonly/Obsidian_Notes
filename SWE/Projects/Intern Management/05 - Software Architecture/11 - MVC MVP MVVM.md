---
tags: [concept, architecture, mvc, mvp, mvvm]
type: concept
status: complete
related:
  - [[05 - Software Architecture/10 - Layered Architecture]]
  - [[19 - JavaFX Fundamentals/00 - MOC - JavaFX]]
---

# MVC, MVP, MVVM

## Three UI architectural patterns

| Pattern | Year | Origin | Key feature |
|---|---|---|---|
| MVC | 1979 | Trygve Reenskaug (Smalltalk) | Controller mediates between Model and View |
| MVP | 1996 | Mike Potel (Taligent) | Presenter is the middleman; View is passive |
| MVVM | 2005 | John Gossman (Microsoft, WPF) | ViewModel exposes data bindable to View |

## MVC (Model-View-Controller)

```
   ┌──────────┐
   │   View   │ ←──────┐
   └────┬─────┘        │
        │              │
        ▼              │
   ┌──────────┐   ┌──────────┐
   │  Model   │←──│Controller│
   └──────────┘   └──────────┘
```

- **Model** — the data and business logic. Notifies the View of changes (Observer pattern).
- **View** — displays the model. Forwards user input to the Controller.
- **Controller** — handles input, updates the model.

Classic MVC (Smalltalk) had the View observing the Model directly. Web MVC (Rails, Spring MVC) simplified this: Controller fetches the Model and passes it to the View for rendering.

## MVP (Model-View-Presenter)

```
   ┌──────────┐
   │   View   │ ←──────┐
   └────┬─────┘        │
        │              │
        ▼              │
   ┌──────────┐   ┌──────────┐
   │Presenter │──→│   View   │ (via interface)
   └────┬─────┘   └──────────┘
        │
        ▼
   ┌──────────┐
   │  Model   │
   └──────────┘
```

- **Model** — data and business logic.
- **View** — passive (dumb) UI. Forwards all input to the Presenter. Implements a `View` interface.
- **Presenter** — handles input, updates the Model, updates the View via the interface.

The View is fully passive (no business logic). The Presenter is testable because it talks to the View through an interface (mockable).

## MVVM (Model-View-ViewModel)

```
   ┌──────────┐
   │   View   │ ←──────┐
   └────┬─────┘        │
        │              │ (two-way binding)
        ▼              │
   ┌──────────┐   ┌──────────┐
   │ViewModel │←──│   View   │
   └────┬─────┘   └──────────┘
        │
        ▼
   ┌──────────┐
   │  Model   │
   └──────────┘
```

- **Model** — data and business logic.
- **View** — the UI. Binds to the ViewModel's properties.
- **ViewModel** — exposes properties and commands the View binds to. No reference to the View.

The key feature: **two-way data binding**. When the ViewModel's `name` property changes, the View's TextField updates automatically. When the user types in the TextField, the ViewModel's `name` property updates automatically. No manual update code.

## Which one for JavaFX?

JavaFX is built for **MVVM**. Properties (`StringProperty`, `IntegerProperty`, `BooleanProperty`), bindings (`Bindings.bind`, `bindBidirectional`), and `ObservableValue` enable two-way binding.

```java
public class InternViewModel {
    private final StringProperty name = new SimpleStringProperty();
    private final StringProperty email = new SimpleStringProperty();
    private final BooleanProperty saveDisabled = new SimpleBooleanProperty(true);

    public InternViewModel() {
        saveDisabled.bind(name.isEmpty().or(email.isEmpty()));
    }

    public StringProperty nameProperty() { return name; }
    public StringProperty emailProperty() { return email; }
    public BooleanProperty saveDisabledProperty() { return saveDisabled; }

    public void save() { internService.save(new Intern(name.get(), email.get())); }
}
```

```xml
<TextField text="${viewModel.name}"/>
<TextField text="${viewModel.email}"/>
<Button text="Save" disable="${viewModel.saveDisabled}" onAction="#save"/>
```

## Project Connection

The project uses a degenerate MVC — Controllers directly manipulate the View (FXML fields) and directly call the Model (`oracleConnector`). There's no binding, no separation, no testability.

The fix: introduce ViewModels (or at least Presenters) and use JavaFX properties + bindings. See [[19 - JavaFX Fundamentals/00 - MOC - JavaFX]].

## Common pitfalls

- **"MVC" as a buzzword** — calling your architecture "MVC" without understanding the pattern. Most "MVC" apps are actually Smart UI.
- **Massive View Controller** — iOS's classic problem: controllers that do everything. Same as the project's controllers.
- **Binding everything** — two-way binding is powerful but can create hard-to-debug update cycles. Use it carefully.

## Further reading

- Reenskaug, "Models-Views-Controllers" (1979).
- Fowler, "GUI Architectures" (martinfowler.com).
- *Patterns of Enterprise Application Architecture* (Fowler).
