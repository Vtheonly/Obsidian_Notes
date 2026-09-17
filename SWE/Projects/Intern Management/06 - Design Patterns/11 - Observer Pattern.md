---
tags: [pattern, behavioral, observer]
type: concept
status: complete
related:
  - [[19 - JavaFX Fundamentals/00 - MOC - JavaFX]]
  - [[06 - Design Patterns/10 - Mediator Pattern]]
---

# Observer Pattern

> "Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically." — GoF

## What it is

An **observable** (subject) maintains a list of **observers**. When the observable's state changes, it notifies all observers.

```java
public interface Observable {
    void addObserver(Observer o);
    void removeObserver(Observer o);
    void notifyObservers();
}

public interface Observer {
    void update(Observable o);
}
```

## Java's built-in support

Java has `java.util.Observable` (deprecated in Java 9) and `java.beans.PropertyChangeSupport`. Modern Java uses `PropertyChangeListener` or reactive streams.

## JavaFX properties are Observers

```java
StringProperty name = new SimpleStringProperty("Alice");
name.addListener((obs, oldVal, newVal) -> {
    System.out.println("Name changed from " + oldVal + " to " + newVal);
});
name.set("Bob");  // prints: Name changed from Alice to Bob
```

The `StringProperty` is the observable. The `ChangeListener` is the observer. When `name.set()` changes the value, all listeners are notified.

## EventBus (publish-subscribe)

For cross-component communication, use an **event bus** (Guava EventBus, Spring ApplicationEventPublisher):

```java
// Publisher
eventBus.post(new InternAcceptedEvent(internId, chiefId));

// Subscriber
@Subscribe
public void onInternAccepted(InternAcceptedEvent event) {
    emailService.sendAcceptanceEmail(event.internId());
}
```

The publisher and subscriber don't know each other — they communicate via the bus.

## Why it exists

- **Decoupling** — the observable doesn't know who its observers are.
- **Multiple listeners** — many observers can react to one event.
- **Reactive** — the system reacts to state changes automatically.

## Project Connection

The project's `static String labelText` is a (broken) attempt at cross-controller communication. The fix: use JavaFX properties or an EventBus for "intern accepted" → "refresh list" notifications.

## Common pitfalls

- **Memory leaks** — if an observer is registered but never unregistered, it can't be GC'd. Use weak references or explicit `removeObserver`.
- **Cascade updates** — observer A updates the observable, which notifies observer B, which updates, which notifies A... infinite loop.
- **Order of notification** — observers are notified in registration order. If order matters, use a priority queue.

## Further reading

- *Design Patterns* (GoF), Observer.
- JavaFX Properties documentation.
