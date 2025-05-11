[[TP 5.1 Chaining]]
## A. Forward Chaining

The following code introduces the data from the course example. Execute it up to line 10.

```R
  verbose <- TRUE
  # Data Acquisition
  if (verbose) { # Course Example
    BF <- list("D", "E", "F") # Fact Base (Base de Faits)
    BR <- list( # Rule Base (Base de Règles)
      list("A", "B", "C"), # R1: A & B => C
      list("D","C"),        # R2: D => C
      list("C", "E","F","G") # R3: C & E & F => G
    )
   BUT <- "G" # Goal (But)
 } else {
   # (Code for interactive input would go here)
 }
 # ... (rest of the script)
 names(BF) <- paste0("F", 1:length(BF))
 names(BR) <- paste0("R", 1:length(BR))
```

**Q1: What data structure is used to implement the fact base and the rule base in this code?**
*   **Answer:** Both the fact base (`BF`) and the rule base (`BR`) are implemented using R **lists**.
    *   `BF` is a simple list where each element is a character string representing a single fact.
    *   `BR` is a list of lists. Each inner list represents a single rule.

**Q2: In the structure associated with the rule base, identify the antecedent and the conclusion.**
*   **Answer:** In each inner list representing a rule (e.g., `list("A", "B", "C")`):
    *   The **antecedent** (or premises/conditions) consists of all elements *except the last one* (e.g., "A", "B").
    *   The **conclusion** (or consequent) is the *very last element* (e.g., "C").

**Q3: What is the role of lines 29 and 30? Show BF and BR before and after their execution and view the `paste()` function in the help.**
*   **Answer:** Lines 29 and 30 assign names to the elements of the `BF` and `BR` lists using the `names()` function and `paste0()`.
    *   `names(BF) <- paste0("F", 1:length(BF))` creates names "F1", "F2", "F3", ... for the facts.
    *   `names(BR) <- paste0("R", 1:length(BR))` creates names "R1", "R2", "R3", ... for the rules.
    *   This makes the lists easier to read and reference during debugging or analysis. `paste0()` concatenates strings without any separator.

    *Before execution:*
    ```R
    > BF
    [[1]]
    [1] "D"
    [[2]]
    [1] "E"
    [[3]]
    [1] "F"
    > BR
    [[1]]
    [1] "A" "B" "C"
    [[2]]
    [1] "D" "C"
    [[3]]
    [1] "C" "E" "F" "G"
    ```
    *After execution:*
    ```R
    > BF
    $F1
    [1] "D"
    $F2
    [1] "E"
    $F3
    [1] "F"
    > BR
    $R1
    [1] "A" "B" "C"
    $R2
    [1] "D" "C"
    $R3
    [1] "C" "E" "F" "G"
    ```
    *(Viewing `?paste` or `?paste0` in R provides help on string concatenation.)*

The rest of the script is given in the code on the following page. Answer the following questions without executing it yet.

```r
# Strategie Premiere regle declanchable
getFirstActvRule <- function(BF,BR){
  for(i in 1:length(BR)){
    nbrAntcd <- length(BR[[i]])-1
    if(sum(sapply(BR[[i]][1:nbrAntcd], function(x) x %in% BF))==nbrAntcd){
      return(i)
    }
  }
  return(0)
}


# Chainage Avant
frwdChain <- function(BF,BR,BUT){
  if(BUT %in% BF) return(TRUE)
  activeRule <- getFirstActvRule(BF,BR)
  if(activeRule == 0){
    return(FALSE)
  }else{
    conclusion <- BR[[activeRule]][length(BR[[activeRule]])];
    if(!(conclusion %in% BF)) BF <- append(BF,conclusion)
    BR[[activeRule]] <- NULL
    if(verbose){
      cat("\n Forward Chaining in progress ...")
      printSysExp(BF,BR)
    }
    return(frwdChain(BF,BR,BUT))
  }
}
```



*(Image shows line 57: `return(frwdChain(BF, BR, BUT))`)*

**Q4: Identify the function that implements forward chaining. What are its arguments?**
*   **Answer:** The function is `frwdChain`. Its arguments are `BF` (Fact Base), `BR` (Rule Base), and `BUT` (Goal).

