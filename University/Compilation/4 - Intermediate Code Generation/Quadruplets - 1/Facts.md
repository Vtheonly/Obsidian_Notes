
## 1. True OR False

|   | Statement                                                                                                 | V   | F   |
|---|----------------------------------------------------------------------------------------------------------|-----|-----|
| a) | Les entrées de la table des symboles sont crées et utilisées pendant la phase d'analyse lexical          |     |  X  |
| b) | Dans un compilateur, la gestion des erreurs est plus facile à la phase analyse lexical                   |     |  X  |
| c) | Un compilateur peut construire plusieurs tables de symboles pour un programme                             |  X  |     |
| d) | La grammaire définie par la règle : S→𝜀 génère un langage vide                                           |     |  X  |
| e) | La grammaire définie par D→ bDc ¦ 𝜀 possède une seule règle de production                                |     |  X  |
| f) | Dans une grammaire LL(1) nous avons besoin d'au moins un symbole pour décider de la dérivation à faire   |     |  X  |
| g) | (a¦b) abba (a¦b) : est une ER pour toutes les chaines des a et des b qui contiennent la sous chaine : abba |     |  X  |
| h) | Une analyse LR(k) permet d'obtenir une dérivation droite par remontée de l'arbre syntaxique              |  X  |     |
| i) | Une G est ambiguë si 2 mots différents reconnus par cette grammaire admettent le même arbre syntaxique   |     |  X  |
| j) | Les AFN permettent de modéliser plus de langages que les AFD                                             |     |  X  |

---


## 2. Advantage of Each grammar



**1. LL(1) Grammars**

- **Advantages:**
    - **LL(1) grammars** are another type of context-free grammar, but they are used in top-down parsing.
    - **LL parsers** (Left-to-right, Leftmost derivation) are also relatively efficient and are often used in recursive descent parsing.
    - The "(1)" means that the parser uses one symbol of lookahead to make parsing decisions.
    - **Advantages of LL(1) grammars:** They are generally easier to understand and implement than LR grammars, particularly for hand-written parsers. Recursive descent parsers, which are commonly used for LL(1) grammars, are straightforward to write and debug. The use of one lookahead symbol helps to resolve ambiguities that might arise in simpler LL(0) grammars.
    - **Easy to Understand and Implement:** LL(1) parsers, especially when implemented using recursive descent, are relatively easy to understand and write by hand.
    - **Good Error Reporting:** LL(1) parsers can provide good error messages because the parsing process closely follows the structure of the grammar.
    - **Predictive Parsing:** LL(1) parsing is predictive, meaning the parser can determine the correct production to apply based on the current input symbol and the lookahead.
    - **No Left Recursion:** LL(1) grammars cannot have left recursion, a property which simplifies parser construction.
        
- **Disadvantages:**
    
    - **Limited Expressiveness:** LL(1) grammars are less expressive than LR grammars. They cannot handle all context-free grammars.
        
    - **Left Factoring Required:** LL(1) grammars often require left factoring to eliminate common prefixes in production rules, which can make the grammar more complex.
        
    - **Not Suitable for All Languages:** Some programming language constructs cannot be naturally expressed using LL(1) grammars.
        

**2. SLR(1) Grammars (Simple LR)**

- **Advantages:**
    
    - **More Powerful than LR(0):** SLR(1) is an improvement over LR(0). It can handle more grammars by using a small amount of lookahead (one symbol) to resolve some shift/reduce conflicts.
        
    - **Relatively Easy to Construct:** SLR(1) parser tables are relatively straightforward to construct compared to more complex LR parsers.
        
    - **Efficient Parsing:** Like other LR parsers, SLR(1) parsers are efficient.
        
- **Disadvantages:**
    
    - **Still Limited:** While more powerful than LR(0), SLR(1) still cannot handle all context-free grammars.
        
    - **Shift/Reduce and Reduce/Reduce Conflicts:** SLR(1) can still suffer from shift/reduce and reduce/reduce conflicts, though fewer than LR(0).
        
    - **Not as Powerful as LALR(1) or LR(1):** SLR(1) is less powerful than LALR(1) or canonical LR(1) in terms of the grammars it can handle.
        

**3. LALR(1) Grammars (Look-Ahead LR)**

