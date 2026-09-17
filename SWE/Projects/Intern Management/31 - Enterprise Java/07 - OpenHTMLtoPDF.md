---
tags: [concept, enterprise, pdf, openhtmltopdf]
type: concept
status: complete
related:
  - [[31 - Enterprise Java/02 - Apache POI]]
---

# OpenHTMLtoPDF

## What it is

**OpenHTMLtoPDF** is a modern Java library for rendering HTML/CSS to PDF. Replaces the deprecated iText/OpenPDF `HTMLWorker`.

## Why

- **Modern CSS** — supports CSS 2.1 + partial CSS 3 (flexbox, gradients).
- **Actively maintained** — unlike `HTMLWorker` (deprecated 2010).
- **Pure Java** — no native dependencies.
- **Open source** (Apache 2.0).

## Maven

```xml
<dependency>
    <groupId>com.openhtmltopdf</groupId>
    <artifactId>openhtmltopdf-core</artifactId>
    <version>1.0.10</version>
</dependency>
<dependency>
    <groupId>com.openhtmltopdf</groupId>
    <artifactId>openhtmltopdf-pdfbox</artifactId>
    <version>1.0.10</version>
</dependency>
```

## Usage

```java
PdfRendererBuilder builder = new PdfRendererBuilder();
builder.useFastMode();
builder.withHtmlContent("<html><body><h1>Hello</h1></body></html>", null);
builder.toStream(outputStream);
builder.run();
```

## With a template

```java
String html = "<html><body><h1>Intern Report</h1><table>"
    + "<tr><th>Name</th><th>Email</th><th>Status</th></tr>"
    + interns.stream()
        .map(i -> "<tr><td>" + i.getName() + "</td><td>" + i.getEmail()
                + "</td><td>" + i.getStatus() + "</td></tr>")
        .collect(Collectors.joining())
    + "</table></body></html>";

PdfRendererBuilder builder = new PdfRendererBuilder();
builder.withHtmlContent(html, null);
builder.toStream(out);
builder.run();
```

## Why over OpenPDF's HTMLWorker

- `HTMLWorker` was deprecated in 2010, removed in iText 7.
- `HTMLWorker` doesn't support modern CSS (no flexbox, no gradients, limited layout).
- `HTMLWorker` produces misaligned output on anything but simple HTML.

## Project Connection

The project uses `HTMLWorker`:
```java
HTMLWorker.parse(new StringReader(PDF_INPUT.getHtmlText()));
```

The fix:
```java
PdfRendererBuilder builder = new PdfRendererBuilder();
builder.useFastMode();
builder.withHtmlContent(PDF_INPUT.getHtmlText(), null);

FileChooser fc = new FileChooser();
fc.getExtensionFilters().add(new FileChooser.ExtensionFilter("PDF", "*.pdf"));
File file = fc.showSaveDialog(stage);
if (file != null) {
    try (OutputStream out = new FileOutputStream(file)) {
        builder.toStream(out);
        builder.run();
    }
}
```

## Further reading

- OpenHTMLtoPDF GitHub.
