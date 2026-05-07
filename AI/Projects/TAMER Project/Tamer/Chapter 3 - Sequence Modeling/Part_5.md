## 8. The Tensor Journey: Dimensional Shifts during Decoding

To understand why your model works, you must follow the "Shape" of the data as it transforms from a single integer ID to a LaTeX character.

1.  **Step 0: Tokenization:** The word `\frac` is converted to integer `42`.
2.  **Step 1: Embedding:** Integer `42` is looked up in the embedding matrix. It becomes a vector of size **768**.
3.  **Step 2: Positional Encoding:** A 1D sine wave is added to this vector so the model knows this is the *first* token in the sequence.
4.  **Step 3: The 10-Layer Gauntlet:** The vector passes through the 10 blocks described above. It interacts with the image features. By the time it leaves Layer 10, the vector `[0.12, -0.5, ...]` has been modified by the attention heads to represent the "idea" of the symbol sitting at the visual coordinates of the numerator.
5.  **Step 4: The Output Projection:** The vector is multiplied by a massive matrix of size $(768 \times \text{Vocab\_Size})$. 
6.  **Step 5: The Logits:** This produces a list of "Logits" (scores). If your vocab has 500 tokens, you get 500 scores.
7.  **Step 6: Softmax/Argmax:** The highest score (e.g., at index 105) is chosen. You look at your vocabulary, and index 105 corresponds to the character `{`. 

**Why the dimensions are specific:**
*   **768:** Small enough to allow a Batch Size of 36 on your 96GB GPU, but large enough to hold the "meaning" of complex LaTeX commands.
*   **10 Layers:** Deep enough to resolve the nested structure of math (fractions within square roots).
*   **12 Heads:** Allows the model to look at 12 different things simultaneously (e.g., Head 1 looks for the next character, Head 2 looks for a closing bracket, Head 3 looks for a superscript).
