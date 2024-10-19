
The `Math` class in Java, part of the `java.lang` package, provides a collection of methods for performing basic mathematical operations. Since `java.lang` is automatically imported, you can use the `Math` class methods directly in your code without any additional import statements.

#### 1. **`Math.abs()` - Absolute Value**

The `Math.abs()` method returns the absolute value of a given number, whether it’s an integer or a floating-point number. 

```java
int absoluteValue = Math.abs(-5);  // Returns 5
double absoluteDouble = Math.abs(-5.5);  // Returns 5.5
```

#### 2. **`Math.ceil()` and `Math.floor()` - Rounding**

- **`Math.ceil()`**: Rounds a floating-point number up to the nearest integer and returns it as a double.
- **`Math.floor()`**: Rounds a floating-point number down to the nearest integer and returns it as a double.

```java
double ceilValue = Math.ceil(4.3);  // Returns 5.0
double floorValue = Math.floor(4.9); // Returns 4.0
```

#### 3. **`Math.sqrt()` - Square Root**

The `Math.sqrt()` method returns the square root of a given number.

```java
double squareRoot = Math.sqrt(16);  // Returns 4.0
```

#### 4. **`Math.pow(base, exponent)` - Power Function**

The `Math.pow()` method raises a base number to the power of an exponent.

```java
double power = Math.pow(2, 3);  // Returns 8.0 (2^3)
```

#### 5. **`Math.round()` - Rounding to Nearest Integer**

The `Math.round()` method rounds a floating-point number to the nearest integer. It returns a `long` when rounding a `float`, and an `int` when rounding a `double`.

```java
long roundedValue = Math.round(4.6);  // Returns 5
```

#### 6. **`Math.min()` and `Math.max()` - Minimum and Maximum Values**

- **`Math.min()`**: Returns the smaller of two values.
- **`Math.max()`**: Returns the larger of two values.

```java
int minValue = Math.min(3, 7);  // Returns 3
int maxValue = Math.max(3, 7);  // Returns 7
```

#### 7. **`Math.random()` - Random Number Generation**

The `Math.random()` method generates a random `double` value between 0.0 (inclusive) and 1.0 (exclusive).

```java
double randomValue = Math.random();
```

#### Example Usage of Math Library

```java
public class MathExample {
    public static void main(String[] args) {
        int absoluteValue = Math.abs(-5);
        System.out.println("Absolute Value: " + absoluteValue);

        double squareRoot = Math.sqrt(16);
        System.out.println("Square Root: " + squareRoot);

        double power = Math.pow(2, 3);
        System.out.println("Power (2^3): " + power);

        long roundedValue = Math.round(4.6);
        System.out.println("Rounded Value: " + roundedValue);

        int minValue = Math.min(3, 7);
        System.out.println("Minimum Value: " + minValue);

        double randomValue = Math.random();
        System.out.println("Random Value: " + randomValue);
    }
}
```

In this example, the `Math` class methods are used to perform various mathematical operations. Note that there's no need to import the `Math` class explicitly, as it is part of the `java.lang` package, which is automatically included in every Java program.

#### Key Methods Recap

1. **`Math.abs()`**: Returns the absolute value of a number.
2. **`Math.pow(base, exponent)`**: Raises a base number to the power of the exponent.
3. **`Math.sqrt()`**: Returns the square root of a number.