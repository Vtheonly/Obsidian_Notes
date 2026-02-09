
## The Set Interface (`java.util.Set`)

A **Set** is a collection that contains **no duplicate elements**. It models the mathematical set abstraction.

**Key Properties:**
1.  **Unique**: `set.add("A"); set.add("A");` -> The second add is ignored.
2.  **Order**: Usually NOT guaranteed (depends on implementation).

### 1. HashSet (`java.util.HashSet`)
*   **Backing**: Uses a `HashMap` internally.
*   **Order**: Completely unpredictable. It looks random.
*   **Performance**: Extremely fast (**$O(1)$**) for add, remove, and contains.
*   **Use Case**: You need to remove duplicates or check for existence efficiently.

### 2. LinkedHashSet (`java.util.LinkedHashSet`)
*   **Backing**: Hash table + Linked List.
*   **Order**: Preserves **Insertion Order** (the order you added them).
*   **Performance**: Slightly slower than HashSet due to maintaining links.

### 3. TreeSet (`java.util.TreeSet`)
*   **Backing**: Red-Black Tree (Balanced Binary Search Tree).
*   **Order**: **Sorted** (Natural ordering like A-Z, 1-100, or via a custom Comparator).
*   **Performance**: **$O(\log n)$**. Slower than HashSet but keeps data sorted.

### Detailed Comparison

| Feature | HashSet | LinkedHashSet | TreeSet |
| :--- | :--- | :--- | :--- |
| **Duplicates** | No | No | No |
| **Ordering** | None (Chaos) | Insertion Order | Sorted (Natural/Comparator) |
| **Null allowed?** | Yes | Yes | No (usually throws exception) |
| **Speed** | Fastest ($O(1)$) | Fast ($O(1)$) | Medium ($O(\log n)$) |

> [!WARNING]
> **Mutable Objects in Sets**
> Be very careful putting mutable objects (like a `Person` object where fields can change) into a `HashSet`. If you change the fields of the object *after* putting it in the set, its Hash Code changes, and the Set might "lose" it (it won't find it even if it's there).
