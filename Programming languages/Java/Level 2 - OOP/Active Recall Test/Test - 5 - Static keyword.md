---
sources:
  - "12.pdf"
  - "3.pdf"
  - "4.pdf"
---
> [!question] True or False: A `static` method in Java can directly access and modify non-static instance variables of the same class without needing an object instance.
>> [!success]- Answer
>> False

> [!question] True or False: `static` methods can be overridden in subclasses, exhibiting polymorphic behavior similar to instance methods.
>> [!success]- Answer
>> False

> [!question] Which of the following statements correctly describes a characteristic of `static` attributes (class variables) in Java?
> a) Each object instance of the class maintains its own copy of the `static` attribute.
> b) `static` attributes are initialized only when the first object of the class is created.
> c) `static` attributes are shared across all instances of a class and can be accessed directly via the class name.
> d) `static` attributes can only be declared within methods, limiting their scope.
>> [!success]- Answer
>> c) `static` attributes are shared across all instances of a class and can be accessed directly via the class name.

> [!question] Consider a `static` method. Which of the following is a valid operation within such a method?
> a) Using the `this` keyword to refer to the current object.
> b) Calling a non-static instance method of the same class directly.
> c) Accessing a `static` attribute of the same class.
> d) Overriding a `static` method from a superclass.
>> [!success]- Answer
>> c) Accessing a `static` attribute of the same class.

> [!question] Match the `static` keyword usage with its implication.
>> [!example] Group A
>> a) `static` attribute
>> b) `static` method
>> c) `static` in `main` method signature
>
>> [!example] Group B
>> n) Allows the method to be executed without an object instance, serving as an entry point for programs.
>> o) Represents a piece of data that belongs to the class itself, rather than to any specific object.
>> p) A function that operates independently of any particular object and cannot access instance-specific data.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
