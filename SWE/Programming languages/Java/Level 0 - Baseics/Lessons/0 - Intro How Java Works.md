
![[0.png]]![[1.png]]

#### **Computer Languages: High-Level vs. Low-Level**

Computer languages can be categorized as **high-level** (i.e., more human-readable, like Java or Python) and **low-level** (i.e., closer to machine code, like Assembly language). High-level languages allow developers to write code that is easier to understand and maintain. However, computers only understand **binary code** (i.e., machine code), which is composed of 0s and 1s. Therefore, high-level code must be translated into machine code for the computer to execute it.

#### **Source Code and Java Source Code**

**Source code** is the human-readable code written by developers, typically in a high-level language. In the context of Java, this source code is written in files with a `.java` extension (i.e., `abc.java`). This source code contains instructions that define the behavior and functionality of a Java program.

#### **Compilation Process: From Source Code to Bytecode**

1. **Java Source Code (`.java` file):**
   - The starting point is the **Java source code**. This code is saved in a `.java` file (i.e., `abc.java`).

2. **Java Compiler (`javac`):**
   - The **Java Compiler (`javac`)** is responsible for compiling the Java source code into an intermediate form called **Bytecode**.
   - During compilation, `javac` checks the source code for syntax errors and other issues. If errors are found, the compiler generates error messages, and the process stops until the errors are fixed.
   - If the code is error-free, `javac` produces a `.class` file (i.e., `abc.class`), which contains the **Bytecode**.

3. **Bytecode (`.class` file):**
   - The **Bytecode** is a platform-independent, low-level code that serves as an intermediary between the high-level Java source code and the machine code executed by the computer's hardware.
   - Bytecode is designed to be executed by the **Java Virtual Machine (JVM)**, allowing the same `.class` file to run on any platform with a compatible JVM.

#### **Execution Process: From Bytecode to Running Program**

The execution of a Java program involves several steps, which can be categorized into **Compile Time** and **Run Time** stages.

### **Compile Time**

1. **Java Source Code (`abc.java`):**
   - The developer writes the Java source code, which is saved with a `.java` file extension.

2. **javac (Compiler):**
   - The **javac** compiler processes the `.java` file, checking for errors and converting the source code into **Bytecode**.
   - If the compilation is successful (i.e., no errors), the result is a `.class` file containing the Bytecode.

### **Run Time**

1. **Java Virtual Machine (JVM):**
   - The **JVM** is the runtime environment that executes the Java Bytecode. It abstracts the underlying hardware and operating system, allowing Java programs to run on any platform with a JVM.

2. **Class Loader:**
   - The **Class Loader** is a part of the JVM that loads the `.class` file (i.e., the Bytecode) into memory. It ensures that all necessary classes are available and properly linked for execution.

3. **Bytecode Verifier:**
   - The **Bytecode Verifier** checks the loaded Bytecode for errors, security issues, and integrity. This step ensures that the Bytecode adheres to Java's strict rules, preventing unsafe or malicious code from running.

4. **Interpreter:**
   - Initially, the JVM uses an **Interpreter** to execute the Bytecode. The interpreter reads the Bytecode and translates it into machine code, which the CPU can execute.
   - The interpreter executes the Bytecode line by line, making it slower than directly running machine code.

5. **JIT (Just-In-Time Compiler):**
   - To improve performance, the JVM includes a **Just-In-Time (JIT) Compiler**. The JIT compiler optimizes frequently executed parts of the Bytecode by compiling them into native machine code at runtime.
   - Once a section of Bytecode is compiled by the JIT, it bypasses the interpreter, resulting in faster execution during subsequent runs.

6. **Operating System (OS) and Hardware:**
   - The JVM interacts with the underlying **Operating System (OS)** and **Hardware** to execute the native machine code.
   - This interaction allows the Java program to access system resources (i.e., memory, CPU) and perform tasks such as file I/O, network communication, and more.

### **Summary**

The Java execution process begins with writing **Java source code** (`.java` files) and involves compiling this code into **Bytecode** using the `javac` compiler. The **Bytecode** is a platform-independent intermediary code that can run on any system with a **JVM**. At runtime, the **JVM** loads, verifies, and interprets the Bytecode, with the option of optimizing it using the **JIT compiler** for faster execution. Finally, the JVM communicates with the **OS** and **Hardware** to execute the program, making Java a truly cross-platform language.

