---
tags: [exam-questions, theory]
aliases: [exam questions, theory]
keywords: [exam questions, theory]
---

# 1. Theoretical Exam Questions (The Free Points Bank)

[[106 Parameter Directions and Enumerations|In]] almost every MCA exam, the first part is "Questions de cours". The professor uses highly specific phrasing, and expects the exact definitions from the slides and corrections. Here are the exact questions from your past exams and their perfect answers.

### 1. The [[107 UML [[202 Associations Roles and Navigability|Associations]] Navigability Roles and [[203 Multiplicity and Cardinality in Depth|Multiplicity]]|Multiplicity]] Definition
**Exam Question (PDF 14 - Examen MCA):** *"Qu'est-ce qu'une multiplicité dans un diagramme de classes ?"* (0.5 pts)
* **The Perfect Answer:** Une caractéristique qui définit le nombre d'instances d'une classe (ou d'un objet) liées à une autre classe (ou un autre objet) via une association.
* **Reasoning:** Do not just say "it's the numbers on the line". You must explicitly mention **"le nombre d'instances"** (the number of instances) because multiplicity strictly governs object instantiation at runtime.

### 2. The [[201 Intro to Class Relationships and Dependencies|Dependency]] vs Association Trap
**Exam Question (PDF 14 - Examen MCA):** *"Donner le diagramme de classe de la situation suivante : une classe A n'a pas d'attribut typé B mais qu'une de ses méthodes envoie un message vers B."* (1 pt)
* **The Perfect Answer:** You must draw a **Dependency** (Relation de dépendance). Draw Class A, Class B, and a dashed line with an open arrow `..>` pointing from A to B.
* **Reasoning:** If A has an attribute of type B, it is an Association (solid line). Because A only sends a message to B via a method (meaning B is just a parameter or a local variable inside the method), the structural link is temporary. This is the exact definition of a Dependency.

### 3. The Object Diagram (DOB) Definition and Limits
**Exam Question (PDF 10 - Correction):** *"Indiquer le rôle d'un diagramme d'objets... Combien existent-ils de diagrammes d'objets issus d'un diagramme de classes ?"* (0.75 pts)
* **The Perfect Answer:**
  * **Rôle:** Il représente les objets d'un système et leurs liens à un instant donné (une vue figée/photographie du système à un moment précis). Il permet de donner des exemples, affiner le diagramme de classes et mieux le comprendre.
  * **Combien ?** Il existe une **infinité** de diagrammes d'objets pour un seul diagramme de classes.
* **Reasoning:** A [[101 Static vs Dynamic Views|[[102 Anatomy of a Class|[[404 From Class Diagrams to Object Diagrams|Class diagram]]]]]] is the mold (the blueprint). You can pour infinite objects out of a mold. Missing the word "infinité" will cost you 0.25 pts.

### 4. [[304 Abstract Classes Interfaces and Realization|Interface]] vs Interface Usage (`<<realize>>` vs `<<use>>`)
**Slide Detail (Slide 67):** How do you show that a client *uses* an interface without implementing it?
* **Concept:** If `Document` implements `Imprimable`, you use Realization (dashed line, closed triangle). But if a `Personne` *uses* the printer interface to print something, you draw a Dependency `..>` with the [[401 Constructors Destructors and Method Stereotypes|stereotype]] `<<use>>`.
* **Exam Trick:** Do not connect the User directly to the Interface with a solid line. An interface cannot be instantiated, so you cannot have a direct structural association with it. You "use" it.


---
**Keywords:** #exam-questions, #theory