**Q5: Is this function recursive or iterative? Justify.**
*   **Answer:** The function `frwdChain` is **recursive**. The justification is the statement `return(frwdChain(BF, BR, BUT))` on line 57, where the function calls itself.

*(Image shows line 45: `if(BUT %in% BF) return(TRUE)`)*

**Q6: What is the role of the conditional statement on line 45?**
*   **Answer:** Line 45 `if(BUT %in% BF) return(TRUE)` is the primary success **termination condition** for the recursion. It checks if the `BUT` (goal) is present in the current `BF` (fact base). If it is, the forward chaining process has successfully reached the goal, and the function returns `TRUE`.

*(Image shows lines 46-48: `activeRule <- getFirstActvRule(BF, BR)` `if (activeRule == 0){ return(FALSE) }`)*

**Q7: Is there another termination condition for the recursion? Identify the corresponding line of code and determine which function's return value it depends on.**
*   **Answer:** Yes, there is another termination condition on lines 47-48: `if (activeRule == 0){ return(FALSE) }`. This condition acts as a failure **termination condition**. It triggers when no more rules can be activated (fired). It depends on the return value of the `getFirstActvRule(BF, BR)` function (called on line 46). If `getFirstActvRule` returns 0, it means no activatable rule was found, the chaining process cannot proceed further, and `frwdChain` returns `FALSE`.

```R
 # Strategy: First activatable rule
 getFirstActvRule <- function(BF, BR) {
   for (i in 1:length(BR)) {
     nbrAntcd <- length(BR[[i]]) - 1
     if (nbrAntcd == 0) { # Rule with no antecedents
        # Handle rules with no antecedents if necessary, maybe return i immediately
        # Or ensure nbrAntcd is never 0 if rules must have antecedents
        # Current logic might skip rules like list("X") if nbrAntcd becomes 0
        # Assuming rules always have at least one antecedent and one conclusion
        # If a rule can just be a conclusion like list("C"), nbrAntcd would be 0.
        # Let's assume rules have at least one antecedent for this logic.
        # If nbrAntcd can be 0, line 36 needs adjustment.
        # For simplicity, let's assume length(BR[[i]]) >= 2
           next # Skip rules without antecedents based on current logic
        }
        # Check if all antecedents are in BF
        is_activatable <- sum(sapply(BR[[i]][1:nbrAntcd], function(x) x %in% BF)) == nbrAntcd
      if (is_activatable) {
        return(i) # Return index of the first activatable rule
      }
   }
   return(0) # Return 0 if no rule is activatable
 }

 # Forward Chaining
 frwdChain <- function(BF, BR, BUT) {
   if (BUT %in% BF) return(TRUE) # Goal reached (Q6)

   activeRule <- getFirstActvRule(BF, BR) # Find a rule to fire (Q8)

   if (activeRule == 0) { # No rule can fire (Q7)
     return(FALSE)
   } else {
     conclusion <- BR[[activeRule]][[length(BR[[activeRule]])]] # Get conclusion

     # Add conclusion to BF only if it's new
     if (!(conclusion %in% BF)) {
       BF <- append(BF, conclusion)
       # Optionally re-assign names if needed, e.g., after append
       # names(BF) <- paste0("F", 1:length(BF)) # Be careful with performance
     }

     # Remove the rule that just fired (set to NULL)
     BR_updated <- BR
     BR_updated[[activeRule]] <- NULL
     # Keep only non-NULL elements if rules are removed frequently
     # BR_updated <- BR_updated[!sapply(BR_updated, is.null)] # Can be slow

     if (verbose) {
       cat("\n Forward Chaining in progress ... Rule", names(BR)[activeRule], "fired.\n")
       # printSysExp(BF, BR_updated) # Assuming printSysExp exists
       print("Current BF:")
       print(BF)
       # print("Current BR:")
       # print(BR_updated) # Printing large BR can be slow
     }

     # Recursive call with updated BF and BR (Q5, Q14)
     return(frwdChain(BF, BR_updated, BUT))
   }
 }
```
*(Note: Added checks/comments around line 36 in `getFirstActvRule` regarding rules with no antecedents, and slightly modified the main loop structure for clarity)*

