- **Expressions régulières**
- **Décident Analyzer**
- **Les grammaires :**
    - **Automates liés aux grammaires :**
        - Minimization, détermination, les règles de Thompson.
        - Construire l’automate non déterministe (AFN) de l’expression régulière suivante : 𝒂(𝒂 | 𝒃)∗. (ou l'inverse)
        - Rendre l’automate non déterministe (AFN).
    - **Ambiguïté récursive et factorisation.**
    - **Analyse des grammaires :**
        - Quand un langage est LL(1), LR(0), SLR(0) ? Table d'analyse LL(1), LR(0), SLR(0).
        - Item `goto(I1, I2, I3, I4, ..., {a, b, c, d, ...})`.
        - Grammaire engendrée par un langage.
        - Grammaire équivalente.
        - Analyse d'une chaîne de caractères (analyse d'un arbre de dérivation de chaîne de caractères).
            - Si G n’est pas LL(1), trouver une grammaire G’ équivalente qui est LL(1), puis analyser la chaîne C.
        - **Comparaisons et relations entre grammaires :**
            - Comparison between SLR(0), LL(1), LR(0), LALR.
            - If a language is SLR(0), could it be LL(1), LL(2), LL(k), LR(0)?
            - If a language is LL(1), could it be an SLR(0), LR(0)?
            - If a language is LR(0), could it be SLR(0), LL(1)?
    - Memorize famous grammars like the ambiguous `E*T`:
    - Dangling IF Problem
        $$
        \begin{aligned}
        &S \rightarrow E ; S / \epsilon \\
        &E \rightarrow E + T / E - T / T \\
        &T \rightarrow T * F / T \div F / F \\
        &F \rightarrow \text{id} / (E)
        \end{aligned}
        $$

- **Étapes de la "compilation" :**
    - What is the output of each step?
    - La différence entre un interpréteur et un compilateur.
    - Le rôle des outils Lex et Yacc.

- **Conversion et algorithmes :**
    - Conversion of a C code to a portion of quadruplets.
    - Convert expression to triplets.
    - Give the algorithm of a lexer.

- **Analyse lexicale :**
    - Given a language, proposer un analyseur lexical pour ce langage.
