---
title: "Hello, World! in C++"
---

To create a simple C++ program that prints "Hello, World!" to the screen, you need to use a text editor to create a new file (e.g., `hello.cpp`—the file extension is typically `.cpp`).

### hello.cpp

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
```

### Breakdown of the Program

Let's examine this simple program line by line:

1.  **`#include <iostream>`**
    This line is a preprocessor directive that tells the compiler to include the `iostream` header file. This header is part of the C++ Standard Library and contains the declarations for input/output operations, such as `std::cout`.

2.  **`int main()`**
    This line defines the `main` function. In C++, program execution always begins in the `main` function. The `int` indicates that the function will return an integer value to the operating system upon completion.

3.  **`{ ... }`**
    The curly braces `{` and `}` define the scope of the `main` function. All the code inside these braces is part of the function.

4.  **`std::cout << "Hello, World!" << std::endl;`**
    This is the line that does the printing.
    -   `std::cout` is the standard character output stream, which usually directs output to the console.
    -   The `<<` operator is the stream insertion operator. It "inserts" the data that follows it into the stream.
    -   `"Hello, World!"` is a string literal that we want to print.
    -   `std::endl` is a manipulator that inserts a newline character into the output stream and flushes the stream. This moves the cursor to the next line.
    -   Every statement in C++ must end with a semicolon (`;`).

5.  **`return 0;`**
    This statement ends the `main` function and returns the value `0` to the operating system. A return value of `0` conventionally indicates that the program executed successfully.

### Compiling and Running the Program

To run the program, you must first compile the source file (`hello.cpp`) into an executable file using a C++ compiler like `g++` or `clang++`.

#### Compile using `g++`

1.  Open a terminal or command prompt.
2.  Navigate to the directory where you saved `hello.cpp`.
3.  Run the following command:

    ```bash
    g++ hello.cpp -o hello
    ```

    -   `g++` is the command to invoke the GNU C++ compiler.
    -   `hello.cpp` is your source file.
    -   `-o hello` tells the compiler to name the output executable file `hello`.

4.  If there are no errors, the compiler will create an executable file named `hello` (or `hello.exe` on Windows).

5.  To run the program, execute the following command:

    ```bash
    ./hello
    ```

    You should see the following output on your screen:

    ```
    Hello, World!
    ```