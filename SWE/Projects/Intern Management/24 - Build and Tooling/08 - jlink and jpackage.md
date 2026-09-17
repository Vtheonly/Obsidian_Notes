---
tags: [concept, java, jlink, jpackage, deployment]
type: concept
status: complete
related:
  - [[24 - Build and Tooling/02 - JPMS Modules]]
---

# jlink and jpackage

## jlink

`jlink` creates a **custom Java runtime** containing only the modules your app needs. Smaller than a full JDK.

```bash
jlink --module-path $JAVA_HOME/jmods:./target/modules       --add-modules com.example.internmanagement       --output target/custom-runtime       --strip-debug --no-man-pages --no-header-files --compress=2
```

The output is a directory with a `bin/java` executable. You can run your app with `target/custom-runtime/bin/java -m com.example.internmanagement`.

## jpackage

`jpackage` packages your app into a **native installer** (.deb, .rpm, .msi, .dmg, .pkg).

```bash
jpackage --type msi          --input target          --name InternManagement          --main-jar intern-management-1.0.0.jar          --main-class com.example.internmanagement.InternManagementApp          --runtime-image target/custom-runtime          --icon icon.ico          --win-shortcut --win-menu
```

Output: `InternManagement-1.0.0.msi` — double-click to install.

## Why this matters

- **No JDK required** — the user doesn't need Java installed.
- **Native installer** — .msi (Windows), .dmg (macOS), .deb (Linux).
- **Smaller than a full JDK** — jlink strips unused modules.
- **Start menu shortcut** — professional deployment.

## Project Connection

The project uses `javafx-maven-plugin` to run via `mvn javafx:run`. For distribution, use jlink + jpackage:

```bash
mvn clean package
jlink --module-path target/modules:$JAVA_HOME/jmods       --add-modules com.example.internmanagement       --output target/custom-runtime       --strip-debug --no-man-pages --no-header-files
jpackage --type msi --input target --name InternManagement          --main-jar intern-management-1.0.0.jar          --runtime-image target/custom-runtime
```

## Further reading

- JEP 282 (jlink).
- JEP 343 (jpackage).
