---
sources:
  - "12.pdf"
  - "3.pdf"
  - "4.pdf"
---
> [!question] True or False: Upcasting in Java is an explicit operation that requires a cast operator, similar to how primitive types are converted to a larger type.
>> [!success]- Answer
>> False

> [!question] True or False: When an object is upcasted, its actual runtime type changes to the superclass type, thereby losing access to any subclass-specific methods.
>> [!success]- Answer
>> False

> [!question] Consider the following Java code snippet:
> ```java
> class Animal { void makeSound() { System.out.println("Animal sound"); } }
> class Dog extends Animal { void makeSound() { System.out.println("Woof"); } void fetch() { System.out.println("Fetching"); } }
>
> public class Test {
>     public static void main(String[] args) {
>         Animal myAnimal = new Dog();
>         myAnimal.makeSound();
>         // myAnimal.fetch(); // Line X
>     }
> }
> ```
> What is the output of `myAnimal.makeSound();` and what happens at `Line X`?
> a) "Animal sound"; Line X compiles and runs, printing "Fetching".
> b) "Woof"; Line X results in a compile-time error.
> c) "Animal sound"; Line X results in a runtime error.
> d) "Woof"; Line X compiles but results in a runtime error.
>> [!success]- Answer
>> b) "Woof"; Line X results in a compile-time error.

> [!question] Which of the following scenarios correctly demonstrates a valid and safe use of downcasting in Java?
> a) `Object obj = new String("hello"); String str = (String) obj;`
> b) `Animal animal = new Animal(); Dog dog = (Dog) animal;` (where `Dog` extends `Animal`)
> c) `List<Object> list = new ArrayList<String>(); ArrayList<String> specificList = (ArrayList<String>) list;`
> d) `Number num = Integer.valueOf(10); Double dbl = (Double) num;`
>> [!success]- Answer
>> a) `Object obj = new String("hello"); String str = (String) obj;`

> [!question] Match the casting operation with its primary characteristic.
>> [!example] Group A
>> a) Upcasting
>> b) Downcasting
>> c) `instanceof`
>
>> [!example] Group B
>> n) An explicit type conversion that attempts to treat a superclass reference as a subclass reference.
>> o) An implicit type conversion where a subclass instance is assigned to a superclass reference.
>> p) A keyword used to check if an object is an instance of a particular class or an interface.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)
