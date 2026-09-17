---
tags: [concept, observability, logging, slf4j, logback]
type: concept
status: complete
---

# SLF4J and Logback

## What it is

- **SLF4J** (Simple Logging Facade for Java) — logging API (interface).
- **Logback** — logging implementation (SLF4J's native implementation).

## Why SLF4J

- **Facade** — your code depends on SLF4J, not the implementation. Swap implementations (Logback, Log4j 2, java.util.logging) without code changes.
- **Widely adopted** — most Java libraries use SLF4J.

## Usage

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class InternService {
    private static final Logger log = LoggerFactory.getLogger(InternService.class);

    public Intern create(CreateInternCommand cmd) {
        log.info("Creating intern: name={}, email={}", cmd.name(), cmd.email());
        try {
            Intern intern = repository.save(...);
            log.debug("Created intern with id={}", intern.getId());
            return intern;
        } catch (DuplicateEmailException e) {
            log.warn("Duplicate email: {}", cmd.email());
            throw e;
        } catch (Exception e) {
            log.error("Failed to create intern: name={}", cmd.name(), e);
            throw e;
        }
    }
}
```

## Parameterized logging

```java
log.info("User {} logged in from {}", username, ip);  // good
log.info("User " + username + " logged in from " + ip);  // bad — string concatenation always
```

Parameterized logging only concatenates if the level is enabled. Faster.

## Logback configuration (`logback.xml`)

```xml
<configuration>
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>logs/app.log</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
            <fileNamePattern>logs/app-%d{yyyy-MM-dd}.%i.log.gz</fileNamePattern>
            <maxFileSize>10MB</maxFileSize>
            <maxHistory>30</maxHistory>
            <totalSizeCap>2GB</totalSizeCap>
        </rollingPolicy>
        <encoder class="net.logstash.logback.encoder.LogstashEncoder"/>
    </appender>

    <root level="INFO">
        <appender-ref ref="CONSOLE"/>
        <appender-ref ref="FILE"/>
    </root>

    <logger name="com.example" level="DEBUG"/>
</configuration>
```

## JSON logging (for ELK/Loki)

Use `logstash-logback-encoder`:
```xml
<encoder class="net.logstash.logback.encoder.LogstashEncoder"/>
```

Output:
```json
{"@timestamp":"2026-07-13T14:30:00.123Z","level":"INFO","logger":"com.example.InternService","message":"Creating intern","name":"Alice","email":"alice@example.com"}
```

## MDC (Mapped Diagnostic Context)

Add context to every log line:
```java
MDC.put("userId", currentUser.getId());
MDC.put("requestId", UUID.randomUUID().toString());
try {
    // ... logging includes userId and requestId automatically
} finally {
    MDC.clear();
}
```

## Project Connection

The project uses `System.out.println` and `e.printStackTrace()`. The fix: SLF4J + Logback with structured JSON logging, MDC for correlation IDs, rolling file appender.

## Further reading

- SLF4J FAQ.
- Logback documentation.
