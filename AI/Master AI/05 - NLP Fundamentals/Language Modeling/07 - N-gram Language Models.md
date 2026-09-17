---
tags: [nlp, language-modeling, ngram]
iteration: 11
created: 2026-08-07
last_updated: 2026-08-08
aliases: [N-gram Language Models]
---

# 07 - N-gram Language Models

> [!info] TL;DR
> Before neural LMs, there were n-gram LMs: estimate $P(w_t \mid w_{t-n+1}, \ldots, w_{t-1})$ by counting in a corpus. Simple, fast, interpretable — and still useful as a baseline and for speculative decoding.

## The Idea

A language model assigns probabilities to sequences:

$$
P(w_1, w_2, \ldots, w_T) = \prod_{t=1}^{T} P(w_t \mid w_1, \ldots, w_{t-1})
$$

Computing the full conditional is infeasible (too many possible histories). The **Markov assumption**: only the last $n-1$ words matter:

$$
P(w_t \mid w_1, \ldots, w_{t-1}) \approx P(w_t \mid w_{t-n+1}, \ldots, w_{t-1})
$$

This is an **n-gram model**. Bigram ($n=2$): condition on previous word. Trigram ($n=3$): condition on previous two.

## Estimation by Counting

$$
P(w_t \mid w_{t-n+1}, \ldots, w_{t-1}) = \frac{\text{count}(w_{t-n+1}, \ldots, w_t)}{\text{count}(w_{t-n+1}, \ldots, w_{t-1})}
$$

For a bigram model: $P(w_t \mid w_{t-1}) = \frac{\text{count}(w_{t-1}, w_t)}{\text{count}(w_{t-1})}$.

```python
from collections import Counter
from nltk import bigrams

tokens = "the cat sat on the mat the cat ran".split()
unigram_counts = Counter(tokens)
bigram_counts = Counter(bigrams(tokens))

def bigram_prob(w_prev, w):
    return bigram_counts[(w_prev, w)] / unigram_counts[w_prev]

print(bigram_prob("the", "cat"))  # 2/3 — "the cat" appears 2 of 3 "the"s
```

## The Problem: Sparsity

For trigrams, there are $|V|^3$ possible trigrams. Most never appear in the corpus, so the count is 0 — but the true probability isn't 0. The model assigns 0 probability to any unseen trigram, which means it assigns 0 probability to entire sentences.

### Smoothing

Add a small constant to all counts:

$$
P_{\text{smooth}}(w_t \mid \ldots) = \frac{\text{count}(\ldots, w_t) + \alpha}{\text{count}(\ldots) + \alpha |V|}
$$

This is **additive (Laplace) smoothing** for $\alpha = 1$. More sophisticated:
- **Kneser-Ney smoothing**: the standard for n-gram LMs. Handles both seen and unseen n-grams gracefully.
- **Backoff**: if the trigram count is too small, fall back to bigram, then unigram.
- **Interpolation**: linearly combine trigram, bigram, unigram probabilities.

## Strengths of N-gram Models

- **Simple**: just counting.
- **Fast**: lookup is O(1) per token.
- **Interpretable**: you can inspect any probability.
- **No training in the modern sense**: just count and store.
- **Online**: easy to update with new data.

## Weaknesses

- **Sparsity**: needs smoothing.
- **No semantic understanding**: "cat sat on mat" and "feline rested on rug" are completely unrelated to an n-gram model.
- **No long-range dependencies**: a 5-gram model can't relate words 6 apart.
- **Exponential growth**: $n$-grams grow as $|V|^n$ — practical limit is $n = 4$ or $5$.
- **No generalization to unseen words**: out-of-vocabulary tokens are stuck.

## Modern Uses

Despite being "obsolete", n-grams are still useful:

### 1. Speculative decoding
N-gram models (especially "lookahead" n-grams from the prompt) are used as cheap draft models for speculative decoding. See [[13 - Inference/Speculative Decoding/Speculative Decoding|Speculative Decoding]].

### 2. Baseline for LM evaluation
If your neural LM doesn't beat an n-gram baseline, something is wrong.

### 3. Spelling correction / fuzzy matching
N-gram overlap (especially character n-grams) is a robust similarity measure for noisy text.

### 4. Search and IR
BM25 (next note) is essentially an n-gram model adapted for document retrieval.

### 5. Lightweight on-device LMs
For very constrained environments (microcontrollers), n-gram LMs are still viable.

## Worked Example (Trigram LM with Kneser-Ney)

