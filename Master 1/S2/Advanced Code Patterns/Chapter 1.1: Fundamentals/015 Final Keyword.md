In Java, the `const` keyword is not used as it is in some other programming languages like C++ or JavaScript. Instead, Java uses the `final` keyword for similar purposes, but it is used in a different context.

### `final` Keyword in Java:

1. **Final Variables:**
   - When you declare a variable as `final`, you indicate that its value cannot be changed once it's assigned.

   ```java
   final int x = 10;
   // The value of x cannot be changed
   ```

2. **Final Methods:**
   - When you declare a method as `final` in a class, you indicate that the method cannot be overridden by subclasses.

   ```java
   public class MyClass {
       final void myMethod() {
           // Method implementation
       }
   }
   ```

3. **Final Classes:**
   - When you declare a class as `final`, you indicate that the class cannot be subclassed.

   ```java
   final class MyFinalClass {
       // Class implementation
   }
   ```

### final in Arrays :

When it comes to arrays in Java, the `final` keyword can be used in a different way. If a variable is declared as `final` and it is a reference to an array, the reference cannot be changed to point to a different array. However, the content of the array itself can still be modified.

Example:

```java
public class ArrayExample {
    public static void main(String[] args) {
        final int[] numbers = {1, 2, 3, 4, 5};

        // The reference 'numbers' cannot be changed
        // Uncommenting the line below would result in a compilation error
        // numbers = new int[]{6, 7, 8, 9, 10};

        // The content of the array can be modified
        numbers[0] = 100;

        // Print the modified array
        for (int number : numbers) {
            System.out.println(number);
        }
    }
}
```

In this example, `numbers` is declared as `final`, so you cannot reassign it to point to a different array. However, you can still modify the content of the array itself.

It's important to note that while the `final` keyword prevents reassignment of the reference for object types (like arrays), it does not make the object itself immutable. If you need an immutable array-like structure in Java, you might consider using `java.util.Collections.unmodifiableList` or similar approaches.