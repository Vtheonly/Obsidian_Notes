## Chapter 3: Syntax Analysis

### 1. Introduction

Syntax analysis, the second stage of compilation, involves a **parser** which verifies the conformity of the source program (written in language L1) with the syntax of L1 defined by a context-free grammar (CFG) G. The parser outputs a syntax tree, with leaves representing the tokens generated during lexical analysis. 

This chapter focuses on specific descending and ascending parsing methods. Syntax analysis utilizes a CFG, a stack automaton, and the sequence of coded tokens from the lexical analyzer. We will discuss challenges posed by ambiguous, left-recursive, and unfactored grammars.

### 2. Basic Concepts

#### 2.1 Ambiguity

Ambiguity arises when a grammar allows multiple parse trees for a single input string. 

**Example:**

Consider the grammar G:  `E → E+E / E*E / (E) / idf / cstent`

To resolve ambiguity, we introduce operator precedence and associativity rules. Assuming standard arithmetic precedence ( '*'  and '/' have higher precedence than '+' and '-' , and operators are left-associative), we obtain the unambiguous grammar G':

- `E → E + T / T`
- `T → T * F / F`
- `F → (E) / idf / cstent`

#### 2.2 Left Recursion

Left recursion occurs when a non-terminal derives a string that starts with itself, potentially leading to infinite recursion during parsing.

##### 2.2.1 Direct Left Recursion

Direct left recursion occurs when a production rule has the form: `A → Aα`

**Elimination:**

Rewrite rules of the form `A → Aα1 / ... / Aαn / β1 / ... / βm` (where βi does not start with A) as:

- `A → β1A' / ... / βmA'`
- `A' → α1A' / ... / αnA' / ε`

**Example:**

The grammar G' above exhibits left recursion. Eliminating it yields G'':

- `E → TE'`
- `E' → +TE' / ε`
- `T → FT'`
- `T' → *FT' / ε`
- `F → (E) / idf / cstent`

##### 2.2.2 Indirect Left Recursion

Indirect left recursion occurs when a non-terminal A derives a string containing A through a series of productions.

**Solution:**

1. Transform the grammar to contain only direct left recursion.
2. Eliminate direct left recursion using the method described above.

The transformation involves ordering the non-terminals and applying substitutions to rewrite the grammar without left recursion while preserving the language generated.

##### 2.2.3 Algorithm for Removing Left Recursion

1. Ensure the grammar G is clean (no cycles or ε-productions).
2. Order the non-terminals A<sub>i</sub>.
3. For i = 1 to n:
   - For j = 1 to i - 1:
     - If a production rule A<sub>i</sub> → A<sub>j</sub>α exists, replace it with A<sub>i</sub> → β<sub>1</sub>α / ... / β<sub>n</sub>α, where A<sub>j</sub> → β<sub>1</sub> / ... / β<sub>n</sub>.
   - Eliminate direct left recursion from A<sub>i</sub>-productions.

**Example:**

```
G: 
S → Aa / b
A → Ac | Sd | c 
```
After removing left recursion:
```
G':
S → Aa / b
A → cA' / SdA' 
A' → cA' / dA' / ε 
```


#### 2.3 Left Factoring

Left factoring eliminates common prefixes in production rules to avoid backtracking during parsing.

A grammar is unfactored if a production rule has the form: `A → αA1 / αA2 / ... / αAn / β1 / β2 / ... / βm`

**Factoring:**

Rewrite the rule as:

- `A → αA' / β1 / β2 / ... / βm`
- `A' → A1 / A2 / ... / An`

Repeat for all production rules with common prefixes.

**Example:**

```
A → abC / aAB / caF 
```
After left factoring:
```
A → aA' / caF
A’ → bC / AB
```

### 2.4 Notions of FIRST and FOLLOW Sets

#### Example Grammar Gexp:
```
E  -> T E'
E' -> + T E' | ε
T  -> F T'
T' -> * F T' | ε
F  -> ( E ) | idf
```

#### a) Construction of FIRST Sets
For any string \(X\) composed of terminal and non-terminal symbols, the goal is to find the set of all terminal symbols that can start a string derived from \(X\).

**Steps for all productions:**
1. If \(X \rightarrow ε\) is a production, add \(ε\) to FIRST(X).
2. If \(X \rightarrow a\) is a production and \(a\) is a terminal, then \(FIRST(X) = \{a\}\).
3. If \(X \rightarrow Y_1 Y_2 \ldots Y_n\) is a production (with \(Y_i\) being terminal or non-terminal), then:
   - Add elements of \(FIRST(Y_1)\) except \(ε\) to FIRST(X).
   - If there exists \(j\) (with \(j = 2..n\)) such that for all \(i = 1..j-1\), \(ε \in FIRST(Y_i)\), then add elements of \(FIRST(Y_j)\) except \(ε\) to FIRST(X).
   - If for all \(i = 1..n\), \(ε \in FIRST(Y_i)\), then add \(ε\) to FIRST(X).

