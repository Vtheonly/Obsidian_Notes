---
title: "Using g++: The GNU C++ Compiler"
---

## The GNU C++ Compiler (`g++`)

`g++` is the command for the C++ compiler that is part of the GNU Compiler Collection (GCC). It is one of the most widely used, standards-compliant C++ compilers, making it an essential tool for any C++ developer.

Key features of `g++`:

1.  **Multi-language support**: GCC supports C++, C, Objective-C, Fortran, Ada, Go, and D. `g++` specifically invokes the C++ compiler.
2.  **Cross-platform**: `g++` can generate code for a vast range of processor architectures and operating systems.
3.  **Standards Compliance**: It closely follows the ISO C++ standards, including the latest versions like C++11, C++14, C++17, C++20, and C++23.
4.  **Optimization**: `g++` provides powerful optimization capabilities to improve the performance of the compiled code.
5.  **Free Software**: It is released under the GNU General Public License (GPL).

### Basic `g++` Usage

Here are some common `g++` commands for C++ development:

1.  **Compiling a simple C++ program**:
    ```bash
    g++ myprogram.cpp -o myprogram
    ```

2.  **Specifying a C++ standard**:
    ```bash
    g++ -std=c++20 myprogram.cpp -o myprogram
    ```

3.  **Enabling warnings for better code quality**:
    ```bash
    g++ -Wall -Wextra myprogram.cpp -o myprogram
    ```

4.  **Compiling with debugging information for use with GDB**:
    ```bash
    g++ -g myprogram.cpp -o myprogram
    ```

### Important `g++` Flags

-   `-std=<standard>`: Specifies the C++ language standard (e.g., `-std=c++17`, `-std=c++20`).
-   `-Wall`: Enables most common warnings.
-   `-Wextra`: Enables additional warnings not covered by `-Wall`.
-   `-Werror`: Treats all warnings as errors, stopping compilation.
-   `-O<level>`: Sets the optimization level. Common levels are:
    -   `-O0`: No optimization (default).
    -   `-O2`: A good balance of optimization for release builds.
    -   `-O3`: More aggressive optimizations.
    -   `-Os`: Optimizes for code size.
-   `-g`: Includes debugging information in the executable.
-   `-c`: Compiles the source file into an object file (`.o`) without linking.
-   `-I<dir>`: Adds a directory to the header file search path.
-   `-L<dir>`: Adds a directory to the library search path.
-   `-l<name>`: Links against a library (e.g., `-lfmt` to link against the {fmt} library).

### Example: Compiling a Multi-File Project

Suppose you have a project with `main.cpp`, `helper.cpp`, and `helper.hpp`:

**Step 1: Compile each source file into an object file.**
```bash
g++ -std=c++20 -c main.cpp -o main.o
g++ -std=c++20 -c helper.cpp -o helper.o
```

**Step 2: Link the object files together to create the executable.**
```bash
g++ main.o helper.o -o myprogram
```

Or, you can do it in a single step, though this is less efficient for large projects as it recompiles everything every time:
```bash
g++ -std=c++20 main.cpp helper.cpp -o myprogram
```

### Using `g++` with Make

For larger projects, `make` is used to automate the build process. A simple `Makefile` for a C++ project might look like this:

```makefile
# Use g++ as the C++ compiler
CXX=g++
# Set compiler flags: C++20 standard, all warnings, and debug info
CXXFLAGS=-std=c++20 -Wall -Wextra -g

# List of source files
SRCS=main.cpp helper.cpp
# Generate object file names from source files
OBJS=$(SRCS:.cpp=.o)
# The final executable name
TARGET=myprogram

# The default rule: build the executable
all: $(TARGET)

# Rule to link the executable
$(TARGET): $(OBJS)
    $(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS)

# Rule to compile a .cpp file into a .o file
%.o: %.cpp
    $(CXX) $(CXXFLAGS) -c $< -o $@

# Rule to clean up generated files
clean:
    rm -f $(OBJS) $(TARGET)
```

With this `Makefile`, you can build the project by simply running `make`, and clean up with `make clean`.

Understanding `g++` and its options is fundamental for C++ development, giving you control over standards, performance, and debugging.
