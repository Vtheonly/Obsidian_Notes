


## Introduction
Wrapper classes in Java provide a way to use primitive data types as reference data types. This note covers the basic concepts, advantages, disadvantages, and practical examples of using wrapper classes, as well as the features of autoboxing and unboxing.

## What Are Wrapper Classes?
- **Primitive Data Types**: Include `boolean`, `char`, `int`, `double`, `byte`, `short`, `float`, etc.
- **Reference Data Types**: Wrapper classes allow primitive data types to be treated as objects, enabling the use of methods and compatibility with collections such as `ArrayLists`.
  
## Advantages of Wrapper Classes
1. **Useful Methods**: Each wrapper class provides useful methods. For example:
   - `String` methods
   - `Boolean`, `Character`, `Integer`, and `Double` methods
2. **Collections Compatibility**: Only reference data types can be used with certain collections like `ArrayLists`.

## Disadvantages of Wrapper Classes
1. **Performance**: Reference data types are slower to access than primitive data types because they involve additional steps.
2. **Increased Processing Power**: Using reference data types for large datasets (e.g., millions of numbers) requires more time and processing power.

## Naming Convention of Wrapper Classes
- Each primitive data type has a corresponding wrapper class with the same name but with the first letter capitalized.
  - `boolean` -> `Boolean`
  - `char` -> `Character`
  - `int` -> `Integer`
  - `double` -> `Double`

## Practical Example: Autoboxing and Unboxing
Java provides features called **autoboxing** and **unboxing**:
- **Autoboxing**: Automatic conversion of primitive data types to their corresponding wrapper classes.
  ```java
  Boolean a = true; // Auto-boxing of boolean to Boolean
  Character b = '@'; // Auto-boxing of char to Character
  Integer c = 123; // Auto-boxing of int to Integer
  Double d = 3.14; // Auto-boxing of double to Double
  ```
- **Unboxing**: The reverse process, where a wrapper class is automatically converted to a primitive data type.
  ```java
  if (a == true) { // Unboxing of Boolean to boolean
      System.out.println("This is true");
  }
  ```

## Summary of Methods in Wrapper Classes
- **Boolean**: Methods like `compareTo`, `equals`, `parseBoolean`.
- **Character**: Methods like `isDigit`, `isLetter`, `toUpperCase`.
- **Integer**: Methods like `parseInt`, `compare`, `toString`.
- **Double**: Methods like `compareTo`, `isNaN`, `toString`.

## Conclusion
Wrapper classes are essential when you need to treat primitive data types as objects, especially in situations involving collections. However, they come with performance trade-offs, so it's important to choose between using primitive types and wrapper classes based on the context of your program.
