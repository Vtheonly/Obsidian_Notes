---
tags: [upcasting, downcasting, type-casting]
aliases: [upcasting, downcasting, type casting]
keywords: [upcasting, downcasting, type casting]
---

### 1. Upcasting:

- **Definition:**
  - Upcasting refers to casting an [[002 Object|object]] of a subclass to its superclass. It happens implicitly, and no explicit casting is required.

- **Example:**
  ```java
  class Animal { /* ... */ }
  class Dog extends Animal { /* ... */ }

  Dog myDog = new Dog();
  Animal myAnimal = myDog; // Upcasting (implicit)
  ```

- **Explanation:**
  - Here, `myDog` is an object of the subclass `Dog`. When it's assigned to `myAnimal`, it's implicitly upcast to the superclass `Animal`.

### 2. Downcasting:

- **Definition:**
  - Downcasting refers to casting an object of a superclass to its subclass. It requires explicit casting and may lead to `ClassCastException` if the object is not an instance of the subclass.

- **Example:**
  ```java
  class Animal { /* ... */ }
  class Dog extends Animal { /* ... */ }

  Animal myAnimal = new Dog();
  Dog myDog = (Dog) myAnimal; // Downcasting (explicit)
  ```

- **Explanation:**
  - Here, `myAnimal` is an object of the superclass `Animal`. It's explicitly downcast to the subclass `Dog` using `(Dog)`.

### Important Points:

1. **Safety Concerns:**
   - Upcasting is generally safe and implicit.
   - Downcasting is explicit and may lead to [[004 Compile Time vs Run Time|runtime]] errors (ClassCastException) if not done carefully.

2. **Type Checking:**
   - Use `instanceof` to check the type before downcasting:
     ```java
     if (myAnimal instanceof Dog) {
         Dog myDog = (Dog) myAnimal;
     }
     ```

3. **[[030 Inheritance|Inheritance]] Hierarchy:**
   - Upcasting and downcasting are meaningful in the context of [[005 Intro to Classes|class]] inheritance.

4. **[[042 Polymorphism Summary|Polymorphism]]:**
   - These concepts contribute to achieving polymorphism in Java, where an object can take multiple forms.

### Example with Inheritance Hierarchy:

```java
class Animal {
    void makeSound() {
        System.out.println("Some generic sound");
    }
}

class Dog extends Animal {
    void bark() {
        System.out.println("Woof woof!");
    }
}

public class Main {
    public static void main(String[] args) {
        // Upcasting
        Animal myAnimal = new Dog(); // Implicit upcasting

        // Downcasting
        if (myAnimal instanceof Dog) {
            Dog myDog = (Dog) myAnimal; // Explicit downcasting
            myDog.bark();
        }

        // Calling overridden method
        myAnimal.makeSound(); // Polymorphism
    }
}
```

In this example, `myAnimal` is upcast to `Animal` and then downcast to `Dog` to access `bark()`. The `makeSound()` method demonstrates polymorphism by calling the overridden method in the subclass.

---
**Keywords:** #upcasting, #downcasting, #type-casting
