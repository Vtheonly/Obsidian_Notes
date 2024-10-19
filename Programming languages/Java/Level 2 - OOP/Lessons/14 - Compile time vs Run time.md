In Java (and programming in general), tasks can be divided into two categories: **compile-time** and **run-time**. Understanding the difference between these can help you optimize your code and debug more effectively. Below, I will outline the common tasks that are handled at compile-time versus those that occur at run-time.

### Compile-Time Tasks
These tasks are performed when the code is compiled. The Java compiler checks the code for syntax errors, type checks, and more. Here are some key activities that happen at compile time:

1. **Variable Declaration**: 
   - The compiler checks that variables are declared with valid types.
   ```java
   int number; // Declaration
   ```

2. **Variable Initialization**:
   - The compiler ensures that variables are initialized properly (if required) before being used.
   ```java
   int number = 10; // Initialization
   ```

3. **Constant Checking**:
   - Constants defined using `final` are resolved at compile time, and their values cannot change.
   ```java
   final int MAX_VALUE = 100; // Constant declaration
   ```

4. **Type Checking**:
   - The compiler checks for type compatibility, ensuring that operations between different data types are valid.
   ```java
   int result = number + 5; // Type checking
   ```

5. **Method Overloading Resolution**:
   - The compiler determines which overloaded method to call based on the method signature at compile time.
   ```java
   public void display(int a) { ... }
   public void display(String b) { ... }
   ```

6. **Array Declaration**:
   - The array's size can be determined at compile time when declared with a fixed size.
   ```java
   int[] numbers = new int[5]; // Compile-time size declaration
   ```

### Run-Time Tasks
These tasks are performed when the program is executed. This is when the actual logic and operations happen. Here are some key activities that occur at run time:

1. **Instantiation**:
   - Objects are created during run time using constructors.
   ```java
   Dog myDog = new Dog(); // Instantiation at run time
   ```

2. **Dynamic Binding**:
   - The method to invoke is determined at run time, especially in the case of overridden methods.
   ```java
   Animal animal = new Dog(); 
   animal.speak(); // Dynamic binding at run time
   ```

3. **Array Filling**:
   - The process of assigning values to an array is done during run time.
   ```java
   int[] numbers = new int[5];
   for (int i = 0; i < numbers.length; i++) {
       numbers[i] = i * 10; // Filling array at run time
   }
   ```

4. **Array Iteration**:
   - The loop that goes through the array elements occurs at run time.
   ```java
   for (int number : numbers) {
       System.out.println(number); // Iterating at run time
   }
   ```

5. **Exception Handling**:
   - Exception handling mechanisms, such as try-catch blocks, are resolved during run time when an exception occurs.
   ```java
   try {
       // code that may throw an exception
   } catch (Exception e) {
       // handle exception
   }
   ```

6. **User Input**:
   - Collecting input from users occurs during the execution of the program.
   ```java
   Scanner scanner = new Scanner(System.in);
   int input = scanner.nextInt(); // Run time user input
   ```

### Summary
Understanding the distinction between compile-time and run-time tasks is crucial for writing efficient code, debugging, and optimizing performance. Here's a quick summary:

| **Compile-Time Tasks**          | **Run-Time Tasks**                |
|---------------------------------|-----------------------------------|
| Variable Declaration            | Object Instantiation              |
| Variable Initialization         | Dynamic Binding                   |
| Constant Checking               | Array Filling                     |
| Type Checking                   | Array Iteration                   |
| Method Overloading Resolution    | Exception Handling                |
| Array Declaration               | User Input                        |

If you have any further questions or need clarification on any specific points, feel free to ask!