9. Best Practices - Coding to Interfaces.md

## The Golden Rule: Code to Interfaces

This is the hallmark of a professional Java developer. You should almost never declare a variable using the specific class implementation.

### The Wrong Way
```java
// Tightly coupled. Hard to change later.
ArrayList<String> users = new ArrayList<>(); 
```

### The Right Way
```java
// Loosely coupled. Polymorphic.
List<String> users = new ArrayList<>();
```

### Why? "Dependency Inversion"
By using the Interface (`List`) on the left side:
1.  **Flexibility**: You can change the implementation later without breaking the rest of your code.
    *   If you realize you need faster inserts, you simply change `new ArrayList<>()` to `new LinkedList<>()`. Because the rest of your code only knows it's a `List`, nothing else needs to change.
2.  **API Design**: If you write a method, accept the interface:
    *   `public void processUsers(List<String> users)`
    *   This allows the caller to pass an `ArrayList`, a `LinkedList`, or even an unmodifiable List.

### Generic Type Inference (The Diamond Operator `<>`)
Since Java 7, you do not need to repeat the type on the right side.

```java
// Verbose (Old Java 5/6)
List<String> list = new ArrayList<String>(); 

// Clean (Modern Java)
List<String> list = new ArrayList<>();
```

### Summary of Best Practices
1.  **Always** use the interface type for variable declarations (`List`, `Set`, `Map`).
2.  **Prefer** `ArrayList` over `LinkedList` generally.
3.  **Prefer** `ArrayDeque` over `Stack`.
4.  **Use Generics** strictly (no raw types like `List list = new ArrayList()`).
5.  **Understand** the difference between `==` (reference check) and `.equals()` (content check) when searching collections.