**Q8: What is the role of the `getFirstActvRule()` function and what are its arguments?**
*   **Answer:** The role of `getFirstActvRule` is to find the index of the **first** rule in the Rule Base (`BR`) whose antecedents are all present in the current Fact Base (`BF`). It implements the "first activatable rule" conflict resolution strategy. Its arguments are `BF` (Fact Base) and `BR` (Rule Base). It returns the index (e.g., 1, 2, 3...) of the first activatable rule found, or `0` if no rule can be activated.

**Q9: In line 35, what value is assigned to the variable `nbrAntcd` during the 1st iteration of the for loop?**
*   **Answer:** In the first iteration (`i=1`), `BR[[1]]` is `list("A", "B", "C")`. The length `length(BR[[1]])` is 3. Therefore, `nbrAntcd` is assigned the value `3 - 1 = 2`.

**Q10: Under what conditions can the `for` loop (in `getFirstActvRule`) be exited?**
*   **Answer:** The loop can be exited in two main ways:
    1.  If an activatable rule is found (the condition `is_activatable` on line 45 is `TRUE`), the `return(i)` statement on line 46 is executed, immediately exiting both the loop and the function.
    2.  If the loop iterates through all the rules in `BR` without finding an activatable one, the loop completes normally, and the function proceeds to line 49 (`return(0)`), exiting the function.

**Q11: Using copy-paste from lines 35 and 45 to the console, replace the variable `i` with the value 1 to create and execute the following code. Do the same for values 2 and 3.**
*   *(Assuming initial BF is `list("D", "E", "F")` and BR is the course example)*

```R
# For i = 1 (Rule R1: A, B => C)
i <- 1
nbrAntcd <- length(BR[[i]]) - 1 # nbrAntcd = 2
sapply(BR[[i]][1:nbrAntcd], function(x) x %in% BF)
# Output: [1] FALSE FALSE
sum(sapply(BR[[i]][1:nbrAntcd], function(x) x %in% BF)) == nbrAntcd
# Output: [1] FALSE (0 == 2 is FALSE)

# For i = 2 (Rule R2: D => C)
i <- 2
nbrAntcd <- length(BR[[i]]) - 1 # nbrAntcd = 1
sapply(BR[[i]][1:nbrAntcd], function(x) x %in% BF)
# Output: [1] TRUE
sum(sapply(BR[[i]][1:nbrAntcd], function(x) x %in% BF)) == nbrAntcd
# Output: [1] TRUE (1 == 1 is TRUE)

# For i = 3 (Rule R3: C, E, F => G)
i <- 3
nbrAntcd <- length(BR[[i]]) - 1 # nbrAntcd = 3
sapply(BR[[i]][1:nbrAntcd], function(x) x %in% BF)
# Output: [1] FALSE  TRUE  TRUE
sum(sapply(BR[[i]][1:nbrAntcd], function(x) x %in% BF)) == nbrAntcd
# Output: [1] FALSE (2 == 3 is FALSE)
```

**Q12: Check the console outputs using the rule base from the course example, then using the Help (see next screenshot showing `sapply`), deduce what the condition on line 45 does.**
*   **Answer:** The condition `sum(sapply(BR[[i]][1:nbrAntcd], function(x) x %in% BF)) == nbrAntcd` (line 45 in the modified code block, corresponds to line 36 in the original image) checks if a rule is activatable.
    *   `BR[[i]][1:nbrAntcd]` extracts the list of antecedents for the current rule `i`.
    *   `sapply(..., function(x) x %in% BF)` applies a check to each antecedent (`x`). The check `x %in% BF` returns `TRUE` if the antecedent is found in the Fact Base (`BF`) and `FALSE` otherwise. `sapply` returns a logical vector (e.g., `c(FALSE, TRUE, TRUE)`).
    *   `sum(...)` then sums this logical vector, treating `TRUE` as 1 and `FALSE` as 0. This effectively counts how many of the rule's antecedents are present in `BF`.
    *   `== nbrAntcd` compares this count to the total number of antecedents for that rule (`nbrAntcd`).
    *   If the sum equals the total number of antecedents, it means **all** antecedents are present in `BF`, the condition is `TRUE`, and the rule is activatable.

