---
sources:
  - "12.pdf"
  - "3.pdf"
  - "4.pdf"
---
> [!question] True or False: Polymorphism in Java allows static methods to be dynamically bound at runtime, enabling different implementations based on the actual object type.
>> [!success]- Answer
>> False

> [!question] True or False: When an object is upcasted, the compiler restricts access to subclass-specific methods, but at runtime, the dynamically bound method will always be the one from the actual object's type.
>> [!success]- Answer
>> True

> [!question] Which of the following best defines polymorphism in the context of Object-Oriented Programming in Java?
> a) The ability of a class to inherit properties and behaviors from multiple parent classes.
> b) The mechanism of bundling data and methods into a single unit, controlling access.
> c) The capacity to perceive an object as an instance of various classes, dynamically choosing the method corresponding to its real type.
> d) The process of converting a superclass reference to a subclass reference explicitly.
>> [!success]- Answer
>> c) The capacity to perceive an object as an instance of various classes, dynamically choosing the method corresponding to its real type.

> [!question] Consider the following code:
> ```java
> class A { void display() { System.out.println("Class A"); } }
> class B extends A { void display() { System.out.println("Class B"); } }
>
> public class Test {
>     public static void main(String[] args) {
>         A obj = new B();
>         obj.display();
>     }
> }
> ```
> What is the output of this program, and what principle does it demonstrate?
> a) "Class A"; demonstrates static binding.
> b) "Class B"; demonstrates dynamic binding (polymorphism).
> c) "Class A"; demonstrates method hiding.
> d) "Class B"; demonstrates method overloading.
>> [!success]- Answer
>> b) "Class B"; demonstrates dynamic binding (polymorphism).

> [!question] Match the polymorphism-related concept with its characteristic.
>> [!example] Group A
>> a) Dynamic Binding
>> b) Overriding
>> c) Method Hiding
>
>> [!example] Group B
>> n) The compile-time resolution of method calls, typically for static methods.
>> o) The runtime resolution of method calls, where the actual object type determines the method executed.
>> p) A subclass providing a specific implementation for a method already defined in its superclass, with the same signature.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
