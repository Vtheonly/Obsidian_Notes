

The `java.util.Random` class in Java is commonly used to generate random numbers. Below are some commonly used methods and functions provided by the `Random` class:

### 1. Generating Random Integers:

- **Method:** `nextInt(int bound)`
  - Generates a random integer between 0 (inclusive) and the specified bound (exclusive).

  ```java
  import java.util.Random;

  public class RandomExample {
      public static void main(String[] args) {
          Random random = new Random();
          int randomNumber = random.nextInt(10); // Generates a random integer between 0 and 9
          System.out.println("Random Integer: " + randomNumber);
      }
  }
  ```

### 2. Generating Random Doubles:

- **Method:** `nextDouble()`
  - Generates a random double between 0.0 (inclusive) and 1.0 (exclusive).

  ```java
  import java.util.Random;

  public class RandomExample {
      public static void main(String[] args) {
          Random random = new Random();
          double randomDouble = random.nextDouble(); // Generates a random double between 0.0 and 1.0
          System.out.println("Random Double: " + randomDouble);
      }
  }
  ```

### 3. Generating Random Booleans:

- **Method:** `nextBoolean()`
  - Generates a random boolean value.

  ```java
  import java.util.Random;

  public class RandomExample {
      public static void main(String[] args) {
          Random random = new Random();
          boolean randomBoolean = random.nextBoolean(); // Generates a random boolean
          System.out.println("Random Boolean: " + randomBoolean);
      }
  }
  ```

### 4. Setting Seed for Reproducibility:

- **Constructor with Seed:** `Random(long seed)`
  - Creates a new random number generator using a specified seed.
  - Using the same seed will produce the same sequence of random numbers.

  ```java
  import java.util.Random;

  public class RandomExample {
      public static void main(String[] args) {
          long seed = 123;
          Random random = new Random(seed);
          int randomNumber = random.nextInt(10);
          System.out.println("Random Integer with Seed: " + randomNumber);
      }
  }
  ```

### 5. Shuffling Arrays:

- **Method:** `shuffle(T[] array)`
  - Shuffles the elements of an array randomly.

  ```java
  import java.util.Arrays;
  import java.util.Collections;
  import java.util.List;
  import java.util.Random;

  public class RandomExample {
      public static void main(String[] args) {
          Integer[] array = {1, 2, 3, 4, 5};
          List<Integer> list = Arrays.asList(array);
          Collections.shuffle(list, new Random());
          System.out.println("Shuffled Array: " + list);
      }
  }
  ```

These are some of the commonly used methods and functions provided by the `Random` class. The class provides more methods for generating different types of random values, and you can choose the one that fits your specific needs.



