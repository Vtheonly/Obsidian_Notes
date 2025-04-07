# Calculating Entropy and Information Gain: A Note

In many machine learning applications—especially when building decision trees—**entropy** and **information gain** are essential metrics used to quantify the impurity of a dataset and to determine the best attribute for splitting the data.

---

## Entropy

Entropy measures the uncertainty or disorder in a set of data. In classification tasks, it indicates how mixed the classes are in a dataset.

### The Formula

\[
Entropy(S) = -\sum_{i=1}^{n} p_i \cdot \log_2(p_i)
\]

- **\(S\)**: The dataset.
- **\(p_i\)**: The probability (or proportion) of class \(i\) in \(S\).
- The logarithm is base 2 because we measure information in bits.

### Example Calculation of Entropy

Consider a dataset \(S\) with 10 samples:
- 6 positive examples
- 4 negative examples

First, calculate the class probabilities:

\[
p(\text{positive}) = \frac{6}{10} = 0.6 \quad \text{and} \quad p(\text{negative}) = \frac{4}{10} = 0.4
\]

Plug these into the formula:

\[
Entropy(S) = - \Bigl(0.6 \cdot \log_2(0.6) + 0.4 \cdot \log_2(0.4)\Bigr)
\]

Using approximate values:
- \(\log_2(0.6) \approx -0.737\)
- \(\log_2(0.4) \approx -1.322\)

The calculation becomes:

\[
Entropy(S) \approx - \Bigl(0.6 \times (-0.737) + 0.4 \times (-1.322)\Bigr)
\]
\[
\approx - \Bigl(-0.442 - 0.529\Bigr) \approx 0.971 \text{ bits}
\]

---

## Information Gain

Information Gain quantifies how much the entropy is reduced by splitting the dataset based on a particular attribute. It helps determine the attribute that best separates the classes.

### The Formula

\[
Gain(S, A) = Entropy(S) - \sum_{v \in Values(A)} \frac{|S_v|}{|S|} \cdot Entropy(S_v)
\]

- **\(S\)**: The entire dataset.
- **\(A\)**: The attribute on which the split is made.
- **\(S_v\)**: The subset of \(S\) where attribute \(A\) takes the value \(v\).
- \(|S_v|\) and \(|S|\) are the number of samples in \(S_v\) and \(S\), respectively.

### Example Calculation of Information Gain

Assume the same dataset \(S\) (10 samples with 6 positives and 4 negatives) is split by an attribute \(A\) into two subsets:

1. **Subset \(S_1\)** (7 samples):
   - 4 positive examples
   - 3 negative examples

2. **Subset \(S_2\)** (3 samples):
   - 2 positive examples
   - 1 negative example

#### Step 1: Calculate the Entropy for Each Subset

**For \(S_1\):**

- \(p(\text{positive}) = \frac{4}{7} \approx 0.571\)
- \(p(\text{negative}) = \frac{3}{7} \approx 0.429\)

\[
Entropy(S_1) = -\left(0.571 \cdot \log_2(0.571) + 0.429 \cdot \log_2(0.429)\right)
\]

Using approximate values:
- \(\log_2(0.571) \approx -0.807\)
- \(\log_2(0.429) \approx -1.222\)

\[
Entropy(S_1) \approx -\left(0.571 \times (-0.807) + 0.429 \times (-1.222)\right) \approx 0.985 \text{ bits}
\]

**For \(S_2\):**

- \(p(\text{positive}) = \frac{2}{3} \approx 0.667\)
- \(p(\text{negative}) = \frac{1}{3} \approx 0.333\)

\[
Entropy(S_2) = -\left(0.667 \cdot \log_2(0.667) + 0.333 \cdot \log_2(0.333)\right)
\]

Using approximate values:
- \(\log_2(0.667) \approx -0.585\)
- \(\log_2(0.333) \approx -1.585\)

\[
Entropy(S_2) \approx -\left(0.667 \times (-0.585) + 0.333 \times (-1.585)\right) \approx 0.918 \text{ bits}
\]

#### Step 2: Compute the Weighted Average Entropy After the Split

\[
\text{Weighted Entropy} = \frac{7}{10} \cdot Entropy(S_1) + \frac{3}{10} \cdot Entropy(S_2)
\]
\[
\approx \frac{7}{10} \times 0.985 + \frac{3}{10} \times 0.918
\]
\[
\approx 0.6895 + 0.2754 = 0.9649 \text{ bits}
\]

#### Step 3: Calculate the Information Gain

Recall the original entropy of \(S\) is approximately 0.971 bits. Now, subtract the weighted entropy:

\[
Gain(S, A) = Entropy(S) - \text{Weighted Entropy} \approx 0.971 - 0.9649 \approx 0.0061 \text{ bits}
\]

This very small information gain suggests that the attribute \(A\) does not significantly reduce the uncertainty in this particular example.

---

## Conclusion

- **Entropy** quantifies the impurity or disorder within a dataset.
- **Information Gain** measures the reduction in entropy after splitting the dataset on an attribute.
- In our example, splitting by attribute \(A\) yielded an information gain of approximately **0.0061 bits**, indicating that \(A\) is not very effective for separating the classes in this dataset.

This note outlines the step-by-step process for calculating entropy and information gain, along with a concrete example. Such calculations are fundamental when constructing decision trees, where the goal is to choose the attribute that best reduces uncertainty in the dataset.
