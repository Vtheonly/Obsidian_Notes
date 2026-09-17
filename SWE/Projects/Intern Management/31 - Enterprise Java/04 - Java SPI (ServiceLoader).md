---
tags: [concept, enterprise, spi, serviceloader]
type: concept
status: complete
related:
  - [[06 - Design Patterns/13 - Plugin Pattern]]
  - [[04 - OOD and SOLID/15 - Open-Closed Principle (OCP)]]
---

# Java SPI (ServiceLoader)

## What it is

**Java SPI** (Service Provider Interface) is Java's built-in plugin mechanism. Define an interface; implementations are discovered at runtime via `META-INF/services/`.

## Why

- **Extensibility** — add new implementations without modifying the core.
- **Decoupling** — the core doesn't know about implementations.
- **Modularity** — each implementation is a separate JAR.

## Example: DocumentExporter

### 1. Define the interface
```java
package com.example.export;

public interface DocumentExporter {
    String getFormatType();        // "PDF", "CSV", "XLSX"
    String getFileExtension();     // ".pdf", ".csv", ".xlsx"
    void export(Map<String, String> metadata, List<String> headers,
                List<Map<String, Object>> data, OutputStream out) throws Exception;
}
```

### 2. Implement (in a separate JAR or module)
```java
package com.example.export.pdf;

public class PdfExporter implements DocumentExporter {
    public String getFormatType() { return "PDF"; }
    public String getFileExtension() { return ".pdf"; }
    public void export(...) {
        // OpenHTMLtoPDF rendering
    }
}
```

### 3. Register
File: `META-INF/services/com.example.export.DocumentExporter`
Content:
```
com.example.export.pdf.PdfExporter
```

### 4. Discover
```java
ServiceLoader<DocumentExporter> loader = ServiceLoader.load(DocumentExporter.class);
Map<String, DocumentExporter> exporters = new HashMap<>();
for (DocumentExporter exporter : loader) {
    exporters.put(exporter.getFormatType().toUpperCase(), exporter);
}

// Use
DocumentExporter pdfExporter = exporters.get("PDF");
pdfExporter.export(metadata, headers, data, outputStream);
```

## Why this is powerful

- Adding a new format (CSV, XLSX) = write a new class + register it. No modification of existing code (OCP).
- The core app doesn't know which formats are available — it discovers them at runtime.
- Each exporter is a separate module — can be added/removed without recompiling the core.

## JDBC uses SPI

JDBC drivers auto-register via SPI:
```
META-INF/services/java.sql.Driver
```
containing `oracle.jdbc.OracleDriver`. That's why `Class.forName` is no longer needed.

## Project Connection

The project's PDF generation is hardcoded to OpenPDF's `HTMLWorker`. The fix: `DocumentExporter` SPI with PDF, CSV, XLSX implementations. Adding a format is a new JAR, no code changes.

## Further reading

- Java `ServiceLoader` documentation.
