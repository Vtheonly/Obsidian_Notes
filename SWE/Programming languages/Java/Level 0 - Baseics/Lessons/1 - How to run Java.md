### Running a Java Program from the Terminal

When running a Java program from the terminal, it's important to understand the relationship between your source code, the compiled class files, and the terminal commands you use to execute your program.

#### Basic Steps:

1. **Navigate to the Directory:**
   - Ensure you are in the directory where your `.java` file is located.
   - Use the `cd` command to navigate:

     ```bash
     cd path_to_your_directory
     ```

2. **Compile the Java File:**
   - Use `javac` to compile your `.java` file into a `.class` file:

     ```bash
     javac Example.java
     ```

   - This will generate a `Example.class` file in the same directory.

3. **Run the Compiled Class:**
   - Use the `java` command to run the compiled class:

     ```bash
     java Example
     ```

   - Note that you should **not** include the `.class` extension in this command.

#### Using the `-cp` Option:

- The `-cp` (or `-classpath`) option allows you to explicitly specify the classpath, which is the location where the JVM should look for the compiled `.class` files.

  ```bash
  java -cp . Example
  ```

- In this example, `.` specifies the current directory as the classpath. This is useful if you want to ensure that the JVM is looking in the correct location.

#### Common Errors:

- **Class Not Found:** If you see an error like `ClassNotFoundException`, it usually means the JVM cannot find the specified class. Ensure the `.class` file is in the directory you are running the command from.
  
- **No Main Method:** If the class you're trying to run does not have a `main` method, the JVM will not know where to start execution, and it will throw an error.

#### Practical Example:

Assume you have the following files in your directory:

- `Example.java` (contains the `public static void main(String[] args)` method)
- `Runner.java` (no `main` method)

**Compilation:**

```bash
javac Example.java Runner.java
```

**Running the Program:**

```bash
java Example
```

This command will execute the `main` method in the `Example` class.

### Key Points:

- Always compile your `.java` files before running them.
- Use the class name (without `.class`) when running the compiled program.
- If you need to specify a custom classpath, use the `-cp` option.

This note should help you effectively compile and run Java programs from the terminal.