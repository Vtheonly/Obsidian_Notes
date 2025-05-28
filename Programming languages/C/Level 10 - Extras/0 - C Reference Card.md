
## Program Structure and Functions

- **Function Prototype**: `type fnc(type1, ...)`
- **Variable Declaration**: `type name;`
- **Main Routine**:
  ```c
  int main(void) {
      // Declarations
      // Statements
  }
  ```
- **Function Definition**:
  ```c
  type fnc(arg1, ...) {
      // Declarations
      // Statements
      return value;
  }
  ```
- **Comments**: `/* */` or `//` (C99 and later)
- **Main with Args**: `int main(int argc, char *argv[])`
- **Terminate Execution**: `exit(arg);`

Example:
```c
#include <stdio.h>
#include <stdlib.h>

// Function prototype
int add(int a, int b);

int main(int argc, char *argv[]) {
    int x = 5, y = 7;
    
    /* This is a multi-line comment
       Calling the add function */
    int result = add(x, y);
    
    printf("The sum of %d and %d is %d\n", x, y, result);
    
    return 0;
}

// Function definition
int add(int a, int b) {
    return a + b;
}
```

## C Preprocessor

- **Include Library File**: `#include <filename>`
- **Include User File**: `#include "filename"`
- **Replacement Text**: `#define name text`
- **Replacement Macro**: `#define name(var) text`
- **Undefine Macro**: `#undef name`
- **Quoted String in Replacement**: `#`
- **Concatenate Args and Rescan**: `##`
- **Conditional Execution**: `#if`, `#else`, `#elif`, `#endif`
- **Name Defined or Not?**: `#ifdef`, `#ifndef`, `defined(name)`
- **Line Continuation**: `\`

Example:
```c
#include <stdio.h>

#define PI 3.14159
#define SQUARE(x) ((x) * (x))
#define PRINT_VAR(var) printf(#var " = %d\n", var)
#define CONCAT(a, b) a##b

#ifdef DEBUG
    #define LOG(msg) printf("DEBUG: %s\n", msg)
#else
    #define LOG(msg)
#endif

int main() {
    int radius = 5;
    printf("Area of circle: %.2f\n", PI * SQUARE(radius));
    
    int x = 10;
    PRINT_VAR(x);
    
    int ab = 42;
    printf("CONCAT(a, b) = %d\n", CONCAT(a, b));
    
    LOG("This is a debug message");
    
    return 0;
}
```

## Data Types and Declarations

- **Character (1 byte)**: `char`
- **Integer**: `int`
- **Real Number**: `float`, `double`
- **Short (16-bit Integer)**: `short`
- **Long (32-bit Integer)**: `long`
- **Double Long (64-bit Integer)**: `long long`
- **Signed/Unsigned**: `signed`, `unsigned`
- **Pointer**: `int*`, `float*`, etc.
- **Enumeration Constant**: `enum tag {name1 = value1, ...};`
- **Constant (Read-Only Value)**: `const type name;`
- **External Variable**: `extern`
- **Internal to Source File**: `static`
- **Local Persistent Between Calls**: `static`
- **No Value**: `void`
- **Structure**: `struct tag { ... };`
- **Type Alias**: `typedef type name;`
- **Size of Object**: `sizeof(object)`
- **Size of Data Type**: `sizeof(type)`

Example:
```c
#include <stdio.h>

// Enumeration
enum Days {MON=1, TUE, WED, THU, FRI, SAT, SUN};

// Structure
struct Point {
    int x;
    int y;
};

// Type alias
typedef unsigned long ulong;

int main() {
    char c = 'A';
    int i = 42;
    float f = 3.14f;
    double d = 2.71828;
    unsigned long ul = 1234567890UL;
    
    int *ptr = &i;
    const int MAX = 100;
    
    enum Days today = WED;
    
    struct Point p = {10, 20};
    
    ulong big_number = 9876543210UL;
    
    printf("Size of int: %zu bytes\n", sizeof(int));
    printf("Size of Point struct: %zu bytes\n", sizeof(struct Point));
    
    return 0;
}
```

## Initialization

- **Variable Initialization**: `type name = value;`
- **Array Initialization**: `type name[] = {value1, ...};`
- **String Initialization**: `char name[] = "string";`

Example:
```c
#include <stdio.h>

