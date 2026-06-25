---
title: "Passing Pointers and References to Functions in C++"
---

The way you pass arguments to a function in C++ determines whether the function works with a copy of the data or can modify the original data. Let's compare passing by value, by pointer, and by reference.

### 1. Pass-by-Value

When you pass a variable by value, the function receives a **copy** of the variable. Any modifications made to the parameter inside the function do not affect the original variable.

```cpp
#include <iostream>

void change_to_six(int x) {
    // 'x' is a local copy of the original argument.
    x = 6; // This only changes the copy.
}

int main() {
    int my_var = 10;
    change_to_six(my_var);
    std::cout << my_var << std::endl; // Output: 10. The original is unchanged.
    return 0;
}
```

**Why it doesn't modify the original**: The function operates on a separate copy of `my_var` that exists only within the function's scope. The original `my_var` in `main` is untouched.

### 2. Pass-by-Pointer

When you pass a variable by pointer, you are passing its **memory address**. The function then receives a pointer that holds this address. By dereferencing the pointer, the function can directly access and modify the original variable.

```cpp
#include <iostream>

void change_to_six(int* x_ptr) {
    // x_ptr holds the memory address of the original variable.
    if (x_ptr) { // Good practice: check for nullptr
        *x_ptr = 6; // Dereference the pointer to modify the original value.
    }
}

int main() {
    int my_var = 10;
    change_to_six(&my_var); // Pass the address of my_var
    std::cout << my_var << std::endl; // Output: 6. The original is changed.
    return 0;
}
```

**Why it works**: The function knows the exact location of `my_var` in memory and can change the value stored at that location.

### 3. Pass-by-Reference (The C++ Way)

C++ introduced references, which provide a cleaner and safer way to achieve the same result as pointers for this use case. When you pass by reference, the function parameter becomes an **alias** for the original variable. No copy is made, and there's no need for dereferencing syntax.

```cpp
#include <iostream>

void change_to_six(int& x_ref) {
    // x_ref is an alias for the original variable.
    x_ref = 6; // This directly modifies the original variable.
}

int main() {
    int my_var = 10;
    change_to_six(my_var); // Pass the variable itself
    std::cout << my_var << std::endl; // Output: 6. The original is changed.
    return 0;
}
```

**Why it works and is preferred**: The syntax is cleaner than pointers (no `&` on the call site, no `*` inside the function). References cannot be null, which eliminates the need for null checks and makes the function's intention clearer: it expects a valid object to modify.

### Summary

| Passing Method      | What is Passed?          | Can Modify Original? | Syntax in Function | Syntax at Call Site |
|---------------------|--------------------------|----------------------|--------------------|---------------------|
| **Pass-by-Value**   | A copy of the value.     | No                   | `void func(int x)`   | `func(my_var)`      |
| **Pass-by-Pointer** | The memory address.      | Yes                  | `void func(int* p)`  | `func(&my_var)`     |
| **Pass-by-Reference**| An alias to the variable.| Yes                  | `void func(int& r)`  | `func(my_var)`      |

### Conclusion

-   Use **pass-by-value** for small objects that you don't need to modify.
-   Use **pass-by-reference** when you want to modify the original object or to avoid the cost of copying a large object. For non-modified large objects, use **pass-by-const-reference** (`const T&`).
-   Use **pass-by-pointer** when you need to represent that an argument is optional (by passing `nullptr`) or when dealing with C-style APIs.

For modifying function arguments, **pass-by-reference is the idiomatic and preferred method in modern C++**.