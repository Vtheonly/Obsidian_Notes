

#### 1. What is the Scanner Library in Java?

The `Scanner` class is part of the `java.util` package in Java and is used for reading input from various sources such as the console, files, or strings. It provides methods for parsing and processing different types of data, making it a versatile tool for handling user input and other data streams.

#### 2. What Can the Scanner Library Do?

The `Scanner` class can be used to read different types of data, such as integers, floating-point numbers, strings, and more. It allows you to interactively accept user input or read from other input sources like files. Below is a simple example of using `Scanner` to read an integer from the console:

```java
import java.util.Scanner;

public class ScannerExample {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter an integer: ");
        int userInput = scanner.nextInt();

        System.out.println("You entered: " + userInput);

        // Don't forget to close the scanner to avoid resource leaks
        scanner.close();
    }
}
```

#### 3. Difference Between `nextLine` and `nextInt`

- **`nextLine`**: This method reads the entire line of input as a string, including spaces. It consumes the newline character (`\n`) left in the input buffer after a previous `nextInt`, `nextDouble`, etc. For example:

    ```java
    Scanner scanner = new Scanner(System.in);

    System.out.print("Enter a line of text: ");
    String line = scanner.nextLine();

    System.out.println("You entered: " + line);

    scanner.close();
    ```

- **`nextInt`**: This method reads the next token of input as an integer. It does not consume the newline character, leaving it in the buffer. If you subsequently use `nextLine`, it will read the remaining newline character, resulting in an empty line. To avoid this, you can consume the newline character using an additional `nextLine()` call after `nextInt`. For example:

    ```java
    Scanner scanner = new Scanner(System.in);

    System.out.print("Enter an integer: ");
    int number = scanner.nextInt();

    // Consume the newline character
    scanner.nextLine();

    System.out.println("You entered: " + number);

    scanner.close();
    ```

#### 4. Using Scanner for File I/O Basics

`Scanner` can also be used for reading from files. Here's a simple example of reading from a text file:

```java
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class FileScannerExample {
    public static void main(String[] args) {
        try {
            // Specify the file path
            File file = new File("example.txt");

            // Create a Scanner to read from the file
            Scanner fileScanner = new Scanner(file);

            // Read and print each line from the file
            while (fileScanner.hasNextLine()) {
                String line = fileScanner.nextLine();
                System.out.println(line);
            }

            // Close the file scanner
            fileScanner.close();
        } catch (FileNotFoundException e) {
            System.out.println("File not found: " + e.getMessage());
        }
    }
}
```

This example assumes there's a file named "example.txt" in the same directory as the Java program.

#### 5. Common Use Cases

- **Reading Integers:**
  - Reads an integer from the console.

    ```java
    Scanner scanner = new Scanner(System.in);
    int userInput = scanner.nextInt();
    ```

- **Reading Strings:**
  - Reads a string from the console.

    ```java
    Scanner scanner = new Scanner(System.in);
    String userInput = scanner.nextLine();
    ```

- **Reading Doubles:**
  - Reads a double from the console.

    ```java
    Scanner scanner = new Scanner(System.in);
    double userInput = scanner.nextDouble();
    ```

#### Conclusion

The `Scanner` class is a powerful tool in Java for handling input from various sources. It offers flexibility in reading different data types and can be used effectively in both console-based and file-based input scenarios. Understanding the nuances between methods like `nextLine` and `nextInt` is crucial for avoiding common pitfalls in input handling.