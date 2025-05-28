
To create a simple C program that prints "Hello, World" on the screen, you need to use a text editor to create a new file (e.g., `hello.c` — the file extension must be `.c`). The following is the source code for the program:

### hello.c

```c
#include <stdio.h>

int main(void)
{
    puts("Hello, World");
    return 0;
}
```

Live demo on [Coliru](http://coliru.stacked-crooked.com/)

---

### Breakdown of the Program

Let's examine this simple program line by line:

1. **`#include <stdio.h>`**  
   This line tells the compiler to include the contents of the standard library header file `stdio.h` in the program. Headers are files that typically contain function declarations, macros, and data types.  
   Including `stdio.h` allows the use of the `puts()` function.  
   [See more about headers.](#)

2. **`int main(void)`**  
   This line begins the definition of a function. It specifies:
   - The name of the function (`main`).
   - The type and number of arguments it expects (`void`, meaning none).
   - The return type of the function (`int`).  
   
   Program execution always starts in the `main()` function.

3. **`{ ... }`**  
   The curly braces `{` and `}` are used to indicate where a block of code begins and ends. In this case, they define the start and end of the `main` function.

4. **`puts("Hello, World");`**  
   This line calls the `puts()` function to output text to the standard output (typically the screen), followed by a newline.  
   - `"Hello, World"` is a string literal enclosed in double quotes.  
   - In C, every statement must end with a semicolon (`;`).  
   [See more about strings.](#)

5. **`return 0;`**  
   The `main()` function is defined to return an `int` value, and `return 0;` indicates that the program has completed successfully. This statement also marks the end of the execution of the program.

---

### Editing the Program

You can use simple text editors to write the program, such as:
- **Linux:** `vim`, `gedit`
- **Windows:** `Notepad`
- **Cross-Platform Editors:** Visual Studio Code, Sublime Text

> Ensure that the editor creates plain text files and not RTF or any other format.

### Compiling and Running the Program

To run the program, the source file (`hello.c`) must first be compiled into an executable file (e.g., `hello` on Unix/Linux or `hello.exe` on Windows). This process uses a C language compiler.

#### Compile using GCC

GCC (GNU Compiler Collection) is a widely used C compiler. Follow these steps:

1. Open a terminal.
2. Navigate to the source file's location.
3. Run the following command:

```bash
gcc hello.c -o hello
```

- If no errors are found, the compiler creates a binary file named `hello` (the name specified after the `-o` option).

> To add warning options that help identify potential issues, use:  
```bash
gcc -Wall -Wextra -Werror -o hello hello.c
```

These warnings are optional for simple programs but can help avoid unexpected results.
