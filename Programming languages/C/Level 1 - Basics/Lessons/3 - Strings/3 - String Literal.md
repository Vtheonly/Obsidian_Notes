

### What is a String Literal?

- A **string literal** in C is a sequence of characters (`chars`) terminated by a null character (`'\0'`). 
- For example:  
  ```c
  char* str = "hello, world"; // A string literal
  ```

### Using String Literals

- String literals can be used to initialize character arrays.
  - Example:
    ```c
    char a1[] = "abc";       // `a1` is `char[4]` holding {'a','b','c','\0'}
    char a2[4] = "abc";      // Same as `a1`, explicitly specifying the size
    char a3[3] = "abc";      // `a3` is `char[3]` holding {'a','b','c'}, missing the '\0'
    ```

Nothing stops you from creating an array of characters and not ending it with a null-terminator, but **using it as a null-terminated byte string will lead to undefined behavior**. A C string is an array of characters terminated by a NUL character; if we don't have that character, we do not have a string.
### Key Properties of String Literals

1. **Immutability**:
   - **String literals are not modifiable**. They may be stored in read-only memory (`.rodata` section), so modifying them leads to undefined behavior.
   - Example:
     ```c
     char* s = "foobar";
     s[0] = 'F';
      // Undefined behavior: Attempting to modify a string literal
     // The code may compile successfully, but this does not guarantee that it will run correctly.
     ```

2. **Best Practice**:
   - It is good practice to declare string literals as `const` to avoid accidental modification.
   - Example:
     ```c
     char const* s1 = "foobar";
     s1[0] = 'F'; // Compiler error: Trying to modify a constant string literal
     ```

### String Literal Concatenation

- **Multiple string literals** can be concatenated at compile time.
  - Example (version < C99):
    ```c
    char* s = "Hello, " "World"; // Two string literals are concatenated into one.
    ```

- **Since C99**: More than two string literals can be concatenated, but it is implementation-defined.
  - Example:
    ```c
    char* s1 = "Hello" ", " "World"; // Multiple literals concatenated
    ```

### Character Sets for String Literals

- **String literals** support different character sets, including wide characters and UTF encodings:
  - **Normal string literal**:
    ```c
    char* s1 = "abc"; // Type: char[]
    ```
  - **Wide character string literal**:
    ```c
    wchar_t* s2 = L"abc"; // Type: wchar_t[]
    ```
  - **UTF-8 string literal (C11 and later)**:
    ```c
    char* s3 = u8"abc"; // Type: char[]
    ```
  - **16-bit wide string literal (C11 and later)**:
    ```c
    char16_t* s4 = u"abc"; // Type: char16_t[]
    ```
  - **32-bit wide string literal (C11 and later)**:
    ```c
    char32_t* s5 = U"abc"; // Type: char32_t[]
    ```

### Summary

- **String literals** in C are immutable sequences of characters ending with a null character.
- They can be used to initialize arrays and are best declared with `const` to prevent modification.
- String literals can be concatenated at compile time.
- C provides support for various character sets, including wide and UTF-encoded strings starting from C11.



## Difference: 
The two declarations, `char* s = "foobar"` and `char s[7] = "foobar"`, differ in both their memory allocation and usage. Let's break down the differences:

### 1. `char* s = "foobar"`

- **Type:**  
  `s` is a pointer to `char`. It points to the memory location where the string literal `"foobar"` is stored.
  
- **Memory Allocation:**  
  The string `"foobar"` is stored in a **read-only section** of memory, usually in a segment like `.rodata` (read-only data). `s` itself is stored in a different location (like the stack), and it holds the address of the first character of the string literal (`'f'`).

- **Modifiability:**  
  The string literal `"foobar"` is **not modifiable**. Attempting to modify the contents of `*s` (like `s[0] = 'F';`) leads to **undefined behavior** because it is stored in a read-only memory section.

- **Example Usage:**
  ```c
  char* s = "foobar";
  // s points to a read-only string literal in memory
  ```

### 2. `char s[7] = "foobar"`

