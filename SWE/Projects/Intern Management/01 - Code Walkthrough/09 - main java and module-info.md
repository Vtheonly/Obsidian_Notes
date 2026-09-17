---
tags: [case-study, code-walkthrough, javafx, jpms]
type: case-study
status: complete
---

# main.java and module-info.java

## main.java (21 lines)

```java
package com.example.intern_manegement_app;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.stage.Stage;
import java.io.IOException;
public class main extends Application {
    public static void main(String[] args) { launch(); }
    @Override
    public void start(Stage stage) throws IOException {
        FXMLLoader fxmlLoader = new FXMLLoader(main.class.getResource("login_page.fxml"));
        Scene scene = new Scene(fxmlLoader.load());
        stage.setScene(scene);
        stage.setTitle("login");
        stage.setResizable(true);
        stage.show();
    }
}
```

### What it does
- Extends `javafx.application.Application` (JavaFX entry point contract).
- `main()` calls `launch()` which calls `start()` on the JavaFX Application Thread.
- Loads `login_page.fxml` from the same package.
- Sets the scene on the primary stage, sets title, makes resizable, shows.

### What's wrong
1. **Lowercase class name `main`** violates JLS §6.2 (PascalCase). Should be `Main` or `InternManagementApp`.
2. **Hardcoded FXML path** — no DI, no controller factory, no way to swap views for testing.
3. **No exception handling** — if `fxmlLoader.load()` fails (missing FXML, malformed FXML), the exception propagates and the app dies with a stack trace.
4. **No `Application.Parameters` handling** — no way to pass command-line args (e.g., `--db-url=...`).
5. **Comment listing all FXML files** — dead comment, suggests the author copied FXML names from a list.

## module-info.java (13 lines)

```java
module com.example.intern_mnagement_app {
    requires javafx.controls;
    requires javafx.fxml;
    requires javafx.web;
    requires java.sql;
    requires java.mail;
    requires org.apache.pdfbox;
    requires java.desktop;
    requires com.github.librepdf.openpdf;
    requires javafx.graphics;
    opens com.example.intern_manegement_app to javafx.fxml;
    exports com.example.intern_manegement_app;
}
```

### What it does
- Declares a JPMS module named `com.example.intern_mnagement_app` (note typo: `mnagement`).
- `requires` JavaFX modules, `java.sql`, `java.mail`, `org.apache.pdfbox`, `java.desktop`, `com.github.librepdf.openpdf`.
- `opens` the package to `javafx.fxml` (so FXMLLoader can reflectively instantiate controllers).
- `exports` the package (so other modules could import it — none do).

### What's wrong
1. **Module name ≠ package name** — module is `intern_mnagement_app` (typo missing 'a'), package is `intern_manegement_app` (different typo). The `opens`/`exports` reference the package, so the module is internally inconsistent. This can produce `LayerInstantiationException` on stricter JDKs.
2. **`requires java.desktop`** — only needed because of `javax.swing.JOptionPane`. Mixing Swing and JavaFX is the root cause.
3. **`requires java.mail` and `org.apache.pdfbox`** — declared but **never used** in any Java file. Dead dependencies.
4. **No `requires transitive`** — fine for an app, but a library would need to expose transitive deps.
5. **No `uses`/`provides`** — no ServiceLoader usage (would be the modern way to do plugin architecture). See [[31 - Enterprise Java/04 - Java SPI (ServiceLoader)]].

## The fix

- Rename module to `com.example.internmanagement` (no typos, matches package).
- Remove `requires java.desktop`, `java.mail`, `org.apache.pdfbox`.
- Remove `requires javafx.web` (HTMLEditor is in `javafx.web`, but the email tab is dead).
- Move to Java 21 LTS (currently Java 20, non-LTS, EOL).
- Add a `Application.launch(InternManagementApp.class, args)` style entry point.

See [[24 - Build and Tooling/02 - JPMS Modules]] and [[24 - Build and Tooling/04 - Maven]] for the modern setup.