```python
# Pseudocode — full KN smoothing is intricate
class TrigramLM:
    def __init__(self, corpus):
        self.tri_counts = Counter()
        self.bi_counts = Counter()
        self.uni_counts = Counter()
        # Build counts from corpus (left as exercise)
    
    def prob(self, w1, w2, w3):
        # Kneser-Ney: combination of trigram, bigram, unigram with discounts
        # Simplified — see Chen & Goodman (1999) for the full formulation
        return self._kn_prob(w1, w2, w3)
    
    def perplexity(self, text):
        log_prob = sum(np.log(self.prob(*triple)) for triple in trigrams(text))
        return np.exp(-log_prob / (len(text) - 2))
```

## Why This Matters for AI

- N-gram models are the **historical baseline** for language modeling. Neural LMs are evaluated against them.
- The shift from n-grams to neural LMs (Bengio 2003, then Word2Vec, then Transformers) is the **foundational story** of modern NLP.
- N-gram concepts (Markov assumption, smoothing) appear in modern contexts: trigram language identification, BM25 retrieval, n-gram overlap metrics (BLEU, ROUGE).
- For **speculative decoding**, n-gram models provide a cheap draft that doesn't require running another LLM.

## Production Implications

- For **search**, use BM25 (an n-gram-derived scoring function) — still SOTA for keyword search.
- For **spelling correction**, character n-grams are robust and cheap.
- For **speculative decoding** in latency-sensitive settings, a prompt-derived n-gram model is essentially free.
- Don't use n-gram LMs for actual text generation — neural LMs are vastly better.

## Common Pitfalls

- **Forgetting smoothing** — your LM will assign 0 probability to any sentence containing an unseen n-gram.
- **Wrong vocabulary handling** — out-of-vocabulary tokens need an explicit `<UNK>` strategy.
- **Mixing up conditional direction** — $P(w_t \mid w_{t-1})$ ≠ $P(w_{t-1} \mid w_t)$.
- **Reporting perplexity across different tokenizers** — meaningless. See [[08 - Perplexity]].

## Further Reading

- Jurafsky & Martin, *Speech and Language Processing*, Chapter 3 (n-gram LMs).
- Chen & Goodman (1999), *An Empirical Study of Smoothing Techniques for Language Modeling* (Kneser-Ney).

## See Also

- [[08 - Perplexity]]
- [[05 - Word2Vec GloVe FastText]]
- [[09 - TF-IDF]]
- [[10 - BM25]]
- [[05 - NLP Fundamentals/MOC|NLP MOC]]

## Kneser-Ney Smoothing — The Details

Kneser-Ney (KN) smoothing is the standard for n-gram LMs. The key idea: absolute discounting + backoff with a continuations-based lower-order distribution.

### Absolute discounting

Subtract a constant $d$ from each non-zero count:

$$
P_{\text{abs}}(w_i \mid w_{i-n+1}^{i-1}) = \frac{\max(\text{count}(w_{i-n+1}^i) - d, 0)}{\text{count}(w_{i-n+1}^{i-1})} + \lambda(w_{i-n+1}^{i-1}) P(w_i \mid w_{i-n+2}^{i-1})
$$

where $\lambda$ is a normalization weight that distributes the discounted probability mass to the lower-order model. $d \approx 0.75$ is typical.

### Continuations-based lower-order distribution

The standard lower-order distribution $P(w_i \mid w_{i-n+2}^{i-1})$ overweights frequent words. KN replaces it with a continuations-based distribution: how many distinct words does $w_i$ follow?

$$
P_{\text{cont}}(w_i) = \frac{|\{w : \text{count}(w, w_i) > 0\}|}{|\{(w, w') : \text{count}(w, w') > 0\}|}
$$

This gives credit to words that appear in many distinct contexts (good continuations), not just frequent words. For predicting "I want to ___", "eat" is a better continuation than "the", even though "the" is more frequent overall.

### Modified KN (the standard)

Modified KN (interpolated) blends the discounted high-order probability with the lower-order continuations probability. This is the version used in practice. The exact formulas are intricate; see Chen & Goodman (1999) for the full treatment.

## Modern Uses — Detailed

### Speculative decoding draft models

N-gram models (especially prompt-derived ones) are used as cheap draft models for speculative decoding. The idea: build an n-gram model on-the-fly from the prompt, use it to predict the next $K$ tokens, and verify with the expensive LLM. If the n-gram is right, you save $K$ LLM forward passes. Hit rate: 30-60% for repetitive content (code, structured output). Cost: building the n-gram model is $O(N)$ per prompt; querying is $O(1)$ per token.

