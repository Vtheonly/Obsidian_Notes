# 04 Decomposition into Related Relations

A typical normalized direction separates independent themes.

## Client

`CLIENT(code_client, nom_client, adresse)`

Client facts are stored once.

## Product

`PRODUIT(code_produit, nom_produit, prix_unitaire)`

Product facts are independent of a particular client order.

## Order

`COMMANDE(code_commande, code_client, date, code_produit, quantity)`

The order relation references the client and product rather than repeating their descriptive facts.

## Why this helps

- client information can be inserted before an order exists;
- deleting an order does not have to delete the client;
- changing an address requires one client row to be updated;
- repeated descriptive data is reduced.

This is the practical motivation behind normalization and dependency-based decomposition.
