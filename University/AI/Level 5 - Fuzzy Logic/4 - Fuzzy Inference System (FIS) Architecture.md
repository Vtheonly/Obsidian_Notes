

#ai #fuzzy-logic #fis #architecture #fuzzification #inference #defuzzification

A Fuzzy Inference System (FIS) is the process of mapping from a given input to an output using fuzzy logic. It typically consists of four main components:

1.  **Fuzzification Module:**
    *   **Purpose:** Converts crisp (real-world, numerical) input values into fuzzy values (degrees of membership in fuzzy sets).
    *   **Process:** Takes the input variables and determines the degree to which they belong to each of the appropriate fuzzy sets using the defined [[4.1 - membership functions]].
    *   *Example:* If the input temperature is 21°C, the fuzzification module would calculate its degree of membership in the fuzzy sets `Moyenne` (Medium) and `Élevée` (High) based on their respective membership functions (e.g., `μMoyenne(21) = 0.5`, `μÉlevée(21) = 0.2`).

2.  **Rule Base:**
    *   **Purpose:** Stores the collection of fuzzy IF-THEN rules provided by experts or derived from data.
    *   **Content:** Contains the linguistic rules that describe how the system should make decisions based on the fuzzy inputs. (See Section 3 for rule examples).

3.  **Inference Engine:**
    *   **Purpose:** Simulates human reasoning by making inferences based on the fuzzy inputs and the rules in the Rule Base.
    *   **Process:**
        *   Takes the fuzzified inputs.
        *   Evaluates the antecedents (IF parts) of all relevant rules. This involves applying fuzzy operators (like AND/min, OR/max) to the membership degrees of the inputs. The result is the "firing strength" or "truth value" of each rule's premise.
        *   Applies the firing strength to the consequent (THEN part) of each triggered rule. This typically involves "clipping" or "scaling" the output fuzzy set defined in the consequent (using methods like Mamdani's min/max or Sugeno's approach).
        *   Aggregates the results from all triggered rules to form a single fuzzy set (or a crisp value/function in Sugeno) representing the overall output.

4.  **Defuzzification Module:**
    *   **Purpose:** Converts the aggregated fuzzy output set from the inference engine back into a single crisp (numerical) value.
    *   **Necessity:** Real-world systems often require a specific, actionable numerical output (e.g., exact fan speed, precise valve opening).
    *   **Common Methods:**
        *   **Centroid (Center of Gravity - COG):** Calculates the center of the area under the aggregated fuzzy output set. This is the most common method.
        *   **Bisector:** Finds the vertical line that divides the area into two equal halves.
        *   **Mean of Maximum (MOM):** Takes the average of the values with the highest membership degree.
        *   **Smallest of Maximum (SOM), Largest of Maximum (LOM):** Uses the smallest or largest value among those with the maximum membership degree.
    *   *Example:* If the aggregated fuzzy output for `Chauffage` (Heating) is a complex shape, the defuzzification module (e.g., using Centroid) might calculate a single crisp output value like "Set heating power to 75%".