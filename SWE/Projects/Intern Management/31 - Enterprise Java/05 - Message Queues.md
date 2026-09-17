---
tags: [concept, enterprise, messaging, kafka, rabbitmq]
type: concept
status: complete
related:
  - [[12 - Advanced Database Features/07 - Oracle Advanced Queuing (AQ)]]
---

# Message Queues

## What it is

A **message queue** decouples producers from consumers. Producers send messages; consumers process them asynchronously.

## Why

- **Async** — don't make the user wait for email/PDF generation.
- **Decoupling** — producer doesn't know about consumers.
- **Reliability** — messages survive consumer crashes.
- **Scaling** — multiple consumers process in parallel.

## Common queues

### Apache Kafka
- **Distributed log** — messages are append-only, persisted.
- **High throughput** — millions of messages/sec.
- **Replay** — consumers can re-read from any point.
- Use case: event streaming, log aggregation, microservices communication.

### RabbitMQ
- **Traditional broker** — queues, exchanges, routing.
- **Lower throughput** than Kafka, but more flexible routing.
- Use case: task queues, pub/sub, RPC.

### Redis Streams
- **Simple** — built into Redis.
- Use case: small apps, low throughput.

### Oracle AQ
- **In-database** — messages are transactional with DB writes.
- Use case: when messages and DB updates must be atomic.

## Pattern: async email

```java
// Producer (in the service)
public void acceptIntern(long internId, long chiefId) {
    internRepository.updateStatus(internId, "Accepted");
    messageQueue.publish(new InternAcceptedEvent(internId, chiefId));
}

// Consumer (background worker)
@RabbitListener(queues = "intern-events")
public void onInternAccepted(InternAcceptedEvent event) {
    emailService.sendAcceptanceEmail(event.internId());
    auditService.log("ACCEPT", event.internId(), event.chiefId());
}
```

The user sees "Accepted" immediately; the email is sent in the background.

## Project Connection

For a desktop app, an in-process `ExecutorService` is sufficient for async work. If the app evolves to a server with multiple workers, Kafka or RabbitMQ for cross-service messaging.

## Further reading

- *Designing Data-Intensive Applications* (Kleppmann), Chapter 11.
