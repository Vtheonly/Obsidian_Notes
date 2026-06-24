### Basics of File I/O in Java

File Input/Output (I/O) operations in Java are essential for reading from and writing to files. These operations are handled by classes within the `java.io` package.

#### 1. **Reading from a File**

To read from a file, classes like `FileReader` and `BufferedReader` are commonly used. These classes allow you to read the contents of a file line by line efficiently.

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class ReadFileExample {
    public static void main(String[] args) {
        try (BufferedReader reader = new BufferedReader(new FileReader("example.txt"))) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

- **`FileReader`**: Reads the file character by character.
- **`BufferedReader`**: Wraps `FileReader` to read text efficiently, buffering the input.

#### 2. **Writing to a File**

To write to a file, you can use `FileWriter` and `BufferedWriter`. These classes enable you to write data to files efficiently, line by line if necessary.

```java
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class WriteFileExample {
    public static void main(String[] args) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("output.txt"))) {
            writer.write("Hello, this is a line in the file.");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

- **`FileWriter`**: Writes characters to a file.
- **`BufferedWriter`**: Wraps `FileWriter` to write text efficiently, buffering the output.

### Most Used File I/O Methods

#### Reading from a File

1. **`FileReader(String fileName)`**: 
   - Initializes a `FileReader` for the specified file.
   - Example:
     ```java
     FileReader fileReader = new FileReader("example.txt");
     ```

2. **`BufferedReader(Reader in)`**: 
   - Wraps an existing `Reader` for buffered input.
   - Example:
     ```java
     BufferedReader bufferedReader = new BufferedReader(fileReader);
     ```

3. **`readLine()` (in `BufferedReader`)**: 
   - Reads a line of text from the input stream.
   - Example:
     ```java
     String line = bufferedReader.readLine();
     ```

#### Writing to a File

1. **`FileWriter(String fileName)`**: 
   - Initializes a `FileWriter` for the specified file.
   - Example:
     ```java
     FileWriter fileWriter = new FileWriter("output.txt");
     ```

2. **`BufferedWriter(Writer out)`**: 
   - Wraps an existing `Writer` for buffered output.
   - Example:
     ```java
     BufferedWriter bufferedWriter = new BufferedWriter(fileWriter);
     ```

3. **`write(String str)` (in `BufferedWriter`)**: 
   - Writes a string to the output stream.
   - Example:
     ```java
     bufferedWriter.write("Hello, World!");
     ```

### Additional Methods

#### File Existence Check

1. **`exists()` (in `File`)**: 
   - Checks if the file exists.
   - Example:
     ```java
     File file = new File("example.txt");
     if (file.exists()) {
         System.out.println("File exists.");
     } else {
         System.out.println("File does not exist.");
     }
     ```

#### Reading All Lines from a File (Java 8 and later)

1. **`Files.readAllLines(Path path)` (in `java.nio.file.Files`)**: 
   - Reads all lines from a file as a `List<String>`.
   - Example:
     ```java
     import java.nio.file.Files;
     import java.nio.file.Path;
     import java.nio.file.Paths;
     import java.io.IOException;
     import java.util.List;

     public class ReadAllLinesExample {
         public static void main(String[] args) {
             try {
                 Path path = Paths.get("example.txt");
                 List<String> lines = Files.readAllLines(path);
                 for (String line : lines) {
                     System.out.println(line);
                 }
             } catch (IOException e) {
                 e.printStackTrace();
             }
         }
     }
     ```

### Summary

- **Reading**: Use `FileReader` with `BufferedReader` for efficient file reading.
- **Writing**: Use `FileWriter` with `BufferedWriter` for efficient file writing.
- **File Existence**: Check file existence with `File.exists()`.
- **Java 8 File Reading**: Use `Files.readAllLines()` for reading all lines into a list.

These basics cover essential File I/O operations in Java. Always ensure to handle `IOException` for robust file-handling code.