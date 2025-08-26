---
title: "Strings and String Literals in C++"
---

In C++, text can be represented by low-level C-style string literals or, more commonly, by the high-level `std::string` class.

### 1. C-Style String Literals

A C-style string literal is a sequence of characters enclosed in double quotes (e.g., `"hello"`). Its type is `const char[]`, and it is terminated by a null character (`\0`).

-   **Immutability**: They are stored in read-only memory. Modifying a string literal results in undefined behavior.
-   **Usage**: Primarily used for initializing `std::string` objects or for passing to legacy C-style functions.

```cpp
const char* c_style_string = "This is a read-only string.";
```

### 2. The Modern C++ Way: `std::string`

For nearly all programming tasks, **you should use `std::string`** from the `<string>` header. It is a powerful class that manages its own memory and provides a safe and convenient interface.

**Key Advantages over C-style strings:**
-   **Automatic Memory Management**: No need for `malloc`/`free` or `new[]`/`delete[]`. `std::string` handles it all.
-   **Safety**: Operations are bounds-checked, preventing buffer overflows.
-   **Rich Functionality**: Provides a wealth of member functions for searching (`.find()`), modifying (`.append()`, `+=`), and comparing (`==`, `!=`, `<`).
-   **Size Awareness**: Always knows its own length (`.size()` or `.length()`).

```cpp
#include <iostream>
#include <string>

int main() {
    // Initialization
    std::string greeting = "Hello, C++!";

    // Modification
    greeting += " It's a pleasure to meet you.";

    // Access and Size
    std::cout << greeting << std::endl;
    std::cout << "Length: " << greeting.length() << std::endl;

    return 0;
}
```

### Special String Literals in C++

Modern C++ enhances string literals with useful features:

-   **`s` Suffix (C++14)**: Creates a `std::string` object directly.
    ```cpp
    using namespace std::string_literals;
    auto my_string = "This is a std::string"s; // Type is std::string
    ```

-   **Raw String Literals (C++11)**: `R"(...) "`. Ignores escape characters, which is perfect for file paths or regular expressions.
    ```cpp
    std::string path = R"(C:\Users\YourUser\Documents)";
    ```

### Summary

| Feature | C-Style String (`const char*`) | `std::string` |
| :--- | :--- | :--- |
| **Memory** | Manual, error-prone | Automatic, safe (RAII) |
| **Safety** | Unsafe (buffer overflows) | Safe |
| **Functionality** | Minimal (requires `<cstring>`) | Rich and extensive |
| **Recommendation**| Avoid. Use only for C API compatibility. | **Always prefer `std::string`.** |

For a detailed guide on transitioning from C-style strings, see [[4 - From C-Style Strings to std::string]].
