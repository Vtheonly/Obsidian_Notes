---
sources:
  - "12.pdf"
  - "3.pdf"
  - "4.pdf"
---
> [!question] True or False: The `super` keyword can be used to call a superclass's constructor at any point within a subclass's constructor, as long as it's before any other statements.
>> [!success]- Answer
>> False

> [!question] True or False: When a subclass method overrides a superclass method, `super.methodName()` can be used to explicitly invoke the superclass's implementation from within the overriding method.
>> [!success]- Answer
>> True

> [!question] Which of the following is a mandatory rule when using `super(...)` to invoke a superclass constructor from a subclass constructor?
> a) It must be the last statement in the subclass constructor.
> b) It can only be used if the superclass has a no-argument constructor.
> c) It must be the first statement in the subclass constructor.
> d) It is optional if the superclass has a default constructor.
>> [!success]- Answer
>> c) It must be the first statement in the subclass constructor.

> [!question] Consider a scenario where a subclass `B` extends `A`, and both have a field named `value`. If `B`'s method needs to access `A`'s `value` field, how can it be explicitly referenced?
> a) `this.value`
> b) `super.value`
> c) `A.value`
> d) `B.value`
>> [!success]- Answer
>> b) `super.value`

> [!question] Match the `super` keyword usage with its purpose.
>> [!example] Group A
>> a) `super()`
>> b) `super.method()`
>> c) `super.field`
>
>> [!example] Group B
>> n) To explicitly invoke a superclass's constructor.
>> o) To access a superclass's field that is masked by a subclass's field of the same name.
>> p) To call an overridden method from the superclass within a subclass's method.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)
