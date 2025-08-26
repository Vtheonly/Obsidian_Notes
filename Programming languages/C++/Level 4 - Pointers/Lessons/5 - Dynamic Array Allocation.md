---
title: "Dynamic Arrays in C++"
---

In C++, you often need arrays whose size is not known at compile-time. This is where dynamic arrays are essential. While C uses `malloc` and `free`, C++ provides more powerful and safer tools.

### The C-Style Approach (`new[]` and `delete[]`)

The C++ equivalent of `malloc` for arrays is the `new[]` operator. It allocates a contiguous block of memory on the heap. The memory must be deallocated with the `delete[]` operator.

```cpp
#include <iostream>

int main() {
    int length;
    std::cout << "Enter a length: ";
    std::cin >> length;

    // Allocate a dynamic array on the heap
    int* a = new int[length];

    // Populate the array
    for (int i = 0; i < length; i++) {
        a[i] = i;
    }

    // Print the array
    for (int i = 0; i < length; i++) {
        std::cout << "a[" << i << "] = " << a[i] << std::endl;
    }

    // Deallocate the memory
    delete[] a;

    return 0;
}
```

**Problems with this approach:**

-   **Memory Leaks**: It's very easy to forget to call `delete[] a`, leading to a memory leak.
-   **No Size Information**: The raw pointer `a` does not know its own size. You must track the length separately.
-   **Exception Unsafe**: If an exception occurs between `new[]` and `delete[]`, the memory will not be freed.

### The Modern C++ Solution: `std::vector`

For dynamic arrays, the idiomatic and recommended solution in modern C++ is `std::vector`. It is a container from the Standard Library that encapsulates a dynamic array, handling all memory management automatically.

```cpp
#include <iostream>
#include <vector>

int main() {
    int length;
    std::cout << "Enter a length: ";
    std::cin >> length;

    // Create a std::vector of the desired size
    std::vector<int> a(length);

    // Populate the vector
    for (int i = 0; i < length; i++) {
        a[i] = i;
    }

    // Print the vector using a range-based for loop (cleaner and safer)
    int index = 0;
    for (int value : a) {
        std::cout << "a[" << index++ << "] = " << value << std::endl;
    }

    // No need to call delete! Memory is automatically managed by the vector.
    return 0;
}
```

### Why `std::vector` is Better

1.  **Automatic Memory Management (RAII)**: The `std::vector` destructor automatically frees the memory it controls when the vector goes out of scope. No more memory leaks.
2.  **Size Management**: It keeps track of its own size. You can always get the number of elements with the `.size()` member function.
3.  **Rich Functionality**: It provides a wealth of useful member functions, such as `push_back()` to add elements, `pop_back()` to remove them, `resize()`, `clear()`, etc.
4.  **Safety**: The `.at()` member function provides bounds-checked access, which throws an exception if you try to access an invalid index, making debugging easier.
5.  **Compatibility**: It works seamlessly with standard algorithms (`std::sort`, `std::find`, etc.).

### Summary

| Feature                 | C-Style Dynamic Array (`new[]`/`delete[]`) | `std::vector`                               |
|-------------------------|--------------------------------------------|---------------------------------------------|
| **Memory Management**   | Manual (error-prone)                       | Automatic (RAII, safe)                      |
| **Size Tracking**       | Manual                                     | Automatic (`.size()`)                       |
| **Functionality**       | Basic array access                         | Rich (add, remove, resize, etc.)            |
| **Safety**              | Unsafe (no bounds checking)                | Safe (bounds checking with `.at()`)         |
| **Recommended Use**     | Avoid in modern C++. Use only for legacy API interaction. | **The default choice for dynamic arrays.** |

For any new C++ code, you should **always prefer `std::vector` over raw dynamic arrays**. It is the cornerstone of modern, safe, and efficient C++ programming.