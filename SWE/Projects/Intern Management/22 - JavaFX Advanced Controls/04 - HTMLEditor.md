---
tags: [concept, javafx, htmleditor, controls]
type: concept
status: complete
---

# HTMLEditor

## What it is

`HTMLEditor` is a JavaFX control for editing HTML content (rich text editor).

## Usage

```java
HTMLEditor editor = new HTMLEditor();
editor.setHtmlText("<h1>Title</h1><p>Content...</p>");

String html = editor.getHtmlText();
// Use html for PDF generation, email, etc.
```

## Limitations

- **Limited HTML support** — based on JavaFX WebView (WebKit); supports a subset of HTML/CSS.
- **No image upload** — you'd need to embed images as data URIs.
- **No custom toolbar** — the toolbar is fixed.
- **Heavyweight** — uses WebView internally.

## Security considerations

- **XSS** — if the HTML is displayed to other users (e.g., in a web view), sanitize it.
- **PDF generation** — the project uses `HTMLWorker` (deprecated) to convert HTML to PDF. Use OpenHTMLtoPDF instead.

## Project Connection

The project uses `HTMLEditor` for:
- The Report tab (`PDF_INPUT`).
- The Email tab (no handler — dead UI).

The fix: keep `HTMLEditor` for the report, replace `HTMLWorker` with OpenHTMLtoPDF.

## Further reading

- JavaFX `HTMLEditor` documentation.
