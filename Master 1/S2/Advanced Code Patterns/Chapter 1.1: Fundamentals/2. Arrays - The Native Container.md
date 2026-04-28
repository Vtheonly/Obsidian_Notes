
## Arrays (The Low-Level Foundation)

Arrays are **not** part of the Collections Framework. They are a feature built directly into the Java language syntax.

### Declaration and instantiation
```java
// 1. Declaration
int[] numbers; 

// 2. Instantiation (Size is mandatory!)
numbers = new int[5]; 

// 3. Inline initialization
String[] names = {"Alice", "Bob", "Charlie"};
```

### Characteristics

1.  **Fixed Size**: Once you type `new int[5]`, that array will hold 5 integers forever. You cannot resize it. To "add" a 6th item, you must manually create a new, larger array and copy all data over.
2.  **Contiguous Memory**: Arrays typically occupy a single, unbroken block of memory. This makes them extremely cache-friendly for the CPU.
3.  **Primitives**: This is the *only* container that can store raw primitives (`int`, `double`, `boolean`) without overhead.

### Why `.length` and not `.size()`?

A common point of confusion is how to get the size of an array.

*   **Arrays** use a **field** (variable): `arr.length`.
*   **Collections** use a **method**: `list.size()`.

```java
int[] arr = new int[10];
System.out.println(arr.length); // Prints 10 (capacity), not how many slots you filled.
// System.out.println(arr.add(5)); // COMPILE ERROR: Arrays have no methods!
```

> [!WARNING]
> **The Null Pitfall**
> When you create an object array like `String[] arr = new String[5];`, Java fills it with `null` by default. If you try to access `arr[0].toUpperCase()` before putting a string in there, you will get a `NullPointerException`.

### When to use Arrays?
Use arrays only when:
1.  You know the exact number of elements in advance.
2.  You need maximum performance for primitive number crunching (e.g., image processing, matrices).
3.  You are implementing a low-level data structure (like building your own ArrayList).
