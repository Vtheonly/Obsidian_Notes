# Section 7: Fuzzy Inference Example (Mamdani Method - Corrected based on Slides)

#ai #fuzzy-logic #fis #inference #mamdani #example #corrected

This section details the fuzzy inference process step-by-step, based *accurately* on the provided slides ("Logique floue", "Base de règles floues", "Méthode de Mamdani - Etape 1 & 2"). The goal is to determine a fuzzy output for "vitesse" (speed) based on crisp inputs for "température" (temperature) and "humidité" (humidity), using the specific rules given.

## System Setup (From Slides)

*   **Input Variables:**
    *   `température` (T) with Universe of Discourse [14, 26]
    *   `humidité` (H) with Universe of Discourse [52, 100]
*   **Output Variable:**
    *   `vitesse` (V) with Universe of Discourse [0, 100]
*   **Membership Functions (MFs):** As shown in the first slide ("Trois variables linguistiques").
    *   `température`: `Faible`, `Moyenne`, `Élevée`
    *   `humidité`: `Sec`, `Humide`
    *   `vitesse`: `Faible`, `Moyenne`, `Élevée`
*   **Rule Base (From "Base de règles floues" Slide):**
    *   **Rule 1:** SI `température` est `faible` **OU** `humidité` est `sec` ALORS `vitesse` est `faible`. (Uses **OR**)
    *   **Rule 2:** SI `température` est `moyenne` **ET** `humidité` est `humide` ALORS `vitesse` est `moyenne`. (Uses **AND**)
    *   **Rule 3:** SI `température` est `élevée` ALORS `vitesse` est `élevée`. (Single antecedent)
*   **Crisp Inputs (From "Etape 1" Slide):**
    *   `température` = 18
    *   `humidité` = 80

## Inference Process Step-by-Step (Following Slides)

### Step 1: Fuzzification (As shown in "Etape 1" Slide)

Determine the degree of membership of the crisp inputs in the relevant fuzzy sets.

*   **For `température` = 18:**
    *   $\mu_{Faible}(18) = 0.5$
    *   $\mu_{Moyenne}(18) = 0.33$
    *   $\mu_{Élevée}(18) = 0.0$
*   **For `humidité` = 80:**
    *   $\mu_{Sec}(80) = 0.25$
    *   $\mu_{Humide}(80) = 0.75$

### Step 2: Rule Evaluation & Implication (Mamdani - As shown in "Etape 2" Slide)

Evaluate each rule's antecedent (IF part) to find its firing strength ($\alpha$), then apply this strength to its consequent (THEN part) using clipping.

*   **Rule 1: IF T is `Faible` OR H is `Sec` THEN V is `Faible`**
    1.  **Antecedent Evaluation:** The rule uses **OR**. We use the `max` operator for fuzzy OR, as indicated by "MAX" on the top row of the "Etape 2" slide.
        *   Firing Strength $\alpha_1 = \max(\mu_{Faible}(18), \mu_{Sec}(80))$
        *   $\alpha_1 = \max(0.5, 0.25) = 0.5$
    2.  **Implication (Clipping):** Apply $\alpha_1$ to the consequent "V is `Faible`". Clip the `Faible` MF for `vitesse` at the height of 0.5.
        *   The resulting fuzzy set $\mu_{output1}(V)$ is the original $\mu_{Faible}(V)$ shape cut off at a maximum value of 0.5. This is the green shaded area in the **top-right** graph of "Etape 2".
        *   Mathematically: $\mu_{output1}(V) = \min(\alpha_1, \mu_{Faible}(V)) = \min(0.5, \mu_{Faible}(V))$.