### BM25 (the n-gram for search)

BM25 is essentially an n-gram model adapted for document retrieval. It scores documents by how well they match a query, using term frequency (TF) and inverse document frequency (IDF) with saturation and length normalization. The BM25 score for a document $d$ and query $q$:

$$
\text{BM25}(d, q) = \sum_{t \in q} \text{IDF}(t) \cdot \frac{\text{TF}(t, d) \cdot (k_1 + 1)}{\text{TF}(t, d) + k_1 \cdot (1 - b + b \cdot |d| / \text{avgdl})}
$$

$k_1 = 1.2$, $b = 0.75$ are typical. BM25 is the standard for keyword search in 2026 — every search engine uses it or a variant.

### Character n-grams for fuzzy matching

Character n-grams are robust to typos and morphology. "café" and "cafe" share most character n-grams. Used for: spell checking, fuzzy search, deduplication, near-duplicate detection. Jaccard similarity on character n-gram sets is a standard metric.

## Worked Example: Trigram LM with KN Smoothing

```python
from collections import Counter, defaultdict

class TrigramLM:
    """Trigram LM with absolute discounting and backoff."""
    def __init__(self, d=0.75):
        self.d = d  # Discount constant
        self.tri_counts = Counter()  # count(w_{t-2}, w_{t-1}, w_t)
        self.bi_counts = Counter()   # count(w_{t-1}, w_t) — for continuations
        self.uni_counts = Counter()  # count(w_t)
        self.context_counts = Counter()  # count(w_{t-2}, w_{t-1})

    def train(self, tokens):
        for i in range(2, len(tokens)):
            self.tri_counts[(tokens[i-2], tokens[i-1], tokens[i])] += 1
            self.bi_counts[(tokens[i-1], tokens[i])] += 1
            self.uni_counts[tokens[i]] += 1
            self.context_counts[(tokens[i-2], tokens[i-1])] += 1

    def prob(self, w1, w2, w3):
        """P(w3 | w1, w2) with absolute discounting + backoff."""
        tri = self.tri_counts.get((w1, w2, w3), 0)
        ctx = self.context_counts.get((w1, w2), 0)

        if ctx == 0:
            # Unseen context: fall back to unigram
            return self._unigram_prob(w3)

        # Discounted trigram probability
        discounted = max(tri - self.d, 0) / ctx

        # Continuations-based lower-order (simplified)
        continuation_count = sum(1 for w in self.uni_counts if (w, w3) in self.bi_counts)
        total_continuations = len(self.bi_counts)
        lower_order = continuation_count / max(total_continuations, 1)

        # Lambda (weight for lower-order)
        unique_followups = sum(1 for w in self.uni_counts if (w1, w2, w) in self.tri_counts)
        lam = (self.d / ctx) * unique_followups

        return discounted + lam * lower_order

    def _unigram_prob(self, w):
        total = sum(self.uni_counts.values())
        return self.uni_counts.get(w, 0) / max(total, 1)

    def perplexity(self, tokens):
        import math
        log_prob = 0
        n = 0
        for i in range(2, len(tokens)):
            p = self.prob(tokens[i-2], tokens[i-1], tokens[i])
            log_prob += math.log(max(p, 1e-10))
            n += 1
        return math.exp(-log_prob / max(n, 1))
```

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| PPL is infinity | Unseen n-gram with no smoothing | Apply Kneser-Ney or at least add-k smoothing |
| PPL is very high | Insufficient training data; too-large n | Use smaller n (trigram → bigram); or more data |
| Wrong conditional direction | $P(w_t \mid w_{t-1})$ vs $P(w_{t-1} \mid w_t)$ | Double-check: $P(w_t \mid w_{t-1}) = \text{count}(w_{t-1}, w_t) / \text{count}(w_{t-1})$ |
| Comparing PPL across tokenizers | Different tokenizers give different PPL | Only compare PPL within the same tokenizer |

## Connection to Other Concepts

- [[05 - NLP Fundamentals/Language Modeling/08 - Perplexity|Perplexity]] — the standard LM metric.
- [[05 - NLP Fundamentals/Pre-Transformer NLP/10 - BM25|BM25]] — n-gram for search.
- [[05 - NLP Fundamentals/Pre-Transformer NLP/09 - TF-IDF|TF-IDF]] — simpler n-gram.
- [[05 - NLP Fundamentals/Embeddings/05 - Word2Vec GloVe FastText|Word2Vec GloVe FastText]] — the neural successor.
- [[08 - LLMs/MOC|LLMs MOC]] — modern neural LMs.
- [[13 - Inference/Speculative Decoding/05 - Speculative Decoding|Speculative Decoding]] — modern use of n-grams as draft models.
- [[26 - Papers/Agents and RAG/35 - RAG 2020|RAG 2020]] — retrieval uses BM25.
- [[26 - Papers/Transformers/02 - Vaswani Attention Is All You Need 2017|Vaswani 2017]] — what replaced n-gram LMs.

