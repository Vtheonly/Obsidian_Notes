The difference between these two functions lies in how they handle the parameter `x` and what the pointer is pointing to in each case. Let's break it down:

### Case 1: `change_to_six(int* x)`

```c
void change_to_six(int* x) {
    int* addesr = x;  // The pointer `addesr` now holds the same address as `x`.
    *addesr = 6;      // Dereferences `addesr` to change the value at the address to 6.
}
```

#### Why it works:
- **Parameter is a pointer:** In this version, `x` is a pointer to an `int`. It points to a valid memory location (passed from the calling function).
- **Pointer manipulation:** By dereferencing `addesr` (which is a copy of `x`), the function directly modifies the value stored at the memory address that `x` points to. The change is reflected outside the function because `x` points to a variable in the calling code, allowing the function to directly modify that variable.

### Case 2: `change_to_six(int x)`

```c
void change_to_six(int x) {
    int* addesr = &x;  // `addesr` points to the local copy of `x` inside this function.
    *addesr = 6;       // This modifies the local copy of `x` within the function, but not outside.
}
```

#### Why it doesn't work:
- **Parameter is not a pointer:** In this version, `x` is an `int`, not a pointer. When you pass an `int` to this function, you pass a copy of the value (not the actual variable). So, any changes to `x` will only affect the copy inside the function, not the original variable in the calling code.
- **Pointer points to a local copy:** Inside the function, `addesr` points to the local variable `x`, which is a copy of the original value. When you dereference `addesr`, it changes the value of the local copy of `x`, but this change does not affect the original variable outside the function.

### Summary:

- In the first case (`int* x`), you pass a pointer to a variable, allowing the function to modify the original variable by dereferencing the pointer.
- In the second case (`int x`), you pass a copy of the variable. The function can modify the local copy, but these changes are not reflected outside the function, making the modification meaningless from the caller's perspective.
- there is no way to get the address of the original `x` (i.e., the variable passed to the function) without explicitly passing a reference (a pointer) to it.
