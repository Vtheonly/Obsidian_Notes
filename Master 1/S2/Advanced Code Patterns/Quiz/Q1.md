---
sources:
  - "[[Encapsulation and Access Modifiers]]"
---
> [!question] A class with default (package-private) access can be subclassed by a class in a different package.
>> [!success]- Answer
>> False

> [!question] The protected modifier provides wider access than the default (package-private) modifier.
>> [!success]- Answer
>> True

> [!question] If a variable is declared protected in class A (located in package P1), class B (located in package P2) which inherits from A can access this variable.
>> [!success]- Answer
>> True

> [!question] Java has an explicit keyword called default that is used to declare package-private access for member variables.
>> [!success]- Answer
>> False

> [!question] A private member is accessible only inside the same class file.
>> [!success]- Answer
>> True

> [!question] Encapsulation is solely about hiding data and does not involve bundling behavior.
>> [!success]- Answer
>> False

> [!question] A subclass in a different package can access a parent class's protected member, but an unrelated class in that same subclass's package cannot.
>> [!success]- Answer
>> True

> [!question] Variable shadowing occurs when a local variable has the same name as an instance variable in the same scope.
>> [!success]- Answer
>> True

> [!question] Setting a variable to package-private access prevents any other class in the same folder (package) from modifying it.
>> [!success]- Answer
>> False

> [!question] Using the "this" keyword allows a programmer to resolve ambiguity between instance variables and parameters with matching names.
>> [!success]- Answer
>> True

> [!question] Which of the following correctly orders Java access modifiers from the most restrictive to the least restrictive?
> a) private -> default -> protected -> public
> b) private -> protected -> default -> public
> c) default -> private -> protected -> public
> d) private -> default -> public -> protected
>> [!success]- Answer
>> a) private -> default -> protected -> public

> [!question] What happens if you do not specify an access modifier for a class member in Java?
> a) It becomes public.
> b) It becomes private.
> c) It becomes package-private (default).
> d) It causes a compilation error.
>> [!success]- Answer
>> c) It becomes package-private (default).

> [!question] A class Parent in package pack1 has a protected field x. A class Child in package pack2 extends Parent. Which statement is true?
> a) Child cannot access x because it is in a different package.
> b) Child can access x via inheritance.
> c) Any class in pack2 can access x by importing pack1.Parent.
> d) x is treated as private in Child.
>> [!success]- Answer
>> b) Child can access x via inheritance.

> [!question] In the cell analogy of encapsulation, what do the "gateways" correspond to?
> a) Private fields
> b) Protected fields
> c) Public methods (such as Getters and Setters)
> d) Package-private helper classes
>> [!success]- Answer
>> c) Public methods (such as Getters and Setters)

> [!question] Which keyword refers to the current object instance running the code?
> a) super
> b) parent
> c) this
> d) instance
>> [!success]- Answer
>> c) this

> [!question] Why is it considered risky to leave fields as package-private (default) by accident?
> a) It makes compilation slower.
> b) Any class in the same package can modify the fields directly, bypassing validation logic.
> c) It automatically makes the entire class final.
> d) Memory consumption is significantly higher.
>> [!success]- Answer
>> b) Any class in the same package can modify the fields directly, bypassing validation logic.

> [!question] If you want to allow child classes to access a parent's variable directly while hiding it from unrelated external classes, which modifier should you use?
> a) private
> b) public
> c) protected
> d) default
>> [!success]- Answer
>> c) protected

> [!question] What is the primary setup of a "Read-Only" variable implementation in OOP?
> a) To provide a getter but no setter.
> b) To provide a setter but no getter.
> c) To use the final keyword without any class methods.
> d) To mark the source code file as write-protected.
>> [!success]- Answer
>> a) To provide a getter but no setter.

> [!question] Consider the code: "this.name = name;" inside a setter. What does "this.name" refer to?
> a) The parameter passed to the setter method.
> b) The local variable defined within the setter block.
> c) The instance variable belonging to the current object.
> d) A global static class variable.
>> [!success]- Answer
>> c) The instance variable belonging to the current object.

> [!question] Which access modifier is best suited for internal helper methods that should never be accessed or overridden outside their containing class?
> a) public
> b) protected
> c) default
> d) private
>> [!success]- Answer
>> d) private

> [!question] Match the Java modifier with its scope.
>> [!example] Group A
>> a) private
>> b) default
>> c) protected
>> d) public
>
>> [!example] Group B
>> n) Visible everywhere.
>> o) Visible to class, package, and subclasses.
>> p) Visible to class and package only.
>> q) Visible only within the same class.
>
>> [!success]- Answer
>> a) -> q)
>> b) -> p)
>> c) -> o)
>> d) -> n)

> [!question] Match the cell analogy components to their OOP counterparts.
>> [!example] Group A
>> a) Cell Nucleus
>> b) Cell Wall
>> c) Gateways
>
>> [!example] Group B
>> n) Encapsulation Boundary / Shell
>> o) Private Data / Core internal logic
>> p) Public Methods / Getters and Setters
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the interface access design patterns.
>> [!example] Group A
>> a) Read-Only
>> b) Write-Only
>> c) Validation Logic
>
>> [!example] Group B
>> n) Setter method checking conditional logic before assignment.
>> o) Private field with a getter but no setter.
>> p) Private field with a setter but no getter.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the access modifier to its behavior with inheritance across packages.
>> [!example] Group A
>> a) default
>> b) protected
>
>> [!example] Group B
>> n) Inheritable by child classes across different packages.
>> o) Not inheritable by child classes across different packages.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the Java variables and terms to their corresponding scopes.
>> [!example] Group A
>> a) Instance Variable
>> b) Local Variable
>> c) "this" keyword
>
>> [!example] Group B
>> n) Points directly to the current object instance.
>> o) Global within the scope of the class template.
>> p) Scoped strictly within a method parameter or block.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the OOP structural problem to its correct programmatic solution.
>> [!example] Group A
>> a) Variable Shadowing Ambiguity
>> b) Direct Unvalidated Field Manipulation
>
>> [!example] Group B
>> n) Implement private fields with public Setters containing gatekeeping code.
>> o) Explicitly prepend the instance field reference with "this".
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the subclassing scenario to its accessibility status.
>> [!example] Group A
>> a) Subclass in the same package
>> b) Subclass in a different package
>
>> [!example] Group B
>> n) Can access protected fields but cannot access default (package-private) fields.
>> o) Can access both default and protected fields of the parent class.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the access modifiers to their specific architecture design intentions.
>> [!example] Group A
>> a) public
>> b) private
>> c) protected
>
>> [!example] Group B
>> n) Developing extension points where child classes can safely override or view variables.
>> o) Building public APIs/interfaces meant for any external consumer.
>> p) Sealing internal states and helper structures entirely within a class.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the components of the medical capsule analogy.
>> [!example] Group A
>> a) Outer Shell
>> b) Chemical Contents
>
>> [!example] Group B
>> n) Private fields, internal algorithms, and sensitive behavior.
>> o) Class declaration boundary and restricted visibility modifiers.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the architectural relation to the maximum allowed access level (excluding public).
>> [!example] Group A
>> a) Class in the same package (no inheritance)
>> b) Class in a different package (no inheritance)
>> c) Subclass in a different package
>
>> [!example] Group B
>> n) Cannot access private, default, or protected elements.
>> o) Can access default and protected elements.
>> p) Can access protected elements but not default elements.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)