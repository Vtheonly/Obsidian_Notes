---
title: "Key C++ Features Reference Card"
---

This card highlights features that are central to C++ and distinguish it from C.

### Console & File I/O Streams

C++ uses a stream-based model for I/O, found in `<iostream>` and `<fstream>`.

```cpp
#include <iostream>
#include <fstream>
#include <string>

// Console I/O
std::string name;
std::cout << "Enter name: ";
std::getline(std::cin, name);
std::cout << "Hello, " << name << std::endl;

// File I/O
std::ofstream outFile("output.txt");
outFile << "This is some data.";
outFile.close();

std::ifstream inFile("output.txt");
std::string line;
std::getline(inFile, line);
std::cout << line << std::endl;
inFile.close();
```

### Classes and Objects

Classes are the cornerstone of Object-Oriented Programming in C++.

```cpp
class Square {
public:
    // Constructor with member initializer list
    Square(float w) : width(w) {}

    void setWidth(float w) {
        if (w >= 0) width = w;
    }

    float getArea() const { // const-correctness
        return width * width;
    }

private:
    float width;
};

// Usage
Square s1(3.5f);
std::cout << s1.getArea() << std::endl;

// Dynamic allocation with smart pointers
#include <memory>
auto sPtr = std::make_unique<Square>(1.8f);
std::cout << sPtr->getArea() << std::endl;
```

### Inheritance

Inheritance allows creating new classes from existing ones.

```cpp
class Student {
public:
    Student(std::string n, std::string id) : name(n), netID(id) {}
    virtual void print() const { // virtual for polymorphism
        std::cout << "Name: " << name << ", ID: " << netID;
    }
protected:
    std::string name;
    std::string netID;
};

class GradStudent : public Student {
public:
    GradStudent(std::string n, std::string id, std::string prev)
        : Student(n, id), prevDegree(prev) {}

    void print() const override { // override for safety
        Student::print();
        std::cout << ", Previous Degree: " << prevDegree;
    }
private:
    std::string prevDegree;
};
```

### Operator Overloading

Customizes operators for user-defined types.

```cpp
class Complex {
public:
    Complex(double r = 0, double i = 0) : real(r), imag(i) {}

    Complex operator+(const Complex& other) const {
        return Complex(real + other.real, imag + other.imag);
    }
private:
    double real, imag;
};

// Usage
Complex a(1, 2), b(3, 4);
Complex c = a + b; // Uses overloaded operator+
```

### Exception Handling

Provides a standard way to handle runtime errors.

```cpp
#include <stdexcept>

double divide(double a, double b) {
    if (b == 0) {
        throw std::runtime_error("Division by zero!");
    }
    return a / b;
}

try {
    double result = divide(10, 0);
} catch (const std::exception& e) {
    std::cerr << "Error: " << e.what() << std::endl;
}
```

### Templates (Generic Programming)

Templates allow writing code that works with any type.

**Function Template:**
```cpp
template <typename T>
T getMax(T a, T b) {
    return (a > b) ? a : b;
}

int max_i = getMax(3, 7);
double max_d = getMax(3.14, 2.71);
```

**Class Template:**
```cpp
template <typename T>
class Point {
public:
    Point(T x, T y) : x_coord(x), y_coord(y) {}
private:
    T x_coord, y_coord;
};

Point<int> p1(1, 2);
Point<double> p2(1.5, 2.5);
```

### The Standard Template Library (STL)

The STL is a collection of powerful and efficient generic containers, algorithms, and iterators.

-   **Containers**: `std::vector`, `std::list`, `std::map`, `std::set`, `std::string`
-   **Algorithms**: `std::sort`, `std::find`, `std::copy`, `std::transform`
-   **Iterators**: Provide a uniform way to access elements in containers.

```cpp
#include <vector>
#include <algorithm>

std::vector<int> v = {5, 1, 4, 2, 3};
std::sort(v.begin(), v.end()); // Sorts the vector

for(int i : v) { // Range-based for loop
    std::cout << i << " ";
}
```

### Lambdas (C++11)

Anonymous, in-place functions that are extremely useful with STL algorithms.

```cpp
#include <vector>
#include <algorithm>

std::vector<int> v = {1, 2, 3, 4, 5, 6};

// Count even numbers using a lambda
int even_count = std::count_if(v.begin(), v.end(), [](int n) {
    return n % 2 == 0;
});

std::cout << "Even numbers: " << even_count << std::endl;
```
