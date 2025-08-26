---
sources:
  - "12.pdf"
  - "3.pdf"
  - "4.pdf"
---
> [!question] True or False: In Java, `List<Object>` is a supertype of `List<String>`, meaning a `List<String>` can be directly assigned to a `List<Object>` variable.
>> [!success]- Answer
>> False

> [!question] True or False: Generic type parameters in Java are erased at compile time, meaning the runtime environment does not retain information about the actual type arguments.
>> [!success]- Answer
>> True

> [!question] Which of the following statements accurately describes the primary purpose of generics in Java?
> a) To allow classes to inherit from multiple parent classes.
> b) To provide runtime type safety and eliminate the need for explicit casting for collections.
> c) To enable methods to be overloaded with different return types.
> d) To define classes and methods that operate on types specified at compile time, enhancing type safety and code reusability.
>> [!success]- Answer
>> d) To define classes and methods that operate on types specified at compile time, enhancing type safety and code reusability.

> [!question] Consider a generic class `Paire<T, S>`. If you instantiate it as `Paire<Integer, String> myPair = new Paire<>(2, "Hello");`, which of the following is a valid operation?
> a) `myPair.setV1("World");`
> b) `myPair.setV2(3.14);`
> c) `Integer val1 = myPair.getV1();`
> d) `String val2 = myPair.getV1();`
>> [!success]- Answer
>> c) `Integer val1 = myPair.getV1();`

> [!question] Match the generic concept with its characteristic.
>> [!example] Group A
>> a) Generic Class
>> b) Wildcard (`?`)
>> c) Type Erasure
>
>> [!example] Group B
>> n) A mechanism where generic type information is removed during compilation, replaced with raw types.
>> o) A class whose definition is parameterized with one or more "variable" types, specified at instantiation.
>> p) Used in generic type parameters to represent an unknown type, often with bounds (`extends` or `super`).
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
