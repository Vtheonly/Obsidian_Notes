

#ai #fuzzy-logic #operations #rules #inference

## Fuzzy Set Operations

Similar to classical sets, operations can be performed on fuzzy sets. The primary ones are Complement, Intersection, and Union.

*   **Complement (NOT):** Represents the degree to which an element *does not* belong to a fuzzy set.
    *   `μ¬A(x) = 1 - μA(x)`
    *   *Example:* If the membership degree of temperature `T=18°C` in the set `Faible` (Low) is `μFaible(18) = 0.5`, then the membership degree in `NOT Faible` is `1 - 0.5 = 0.5`.
*   **Intersection (AND):** Represents the degree to which an element belongs to *both* fuzzy sets A and B. Often calculated using the `min` operator.
    *   `μA∩B(x) = min(μA(x), μB(x))`
    *   *Example:* For `T=18°C`, `μFaible(18) = 0.5` and `μMoyenne(18) = 0.33`. The degree of membership in `Faible AND Moyenne` is `min(0.5, 0.33) = 0.33`.
*   **Union (OR):** Represents the degree to which an element belongs to *either* fuzzy set A or fuzzy set B (or both). Often calculated using the `max` operator.
    *   `μA∪B(x) = max(μA(x), μB(x))`
    *   *Example:* For `T=18°C`, the degree of membership in `Faible OR Moyenne` is `max(0.5, 0.33) = 0.5`.

    ![[Fuzzy_Set_Operations_Graph.png]] *(Placeholder for the graphical representation of operations from slide 4)*

## Fuzzy Rules (IF-THEN)

Fuzzy rules form the core of a fuzzy inference system. They are expressed in a human-readable IF-THEN format to capture knowledge.

*   **Structure:** `IF <antecedent> THEN <consequent>`
    *   **Antecedent (Premise):** The condition part (IF). It typically involves one or more linguistic variables connected by fuzzy operators (AND, OR).
    *   **Consequent (Conclusion):** The action or result part (THEN). It usually defines the fuzzy set assigned to an output linguistic variable.

*   **Example Rule:**
    *   `IF Temperature IS Faible (Low) THEN Chauffage (Heating) IS Fort (High)`
    *   This rule links the input linguistic variable `Temperature` with the output linguistic variable `Chauffage`.

*   **Rule Base:** A collection of fuzzy rules that defines the behavior of the fuzzy system.

*   **Inference Methods:** Different methods exist to interpret these rules and combine their results, most notably:
    *   **Mamdani Method:** Widely used, produces a fuzzy set as output. (Implicitly used in the examples shown).
    *   **Sugeno Method (TSK - Takagi-Sugeno-Kang):** Often used in control systems, produces a crisp value or a linear function as output.