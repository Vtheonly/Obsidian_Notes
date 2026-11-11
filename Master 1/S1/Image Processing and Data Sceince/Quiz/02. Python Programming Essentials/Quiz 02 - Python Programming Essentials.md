---
sources:
  - "[[02.1. Python Runtime, Dynamic Typing, and Core Primitives]]"
  - "[[02.2. Python Lists, Sequence Operations, and Internal Memory Architecture]]"
  - "[[02.3. Dictionaries, Sets, Tuples, and High-Performance Collections]]"
  - "[[02.4. Control Flow, Conditionals, and Comprehensions Mastery]]"
  - "[[02.5. Exhaustive Guide to Iteration, Iterables, and the Iterator Protocol]]"
  - "[[02.6. Generators, Lazy Evaluation, and Asynchronous Streaming Pipelines]]"
  - "[[02.7. The 1 Million Records Memory Explosion Autopsy and Production Streaming Solutions]]"
  - "[[02.8. Object-Oriented Programming and Class Design Patterns]]"
  - "[[02.9. Robust Exception Handling and Resource Management]]"
  - "[[02.10. Code Modularity, Packaging, and Standard Library Systems]]"
  - "[[02.11. Tutorial 03 - Modular Sales Inventory Processing Pipeline]]"
  - "[[02.12. Tutorial 03 - Student Cohort Generation and Statistical Analysis System]]"
---
> [!question] In Python, a variable stores its value directly inside the variable itself, much like a box holding its contents.
>> [!success]- Answer
>> False

> [!question] CPython pre-allocates singleton integer objects for the values between -5 and 256, so after `x = 256` and `y = 256` the expression `x is y` evaluates to True.
>> [!success]- Answer
>> True

> [!question] Thanks to CPython's over-allocation growth strategy, appending elements to a list runs in amortized $O(1)$ time.
>> [!success]- Answer
>> True

> [!question] A Python list can be used as a dictionary key because dictionaries accept any object as a key.
>> [!success]- Answer
>> False

> [!question] The `else` clause of a `for` loop executes only when the loop completes normally without encountering a `break` statement.
>> [!success]- Answer
>> True

> [!question] Once a generator object is exhausted, calling `iter()` on it returns a fresh iterator that restarts the sequence from the beginning.
>> [!success]- Answer
>> False

> [!question] Calling a generator function runs its body immediately and returns the first yielded value to the caller.
>> [!success]- Answer
>> False

> [!question] Because CSV text is compact on disk, loading 1,000,000 rows with `list(csv.DictReader(f))` consumes only a few megabytes of RAM.
>> [!success]- Answer
>> False

> [!question] When a file is opened with `with open(path) as f`, the file descriptor is guaranteed to be closed when the block exits, even if an exception occurs inside the block.
>> [!success]- Answer
>> True

> [!question] In the modular sales inventory pipeline, a record whose price field cannot be parsed as a number is skipped with a warning instead of crashing the program.
>> [!success]- Answer
>> True

> [!question] Given two separate assignments `a = [1, 2, 3]` and `b = [1, 2, 3]`, what do the expressions `a == b` and `a is b` evaluate to?
> a) Both expressions evaluate to True.
> b) Both expressions evaluate to False.
> c) `a == b` is True and `a is b` is False.
> d) `a == b` is False and `a is b` is True.
>> [!success]- Answer
>> c) `a == b` is True and `a is b` is False.

> [!question] After running `original = [[1, 2], [3, 4]]`, then `shallow = original.copy()`, then `original[0][0] = 999`, what is the value of `shallow[0][0]`?
> a) 1, because `copy()` recursively duplicates every nested object.
> b) 999, because the copied outer list still references the original inner sublists.
> c) 1, because the shallow copy snapshots the nested values at the moment of copying.
> d) It raises an AttributeError because lists do not provide a `copy()` method.
>> [!success]- Answer
>> b) 999, because the copied outer list still references the original inner sublists.

> [!question] What is the value of `a` after executing `a = [1, 2]` followed by `a.append([3, 4])`?
> a) `[1, 2, 3, 4]`
> b) `[1, 2, [3, 4]]`
> c) `[[1, 2], [3, 4]]`
> d) `[1, 2]`
>> [!success]- Answer
>> b) `[1, 2, [3, 4]]`

> [!question] What is the result of evaluating `set_a - set_b` where `set_a = {1, 2, 3}` and `set_b = {3, 4, 5}`?
> a) `{3}`
> b) `{1, 2, 4, 5}`
> c) `{1, 2, 3, 4, 5}`
> d) `{1, 2}`
>> [!success]- Answer
>> d) `{1, 2}`

