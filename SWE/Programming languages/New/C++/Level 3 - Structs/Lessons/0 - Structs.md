---
title: "Structs and Classes in C++"
---

In C++, `struct` and `class` are keywords used to define your own custom data types. They are fundamental to object-oriented programming.

### Structs in C++

A `struct` (structure) is a collection of member variables and member functions. In C++, a `struct` is almost identical to a `class`.

```cpp
#include <iostream>
#include <string>

struct Point {
    // Member variables
    double x;
    double y;

    // Member function (method)
    void print() {
        std::cout << "Point(" << x << ", " << y << ")" << std::endl;
    }
};

int main() {
    // Create an instance of the Point struct
    Point p1;
    p1.x = 10.0;
    p1.y = 20.0;
    p1.print(); // Output: Point(10, 20)

    // Using an initializer list
    Point p2 = {5.0, -3.0};
    p2.print(); // Output: Point(5, -3)

    return 0;
}
```

### Member Access Operators

There are two operators used to access the members (variables and functions) of a `struct` or `class`.

1.  **Dot Operator (`.`):** Used to access members of an object directly.

    ```cpp
    Point my_point;
    my_point.x = 42.0;
    ```

2.  **Arrow Operator (`->`):** Used to access members of an object through a pointer. It is syntactic sugar for dereferencing the pointer first and then using the dot operator.

    ```cpp
    Point* point_ptr = new Point{1.0, 2.0};

    // The arrow operator is clean and clear
    point_ptr->print(); // Output: Point(1, 2)

    // This is what it is shorthand for:
    (*point_ptr).print();

    delete point_ptr; // Don't forget to free the memory!
    ```

    **Modern C++ Note:** It is highly recommended to use smart pointers like `std::unique_ptr` or `std::shared_ptr` to manage dynamically allocated objects to prevent memory leaks.

    ```cpp
    #include <memory>

    std::unique_ptr<Point> smart_ptr = std::make_unique<Point>();
    smart_ptr->x = 100;
    smart_ptr->print();
    // No `delete` needed! Memory is managed automatically.
    ```

### `struct` vs. `class`

In C++, the only technical difference between a `struct` and a `class` is the **default member access specifier**:

-   **`struct`**: Members are `public` by default.
-   **`class`**: Members are `private` by default.

```cpp
struct MyStruct {
    int x; // This is public
};

class MyClass {
    int y; // This is private
public:
    int z; // This is public
};

int main() {
    MyStruct s;
    s.x = 10; // OK

    MyClass c;
    // c.y = 20; // Error: y is private
    c.z = 30; // OK
    return 0;
}
```

**Convention and Style**

By convention, C++ programmers often use:

-   **`struct`** for Plain Old Data (POD) types, which are simple data aggregates with few or no member functions and where all members are public.
-   **`class`** for more complex types that have private data, invariants to maintain, and a public interface (member functions) to interact with that data. This is the essence of **encapsulation**.

### Conclusion

Structs and classes are the building blocks of object-oriented programming in C++. They allow you to create complex, user-defined types that bundle data and behavior together. While they are technically very similar, the choice between them is often guided by convention to signal the intended use of the type.
