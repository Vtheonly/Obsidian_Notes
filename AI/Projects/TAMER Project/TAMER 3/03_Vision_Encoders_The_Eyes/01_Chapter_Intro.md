# Chapter 3: The Tokenizer - Mapping Math to Discrete Tokens

---

## Chapter Introduction

This chapter covers two critical components of the TAMER pipeline: the **tokenizer** that converts LaTeX strings into discrete tokens, and the **2D positional encoding** that gives the vision encoder spatial awareness.

The first half of the chapter addresses tokenization. Standard NLP tokenizers like BPE (Byte-Pair Encoding) and WordPiece fail catastrophically on LaTeX because they split semantically atomic constructs like `\begin{pmatrix}` into meaningless fragments based on frequency statistics. TAMER replaces statistical tokenization with a **rule-based lexical tokenizer** that treats LaTeX like a programming language, applying explicit scanning rules:

- **Backslash commands** (e.g., `\frac`, `\alpha`) are scanned as single atomic tokens.
- **Double backslash** (`\\`) is recognized as the row separator before the single-backslash rule is applied.
- **Environment commands** (e.g., `\begin{matrix}`) are merged into single indivisible tokens so the model cannot predict a mismatched closing tag.
- **Digits** are tokenized individually so the model can compose any number from the digit vocabulary, avoiding out-of-vocabulary failures.

The tokenizer's vocabulary is small (300-600 tokens) compared to NLP models (100,000+), which is a significant computational advantage: the final linear projection layer and softmax operations are trivially small.

The second half of the chapter (Section 3.7) provides a deep dive into **positional encoding** — both 1D sinusoidal for the decoder and 2D learned for the encoder. The Transformer's self-attention is permutation equivariant, meaning it has no inherent concept of spatial position. Positional encoding injects coordinate information so the model can distinguish between a `2` in the superscript position (an exponent) and a `2` at the baseline (a coefficient). TAMER uses a **factored learned 2D encoding** (separate row and column embedding tables concatenated) that is 85x more parameter-efficient than a full 2D grid and generalizes better to unseen image sizes.

### Sections in this Chapter

| Section | Title | Key Topics |
|---------|-------|------------|
| 1 | Lexical Analysis of LaTeX | BPE failure on LaTeX, rule-based tokenizer, backslash commands, environment atomicity, digit-level tokenization |
| 2 | Vocabulary and Special Tokens | `<pad>`, `<sos>`, `<eos>`, `<unk>`, padding mask requirements, small vocabulary advantages |
| 3.7 | What Is Positional Encoding (1D vs 2D) | Permutation equivariance, 1D sinusoidal derivation, 2D factored learned encoding, why 1D fails for images |

---