**Q13: Which lines of code are executed if an active rule is found? Explain them.**
*   **Answer:** If `getFirstActvRule` returns a non-zero value (`activeRule`), the `else` block starting on line 60 is executed:
    *   **Line 61:** `conclusion <- BR[[activeRule]][[length(BR[[activeRule]])]]`: Extracts the conclusion (the last element) of the activated rule.
    *   **Lines 64-65:** `if (!(conclusion %in% BF)) { BF <- append(BF, conclusion) }`: Checks if the conclusion is *not* already in the Fact Base. If it's a new fact, it's added to `BF` using `append()`. This prevents adding duplicate facts and potentially infinite loops.
    *   **Lines 71-72:** `BR_updated <- BR; BR_updated[[activeRule]] <- NULL`: Creates a copy of the rule base and removes the rule that just fired by setting its element to `NULL`. This prevents the *same rule instance* from firing again immediately in the next recursive step (a common strategy in simple forward chaining).
    *   **Lines 76-83:** `if (verbose) {...}`: If `verbose` is `TRUE`, it prints progress messages, showing which rule fired and the current state (optional).
    *   **Line 86:** `return(frwdChain(BF, BR_updated, BUT))`: Makes the **recursive call** to continue the chaining process with the potentially updated Fact Base (`BF`) and the modified Rule Base (`BR_updated`).

**Q14: Deduce the modifications made to the arguments sent in the recursive call.**
*   **Answer:** In the recursive call `frwdChain(BF, BR_updated, BUT)` on line 86:
    *   `BF`: May contain a new fact (the conclusion of the rule that just fired) if it wasn't already present.
    *   `BR_updated`: Is different from the `BR` received by the current function call because the rule that just fired (`activeRule`) has been removed (set to `NULL`).
    *   `BUT`: The goal remains unchanged and is passed along to the next recursive call.

**Q15: Execute the entire code using the source button, then analyze the console output. Does it correspond to the expected result?**
*   **Answer:** Yes, the console output shown in the screenshot corresponds to the expected result for this example.
    *   **Initial State:** BF={D, E, F}, BR={R1:[A,B=>C], R2:[D=>C], R3:[C,E,F=>G]}, BUT=G.
    *   **Step 1:** `getFirstActvRule` finds R2 (D=>C) is activatable. `frwdChain` fires R2. 'C' is added to BF. BF becomes {D, E, F, C}. R2 is removed from BR for the next step. Recursive call.
    *   **Step 2:** `getFirstActvRule` (with updated BF & BR) finds R3 (C&E&F=>G) is activatable. `frwdChain` fires R3. 'G' is added to BF. BF becomes {D, E, F, C, G}. R3 is removed from BR. Recursive call.
    *   **Step 3:** In the next call, the condition `if (BUT %in% BF)` (line 54) becomes true because 'G' is now in BF. The function returns `TRUE`.
    *   The final output shows `Resultat: BUT = "G" proven? TRUE`.

*(Screenshot shows initial system, steps of forward chaining adding C then G, and final result TRUE)*

**Q16: Display the content of the fact base and the rule base on the console. What do you notice?**
*   **Answer:** The screenshot showing the output of `printSysExp(BF,BR)` (a presumed helper function) or similar command displays the BF and BR, likely using the names assigned earlier (F1, F2, R1, R2 etc.). We notice it provides a structured view, showing facts like `F1: D` and rules like `R2: D => C`, making it easier to understand the system's state at a given point compared to just printing the raw R list structure.

*(Screenshot shows BF with F1="D", F2="E", F3="F" and BR with R1, R2, R3)*

**Q17: Deduce the default argument passing mechanism used by R.**
*   **Answer:** R uses a **pass-by-value** mechanism, often implemented with optimizations like **copy-on-modify**. When arguments like lists (`BF`, `BR`) are passed to `frwdChain`, the function initially works with references. However, as soon as the function *modifies* one of these arguments (e.g., `BF <- append(BF, conclusion)` or creating `BR_updated` and setting an element to `NULL`), R typically creates a *local copy* of that object within the function's environment. The modifications affect this local copy. Crucially, in recursion, this modified local copy is then passed as the argument to the *next* recursive call (line 86). This allows the state changes (added facts, removed rules) to propagate through the chain of recursive calls. The original objects outside the *initial* call to `frwdChain` remain unchanged unless the final result is explicitly assigned back to them.

