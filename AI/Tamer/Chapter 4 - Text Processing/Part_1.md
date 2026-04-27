# Chapter 4: Text Processing and Tokenization

## 1. Tokenizing Mathematical LaTeX

**Background Knowledge:**
Language models usually tokenize text using BPE (Byte-Pair Encoding), creating sub-words (e.g., "equation" -> "equa", "tion"). For math, BPE is disastrous because it chops up LaTeX commands unpredictably.

**The TAMER Tokenization Logic:**
Your `LaTeXTokenizer` parses math based on mathematical syntax:
1.  **Atomic Commands**: Tokens like `\frac`, `\sqrt`, `\alpha` are treated as single integer IDs. 
2.  **Atomic Environments**: `\begin{pmatrix}` and `\end{pmatrix}` are kept whole. If you split them into `\begin`, `{`, `pmatrix`, `}`, the model might hallucinate `\begin{bmatrix}` but close it with `\end{pmatrix}`. Making them atomic forces structural perfection.
3.  **Atomic Row Separators**: `\\` is treated as one token. (A bug in older versions parsed it as two `\` characters, breaking matrix matrices).
4.  **Character/Digit Level**: Numbers and variables are tokenized individually (`1`, `2`, `.`, `x`). This makes the model robust to unseen numbers. If it trained on "123", it doesn't need a "123" token; it just outputs "1", "2", "3".

## 2. Special Tokens and Vocabulary

Every sequence requires navigational markers:
*   `<sos>` (Start of Sequence): Fed to the decoder at Step 0 to kick off generation.
*   `<eos>` (End of Sequence): When the model predicts this, inference stops.
*   `<pad>`: Used to equalize sequence lengths in a batch. Ignored by the loss function.
*   `<unk>`: Out of vocabulary (rare, since you tokenize at the character level).