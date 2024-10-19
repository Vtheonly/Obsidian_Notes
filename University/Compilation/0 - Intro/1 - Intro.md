## Compiler Phases: From Source Code to Intermediate Code

This document outlines the key phases involved in compiling a program, focusing on lexical analysis, syntax analysis, semantic analysis, and intermediate code generation.

### 1. Lexical Analysis (Scanning)

**Purpose:** To break down the source code into meaningful units called tokens.

**Process:**

1. **Tokenization:** Identify and isolate individual words, symbols, and operators.
2. **Classification:** Determine the type of each token (keyword, identifier, operator, constant, separator).
3. **Symbol Table Management:** Add new identifiers to the symbol table, storing information about them.
4. **Error Handling:** Detect and report lexical errors, such as invalid characters or malformed tokens.

**Output:** A stream of tokens, each with an associated type and potentially other relevant information.

### 2. Syntax Analysis (Parsing)

**Purpose:** To verify that the sequence of tokens conforms to the grammar rules of the programming language.

**Process:**

1. **Grammatical Analysis:** Check if the token stream adheres to the defined syntax rules.
2. **Parse Tree Construction:** Create a hierarchical representation (parse tree) reflecting the grammatical structure of the code.
3. **Symbol Table Updates:** Add information about the scope and type of declared variables to the symbol table.
4. **Error Handling:** Detect and report syntax errors, such as missing semicolons or mismatched parentheses.

**Output:** A parse tree representing the syntactically valid structure of the program.

### 3. Semantic Analysis

**Purpose:** To ensure the program makes logical sense and adheres to the language's semantic rules.

**Process:**

1. **Type Checking:** Verify that operations are performed on compatible data types.
2. **Declaration Checking:** Ensure all variables are declared before use.
3. **Initialization Checking:** Confirm variables are initialized before being read.
4. **Semantic Error Handling:** Detect and report semantic errors, such as type mismatches or undeclared variables.

**Output:** An annotated parse tree (decorated syntax tree) containing semantic information.

### 4. Intermediate Code Generation

**Purpose:** To transform the decorated syntax tree into a platform-independent intermediate representation, bridging the gap between high-level code and machine code.

**Intermediate Code Forms:**

**4.1. Postfix Notation:**

* **Concept:** Operators follow their operands, eliminating the need for parentheses and precedence rules.
* **Example:** `a + b * c` becomes `a b c * +`.

**4.2. Three-Address Code:**

* **Concept:** Uses simple instructions with at most three addresses (two for operands and one for the result).

    * **Quadruples:** `(operator, operand1, operand2, result)` 
        * Example: 
        ```
        (*, b, c, t1)
        (+, t1, a, t2)
        (=, t2, x, -) 
        ```

    * **Triples:** `(operator, operand1, operand2)` - previous result is implicitly used.
        * Example:
        ```
        (*, b, c)
        (+, (1), a) 
        (=, (2), x)
        ```

    * **Indirect Triples:** Similar to triples but uses an index table to refer to results.

**4.3. Abstract Syntax Tree (AST):**

* **Concept:**  A tree structure where internal nodes represent operators and leaf nodes represent operands.
* **Example:** 
    ```
        =
       / \
      x   +
         / \
        a   *
           / \
          b   c
    ```

**Output:** An intermediate code representation of the program, suitable for further optimization and translation.
### 4.5 Intermediate Code Optimization

This phase aims to improve the efficiency of the generated intermediate code, striking a balance between execution speed and memory usage. 

**Optimization Techniques:**

* **Dead Code Elimination:** Removing code that doesn't contribute to the final result (e.g., unreachable code, unused variable assignments).
* **Loop Invariant Code Motion:** Moving calculations that produce the same result inside a loop to outside the loop, reducing redundant computations.
* **Operator Strength Reduction:** Replacing computationally expensive operators with equivalent but faster alternatives (e.g., replacing multiplication with repeated addition when appropriate).

**Benefits:**

* Faster execution speed.
* Reduced memory footprint.

### 4.6 Object Code Generation

This phase translates the optimized intermediate code into machine-specific object code, taking into account the target architecture.

**Considerations:**

* **Target Machine Architecture:**  Instruction set, register allocation, memory organization.
* **Operating System:** System calls, library functions.
* **Assembler:**  Syntax and directives of the target assembler.

**Output:**  Object code files containing machine instructions ready for linking and execution.

### 4.7 Symbol Table Management

The symbol table is a crucial data structure maintained throughout the compilation process. It stores information about:

* **Identifiers:** Variable names, function names, etc.
* **Types:** Data types of identifiers.
* **Scopes:** Where identifiers are declared and accessible.
* **Memory Addresses:** Locations assigned to variables.

**Usage in Different Phases:**

* **Lexical Analysis:** Adding new identifiers.
* **Syntax Analysis:**  Verifying declaration and scope rules.
* **Semantic Analysis:** Type checking and resolving identifier references.
* **Intermediate Code Generation:**  Using symbol table information for address assignments.

**Importance:** Ensures correct identifier resolution, type safety, and efficient code generation.




### 4.8 Error Handling

Effective error handling is crucial throughout the compilation process to provide helpful feedback to the programmer and ensure the generation of correct code.

**Types of Errors:**

