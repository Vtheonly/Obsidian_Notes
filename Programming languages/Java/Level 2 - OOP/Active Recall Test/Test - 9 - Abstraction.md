---
sources:
  - "12.pdf"
  - "3.pdf"
  - "4.pdf"
---
> [!question] True or False: An abstract class in Java must contain at least one abstract method; otherwise, it cannot be declared abstract.
>> [!success]- Answer
>> False

> [!question] True or False: It is possible to directly instantiate an abstract class in Java, provided all its abstract methods have been implemented in an anonymous inner class.
>> [!success]- Answer
>> False

> [!question] Which of the following is a fundamental characteristic of an abstract method in Java?
> a) It must provide a default implementation that can be overridden by subclasses.
> b) It is declared with the `abstract` keyword and has no method body.
> c) It can only be defined in a concrete class, not an abstract one.
> d) It can be called directly using the class name without an object instance.
>> [!success]- Answer
>> b) It is declared with the `abstract` keyword and has no method body.

> [!question] Consider a scenario where a class `Shape` is declared `abstract` and contains an abstract method `calculateArea()`. If a concrete class `Circle` extends `Shape`, what is the mandatory requirement for `Circle`?
> a) `Circle` must also be declared `abstract`.
> b) `Circle` must implement the `calculateArea()` method.
> c) `Circle` can choose to implement `calculateArea()` or not, depending on its needs.
> d) `Circle` must override all non-abstract methods from `Shape`.
>> [!success]- Answer
>> b) `Circle` must implement the `calculateArea()` method.

> [!question] Match the abstraction-related concept with its defining characteristic.
>> [!example] Group A
>> a) Abstract Class
>> b) Abstract Method
>> c) Concrete Class
>
>> [!example] Group B
>> n) A class that can be instantiated and provides full implementations for all its methods.
>> o) A class that cannot be instantiated directly and may contain unimplemented methods.
>> p) A method declared without an implementation, requiring subclasses to provide one.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