> [!question] What is the value of the list comprehension `[x * x for x in range(10) if x % 2 == 0]`?
> a) `[0, 4, 16, 36, 64]`
> b) `[1, 9, 25, 49, 81]`
> c) `[0, 2, 4, 6, 8]`
> d) `{0, 4, 16, 36, 64}`
>> [!success]- Answer
>> a) `[0, 4, 16, 36, 64]`

> [!question] How does CPython actually execute a `for` loop over a list?
> a) It walks the list with an internal counter and stops when an IndexError is raised.
> b) It materializes the loop body into a generator function and calls it once.
> c) It obtains an iterator with `iter()` and repeatedly calls `next()` until `StopIteration` is raised.
> d) It copies the list into a dictionary and loops over its keys in sorted order.
>> [!success]- Answer
>> c) It obtains an iterator with `iter()` and repeatedly calls `next()` until `StopIteration` is raised.

> [!question] Roughly how much memory does the generator expression `(x for x in range(10000000))` consume?
> a) Hundreds of megabytes, matching the equivalent list comprehension.
> b) About 112 bytes, because values are produced on demand instead of being stored.
> c) Exactly zero bytes until the first element is requested.
> d) Roughly one tenth of the list comprehension, since only a sample of values is kept.
>> [!success]- Answer
>> b) About 112 bytes, because values are produced on demand instead of being stored.

> [!question] Which factor drives the memory explosion when one million CSV rows are materialized with `list(csv.DictReader(f))`?
> a) Each row becomes a dictionary that typically consumes around 250 to 350 bytes of heap memory.
> b) The `csv` module stores every row twice, once as a list and once as a tuple.
> c) Opening the file in text mode forces the whole file into one immutable string before parsing begins.
> d) The `with` statement keeps a hidden full copy of the file in memory after the block exits.
>> [!success]- Answer
>> a) Each row becomes a dictionary that typically consumes around 250 to 350 bytes of heap memory.

> [!question] In an object design where a `Student` instance creates and owns its own `StudentCard`, so that destroying the student destroys the card, which relationship is being illustrated?
> a) Aggregation, because the card exists independently of the student.
> b) Inheritance, because `StudentCard` extends `Student`.
> c) Polymorphism, because both classes share a common interface.
> d) Composition, because the card's lifecycle is bound to the student's.
>> [!success]- Answer
>> d) Composition, because the card's lifecycle is bound to the student's.

> [!question] Why does the student cohort generator call `random.seed(101)` before producing its synthetic records?
> a) It seeds the pseudo-random generator so the produced sequence is reproducible on every run.
> b) It increases the entropy of the generator so the values become more random.
> c) It initializes the hash table used to deduplicate student identifiers.
> d) It calibrates the `datetime` module to the 2026 reference year.
>> [!success]- Answer
>> a) It seeds the pseudo-random generator so the produced sequence is reproducible on every run.

> [!question] Match each component of the CPython object model with its role.
>> [!example] Group A
>> a) `ob_refcnt`
>> b) `ob_type`
>> c) Value fields
>> d) Dynamic typing
>
>> [!example] Group B
>> n) A pointer to the object's type descriptor.
>> o) The runtime mechanism that lets a single variable name be rebound to objects of different types, because type information lives on the object rather than the variable.
>> p) The reference count field that drives automatic garbage collection.
>> q) The pointer or memory buffer holding the object's actual data.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)

> [!question] Match each collection type with its defining properties.
>> [!example] Group A
>> a) Tuple
>> b) Dictionary
>> c) Set
>> d) `collections.deque`
>
>> [!example] Group B
>> n) A mutable key-value mapping that preserves insertion order since Python 3.7, with $O(1)$ average lookups.
>> o) A doubly linked structure offering $O(1)$ insertion and deletion at both ends for stacks and queues.
>> p) An immutable ordered sequence suited to fixed records, hashable enough to serve as a mapping key.
>> q) A mutable, unordered hash-backed collection used for deduplication and membership testing.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)

> [!question] Match each element of Python's iteration machinery with what it does.
>> [!example] Group A
>> a) Iterable
>> b) Iterator
>> c) `iter()`
>> d) `next()`
>> e) `StopIteration`
>
>> [!example] Group B
>> n) The built-in that fetches a fresh stream cursor from a container before looping begins.
>> o) The exception that signals the stream is exhausted so the loop can end gracefully.
>> p) An object that can hand out its members one at a time and produce a new independent cursor each time it is asked.
>> q) A stateful single-pass object whose position advances with every element request; once spent, it stays spent.
>> r) The built-in that requests the following element from the active cursor on each call.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> r)
>> e) -> o)

