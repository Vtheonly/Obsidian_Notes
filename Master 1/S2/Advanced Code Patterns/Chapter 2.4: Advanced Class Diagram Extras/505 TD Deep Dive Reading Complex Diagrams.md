---
tags: [td, complex-diagrams]
aliases: [td, complex diagrams]
keywords: [td, complex diagrams]
---

# 5. [[502 [[503 [[504 TD Deep Dive File System and Shortcuts|TD]] Deep Dive Arithmetic Expression Trap|TD]] Identification Exercise|TD]] Deep Dive: Reading Complex Diagrams (TD 3 Ex 1)

[[106 Parameter Directions and Enumerations|In]] PDF 20, you are given a [[101 Static vs Dynamic Views|[[102 Anatomy of a Class|[[404 From Class Diagrams to Object Diagrams|Class Diagram]]]]]] of a Website and asked to check the true statements. This tests your ability to read inherited properties and XOR constraints.

**The Diagram Analysis:**
* `Structure` is a superclass with attributes `Titre` and `Version`.
* `Site Web`, `Chapitre`, `Section`, and `Page` all inherit from `Structure` (Hollow arrows point up).
* `Site Web` contains `1..*` `Chapitre` (Composition).
* `Chapitre` contains `1..*` `Section`.
* `Section` contains `0..1` `Section` OR `0..1` `Page`. **There is an `{XOR}` constraint between the Section loop and the Page link.**

### The Questionnaire Breakdown

1. **"Tous les chapitres ont un titre."**
   * **Correct Answer: TRUE.**
   * **Reasoning:** `Chapitre` inherits from `Structure`. `Structure` has the attribute `Titre`. Therefore, via [[109 [[302 Inheritance and Generalization|Inheritance]] [[301 Aggregation vs Composition|Aggregation]] and Composition|inheritance]], all chapters have a title.

2. **"Il est possible d'avoir un auteur différent pour chaque chapitre."**
   * **Correct Answer: FALSE.**
   * **Reasoning:** The attribute `Auteur` is located strictly inside the `Site Web` class. It is not in `Structure` or `Chapitre`. Therefore, the author applies to the whole website, not individual chapters.

3. **"Toutes les sections contiennent au moins une section."**
   * **Correct Answer: FALSE.**
   * **Reasoning:** The [[306 Recursive Composition Pattern Trap|recursive composition]] on `Section` has a [[107 UML [[202 Associations Roles and Navigability|Associations]] Navigability Roles and [[203 Multiplicity and Cardinality in Depth|Multiplicity]]|multiplicity]] of `0..1`. "0" means it does not *have* to contain a section. Also, because of the `{XOR}`, if it contains a `Page`, it cannot contain a `Section`.

4. **"Toutes les sections contiennent au moins une page."**
   * **Correct Answer: FALSE.**
   * **Reasoning:** The association to `Page` is `0..1`. And again, the `{XOR}` means a Section might contain another Section instead of a Page.

5. **"Toutes les sites Web contiennent au moins une page."**
   * **Correct Answer: FALSE (Technically).**
   * **Reasoning:** A Website contains at least one Chapter (`1..*`). A Chapter contains at least one Section (`1..*`). However, a Section can contain either a nested Section OR a Page (`0..1`). Because it's `0..1`, the chain could technically end without a Page ever being instantiated, or loop infinitely with Sections.

---
**Keywords:** #td, #complex-diagrams
