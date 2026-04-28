### 1. The Goal

A calculator that parses a string equation (e.g., "4 + 5 \* 3") and calculates the result using **Interfaces**.

### 2. The Interface Strategy

Instead of a giant `if-else` block inside the main method, the project uses an Interface `Operate`.

```java
public interface Operate {
    Double getResult(Double... numbers);
}
```

**Concrete Implementations:**

- `class Add implements Operate` -> implements addition logic.
- `class Multiply implements Operate` -> implements multiplication logic.

### 3. Queue Data Structure

The project uses a `Queue` (specifically `LinkedList`) to process the equation.

- **Poll():** Retrieves and removes the head of the queue.
- The logic splits numbers and operators into two separate queues. It polls a number, polls an operator, initializes the correct class (`Add` or `Multiply`), and computes the result sequentially.

**Key Takeaway:** By using the `Operate` interface, the main calculator logic doesn't care _how_ addition works. It just calls `.getResult()`. This makes it easy to add a "Power" or "Modulus" feature later without breaking the main loop.
