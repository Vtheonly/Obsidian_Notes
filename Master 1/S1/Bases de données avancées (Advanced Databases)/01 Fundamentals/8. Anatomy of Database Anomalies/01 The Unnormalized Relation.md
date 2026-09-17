# 01 The Unnormalized Relation

Consider the flat relation:

`R(product, client, address, date, quantity, amount)`

Example rows may contain the same client and address repeatedly because every order is stored in the same relation.

## Main problem: redundancy

If Dupuis appears on several orders, `Dupuis` and `Lille` are repeated on several rows.

This repetition is not just a storage issue. It means one real-world fact is represented in several places, so modifications must keep all copies consistent.

## Functional view

The relation mixes different themes:

- client facts;
- product facts;
- order facts.

When independent facts are stored together, redundancy and anomalies become likely.

## Normalization connection

The purpose of decomposition is not simply to create more tables. It is to separate facts according to their dependencies so that each fact has an appropriate place.