**Q18: Replace the `if` condition on line 3 with `FALSE`.**
*   **Answer:** If the condition `if (verbose)` on line 3 is replaced with `if (FALSE)`, the block of code defining the initial example BF, BR, and BUT (lines 4-10) will be skipped. Instead, the `else` block (lines 11 onwards, shown in the screenshot for Q20 containing interactive input prompts) will be executed. This part of the script allows the user to define the Fact Base and Rule Base interactively.

**Q19: Use the Help to find out the role of the `as.list()` function.**
*   **Answer:** The `as.list()` function attempts to **coerce** its argument into an R list. For example, if `facts` is a character vector `c("A", "B")` obtained from `scan(what="")`, then `as.list(facts)` converts it into `list("A", "B")`. This is used in the interactive part (lines 14 and 23 in the screenshot) to ensure `BF` and the individual rules within `BR` are stored as lists, consistent with the structure used in the example.

**Q20: Clear the workspace, execute using the source button, then enter the data from the course exercise.**
*   **Answer:** After clearing the workspace (e.g., `rm(list=ls())`) and running the script (with the line 3 condition set to `FALSE`), the interactive input prompts appear:
    1.  `Introduire la base des faits (lettres en majuscule):` -> User enters `A`, then `B`, then presses Enter on a blank line. `BF` becomes `list("A", "B")`.
    2.  `Introduire la taille de la base des regles:` -> User enters `4`.
    3.  `Introduction de la BR...`
    4.  `Introduire la regle 1:` -> User enters `A`, `C`, `F`. `BR[[1]]` becomes `list("A", "C", "F")`.
    5.  `Introduire la regle 2:` -> User enters `A`, `E`, `G`. `BR[[2]]` becomes `list("A", "E", "G")`.
    6.  `Introduire la regle 3:` -> User enters `B`, `E`. `BR[[3]]` becomes `list("B", "E")`.
    7.  `Introduire la regle 4:` -> User enters `G`, `D`. `BR[[4]]` becomes `list("G", "D")`.
    8.  The `BUT` variable would need to be set, presumably to `D` for this exercise run, either within the script or manually after sourcing.

**Q21: Execute then verify if the obtained result corresponds to the expected one.**
*   **Answer:** Yes, the execution trace shown in the screenshot corresponds to the expected forward chaining result for the interactively entered data (BF={A, B}, BR={R1:[A,C=>F], R2:[A,E=>G], R3:[B=>E], R4:[G=>D]}, BUT=D).
    *   **Start:** BF={A, B}.
    *   **Step 1:** Rule R3 (B=>E) fires. BF becomes {A, B, E}.
    *   **Step 2:** Rule R2 (A&E=>G) fires. BF becomes {A, B, E, G}.
    *   **Step 3:** Rule R4 (G=>D) fires. BF becomes {A, B, E, G, D}.
    *   **Step 4:** Goal `D` is now in BF. The function returns `TRUE`.
    *   The final output confirms `BUT = "D" proven? TRUE`.

**Q22: What is the expected result if we consider the expert system without R3?**
*   **Answer:** If Rule R3 (B=>E) is removed, the expected result is `FALSE`.
    *   **Start:** BF={A, B}, BR={R1:[A,C=>F], R2:[A,E=>G], R4:[G=>D]}, BUT=D.
    *   **Step 1:** `getFirstActvRule` checks the rules:
        *   R1 needs 'C' (not in BF).
        *   R2 needs 'E' (not in BF).
        *   R4 needs 'G' (not in BF).
    *   No rule is activatable. `getFirstActvRule` returns 0.
    *   `frwdChain` returns `FALSE`. The goal `D` cannot be proven because 'E' is never added to the fact base, preventing R2 and subsequently R4 from firing.

