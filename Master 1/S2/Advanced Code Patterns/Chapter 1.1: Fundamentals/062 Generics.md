
Generics enable types (classes and interfaces) to be parameters when defining classes, interfaces, and methods. This feature eliminates the need to create multiple versions of methods or classes for various data types, allowing for a more efficient and cleaner codebase.

## Benefits of Generics
- **Code Reusability**: One version of a method or class can handle multiple data types.
- **Type Safety**: Compile-time checks ensure type correctness.

## Example: Generic Methods

### Non-Generic Method
Initially, if we want to display elements from different arrays (e.g., integers, doubles, characters, strings), we would need separate methods for each type:

```java
public void displayIntArray(int[] arr) { ... }
public void displayDoubleArray(double[] arr) { ... }
public void displayCharArray(char[] arr) { ... }
public void displayStringArray(String[] arr) { ... }
```

### Using Generics
Instead of creating multiple methods, we can define a single generic method:

```java
public static <T> void displayArray(T[] arr) {
    for (T element : arr) {
        System.out.println(element);
    }
}
```

### Generic Method Example
Here’s how we can use the generic method to display arrays of different types:

```java
Integer[] intArray = {1, 2, 3};
Double[] doubleArray = {1.1, 2.2, 3.3};
Character[] charArray = {'a', 'b', 'c'};
String[] stringArray = {"Hello", "World"};

displayArray(intArray);
displayArray(doubleArray);
displayArray(charArray);
displayArray(stringArray);
```

## Example: Generic Classes

### Non-Generic Classes
To store different types of data, we could create multiple classes:

```java
public class MyInteger {
    private int x;
    public MyInteger(int x) { this.x = x; }
    public int getValue() { return x; }
}
```

### Using a Generic Class
Instead of creating separate classes for each type, we can define a generic class:

```java
public class MyGeneric<T> {
    private T x;
    public MyGeneric(T x) { this.x = x; }
    public T getValue() { return x; }
}
```

### Using the Generic Class
We can create instances of the generic class for different types:

```java
MyGeneric<Integer> myInt = new MyGeneric<>(1);
MyGeneric<Double> myDouble = new MyGeneric<>(3.14);
MyGeneric<Character> myChar = new MyGeneric<>('@');
MyGeneric<String> myString = new MyGeneric<>("Hello");
```

## Advanced Generics: Multiple Parameters
You can also define generic classes with multiple parameters:

```java
public class MyGenericTwo<T, U> {
    private T x;
    private U y;
    public MyGenericTwo(T x, U y) { this.x = x; this.y = y; }
    public U getSecondValue() { return y; }
}
```

### Example of Usage
```java
MyGenericTwo<Integer, String> pair = new MyGenericTwo<>(1, "One");
System.out.println(pair.getSecondValue()); // Output: One
```

## Bounded Types
To limit the scope of reference data types that can be passed to a generic class, we can use bounded types:

```java
public class MyNumber<T extends Number> {
    private T x;
    public MyNumber(T x) { this.x = x; }
}
```

### Example of Usage
```java
MyNumber<Integer> intNum = new MyNumber<>(5);
MyNumber<Double> doubleNum = new MyNumber<>(3.14);
```

## Conclusion
Generics in Java allow for creating flexible and reusable code while maintaining type safety. By leveraging generic methods and classes, you can significantly reduce code duplication and improve readability.