- **Type:**  
  `s` is a character array of size 7 (`char[7]`).

- **Memory Allocation:**  
  The array `s` is allocated on the **stack** (or in the global/static memory if declared globally). It contains a **copy** of the string `"foobar"`, including the null terminator (`'\0'`), making the total size 7 characters.

- **Modifiability:**  
  The array `s` is **modifiable**. You can modify the content of `s` safely (e.g., `s[0] = 'F';`) because it's a local array on the stack, and it has its own copy of the string.

- **Example Usage:**
  ```c
  char s[7] = "foobar";
  // s is an array holding {'f', 'o', 'o', 'b', 'a', 'r', '\0'}
  s[0] = 'F'; // Valid: modifies the array
  ```

### Key Differences

| Aspect                   | `char* s = "foobar"`                       | `char s[7] = "foobar"`                    |
|--------------------------|-------------------------------------------|-------------------------------------------|
| **Type**                 | Pointer to `char`                         | Array of `char` (size 7)                  |
| **Memory Location**      | Pointer to read-only memory               | Allocated on the stack (or static/global) |
| **Content Modifiable?**  | No (Undefined behavior if attempted)      | Yes                                       |
| **Memory Allocation**    | Only pointer `s` is on the stack; string in read-only memory | Entire array allocated on the stack       |
| **String Copy?**         | No (points to a literal)                  | Yes (makes a copy of the literal)         |

### Summary

- `char* s = "foobar"`: `s` is a pointer to a read-only string literal, and modifying its content results in undefined behavior.
- `char s[7] = "foobar"`: `s` is a modifiable array that contains a copy of the string literal, and you can safely change its contents.


---


Got it! Let's focus purely on how `printf` prints the entire string starting from the first address when using `%s` and why that happens:

### Printing an Entire String When Only Given the First Address

When you pass the first address of a string (or array of characters) to `printf` using the `%s` format specifier, the function doesn't just print the first character. Instead, it continues to print each subsequent character until it encounters a null terminator (`\0`), which marks the end of the string.

