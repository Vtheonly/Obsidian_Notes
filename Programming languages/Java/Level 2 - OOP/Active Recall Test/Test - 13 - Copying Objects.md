---
sources:
  - "12.pdf"
  - "3.pdf"
  - "4.pdf"
---
> [!question] True or False: Assigning one object reference to another (e.g., `obj2 = obj1;`) creates a deep copy of the object, meaning `obj2` will be an independent duplicate of `obj1`.
>> [!success]- Answer
>> False

> [!question] True or False: Implementing the `Cloneable` interface and overriding the `clone()` method guarantees a deep copy of an object, including all its nested objects.
>> [!success]- Answer
>> False

> [!question] Which of the following is the primary issue with simply assigning one object reference to another when attempting to "copy" an object in Java?
> a) It creates a new object with identical attribute values but a different memory address.
> b) It results in a compile-time error because objects cannot be directly assigned.
> c) It creates an alias, where both references point to the same object in memory, leading to shared state.
> d) It performs a shallow copy, duplicating primitive fields but not object references.
>> [!success]- Answer
>> c) It creates an alias, where both references point to the same object in memory, leading to shared state.

> [!question] To achieve a deep copy of an object in Java, which of the following approaches is generally recommended and discussed in the context?
> a) Directly assigning object references using the `=` operator.
> b) Implementing the `Cloneable` interface and ensuring the `clone()` method recursively copies all mutable object fields.
> c) Relying on the default behavior of the `Object.clone()` method without any modifications.
> d) Using a custom `copy()` method that only duplicates primitive fields.
>> [!success]- Answer
>> b) Implementing the `Cloneable` interface and ensuring the `clone()` method recursively copies all mutable object fields.

> [!question] Match the copying concept with its description.
>> [!example] Group A
>> a) Shallow Copy
>> b) Deep Copy
>> c) `Cloneable` interface
>
>> [!example] Group B
>> n) A marker interface indicating that a class permits cloning, requiring the `clone()` method to be overridden.
>> o) A copy where new objects are created for all fields, including nested objects, ensuring complete independence.
>> p) A copy where a new object is created, but its fields that are object references still point to the same objects as the original.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)
