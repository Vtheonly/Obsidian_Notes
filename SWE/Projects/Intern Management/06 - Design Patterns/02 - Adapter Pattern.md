---
tags: [pattern, structural, adapter]
type: concept
status: complete
related:
  - [[05 - Software Architecture/07 - Facade Pattern]]
  - [[05 - Software Architecture/06 - Exception Translation]]
---

# Adapter Pattern

> "Convert the interface of a class into another interface clients expect. Adapter lets classes work together that couldn't otherwise because of incompatible interfaces." — GoF

## What it is

An **adapter** wraps an existing class and presents a different interface. Like a power adapter — same electricity, different plug shape.

```java
// Old interface (javax.mail)
public interface MailSender {
    void send(String to, String subject, String body);
}

// New library (jakarta.mail)
public class JakartaMailClient {
    public void sendEmail(MimeMessage message) { ... }
}

// Adapter
public class JakartaMailSenderAdapter implements MailSender {
    private final JakartaMailClient client;
    public JakartaMailSenderAdapter(JakartaMailClient client) { this.client = client; }

    @Override
    public void send(String to, String subject, String body) {
        MimeMessage message = buildMessage(to, subject, body);
        client.sendEmail(message);
    }
}
```

The caller uses `MailSender` (the old interface). The adapter wraps `JakartaMailClient` (the new library) and translates the call.

## Why it exists

- **Migration** — switch libraries without touching every call site.
- **Integration** — adapt a third-party API to your interface.
- **Testing** — adapt a mock to your interface.

## Adapter vs Facade vs Decorator

- **Adapter** — changes the interface (one-to-one).
- **Facade** — simplifies the interface (one-to-many).
- **Decorator** — adds behavior without changing the interface (one-to-one).

## Project Connection

The project uses OpenPDF's `HTMLWorker` (deprecated). To migrate to OpenHTMLtoPDF:
```java
// Old interface
public interface ReportGenerator {
    void generate(String html, OutputStream out);
}

// OpenHTMLtoPDF adapter
public class OpenHtmlToPdfReportGenerator implements ReportGenerator {
    public void generate(String html, OutputStream out) {
        PdfRendererBuilder builder = new PdfRendererBuilder();
        builder.useFastMode();
        builder.withHtmlContent(html, null);
        builder.toStream(out);
        builder.run();
    }
}
```

The controller calls `ReportGenerator.generate()` — doesn't know which library is underneath.

## Common pitfalls

- **Adapter that does too much** — if the adapter adds logic, it's becoming a service. Keep adapters thin.
- **Adapting an interface to itself** — useless. Only adapt when interfaces differ.

## Further reading

- *Design Patterns* (GoF), Adapter.
