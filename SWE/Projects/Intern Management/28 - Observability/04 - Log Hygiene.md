---
tags: [concept, observability, logging, security]
type: concept
status: complete
related:
  - [[17 - Application Security/07 - PII Protection]]
---

# Log Hygiene

## What NOT to log

- **Passwords** — never, not even hashes.
- **PII** — phone, email, SSN (or mask them).
- **Credit card numbers** — never (PCI DSS).
- **API keys / tokens** — never.
- **Full request bodies** — may contain secrets.
- **Stack traces in production** — log at DEBUG; ERROR should have a message.
- **High-frequency events** — floods the log; sample instead.

## Masking

```java
public class LogSanitizer {
    public static String maskEmail(String email) {
        int at = email.indexOf('@');
        if (at < 1) return "***";
        return email.charAt(0) + "***" + email.substring(at);
    }
    // alice@example.com → a***@example.com

    public static String maskPhone(String phone) {
        if (phone.length() < 4) return "***";
        return "***" + phone.substring(phone.length() - 4);
    }
    // +213770123456 → ***3456
}

log.info("User {} logged in", maskEmail(user.getEmail()));
```

## Log levels

| Level | When |
|---|---|
| ERROR | Something failed; user impacted. |
| WARN | Something unusual; not a failure. |
| INFO | Significant events (login, payment, job started). |
| DEBUG | Diagnostic detail (for developers). |
| TRACE | Very detailed (per-row, per-iteration). |

In production: INFO or WARN. In dev: DEBUG. TRACE is rarely used.

## Don't log and rethrow

```java
// Bad — logs twice (here and at the caller)
catch (SQLException e) {
    log.error("Failed", e);
    throw e;
}

// Good — log once (at the boundary)
catch (SQLException e) {
    throw new DataAccessException("Failed", e);
}
// Caller catches DataAccessException and logs at the boundary.
```

## Project Connection

The project logs via `System.out.println` and `e.printStackTrace()`. No levels, no structure, no hygiene. The fix: SLF4J + Logback, parameterized logging, mask PII, set levels appropriately.

## Further reading

- OWASP Logging Cheat Sheet.
