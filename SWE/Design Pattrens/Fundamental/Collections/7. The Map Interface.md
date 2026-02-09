
## The Map Interface (`java.util.Map`)

**Map is NOT a Collection.** It does not extend the `Collection` interface. It is a distinct data structure mapping **Keys** to **Values**.

*   **Key**: Must be unique.
*   **Value**: Can be duplicated.

### 1. HashMap
*   **Order**: No guarantee.
*   **Performance**: **$O(1)$** for `get(key)` and `put(key, value)`.
*   **Nulls**: Allows one null key and multiple null values.
*   **How it works**: Uses the `.hashCode()` of the Key to calculate where to store the data in memory.

### 2. LinkedHashMap
*   **Order**: Maintains **Insertion Order** of keys.
*   Useful if you are building a cache (LRU Cache) or need to iterate in order.

### 3. TreeMap
*   **Order**: Keys are **Sorted** (Natural order or Comparator).
*   **Performance**: **$O(\log n)$**.
*   **Sub-maps**: Allows cool operations like `headMap(key)` (give me everything strictly less than this key).

### Iterating a Map
Since Map is not `Iterable`, you cannot loop over it directly. You must convert it to a Collection view:
1.  `map.keySet()`: Returns a Set of keys.
2.  `map.values()`: Returns a Collection of values.
3.  `map.entrySet()`: Returns a Set of Key-Value pairs.

```java
Map<String, Integer> scores = new HashMap<>();
scores.put("Alice", 90);

// Correct way to loop
for (Map.Entry<String, Integer> entry : scores.entrySet()) {
    System.out.println(entry.getKey() + ": " + entry.getValue());
}
```

---
