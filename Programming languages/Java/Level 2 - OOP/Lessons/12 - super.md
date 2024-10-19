In this video transcript, the creator explains the **super keyword** in Java with an example involving superheroes, showcasing how to use it to access the properties and methods of a superclass (or parent class). Let's summarize the key points of the explanation and example.

### The `super` Keyword in Java
The `super` keyword in Java is used to refer to the superclass (or parent class) of the current object. It is similar to the `this` keyword, which refers to the current class, but `super` focuses on the parent class. This is particularly important when working with inheritance, as it allows access to the superclass's methods, constructors, or variables.

### Example Overview

In this example, the instructor sets up two classes:
- **Person**: The superclass that holds general attributes for a person (name, age).
- **Hero**: A subclass that extends `Person` and adds an extra attribute (power) specific to superheroes.

The use of `super` demonstrates how to call the constructor and methods of the `Person` class when creating a `Hero` object.

### Step-by-Step Breakdown

1. **Person Class (Superclass)**:
   - Attributes: `String name` and `int age`.
   - Constructor: Initializes the `name` and `age` of a person.
   - `toString` Method: Returns a string with the person's name and age.

2. **Hero Class (Subclass)**:
   - Additional Attribute: `String power`.
   - Constructor: Initializes `name`, `age`, and `power` by calling the superclass constructor using `super(name, age)` and assigning the `power`.
   - `toString` Method: Calls the `toString` method of the superclass using `super.toString()` and appends the `power` attribute.

### Usage of `super`
- **Calling Superclass Constructor**: The `Hero` constructor uses `super(name, age)` to pass the `name` and `age` parameters to the `Person` constructor.
- **Calling Superclass Methods**: The `Hero` class also uses `super.toString()` to call the `Person` class’s `toString` method before appending its own additional information (`power`).

### Code Example

```java
class Person {
    String name;
    int age;

    Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String toString() {
        return this.name + "\n" + this.age + "\n";
    }
}

class Hero extends Person {
    String power;

    Hero(String name, int age, String power) {
        super(name, age);  // Call to superclass constructor
        this.power = power;
    }

    public String toString() {
        return super.toString() + this.power + "\n";  // Call to superclass method
    }
}

public class Main {
    public static void main(String[] args) {
        Hero hero1 = new Hero("Batman", 42, "Money");
        Hero hero2 = new Hero("Superman", 43, "Everything");

        System.out.println(hero1.toString());
        System.out.println(hero2.toString());
    }
}
```

### Output
```
Batman
42
Money

Superman
43
Everything
```

### Conclusion

The **`super` keyword** allows subclasses to access properties and methods from the superclass, simplifying code reuse and ensuring that superclass attributes are initialized or methods are called as needed. This is particularly useful in hierarchical class structures like the `Person` and `Hero` example above.

By using `super`, you ensure that common attributes or behaviors (such as `name` and `age` in this case) are managed in the parent class and reused in the child class, avoiding code duplication and adhering to best practices in object-oriented programming.