#### How This Works:
1. **First Address Points to the Entire String**:
   - When you pass a pointer (or an array's name) to `printf` with `%s`, you are essentially passing the **address of the first character**.
   - The string or array is stored in contiguous memory, meaning that each character is placed one after another in memory. The string continues until a special character `\0` (the null terminator) indicates the end.

2. **Contiguous Memory Layout**:
   - For example, when you declare:
     ```c
     char s1[] = "abcdef";
     ```
     The array `s1` is stored in memory like this:
     ```
     Address     | Value
     --------------------
     0x1000      | 'a'
     0x1001      | 'b'
     0x1002      | 'c'
     0x1003      | 'd'
     0x1004      | 'e'
     0x1005      | 'f'
     0x1006      | '\0'  // Null terminator
     ```

3. **`printf("%s", s1)` Behavior**:
   - When you call `printf("s1: %s\n", s1);`, you are passing the **address of `s1[0]`** (the first character, `'a'`).
   - `printf` begins at this memory address, printing the character `'a'`.
   - It then **moves to the next address** (in this case, `0x1001`) and prints `'b'`, and so on.
   - This continues until it reaches the null terminator `\0` at address `0x1006`. When `printf` detects `\0`, it knows the string has ended and stops printing.

4. **Role of the Null Terminator (`\0`)**:
   - The null terminator is critical because it tells `printf` where the string ends. Without it, `printf` would keep printing characters from memory, possibly printing garbage values or causing an error.
   - This is why strings in C are typically null-terminated — to define the end of the sequence for functions like `printf`.

### Why It Prints the Whole String:
- Even though you only provide the **address of the first character** (`s1` or `&s1[0]`), `printf` keeps reading memory sequentially, printing each character until it encounters the null terminator `\0`.
- So, if you pass `s1`, which starts at `'a'`, it will print `'a'`, `'b'`, `'c'`, and so on, until it reaches the null terminator at the end of the string.

### Conclusion:
The reason `printf` can print the entire string when only given the first address is because:
- Strings are stored in contiguous memory.
- The null terminator (`\0`) marks the end of the string.
- `printf` prints each character sequentially, starting from the first address, until it reaches `\0`.


---

In C, string literals are immutable, and you can't directly assign a new string to an existing character array after it has been initialized. Here's why:

1. `char x[] = "hi";` initializes the character array `x` with the string "hi", and the size of the array is determined based on the length of the string.
2. Once the array is created, you cannot reassign it to point to another string using `x = "changed";`. This is because arrays in C are not pointers; they are fixed-size blocks of memory.

If you want to change the contents of the array, you need to either copy a new string into the array or work with pointers instead.

### Option 1: Using `strcpy` to copy a new string into the array
```c
#include <stdio.h>
#include <string.h>

int main() {
    char x[] = "hi";  // Initializes a character array
    printf("Before change: %s\n", x);

    strcpy(x, "changed");  // Copies a new string into the existing array
    printf("After change: %s\n", x);

    return 0;
}
```
Note: Make sure that the size of `x` is large enough to hold the new string. If the string you're copying is larger than the original array size, you'll encounter undefined behavior.

### Option 2: Using pointers to allow reassignment
```c
#include <stdio.h>

int main() {
    const char *x = "hi";  // x is a pointer to a string literal
    printf("Before change: %s\n", x);

    x = "changed";  // Reassign the pointer to point to another string
    printf("After change: %s\n", x);

    return 0;
}
```
In this case, `x` is a pointer to a string literal, and you can reassign it to point to a different string. However, remember that string literals themselves are immutable, so you can't modify the contents of the string once assigned.


Here’s a small note about the `const` keyword in C, particularly in the context of string manipulation like `const char[]`:

---

### Understanding `const` in C

In C, the `const` keyword is used to define variables whose values cannot be changed after initialization. It is particularly useful when you want to protect data from being altered, ensuring that certain variables remain constant throughout the execution of the program.

#### Example:

```c
const char nno[] = ", !";
```

This defines an array of characters `nno`, which contains the string `", !"`. Since it is marked as `const`, the contents of `nno` cannot be modified. Any attempt to change the value of an element in the array will result in a compilation error.

#### Key Points:

- **Immutable Data**: The `const` modifier ensures that the data is read-only and cannot be modified after it has been set.
  
  ```c
  nno[0] = 'A';  // This will cause a compilation error because nno is constant.
  ```

- **Protection Against Accidental Changes**: By marking a variable as `const`, you prevent accidental modification of its value, which can help make your code more robust and less prone to bugs.
  
- **Use with Pointers**: `const` can also be used with pointers to ensure that the value the pointer points to does not change.

  ```c
  const char *ptr = "Hello!";
  ```

- **Difference from `char[]`**: When using `const char[]`, the array itself is constant and cannot be modified. However, a non-const `char[]` would allow changes to individual elements.

#### Practical Use Case:

Consider a scenario where you want to work with predefined data, such as punctuation characters, that should never change during program execution:

```c
#include <stdio.h>

const char nno[] = ", !";

int main() {
    printf("Constant string: %s\n", nno);
    // nno[0] = 'A';  // This would cause a compilation error.
    return 0;
}
```

This simple program demonstrates how `const` prevents modification of the `nno` array and ensures the integrity of its contents.

--- 

### In Summary:

- `const` ensures that the value of a variable or array cannot be modified after initialization.
- It's useful for protecting important data, like fixed strings or constant values, from accidental changes.


---

### Section 6.5: Copying Strings in C

In C, strings are represented as arrays of characters terminated by a null character (`'\0'`). Copying strings is a bit more involved than copying basic data types like integers due to the nature of arrays and pointers in C.

#### Pointer Assignments Do Not Copy Strings

Unlike integers, where you can simply use the assignment operator (`=`) to copy values, the same is not true for strings. When you use the assignment operator with strings, it only copies the **address** of the string, not the actual content of the string.

##### Example 1: Pointer Assignment (Shallow Copy)

```c
#include <stdio.h>

int main(void) {
    int a = 10, b;
    char c[] = "abc", *d;

    b = a;  // Integer is copied
    a = 20;  // Modifying a leaves b unchanged (deep copy)
    printf("%d %d\n", a, b);  // Prints "20 10"

    d = c;  // Only copies the address of the string (shallow copy)
    
    c[1] = 'x';  // Modifies the original string
    printf("%s %s\n", c, d);  // Prints "axc axc" since both c and d point to the same string
    return 0;
}
```

- **Explanation**: In this example, `d = c;` only copies the **address** of the string `c` to `d`. As a result, both `c` and `d` point to the same string in memory. Any modification to `c` will also affect `d` because they share the same memory location.
- This behavior is known as a **shallow copy** because it only copies the pointer, not the actual data.

##### Example 2: Assignment to Arrays (Compile Error)

```c
#include <stdio.h>

int main(void) {
    char a[] = "abc";
    char b[8];

    b = a;  // This will cause a compile error
    printf("%s\n", b);
    return 0;
}
```

- **Explanation**: In this example, `b = a;` will result in a **compile error** because arrays in C cannot be assigned to each other directly. You cannot use the assignment operator to copy arrays (including strings).

#### Copying Strings Using Standard Functions

To copy the contents of a string into another, you need to use standard library functions like `strcpy()` from the `string.h` library. This function ensures that the actual characters in the string are copied, not just the pointer.

##### Example 3: Copying Strings with `strcpy()`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char a[] = "abc";
    char b[8];

    strcpy(b, a);  // Copies the content of string 'a' to 'b'
    printf("%s\n", b);  // Prints "abc"
    return 0;
}
```

- **Explanation**: `strcpy(b, a);` performs a **deep copy**, meaning it copies the actual content of the string `a` into the array `b`. The destination array `b` must have enough space allocated to hold the string, including the null terminator (`'\0'`).

#### Key Points:

- **Shallow Copy**: Using the assignment operator with strings only copies the pointer to the string, not the string itself. Both pointers will refer to the same memory location.
- **Deep Copy**: To copy the actual contents of a string, use functions like `strcpy()` that ensure the characters are copied to a new memory location.
- **Array Assignment**: Arrays (including strings) cannot be assigned directly in C, and doing so will result in a compile-time error.

#### Summary:

- Strings are arrays of characters in C, and the assignment operator (`=`) does not perform a deep copy for strings.
- To copy a string's content, use functions like `strcpy()` from `string.h`.
- Ensure that the destination array has enough space for the copied string, including the null terminator.

### Section 6.9: String Formatted Data Read/Write

#### Writing Formatted Data to String

The `sprintf()` function allows you to format and store data into a string. It works similarly to `printf()`, but instead of printing the data to the console, it writes the formatted data to the provided string buffer.

##### Function Prototype
```c
int sprintf(char *str, const char *format, ...);
```
- `str`: Pointer to the destination buffer where the formatted string is stored.
- `format`: The format string (same as in `printf`).
- `...`: Additional arguments, depending on the format specifiers.

##### Example: Writing Float Data to String
```c
#include <stdio.h>

