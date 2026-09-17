---
tags: [concept, database, oracle-aq, messaging]
type: concept
status: complete
related:
  - [[31 - Enterprise Java/05 - Message Queues]]
---

# Oracle Advanced Queuing (AQ)

## What it is

**Oracle AQ** is a message queue built into the database. Producers enqueue messages; consumers dequeue and process them. The queue is transactional — messages are committed/rolled back with the transaction.

## Why it exists

- **Async processing** — don't make the user wait for an email to send; enqueue a "send email" message.
- **Decoupling** — producer and consumer don't need to know each other.
- **Reliability** — messages survive crashes; the queue is in the DB.

## Basic usage

```sql
-- Create a queue table
BEGIN
    DBMS_AQADM.CREATE_QUEUE_TABLE(
        queue_table        => 'qt_intern_events',
        queue_payload_type => 'SYS.AQ$_JMS_TEXT_MESSAGE'
    );
    DBMS_AQADM.CREATE_QUEUE(queue_name => 'q_intern_events', queue_table => 'qt_intern_events');
    DBMS_AQADM.START_QUEUE(queue_name => 'q_intern_events');
END;
/

-- Enqueue
DECLARE
    msg SYS.AQ$_JMS_TEXT_MESSAGE;
    enq_opts DBMS_AQ.ENQUEUE_OPTIONS_T;
    msg_props DBMS_AQ.MESSAGE_PROPERTIES_T;
    msg_id RAW(16);
BEGIN
    msg := SYS.AQ$_JMS_TEXT_MESSAGE.construct;
    msg.set_text('{"event":"intern_accepted","id":123}');
    DBMS_AQ.ENQUEUE(
        queue_name         => 'q_intern_events',
        enqueue_options    => enq_opts,
        message_properties => msg_props,
        payload            => msg,
        msgid              => msg_id
    );
    COMMIT;
END;
/

-- Dequeue (consumer)
DECLARE
    msg SYS.AQ$_JMS_TEXT_MESSAGE;
    deq_opts DBMS_AQ.DEQUEUE_OPTIONS_T;
    msg_props DBMS_AQ.MESSAGE_PROPERTIES_T;
    msg_id RAW(16);
BEGIN
    DBMS_AQ.DEQUEUE(
        queue_name         => 'q_intern_events',
        dequeue_options    => deq_opts,
        message_properties => msg_props,
        payload            => msg,
        msgid              => msg_id
    );
    DBMS_OUTPUT.PUT_LINE(msg.get_text());
    COMMIT;
END;
/
```

## Alternatives

- **Apache Kafka** — distributed, high-throughput log. For microservices.
- **RabbitMQ** — traditional message broker.
- **Redis Streams** — simple, fast.
- **JMS** (Java Message Service) — Java standard, can use various brokers.

## Project Connection

The project doesn't use AQ. For a desktop app, AQ is probably overkill — a simple `ExecutorService` for async email sending is sufficient. AQ would be useful if the app evolves to a server with multiple workers.

## Further reading

- Oracle Database Advanced Queuing User's Guide.
