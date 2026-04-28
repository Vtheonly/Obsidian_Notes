---
sources:
  - "12.pdf"
  - "3.pdf"
  - "4.pdf"
---
> [!question] True or False: An interface in Java can contain both abstract methods and concrete methods with default implementations.
>> [!success]- Answer
>> False

> [!question] True or False: A class can implement multiple interfaces but can only extend one abstract class in Java.
>> [!success]- Answer
>> True

> [!question] Which of the following statements accurately describes a key characteristic of interfaces in Java?
> a) Interfaces can be directly instantiated to create objects.
> b) Interfaces can define instance variables (non-static, non-final).
> c) All methods declared in an interface are implicitly `public` and `abstract` (prior to Java 8 default/static methods).
> d) A class implementing an interface is only required to implement a subset of its methods.
>> [!success]- Answer
>> c) All methods declared in an interface are implicitly `public` and `abstract` (prior to Java 8 default/static methods).

> [!question] Consider an interface `Flyable` with a method `fly()`. If a class `Bird` implements `Flyable`, and another class `Airplane` also implements `Flyable`, what is the implication for these classes?
> a) Both `Bird` and `Airplane` must extend a common abstract class that defines `fly()`.
> b) Both `Bird` and `Airplane` must provide their own concrete implementation for the `fly()` method.
> c) `Bird` and `Airplane` can choose to implement `fly()` or not, as it's optional.
> d) Only one class can implement `Flyable` at a time to avoid conflicts.
>> [!success]- Answer
>> b) Both `Bird` and `Airplane` must provide their own concrete implementation for the `fly()` method.

> [!question] Match the interface-related concept with its defining characteristic.
>> [!example] Group A
>> a) `implements` keyword
>> b) Interface Inheritance
>> c) `Cloneable` interface
>
>> [!example] Group B
>> n) Used by a class to declare that it will provide implementations for all abstract methods defined in one or more interfaces.
>> o) A marker interface that indicates a class can be duplicated, requiring the class to override the `clone()` method.
>> p) Allows an interface to extend another interface, inheriting its method signatures.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)
