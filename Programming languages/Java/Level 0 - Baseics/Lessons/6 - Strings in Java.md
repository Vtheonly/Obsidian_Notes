In Java, strings are objects rather than arrays of characters. Although strings have methods for various operations, you cannot access individual characters using array notation. Instead, you use the `charAt()` method to retrieve specific characters at a given index.

#### Accessing Characters in a String

You can access individual characters in a string using the `charAt()` method:

```java
String A = "word";
char firstCharacter = A.charAt(0);
System.out.println("The first character is: " + firstCharacter);
```

**Output:**
```
The first character is: w
```

If you want to treat a string like an array and iterate over each character, you can use a loop:

```java
String A = "word";

for (int i = 0; i < A.length(); i++) {
    char currentChar = A.charAt(i);
    System.out.println("Character at index " + i + ": " + currentChar);
}
```

This code will print each character in the string along with its index.

#### Common String Operations

Java provides various methods in the `String` class for manipulating strings:

- **Concatenation:**
  ```java
  String B = " Java";
  String concatenated = A + B; // "word Java"
  ```

- **Substring:**
  ```java
  String substring = A.substring(1, 3); // "or"
  ```

- **Length:**
  ```java
  int length = A.length(); // 4
  ```

- **Conversion between String and Numbers:**
  ```java
  int number = Integer.parseInt("123"); // Convert string to int
  String str = String.valueOf(456);    // Convert int to string
  ```

#### Useful String Methods

1. **`trim()` - Remove Leading and Trailing Whitespace:**
   ```java
   String trimmedString = inputString.trim();
   ```

2. **`toUpperCase()` - Convert to Uppercase:**
   ```java
   String upperCaseString = inputString.toUpperCase();
   ```

3. **`toLowerCase()` - Convert to Lowercase:**
   ```java
   String lowerCaseString = inputString.toLowerCase();
   ```

4. **`indexOf(char)` - Find Index of a Character:**
   ```java
   int indexOfChar = inputString.indexOf('a');
   ```

5. **`charAt(index)` - Get Character at Index:**
   ```java
   char charAtIndex = inputString.charAt(2);
   ```

6. **`replace(oldChar, newChar)` - Replace Characters:**
   ```java
   String replacedString = inputString.replace('a', 'b');
   ```

7. **`replaceAll(regex, replacement)` - Replace with Regular Expression:**
   ```java
   String replacedString = inputString.replaceAll("\\s", "_");
   ```

8. **`split(regex)` - Split String into Array:**
   ```java
   String[] parts = inputString.split("\\s");
   ```

9. **Parsing to Int:**
   ```java
   int number = Integer.parseInt(inputString);
   ```

10. **Parsing to Double:**
    ```java
    double value = Double.parseDouble(inputString);
    ```

#### Immutability of Strings

Remember that strings in Java are immutable. Once a string is created, its content cannot be changed. Any operation that seems to modify a string actually creates a new string. For frequent modifications, consider using `StringBuilder` for better performance.