- **Advantages:**
    
    - **Widely Used in Practice:** LALR(1) is a good balance between power and efficiency. Many parser generators (like Yacc and Bison) use LALR(1).
        
    - **Handles Many Practical Grammars:** LALR(1) can handle most programming language grammars.
        
    - **Smaller Tables than LR(1):** LALR(1) parsers have significantly smaller tables than canonical LR(1) parsers, making them more practical for real-world use.
        
- **Disadvantages:**
    
    - **More Complex than SLR(1):** LALR(1) parser table construction is more complex than SLR(1).
        
    - **May Introduce Reduce/Reduce Conflicts:** While LALR(1) can resolve many conflicts that SLR(1) cannot, it may introduce reduce/reduce conflicts that do not exist in the corresponding LR(1) grammar. These conflicts usually have to be resolved by modyfying the grammar.
        
    - **Error Reporting Can be Tricky:** Because of the lookahead and the merging of states, error reporting in LALR(1) parsers can sometimes be less precise than in LL(1) parsers.
        

**4. LR(0) Grammars**

- **Advantages:**
    - **LR(0) grammars** are a type of context-free grammar used in the bottom-up parsing of programming languages.
    - **LR parsers** (Left-to-right, Rightmost derivation) are efficient and can handle a wide range of grammars.
    - The "(0)" indicates that the parser makes decisions based only on the current state and without looking ahead at any input symbols.
    - **Advantages of LR(0) grammars:** They are simple to understand and implement, at least conceptually. Parsing is very efficient, as no lookahead is needed. The parser's actions are determined solely by the current state.
	- **Simplest LR Parser:** LR(0) parsers are the simplest to understand and implement (at least conceptually) among the LR family.
	- **No Lookahead:** Parsing decisions are made solely based on the current state, leading to very fast parsing.
	- **Deterministic:** LR(0) parsing is deterministic.
        
- **Disadvantages:**
    
    - **Very Limited:** LR(0) is very limited in the types of grammars it can handle. Most practical programming languages are not LR(0).
        
    - **Many Conflicts:** LR(0) grammars are highly prone to shift/reduce and reduce/reduce conflicts, making them unsuitable for most real-world applications without significant modification.
        

**Summary Table**

|   |   |   |   |   |
|---|---|---|---|---|
|Feature|LL(1)|SLR(1)|LALR(1)|LR(0)|
|Power|Least Powerful|More Powerful than LR(0)|More Powerful than SLR(1)|Least Powerful|
|Table Size|Smallest|Larger than LL(1)|Smaller than LR(1)|Smallest|
|Complexity|Simple|Moderate|Complex|Simplest|
|Lookahead|1 Symbol|1 Symbol (computed simply)|1 Symbol (computed smartly)|No Lookahead|
|Conflicts|No|Fewer than LR(0)|May introduce R/R|Many S/R and R/R|
|Error Reporting|Good|Can be less precise|Can be tricky|Can be less precise|
|Practical Use|Limited, often hand-written|Limited|Widely used (e.g., Yacc)|Very Limited|

**In Conclusion**

- **LL(1)** is good for simple languages and when you want easy-to-understand, hand-written parsers.
    
- **LR(0)** is mostly of theoretical interest due to its limitations.
    
- **SLR(1)** is a step up from LR(0) but is still quite limited.
    
- **LALR(1)** is the most widely used in practice because it offers a good balance of power and efficiency.
    
- **LR(1)** is the most powerful but has larger tables and is more complex to implement, making LALR(1) often preferred.
    

---

## 3. **Left-recursion** Non-factored **Ambiguous grammars**

LL parsers are **top-down parsers** that work by predicting and matching tokens in a **left-to-right, leftmost derivation**. They have limitations when it comes to:

1. **Left-recursion**:  
    LL parsers cannot handle left-recursive grammars (e.g., `A → Aα | β`) because they would enter infinite recursion during the predictive parsing process.
    
2. **Non-factored grammars**:  
    Grammars with common prefixes (e.g., `A → αβ | αγ`) require **left-factoring** to remove ambiguity in the prediction step. Without factoring, the parser cannot decide which rule to apply.
    
3. **Ambiguous grammars**:  
    LL parsers cannot handle ambiguous grammars (e.g., grammars with multiple valid parse trees for a single string) because they rely on deterministic decision-making, which breaks down in cases of ambiguity.
    

