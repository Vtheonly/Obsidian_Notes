In Java, immutable types are types whose instances cannot be modified after they are created. This immutability is achieved by not providing methods that allow modification of the internal state, and by ensuring that operations that seem to modify the object actually return a new instance. A key example of an immutable type in Java is the `String` class.

### Object References and Immutability

Understanding how object references and immutability work in Java is crucial, especially with types like `String`.

1. **Object References:**
   - When an object is assigned to a variable in Java, you're actually assigning a reference to the object, not the object itself. This reference points to the memory address where the object is stored.
   - Example:
     ```java
     String str1 = "Hello";
     String str2 = str1;
     ```
     Here, both `str1` and `str2` refer to the same `String` object in memory.

2. **Immutability of `String`:**
   - A `String` object, once created, cannot be altered. If you perform an operation like concatenation, a new `String` object is created rather than modifying the original.
   - Example:
     ```java
     String str1 = "Hello";
     String str2 = str1.concat(" World");
     ```
     - `str1` continues to refer to the original "Hello" string.
     - `str2` now refers to a new `String` object containing "Hello World".

3. **Memory Address and Reference Changes:**
   - Operations like `concat()` do not modify the original `String`. Instead, they generate a new `String` object at a different memory address. Thus, `str1` remains pointing to the original "Hello" string, while `str2` points to the new "Hello World" string.

### Security Implications of Immutability

Immutability provides significant security benefits:
- **Unmodifiable State:** Once a `String` is created, its content cannot be altered. This ensures that any method receiving a `String` cannot change its original value.
- **No Side Effects:** Immutability helps prevent unintended side effects and enhances security by keeping the state of the object consistent and predictable.

### Example Code

```java
public class Main {
    public static void main(String[] args) {
        String path = "C:/Users/John/Documents";
        String query = "SELECT * FROM users";

        modifyStrings(path, query);

        // Original strings are unchanged
        System.out.println("Path: " + path); // Output: C:/Users/John/Documents
        System.out.println("Query: " + query); // Output: SELECT * FROM users
    }

    private static void modifyStrings(String path, String query) {
        path = path + "/newFolder";
        query = query + " WHERE age > 30";
    }
}
```

- **Explanation:** 
  - `path` and `query` are passed to the `modifyStrings` method, but the original strings remain unchanged because the operations inside the method create new `String` objects instead of modifying the originals.

### Summary

In Java, immutable types like `String` guarantee that once an object is created, its state cannot be altered. Operations that seem to modify the object actually result in new instances, ensuring that original objects remain unchanged. This behavior enhances security and reliability in programs by preventing unintended data alterations.

---

### 1. String

```java
String str = "Hello, World!";
str = str.pconcat(" Welcome"); // This creates a new string, original string remains unchanged
```

In the code snippet you've provided:

```java
String str = "Hello, World!";
str = str.concat(" Welcome");
```

Here's what happens step by step:

### Step 1: Initial Assignment

```java
String str = "Hello, World!";
```

- A `String` object containing `"Hello, World!"` is created in memory.
- The variable `str` is a reference to this `String` object.

### Step 2: Concatenation

```java
str = str.concat(" Welcome");
```

- The `concat()` method is called on the `str` object.
- Since `String` is immutable, `concat()` doesn't modify the original `"Hello, World!"` object. Instead, it creates a new `String` object in memory that contains the concatenated result: `"Hello, World! Welcome"`.
- The reference `str` is then updated to point to this new `String` object.

### Step 3: Reference Update

- After the concatenation, `str` no longer points to the original `"Hello, World!"` string. Instead, it points to the new `"Hello, World! Welcome"` string.
- The original `"Hello, World!"` string still exists in memory (unless it's no longer referenced by any variable, in which case it becomes eligible for garbage collection).

### Visualization

- **Before `concat`:**
  - `str` → `"Hello, World!"`

- **After `concat`:**
  - `str` → `"Hello, World! Welcome"`

The key point is that `String` objects are immutable, so any operation that modifies a `String` (like `concat`) actually results in the creation of a new `String` object. The reference (`str`) is then updated to point to this new object.

### Summary

In this example, `str` initially points to a `String` object with the value `"Hello, World!"`. After calling `concat(" Welcome")`, a new `String` object with the value `"Hello, World! Welcome"` is created, and `str` now points to this new object. The original `String` remains unchanged.