*   **Rule 2: IF T is `Moyenne` AND H is `Humide` THEN V is `Moyenne`**
    1.  **Antecedent Evaluation:** The rule uses **AND**. We use the `min` operator, as indicated by "MIN" on the middle row of the "Etape 2" slide.
        *   Firing Strength $\alpha_2 = \min(\mu_{Moyenne}(18), \mu_{Humide}(80))$
        *   $\alpha_2 = \min(0.33, 0.75) = 0.33$
    2.  **Implication (Clipping):** Apply $\alpha_2$ to the consequent "V is `Moyenne`". Clip the `Moyenne` MF for `vitesse` at the height of 0.33.
        *   The resulting fuzzy set $\mu_{output2}(V)$ is the original $\mu_{Moyenne}(V)$ shape cut off at a maximum value of 0.33. This is the green shaded area in the **middle-right** graph of "Etape 2".
        *   Mathematically: $\mu_{output2}(V) = \min(\alpha_2, \mu_{Moyenne}(V)) = \min(0.33, \mu_{Moyenne}(V))$.

*   **Rule 3: IF T is `Élevée` THEN V is `Élevée`**
    1.  **Antecedent Evaluation:** Single antecedent.
        *   Firing Strength $\alpha_3 = \mu_{Élevée}(18) = 0.0$
    2.  **Implication (Clipping):** Apply $\alpha_3$ to the consequent "V is `Élevée`". Clip the `Élevée` MF for `vitesse` at the height of 0.0.
        *   The resulting fuzzy set $\mu_{output3}(V)$ has zero membership everywhere. This rule contributes nothing to the final output for these inputs, as shown by the unshaded yellow area in the **bottom-right** graph (representing the original $\mu_{Élevée}(V)$ before clipping).
        *   Mathematically: $\mu_{output3}(V) = \min(\alpha_3, \mu_{Élevée}(V)) = \min(0.0, \mu_{Élevée}(V)) = 0$.

### Step 3: Aggregation of Rule Outputs (Mamdani: MAX)

Combine the fuzzy sets resulting from the implication step of all active rules ($\alpha > 0$) into a single fuzzy set for the output variable `vitesse`. The standard Mamdani aggregation method uses the `max` operator, as indicated by "MAX" applied to the final aggregation in the "Etape 2" slide.

1.  **Combine Outputs:** We combine the outputs from Rule 1 and Rule 2 (Rule 3 contributes nothing).
    *   $\mu_{output1}(V)$ (clipped `Faible` at 0.5)
    *   $\mu_{output2}(V)$ (clipped `Moyenne` at 0.33)
2.  **Apply MAX Operator:** The membership function of the final aggregated fuzzy set, $\mu_{aggregated}(V)$, is the point-wise maximum of the individual rule outputs.
    *   $\mu_{aggregated}(V) = \max(\mu_{output1}(V), \mu_{output2}(V), \mu_{output3}(V))$
    *   $\mu_{aggregated}(V) = \max(\min(0.5, \mu_{Faible}(V)), \min(0.33, \mu_{Moyenne}(V)), 0)$
3.  **Resulting Shape:** This aggregated fuzzy set is precisely the one shown in the **bottom-right** graph of "Etape 2", labeled "Firing and aggregation".
    *   It takes the shape of the `Faible` fuzzy set clipped at 0.5 for lower `vitesse` values.
    *   It includes the portion of the `Moyenne` fuzzy set clipped at 0.33 where that value is higher than the clipped `Faible` set (which doesn't happen in this specific case, as the clipped `Faible` shape at 0.5 completely covers the area where the clipped `Moyenne` at 0.33 exists).
    *   The overall shape is determined by the union (point-wise maximum) of the two green shaded areas from the top-right and middle-right graphs. The peak membership value of this aggregated set is 0.5.

## Conclusion of Inference (Corrected)

The Inference Engine process, correctly applying the rules from the slides using the Mamdani method (MAX for OR, MIN for AND, MIN for implication/clipping, MAX for aggregation), takes the crisp inputs (T=18, H=80), fuzzifies them, evaluates the rules to find firing strengths ($\alpha_1=0.5$, $\alpha_2=0.33$, $\alpha_3=0.0$), clips the corresponding output fuzzy sets, and finally aggregates these clipped sets using `max`.

The output of "Etape 2" is the **aggregated fuzzy set** shown in the bottom-right graph of the inference slide. This correctly represents the system's fuzzy recommendation for the `vitesse`, peaking at a membership degree of 0.5. The next step would be Defuzzification.