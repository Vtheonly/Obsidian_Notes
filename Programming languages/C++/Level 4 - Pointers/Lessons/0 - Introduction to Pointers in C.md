---
title: "Introduction to Pointers and References in C++"
---

### What Are Pointers?

A **pointer** is a variable that stores the memory address of another object. Instead of holding data directly, it "points" to the location where the data is stored. Pointers are a powerful, low-level feature inherited from C.

-   **Memory**: When a program runs, its data is stored in memory (RAM). Every location in memory has a unique address.
-   **Variables and Addresses**: When you declare a variable like `int x;`, the system allocates memory for it at a specific address.

### What Are References?

A **reference** is an alias—another name—for an existing variable. Once a reference is initialized to a variable, it cannot be changed to refer to another variable. References are a C++ feature that provide a safer alternative to pointers for many use cases.

### Declaring and Using Pointers

To declare a pointer, you use the `*` symbol. To get the address of a variable, you use the address-of operator `&`.

```cpp
int b = 42;
int* a = &b; // 'a' is a pointer that holds the memory address of 'b'
```

To access the value a pointer points to, you **dereference** it with the `*` operator.

```cpp
std::cout << *a; // Prints the value of b (42)
*a = 50;         // Changes the value of b to 50
```

### Declaring and Using References

To declare a reference, you use the `&` symbol. A reference must be initialized when it is declared.

```cpp
int b = 42;
int& ref_b = b; // 'ref_b' is now another name for 'b'
```

You use the reference directly, as if it were the original variable.

```cpp
std::cout << ref_b; // Prints the value of b (42)
ref_b = 50;        // Changes the value of b to 50
```

### Why Use Pointers and References?

1.  **Passing Arguments to Functions**: They allow functions to modify the original variables passed to them.
    -   **Pass-by-pointer**: `void swap(int* a, int* b);`
    -   **Pass-by-reference**: `void swap(int& a, int& b);` (Generally safer and easier to read).

2.  **Dynamic Memory Management**: Pointers are essential for allocating memory on the heap at runtime using `new` and `delete`. This is for objects whose lifetime is not tied to a specific scope.

3.  **Polymorphism**: Pointers (and references) to a base class are used to achieve polymorphism, allowing you to call derived class methods through a base class interface.

### Example: Pointers vs. References

```cpp
#include <iostream>

int main() {
    int b = 42;

    // --- Using a Pointer ---
    int* a = &b;
    std::cout << "Value of b: " << b << std::endl;
    std::cout << "Address of b: " << &b << std::endl;
    std::cout << "Address stored in a: " << a << std::endl;
    std::cout << "Value pointed to by a: " << *a << std::endl;
    *a = 50; // Modify b through the pointer
    std::cout << "New value of b: " << b << std::endl; // Prints 50

    std::cout << "--------------------" << std::endl;

    // --- Using a Reference ---
    int& ref_b = b;
    b = 100; // Reset b
    std::cout << "Value of b: " << b << std::endl;
    std::cout << "Value via reference: " << ref_b << std::endl;
    ref_b = 110; // Modify b through the reference
    std::cout << "New value of b: " << b << std::endl; // Prints 110

    return 0;
}
```

### Modern C++: Smart Pointers

Manual memory management with raw pointers (`new`/`delete`) is error-prone. Modern C++ strongly advocates for using **smart pointers** (`std::unique_ptr`, `std::shared_ptr`) to manage dynamic memory automatically, preventing memory leaks.

### Summary

| Feature         | Pointer (`*`)                               | Reference (`&`)                             |
|-----------------|---------------------------------------------|---------------------------------------------|
| **What it is**  | A variable that stores a memory address.    | An alias for an existing variable.          |
| **Can be Null** | Yes (`nullptr`).                            | No, must be initialized to a valid object.  |
| **Reassignment**| Can be reassigned to point to another object. | Cannot be reseated to refer to another object.|
| **Syntax**      | Requires `*` to dereference.                | Used directly like the original variable.   |
| **Use Case**    | Dynamic memory, optional objects, polymorphism. | Function parameters, return values, aliases.|

In modern C++, prefer references when you can, and use smart pointers for managing ownership of dynamic resources. Use raw pointers only in specific, low-level situations.