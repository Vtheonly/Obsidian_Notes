---
tags: [concept, javafx, lifecycle]
type: concept
status: complete
---

# Application Lifecycle

## The Application class

```java
public class MyApp extends Application {
    @Override
    public void init() throws Exception {
        // Runs on the launcher thread, before start().
        // Initialize resources, load config, etc.
        // CANNOT touch the UI (scene graph not ready).
    }

    @Override
    public void start(Stage primaryStage) throws Exception {
        // Runs on the JavaFX Application Thread.
        // Build the UI and show it.
        Parent root = FXMLLoader.load(getClass().getResource("main.fxml"));
        primaryStage.setScene(new Scene(root));
        primaryStage.show();
    }

    @Override
    public void stop() throws Exception {
        // Runs on the JavaFX Application Thread when the app is closing.
        // Clean up resources, close connections, save state.
        dataSource.close();
    }

    public static void main(String[] args) {
        launch(args);  // creates the Application, calls init(), then start()
    }
}
```

## Lifecycle sequence

1. `main()` calls `launch()`.
2. JavaFX runtime creates the `Application` instance.
3. `init()` runs (launcher thread) — no UI access.
4. JavaFX Application Thread starts.
5. `start(primaryStage)` runs (FX thread) — build and show UI.
6. App runs, handling events.
7. User closes the last window (or `Platform.exit()`).
8. `stop()` runs (FX thread) — cleanup.
9. JVM exits.

## Parameters

```java
@Override
public void start(Stage stage) {
    Parameters params = getParameters();
    String dbUrl = params.getNamed().get("db-url");
    List<String> rawArgs = params.getRaw();
    // ...
}

// Run: java MyApp --db-url=jdbc:oracle:thin:@...
```

## HostServices

```java
getHostServices().showDocument("https://example.com");  // opens browser
```

## Project Connection

The project's `main.java` only overrides `start()`. No `init()` (so no resource initialization) and no `stop()` (so no cleanup — the connection pool stays open on JVM exit, which is fine for a desktop app but bad for a server).

The fix:
```java
public class InternManagementApp extends Application {
    private HikariDataSource dataSource;

    @Override
    public void init() {
        dataSource = createDataSource();  // init pool on launcher thread
    }

    @Override
    public void start(Stage stage) {
        // build UI, show
    }

    @Override
    public void stop() {
        dataSource.close();  // clean up
    }
}
```

## Further reading

- JavaFX `Application` documentation.
