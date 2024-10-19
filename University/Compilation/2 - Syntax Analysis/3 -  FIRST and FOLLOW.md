
Sure, I'll provide three other grammar examples and calculate their FIRST and FOLLOW sets. Then, I'll present the results in tables for each grammar similar to the one in the image you provided.

### Grammar 1

#### Example Grammar G1:
```
S -> A B
A -> a A | ε
B -> b B | ε
```

#### FIRST and FOLLOW Sets:
| Non-Terminal | FIRST         | FOLLOW  |
|--------------|---------------|---------|
| S            | {a, ε}        | {#}     |
| A            | {a, ε}        | {a, b, #}|
| B            | {b, ε}        | {#}     |

### Grammar 2

#### Example Grammar G2:
```
S -> A C B
A -> a | ε
B -> b | ε
C -> c C | d
```

#### FIRST and FOLLOW Sets:
| Non-Terminal | FIRST         | FOLLOW  |
|--------------|---------------|---------|
| S            | {a, c, d}     | {#}     |
| A            | {a, ε}        | {c, d}  |
| B            | {b, ε}        | {#}     |
| C            | {c, d}        | {b, #}  |

### Grammar 3

#### Example Grammar G3:
```
S -> X Y
X -> x X | ε
Y -> y
```

#### FIRST and FOLLOW Sets:
| Non-Terminal | FIRST         | FOLLOW  |
|--------------|---------------|---------|
| S            | {x, y}        | {#}     |
| X            | {x, ε}        | {y}     |
| Y            | {y}           | {#}     |

These tables should help visualize the FIRST and FOLLOW sets for each grammar clearly, similar to the format shown in the image you provided.

---
Sure, I'll provide three more complex grammar examples and calculate their FIRST and FOLLOW sets. Then, I'll present the results in tables similar to the one in the image you provided.

### Grammar 1

#### Example Grammar G1:
```
S  -> A B C
A  -> a A | ε
B  -> b B | C
C  -> c C | d
```

#### FIRST and FOLLOW Sets:
| Non-Terminal | FIRST         | FOLLOW    |
|--------------|---------------|-----------|
| S            | {a, b, c, d}  | {#}       |
| A            | {a, ε}        | {b, c, d} |
| B            | {b, c, d}     | {c, d, #} |
| C            | {c, d}        | {#}       |

### Grammar 2

#### Example Grammar G2:
```
E  -> T E'
E' -> + T E' | ε
T  -> F T'
T' -> * F T' | ε
F  -> ( E ) | id
```

#### FIRST and FOLLOW Sets:
| Non-Terminal | FIRST          | FOLLOW     |
|--------------|----------------|------------|
| E            | {(, id}        | {#, )}     |
| E'           | {+, ε}         | {#, )}     |
| T            | {(, id}        | {+, #, )}  |
| T'           | {*, ε}         | {+, #, )}  |
| F            | {(, id}        | {*, +, #, )}|

### Grammar 3

#### Example Grammar G3:
```
S  -> A B
A  -> a A | b
B  -> c D | ε
D  -> d D | e
```

#### FIRST and FOLLOW Sets:
| Non-Terminal | FIRST         | FOLLOW  |
|--------------|---------------|---------|
| S            | {a, b}        | {#}     |
| A            | {a, b}        | {c, #}  |
| B            | {c, ε}        | {#}     |
| D            | {d, e}        | {#}     |

### Summary Tables

#### Grammar 1
| Non-Terminal | FIRST         | FOLLOW    |
|--------------|---------------|-----------|
| S            | {a, b, c, d}  | {#}       |
| A            | {a, ε}        | {b, c, d} |
| B            | {b, c, d}     | {c, d, #} |
| C            | {c, d}        | {#}       |

#### Grammar 2
| Non-Terminal | FIRST          | FOLLOW     |
|--------------|----------------|------------|
| E            | {(, id}        | {#, )}     |
| E'           | {+, ε}         | {#, )}     |
| T            | {(, id}        | {+, #, )}  |
| T'           | {*, ε}         | {+, #, )}  |
| F            | {(, id}        | {*, +, #, )}|

#### Grammar 3
| Non-Terminal | FIRST         | FOLLOW  |
|--------------|---------------|---------|
| S            | {a, b}        | {#}     |
| A            | {a, b}        | {c, #}  |
| B            | {c, ε}        | {#}     |
| D            | {d, e}        | {#}     |

These tables provide a clear visualization of the FIRST and FOLLOW sets for each grammar, helping to understand the structure and derivations of the grammars.