int main() {
    int x = 5;
    float pi = 3.14159f;
    
    int numbers[] = {1, 2, 3, 4, 5};
    
    char greeting[] = "Hello, World!";
    
    int matrix[2][3] = {{1, 2, 3}, {4, 5, 6}};
    
    printf("x = %d\n", x);
    printf("First number: %d\n", numbers[0]);
    printf("Greeting: %s\n", greeting);
    printf("Matrix[1][2] = %d\n", matrix[1][2]);
    
    return 0;
}
```

## Constants

- **Suffix**: `long`, `unsigned`, `float` (e.g., `65536L`, `-1U`, `3.0F`)
- **Exponential Form**: `4.2e1`
- **Prefix**: `octal (0)`, `hexadecimal (0x or 0X)`
- **Character Constants**: `'a'`, `'\ooo'`, `'\xhh'`
- **Special Characters**: `\n`, `\r`, `\t`, `\b`, `\\`, `\?`, `\'`, `\"`
- **String Constant**: `"abc...de"`

Example:
```c
#include <stdio.h>

int main() {
    long big_number = 123456789L;
    unsigned int positive_only = 4294967295U;
    float precise = 0.1234F;
    
    double scientific = 6.022e23;  // Avogadro's number
    
    int octal = 0755;  // 493 in decimal
    int hex = 0xFF;    // 255 in decimal
    
    char newline = '\n';
    char tab = '\t';
    char single_quote = '\'';
    char backslash = '\\';
    
    char hex_char = '\x41';  // 'A' in ASCII
    
    printf("Big number: %ld\n", big_number);
    printf("Scientific notation: %e\n", scientific);
    printf("Octal: %d, Hex: %d\n", octal, hex);
    printf("Special chars: %c%c%c%c\n", newline, tab, single_quote, backslash);
    printf("Hex char: %c\n", hex_char);
    
    return 0;
}
```

## Pointers, Arrays, and Structures

- **Pointer Declaration**: `type *name;`
- **Function Returning Pointer**: `type *f();`
- **Pointer to Function**: `type (*pf)();`
- **Generic Pointer**: `void *`
- **Null Pointer**: `NULL`
- **Dereference Pointer**: `*pointer`
- **Address of Object**: `&name`
- **Array Declaration**: `name[dim]`
- **Multi-Dimensional Array**: `name[dim1][dim2]`
- **Structure Declaration**: `struct tag { ... };`
- **Access Structure Member**: `name.member`
- **Access Structure via Pointer**: `pointer->member`

Example:
```c
#include <stdio.h>
#include <stdlib.h>

struct Person {
    char name[50];
    int age;
};

int* create_array(int size);
void print_person(struct Person *p);

int main() {
    int *arr = create_array(5);
    for (int i = 0; i < 5; i++) {
        arr[i] = i * 10;
        printf("arr[%d] = %d\n", i, arr[i]);
    }
    free(arr);
    
    int matrix[2][3] = {{1, 2, 3}, {4, 5, 6}};
    printf("matrix[1][2] = %d\n", matrix[1][2]);
    
    struct Person john = {"John Doe", 30};
    struct Person *p_john = &john;
    
    printf("Name: %s, Age: %d\n", john.name, john.age);
    print_person(p_john);
    
    return 0;
}

int* create_array(int size) {
    return (int*)malloc(size * sizeof(int));
}

void print_person(struct Person *p) {
    printf("Name: %s, Age: %d\n", p->name, p->age);
}
```

## Operators

- **Struct Member Operator**: `name.member`
- **Struct Member via Pointer**: `pointer->member`
- **Increment/Decrement**: `++`, `--`
- **Plus/Minus, Logical Not, Bitwise Not**: `+`, `-`, `!`, `~`
- **Pointer Indirection**: `*pointer`, `&name`
- **Cast Expression**: `(type) expr`
- **Size of Object**: `sizeof`
- **Arithmetic Operators**: `*`, `/`, `%`, `+`, `-`
- **Bitwise Shift**: `<<`, `>>`
- **Relational Operators**: `>`, `>=`, `<`, `<=`
- **Equality**: `==`, `!=`
- **Bitwise AND/OR/XOR**: `&`, `|`, `^`
- **Logical AND/OR**: `&&`, `||`
- **Conditional Expression**: `expr1 ? expr2 : expr3`
- **Assignment Operators**: `+=`, `-=`, `*=`, etc.
- **Comma Operator**: `,`

