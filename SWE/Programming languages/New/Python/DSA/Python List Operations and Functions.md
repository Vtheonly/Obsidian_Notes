
This is basically a **complexity reference for Python list operations and common built-ins**. I’ll give you a structured table.

---

# Complexity of Python List Operations and Functions

|Function / Method|Description|Time Complexity|Space Complexity|
|---|---|---|---|
|`len(lst)`|Get length|**O(1)**|**O(1)**|
|`lst[i]`|Indexing|**O(1)**|**O(1)**|
|`lst[i] = x`|Assignment|**O(1)**|**O(1)**|
|`for x in lst:`|Iteration|**O(n)**|**O(1)**|
|`x in lst`|Membership test|**O(n)**|**O(1)**|
|`lst.append(x)`|Add at end|**O(1)** amortized|**O(1)**|
|`lst.pop()`|Remove from end|**O(1)**|**O(1)**|
|`lst.pop(i)`|Remove at index|**O(n)**|**O(1)**|
|`lst.insert(i, x)`|Insert at index|**O(n)**|**O(1)**|
|`del lst[i]`|Delete element|**O(n)**|**O(1)**|
|`lst.remove(x)`|Remove first occurrence|**O(n)**|**O(1)**|
|`lst.sort()`|Sort in place|**O(n log n)**|**O(1)** extra|
|`sorted(lst)`|Return new sorted list|**O(n log n)**|**O(n)**|
|`reversed(lst)`|Reverse iterator|**O(1)**|**O(1)**|
|`lst.reverse()`|In-place reverse|**O(n)**|**O(1)**|
|`min(lst) / max(lst)`|Minimum or maximum|**O(n)**|**O(1)**|
|`sum(lst)`|Sum all elements|**O(n)**|**O(1)**|
|`list(set(lst))`|Convert to set then list|**O(n)** avg|**O(n)**|
|`list(dict.fromkeys(lst))`|Remove duplicates, keep order|**O(n)** avg|**O(n)**|
|`map(func, lst)`|Apply func to each|**O(n)**|**O(n)** if expanded|
|`filter(func, lst)`|Keep matching elements|**O(n)**|**O(n)** if expanded|
|`lst.copy()`|Shallow copy|**O(n)**|**O(n)**|
|`lst[:]`|Slice copy|**O(n)**|**O(n)**|
|`lst[a:b]`|Slice|**O(k)** (k = slice size)|**O(k)**|
|`lst.extend(lst2)`|Concatenate|**O(k)** (k = len(lst2))|**O(k)**|
|`lst + lst2`|Concatenate|**O(n + k)**|**O(n + k)**|
|`zip(lst1, lst2)`|Pair elements|**O(min(n, m))**|**O(min(n, m))**|
|`enumerate(lst)`|Index + value|**O(n)**|**O(1)**|
|`any(lst)`|Return True if any element is True|**O(n)** worst case|**O(1)**|
|`all(lst)`|Return True if all elements are True|**O(n)** worst case|**O(1)**|

---

### Notes

1. **n** = size of list.
    
2. Hash-based ops (like `set`, `dict.fromkeys`) are **O(n)** on average, but could degrade in pathological hash collisions.
    
3. Iterators like `reversed`, `map`, `filter`, `enumerate`, `zip` are **lazy** in Python. Their creation is O(1), but expanding them fully costs O(n).
    
