---
title: "Const Pointers and Pointers to Const in C++"
---

In C++, the `const` keyword is used to prevent modification of a value. When used with pointers, it can apply to either the data being pointed to, the pointer itself, or both. Understanding the difference is crucial for writing safe and correct code.

This is often read from right to left to understand the declaration.

### 1. Pointer to a Constant (`const T* ptr`)

This is a pointer that points to a value that cannot be changed *through this pointer*.

-   **Syntax**: `const T* ptr` or `T const* ptr` (they are equivalent).
-   **Behavior**:
    -   The **data** is constant.
    -   The **pointer** is variable.

```cpp
#include <iostream>

int main() {
    int a = 10;
    int b = 20;
    const int* ptr = &a; // Pointer to a constant integer

    // *ptr = 15; // ERROR: Cannot modify the data ptr points to.

    ptr = &b; // OK: The pointer itself can be changed to point elsewhere.
    std::cout << *ptr << std::endl; // Outputs 20

    return 0;
}
```

**Use Case**: Use this when you want to pass a pointer to a function to read data without allowing the function to modify it.

### 2. Constant Pointer (`T* const ptr`)

This is a pointer that cannot be changed to point to a different memory address after it has been initialized.

-   **Syntax**: `T* const ptr`
-   **Behavior**:
    -   The **data** is variable.
    -   The **pointer** is constant.

```cpp
#include <iostream>

int main() {
    int a = 10;
    int b = 20;
    int* const ptr = &a; // Constant pointer to an integer

    *ptr = 15; // OK: The data it points to can be modified.
    std::cout << a << std::endl; // Outputs 15

    // ptr = &b; // ERROR: Cannot change the pointer itself.

    return 0;
}
```

**Use Case**: Use this when you have a pointer that must always point to the same object, like a hardware address or a member variable pointer in a class that shouldn't be changed.

### 3. Constant Pointer to a Constant (`const T* const ptr`)

This is a pointer where both the pointer itself and the data it points to are constant.

-   **Syntax**: `const T* const ptr`
-   **Behavior**:
    -   The **data** is constant.
    -   The **pointer** is constant.

```cpp
#include <iostream>

int main() {
    int a = 10;
    int b = 20;
    const int* const ptr = &a; // Constant pointer to a constant integer

    // *ptr = 15; // ERROR: Cannot modify the data.
    // ptr = &b;  // ERROR: Cannot change the pointer.

    std::cout << *ptr << std::endl; // Outputs 10

    return 0;
}
```

**Use Case**: Use this when you need a pointer to a constant piece of data that will never change its location.

### Summary Table

| Declaration                      | Can Change Pointer Address? | Can Change Pointed-to Value? |
|----------------------------------|-----------------------------|------------------------------|
| `T* ptr`                         | Yes                         | Yes                          |
| `const T* ptr`                   | Yes                         | No                           |
| `T* const ptr`                   | No                          | Yes                          |
| `const T* const ptr`             | No                          | No                           |

### Conclusion

The placement of `const` in a pointer declaration precisely controls what can and cannot be modified. Reading the declaration from right to left can help clarify its meaning:

-   `const int* ptr`: "ptr is a pointer to an integer that is constant."
-   `int* const ptr`: "ptr is a constant pointer to an integer."

Mastering this distinction is a key step in writing robust and `const`-correct C++ code.