**Example using Gexp:**
- \(FIRST(E) = FIRST(TE') = FIRST(T) - \{ε\}\)
- \(FIRST(E') = FIRST(+TE') \cup FIRST(ε) = \{+\} \cup \{ε\} = \{+, ε\}\)
- \(FIRST(T) = FIRST(F) - \{ε\} = \{(, idf\}\)
- \(FIRST(F) = FIRST((E)) \cup FIRST(idf) = FIRST(() \cup FIRST(idf) = \{(, idf\}\)
- \(FIRST(T') = FIRST(*FT') \cup FIRST(ε) = \{*\} \cup \{ε\} = \{*, ε\}\)

Therefore:
- \(FIRST(E) = \{(, idf\}\)
- \(FIRST(E') = \{+, ε\}\)
- \(FIRST(T) = \{(, idf\}\)
- \(FIRST(T') = \{*, ε\}\)
- \(FIRST(F) = \{(, idf\}\)

#### b) Construction of FOLLOW Sets
For any non-terminal \(A\), FOLLOW(A) is the set of all terminal symbols that can appear immediately to the right of \(A\) in a derivation.

**Steps for all productions:**
1. If \(S\) is the start symbol of the grammar, add the end-of-string marker (e.g., #) to FOLLOW(S).
2. If there is a production \(A \rightarrow \alpha B \beta\) and \(B\) is a non-terminal, add \(FIRST(\beta)\) except \(ε\) to FOLLOW(B).
3. If there is a production \(A \rightarrow \alpha B\), add FOLLOW(A) to FOLLOW(B).
4. If there is a production \(A \rightarrow \alpha B \beta\) with \(ε \in FIRST(\beta)\), add FOLLOW(A) to FOLLOW(B).

**Example using Gexp:**
- \(FOLLOW(E) = \{#\} \cup (FIRST()) - \{ε\} = \{#, )\}\)
- \(FOLLOW(E') = FOLLOW(E) = \{#, )\}\)
- \(FOLLOW(T) = (FIRST(E') - \{ε\}) \cup FOLLOW(E') = \{+, #, )\}\)
- \(FOLLOW(T') = FOLLOW(T) = \{+, #, )\}\)
- \(FOLLOW(F) = \{*, +, #, )\}\)

Therefore:
- \(FOLLOW(E) = \{#, )\}\)
- \(FOLLOW(E') = \{#, )\}\)
- \(FOLLOW(T) = \{+, #, )\}\)
- \(FOLLOW(T') = \{+, #, )\}\)
- \(FOLLOW(F) = \{*, +, #, )\}\)

[[3 -  FIRST and FOLLOW]]

## 3. Descending Parsing

### 3.1) LL(1) Grammar
An LL(1) grammar is a context-free grammar for which the predictive parsing table has no cell containing more than one production rule. "LL(1)" refers to:
- L: Left to right scanning of the input.
- L: Leftmost derivation.
- (1): Only one lookahead symbol is needed to make each parsing decision.

#### a) Definition 1
Formally, an LL(1) grammar's production rules satisfy the following conditions for any two alternatives of a non-terminal:
1. If \(A \rightarrow \alpha\) and \(A \rightarrow \beta\), then \(FIRST(\alpha) \cap FIRST(\beta) = \emptyset\).
2. If \(A \rightarrow \alpha\) and \(A \rightarrow \beta\), then either \(\alpha \rightarrow_G^* \epsilon\) or \(\beta \rightarrow_G^* \epsilon\).
3. If \(A \rightarrow \alpha\) and \(A \rightarrow \beta\) and \(\beta \rightarrow_G^* \epsilon\), then \(FIRST(\alpha) \cap FOLLOW(A) = \emptyset\).

#### b) Definition 2
An LL(1) grammar is a grammar for which the predictive parsing table has no cell containing more than one production rule.

**Remarks:**
1. An ambiguous or left-recursive or non-left-factored grammar is not LL(1).
2. A grammar that is factored and neither ambiguous nor left-recursive is not necessarily LL(1).

### 3.2) Construction of the LL(1) Predictive Parsing Table
The parsing table is a two-dimensional array that indicates, for each non-terminal \(A\) and each terminal \(a\) or end-of-input symbol \(#\), the production rule to apply.

**Steps:**
1. The first row contains all tokens of \(V_t\), and the first column contains all non-terminals of \(V_n\).
2. For each production \(A \rightarrow \alpha\):
   - For each \(a \in FIRST(\alpha)\) (where \(a \neq \epsilon\)), put \(A \rightarrow \alpha\) in cell \(Tab[A,a]\).
   - If \(\epsilon \in FIRST(\alpha)\), for each \(b \in FOLLOW(A)\), put \(A \rightarrow \alpha\) in cell \(Tab[A,b]\).
3. Each empty cell \(Tab[A,a]\) represents a syntax error (a specific error code can be specified).

**Example:**

With grammar \(G_{exp}\), we calculate for each \(\alpha\) of \(A \rightarrow \alpha\) and obtain the following table:

### Example Grammars and Their FIRST and FOLLOW Sets

#### Grammar 1

```
S  -> A B C
A  -> a A | ε
B  -> b B | C
C  -> c C | d
```

| Non-Terminal | FIRST         | FOLLOW    |
|--------------|---------------|-----------|
| S            | {a, b, c, d}  | {#}       |
| A            | {a, ε}        | {b, c, d} |
| B            | {b, c, d}     | {c, d, #} |
| C            | {c, d}        | {#}       |

#### Grammar 2

```
E  -> T E'
E' -> + T E' | ε
T  -> F T'
T' -> * F T' | ε
F  -> ( E ) | id
```

| Non-Terminal | FIRST          | FOLLOW     |
|--------------|----------------|------------|
| E            | {(, id}        | {#, )}     |
| E'           | {+, ε}         | {#, )}     |
| T            | {(, id}        | {+, #, )}  |
| T'           | {*, ε}         | {+, #, )}  |
| F            | {(, id}        | {*, +, #, )}|

#### Grammar 3

```
S  -> X Y
X  -> x X | ε
Y  -> y
```

| Non-Terminal | FIRST         | FOLLOW  |
|--------------|---------------|---------|
| S            | {x, y}        | {#}     |
| X            | {x, ε}        | {y}     |
| Y            | {y}           | {#}     |

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
| S            | {x, y}        | {#}     |
| X            | {x, ε}        | {y}     |
| Y            | {y}           | {#}     |

These tables provide a clear visualization of the FIRST and FOLLOW sets for each grammar, aiding in the construction of LL(1) parsing tables.