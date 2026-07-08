---
source_collections:
  - "TAMER 1"
  - "TAMER 2"
  - "TAMER 3"
original_paths:
  - "TAMER 2/Chapter 7 - Data Pipeline and Preprocessing/2. LaTeX Tokenization.md"
  - "TAMER 1/Chapter 1/1.3 Tokenization and Mathematical Grammar.md"
  - "TAMER 3/03_Vision_Encoders_The_Eyes/02_Section_1_Lexical_Analysis_of_LaTeX.md"
  - "TAMER 3/03_Vision_Encoders_The_Eyes/03_Section_2_Vocabulary_and_Special_Tokens.md"
roles_in_master:
  - "canonical"
  - "supplement"
topic: "tokenization"
master_chapter: "80_Data_Pipeline_and_Preprocessing"
master_filename: "02_LaTeX_Tokenization.md"
n_source_files_merged: 4
merged: True
---

# 2. LaTeX Tokenization

## Overview

Before a neural network can process a LaTeX string, that string must be converted into a sequence of integers — a process called **tokenization**. In TAMER, this is handled by the `LaTeXTokenizer` class, which breaks LaTeX expressions into discrete tokens and maps each token to a unique integer ID. The tokenizer is the bridge between the human-readable world of mathematical notation and the machine-readable world of tensor indices.

Unlike natural language tokenization (which often uses subword methods like BPE or SentencePiece), LaTeX tokenization in TAMER operates at the **character and command level**. This choice is deliberate and deeply tied to the structured nature of the LaTeX language itself.

---

## 2.1 What Is Tokenization?

Tokenization is the process of converting a raw text string into a list of discrete symbols (tokens), each of which is then mapped to an integer index. Consider a simple example:

```
Input:  "\frac{1}{2}"
Tokens: ["\frac", "{", "1", "}", "{", "2", "}"]
IDs:    [45, 12, 8, 13, 12, 9, 13]
```

