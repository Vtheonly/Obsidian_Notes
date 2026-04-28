
## Java Inheritance Notes

Inheritance in Java allows a **subclass** (child class) to derive or inherit properties (fields) and behaviors (methods) from a **superclass** (parent class). This feature promotes **code reuse**, **polymorphism**, and **extensibility**.

---

### Key Benefits of Inheritance:
1. **Code Reusability**: Common functionality can be placed in a superclass to avoid repetition.
2. **Polymorphism**: Inheritance enables method overriding, allowing subclasses to have different behaviors for methods defined in the superclass.
3. **Extensibility**: Inheritance supports scalability, allowing new classes to build on existing ones for easier code maintenance.

---

### Example Code:

```java
// Base class
class Vehicle {
    double speed;
    
    public void go() {
        System.out.println("The vehicle is moving.");
    }
    
    public void stop() {
        System.out.println("The vehicle has stopped.");
    }
}

// Derived class
class Car extends Vehicle {
    int doors = 4;
}

class Bicycle extends Vehicle {
    int pedals = 2;
}

public class Main {
    public static void main(String[] args) {
        // Creating Car object
        Car car = new Car();
        car.go();  // Inherited method from Vehicle
        System.out.println("Car has " + car.doors + " doors.");
        
        // Creating Bicycle object
        Bicycle bike = new Bicycle();
        bike.stop();  // Inherited method from Vehicle
        System.out.println("Bicycle has " + bike.pedals + " pedals.");
    }
}
```

**Output**:
```
The vehicle is moving.
Car has 4 doors.
The vehicle has stopped.
Bicycle has 2 pedals.
```

---

### Key Terminology:
- **Class**: A blueprint from which objects are created, containing data and methods.
- **Super Class**: The parent class from which other classes inherit.
- **Sub Class**: The child class that inherits properties and methods from the superclass.
- **`extends` Keyword**: Indicates that a class is inheriting from another class.

**Syntax**:
```java
class SubClass extends SuperClass {
    // Additional fields and methods
}
```

---

### Practical Uses:
1. **Code Reusability**: Common properties like speed in vehicles can be shared between subclasses like cars and bikes, reducing redundancy.
2. **Overriding Methods**: Subclasses can modify the behavior of a method inherited from the superclass to suit their specific needs.

---

### Example 2: Multi-Level Inheritance

```java
// Base class
class Animal {
    void sound() {
        System.out.println("Animal makes a sound");
    }
}

// Derived class
class Dog extends Animal {
    void sound() {
        System.out.println("Dog barks");
    }
}

// Further Derived class
class Puppy extends Dog {
    void sound() {
        System.out.println("Puppy yaps");
    }
}

public class Main {
    public static void main(String[] args) {
        Puppy puppy = new Puppy();
        puppy.sound();  // Output: Puppy yaps
    }
}
```

---

### Common Pitfalls:
- **Deep inheritance hierarchies** can make code hard to maintain. It's best to limit inheritance levels.
- **Method hiding**: Always use `@Override` when overriding methods to avoid accidental hiding of methods from the superclass.

---

### Example: Bicycle and MountainBike

```java
// Base class
class Bicycle {
    public int gear;
    public int speed;

    public Bicycle(int gear, int speed) {
        this.gear = gear;
        this.speed = speed;
    }

    public void applyBrake(int decrement) {
        speed -= decrement;
    }

    public void speedUp(int increment) {
        speed += increment;
    }

    @Override
    public String toString() {
        return "No of gears: " + gear + "\nSpeed: " + speed;
    }
}

// Derived class
class MountainBike extends Bicycle {
    public int seatHeight;

    public MountainBike(int gear, int speed, int startHeight) {
        super(gear, speed);
        this.seatHeight = startHeight;
    }

    public void setHeight(int newValue) {
        seatHeight = newValue;
    }

    @Override
    public String toString() {
        return super.toString() + "\nSeat height: " + seatHeight;
    }
}

// Driver class
public class Test {
    public static void main(String[] args) {
        MountainBike mb = new MountainBike(3, 100, 25);
        System.out.println(mb.toString());
    }
}
```

**Output**:
```
No of gears: 3
Speed: 100
Seat height: 25
```

---

### Types of Inheritance in Java:
1. **Single Inheritance**: A subclass inherits from one superclass.
2. **Multilevel Inheritance**: A subclass inherits from another subclass.
3. **Hierarchical Inheritance**: Multiple subclasses inherit from the same superclass.
4. **Multiple Inheritance**: Achieved through interfaces in Java.
5. **Hybrid Inheritance**: A combination of single, multiple, and hierarchical inheritance, using interfaces.

### Example: Single Inheritance

```java
class One {
    public void printMessage() {
        System.out.println("Geeks");
    }
}

class Two extends One {
    public void printFor() {
        System.out.println("for");
    }
}

public class Main {
    public static void main(String[] args) {
        Two g = new Two();
        g.printMessage();
        g.printFor();
    }
}
```

**Output**:
```
Geeks
for
```

---

### Java Inheritance Relationships:

The **IS-A** relationship defines inheritance, where one class is a type of another. For example:

```java
class SolarSystem {}
class Earth extends SolarSystem {}
class Mars extends SolarSystem {}
class Moon extends Earth {}
```

- **SolarSystem** is the superclass of **Earth** and **Mars**.
- **Earth** is a subclass of **SolarSystem** and a superclass of **Moon**.

---

### Advantages of Inheritance:
- **Code Reusability**: Reduces redundancy and promotes cleaner code.
- **Abstraction**: Provides a level of abstraction where subclasses implement specific details.
- **Polymorphism**: Allows objects to take multiple forms.
- **Class Hierarchy**: Mimics real-world hierarchical structures.

### Disadvantages of Inheritance:
- **Complexity**: Deep inheritance hierarchies can make code harder to understand and maintain.
- **Tight Coupling**: Changes to a superclass can inadvertently affect all subclasses.

---

### Key Points:
- All classes have one direct superclass, except `Object`, which is the root class in Java.
- A subclass inherits methods and fields but not constructors from the superclass.
- **Private members** of a superclass are not inherited but can be accessed through public or protected methods.

---

### Tips and Tricks:
1. **DRY Principle**: Use inheritance to avoid code repetition across classes with common behaviors.
2. **Method Overriding**: Subclasses can customize behavior by overriding superclass methods.
3. **Constructor Calls**: Use `super()` to invoke the superclass constructor from the subclass constructor.
4. **Avoid Overusing Inheritance**: Only use inheritance when there's a clear **"is-a"** relationship. If not, consider composition instead.

---

This unified note should give you a comprehensive understanding of Java inheritance, including examples, practical uses, and common pitfalls!