int main() {
    char buffer[50];
    double PI = 3.1415926;

    sprintf(buffer, "PI = %.7f", PI);  // Writes "PI = 3.1415926" to buffer
    printf("%s\n", buffer);            // Prints the content of buffer

    return 0;
}
```

- **Explanation**: In this example, `sprintf()` formats the value of `PI` to a string with 7 decimal places and stores it in the `buffer`. The buffer is then printed.

---

#### Reading Formatted Data from String

The `sscanf()` function reads data from a string based on a specified format. It is essentially the opposite of `sprintf()`, extracting values from a formatted string.

##### Function Prototype
```c
int sscanf(const char *str, const char *format, ...);
```
- `str`: The source string to read from.
- `format`: The format string used to extract values.
- `...`: Pointers to variables where the extracted values will be stored.

##### Example: Parsing Formatted Data
```c
#include <stdio.h>

int main() {
    char sentence[] = "date : 06-06-2012";
    char str[50];
    int year, month, day;

    sscanf(sentence, "%s : %2d-%2d-%4d", str, &day, &month, &year);
    printf("%s -> %02d-%02d-%4d\n", str, day, month, year);  // Prints: date -> 06-06-2012

    return 0;
}
```

- **Explanation**: In this example, `sscanf()` parses the formatted string `sentence`, extracting the day, month, and year. The extracted values are then printed in the desired format.

---

### Section 6.10: Find First/Last Occurrence of a Specific Character

The functions `strchr()` and `strrchr()` are used to find the first and last occurrence of a specific character in a null-terminated string.

- **`strchr()`**: Returns a pointer to the first occurrence of a character.
- **`strrchr()`**: Returns a pointer to the last occurrence of a character.

#### Example: Finding Character Occurrence
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char toSearchFor = 'A';
    char input[] = "BAbbbbbAccccAAAAzzz";

    char *firstOcc = strchr(input, toSearchFor);
    if (firstOcc != NULL) {
        printf("First position of %c in %s is %td.\n", toSearchFor, input, firstOcc - input);
    } else {
        printf("%c is not in %s.\n", toSearchFor, input);
    }

    char *lastOcc = strrchr(input, toSearchFor);
    if (lastOcc != NULL) {
        printf("Last position of %c in %s is %td.\n", toSearchFor, input, lastOcc - input);
    }

    return 0;
}
```

