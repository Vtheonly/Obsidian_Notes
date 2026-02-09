### 1. Exception Handling (The Safety Net)

In the ATM Project (File 4), user input is unpredictable. A user might type "Hello" when the ATM asks for a numeric PIN.

- **The Crash:** Without handling, entering a String into `scanner.nextInt()` causes an `InputMismatchException`, crashing the program immediately.
- **The Solution (`try-catch`):** We wrap risky code in a "safety bubble."

```java
try {
    // Risky code
    int pin = input.nextInt();
} catch (Exception e) {
    // What to do if it explodes
    System.out.println("Invalid Characters. Only Numbers Allowed.");
    x = 2; // Logic to restart the loop
}
```

**Checked vs. Unchecked Exceptions:**

- **Checked (Compile-time):** Java forces you to handle these (e.g., `IOException` when reading a file). The code won't compile without a try-catch.
- **Unchecked (Runtime):** Errors logic (e.g., `NullPointerException`, `IndexOutOfBounds`). Java doesn't force you to catch these, but you should prevent them.

### 2. Variable Arguments (Varargs)

In Project 3 (Calculator), the `Operate` interface uses a special syntax:

```java
public interface Operate {
    Double getResult(Double... numbers);
}
```

**The `...` Syntax:**

- This is "Syntactic Sugar" for an array.
- It allows the method to accept **zero or more** arguments.
- Internally, Java treats `numbers` as `Double[] numbers`.
- **Benefit:** Flexibility. You can call `getResult(1.0, 2.0)` or `getResult(1.0, 2.0, 3.0, 4.0)` without overloading the method 10 times.
