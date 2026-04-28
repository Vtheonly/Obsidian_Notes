---
sources:
  - "12.pdf"
  - "3.pdf"
  - "4.pdf"
---
> [!question] True or False: In Java, if a class defines at least one explicit constructor, the compiler will still automatically provide a default no-argument constructor.
>> [!success]- Answer
>> False

> [!question] True or False: The `finalize()` method is guaranteed to be called by the Garbage Collector immediately before an object is destroyed, making it a reliable place for resource cleanup.
>> [!success]- Answer
>> False

> [!question] Which of the following accurately describes the role and characteristics of a constructor in Java?
> a) It is a method that returns a value, typically the newly created object's reference.
> b) Its primary purpose is to define the behaviors an object can perform.
> c) It is a special method with the same name as its class, executed during object creation to initialize its state.
> d) It can be called explicitly by the programmer at any point during an object's lifecycle to re-initialize it.
>> [!success]- Answer
>> c) It is a special method with the same name as its class, executed during object creation to initialize its state.

> [!question] Consider the three steps triggered by the `new` keyword during object creation. Which of these steps is responsible for making the object accessible via a reference?
> a) Creation of a memory zone to contain attributes.
> b) Initialization of attributes to their default or specified values.
> c) Execution of the constructor method.
> d) Returning the reference (address) of the allocated memory zone.
>> [!success]- Answer
>> d) Returning the reference (address) of the allocated memory zone.

> [!question] Match the term related to object lifecycle management with its description.
>> [!example] Group A
>> a) Constructor Overloading
>> b) Garbage Collector
>> c) `this(...)`
>
>> [!example] Group B
>> n) Mechanism for automatically reclaiming memory occupied by unreferenced objects.
>> o) Allowing multiple constructors in a class with different parameter lists.
>> p) Used within a constructor to call another constructor in the same class.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)
