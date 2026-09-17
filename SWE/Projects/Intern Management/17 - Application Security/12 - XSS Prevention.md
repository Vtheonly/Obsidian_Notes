---
tags: [concept, security, xss]
type: concept
status: complete
related:
  - [[17 - Application Security/05 - Input Validation]]
---

# XSS Prevention

## What it is

**XSS** (Cross-Site Scripting) is injecting malicious JavaScript into a web page viewed by other users.

## Types

- **Stored XSS** — malicious script stored in the DB, displayed to other users.
- **Reflected XSS** — script in the URL, reflected back by the server.
- **DOM XSS** — script injected via DOM manipulation (no server round-trip).

## Prevention

- **Output encoding** — escape `<`, `>`, `&`, `"`, `'` when rendering user content.
- **Content Security Policy (CSP)** — restrict script sources.
- **Don't render user HTML** — use textContent, not innerHTML.
- **Sanitize HTML** — if you must allow HTML (rich text editor), sanitize with a library.

## The project's XSS risk

The project's Report tab uses `HTMLEditor` to input HTML, then `HTMLWorker.parse(new StringReader(htmlContent))` to render it to PDF. If the HTML contains malicious content (e.g., a script tag — though HTMLWorker ignores those, or an `<img>` with a malicious URL), it could:
- Cause the PDF generation to fail (DoS).
- Include malicious content in the PDF.

For a desktop app, XSS is less severe (no other users to attack). But if the report is shared, the content matters.

## Further reading

- OWASP XSS Prevention Cheat Sheet.
