
## Overview: The Java Container Landscape

When storing data in Java, beginners often confuse terms like "Array", "List", and "Collection". It is crucial to separate these into three distinct "worlds".

Java divides data containers into three main categories:

1.  **Arrays**: Low-level, language-integrated features.
2.  **The Collections Framework**: A modern set of Interfaces and Classes (List, Set, Map).
3.  **Legacy Collections**: Old classes (Vector, Hashtable) that are mostly obsolete.

### The Mental Model

The most important distinction is between **Arrays** (fixed, fast, primitive) and **Collections** (dynamic, object-oriented, flexible).

```mermaid
graph TD
    subgraph "World 1: Arrays"
        A[Native Array int[], String[]]
    end

    subgraph "World 2: Collections Framework"
        C[Collection Interface] --> L[List Interface]
        C --> S[Set Interface]
        C --> Q[Queue Interface]
        
        L --> AL[ArrayList]
        L --> LL[LinkedList]
        
        S --> HS[HashSet]
        S --> TS[TreeSet]
        
        M[Map Interface] --> HM[HashMap]
    end
    
    subgraph "World 3: Legacy (Avoid)"
        V[Vector]
        ST[Stack]
    end

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#bbf,stroke:#333,stroke-width:2px
    style M fill:#bfb,stroke:#333,stroke-width:2px
    style V fill:#ccc,stroke:#333,stroke-width:2px
```

### Key Differences Summary

| Feature | **Array** | **Collection (e.g., ArrayList)** |
| :--- | :--- | :--- |
| **Size** | Fixed at creation. | Dynamic (grows automatically). |
| **Performance** | Fastest (no overhead). | Slightly slower (wrapper overhead). |
| **Data Types** | Primitives (`int`) & Objects. | **Objects Only** (uses Wrapper classes like `Integer`). |
| **Functionality** | None (no `.add`, `.remove`). | Rich API (`.add`, `.remove`, `.contains`). |
| **Syntax** | `arr[i]` | `list.get(i)` |

> [!TIP]
> **Map is NOT a Collection.**
> Notice in the diagram that `Map` does not extend `Collection`. This is a common interview question. A `Collection` stores individual elements (like a bag of marbles), whereas a `Map` stores pairs (Key-Value).
