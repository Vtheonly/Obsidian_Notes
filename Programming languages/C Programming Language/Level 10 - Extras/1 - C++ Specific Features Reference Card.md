### C++ Data Types

In addition to C data types, C++ introduces:

- `bool`: boolean (true or false)
- `string`: C++ string (from the STL)

### Console Input/Output

C++ introduces stream-based I/O:

```cpp
#include <iostream>
using namespace std;

int main() {
    int i;
    cout << "Enter an integer: ";
    cin >> i;
    cout << "Input: " << i << endl;
    return 0;
}
```

### File Input/Output

C++ uses stream-based file I/O:

```cpp
#include <fstream>
using namespace std;

int main() {
    // Input
    ifstream inputFile("data.txt");
    int inputVariable;
    inputFile >> inputVariable;
    inputFile.close();

    // Output
    ofstream outFile("output.txt");
    outFile << outputVariable;
    outFile.close();

    return 0;
}
```

### Classes

C++ introduces the concept of classes:

```cpp
class Square {
public:
    Square();
    Square(float w);
    void setWidth(float w);
    float getArea();
private:
    float width;
};

// Member function definitions
Square::Square() : width(0) {}

Square::Square(float w) : width(w) {}

void Square::setWidth(float w) {
    if (w >= 0)
        width = w;
    else
        exit(-1);
}

float Square::getArea() {
    return width * width;
}

// Usage
int main() {
    Square s1;
    Square s2(3.5);
    Square* sPtr = new Square(1.8);

    s1.setWidth(1.5);
    cout << s2.getArea() << endl;
    cout << sPtr->getArea() << endl;

    delete sPtr;
    return 0;
}
```

### Inheritance

C++ supports inheritance:

```cpp
class Student {
public:
    Student(string n, string id);
    void print();
protected:
    string name;
    string netID;
};

class GradStudent : public Student {
public:
    GradStudent(string n, string id, string prev);
    void print();
protected:
    string prevDegree;
};
```

### Operator Overloading

C++ allows overloading of operators:

```cpp
class Complex {
public:
    Complex(double r = 0, double i = 0) : real(r), imag(i) {}
    Complex operator+(const Complex& other) {
        return Complex(real + other.real, imag + other.imag);
    }
private:
    double real, imag;
};

// Usage
Complex a(1, 2);
Complex b(3, 4);
Complex c = a + b;  // Uses overloaded +
```

### Exceptions

C++ introduces exception handling:

```cpp
#include <iostream>
#include <stdexcept>

double divide(double a, double b) {
    if (b == 0) {
        throw std::runtime_error("Division by zero!");
    }
    return a / b;
}

int main() {
    try {
        double result = divide(10, 0);
        std::cout << "Result: " << result << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
    return 0;
}
```

### Function Templates

C++ supports function templates for generic programming:

```cpp
template <typename T>
T getMax(T a, T b) {
    return (a > b) ? a : b;
}

// Usage
int maxInt = getMax(3, 7);
double maxDouble = getMax(3.14, 2.718);
```

### Class Templates

C++ also supports class templates:

```cpp
template <typename T>
class Point {
public:
    Point(T x, T y) : x(x), y(y) {}
    void print() {
        std::cout << "(" << x << ", " << y << ")" << std::endl;
    }
private:
    T x, y;
};

// Usage
Point<int> p1(3, 2);
Point<double> p2(3.5, 2.5);
p1.print();
p2.print();
```

These C++-specific features build upon the C language, providing object-oriented programming capabilities, improved type safety, and more powerful abstractions. They allow for more flexible and maintainable code in larger software projects.