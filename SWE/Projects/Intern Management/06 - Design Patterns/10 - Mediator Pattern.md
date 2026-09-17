---
tags: [pattern, behavioral, mediator]
type: concept
status: complete
related:
  - [[06 - Design Patterns/11 - Observer Pattern]]
  - [[20 - JavaFX Layout and CSS/07 - Single-Stage Navigation]]
---

# Mediator Pattern

> "Define an object that encapsulates how a set of objects interact. Mediator promotes loose coupling by keeping objects from referring to each other explicitly, and it lets you vary their interaction independently." — GoF

## What it is

A **mediator** is an object that coordinates communication between other objects (colleagues). Instead of colleagues calling each other directly, they call the mediator.

```
Without mediator:
  A → B, A → C, B → A, B → C, C → A, C → B  (6 dependencies)

With mediator:
  A → M, B → M, C → M, M → A, M → B, M → C  (mediator centralizes)
```

## Example: NavigationController

```java
public class NavigationController {
    private final Stage stage;
    private final AuthService auth;
    private final InternService interns;

    public void showLogin() { stage.setScene(loginScene()); }
    public void showMainView(User user) {
        if (user.getRole() == Role.ADMIN) showAdminView();
        else if (user.getRole() == Role.CHIEF) showChiefView();
        else showSecretaryView();
    }
    public void showAdminView() { stage.setScene(adminScene()); }
    public void showUpdateInternDialog(Intern intern) { /* modal */ }
    // ...
}
```

Controllers don't call each other. They call `NavigationController`, which decides what to show.

## Why it exists

- **Decoupling** — colleagues don't know each other.
- **Centralized logic** — the mediator owns the interaction rules.
- **Reusability** — colleagues can be used in other contexts (with a different mediator).

## Mediator vs Observer

- **Mediator** — colleagues talk to the mediator (centralized).
- **Observer** — colleagues talk to each other via events (decentralized).

Mediator is better when the interaction is complex. Observer is better when the interaction is simple and one-to-many.

## Project Connection

The project has no mediator. Each controller opens new `Stage`s directly, knows about other controllers' FXML files. The fix: `NavigationController` that owns the single `Stage` and swaps scenes. See [[20 - JavaFX Layout and CSS/07 - Single-Stage Navigation]].

## Common pitfalls

- **God mediator** — the mediator knows too much. Keep it focused on coordination.
- **Colleagues that bypass the mediator** — they call each other directly. Enforce the mediator.

## Further reading

- *Design Patterns* (GoF), Mediator.
