A **decorator** in Python is a function (or class) that takes another function (or method) as input, adds or changes its behavior, and returns a new function (or the same one with modifications).

It’s essentially **a reusable way to wrap functionality around existing functions or methods without modifying their actual code**.

---

## 1. How it Works

A decorator:

1. Accepts a function as an argument.
    
2. Defines a wrapper function inside that can run code **before and/or after** the original function.
    
3. Returns that wrapper instead of the original function.
    

Because functions in Python are **first-class objects** (can be passed around like variables), decorators are possible.

---

## 2. Basic Syntax

```python
def my_decorator(func):
    def wrapper():
        print("Before the function runs")
        func()
        print("After the function runs")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
```

**Output:**

```
Before the function runs
Hello!
After the function runs
```

Here:

- `@my_decorator` is equivalent to `say_hello = my_decorator(say_hello)`.
    

---

## 3. Common Uses

- **Logging**
    
- **Authentication/authorization checks**
    
- **Timing function execution**
    
- **Caching results**
    
- **Validating inputs**
    

---

## 4. Example: Logging Decorator

```python
import functools

def log_call(func):
    @functools.wraps(func)  # preserves function name & docstring
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args} {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_call
def add(a, b):
    return a + b

add(3, 4)
```

---

## 5. Key Points

- Use `functools.wraps` to keep the original function’s metadata (name, docstring).
    
- Decorators can be **stacked**:
    

```python
@decorator1
@decorator2
def func():
    pass
```

- There are **class-based decorators** too, when you need stateful behavior.
    

---

If you want, I can also show you **how decorators tie into OOP design patterns** like the _Decorator Pattern_ from GoF, because Python’s decorator syntax is actually inspired by it. That would connect it directly to your design patterns learning.