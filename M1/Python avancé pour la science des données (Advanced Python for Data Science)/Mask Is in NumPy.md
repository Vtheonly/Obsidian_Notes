
## **What a Mask Is in NumPy**

A **mask** in NumPy is simply a **Boolean array** — an array of `True` and `False` values — that’s used to **select** or **filter** elements from another array.

So instead of looping manually, you “mask” the elements that meet a condition.

---

### **Example: Creating a Mask**

```python
import numpy as np

arr = np.array([5, 12, 7, 20, 3])
mask = arr > 10
print(mask)
```

**Output:**

```
[False  True False  True False]
```

Here, `mask` shows which elements are greater than 10.

---

### **Using the Mask Directly**

```python
filtered = arr[mask]
print(filtered)
```

**Output:**

```
[12 20]
```

You can think of this as:

> “Give me all elements where the mask is True.”

---

### **Using `np.where(mask)`**

`np.where(mask)` gives the **indices** of the elements where the mask is `True`.

```python
indices = np.where(mask)
print(indices)
```

**Output:**

```
(array([1, 3]),)
```

This means:

- The elements at indices `1` and `3` are the ones satisfying the condition (`arr > 10`).
    

---

### **Putting It Together**

|Operation|Purpose|Example Output|
|---|---|---|
|`mask = arr > 10`|Create Boolean mask|`[False True False True False]`|
|`arr[mask]`|Filter elements|`[12 20]`|
|`np.where(mask)`|Get indices of True values|`(array([1, 3]),)`|

---

### **You Can Also Combine Conditions**

```python
mask = (arr > 5) & (arr < 15)
print(arr[mask])
```

**Output:**

```
[12 7]
```

---

### **In Short**

- A **mask** is a Boolean array used for **filtering** or **searching**.
    
- `np.where(mask)` gives the **indices** of `True` elements.
    
- `arr[mask]` gives the **values** of those elements.
    

You can use masks as a powerful way to perform vectorized searches and filtering without explicit loops.