Yes, exactly. Reduction works because the operation can be:

```text
split -> compute independently -> merge later
```

That only works for operations that are:

# Associative

Meaning:

```text
(a op b) op c == a op (b op c)
```

like:

- addition
    
- multiplication
    
- min/max
    
- bitwise OR/AND
    

---

# Your Question

What if logic changes dynamically?

Example:

```c
if (x % 2 == 0)
    total += x;
else
    total *= x;
```

or:

```c
if (isPrime(x))
    something...
```

Then things become harder.

---

# Important Distinction

## This is STILL parallelizable:

```c
#pragma omp parallel for
for (...) {
    if (isPrime(i))
        A[i] = ...
}
```

because each iteration is independent.

The logic can be completely different per iteration.

That is fine.

---

# What BREAKS parallelism

is when iterations depend on previous global state.

Bad:

```c
global = f(global, x);
```

because:

```text
iteration i needs result from iteration i-1
```

---

# Reductions Only Work For Mergeable Operations

OpenMP reduction assumes:

```text
thread_local_result_1
thread_local_result_2
thread_local_result_3
```

can later combine safely.

---

# Example That DOES Work

Suppose:

```c
if (x % 2 == 0)
    even_sum += x;
else
    odd_sum += x;
```

You can still do:

```c
reduction(+:even_sum, odd_sum)
```

because addition is mergeable.

---

# Example That DOES NOT Naturally Work

```c
state = encrypt(state, x);
```

because:

```text
next state depends on previous state
```

This creates a dependency chain.

---

# General Rule

Parallelism likes:

```text
output_i = pure_function(input_i)
```

or:

```text
partial_results -> merge
```

It hates:

```text
shared evolving state
```

---

# About Complex Logic

Even very complex conditions are okay:

```c
if (prime(x))
if (hash(x) % 7)
if (neural_network(x) > threshold)
```

as long as:

```text
iteration i does not need iteration i-1
```

That is the real rule.

Not simplicity of logic. Independence.