> [!question] Match each generator mechanism with its behavior.
>> [!example] Group A
>> a) `yield`
>> b) `yield from`
>> c) `gen.send()`
>> d) `gen.close()`
>
>> [!example] Group B
>> n) Delegates value production to an inner sub-generator or iterable.
>> o) Freezes the execution frame, preserving local variables and the instruction pointer, while handing a value to the caller.
>> p) Pushes a value into the suspended generator, where it becomes the result of the currently paused expression.
>> q) Raises a `GeneratorExit` inside the generator to shut it down cleanly.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)
>> d) -> q)

> [!question] Match each production strategy from the million-record memory autopsy with its approach.
>> [!example] Group A
>> a) Pure generator stream
>> b) Chunk-based batch iterator
>> c) Pandas chunked processing
>> d) Chained filtering pipeline
>
>> [!example] Group B
>> n) Wires independent parsing and selection stages together so records flow through them on demand.
>> o) Yields rows one at a time so only a single record is ever held in memory.
>> p) Accumulates rows into fixed-size groups before emitting them, balancing I/O speed against memory use.
>> q) Iterates over DataFrame pieces of a configured size, aggregating each piece before moving on.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> q)
>> d) -> n)

> [!question] Match each pillar of object-oriented programming with its description.
>> [!example] Group A
>> a) Encapsulation
>> b) Inheritance
>> c) Polymorphism
>> d) Abstraction
>
>> [!example] Group B
>> n) Lets different classes share a common interface while providing unique method implementations.
>> o) Bundles data attributes and the methods that operate on them inside objects, restricting direct external access to internal state.
>> p) Enforces interface contracts on child classes, which must implement every required method before instantiation.
>> q) Lets a specialized child class reuse attributes and methods from a parent class.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match each clause of the exception handling statement with when it runs.
>> [!example] Group A
>> a) `try`
>> b) `except`
>> c) `else`
>> d) `finally`
>
>> [!example] Group B
>> n) Catches and handles a specific exception type gracefully.
>> o) Performs cleanup operations in all circumstances, even during unhandled exceptions or `return` statements.
>> p) Contains the code that could raise a runtime exception.
>> q) Runs code only if no exceptions were raised in the guarded block.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)

> [!question] Match each modularity concept with its meaning.
>> [!example] Group A
>> a) Module
>> b) Package
>> c) Package initializer
>> d) Entry-point guard
>> e) `sys.path`
>
>> [!example] Group B
>> n) The marker that converts a plain folder into an import target, commonly re-exporting selected names for convenience.
>> o) The list of directories the importer searches; a project root can be appended to it so sibling code becomes importable.
>> p) A directory of code files that the interpreter can import and distribute as a single unit.
>> q) A single source file containing executable code, functions, and classes.
>> r) Lets a file include standalone executable code, such as self-tests or CLI scripts, that is skipped whenever the file is imported elsewhere.
>
>> [!success]- Answer
>> a) -> q)
>> b) -> p)
>> c) -> n)
>> d) -> r)
>> e) -> o)

> [!question] Match each standard library module with what it provides.
>> [!example] Group A
>> a) `math`
>> b) `random`
>> c) `datetime`
>> d) `statistics`
>> e) `os`
>
>> [!example] Group B
>> n) Number generation using the Mersenne Twister algorithm, with helpers like `randint()`, `uniform()`, and `sample()`.
>> o) Portable operating system interfaces such as working directories, path joining, and directory creation.
>> p) Basic descriptive calculations like mean, median, and stdev on Python iterables.
>> q) Functions implemented on C doubles such as `sqrt()`, `ceil()`, and `log10()`.
>> r) Classes for calendar days, clock times, and duration arithmetic built around `timedelta`.
>
>> [!success]- Answer
>> a) -> q)
>> b) -> n)
>> c) -> r)
>> d) -> p)
>> e) -> o)

> [!question] Match each building block of the two Tutorial 03 projects with what it does.
>> [!example] Group A
>> a) `clean_lines()`
>> b) `parse_products()`
>> c) `Product.total_value()`
>> d) `generate_student_cohort()`
>> e) `compute_class_statistics()`
>
>> [!example] Group B
>> n) Splits each record on commas, converts the numeric fields, and skips malformed entries with a warning.
>> o) Multiplies unit price by stock quantity to obtain the inventory worth of a single item.
>> p) Simulates ten synthetic learner records with random grades and birth dates inside bounded years, starting from a fixed seed.
>> q) Strips surrounding whitespace from each raw record and discards the empty ones using a comprehension with the walrus operator.
>> r) Summarizes the enriched group with the mean, median, standard deviation, minimum, and maximum of the grade averages, plus mean age.
>
>> [!success]- Answer
>> a) -> q)
>> b) -> n)
>> c) -> o)
>> d) -> p)
>> e) -> r)
