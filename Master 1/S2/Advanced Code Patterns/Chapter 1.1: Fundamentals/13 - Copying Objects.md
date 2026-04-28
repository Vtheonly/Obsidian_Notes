
# Copying Objects in Java

## Introduction
In this video, we explore how to copy objects in Java, specifically focusing on a `Car` class. We will cover the concepts of references, memory addresses, and how to properly copy object attributes without losing the integrity of the original object.

## Class Setup
We define a `Car` class with the following features:
- **Private Variables:** `make`, `model`, and `year`
- **Constructor:** Initializes the car object and assigns values to the private variables using setter methods.
- **Getter Methods:** Retrieve the values of the private variables.

### Example Car Class
```java
public class Car {
    private String make;
    private String model;
    private int year;

    // Constructor
    public Car(String make, String model, int year) {
        setMake(make);
        setModel(model);
        setYear(year);
    }

    // Getter methods
    public String getMake() {
        return make;
    }

    public String getModel() {
        return model;
    }

    public int getYear() {
        return year;
    }

    // Setter methods
    public void setMake(String make) {
        this.make = make;
    }

    public void setModel(String model) {
        this.model = model;
    }

    public void setYear(int year) {
        this.year = year;
    }
}
```

## Creating and Printing Car Objects
In the main method, we create two `Car` objects:

```java
Car car1 = new Car("Chevy", "Camaro", 2021);
Car car2 = new Car("Ford", "Mustang", 2022);

// Print addresses and attributes
System.out.println("Car 1 Address: " + System.identityHashCode(car1));
System.out.println("Car 2 Address: " + System.identityHashCode(car2));
System.out.println("Car 1: " + car1.getMake() + " " + car1.getModel() + " " + car1.getYear());
System.out.println("Car 2: " + car2.getMake() + " " + car2.getModel() + " " + car2.getYear());
```

### Address Printing
- **Note:** Printing the addresses shows different memory locations, confirming they are distinct objects.

## Common Mistake: Direct Assignment
A common misconception is to copy objects using assignment:

```java
car2 = car1; // Wrong: Both car1 and car2 now point to the same object
```

### Why It’s Incorrect
- This does not create a new `Car` object. Instead, `car1` and `car2` refer to the same memory location. Changes to `car2` will also affect `car1`, as they are the same object.

## Creating a Copy Method
To correctly copy attributes from one object to another, we implement a copy method in the `Car` class:

### Copy Method
```java
public void copy(Car carX) {
    this.setMake(carX.getMake());
    this.setModel(carX.getModel());
    this.setYear(carX.getYear());
}
```

### Using the Copy Method
In the main method, we can now copy attributes correctly:

```java
car2.copy(car1); // car2 now has the same attributes as car1
```

## Copy Constructor
For instantiation, we can create a copy constructor:

### Copy Constructor Implementation
```java
public Car(Car carX) {
    this.copy(carX);
}
```

### Creating a New Car with the Copy Constructor
```java
Car car2 = new Car(car1); // Creates a new Car object that is a copy of car1
```

## Conclusion
- **Summary:** The video covered how to copy objects in Java through direct methods and constructors. We demonstrated common pitfalls and the correct implementation of copy methods and constructors to maintain object integrity.

If you found this helpful, please consider liking, commenting, and subscribing!

---

Feel free to modify any sections or add more details as you see fit!