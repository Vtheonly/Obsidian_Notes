# 02 Update Anomalies

An update anomaly occurs when one logical fact is repeated in multiple rows and a change must update all copies.

## Example

Suppose Dupuis changes address from Lille to Paris.

If Dupuis appears on five order rows, all five rows must be changed. If one remains `Lille`, the database contains conflicting representations of the same client.

## Why it happens

The client address is a fact about the client, but the unnormalized relation stores it together with each order.

## Normalized direction

Store the client fact once:

`CLIENT(code_client, nom_client, adresse)`

Then orders reference the client by key instead of repeating the address.

## Exam phrase

**Update anomaly = one real-world fact is duplicated, so one change must be propagated to several rows.**
