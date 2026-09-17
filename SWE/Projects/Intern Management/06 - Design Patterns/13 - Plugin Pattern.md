---
tags: [pattern, enterprise, plugin, spi]
type: concept
status: complete
related:
  - [[31 - Enterprise Java/04 - Java SPI (ServiceLoader)]]
---

# Plugin Pattern

## What it is

A **plugin** is a piece of code that extends an application at runtime, without recompiling the application. The application defines an extension point (interface); plugins implement it.

## Java SPI (Service Provider Interface)

Java's built-in plugin mechanism:
1. Define an interface: `public interface DocumentExporter { ... }`.
2. Implement it in one or more JARs: `PdfExporter implements DocumentExporter`.
3. Register the implementation in `META-INF/services/com.example.DocumentExporter`.
4. The application uses `ServiceLoader.load(DocumentExporter.class)` to discover all implementations.

## Example

```java
// Interface
public interface DocumentExporter {
    String getFormatType();
    void export(List<Map<String, Object>> data, OutputStream out);
}

// PDF implementation (in com.example.export.pdf)
public class PdfExporter implements DocumentExporter { ... }
// META-INF/services/com.example.DocumentExporter contains: com.example.export.pdf.PdfExporter

// CSV implementation (in com.example.export.csv)
public class CsvExporter implements DocumentExporter { ... }
// META-INF/services/com.example.DocumentExporter contains: com.example.export.csv.CsvExporter

// Application discovers all
ServiceLoader<DocumentExporter> loader = ServiceLoader.load(DocumentExporter.class);
for (DocumentExporter exporter : loader) {
    System.out.println("Available: " + exporter.getFormatType());
}
```

## Why it exists

- **Extensibility** — add new export formats without touching the core app.
- **Modularity** — each plugin is a separate JAR/module.
- **Decoupling** — the core app doesn't know which plugins exist.

## Project Connection

The project's PDF export is hardcoded to OpenPDF's `HTMLWorker`. The fix: `DocumentExporter` interface with PDF, CSV, XLSX implementations, discovered via SPI. Adding a new format (e.g., HTML) is just adding a new JAR.

See [[31 - Enterprise Java/04 - Java SPI (ServiceLoader)]] for the full implementation.

## Common pitfalls

- **SPI for everything** — overkill for a 3-format app. Use SPI when you want third-party extensibility.
- **No way to choose** — `ServiceLoader.load()` returns all implementations. You need a way to select (by format type, by user choice).

## Further reading

- Java `ServiceLoader` documentation.
- *Java 9 Modularity* (Mak & Sendoa).
