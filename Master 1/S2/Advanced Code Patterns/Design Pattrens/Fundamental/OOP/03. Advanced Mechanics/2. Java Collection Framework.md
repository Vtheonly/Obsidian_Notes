Arrays in Java (`User[] users = new User[10]`) are **fixed-size**. Once created, they cannot grow. This is inefficient for real-world applications where data is dynamic. The **Collection Framework** solves this.

### 1. ArrayList (The Resizable Array)

- **Concept:** A wrapper around a standard array that automatically handles resizing.
- **How it works:**
  1.  Starts with a default capacity (e.g., 10 slots).
  2.  When you add the 11th item, the ArrayList internally creates a _new_, larger array (usually 50% larger).
  3.  It copies all old items to the new array.
  4.  It dumps the old array.
- **Generics `<Type>`:** Java collections are generic. You must specify what goes inside using angle brackets. `ArrayList<Item>` ensures you don't accidentally put a `Horse` into an `Inventory` of `Items`.

```java
// From File 1: Inventory System
private ArrayList<Item> items = new ArrayList<>(); // Only accepts Item or subclasses (Weapon, Fruit)
```

### 2. LinkedList (The Chain)

- **Concept:** Data is not stored contiguously in memory. Each element (Node) holds data and a pointer (address) to the next node.
- **Usage in Project 3 (Calculator):**
  - The calculator parses "4 + 5". It needs to process these in order.
  - It uses a `LinkedList` acting as a **Queue**.

#### **Queue Mechanics: `poll()`**

The Calculator project uses the method `.poll()`.

- **FIFO:** Queues are First-In-First-Out.
- **`.poll()`:** Retrieves the element at the "head" (front) of the line and **removes** it from the list.
- **Why use this?** It allows the calculator to "consume" the numbers and operators one by one until the list is empty.

### 3. HashMap (The Key-Value Store)

- **Concept:** Stores data in pairs. You look up a value using a unique Key, rather than an index number (0, 1, 2).
- **Usage in Project 2 (ATM):**
  - **Goal:** Fast login validation.
  - **Structure:** `HashMap<Integer, Integer>` mapping `Customer Number` -> `PIN`.
- **Efficiency:** Searching an Array for a user ID takes linear time (checking every box). A HashMap allows near-instant access (`O(1)` complexity) because it hashes the key to find the direct memory address.

```java
// From ATM Project
HashMap<Integer, Integer> data = new HashMap<>();
data.put(12345, 9999); // Key: ID, Value: PIN

// Instant lookup logic
if (data.containsKey(inputID) && data.get(inputID) == inputPin) {
    // Login Success
}
```
