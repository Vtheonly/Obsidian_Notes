# 1. Anatomy of Database Anomalies

The slides state that an un-normalized database causes "severe errors" for the designer, but understanding *why* requires breaking down the exact mechanics of Insertion, Update, and Deletion anomalies.

## 2. The Problematic Relation
Consider the flat, un-normalized table: `R (product, client, address, date, quantity, amount)`

| product | client | address | date | quantity | amount |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Cassettes | Dupuis | Lille | 10/02 | 100 | 1000 |
| CD-ROM | Dupuis | Lille | 15/02 | 150 | 1500 |
| CD-ROM | Martin | Marseille | 01/03 | 15 | 150 |
| Disks | Dupont | Lyon | 05/03 | 300 | 600 |

### Problem 1: Redundancy
Notice that `Dupuis` and his address `Lille` are repeated on multiple lines. We are wasting storage space by repeating the same client data for every single order they place.

### Problem 2: Update Anomaly
**Scenario:** Dupuis moves his office from `Lille` to `Paris`.
*   **The Anomaly:** To update his address, the database must scan every single row and update "Lille" to "Paris" wherever the client is "Dupuis". If the system crashes halfway through, or if a query is poorly written, Dupuis will have his address listed as "Paris" on order 1, and "Lille" on order 2. The database is now mathematically inconsistent. We no longer know where Dupuis actually lives.

### Problem 3: Deletion Anomaly
**Scenario:** Martin decides to cancel his order for the CD-ROM.
*   **The Anomaly:** To cancel the order, we delete the row containing Martin's data. However, because client data and order data are tangled in the same table, deleting the order **permanently deletes Martin's existence from the database**. We lose his name and his address (Marseille). 

### Problem 4: Insertion Anomaly
**Scenario:** We sign a new client, "Dubois", who lives in "Dijon". He hasn't placed an order yet.
*   **The Anomaly:** We cannot insert Dubois into the database. Why? Because a record in this table requires an order (a product, date, quantity). Without order data, the row is incomplete (often violating primary key constraints, as `product` and `date` would likely be part of the key). We are forced to wait until he buys something to register him.

## 3. The Normalized Solution
By applying Normalization (1NF, 2NF, 3NF), we break this into three distinct themes.

1.  **R1_CLIENT (code_client, nom_client, adresse)**
    *   *Solves Insertion:* We can add Dubois here without needing an order.
    *   *Solves Deletion:* If Martin cancels an order, his client record stays here safely.
    *   *Solves Update:* Dupuis only exists here ONCE. If he moves, we change his address in exactly one place.
2.  **R2_PRODUIT (code_produit, nom_produit, prix_unitaire)**
3.  **R3_COMMANDE (code_commande, code_client, date, code_produit, quantity)**
    *   *Solves Redundancy:* This table acts as the junction. Instead of repeating "Lille" and "Dupuis", we just put his `code_client`.
