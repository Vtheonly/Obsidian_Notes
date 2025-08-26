---
title: "Dynamic Memory Allocation in C++"
---

### Introduction

Dynamic memory allocation is the process of allocating memory from the **heap** (also called the free store) at runtime. This is essential when the amount of memory you need is not known at compile-time, or when you need an object to exist beyond the scope in which it was created.

In C, this was done with `malloc()`, `calloc()`, and `free()`. C++ provides a more powerful and type-safe mechanism: the `new` and `delete` operators.

### The `new` and `delete` Operators

-   **`new`**: Allocates memory for an object or an array of objects on the heap and returns a typed pointer to that memory.
-   **`delete`**: Deallocates memory that was previously allocated with `new`.
-   **`new[]` and `delete[]`**: Used specifically for allocating and deallocating arrays.

**Key Advantage over `malloc`**: `new` not only allocates memory but also **constructs** the object, meaning its constructor is called. Similarly, `delete` **destructs** the object by calling its destructor before deallocating the memory. This is crucial for proper resource management in C++ (RAII).

### Example: Allocating a Single Object

```cpp
#include <iostream>

int main() {
    // Allocate an integer on the heap
    int* ptr = new int;
    *ptr = 42;

    std::cout << "Value: " << *ptr << std::endl;

    // Deallocate the memory
    delete ptr;
    ptr = nullptr; // Good practice to null out dangling pointers

    return 0;
}
```

### The Problem with Manual Memory Management

Manually managing memory with `new` and `delete` is notoriously error-prone:

1.  **Memory Leaks**: Forgetting to call `delete` for every `new` causes the program to lose memory over time.
2.  **Dangling Pointers**: Accessing a pointer after the memory it points to has been `delete`d leads to undefined behavior.
3.  **Double Free**: Calling `delete` twice on the same pointer leads to undefined behavior.
4.  **Exception Safety**: If an exception is thrown between a `new` and a `delete`, the `delete` might be skipped, causing a memory leak.

### The Modern C++ Solution: Smart Pointers

To solve these problems, modern C++ (C++11 and later) introduced **smart pointers**. Smart pointers are objects that act like pointers but automatically manage the lifetime of the memory they own. They follow the **RAII (Resource Acquisition Is Initialization)** principle.

When a smart pointer goes out of scope, its destructor is automatically called, which in turn `delete`s the managed memory.

#### 1. `std::unique_ptr`

-   Represents **exclusive ownership**. Only one `unique_ptr` can point to a given object at a time.
-   It is very lightweight (zero-cost abstraction).
-   It cannot be copied, but it can be **moved** to transfer ownership.

```cpp
#include <iostream>
#include <memory> // Required for smart pointers

int main() {
    // Use std::make_unique to create the object and the smart pointer
    std::unique_ptr<int> ptr = std::make_unique<int>(101);

    std::cout << "Value: " << *ptr << std::endl;

    // No 'delete' needed! The memory is automatically freed when 'ptr' goes out of scope.
    return 0;
}
```

#### 2. `std::shared_ptr`

-   Represents **shared ownership**. Multiple `shared_ptr`s can point to the same object.
-   It keeps a reference count of how many `shared_ptr`s are pointing to the object.
-   The memory is deallocated only when the last `shared_ptr` owning it is destroyed.

```cpp
#include <iostream>
#include <memory>

int main() {
    // Use std::make_shared for efficiency
    std::shared_ptr<int> ptr1 = std::make_shared<int>(202);
    {
        std::shared_ptr<int> ptr2 = ptr1; // Both pointers now share ownership
        std::cout << "Reference count: " << ptr1.use_count() << std::endl; // Output: 2
    } // ptr2 goes out of scope, reference count becomes 1

    std::cout << "Reference count: " << ptr1.use_count() << std::endl; // Output: 1

    return 0;
} // ptr1 goes out of scope, count becomes 0, memory is freed.
```

### Conclusion

While `new` and `delete` are the fundamental tools for dynamic memory in C++, direct manual use is discouraged in modern code.

-   **Avoid `new` and `delete` directly.**
-   **Prefer smart pointers (`std::unique_ptr` and `std::shared_ptr`)** to automate memory management.
-   Use `std::make_unique` and `std::make_shared` to create smart pointers safely and efficiently.

This approach makes your code safer, cleaner, and free of memory leaks.