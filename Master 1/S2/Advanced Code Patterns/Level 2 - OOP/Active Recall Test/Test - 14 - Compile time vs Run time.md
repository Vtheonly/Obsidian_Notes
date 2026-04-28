---
sources:
  - "12.pdf"
  - "3.pdf"
  - "4.pdf"
---
> [!question] True or False: In Java, the resolution of static method calls (method hiding) is determined at compile time, not runtime, regardless of the object's actual type.
>> [!success]- Answer
>> True

> [!question] True or False: Type checking for method invocations on an upcasted object is performed exclusively at runtime to ensure compatibility with the actual object type.
>> [!success]- Answer
>> False

> [!question] Which of the following concepts is primarily resolved at **compile time** in Java?
> a) Dynamic binding of instance methods.
> b) The actual type of an object referenced by a superclass variable.
> c) Method overloading resolution based on argument types and number.
> d) `ClassCastException` during downcasting.
>> [!success]- Answer
>> c) Method overloading resolution based on argument types and number.

> [!question] Consider the following code:
> ```java
> class Base {
>     static void show() { System.out.println("Base static"); }
>     void print() { System.out.println("Base instance"); }
> }
> class Derived extends Base {
>     static void show() { System.out.println("Derived static"); }
>     void print() { System.out.println("Derived instance"); }
> }
>
> public class Main {
>     public static void main(String[] args) {
>         Base obj = new Derived();
>         obj.show();
>         obj.print();
>     }
> }
> ```
> What will be the output of this program?
> a) "Derived static", "Derived instance"
> b) "Base static", "Base instance"
> c) "Base static", "Derived instance"
> d) "Derived static", "Base instance"
>> [!success]- Answer
>> c) "Base static", "Derived instance"

> [!question] Match the event with when it is primarily resolved or determined.
>> [!example] Group A
>> a) Method Overloading
>> b) Method Overriding (Dynamic Binding)
>> c) `final` keyword enforcement
>
>> [!example] Group B
>> n) Primarily resolved at runtime.
>> o) Primarily resolved at compile time.
>> p) Checked and enforced at compile time.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)