Example:
```c
#include <stdio.h>

struct Point {
    int x, y;
};

int main() {
    int a = 5, b = 3;
    struct Point p = {10, 20};
    struct Point *ptr = &p;
    
    printf("a + b = %d\n", a + b);
    printf("a / b = %d\n", a / b);
    printf("a %% b = %d\n", a % b);
    
    printf("a << 1 = %d\n", a << 1);
    printf("a >> 1 = %d\n", a >> 1);
    
    printf("a & b = %d\n", a & b);
    printf("a | b = %d\n", a | b);
    printf("a ^ b = %d\n", a ^ b);
    printf("~a = %d\n", ~a);
    
    printf("a > b: %d\n", a > b);
    printf("a == b: %d\n", a == b);
    
    printf("!a: %d\n", !a);
    printf("a && b: %d\n", a && b);
    printf("a || b: %d\n", a || b);
    
    int max = (a > b) ? a : b;
    printf("max: %d\n", max);
    
    printf("p.x = %d, p.y = %d\n", p.x, p.y);
    printf("ptr->x = %d, ptr->y = %d\n", ptr->x, ptr->y);
    
    return 0;
}
```

## Flow of Control

- **Statement Terminator**: `;`
- **Block Delimiters**: `{ }`
- **Exit from Loops or Switch**: `break;`
- **Next Iteration of Loop**: `continue;`
- **Goto**: `goto label;`
- **Label**: `label: statement`
- **Return from Function**: `return expr;`

### Flow Constructions
- **If Statement**
- **While Loop**
- **For Loop**
- **Do-While Loop**
- **Switch Statement**

Example:
```c
#include <stdio.h>

int main() {
    // If statement
    int x = 10;
    if (x > 5) {
        printf("x is greater than 5\n");
    } else if (x < 5) {
        printf("x is less than 5\n");
    } else {
        printf("x is equal to 5\n");
    }
    
    // While loop
    int i = 0;
    while (i < 5) {
        printf("%d ", i);
        i++;
    }
    printf("\n");
    
    // For loop
    for (int j = 0; j < 5; j++) {
        if (j == 2) continue;  // Skip 2
        printf("%d ", j);
        if (j == 3) break;     // Stop at 3
    }
    printf("\n");
    
    // Do-while loop
    int k = 0;
    do {
        printf("%d ", k);
        k++;
    } while (k < 5);
    printf("\n");
    
    // Switch statement
    char grade = 'B';
    switch (grade) {
        case 'A':
            printf("Excellent!\n");
            break;
        case 'B':
            printf("Good job!\n");
            break;
        case 'C':
            printf("Average performance.\n");
            break;
        default:
            printf("Needs improvement.\n");
    }
    
    // Goto (use sparingly)
    int m = 0;
start:
    if (m < 5) {
        printf("%d ", m);
        m++;
        goto start;
    }
    printf("\n");
    
    return 0;
}
```

## ANSI Standard Libraries

- `<assert.h>`: Diagnostics
- `<ctype.h>`: Character handling
- `<errno.h>`: Error handling
- `<float.h>`: Floating-point characteristics
- `<limits.h>`: Implementation-defined limits
- `<locale.h>`: Localization
- `<math.h>`: Mathematics
- `<setjmp.h>`: Non-local jumps
- `<signal.h>`: Signal handling
- `<stdarg.h>`: Variable arguments
- `<stddef.h>`: Common definitions
- `<stdio.h>`: Input/output
- `<stdlib.h>`: General utilities
- `<string.h>`: String handling
- `<time.h>`: Date and time


```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <ctype.h>
#include <assert.h>
#include <limits.h>
#include <float.h>

int main() {
    // stdio.h
    printf("Hello, World!\n");
    
    // stdlib.h
    int *arr = (int*)malloc(5 * sizeof(int));
    if (arr == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }
    for (int i = 0; i < 5; i++) {
        arr[i] = i * 10;
    }
    printf("Random number: %d\n", rand() % 100);
    free(arr);
    
    // string.h
    char str1[] = "Hello";
    char str2[] = "World";
    char result[20];
    strcpy(result, str1);
    strcat(result, " ");
    strcat(result, str2);
    printf("Concatenated string: %s\n", result);
    printf("Length of result: %lu\n", strlen(result));
    
    // math.h
    double x = 2.5;
    printf("Square root of %.2f is %.2f\n", x, sqrt(x));
    printf("Sin of %.2f is %.2f\n", x, sin(x));
    
    // time.h
    time_t now = time(NULL);
    printf("Current time: %s", ctime(&now));
    
    // ctype.h
    char c = 'A';
    printf("Is '%c' alphanumeric? %s\n", c, isalnum(c) ? "Yes" : "No");
    printf("Lowercase of '%c' is '%c'\n", c, tolower(c));
    
    // assert.h
    int a = 5;
    assert(a == 5);  // This will pass
    // assert(a == 10);  // This would fail and terminate the program
    
    // limits.h
    printf("Maximum value of int: %d\n", INT_MAX);
    printf("Minimum value of int: %d\n", INT_MIN);
    
    // float.h
    printf("Maximum value of float: %e\n", FLT_MAX);
    printf("Minimum positive value of float: %e\n", FLT_MIN);
    
    return 0;
}
```

