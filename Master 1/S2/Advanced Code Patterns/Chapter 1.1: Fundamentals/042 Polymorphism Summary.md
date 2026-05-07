### Summary of Polymorphism in Java

---

In this video, we dive into **polymorphism**, a fundamental concept in object-oriented programming, specifically in Java. Here's a breakdown of the key points:

### 1. **What is Polymorphism?**
- **Definition**: Polymorphism comes from the Greek words *poly* (meaning many) and *morph* (meaning form). In Java, it refers to the **ability of an object to identify as more than one type**. 
- Example: A `Car` object can identify as both a `Car` and a `Vehicle`, because `Car` is a subclass of `Vehicle`.

### 2. **Setting Up a Polymorphic Example**
- We create a **parent class** `Vehicle` and several **child classes** that extend it:
  ```java
  class Vehicle { }
  class Car extends Vehicle { }
  class Bicycle extends Vehicle { }
  class Boat extends Vehicle { }
  ```

- **Problem**: If we want to store instances of `Car`, `Bicycle`, and `Boat` in an array, we can't do that with arrays of their specific types (e.g., `Car[]`). 
- **Solution**: Use polymorphism by making an array of the **parent type** (`Vehicle[]`). Since `Car`, `Bicycle`, and `Boat` all extend `Vehicle`, they can be stored in this array:
  ```java
  Vehicle[] racers = { new Car(), new Bicycle(), new Boat() };
  ```

### 3. **Creating the `go()` Method**
- Each class (Car, Bicycle, Boat) has a unique implementation of a `go()` method:
  ```java
  class Car extends Vehicle {
      public void go() {
          System.out.println("The car begins moving");
      }
  }
  
  class Bicycle extends Vehicle {
      public void go() {
          System.out.println("The bicycle begins moving");
      }
  }
  
  class Boat extends Vehicle {
      public void go() {
          System.out.println("The boat begins moving");
      }
  }
  ```

### 4. **Method Overriding**
- Each subclass **overrides** the `go()` method from `Vehicle`. This is a key part of polymorphism, allowing the same method (`go()`) to behave differently depending on the object type.

### 5. **Using Polymorphism in a Loop**
- Instead of calling `go()` on each object individually (e.g., `car.go()`), we can use an **enhanced for loop** to iterate over all the vehicles in the array:
  ```java
  for (Vehicle x : racers) {
      x.go();
  }
  ```
  This loop doesn’t care whether `x` is a `Car`, `Bicycle`, or `Boat` — as long as `x` is a `Vehicle` and has the `go()` method, the correct version of `go()` will be called.

### 6. **Why Use Polymorphism?**
- **Simplifies Code**: It allows for writing more **generalized code** that can work with different object types. 
- **Method Overriding**: Enables objects to define their own unique behavior for inherited methods, such as `go()`.

### Example Code:
```java
class Vehicle {
    public void go() { }
}

class Car extends Vehicle {
    @Override
    public void go() {
        System.out.println("The car begins moving");
    }
}

class Bicycle extends Vehicle {
    @Override
    public void go() {
        System.out.println("The bicycle begins moving");
    }
}

class Boat extends Vehicle {
    @Override
    public void go() {
        System.out.println("The boat begins moving");
    }
}

public class Main {
    public static void main(String[] args) {
        Vehicle[] racers = { new Car(), new Bicycle(), new Boat() };
        
        for (Vehicle x : racers) {
            x.go();  // Calls the correct go() method for each object
        }
    }
}
```

### 7. **Key Takeaways**
- Polymorphism allows objects of different types to be treated as instances of a parent type.
- Through **method overriding**, each object can have its own version of the same method.
- Polymorphism enhances flexibility and reduces code duplication.


---


That’s a great way to explain dynamic polymorphism in Java! Below, I’ll summarize and break down the key points from your script, providing a clear structure for anyone interested in the concept. This will help clarify dynamic polymorphism and include the code you’ve discussed.

# Dynamic Polymorphism in Java

## Introduction
- **Polymorphism**: Derived from the Greek words "poly" (many) and "morph" (shape/form), polymorphism means "many shapes/forms."
- **Dynamic Polymorphism**: Refers to the ability of an object to take many shapes/forms **after** the program has been compiled, during runtime.

## Key Concepts
- **Parent and Child Classes**: In this example, we create an `Animal` class (parent) and two child classes, `Dog` and `Cat`.
- **Method Overriding**: Child classes can override methods from the parent class. For example, both `Dog` and `Cat` override the `speak` method from the `Animal` class.

## Code Implementation

### Step 1: Create the Animal Class

```java
public class Animal {
    public void speak() {
        System.out.println("Animal goes BRR");
    }
}
```

### Step 2: Create the Dog Class

```java
public class Dog extends Animal {
    @Override
    public void speak() {
        System.out.println("Dog goes bark");
    }
}
```

### Step 3: Create the Cat Class

```java
public class Cat extends Animal {
    @Override
    public void speak() {
        System.out.println("Cat goes meow");
    }
}
```

### Step 4: Main Class with User Input

```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("What animal do you want?");
        System.out.println("1 = Dog");
        System.out.println("2 = Cat");

        int choice = scanner.nextInt();
        Animal animal = null; // Declare an animal variable

        if (choice == 1) {
            animal = new Dog(); // Instantiate as Dog
        } else if (choice == 2) {
            animal = new Cat(); // Instantiate as Cat
        } else {
            System.out.println("Invalid choice");
            animal = new Animal(); // Default animal
        }

        animal.speak(); // Call the speak method (dynamic polymorphism)
    }
}
```

## Explanation of the Code
- **User Input**: The program prompts the user to choose between a dog and a cat.
- **Instantiation**: Based on user input, an `Animal` object is instantiated as either a `Dog` or a `Cat`, demonstrating dynamic polymorphism.
- **Method Invocation**: The `speak` method is called on the `Animal` reference, which will execute the overridden method in the respective class.

## Real-World Examples of Dynamic Polymorphism
1. **Video Games**: Character selection, where a character might be a warrior, mage, or rogue, but is initially represented as a generic character.
2. **Game Development**: Similar to choosing a sprite in games like Pokémon, where the character type is defined later.

## Conclusion
Dynamic polymorphism allows for flexible code that can handle multiple object types at runtime, enhancing the reusability and maintainability of code.
