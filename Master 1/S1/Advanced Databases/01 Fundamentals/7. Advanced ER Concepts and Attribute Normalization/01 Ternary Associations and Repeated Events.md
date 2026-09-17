# 01 Ternary Associations and Repeated Events

## The repeated-event problem

Suppose a `SUBSCRIBER` borrows a `BOOK`. If the binary association is identified only by `(Subscriber_ID, ISBN)`, the same subscriber-book pair can appear only once.

That is insufficient when the same book can be borrowed again later.

## Ternary modeling

If the event is uniquely identified by the combination of subscriber, book, and borrowing date, the date participates in the identification of the event. A conceptual model can represent this explicitly with a ternary association involving `SUBSCRIBER`, `BOOK`, and the borrowing date/event.

The resulting identifier is conceptually:

`(Subscriber_ID, ISBN, Borrow_Date)`

This allows:

- the same subscriber to borrow the same book again;
- each borrowing event to remain distinguishable;
- return information to belong to the borrowing event rather than to the subscriber or book.

## Exam checklist

1. Ask whether the same pair of entities can participate in the relationship more than once.
2. Identify what distinguishes one occurrence from another.
3. Make that distinguishing information part of the event's identification when appropriate.
4. Keep event-specific attributes on the association/event structure.
