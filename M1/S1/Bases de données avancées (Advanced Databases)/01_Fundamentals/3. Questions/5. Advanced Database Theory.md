# 5. Advanced Database Theory

This note explains concepts outside of standard SQL querying, focusing on Object-Oriented Databases and Distributed Systems.

## 1. Object-Oriented Databases (OODBMS)

### Concept: "Stored with attributes AND methods"

In a standard Relational Database (SQL), you only store **Data** (Attributes). The code (Methods) lives in your Java/Python file, separate from the data.

In an OODBMS, you store the **Object** as a whole.

- **Attributes:** The variables (Color, Size, Name).
- **Methods:** The functions (CalculateTax(), Move(), Display()).

**The Analogy:**

- **SQL:** Storing a car by taking it apart and putting the screws in one drawer and the wheels in another. To drive it, you must reassemble it (Query + Mapping).
- **OODBMS:** Parking the car in a garage. To drive it, you just open the door and go. The logic and data are stored together.

---

## 2. Hibernate (ORM)

**Problem:** Programming languages (Java/Python) use **Objects**. Databases use **Tables**. They do not fit together naturally. This is called the "Impedance Mismatch."

**Solution:** Hibernate.

- **Role:** The Translator (Bridge).
- **Function:** It is an **O**bject-**R**elational **M**apper (ORM).
- **How it works:** You write Java code (`student.save()`). Hibernate automatically writes the SQL (`INSERT INTO Students...`) for you. It hides the complexity of SQL from the programmer.

---

## 3. The CAP Theorem

This theorem applies to **Distributed Databases** (NoSQL systems like Cassandra, DynamoDB). It states you can only have **2 out of 3** guarantees.

### C: Consistency

- Every read receives the most recent write or an error.
- _Example:_ If I update my bank balance in NY, the server in Tokyo sees the new balance **instantly**.

### A: Availability

- Every request receives a (non-error) response, without the guarantee that it contains the most recent write.
- _Example:_ The system always works, but the Tokyo server might show my old balance for a few seconds.

### P: Partition Tolerance (The "Must Have")

- The system continues to operate despite an arbitrary number of messages being dropped or delayed by the network between nodes.
- _Meaning:_ If the internet cable between NY and Tokyo is cut, the system does not crash.

**Why is 'P' strictly required?**
In large networks, cables _will_ get cut. Failures happen. You cannot choose to have "No network failures." Therefore, you must choose Partition Tolerance, and then decide between **C** (Consistency) or **A** (Availability).