In summary, LL parsers struggle with **left-recursion, non-factored grammars, and ambiguity** because these features prevent clear, deterministic predictions during parsing.

---
## 4. left-to-right, leftmost derivation
Let's break down the phrase **"left-to-right, leftmost derivation"** and explain what each word means in the context of parsing.


#### **Left-to-right (LTR)**

- This refers to the **order in which the input string is read by the parser**. A parser processes the string starting from the **leftmost character/token** and proceeds sequentially to the **rightmost character/token**.

#### **Examples of Left-to-Right (LTR) Parsing:**

For the string **"abcde"**, the parser reads **`a → b → c → d → e`** in order.

1. **Input:** `abc`  
    **Parsing sequence (LTR):** `a → b → c`
    
2. **Input:** `12345`  
    **Parsing sequence (LTR):** `1 → 2 → 3 → 4 → 5`
    
3. **Input:** `x + y * z`  
    **Parsing sequence (LTR):** `x → + → y → * → z`
    

#### **Examples of Right-to-Left (RTL) Parsing:**

For the same string **"abcde"**, the parser reads **`e → d → c → b → a`**.

1. **Input:** `abc`  
    **Parsing sequence (RTL):** `c → b → a`
    
2. **Input:** `12345`  
    **Parsing sequence (RTL):** `5 → 4 → 3 → 2 → 1`
    
3. **Input:** `x + y * z`  
    **Parsing sequence (RTL):** `z → * → y → + → x`
    

---

#### **Leftmost Derivation**

- This refers to the **order in which the non-terminals in the grammar are replaced** during parsing.
- In **leftmost derivation**, the **leftmost non-terminal** is always replaced first at each step.

#### **Grammar Example:**

Consider the grammar:

```
S → A B  
A → a  
B → b  
```

We want to derive the string **"ab"**.

1. Start with `S`.
2. Replace the **leftmost non-terminal** `A` first:  
    `S → A B → a B`
3. Replace the **next leftmost non-terminal** `B`:  
    `a B → a b`.

#### **Examples of Leftmost Derivations:**

1. **Grammar:**
    
    ```
    S → A B  
    A → x  
    B → y  
    ```
    
    Deriving `"xy"`:  
    `S → A B → x B → x y`
    
2. **Grammar:**
    
    ```
    S → T + T  
    T → a  
    ```
    
    Deriving `"a + a"`:  
    `S → T + T → a + T → a + a`
    
3. **Grammar:**
    
    ```
    S → X Y  
    X → x  
    Y → y z  
    ```
    
    Deriving `"xyz"`:  
    `S → X Y → x Y → x y z`
    

---

### **Comparison: Rightmost Derivation**

In **rightmost derivation**, the **rightmost non-terminal** is replaced first at each step.

For the same grammar above (`S → A B, A → a, B → b`) and string **"ab"**:

1. Start with `S`.
2. Replace the **rightmost non-terminal** `B` first:  
    `S → A B → A b`
3. Replace the **next rightmost non-terminal** `A`:  
    `A b → a b`.

#### **Examples of Rightmost Derivations:**

1. **Grammar:**
    
    ```
    S → A B  
    A → x  
    B → y  
    ```
    
    Deriving `"xy"`:  
    `S → A B → A y → x y`
    
2. **Grammar:**
    
    ```
    S → T + T  
    T → a  
    ```
    
    Deriving `"a + a"`:  
    `S → T + T → T + a → a + a`
    
3. **Grammar:**
    
    ```
    S → X Y  
    X → x  
    Y → y z  
    ```
    
    Deriving `"xyz"`:  
    `S → X Y → X y z → x y z`
    

---

### Summary Table of Examples:

|**Type**|**Example**|**Steps**|
|---|---|---|
|**Left-to-Right (LTR)**|String: `abc`|Read: `a → b → c`|
|**Right-to-Left (RTL)**|String: `abc`|Read: `c → b → a`|
|**Leftmost Derivation**|Grammar: `S → A B, A → a`|Steps: `S → A B → a B → a b`|
|**Rightmost Derivation**|Grammar: `S → A B, B → b`|Steps: `S → A B → A b → a b`|