This example demonstrates the usage of various ANSI Standard Libraries in C. Let's break down each library's usage:

1. `<stdio.h>`: Used for input/output operations, like `printf()` and `fprintf()`.
2. `<stdlib.h>`: Provides functions for memory allocation (`malloc()`), random number generation (`rand()`), and memory deallocation (`free()`).
3. `<string.h>`: Offers string manipulation functions like `strcpy()`, `strcat()`, and `strlen()`.
4. `<math.h>`: Provides mathematical functions such as `sqrt()` and `sin()`.
5. `<time.h>`: Used for time-related functions like `time()` and `ctime()`.
6. `<ctype.h>`: Offers character classification and conversion functions like `isalnum()` and `tolower()`.
7. `<assert.h>`: Provides the `assert()` macro for debugging purposes.
8. `<limits.h>`: Defines constants with the limits of integral types, like `INT_MAX` and `INT_MIN`.
9. `<float.h>`: Defines constants related to floating-point types, such as `FLT_MAX` and `FLT_MIN`.

Additional libraries not demonstrated in this example:

10. `<errno.h>`: Provides access to the error number set by system calls and some library functions.
11. `<locale.h>`: Used for localization, allowing programs to adapt to different cultural conventions.
12. `<setjmp.h>`: Provides non-local jumps, used for handling exceptions and errors.
13. `<signal.h>`: Used for handling various signals (like interrupts) that may occur during program execution.
14. `<stdarg.h>`: Provides facilities for writing functions that accept a variable number of arguments.
15. `<stddef.h>`: Defines several useful types and macros.

These standard libraries provide a wide range of functionality that covers most common programming needs in C. By using these libraries effectively, you can write more robust, efficient, and portable C programs.

## Best Practices and Tips

1. **Memory Management**: Always free dynamically allocated memory to prevent memory leaks.
2. **Input Validation**: Check user inputs to ensure they are within expected ranges.
3. **Error Handling**: Use return values and error codes to handle exceptional situations.
4. **Const Correctness**: Use the `const` keyword to protect data that shouldn't be modified.
5. **Function Design**: Keep functions small and focused on a single task.
6. **Comments and Documentation**: Write clear comments explaining complex logic or algorithms.
7. **Avoid Global Variables**: Limit the use of global variables to improve modularity.
8. **Use Static Analysis Tools**: Employ tools like `lint` or modern static analyzers to catch potential issues.
9. **Consistent Naming Conventions**: Use clear and consistent naming for variables, functions, and types.
10. **Portability**: Be aware of platform-specific features and use standard libraries when possible for better portability.

Example of applying some best practices:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NAME_LENGTH 50

// Function prototype
static int get_user_age(const char *name);

int main() {
    char name[MAX_NAME_LENGTH];
    int age;

    // Input validation
    do {
        printf("Enter your name (max %d characters): ", MAX_NAME_LENGTH - 1);
        if (fgets(name, sizeof(name), stdin) == NULL) {
            fprintf(stderr, "Error reading input\n");
            return 1;
        }
        name[strcspn(name, "\n")] = 0;  // Remove newline if present
    } while (strlen(name) == 0);

    age = get_user_age(name);
    if (age == -1) {
        fprintf(stderr, "Error getting age\n");
        return 1;
    }

    printf("Hello, %s! You are %d years old.\n", name, age);

    return 0;
}

static int get_user_age(const char *name) {
    int age;
    char input[20];

    printf("%s, please enter your age: ", name);
    if (fgets(input, sizeof(input), stdin) == NULL) {
        return -1;
    }

    if (sscanf(input, "%d", &age) != 1 || age < 0 || age > 150) {
        fprintf(stderr, "Invalid age input\n");
        return -1;
    }

    return age;
}
```

This example demonstrates several best practices:

1. Input validation for both name and age.
2. Use of `const` for function parameters that shouldn't be modified.
3. Error handling with appropriate return values.
4. Use of `static` for internal functions.
5. Consistent naming conventions.
6. Use of `#define` for constants.
7. Comments explaining the purpose of code blocks.

By following these best practices and utilizing the standard libraries effectively, you can write more robust, maintainable, and efficient C programs.