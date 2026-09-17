# 04 Complex Translation Example

Consider:

- `CLIENT` places `COMMANDE`;
- `COMMANDE` concerns `ARTICLE`;
- each order has a date;
- each command-article pair has a quantity.

## Step 1 — entities

`CLIENT(num_client, nom, adresse)`

`COMMANDE(num_commande, date)`

`ARTICLE(num_article, designation, prix)`

## Step 2 — order/client relationship

If every order belongs to one client, represent the relationship with:

`COMMANDE(num_commande, date, num_client*)`

## Step 3 — order/article N:M relationship

Because an order can contain several articles and an article can occur in many orders:

`DETAIL_COMMANDE(num_commande*, num_article*, quantité)`

## Result

The design separates:

- client facts;
- order facts;
- article facts;
- facts about each order-article occurrence.

This separation is the central idea behind reliable ER-to-relational translation.
