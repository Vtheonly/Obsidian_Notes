---
tags: [pattern, behavioral, command]
type: concept
status: complete
related:
  - [[06 - Design Patterns/17 - Strategy Pattern]]
---

# Command Pattern

> "Encapsulate a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations." — GoF

## What it is

A **command** is an object that encapsulates an action. Instead of calling `service.doThing()`, you create a `DoThingCommand` object and execute it.

```java
public interface Command<T> {
    T execute();
}

public class AcceptInternCommand implements Command<Void> {
    private final InternService service;
    private final long internId;
    private final long chiefId;

    public AcceptInternCommand(InternService service, long internId, long chiefId) { ... }

    @Override
    public Void execute() {
        service.acceptIntern(internId, chiefId);
        return null;
    }
}

// Usage
Command<Void> cmd = new AcceptInternCommand(service, 123, 456);
cmd.execute();
```

## Why it exists

- **Undo/redo** — store the command, call `undo()` to reverse it.
- **Queueing** — put commands in a queue, execute them later (background jobs).
- **Logging** — log each command for audit.
- **Macro recording** — record a sequence of commands, replay them.

## Undo support

```java
public interface UndoableCommand<T> extends Command<T> {
    void undo();
}

public class AcceptInternCommand implements UndoableCommand<Void> {
    private Intern previousState;  // captured before execute

    public Void execute() {
        previousState = repository.findById(internId).orElseThrow();
        service.acceptIntern(internId, chiefId);
        return null;
    }

    public void undo() {
        repository.save(previousState);  // restore
    }
}
```

## Project Connection

The project's bulk "Accept All" / "Reject All" operations are perfect candidates for the Command pattern:
- Each accept/reject is a command.
- The commands are queued and executed atomically.
- If one fails, the whole batch can be rolled back (or just that command, depending on requirements).
- The commands can be logged for audit.

## Common pitfalls

- **Command that's just a function** — if the command has no state, use a `Runnable` or method reference.
- **Too many commands** — every action wrapped in a command is overkill. Use for undoable, queueable, or auditable operations.

## Further reading

- *Design Patterns* (GoF), Command.
