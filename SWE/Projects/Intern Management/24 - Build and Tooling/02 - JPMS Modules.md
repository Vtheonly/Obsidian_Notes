---
tags: [concept, java, jpms, modules]
type: concept
status: complete
related:
  - [[03 - Java Foundations/04 - Java 21 LTS Features]]
---

# JPMS (Java Platform Module System)

## What it is

JPMS (Java 9+) organizes code into **modules** with explicit dependencies and exports.

## module-info.java

```java
module com.example.internmanagement {
    requires javafx.controls;
    requires javafx.fxml;
    requires java.sql;
    requires com.zaxxer.hikari;
    requires org.slf4j;

    opens com.example.internmanagement.ui to javafx.fxml;
    exports com.example.internmanagement;
}
```

- `requires` — depends on another module.
- `exports` — makes a package available to other modules.
- `opens` — allows reflection (needed by FXMLLoader).
- `requires transitive` — depends on + re-exports.
- `uses` / `provides` — for ServiceLoader (SPI).

## The project's bug

```java
module com.example.intern_mnagement_app {  // typo: "mnagement"
    // ...
    opens com.example.intern_manegement_app to javafx.fxml;  // different typo: "manegement"
    exports com.example.intern_manegement_app;
}
```

Module name ≠ package name. The `opens` and `exports` reference the package, which exists — but the module name is different. This can cause `LayerInstantiationException` on stricter JDKs.

## The fix

```java
module com.example.internmanagement {
    requires javafx.controls;
    requires javafx.fxml;
    requires java.sql;
    requires com.zaxxer.hikari;
    requires org.slf4j;
    requires org.mindrot.jbcrypt;

    opens com.example.internmanagement.ui to javafx.fxml;
    exports com.example.internmanagement;
}
```

No typos. Module name matches package. Remove unused `requires` (`java.mail`, `org.apache.pdfbox`, `java.desktop`).

## When to use JPMS

- **Library** — modules make your API explicit.
- **Large app** — modules enforce boundaries.
- **Custom runtime (jlink)** — modules are required.

For small apps, the classpath still works. But JavaFX apps benefit from JPMS for jlink/jpackage.

## Further reading

- *Java 9 Modularity* (Mak & Sendoa).
- JLS §7 (Modules).
