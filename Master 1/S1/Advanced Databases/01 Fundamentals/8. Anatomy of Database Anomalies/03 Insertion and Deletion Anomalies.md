# 03 Insertion and Deletion Anomalies

## Insertion anomaly

An insertion anomaly occurs when the schema makes it difficult or impossible to record one fact without inventing unrelated data.

Example: a new client Dubois lives in Dijon but has not placed an order. If the only relation is an order-oriented table, there may be no valid row in which to store the client independently.

## Deletion anomaly

A deletion anomaly occurs when removing one fact unintentionally removes another fact that should have remained.

Example: if Martin's only order is deleted and the client information exists only in that order row, deleting the order also deletes Martin's client information.

## Memory aid

- **Insertion:** cannot add a fact by itself.
- **Update:** one fact must be changed in several places.
- **Deletion:** removing one fact removes another fact accidentally.