The tokenizer must correctly identify that `\frac` is a single token (not four separate characters `\`, `f`, `r`, `a`, `c`), while `{` and `1` are individual tokens. This requires understanding LaTeX's syntax — specifically, that a backslash followed by letters forms a command token.

---

## 2.2 LaTeX as a Structured Language

LaTeX is not natural language. It is a **markup language** with well-defined syntax rules:

- **Commands**: Tokens beginning with `\`, such as `\frac`, `\sqrt`, `\int`, `\alpha`. These are the "words" of LaTeX — each one represents a specific mathematical concept or formatting instruction.
- **Braces**: `{` and `}` are grouping delimiters that define the scope of arguments. In `\frac{1}{2}`, the first `{1}` is the numerator and the second `{2}` is the denominator.
- **Symbols**: Single characters like `+`, `-`, `=`, `x`, `2` that represent themselves in the mathematical expression.
- **Environment markers**: `\begin{aligned}` and `\end{aligned}` define block-level structures like matrices and aligned equations.
- **Spacing tokens**: `~`, `\,`, `\;`, `\quad` control horizontal spacing.

This structured nature means that LaTeX has a **finite and relatively small vocabulary** — unlike natural language, which has effectively unlimited words due to compound formation, names, and loan words.

---

## 2.3 The LaTeXTokenizer Architecture

```mermaid
graph LR
    subgraph "Tokenization Pipeline"
        A["Raw LaTeX String<br/>e.g. \frac{1}{2}"]
        B["Tokenize Step<br/>Split into token list"]
        C["Token List<br/>['\\frac', '{', '1', '}', '{', '2', '}']"]
        D["Encode Step<br/>Map tokens → IDs"]
        E["ID Sequence<br/>[45, 12, 8, 13, 12, 9, 13]"]
        F["Add Special Tokens<br/>SOS + IDs + EOS"]
        G["Final Sequence<br/>[1, 45, 12, 8, 13, 12, 9, 13, 2]"]
    end

    A --> B --> C --> D --> E --> F --> G

    subgraph "Vocabulary"
        V["token2id mapping<br/>~522 entries<br/>Saved to tokenizer.json"]
    end

    D -.-> V

    subgraph "Decoding (Inference)"
        H["ID Sequence<br/>[1, 45, 12, 8, 13, 12, 9, 13, 2]"]
        I["Decode Step<br/>Map IDs → tokens"]
        J["Token List<br/>['\\frac', '{', '1', '}', '{', '2', '}']"]
        K["Join Tokens<br/>Reconstruct LaTeX string"]
        L["Output: \frac{1}{2}"]
    end

    H --> I --> J --> K --> L
```

The `LaTeXTokenizer` class implements a three-stage pipeline:

1. **Tokenize**: Split a LaTeX string into a list of string tokens
2. **Encode**: Convert the token list into a list of integer IDs
3. **Decode**: Convert integer IDs back into a LaTeX string

Each stage is described in detail below.

---

## 2.4 The `tokenize()` Method

The `tokenize()` method is responsible for splitting a raw LaTeX string into a list of tokens. The key challenge is correctly identifying LaTeX commands (which start with `\` and consist of one or more letters) while treating individual characters as separate tokens.

### Tokenization Rules

The tokenizer follows these rules, applied in order:

1. **LaTeX commands**: A backslash `\` followed by one or more alphabetic characters forms a single token. For example, `\frac` → one token, `\alpha` → one token, `\begin` → one token.
2. **Single-character commands**: A backslash followed by a single non-alphabetic character (e.g., `\{`, `\}`, `\\`) forms a single token. These are escape sequences for symbols that would otherwise be interpreted as LaTeX syntax.
3. **Individual characters**: Any character not part of a command is its own token. This includes digits, letters (outside commands), operators, and braces.
4. **Whitespace**: Spaces are generally ignored in LaTeX tokenization because LaTeX itself ignores most whitespace in math mode. The tokenizer strips spaces during tokenization.

### Example Walkthrough

```
Input:  "\sqrt{x^2 + 1}"

Step 1: Identify command token → "\sqrt"
Step 2: Next char "{" → token "{"
Step 3: Next char "x" → token "x"
Step 4: Next char "^" → token "^"
Step 5: Next char "2" → token "2"
Step 6: Next char " " → skip (whitespace)
Step 7: Next char "+" → token "+"
Step 8: Next char " " → skip (whitespace)
Step 9: Next char "1" → token "1"
Step 10: Next char "}" → token "}"

Result: ["\sqrt", "{", "x", "^", "2", "+", "1", "}"]
```

### Edge Cases

- **Nested commands**: `\frac{a}{b}` correctly tokenizes as `["\frac", "{", "a", "}", "{", "b", "}"]`. The tokenizer does not need to understand nesting — it just splits at token boundaries.
- **Subscripts and superscripts**: `x_{ij}` tokenizes as `["x", "_", "{", "i", "j", "}"]`. The `_` and `^` operators are individual tokens.
- **Matrix environments**: `\begin{pmatrix}` tokenizes as `["\begin", "{", "pmatrix", "}"]`. The `pmatrix` inside braces is treated as a regular string of individual character tokens in some implementations, or as a single argument token in others.

---

## 2.5 The `encode()` Method

Once we have a list of string tokens, the `encode()` method maps each token to its integer ID using the `token2id` dictionary:

```python
def encode(self, tokens: list[str]) -> list[int]:
    return [self.token2id[t] for t in tokens]
```

If a token is not in the vocabulary, the tokenizer either raises an error (strict mode) or maps it to an `<UNK>` token (lenient mode). In practice, TAMER builds the vocabulary from the entire training corpus before training, so out-of-vocabulary tokens should be rare during training — but they can appear during inference on unseen formulas.

### Special Tokens in Encoding

The `encode()` method typically wraps the token IDs with special tokens:

```
[SOS, token_id_1, token_id_2, ..., token_id_n, EOS]
```

Where:
- **SOS** (Start of Sequence, ID=1): Signals the decoder to begin generating output. Without SOS, the decoder has no initial input to condition on.
- **EOS** (End of Sequence, ID=2): Signals that the expression is complete. During inference, generating an EOS token terminates the decoding loop.
- **PAD** (Padding, ID=0): Used to pad sequences within a batch to equal length. PAD tokens are ignored by the loss function via `ignore_index=0`.

---

## 2.6 The `decode()` Method

The `decode()` method performs the inverse of `encode()` — it maps integer IDs back to string tokens and joins them into a LaTeX string:

```python
def decode(self, ids: list[int], skip_special: bool = True) -> str:
    tokens = []
    for id_ in ids:
        if skip_special and id_ in (self.pad_id, self.sos_id, self.eos_id):
            continue
        tokens.append(self.id2token[id_])
    return "".join(tokens)
```

### The `skip_special` Option

During inference, we typically call `decode()` with `skip_special=True` to strip PAD, SOS, and EOS tokens from the output. This produces a clean LaTeX string ready for rendering or evaluation.

During debugging, `skip_special=False` is useful for inspecting the raw token sequence, including where EOS was predicted and how much padding was applied.

### Important: No Spaces Between Tokens

Note that `"".join(tokens)` concatenates tokens without spaces. This is correct for LaTeX because the language doesn't use spaces to separate tokens in math mode — `\frac{1}{2}` is written as a continuous string. The spacing in rendered math is handled by the LaTeX typesetting engine, not by spaces in the source.

---

## 2.7 Vocabulary Construction

The vocabulary is built by scanning the entire training corpus and collecting all unique tokens:

```python
def build_vocab(self, latex_strings: list[str]) -> None:
    all_tokens = set()
    for latex in latex_strings:
        tokens = self.tokenize(latex)
        all_tokens.update(tokens)

    # Reserve IDs 0-2 for special tokens
    self.token2id = {"<PAD>": 0, "<SOS>": 1, "<EOS>": 2}
    for i, token in enumerate(sorted(all_tokens), start=3):
        self.token2id[token] = i

    self.id2token = {v: k for k, v in self.token2id.items()}
```

### Why ~522 Tokens?

LaTeX's vocabulary in mathematical expressions is remarkably small. The ~522 tokens break down roughly as:

- **3 special tokens**: PAD, SOS, EOS
- **~26 lowercase letters**: a-z (used as variable names)
- **~26 uppercase letters**: A-Z
- **~10 digits**: 0-9
- **~20 operators**: +, -, =, <, >, *, /, etc.
- **~150 LaTeX commands**: \frac, \sqrt, \int, \sum, \alpha through \omega, \begin, \end, etc.
- **~10 structural tokens**: {, }, [, ], (, ), _, ^, &, \\
- **~200+ additional symbols and commands**: Less common symbols, environment names (aligned, cases, pmatrix, etc.), and formatting commands

This is tiny compared to natural language vocabularies (typically 30,000–100,000 tokens). The small vocabulary is a major advantage — it means the output softmax is over a much smaller space, making the prediction task easier and the model more sample-efficient.

---

## 2.8 Why Not BPE or SentencePiece?

Modern NLP systems almost universally use subword tokenization methods like **Byte Pair Encoding (BPE)** or **SentencePiece**. Why doesn't TAMER?

The answer lies in the fundamental difference between LaTeX and natural language:

1. **LaTeX already has a natural token boundary**: The backslash `\` explicitly marks the start of a command. Braces `{}` explicitly mark argument boundaries. There is no ambiguity about where one token ends and another begins — unlike natural language, where word boundaries can be fuzzy (is "don't" one word or two?).

2. **Subword tokenization would destroy LaTeX's compositional structure**: BPE might split `\frac` into `\fr` + `ac`, or `\sqrt` into `\sq` + `rt`. These subword units have no semantic meaning in LaTeX and would make the model's job harder, not easier.

3. **The vocabulary is already small**: BPE was invented to handle the open-ended vocabulary problem in NLP — there are too many words to have one token per word. LaTeX doesn't have this problem. With only ~522 tokens, we can afford a one-token-per-symbol mapping without any vocabulary pressure.

4. **Decoding simplicity**: With character/command-level tokenization, decoding is trivial — just map each ID back to its token string and concatenate. With BPE, you need a merge table and special decoding logic.

---

## 2.9 Saving and Loading: tokenizer.json

The tokenizer's vocabulary mapping is saved to a JSON file called `tokenizer.json`:

```json
{
    "token2id": {
        "<PAD>": 0,
        "<SOS>": 1,
        "<EOS>": 2,
        "\\frac": 3,
        "\\sqrt": 4,
        "{": 5,
        "}": 6,
        ...
    },
    "id2token": {
        "0": "<PAD>",
        "1": "<SOS>",
        "2": "<EOS>",
        "3": "\\frac",
        "4": "\\sqrt",
        "5": "{",
        "6": "}",
        ...
    },
    "vocab_size": 522,
    "pad_id": 0,
    "sos_id": 1,
    "eos_id": 2
}
```

### Why This Matters

**The tokenizer must be absolutely identical between training and inference.** If the tokenizer used during inference has even a single different ID mapping, the model's output will be garbage. For example, if `\frac` is ID 3 during training but ID 5 during inference, the model will predict ID 3 when it means `\frac`, but the decoder will interpret ID 3 as whatever token occupies that slot in the new mapping.

This is why:
1. The tokenizer is saved immediately after vocabulary construction
2. The saved `tokenizer.json` is loaded at inference time, rather than rebuilding the vocabulary
3. The tokenizer file is version-controlled alongside the model checkpoint

---

## 2.10 Consistency Between Training and Inference

The golden rule of tokenization: **train and inference must use the same tokenizer**. This seems obvious, but it's violated surprisingly often in practice. Common mistakes include:

- **Rebuilding the vocabulary at inference time**: If the inference data contains a token not seen during training, the vocabulary size changes, shifting all IDs above the new token's position. The saved tokenizer must be loaded, not rebuilt.
- **Different tokenization rules**: If the training tokenizer treats `\\` as a single token but the inference tokenizer splits it into `\` + `\`, the model will receive incorrect input sequences.
- **Different special token IDs**: If SOS is ID 1 during training but ID 2 during inference, the decoder's initial input will be wrong.

TAMER avoids all these issues by saving the complete tokenizer state to `tokenizer.json` and loading it at inference time. The `save()` and `load()` methods ensure round-trip consistency:

```python
tokenizer.save("tokenizer.json")      # After vocab construction
tokenizer = LaTeXTokenizer.load("tokenizer.json")  # At inference time
```

---

## Key Takeaways

- **Tokenization converts LaTeX strings to integer sequences** that the model can process.
- **LaTeX has a natural token structure** — commands start with `\`, braces delimit arguments, and symbols are individual characters.
- **The vocabulary is small (~522 tokens)** because LaTeX is a structured language with finite vocabulary.
- **BPE/SentencePiece are unnecessary** for LaTeX — they would destroy compositional structure without solving a vocabulary problem that doesn't exist.
- **Special tokens (PAD=0, SOS=1, EOS=2)** are essential for batching, decoding, and loss computation.
- **tokenizer.json must be saved and reloaded** to ensure consistency between training and inference.
- **The three-stage pipeline** (tokenize → encode → decode) provides a clean abstraction that separates string processing from integer mapping.

---

## Supplementary Perspective — from TAMER 1

> **Original file:** `TAMER 1/Chapter 1/1.3 Tokenization and Mathematical Grammar.md`  
> **Role in master vault:** supplement perspective from TAMER 1 — T1 supplement. Different angle: mathematical grammar perspective.  
> **Preservation policy:** full original text reproduced verbatim below; nothing omitted.

---

## 1.3 Tokenization and Mathematical Grammar

Before a neural network can process math, the image features must be mapped to discrete semantic units called **tokens**, and these tokens must follow the rules of mathematical grammar.

###  Tokenization Strategy

In HMER, tokenization must respect LaTeX commands rather than just individual characters. For example, the formula $\frac { x ^ { 2 } } { y + 1 }$ is tokenized into a vocabulary array:

`['\frac', '{', 'x', '^', '{', '2', '}', '}', '{', 'y', '+', '1', '}']`

#### Special Tokens
A robust vocabulary requires structural tokens to manage sequence boundaries:
1.  **`<sos>` (Start of Sequence):** Signals the decoder to begin generating.
2.  **`<eos>` (End of Sequence):** Signals the completion of the formula.
3.  **`<pad>` (Padding):** Ensures all sequences in a training batch are the same length for efficient matrix multiplication.
4.  **`<unk>` (Unknown):** Catches out-of-vocabulary symbols.

###  AST and Parent-Child Relationships

To train the Tree-Aware module, we map every token to its "parent" in an **Abstract Syntax Tree (AST)**.

*   **Logic:** In $x ^ 2$, `x` is the base, `^` modifies `x`, and `2` is the child of `^`.
*   During data preparation, an algorithm explicitly assigns a `parent_index` (the position of the parent token in the sequence) to every content token.

#### Detailed Example: $3^2 - 1 = 8$
The LaTeX string: `3 ^ { 2 } - 1 = 8`
Indices:
0: `3`, 1: `^`, 2: `{`, 3: `2`, 4: `}`, 5: `-`, 6: `1`, 7: `=`, 8: `8`

**Parent-Child Mapping:**
`{(3, 0), (5, 0), (6, 5), (7, 6), (8, 7)}`
*(Note: A parent index of -1 signifies a root-level node)*

```mermaid
graph TD
    Root["Root Level (Parent = -1)"]
    T0["Index 0: '3'"]
    T1["Index 1: '^'"]
    T2["Index 2: '{'"]
    T4["Index 4: '}'"]
    T3["Index 3: '2'"]
    T5["Index 5: '-'"]
    T6["Index 6: '1'"]
    T7["Index 7: '='"]
    T8["Index 8: '8'"]

    Root --> T0
    Root --> T1
    Root --> T2
    Root --> T4
    T0 -->|"Child of 0"| T3
    T0 -->|"Child of 0"| T5
    T5 -->|"Child of 5"| T6
    T6 -->|"Child of 6"| T7
    T7 -->|"Child of 7"| T8
```

 **Common Pitfall:** Students often forget to exclude `<pad>`, `<sos>`, and `<eos>` from tree construction. Structural trees only apply to mathematical content tokens.

---

## Supplementary Perspective — from TAMER 3

> **Original file:** `TAMER 3/03_Vision_Encoders_The_Eyes/02_Section_1_Lexical_Analysis_of_LaTeX.md`  
> **Role in master vault:** supplement perspective from TAMER 3 — T3 supplement. Lexical analysis angle.  
> **Preservation policy:** full original text reproduced verbatim below; nothing omitted.

---

### 1. Lexical Analysis of LaTeX

#### Why Standard NLP Tokenizers Fail on LaTeX

Standard NLP tokenizers like Byte-Pair Encoding (BPE, used in GPT) or WordPiece (used in BERT) are built on a statistical principle: find the most frequent substrings in the training corpus and merge them into single tokens. This is optimal for natural language because word boundaries are probabilistic.

For LaTeX, this is catastrophically wrong.

**The BPE Failure Example:**

Suppose `\begin{pmatrix}` appears 500 times and `\begin{bmatrix}` appears 50 times in the training set. BPE might tokenize them as:

- `\begin{pmatrix}` → `['\begin', '{pmatrix}']` (merged as frequent unit)
- `\begin{bmatrix}` → `['\begin', '{', 'bmatrix', '}']` (split because less frequent)

Now the model learns a completely different token structure for semantically identical constructs. At inference time, if the model predicts `'{bmatrix}'` but the actual token is `'{'` + `'bmatrix'` + `'}'`, the tokenization is mismatched and the output is garbage.

More dangerously: if BPE has never seen `\begin{vmatrix}` in training, it tokenizes it as individual characters `['\', 'b', 'e', 'g', 'i', 'n', ...]`. This Out-of-Vocabulary (OOV) fragmentation makes it nearly impossible for the model to predict the correct token sequence.

---

#### TAMER's Rule-Based Lexical Tokenizer

TAMER builds a deterministic tokenizer using explicit lexical rules, analogous to how a programming language compiler lexes source code.

**Rule 1: Backslash Commands**
Any sequence starting with `\` followed by alphabetic characters is scanned as a single token until a non-alphabetic character is encountered.
- `\frac` → single token `'\frac'`
- `\alpha` → single token `'\alpha'`
- `\sum` → single token `'\sum'`
- `\hat{x}` → three tokens: `'\hat'`, `'{'`, `'x'`, `'}'`

**Rule 2: Double Backslash Priority**
Before applying Rule 1, the scanner checks if the current position is `\\` (two backslashes). If yes, it emits a single `'\\\\'` token and advances by 2 characters. This check must come first because `\\` is the LaTeX row separator and is semantically completely different from two consecutive `\` commands.

If this rule is missing, `\\` becomes `['\\', '\\']` (two identical tokens). The model then treats row separation as two separate escape characters, completely losing its structural understanding.

**Rule 3: Atomic Environments**
The entire construct `\begin{matrix}` (including the `{` and `matrix}`) is merged into a single indivisible token: `'\begin{matrix}'`.

This is critical because the environment name must match exactly. `\begin{matrix}` must be closed by `\end{matrix}`. If the model predicts `'\begin'` + `'{'` + `'matrix'` + `'}'` as separate tokens, it might predict `'\begin'` + `'{'` + `'Matrix'` + `'}'` (wrong capitalization) and produce a LaTeX compile error.

By making the entire environment command atomic, the model either predicts the whole thing correctly or gets it completely wrong. There is no partial credit for getting the right environment name but wrong bracket.

**Rule 4: Digit-Level Tokenization**
All numeric digits are tokenized individually. `3.14159` becomes `['3', '.', '1', '4', '1', '5', '9']`.

The reason: In a math dataset, you might have numbers like `1024`, `2048`, `4096`. If `1024` is a single token, the model learns to predict it as a unit. If the test set contains `3072`, and `3072` is an OOV token, the model fails completely. By tokenizing digit by digit, the model learns the concept of numbers compositionally. It can predict any number from the digit vocabulary `{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, .}`.

---

#### The Tokenizer's Internal State Machine

The lexical scanner can be visualized as a state machine:

```mermaid
stateDiagram-v2
    [*] --> START
    START --> DOUBLE_BACKSLASH : see two backslashes
    START --> COMMAND : see single backslash
    START --> DIGIT : see 0-9
    START --> SPECIAL : see { } ^ _ & $ etc
    START --> WHITESPACE : see space/newline
    DOUBLE_BACKSLASH --> EMIT_ROW_SEP : emit token "\\\\"
    EMIT_ROW_SEP --> START
    COMMAND --> COMMAND : see letter
    COMMAND --> EMIT_CMD : see non-letter
    EMIT_CMD --> START
    DIGIT --> EMIT_DIGIT : emit single digit token
    EMIT_DIGIT --> START
    SPECIAL --> EMIT_SPECIAL : emit single char token
    EMIT_SPECIAL --> START
    WHITESPACE --> START : skip whitespace
```

> **Important reminder:** LaTeX whitespace is semantically meaningless in math mode. `a + b` and `a+b` and `a  +  b` are identical in LaTeX. The tokenizer skips all whitespace. This is correct. Do not preserve spaces as tokens in math mode. Only in text environments like `\text{hello world}` does spacing matter, and TAMER handles this as a special-case atomic token for the `\text{...}` environment.

---

---

## Supplementary Perspective — from TAMER 3

> **Original file:** `TAMER 3/03_Vision_Encoders_The_Eyes/03_Section_2_Vocabulary_and_Special_Tokens.md`  
> **Role in master vault:** supplement perspective from TAMER 3 — T3 supplement. Vocabulary / special tokens angle.  
> **Preservation policy:** full original text reproduced verbatim below; nothing omitted.

---

### 2. Vocabulary and Special Tokens

#### Special Control Tokens

The tokenizer's vocabulary is built from the training set using the lexical rules above. Additionally, four special tokens are hardcoded at fixed indices:

**Index 0: `<pad>` (Padding Token)**

Sequences in a batch must all be the same length to form a rectangular tensor. If batch sequences have lengths [12, 47, 83, 31], they must all be padded to length 83. The padding token fills the gaps.

The loss function masks `<pad>` positions by setting their contribution to zero. The model is not penalized for any prediction at a `<pad>` position.

> **Critical reminder:** The model does see `<pad>` tokens during the decoder's masked self-attention. They are not invisible to the attention mechanism by default. You must explicitly mask them out in the attention computation to prevent the model from attending to meaningless padding and learning spurious patterns. This is done via the `src_key_padding_mask` and `tgt_key_padding_mask` arguments in PyTorch's `nn.TransformerDecoder`.

**Index 1: `<sos>` (Start of Sequence Token)**

The decoder is autoregressive: it predicts one token at a time, each conditioned on previous predictions. But at step $t=0$, there are no previous predictions. The `<sos>` token is the seed. It is always the first input to the decoder at $t=0$, and the decoder is trained to predict the first real token of the sequence as its response to `<sos>`.

**Index 2: `<eos>` (End of Sequence Token)**

The model needs to know when to stop generating. Mathematical formulas have variable lengths. If the generation loop runs forever, it produces infinite garbage tokens.

During training, `<eos>` is appended to the end of every target sequence. The model is trained to predict `<eos>` after the last real token. During inference, the generation loop terminates when `<eos>` is produced.

**Index 3: `<unk>` (Unknown Token)**

If a symbol appears in the validation set that was not in the training vocabulary, the tokenizer cannot represent it. It is mapped to `<unk>`. A model that frequently produces `<unk>` is encountering symbols outside its vocabulary, which indicates either:
1. The training set does not cover the full distribution of mathematical notation.
2. The formula contains symbols from a different LaTeX package not used during training.

A high `<unk>` rate is a data distribution mismatch signal, not a model architecture problem.

---

#### Vocabulary Size Considerations

The TAMER vocabulary typically contains 300-600 tokens depending on the dataset. This is tiny compared to NLP models (GPT-4 has 100,000 tokens).

This small vocabulary is a significant advantage:
- The final linear projection layer (mapping decoder hidden states to token logits) is only `D × V` (e.g., 768 × 512 = 393,216 parameters) instead of billions.
- Softmax over 512 tokens is computationally trivial.
- The model can realistically learn good probability estimates for all 512 token types because they all appear frequently.

---
