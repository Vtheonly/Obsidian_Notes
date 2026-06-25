---
title: "Comments in C++"
---

Comments are used to add explanatory notes to your code. They are completely ignored by the compiler and have no effect on the program's behavior. Their purpose is to make the code more understandable for humans.

C++ supports two main types of comments:

### 1. Single-Line Comments (`//`)

Single-line comments start with `//` and extend to the end of the line. They are useful for short, concise notes.

```cpp
// This is a single-line comment.
int x = 10; // This comment explains what this line does.

// You can stack them for multi-line explanations.
// This is the first line.
// This is the second line.
```

### 2. Multi-line Comments (`/* */`)

Multi-line comments start with `/*` and end with `*/`. They can span multiple lines and are often used for longer explanations or for temporarily disabling a block of code.

```cpp
/*
  This is a multi-line comment.
  It can span several lines and is useful for
  providing detailed explanations of a function or class.
*/
int y = 20;

/* You can also use it on a single line. */

void myFunction() {
    /*
    int temp = 5; // This code is temporarily disabled.
    y += temp;
    */
}
```

#### Pitfall: Nested Multi-line Comments

One important thing to note is that C++ does not support nested multi-line comments. The first `*/` sequence encountered will end the entire comment block, which can lead to compilation errors.

```cpp
/*
  Outer comment.
  /* Nested comment. */ // This is a problem!
  The outer comment ends here, and the rest is a compile error.
*/ 
```

### Best Practices for Commenting

-   **Write comments for the "why," not the "what."** Good code should be self-explanatory about *what* it does. Comments should explain *why* it does it in a particular way, especially if the logic is complex or non-obvious.
-   **Keep comments up-to-date.** Outdated comments that no longer match the code are worse than no comments at all.
-   **Use comments to generate documentation.** Tools like Doxygen can parse specially formatted comments to automatically generate documentation for your project.

```cpp
/**
 * @brief Calculates the factorial of a number.
 * @param n The non-negative integer to calculate the factorial of.
 * @return The factorial of n.
 */
int factorial(int n) {
    // The factorial of 0 is 1 by definition.
    if (n == 0) {
        return 1;
    }
    return n * factorial(n - 1);
}
```