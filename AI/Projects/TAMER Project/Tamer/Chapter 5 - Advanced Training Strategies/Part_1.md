# Chapter 5: Advanced Training Strategies and Loss Functions

## 1. Cross Entropy and Label Smoothing

**The Standard Loss:**
Autoregressive models are trained using **Cross-Entropy Loss**, which penalizes the model based on how far its predicted probability distribution is from the true target token.

**Label Smoothing:**
A model trained with pure Cross-Entropy becomes overconfident, pushing the probability of the correct token to 99.9% and all others to 0%. This leads to overfitting.
**Label Smoothing** (set to 0.1) steals 10% of the probability mass from the correct token and distributes it evenly among all other tokens in the vocabulary. The model is penalized if it becomes too confident, forcing it to learn generalized feature representations rather than memorizing the training data.

## 2. Structure Aware Loss and Global Token Averaging

**The Problem with Standard Averaging:**
In batches containing both short and long sequences, standard loss functions compute the average loss *per sequence*, and then average the batch.
*   A 1-token error in a 5-token equation adds $1/5 = 0.20$ to the batch loss.
*   A 1-token error in a 50-token matrix adds $1/50 = 0.02$ to the batch loss.
*Result:* The model realizes it can ignore complex matrices because their gradients are suppressed by the denominator.

**The Fix: Global Token Averaging:**
Your `StructureAwareLoss` flattens the entire batch into a 1D array. It sums the loss of every valid token, and divides by the *total valid tokens in the batch* (`N_valid`). Now, every token contributes exactly `1/N_valid`. A matrix token is treated identically to an algebra token.

**Structure-Aware Weighting:**
Getting a `+` sign wrong is a minor error. Getting a row separator `\\` or column separator `&` wrong destroys the entire 2D layout of a matrix. 
You assign a **3.0x multiplier** to structural tokens (`\\`, `&`, `\begin{...}`). 
By applying this multiplier during Global Token Averaging, structural errors dominate the gradient, forcing the optimizer to aggressively correct layout mistakes.

## 3. Curriculum Learning

**The Theory:**
Humans don't learn calculus before arithmetic. Neural networks also struggle if fed extreme noise and complexity before learning basic features.

**TAMER's Implementation:**
You categorized the dataset complexity based on mathematical structural density (e.g., matrices and fractions are `complex`, basic algebra is `simple`).
*   **Stage 1**: Train only on `simple` single-line equations. The model learns to map visual strokes to basic tokens.
*   **Stage 2**: Introduce `medium` equations.
*   **Stage 3**: Uncap everything; introduce messy, handwritten `complex` matrices.

## 4. Temperature Based Dataset Sampling

**The Dataset Imbalance Problem:**
You have 4 datasets: Im2LaTeX (100k printed), MathWriting (50k clean), HME100K (100k messy), CROHME (10k competition). If you sample uniformly, CROHME is heavily undersampled. If you sample sequentially, the model catastrophically forgets earlier datasets.

**Temperature Sampling Math:**
Probability of choosing dataset $i$: 
$$ P(i) = \frac{(n_i)^T}{\sum (n_j)^T} $$
Where $n_i$ is the number of samples in dataset $i$, and $T$ is the temperature.
*   **$T=1.0$**: Proportional. (Im2LaTeX dominates).
*   **$T=0.0$**: Uniform. (All 4 datasets sampled exactly 25% of the time).

**Dynamic Scheduling:**
You implemented a decaying temperature (`temp_start=0.8`, `temp_end=0.4`). Early in training, the model samples mostly proportionally, tearing through large datasets quickly to learn general syntax. Later in training, the temperature drops, forcing the model to oversample the small, highly difficult datasets (like CROHME) to fine-tune its performance.