### Class

- **Definition:**
  - A class serves as a blueprint or a template for creating objects. It encapsulates the attributes (properties) and behaviors (methods) that define the objects instantiated from it.

- **Syntax:**
  ```java
  public class MyClass {
      // Attributes (variables)
      int myAttribute;

      // Methods
      void myMethod() {
          // Code for the method
      }
  }
  ```
  - In this example, `MyClass` is a class with an attribute `myAttribute` and a method `myMethod()`.

### Object

- **Definition:**
  - An object is an instance of a class, representing a specific entity with defined attributes and behaviors. Objects are the actual entities that interact in your program, following the structure laid out by their respective classes.

- **Creating an Object:**
  ```java
  // Creating an object of MyClass
  MyClass myObject = new MyClass();
  ```
  - Here, `myObject` is an instance of `MyClass`, created using the `new` keyword.

### Attributes (Variables)

- **Definition:**
  - Attributes are variables that store the state or properties of an object. Each object can have its own unique set of attribute values.

- **Accessing Attributes:**
  ```java
  // Setting the value of an attribute
  myObject.myAttribute = 42;

  // Accessing the value of an attribute
  int value = myObject.myAttribute;
  ```
  - Attributes of an object can be accessed and modified using the dot (`.`) operator.

### Methods

- **Definition:**
  - Methods are functions defined inside a class that dictate the behaviors or actions that objects of the class can perform.

- **Calling Methods:**
  ```java
  // Calling a method
  myObject.myMethod();
  ```
  - To invoke a method on an object, use the dot (`.`) operator followed by the method name.

### Constructor

- **Definition:**
  - A constructor is a special method used to initialize objects of a class. It sets up the initial state of an object when it is created.

- **Syntax:**
  ```java
  public class MyClass {
      // Constructor
      public MyClass() {
          // Initialization code
      }
  }
  ```
  - Constructors have the same name as the class and no return type. They are automatically called when an object is instantiated.
  - One of the important property of java constructor is that **it can not be static**. We know static keyword belongs to a class rather than the object of a class. A constructor is called when an object of a class is created, so no use of the static constructor.

- **Creating an Object with Constructor:**
  ```java
  // Creating an object with a constructor
  MyClass myObject = new MyClass();
  ```
  - In this example, the constructor `MyClass()` initializes `myObject`.

### Encapsulation

- **Definition:**
  - Encapsulation is the practice of bundling the data (attributes) and the methods that manipulate that data within a single unit or class. It also involves restricting access to some of the object's components to protect the integrity of the object's state.

- **Access Modifiers:**
  - Access modifiers like `public`, `private`, and `protected` control the visibility of class members. For example:
  ```java
  public class MyClass {
      private int myAttribute; // Private attribute

      public void setAttribute(int value) {
          myAttribute = value;
      }

      public int getAttribute() {
          return myAttribute;
      }
  }
  ```
  - Here, `myAttribute` is private, meaning it can only be accessed through the public methods `setAttribute` and `getAttribute`.

### Inheritance

- **Definition:**
  - Inheritance allows one class (the subclass) to inherit fields and methods from another class (the superclass). This promotes code reuse and establishes a relationship between the classes.

- **Syntax:**
  ```java
  // Subclass inheriting from a superclass
  public class MySubClass extends MyClass {
      // Additional attributes and methods for the subclass
  }
  ```
  - `MySubClass` inherits from `MyClass`, meaning it can use the attributes and methods of `MyClass`, while also defining its own additional features.



### Polymorphism

- **Definition:**
  - Polymorphism is the ability of objects of different classes to be treated as objects of a common superclass. It allows one interface to be used for a general class of actions, with specific actions being determined by the exact nature of the object that is being acted upon.

- **Types of Polymorphism:**
  - **Compile-time Polymorphism (Method Overloading):**
    - Achieved by defining multiple methods with the same name but different parameters within the same class.
    - Example:
      ```java
      public class MyClass {
          void display(int a) {
              System.out.println("Integer: " + a);
          }

          void display(String b) {
              System.out.println("String: " + b);
          }
      }
      ```

  - **Runtime Polymorphism (Method Overriding):**
    - Achieved when a subclass provides a specific implementation of a method that is already defined in its superclass.
    - Example:
      ```java
      class Animal {
          void sound() {
              System.out.println("Animal makes a sound");
          }
      }

      class Dog extends Animal {
          @Override
          void sound() {
              System.out.println("Dog barks");
          }
      }
      ``` 
      - Here, `Dog` overrides the `sound()` method of the `Animal` class.

- **Benefits:**
  - Polymorphism enhances flexibility and maintainability in code by allowing methods to work with objects of different types, enabling developers to write more generic and reusable code.
---

These core concepts—classes, objects, attributes, methods, constructors, encapsulation, and inheritance—lay the foundation for object-oriented programming in Java. As you delve deeper into Java, you'll explore more complex features that build on these basics, enabling you to create sophisticated and scalable applications.



### Abstraction

- **Definition:**
  - Abstraction is the concept of hiding the complex implementation details of a system and exposing only the essential features to the user. It focuses on what an object does rather than how it does it.

- **Purpose:**
  - The main purpose of abstraction is to reduce complexity by allowing the user to interact with the object at a high level without needing to understand the intricate details of its internal workings.

- **How to Achieve Abstraction:**
  - **Abstract Classes:**
    - An abstract class is a class that cannot be instantiated on its own and is meant to be subclassed. It can have both abstract methods (without implementation) and concrete methods (with implementation).
    - Example:
      ```java
      abstract class Animal {
          abstract void sound();  // Abstract method

          void sleep() {          // Concrete method
              System.out.println("Animal is sleeping");
          }
      }
      ```

  - **Interfaces:**
    - An interface is a contract that defines a set of methods that a class must implement. It provides a way to achieve abstraction and multiple inheritance.
    - Example:
      ```java
      interface Movable {
          void move();  // Abstract method
      }

      class Car implements Movable {
          public void move() {
              System.out.println("Car is moving");
          }
      }
      ```

- **Benefits:**
  - Abstraction simplifies the interaction with objects by providing a clear and simplified interface, making it easier to manage and maintain code. It also allows for flexibility in the implementation, as the internal details can be changed without affecting the user's interaction with the object.