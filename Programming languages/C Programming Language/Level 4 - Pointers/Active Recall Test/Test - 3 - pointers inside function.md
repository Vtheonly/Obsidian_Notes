## Quiz: Pointers vs. Value in C

### 1. What is the primary difference between the two functions `change_to_six(int* x)` and `change_to_six(int x)`?
- [ ] A. They both modify the original value.
- [ ] B. One passes a pointer, the other passes a value.
- [ ] C. Both functions modify the same variable.
- [ ] D. Neither function modifies any variable.

### 2. In the first case, why is `*addesr = 6;` able to change the original value?
- [ ] A. Because `addesr` points to a local copy of `x`.
- [ ] B. Because `addesr` holds the address of a global variable.
- [ ] C. Because `addesr` holds the same address as the pointer passed to the function.
- [ ] D. Because `x` is a global pointer.

### 3. What does the variable `addesr` represent in `change_to_six(int* x)`?
- [ ] A. A new pointer that stores the address of `x`.
- [ ] B. A local integer.
- [ ] C. The original variable `x`.
- [ ] D. A global pointer.

### 4. Why does `change_to_six(int x)` fail to change the original variable's value?
- [ ] A. Because `x` is not a pointer.
- [ ] B. Because the variable `addesr` is incorrectly declared.
- [ ] C. Because `addesr` points to the wrong memory location.
- [ ] D. Because the function is recursive.

### 5. In the second case, `addesr = &x;` points to what?
- [ ] A. The memory address of the original variable.
- [ ] B. A local copy of `x`.
- [ ] C. The global copy of `x`.
- [ ] D. A dynamically allocated memory space.

### 6. How does `int* x` in the first function affect the calling function's variable?
- [ ] A. The variable in the calling function is directly modified.
- [ ] B. The function creates a local copy and modifies it.
- [ ] C. The function allocates new memory for `x`.
- [ ] D. The pointer is destroyed after the function call.

### 7. What is a major limitation of `change_to_six(int x)`?
- [ ] A. It cannot modify any variable inside the function.
- [ ] B. It passes a copy of the value, so changes aren't reflected in the calling code.
- [ ] C. It can modify only pointer types.
- [ ] D. It causes a memory leak.

### 8. Which part of the code allows `change_to_six(int* x)` to affect the original variable?
- [ ] A. The dereferencing of `addesr`.
- [ ] B. The declaration of `x`.
- [ ] C. The initialization of `addesr`.
- [ ] D. The return statement of the function.

### 9. What does the statement `int* addesr = &x;` do in the second case?
- [ ] A. It stores the address of the original `x` variable.
- [ ] B. It stores the address of the local copy of `x`.
- [ ] C. It allocates memory dynamically.
- [ ] D. It stores a reference to a global variable.

### 10. Which of the following would make `change_to_six(int x)` able to modify the original variable?
- [ ] A. Passing a pointer to `x`.
- [ ] B. Returning `x` by reference.
- [ ] C. Using a global variable.
- [ ] D. Declaring `x` as `const`.

### 11. What type of memory management issue could arise from not using pointers properly?
- [ ] A. Memory leaks.
- [ ] B. Buffer overflows.
- [ ] C. Dangling pointers.
- [ ] D. None, if the variables are passed by value.

### 12. Why is it necessary to pass the address of a variable to a function when you want to modify it?
- [ ] A. To ensure memory efficiency.
- [ ] B. To avoid creating local copies that do not affect the original.
- [ ] C. To reduce the function's execution time.
- [ ] D. To avoid stack overflows.

---

## Answers:

1. B
2. C
3. A
4. A
5. B
6. A
7. B
8. A
9. B
10. A
11. C
12. B
