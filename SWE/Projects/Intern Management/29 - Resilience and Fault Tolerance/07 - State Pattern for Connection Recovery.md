---
tags: [concept, resilience, state-pattern, connection]
type: concept
status: complete
prerequisites:
  - [[02 - CS Foundations/11 - State Machines]]
  - [[29 - Resilience and Fault Tolerance/03 - Circuit Breaker Pattern]]
  - [[06 - Design Patterns/16 - State Pattern]]
---

# State Pattern for Connection Recovery

## What it is

A **Database Resilience Engine** that manages DB connection state: CONNECTED, RECONNECTING, OFFLINE. Automatically recovers from transient failures.

## Implementation

```java
public class DatabaseResilienceEngine {
    public enum ConnectionState { CONNECTED, RECONNECTING, OFFLINE }

    private final ReadOnlyObjectWrapper<ConnectionState> state =
        new ReadOnlyObjectWrapper<>(ConnectionState.CONNECTED);
    private final HikariDataSource dataSource;

    private static final int MAX_RETRIES = 5;
    private static final long BASE_BACKOFF_MS = 1000;
    private static final long MAX_BACKOFF_MS = 30000;

    public <T> T executeWithRetry(DatabaseOperation<T> operation) throws SQLException {
        int attempt = 0;
        while (true) {
            try (Connection conn = dataSource.getConnection()) {
                if (state.get() != ConnectionState.CONNECTED) {
                    state.set(ConnectionState.CONNECTED);
                }
                return operation.execute(conn);
            } catch (SQLException e) {
                attempt++;
                if (attempt >= MAX_RETRIES) {
                    state.set(ConnectionState.OFFLINE);
                    throw e;
                }
                state.set(ConnectionState.RECONNECTING);
                long backoff = calculateExponentialBackoff(attempt);
                Thread.sleep(backoff);
            }
        }
    }

    private long calculateExponentialBackoff(int attempt) {
        long backoff = BASE_BACKOFF_MS * (1L << attempt);
        long capped = Math.min(backoff, MAX_BACKOFF_MS);
        long jitter = ThreadLocalRandom.current().nextLong(0, capped / 10);
        return capped + jitter;
    }

    @FunctionalInterface
    public interface DatabaseOperation<T> {
        T execute(Connection conn) throws SQLException;
    }
}
```

## UI binding

```java
stateLabel.textProperty().bind(
    Bindings.createStringBinding(() ->
        engine.getCurrentState().toString(),
        engine.stateProperty()
    )
);

// Color-code: CONNECTED=green, RECONNECTING=amber, OFFLINE=red
```

The user sees the connection status in real time.

## Why

- **Self-healing** — the app recovers from a DB restart without user action.
- **Transparency** — the user knows the app is reconnecting.
- **Graceful degradation** — if the DB is permanently down, show "Offline" instead of crashing.

## Project Connection

The project's static `Connection` dies and stays dead. The fix: `DatabaseResilienceEngine` wrapping every DB call, with retry, backoff, and state tracking.

## Further reading

- *Release It!* (Nygard).
