---
tags: [concept, javafx, filechooser, io]
type: concept
status: complete
---

# FileChooser

## What it is

`FileChooser` is a native file open/save dialog.

## Save dialog

```java
FileChooser fileChooser = new FileChooser();
fileChooser.setTitle("Save Report");
fileChooser.getExtensionFilters().add(
    new FileChooser.ExtensionFilter("PDF", "*.pdf")
);
fileChooser.setInitialDirectory(new File(System.getProperty("user.home"), "Documents"));

File file = fileChooser.showSaveDialog(stage);
if (file != null) {
    reportService.exportToPdf(data, file);
}
```

## Open dialog

```java
File file = fileChooser.showOpenDialog(stage);
if (file != null) {
    List<Intern> imported = importService.importFromCsv(file);
    // ...
}
```

## Directory dialog

```java
DirectoryChooser dirChooser = new DirectoryChooser();
File dir = dirChooser.showDialog(stage);
```

## Why this matters

The project writes PDFs to `document_now.pdf` in the current working directory — unpredictable, no user choice. The fix: `FileChooser.showSaveDialog()`.

## Project Connection

The project's `makePDF`:
```java
PdfWriter.getInstance(document, new FileOutputStream("document_now.pdf"));
```

The fix:
```java
FileChooser fc = new FileChooser();
fc.setTitle("Save Report");
fc.getExtensionFilters().add(new FileChooser.ExtensionFilter("PDF", "*.pdf"));
File file = fc.showSaveDialog(stage);
if (file != null) {
    reportService.exportToPdf(html, file);
}
```

## Further reading

- JavaFX `FileChooser` documentation.