- **Explanation**: The program searches for the character 'A' in the string `input`, finding both the first and last occurrences using `strchr()` and `strrchr()`.

---

### Section 6.11: Copy and Concatenation

In C, `strcpy()` is used to copy strings, and `strcat()` is used to concatenate strings.

#### Example: Copy and Concatenate Strings
```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char mystring[10];

    strcpy(mystring, "foo");  // Copies "foo" into mystring
    printf("%s\n", mystring);  // Output: foo

    strcat(mystring, "bar");   // Concatenates "bar" to mystring
    printf("%s\n", mystring);  // Output: foobar

    strcpy(mystring, "bar");   // Overwrites mystring with "bar"
    printf("%s\n", mystring);  // Output: bar

    return 0;
}
```

- **Explanation**: `strcpy()` copies the string "foo" into `mystring`, and `strcat()` appends "bar" to it.

---

### Section 6.12: String Comparison

Functions like `strcmp()` and `strncmp()` are used to compare strings lexicographically.

- **`strcmp()`**: Compares two strings until a null character or a difference is found.
- **`strncmp()`**: Compares up to the first `n` characters of two strings.

#### Example: String Comparison
```c
#include <stdio.h>
#include <string.h>

void compare(char const *lhs, char const *rhs) {
    int result = strcmp(lhs, rhs);  // Compare the two strings

    if (result < 0) {
        printf("%s comes before %s\n", lhs, rhs);
    } else if (result == 0) {
        printf("%s equals %s\n", lhs, rhs);
    } else {
        printf("%s comes after %s\n", lhs, rhs);
    }
}

int main(void) {
    compare("BBB", "BBB");  // Output: BBB equals BBB
    compare("BBB", "CCCCC");  // Output: BBB comes before CCCCC
    compare("BBB", "AAAAAA");  // Output: BBB comes after AAAAAA

    return 0;
}
```

- **Explanation**: `strcmp()` performs a lexicographical comparison of two strings, and the result is printed based on the comparison outcome.




### Section 6.13: Safely Convert Strings to Numbers (Using `strtoX` Functions)

The `strtoX` functions are used to convert strings (which are essentially text) into numbers. The "X" in `strtoX` can stand for different types of numbers, such as long integers or floating-point numbers. These functions are safer than older methods like `atoi` or `atof` because they can detect if something goes wrong during the conversion, such as:

- **Overflow**: The number is too large for the type.
- **Underflow**: The number is too small for the type.
- **No valid number**: The string doesn't contain a valid number.

