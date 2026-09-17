---
tags: [concept, enterprise, mail, jakarta]
type: concept
status: complete
related:
  - [[31 - Enterprise Java/08 - Quartz Scheduler]]
---

# Jakarta Mail

## What it is

**Jakarta Mail** (formerly JavaMail) is the standard Java API for sending and receiving email.

## Why Jakarta (not javax)

`javax.mail` is deprecated. The Jakarta EE migration renamed packages from `javax.*` to `jakarta.*`. Use:
```xml
<dependency>
    <groupId>jakarta.mail</groupId>
    <artifactId>jakarta.mail-api</artifactId>
    <version>2.1.3</version>
</dependency>
<dependency>
    <groupId>org.eclipse.angus</groupId>
    <artifactId>jakarta.mail</artifactId>
    <version>2.0.3</version>
</dependency>
```

## Sending email

```java
Properties props = new Properties();
props.put("mail.smtp.host", "smtp.example.com");
props.put("mail.smtp.port", "587");
props.put("mail.smtp.auth", "true");
props.put("mail.smtp.starttls.enable", "true");

Session session = Session.getInstance(props, new Authenticator() {
    protected PasswordAuthentication getPasswordAuthentication() {
        return new PasswordAuthentication("user@example.com", "password");
    }
});

Message msg = new MimeMessage(session);
msg.setFrom(new InternetAddress("noreply@example.com"));
msg.setRecipients(Message.RecipientType.TO, InternetAddress.parse("intern@example.com"));
msg.setSubject("Your internship application");
msg.setText("Dear Intern,\n\nCongratulations! Your application has been accepted.");

Transport.send(msg);
```

## HTML email

```java
MimeBodyPart textPart = new MimeBodyPart();
textPart.setText("Plain text version");

MimeBodyPart htmlPart = new MimeBodyPart();
htmlPart.setContent("<h1>Accepted!</h1><p>Your application has been accepted.</p>", "text/html");

Multipart multipart = new MimeMultipart("alternative");
multipart.addBodyPart(textPart);
multipart.addBodyPart(htmlPart);

msg.setContent(multipart);
```

## Async sending

Email sending is slow (SMTP handshake, network). Never send on the UI thread:
```java
CompletableFuture.runAsync(() -> {
    emailService.sendAcceptanceEmail(intern);
}, emailExecutor);
```

## Templates

Use a template engine (Thymeleaf, Freemarker) for complex emails:
```java
String body = thymeleaf.process("acceptance-email.html", Map.of("intern", intern));
msg.setContent(body, "text/html");
```

## Project Connection

The project declares `javax.mail` but has no email code (the Email tab's button has no handler). The fix: Jakarta Mail, async sending via `ExecutorService`, Thymeleaf templates for the email body.

## Further reading

- Jakarta Mail documentation.
