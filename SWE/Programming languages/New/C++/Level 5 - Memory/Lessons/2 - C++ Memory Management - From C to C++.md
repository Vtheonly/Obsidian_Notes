---
title: "From C to C++: Modern Memory Management"
---

Migrating from C to C++ involves a significant shift in memory management philosophy. While C++ supports C's `malloc()` and `free()`, the C++ way is safer, more robust, and better integrated with the language's features like constructors and destructors.

This guide explicitly contrasts the old and new ways.

### Level 1: The C Way (`malloc` and `free`)

In C, dynamic memory is managed manually using functions from `<cstdlib>`.

```c
#include <stdlib.h>

int* arr = (int*)malloc(10 * sizeof(int)); // 1. Allocate
if (arr == NULL) { /* handle failure */ }

// ... use arr ...

free(arr); // 2. Deallocate
```

**Drawbacks:**
-   **Not Type-Safe**: `malloc` returns `void*`, requiring an explicit cast that can hide type errors.
-   **Constructors/Destructors Not Called**: `malloc` and `free` know nothing about C++ objects. They just allocate and free raw memory. This is a critical failure in C++, as objects are not properly initialized or cleaned up.
-   **Error-Prone**: Forgetting `free` causes a memory leak. Using memory after `free` is undefined behavior.

**Verdict**: **Do not use `malloc` and `free` in C++.** They are only for interfacing with C libraries that require them.

--- 

### Level 2: The Old C++ Way (`new` and `delete`)

C++ introduced the `new` and `delete` operators to solve the type-safety and constructor/destructor issues.

```cpp
#include <string>

std::string* str = new std::string("hello"); // 1. Allocate and construct

// ... use str ...

delete str; // 2. Destruct and deallocate
```

**Improvements over `malloc`:**
-   **Type-Safe**: `new` returns a properly typed pointer. No cast is needed.
-   **Object Lifecycle**: `new` calls the constructor after allocating memory. `delete` calls the destructor before freeing memory.

**Remaining Problems:**
-   **Manual and Error-Prone**: You are still responsible for calling `delete`. All the risks of memory leaks, dangling pointers, and double-frees still exist.
-   **Not Exception-Safe**: If an exception is thrown between `new` and `delete`, `delete` is never called, and the memory leaks.

**Verdict**: An improvement, but **avoid manual `new` and `delete` in modern C++**.

--- 

### Level 3: The Modern C++ Way (RAII and Smart Pointers)

Modern C++ automates memory management using the **RAII (Resource Acquisition Is Initialization)** principle, embodied in **smart pointers** from the `<memory>` header.

The core idea: resource ownership is tied to an object's lifetime. When the object (the smart pointer) goes out of scope, its destructor automatically releases the resource.

#### `std::unique_ptr`: Exclusive Ownership

Use this when you need a single, unique owner of a piece of heap-allocated memory. It's lightweight and has no performance overhead compared to a raw pointer.

```cpp
#include <memory>
#include <string>

void modern_way() {
    // Use std::make_unique to create the object and pointer safely
    auto str_ptr = std::make_unique<std::string>("hello");

    // ... use str_ptr like a normal pointer ...
    if (str_ptr->empty()) { /* ... */ }

} // As soon as str_ptr goes out of scope, the string is automatically deleted.
  // No memory leak possible.
```

#### `std::shared_ptr`: Shared Ownership

Use this when multiple parts of your code need to share ownership of an object, and the object should only be destroyed when the *last* owner is gone.

```cpp
#include <memory>
#include <vector>

void shared_ownership() {
    auto shared_data = std::make_shared<std::vector<int>>(1000);

    auto ptr1 = shared_data;
    auto ptr2 = shared_data;

    std::cout << "Owners: " << shared_data.use_count(); // Prints "Owners: 3"

} // ptr1 and ptr2 go out of scope. shared_data is the last owner.
  // When shared_data goes out of scope, the vector is deleted.
```

### The Golden Rule of Modern C++ Memory Management

-   **Don't use `new` and `delete` manually.**
-   For dynamic arrays, **use `std::vector`**. It handles its own memory.
-   For single dynamic objects, use **`std::unique_ptr`** by default.
-   If you need shared ownership, use **`std::shared_ptr`**.

This approach makes your code dramatically safer, cleaner, and easier to reason about.