The functions also allow you to specify the **base** of the number system (e.g., binary, decimal, hexadecimal) when converting integers.

#### Breaking Down the Example:

```c
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <math.h>

int main(int argc, char* argv[]) {
    if (argc < 2) {
        printf("No number given.\n");
        return EXIT_FAILURE; 
    }
    
    char *endptr;
    double ret = strtod(argv[1], &endptr);  // Attempt to convert string to double.

    // Check for conversion errors.
    if (endptr == argv[1]) {
        printf("No number found in the string.\n");
        return EXIT_FAILURE;
    }
    else if ((ret == HUGE_VAL || ret == -HUGE_VAL) && errno == ERANGE) {
        printf("Numeric overflow or underflow occurred.\n");
        return EXIT_FAILURE;
    }

    printf("The number is: %f\n", ret);
    return EXIT_SUCCESS;
}
```

#### Step-by-Step Explanation:

1. **Argument Check**:  
   The program expects a number as a command-line argument. If none is given, it prints "No number given" and exits.

2. **String Conversion (`strtod`)**:  
   - `strtod` tries to convert the string to a **double** (floating-point number).
   - It takes two arguments: the string to convert and a pointer (`endptr`) that will point to the character **after** the number in the string (or the original string if no valid number was found).

3. **Error Checking**:  
   After attempting the conversion, several checks are made:
   - If `endptr` is equal to the string pointer (`argv[1]`), no valid number was found.
   - If the result is `HUGE_VAL` or `-HUGE_VAL`, and `errno` is set to `ERANGE`, an overflow or underflow occurred.

4. **Success**:  
   If everything is fine, the converted number is printed.

#### Example Usage:

If you compile and run the program with the input `"123.45"`, it will output:

```
The number is: 123.450000
```

If you input a string with no number (e.g., `"abc"`), it will output:

```
No number found in the string.
```

If you input a very large number that can't be represented, it will report an overflow or underflow.

---

### Section 6.14: `strspn` and `strcspn`

These functions are used to **find how many characters from a string match (or don’t match) a given set of characters**. 

- **`strspn`**: Finds how many characters at the start of a string belong to a specific set of characters (e.g., separators like `,.!?`).
- **`strcspn`**: Finds how many characters at the start of a string **do not** belong to a specific set of characters (i.e., how many are part of the "tokens").

#### Example:

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    const char sepchars[] = ",.;!?"; // Set of separator characters.
    char foo[] = ";ball call,.fall gall hall!?.,";
    char *s;
    int n;

    for (s = foo; *s != '\0'; /*empty*/) {
        // Find and print the number of separator characters at the start.
        n = (int)strspn(s, sepchars);
        if (n > 0) {
            printf("Skipping separators: << %.*s >> (length=%d)\n", n, s, n);
        }
        s += n;  // Skip past the separators.

        // Find and print the number of token characters (non-separators).
        n = (int)strcspn(s, sepchars);
        if (n > 0) {
            printf("Token found: << %.*s >> (length=%d)\n", n, s, n);
        }
        s += n;  // Skip past the tokens.
    }

    printf("== token list exhausted ==\n");
    return 0;
}
```

#### How It Works:

- **`strspn`**: In the loop, this function checks how many of the first characters in the string belong to the set of separators (like `,.;!?`). It then prints and skips over these separators.
  
- **`strcspn`**: After skipping the separators, it checks how many characters are **not** separators (i.e., part of a "token") and prints the token.

#### Output:

```
Skipping separators: << ; >> (length=1)
Token found: << ball >> (length=4)
Skipping separators: <<  >> (length=1)
Token found: << call >> (length=4)
Skipping separators: << ,. >> (length=2)
Token found: << fall >> (length=4)
Skipping separators: <<  >> (length=1)
Token found: << gall >> (length=4)
Skipping separators: <<  >> (length=1)
Token found: << hall >> (length=4)
Skipping separators: << !?., >> (length=4)
== token list exhausted ==
```

This demonstrates how `strspn` and `strcspn` can be used to process a string with separators and extract tokens from it.