* **Lexical Errors:**  Misspellings, invalid characters, incorrect token formation.
* **Syntax Errors:**  Violations of grammar rules, such as missing semicolons or mismatched parentheses.
* **Semantic Errors:**  Logical inconsistencies, such as type mismatches, undeclared variables, or multiple declarations.
* **Logical Errors:**  Flaws in the program's logic that lead to unexpected results, often detected during runtime.

**Error Severity:**

* **Warnings:**  Potential issues that do not prevent compilation but might indicate problems (e.g., unused variables).
* **Fatal Errors:**  Severe errors that halt compilation and prevent code generation (e.g., syntax errors, undeclared identifiers).

**Error Reporting:**

* **Error Location:** Specifying the line number (and column if possible) where the error occurred.
* **Error Message:** Providing a clear and concise description of the problem.
* **Error Recovery:** Attempting to continue compilation after encountering an error to detect additional issues.

**Error Recovery Techniques:**

* **Panic Mode:** Skipping tokens until a synchronizing token is found (e.g., semicolon, end of block).
* **Phrase Level Recovery:** Attempting to replace a sequence of erroneous tokens with a valid phrase.
* **Error Productions:**  Adding error-handling rules to the grammar to handle specific error scenarios.

**Benefits of Robust Error Handling:**

* **Improved Programmer Productivity:**  Clear error messages and locations facilitate debugging.
* **Enhanced Code Quality:**  Early detection of errors prevents potential runtime issues.
* **Increased Compiler Robustness:**  Error recovery mechanisms enable the compiler to handle unexpected input gracefully.


### Compilation Processes

1. **Tokenization and Lexical Analysis:**
   - **Tokenization:** Each word in the source code is assigned a unique token, essentially converting human-readable characters into numerical representations for the computer.
   - **Lexical Analysis [[Compilation/Library/1 - Lexical Analysis]]:** A part of the compiler that performs lexical analysis uses context-free grammar (type 2). It involves the generation of a syntax tree, which can be traversed in different orders such as infix, postfix, or abstract.

2. **Nature of the Token:**
   - Tokens serve to classify the different elements of your code. They identify keywords (like `if`, `else`, `for`), operators (+, -, *, /), code blocks, function names, variable names, and memory addresses.

3. **Macro:**
   - A macro is a powerful tool that allows you to define a reusable block of code. You define it once with a name, and then you can use that name throughout your program to insert the entire code block. This saves time and makes your code more readable.

4. **Code Error Handling:**
   - **Generate Error Messages:** Compilers provide descriptive messages indicating the type and location of the error.
   - **Create Error Reports:** Some compilers offer detailed reports to help you understand the context of the error.
   - **Suggest Solutions:** In some cases, the compiler might suggest possible solutions to resolve the error.

5. **Loop Transformation:**
   - During compilation, complex loops in your code are often transformed into simpler, lower-level instructions similar to assembly language. This optimization helps your program execute more efficiently.

6. **Variable Simplification:**
   - Compilers break down complex variable types and data structures into simpler instructions that can be easily understood and processed by the computer's hardware.

7. **Tree Traversal (Parsing):**
   - **The Importance of a Starting Pattern:** When a compiler parses your code, it often represents the code's structure as a tree. To traverse this tree correctly, the compiler needs a defined starting point and a clear path to follow.
   - **"Precisez le chemin":** Emphasizes the need for a precise traversal path, ensuring the compiler processes every part of your code correctly.
   - **Analyze Syntax and Tree Generation [[2 - Tree Generation]]:** The analysis of syntax involves generating a tree, and the correct generation requires knowledge of operation priorities.

8. **Linking Multiple Object Files:**
   - **Resolution:** The linker connects function calls and variable references across different files.
   - **Physical Addresses & Pointers:** This involves resolving memory addresses and setting up pointers so that different parts of your program work together seamlessly.

9. **Correct Analysis Doesn't Guarantee Correct Execution:**
   - Even if the compiler successfully analyzes your code and generates an executable file, it doesn't guarantee that your program is entirely free of errors. Logical errors or runtime issues might still exist.

10. **Intermediate Code Generation with Triplets and Quadruplets:**
    - **Triplets [[1 - Triplets]]:** Used in generating intermediate code with syntax like `1000 // address, operand or opcode, num1, num2`. The address is in RAM.
    - **Example of Multiplication [[3 - Multiplication in Compiler]]:** `x = a + b * c` is represented as:
      ```
      100 : *, b, c
      101 : +, a, 100
      ```
    - **Quadruplets [[2 - Quadruplets vs. Triplets]]:** Provide more control over where values are stored, with syntax like:
      ```
      $1 : *, b, c
      $2 : +, a, $1
      ```
    - **User Knowledge vs. Compiler Control [[2 - User Knowledge vs. Compiler Control]]:** The user doesn't know where the value is stored; only the compiler does. Quadruplets allow changing variable names but use more memory.

11. **Simple Operations in Assembly [[1 - Assembly]]:**
    - Operations include arithmetic operations (+, -), conditional and unconditional branching, logical operations, and simple variable operations.

12. **Code Optimization [[1 - Code Optimization]]:**
    - After obtaining intermediate code, optimization is performed. Examples include simplifying expressions like `x = 2*y` to `x = y + y` and removing dead or invalid code.
