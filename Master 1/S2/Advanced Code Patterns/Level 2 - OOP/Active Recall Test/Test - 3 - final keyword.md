---
sources:
  - "12.pdf"
  - "3.pdf"
  - "4.pdf"
---
> [!question] True or False: A `final` variable in Java must be initialized at the point of declaration; it cannot be assigned a value later in the constructor or an initializer block.
>> [!success]- Answer
>> False

> [!question] True or False: Declaring a method as `final` prevents any subclass from overriding that specific method, but it does not prevent method overloading within the same class or subclasses.
>> [!success]- Answer
>> True

> [!question] Which of the following is a correct application of the `final` keyword in Java, according to the provided context?
> a) `final class MyClass extends AnotherClass {}`
> b) `public final void myMethod() { /* ... */ }`
> c) `final int MY_CONSTANT; MY_CONSTANT = 10;` (if `MY_CONSTANT` is a class member and initialized once)
> d) All of the above.
>> [!success]- Answer
>> d) All of the above.

> [!question] If a class is declared as `final`, what are the implications for its extensibility and the behavior of its methods?
> a) Its methods can still be overridden by subclasses, but new methods cannot be added.
> b) It cannot be inherited by any other class, and all its methods are implicitly `final`.
> c) It can be inherited, but only if the subclass also declares itself as `final`.
> d) Only its static methods become `final`, while instance methods remain overridable.
>> [!success]- Answer
>> b) It cannot be inherited by any other class, and all its methods are implicitly `final`.

> [!question] Match the `final` keyword usage with its effect.
>> [!example] Group A
>> a) `final` on a variable
>> b) `final` on a method
>> c) `final` on a class
>
>> [!example] Group B
>> n) Prevents any other class from inheriting from this class.
>> o) Ensures the variable's value can be assigned only once.
>> p) Prohibits subclasses from overriding this specific method.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
