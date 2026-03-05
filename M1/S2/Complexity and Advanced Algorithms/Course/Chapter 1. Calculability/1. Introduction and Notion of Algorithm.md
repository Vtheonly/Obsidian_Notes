
# 1. Introduction and Notion of Algorithm

## Course Context & Motivation
Before diving into the complex mathematics of algorithms, the course introduces two major obstacles in computer science (illustrated by the opening cartoons):
1. **Undecidability (Décidabilité):** Some problems simply have *no efficient algorithm* because **no such algorithm is mathematically possible**. 
2. **NP-Hardness (Complexité):** Some problems have no known efficient algorithm, and no famous computer scientist has ever been able to find one.
[[Qs1]]
> *"The best programs are written so that computing machines can perform them quickly and so that human beings can understand them clearly."* — **Donald Ervin Knuth**

## The Notion of Algorithm
To study what a computer can or cannot do, we must first define what an algorithm is.

**Definition:** An **algorithm** is a finite sequence of instructions designed to solve a given problem.

This raises an immediate question: **What exactly is an instruction?**
* Intuitively, it is an elementary calculation action that is executable in a finite amount of time and in a deterministic manner.
* But what counts as an "action de calcul" (calculation action)? 

> [!warning] The Need for Rigor
> The definition of an "instruction" is inherently vague. Depending on the programming language, an instruction could be adding two numbers or sorting a whole list. Because of this ambiguity, we cannot mathematically prove what algorithms can or cannot do just by using words. 
> 
> **Solution:** This vagueness led to the creation of strict, mathematical **models of computation (modèles de calcul)**, the most famous being the **Turing Machine**.