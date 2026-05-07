

The `new` keyword in Java is used to create a new instance of a class. When you want to instantiate a class, you use the `new` keyword followed by the class constructor. Here's an example using the `Random` class from the `java.util` package:

```java
Random random = new Random();
```

- `Random`: This is the name of the class you want to instantiate. In this case, it's the `Random` class, which provides methods for generating random numbers.

- `random`: This is the name you give to the instance of the `Random` class. You can choose any valid identifier as the name.

- `new Random()`: This part creates a new instance of the `Random` class. The `new` keyword allocates memory for a new object, and `Random()` is a constructor call that initializes the new object.

Once you've created the `Random` object, you can use its methods to generate random numbers. For example:

```java
int randomNumber = random.nextInt(100); // Generates a random integer between 0 (inclusive) and 100 (exclusive)
```

In this example, `nextInt(100)` generates a random integer between 0 (inclusive) and 100 (exclusive).

In summary, the `new` keyword is crucial for creating new instances of classes in Java, and it is used to allocate memory and initialize objects. In the given example, it is used to create a new instance of the `Random` class for generating random numbers.

--- 