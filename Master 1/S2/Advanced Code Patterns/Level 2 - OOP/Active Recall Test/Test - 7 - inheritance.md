---
sources:
  - "12.pdf"
  - "3.pdf"
  - "4.pdf"
---
> [!question] True or False: In Java, a subclass can directly access `private` members of its superclass because inheritance implies full visibility of all parent members.
>> [!success]- Answer
>> False

> [!question] True or False: Java supports multiple inheritance, allowing a class to extend more than one superclass simultaneously, similar to C++.
>> [!success]- Answer
>> False

> [!question] Which of the following statements accurately describes the relationship between a superclass and a subclass in Java inheritance?
> a) A subclass is a more general form of its superclass, abstracting common behaviors.
> b) An object of a subclass is also considered an object of its superclass, inheriting its attributes and methods.
> c) A superclass can directly access the specific attributes and methods defined only in its subclasses.
> d) Inheritance primarily serves to hide the implementation details of the superclass from the subclass.
>> [!success]- Answer
>> b) An object of a subclass is also considered an object of its superclass, inheriting its attributes and methods.

> [!question] When a field in a subclass has the same name as a field in its superclass, what is the default behavior when accessing that field from within the subclass's code?
> a) It results in a compile-time error due to ambiguity.
> b) The subclass's field masks the superclass's field, and the subclass's field is accessed.
> c) The superclass's field is accessed by default, requiring `this` to access the subclass's field.
> d) Both fields are accessed simultaneously, leading to a merged value.
>> [!success]- Answer
>> b) The subclass's field masks the superclass's field, and the subclass's field is accessed.

> [!question] Match the inheritance-related term with its correct description.
>> [!example] Group A
>> a) Superclass
>> b) Subclass
>> c) `@Override`
>
>> [!example] Group B
>> n) A class that extends another class, inheriting its members and potentially adding new ones.
>> o) An annotation used to indicate that a method is intended to override a method in a superclass.
>> p) A class from which other classes inherit attributes and methods, also known as a parent class.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)
