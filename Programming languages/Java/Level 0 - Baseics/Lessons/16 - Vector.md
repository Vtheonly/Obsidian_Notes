
### Vector Class

1. **Definition:**
   - `Vector` is a part of the `java.util` package. It implements the `List` interface and extends the `AbstractList` class. Similar to `ArrayList`, it is a dynamic array that can grow or shrink in size.

2. **Thread Safety:**
   - A key difference between `Vector` and other `List` implementations like `ArrayList` is that `Vector` is thread-safe. All methods in `Vector` are synchronized, making it suitable for use in multi-threaded environments.

### Main Methods

1. **Constructor:**
   - `Vector<String> vector = new Vector<>();` // Default constructor
   - `Vector<String> vectorWithCapacity = new Vector<>(10);` // With initial capacity

2. **Adding Elements:**
   - `addElement(E obj)`: Adds an element to the end of the vector.
   - `add(int index, E element)`: Inserts an element at the specified position.

   ```java
   vector.addElement("Apple");
   vector.add("Banana");
   vector.add(1, "Orange");
   ```

3. **Accessing Elements:**
   - `elementAt(int index)`: Returns the element at the specified position.
   - `get(int index)`: Returns the element at the specified position.

   ```java
   String fruit = vector.elementAt(1);
   ```

4. **Removing Elements:**
   - `remove(int index)`: Removes the element at the specified position.
   - `removeElement(Object obj)`: Removes the first occurrence of the specified element.

   ```java
   vector.remove(0);
   vector.removeElement("Banana");
   ```

5. **Size and Capacity:**
   - `size()`: Returns the number of elements in the vector.
   - `capacity()`: Returns the current capacity of the vector.

   ```java
   int size = vector.size();
   int capacity = vector.capacity();
   ```

6. **Enumeration:**
   - `elements()`: Returns an enumeration of the elements in the vector.

   ```java
   Enumeration<String> enumeration = vector.elements();
   while (enumeration.hasMoreElements()) {
       String element = enumeration.nextElement();
       // Process each element
   }
   ```

### Example

```java
import java.util.Vector;
import java.util.Enumeration;

public class VectorExample {
    public static void main(String[] args) {
        Vector<String> vector = new Vector<>();
        
        // Adding elements
        vector.addElement("Apple");
        vector.addElement("Banana");
        vector.addElement("Orange");

        // Accessing elements
        String fruit = vector.elementAt(1);
        System.out.println("Element at index 1: " + fruit);

        // Removing elements
        vector.removeElement("Banana");

        // Size and Capacity
        int size = vector.size();
        int capacity = vector.capacity();
        System.out.println("Size: " + size);
        System.out.println("Capacity: " + capacity);

        // Enumeration
        Enumeration<String> enumeration = vector.elements();
        while (enumeration.hasMoreElements()) {
            String element = enumeration.nextElement();
            System.out.println("Element: " + element);
        }
    }
}
```

### Comparison: `ArrayList` vs. `Vector`

1. **Thread Safety:**
   - **`ArrayList`**: Not synchronized. Requires external synchronization if used in multi-threaded environments.
   - **`Vector`**: Synchronized, making it thread-safe.

2. **Performance:**
   - **`ArrayList`**: Generally faster due to the absence of synchronization overhead.
   - **`Vector`**: Slightly slower due to synchronization.

3. **Growth of Capacity:**
   - **`ArrayList`**: Increases its capacity by 50% of the current size.
   - **`Vector`**: Doubles its capacity when needed.

4. **Initial Capacity:**
   - **`ArrayList`**: No specific default capacity.
   - **`Vector`**: Default initial capacity of 10, customizable during instantiation.

5. **Legacy Status:**
   - **`ArrayList`**: Introduced in Java 2 (JDK 1.2), considered modern.
   - **`Vector`**: Present since the early versions of Java, considered legacy.

6. **Usage Recommendations:**
   - **`ArrayList`**: Preferred for better performance when thread safety is not a concern.
   - **`Vector`**: Useful in legacy codebases or when thread safety is required without external synchronization.

### Example: `ArrayList` vs. `Vector`

```java
import java.util.ArrayList;
import java.util.Vector;

public class ListComparison {
    public static void main(String[] args) {
        // ArrayList (not synchronized)
        ArrayList<String> arrayList = new ArrayList<>();

        // Vector (synchronized)
        Vector<String> vector = new Vector<>();

        // Add elements to both
        arrayList.add("Item1");
        vector.add("Item1");

        // Thread-safe iteration (Vector)
        for (String item : vector) {
            // Process each item
        }

        // ArrayList does not need synchronization in this case
        for (String item : arrayList) {
            // Process each item
        }
    }
}
```

In summary, while `Vector` provides thread safety, `ArrayList` is typically preferred for its performance unless synchronization is necessary. Modern code often favors `ArrayList` or other concurrent collections over `Vector`.