**Q23: Clear the workspace then verify your manual result using the script.**
*   **Answer:** To verify the result from Q22:
    1.  Clear the workspace (`rm(list=ls())`).
    2.  Ensure line 3's condition is `FALSE` to enable interactive input.
    3.  Run the script (`source(...)`).
    4.  Enter facts: `A`, `B`.
    5.  Enter number of rules: `3`.
    6.  Enter Rule 1 (original R1): `A`, `C`, `F`.
    7.  Enter Rule 2 (original R2): `A`, `E`, `G`.
    8.  Enter Rule 3 (original R4): `G`, `D`.
    9.  Manually set the goal after sourcing the functions or modify the script to set it: `BUT <- "D"`.
    10. Execute `frwdChain(BF, BR, BUT)`.
    11. The script should output `FALSE` (or the equivalent based on the script's final print statement), confirming the manual trace.

---

## B. Backward Chaining (Homework)

**Q1: Using the same structures to represent the fact base and rule base, the `bcwdChain(BF, BR, BUT)` function in the following script (see next page) implements an inference engine with backward chaining. For the course example, the complete script gives the following output:**

*(Screenshot shows backward chaining trace: Goal H -> Needs A -> Needs F -> Needs D&E -> Needs C -> Proven D -> Proven E -> Proven F -> Proven A -> Proven H. Result TRUE)*

**Q2: Draw the AND/OR tree generated by this backward chaining.**
*   **Answer:** The AND/OR search tree starts with the goal H and expands based on rules that conclude the current goal/subgoal. (Simplified based on trace):
    *   **H (Goal)**
        *   OR (Requires Rule R6: A => H)
            *   **A (Subgoal)** (AND node from R6)
                *   OR (Requires R2:D&G=>A, R3:C&F=>A, R8:X&C=>A)
                    *   *(Branch for R2 - likely fails as G cannot be proven)*
                    *   *(Branch for R8 - likely fails as X cannot be proven)*
                    *   *(Branch for R3: C & F => A)*
                        *   **C (Subgoal)** (AND node from R3) -> Found in initial BF. **OK**.
                        *   **F (Subgoal)** (AND node from R3)
                            *   OR (Requires R1: B&D&E => F)
                                *   **B (Subgoal)** (AND node from R1) -> Found in initial BF. **OK**.
                                *   **D (Subgoal)** (AND node from R1)
                                    *   OR (Requires R4: C => D)
                                        *   **C (Subgoal)** (AND node from R4) -> Found in initial BF. **OK**. -> D is proven.
                                *   **E (Subgoal)** (AND node from R1)
                                    *   OR (Requires R5: D => E)
                                        *   **D (Subgoal)** (AND node from R5) -> Proven above. **OK**. -> E is proven.
                                *   (B, D, E proven) -> F is proven.
                        *   (C, F proven) -> A is proven.
            *   (A proven) -> H is proven.

**Q3: Does this solution take into account subgoals proven along the way (look closely at the highlighted zones)?**
*   **Answer:** The trace shows `current proven BUT: D` appearing multiple times. This indicates that when the recursive call for subgoal 'D' succeeds, the calling function recognizes this success. However, the *basic* `bcwdChain` implementation shown likely **does not** modify the global `BF` to store 'D' permanently. It only uses the `TRUE` return value to satisfy the immediate requirement within that specific branch (e.g., proving 'F' required proving 'D' and 'E'). If 'D' were needed again in a *different* part of the search tree, this simple implementation would likely try to prove it again from scratch, as it only checks the *initial* BF and its current recursive goal stack. (See Extension Q2 for improvement).

**Q4: Analyze the `bcwdChain(BF, BR, BUT)` function and explain how recursion is invoked.**
*   **Answer:** The `bcwdChain` function is recursive:
    1.  **Base Case 1 (Success):** It first checks if the current `BUT` is already in the initial `BF` (line 50: `if(BUT %in% BF) return(TRUE)`).
    2.  **Find Relevant Rules:** It finds a rule (`chosenRule`) that concludes the `BUT` (line 51: using `getLeastUnkRule`, which presumably selects a rule concluding `BUT`).
    3.  **Base Case 2 (Failure):** If no rule concludes the `BUT` (`chosenRule == 0`), it returns `FALSE` (line 55).
    4.  **Check Antecedents:** If a rule is found, it checks if all its antecedents are already in `BF` (line 56). If yes, the `BUT` is proven, return `TRUE`.
    5.  **Recursive Step:** If the rule has antecedents not in `BF` (`else` on line 61):
        *   It identifies the unknown antecedents (`unkPos`, line 63-68).
        *   It uses `sapply` (line 69) to iterate through these unknown positions.
        *   For **each** unknown antecedent (`x`), it makes a **recursive call** `bcwdChain(BF, BR, as.character(BR[[chosenRule]][x]))` (line 72). This call treats the unknown antecedent as a new `BUT` (a subgoal).
        *   The function only returns `TRUE` (line 77) if the `sum` of the results of *all* these recursive calls equals the number of unknown antecedents (`length(unkPos)`), meaning all subgoals were successfully proven (line 76). Otherwise, it returns `FALSE`.

**Q5: Complete the script.**
*   **Answer:** "Completing the script" likely involves:
    1.  **Implementing `getLeastUnkRule(BF, BR, BUT)`:** This helper function (called on line 51) needs to be defined. It should search `BR` for rules where the last element matches `BUT`. If multiple rules match, it should implement a strategy (e.g., choose the one with the fewest antecedents not already in BF, or just the first one found). It should return the index of the chosen rule or 0 if no rule concludes `BUT`.
    2.  **Defining Initial State:** Add code at the beginning to define the specific `BF`, `BR`, and the main `BUT` for the problem you want to solve (like the course example).
    3.  **Calling the function:** Add the initial call, e.g., `result <- bcwdChain(BF, BR, BUT)`, and print the `result`.

```R
# Backward Chaining Function Stub from Image
 # Backward Chaining
 bcwdChain <- function(BF, BR, BUT) {
   if (verbose) cat("\n *** Backward current BUT =", BUT)
   if (BUT %in% BF) return(TRUE) # Base case: Goal is in initial facts
   chosenRule <- getLeastUnkRule(BF, BR, BUT) # Find a rule concluding BUT (Needs implementation)
   # if(verbose && (chosenRule != 0)) printRuleInfo(BR, chosenRule) # Optional print
   if (chosenRule == 0) {
     # No rule concludes BUT
     return(FALSE) # Base case: Cannot prove goal
   } else if (sum(BR[[chosenRule]][-length(BR[[chosenRule]])] %in% BF) == (length(BR[[chosenRule]]) - 1)) {
     # Antecedents are all known, Goal is proven by this rule
     # Note: This check might be redundant if getLeastUnkRule only returns rules with unknown antecedents
     if (verbose) cat("\n current proven BUT:", BUT, "by rule", names(BR)[chosenRule], "with known facts")
     return(TRUE)
   } else {
     # Rule found, but needs subgoals (unknown antecedents) proven
     boolUnkPos <- !(BR[[chosenRule]][-length(BR[[chosenRule]])] %in% BF)
     unkPos <- which(boolUnkPos)
     # The original image code for unkPos seems overly complex, simplifying:
     # unkPos <- which(!(BR[[chosenRule]][-length(BR[[chosenRule]])] %in% BF)) # Indices of unknown antecedents

     if (verbose) cat("\n Rule", names(BR)[chosenRule], "selected. Needs proving:", paste(BR[[chosenRule]][unkPos], collapse=", "))

     # Try to prove all unknown antecedents recursively
     conjunkSet <- sum(sapply(unkPos,
                            function(x) {
                              subGoal <- as.character(BR[[chosenRule]][x])
                              result <- bcwdChain(BF, BR, subGoal) # RECURSIVE CALL
                              # Potential Improvement: Add successfully proven subgoal to BF here? (See Extension Q2)
                              return(result)
                            }
     )) == length(unkPos) # Check if ALL recursive calls returned TRUE

     if (conjunkSet && verbose) cat("\n current proven BUT:", BUT, "by rule", names(BR)[chosenRule], "after proving subgoals")

     return(conjunkSet)
   }
 }

# Helper function (Conceptual Implementation)
getLeastUnkRule <- function(BF, BR, BUT){
   possibleRules <- which(sapply(BR, function(rule) !is.null(rule) && rule[[length(rule)]] == BUT))
   if(length(possibleRules) == 0) return(0)

   # Simple strategy: return the first rule found
   # More complex: find rule with fewest unknowns, etc.
   return(possibleRules[1])
}
```

---

## C. Extensions (Homework)

**Q1: Define the functions `lastFactRule()` and `condAwarRule()` to implement the Last_Fact and Condition_Aware strategies, respectively, in forward chaining.**
*   **Answer:** These functions would replace `getFirstActvRule` as the conflict resolution strategy function.
    *   `lastFactRule(BF, BR, lastFact)`:
        *   This function needs the current `BF`, `BR`, and the `lastFact` added to `BF`.
        *   It should find all rules in `BR` that are currently activatable (all antecedents in `BF`).
        *   Among the activatable rules, it should prioritize those where `lastFact` is one of the antecedents.
        *   It returns the index of a prioritized rule, or any activatable rule if none use `lastFact`, or 0 if none are activatable.
    *   `condAwarRule(BF, BR)`: (Condition_Aware / Specificity)
        *   This function needs the current `BF` and `BR`.
        *   It should find *all* activatable rules in `BR`.
        *   For each activatable rule, it calculates its specificity (number of antecedents: `length(rule) - 1`).
        *   It returns the index of the activatable rule with the **maximum** number of antecedents (the most specific rule). If there's a tie, it might return the first one found among the most specific. Returns 0 if no rules are activatable.

**Q2: For backward chaining, propose a script that takes into account proven subgoals to update the fact base.**
*   **Answer:** Modifying backward chaining to update the fact base globally is complex due to recursion and variable scope. A common approach is to use memoization or dynamic programming, storing proven goals in a separate structure or modifying `BF` carefully. Here's a conceptual modification using a shared environment for `BF`:

```R
# Create an environment to hold BF, allowing modification by reference
shared_env <- new.env()
shared_env$BF <- list("B", "C") # Initial facts

bcwdChain_memo <- function(BR, BUT, env) {
  # Use env$BF for checking and updating
  if (verbose) cat("\n *** Backward current BUT =", BUT)
  if (BUT %in% env$BF) return(TRUE) # Check shared BF

  chosenRule <- getLeastUnkRule(env$BF, BR, BUT) # Use shared BF

  if (chosenRule == 0) {
    return(FALSE)
  } else {
    # Simplified: Assume rule needs proving
    boolUnkPos <- !(BR[[chosenRule]][-length(BR[[chosenRule]])] %in% env$BF) # Check shared BF
    unkPos <- which(boolUnkPos)

    if(length(unkPos) == 0) { # All antecedents already known in shared BF
        if (verbose) cat("\n current proven BUT:", BUT, "by rule", names(BR)[chosenRule], "with known facts")
        # Add the proven BUT to the shared BF if not already there
        if(!(BUT %in% env$BF)) {
            env$BF <- append(env$BF, BUT)
            if (verbose) cat("\n Added", BUT, "to shared BF.")
        }
        return(TRUE)
    }

    # Try to prove unknown antecedents recursively
    all_proven <- TRUE
    for(pos in unkPos) {
        subGoal <- as.character(BR[[chosenRule]][pos])
        if (!bcwdChain_memo(BR, subGoal, env)) { # Recursive call with shared env
            all_proven <- FALSE
            break # If one subgoal fails, the rule fails
        }
        # If successful, the recursive call should have updated env$BF
    }

    if (all_proven) {
         if (verbose) cat("\n current proven BUT:", BUT, "by rule", names(BR)[chosenRule], "after proving subgoals")
         # Add the proven BUT to the shared BF if not already there
         if(!(BUT %in% env$BF)) {
             env$BF <- append(env$BF, BUT)
             if (verbose) cat("\n Added", BUT, "to shared BF.")
         }
         return(TRUE)
    } else {
         return(FALSE)
    }
  }
}

# Initial call:
# shared_env$BF <- list("B", "C") # Set initial facts
# result <- bcwdChain_memo(BR, "H", shared_env)
# print(result)
# print(shared_env$BF) # See the updated fact base
```
*Disclaimer: Managing state across recursion this way requires careful handling.*

**Q3: What is the potential effect of this update on the associated AND/OR tree?**
*   **Answer:** Updating the fact base with proven subgoals (memoization) can significantly **prune** the AND/OR search tree. When a subgoal (e.g., 'D') is successfully proven in one part of the tree and added to the shared fact base, any subsequent attempt to prove 'D' in another branch will immediately return `TRUE` by checking the fact base (the first base case). This avoids redundant computation and re-exploration of the subtree required to prove 'D', potentially leading to substantial performance improvements, especially if subgoals are frequently reused across different rules.