## Interview Questions

1. **Q: Explain the Markov assumption and why it enables n-gram models.**
   A: The Markov assumption: only the last $n-1$ words matter for predicting the next word. $P(w_t \mid w_1, \ldots, w_{t-1}) \approx P(w_t \mid w_{t-n+1}, \ldots, w_{t-1})$. This reduces the problem from estimating $P(w_t \mid \text{arbitrary history})$ (infeasible) to estimating $P(w_t \mid n-1 \text{ words})$ (tractable via counting). For trigrams: $P(w_t \mid w_{t-2}, w_{t-1}) = \text{count}(w_{t-2}, w_{t-1}, w_t) / \text{count}(w_{t-2}, w_{t-1})$. The cost: the model can't capture long-range dependencies (beyond $n-1$ words).

2. **Q: What is Kneser-Ney smoothing and why is it the standard?**
   A: KN combines: (1) **absolute discounting** — subtract a constant $d \approx 0.75$ from each non-zero count and redistribute the mass to lower-order models; (2) **continuations-based lower-order distribution** — instead of raw unigram probability, use how many distinct contexts $w_i$ follows. This gives credit to words that appear in many distinct contexts (good continuations), not just frequent words. For "I want to ___", "eat" is a better continuation than "the", even though "the" is more frequent. KN handles both seen and unseen n-grams gracefully, which is why it's the standard for n-gram LMs.

3. **Q: Why did n-gram LMs lose to neural LMs?**
   A: Three reasons. (1) **No semantic understanding** — "cat sat on mat" and "feline rested on rug" are completely unrelated to an n-gram model. Neural LMs learn distributed representations that capture semantic similarity. (2) **No long-range dependencies** — a 5-gram model can't relate words 6 apart. Neural LMs (especially Transformers) can attend to any position. (3) **Sparsity** — n-grams need smoothing because most n-grams never appear in training. Neural LMs generalize via distributed representations; no smoothing needed. The shift (Bengio 2003 → Word2Vec → Transformers) is the foundational story of modern NLP.

4. **Q: How are n-grams still useful in modern LLM systems?**
   A: Four uses. (1) **Speculative decoding** — n-gram models (especially prompt-derived) serve as cheap draft models. If the n-gram is right, you save an LLM forward pass. Hit rate: 30-60% for repetitive content. (2) **Search (BM25)** — BM25 is an n-gram-derived scoring function; still SOTA for keyword search. Every search engine uses it. (3) **Spelling correction / fuzzy matching** — character n-grams are robust to typos. (4) **Lightweight on-device LMs** — for microcontrollers, n-gram LMs are still viable.

5. **Q: What is the relationship between n-gram LMs and BM25?**
   A: BM25 is essentially an n-gram model adapted for document retrieval. It scores documents by how well they match a query, using term frequency (TF) and inverse document frequency (IDF) with saturation (TF capped) and length normalization (document length penalty). The BM25 score is a sum over query terms, similar to how an n-gram LM computes a sum of log-probabilities. BM25 is the standard for keyword search in 2026 — it's still competitive with neural retrieval on many tasks, especially for rare terms that neural embedders miss.

6. **Q: How would you build a prompt-derived n-gram model for speculative decoding?**
   A: (1) Build an n-gram model on-the-fly from the prompt: scan the prompt, count n-grams (typically trigrams or 4-grams). (2) Use this model to predict the next $K$ tokens (e.g., $K = 4$). (3) Feed the $K$ tokens to the expensive LLM for verification. (4) Accept the longest matching prefix; reject the rest. (5) Re-verify the rejected tokens with the LLM. Hit rate: 30-60% for repetitive content (code, structured output, formulaic text). The n-gram model is essentially free (build in $O(N)$ per prompt, query in $O(1)$ per token), so even a 30% hit rate gives a meaningful speedup.

## See Also

- [[08 - Perplexity]]
- [[05 - Word2Vec GloVe FastText]]
- [[09 - TF-IDF]]
- [[10 - BM25]]
- [[05 - NLP Fundamentals/MOC|NLP MOC]]
