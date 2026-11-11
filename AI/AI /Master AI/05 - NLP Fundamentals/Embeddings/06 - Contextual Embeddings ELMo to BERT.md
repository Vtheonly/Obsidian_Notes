---
tags: [nlp, embeddings, contextual, bert, elmo]
iteration: 9
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Contextual Embeddings ELMo to BERT]
---

# 06 - Contextual Embeddings: ELMo → BERT

> [!info] TL;DR
> Static embeddings (Word2Vec, GloVe) give each word one fixed vector. **Contextual embeddings** give each word a different vector depending on its context. ELMo (2018) used bidirectional LSTMs; BERT (2018) used bidirectional Transformers. This shift unlocked modern NLP.

## The Problem with Static Embeddings

Word2Vec and GloVe assign each word a single vector. But words are ambiguous:

- "bank" — river bank? money bank? banked shot?
- "apple" — fruit? company?
- "light" — weight? illumination? verb?

A single vector must average these senses, blurring them. The model can't disambiguate from context.

Contextual embeddings solve this by **conditioning the embedding on the entire context**. The vector for "bank" in "I fished by the river bank" differs from "I deposited money in the bank."

## ELMo (Embeddings from Language Models, 2018)

Peters et al. (2018) used a **bidirectional LSTM** trained as a language model. For each word, the embedding is a weighted combination of the LSTM's hidden states (forward + backward):

$$
\text{ELMo}(word_i) = \gamma \sum_{j=0}^{L} s_j \mathbf{h}_{j, i}
$$

where $\mathbf{h}_{j, i}$ is the hidden state at layer $j$ for word $i$ (concatenating forward and backward), and $s_j$ are learned layer weights.

### Why ELMo was a big deal
- **Contextual**: each word's embedding depends on the whole sentence.
- **Pretrained**: trained once on a large corpus, used as features for many downstream tasks.
- **State-of-the-art** on many NLP benchmarks when released.

### Limitations
- LSTM-based — slow to train, can't parallelize.
- **Shallow contextualization**: the LSTM hidden state mixes information but slowly.
- Used as **features** for downstream models, not fine-tuned end-to-end.

## BERT (Bidirectional Encoder Representations from Transformers, 2018)

Devlin et al. (2018) replaced ELMo's LSTM with a Transformer encoder. Key innovations:

### 1. Bidirectional Transformer encoder
Each token attends to all other tokens (no causal mask). The representation of each word is built from the full context, both left and right.

### 2. Masked Language Model (MLM) pretraining
Randomly mask 15% of tokens; predict them from the rest. Forces the model to use bidirectional context.

```
Input:  the man went to the [MASK] to buy [MASK]
Target: store, milk
```

### 3. Next Sentence Prediction (NSP)
Predict whether two sentences are adjacent in the original text. (Later research showed NSP doesn't help much; RoBERTa dropped it.)

### 4. Fine-tuning, not feature extraction
Unlike ELMo, BERT is fine-tuned end-to-end on each downstream task. Same model, different heads:

- Classification: `[CLS]` token + linear head.
- NER: per-token linear head.
- Q&A: predict start and end positions.

### Impact
BERT set SOTA on 11 NLP benchmarks simultaneously. It kicked off the "pretrain then fine-tune" paradigm that still dominates NLP.

## The Evolution Continues

| Model   | Year | Key change                                     |
|---------|------|------------------------------------------------|
| ELMo    | 2018 | BiLSTM contextual embeddings                   |
| BERT    | 2018 | Bidirectional Transformer; MLM; fine-tune      |
| RoBERTa | 2019 | More data, bigger batches, drop NSP            |
| ALBERT  | 2019 | Factorized embeddings; parameter sharing       |
| DeBERTa | 2020 | Disentangled attention; enhanced mask decoder  |
| ELECTRA | 2020 | Replaced token detection (more efficient)      |
| T5      | 2019 | Encoder-decoder; text-to-text framing          |
| GPT-2/3 | 2019/20 | Decoder-only; autoregressive; scale         |

The encoder branch (BERT family) is best for classification, NER, extraction. The decoder branch (GPT family) is best for generation. The encoder-decoder branch (T5, BART) handles both.

## Worked Example (BERT for classification)

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

inputs = tokenizer("This movie was great!", return_tensors="pt")
outputs = model(**inputs)
logits = outputs.logits  # (1, 2)
```

For fine-tuning: standard supervised training on labeled data, learning rate ~2e-5, 3–5 epochs.

## Why This Matters for AI

- **BERT kicked off the modern NLP era**. The pretrain-then-fine-tune paradigm originated here.
- BERT-style models are still widely used in production for classification, NER, and embedding (sentence-transformers).
- The shift from static to contextual embeddings was the conceptual leap that made LLMs possible.
- For **retrieval / RAG**, BERT-family encoders power many embedding models (BGE, E5 — descendants of BERT architecture).

## Production Implications

- For **classification / NER / extraction** tasks, a fine-tuned BERT-family model is often the right choice — smaller, faster, and more accurate than an LLM.
- For **embeddings** in RAG, use sentence-transformers or BGE (BERT-family with contrastive training).
- BERT models are cheap to fine-tune (an hour on a single GPU) and cheap to serve.
- For **generation**, BERT is wrong — use a decoder-only model (Llama, GPT).

## Common Pitfalls

- **Using BERT for generation** — it can't generate; it's bidirectional.
- **Wrong tokenizer** — `bert-base-uncased` requires lowercased input.
- **Forgetting `[CLS]` and `[SEP]`** — most HuggingFace tokenizers add these automatically with `tokenizer(text)`, but raw `encode` may not.
- **Max sequence length** — BERT is limited to 512 tokens. For longer documents, use sliding window or Longformer.

## Further Reading

- Peters et al. (2018), *Deep Contextualized Word Representations* (ELMo).
- Devlin et al. (2019), *BERT: Pre-training of Deep Bidirectional Transformers*.
- Liu et al. (2019), *RoBERTa: A Robustly Optimized BERT Pretraining Approach*.

## The Static-to-Contextual Revolution (Detailed Timeline)

### 2013: Word2Vec (static)
- Each word → one vector, learned via skip-gram or CBOW.
- "bank" has the same vector whether it's a river bank or a financial bank.
- Polysemy is a fundamental limitation.

### 2014: GloVe (static)
- Global Vectors — learned via matrix factorization of co-occurrence counts.
- Same limitation as Word2Vec: one vector per word.

### 2018 (Feb): ELMo (contextual, LSTM-based)
- Peters et al. — "Deep Contextualized Word Representations".
- Bidirectional LSTM; the embedding is the concatenation of forward and backward LSTM hidden states.
- "bank" in "river bank" gets a different vector than "bank" in "bank account".
- **Limitation**: LSTM-based — slow to train, limited context (LSTM forgets).

### 2018 (Oct): BERT (contextual, Transformer-based)
- Devlin et al. — bidirectional Transformer encoder.
- MLM pretraining: predict masked tokens using full bidirectional context.
- Massively better than ELMo on downstream tasks.
- **Limitation**: encoder-only — not suited for generation.

### 2019: RoBERTa, DistilBERT, ALBERT
- RoBERTa: better pretraining recipe (more data, dynamic masking, no NSP).
- DistilBERT: knowledge distillation, 40% smaller, 60% faster.
- ALBERT: parameter sharing, fewer params, similar quality.

### 2020+: Sentence Transformers, Modern Embedding Models
- Sentence-BERT: pool BERT outputs for sentence embeddings.
- Modern: BGE, GTE, E5, OpenAI text-embedding-3 — trained for retrieval, not MLM.
- See [[09 - Foundation Models/Embedding Models/02 - Embedding Models for Retrieval|Embedding Models for Retrieval]].

## Why Contextual Embeddings Solved Polysemy

The key insight: a word's meaning depends on its context. Static embeddings can't capture this — they assign one vector per word type. Contextual embeddings assign one vector per word **token** — the vector depends on the full sentence.

### Mathematical formulation
For a static embedding model: $\text{embed}(\text{"bank"}) = \mathbf{v} \in \mathbb{R}^d$ — same vector regardless of context.

For a contextual embedding model: $\text{embed}(\text{"bank"} \mid \text{"I went to the river bank"}) = \mathbf{v}_1$, $\text{embed}(\text{"bank"} \mid \text{"I deposited money in the bank"}) = \mathbf{v}_2$, with $\mathbf{v}_1 \neq \mathbf{v}_2$.

The contextual embedding is computed by the Transformer: $\mathbf{v} = \text{Transformer}(\text{sentence})_{\text{position of "bank"}}$. Self-attention lets the model incorporate context from all other words in the sentence.

### Empirical evidence
- Cosine similarity between "bank" in "river bank" and "bank" in "bank account": ~0.3 (static) vs. ~0.7 (contextual — both are still "bank" in some sense).
- Cosine similarity between "bank" in "river bank" and "shore" in "river shore": ~0.2 (static — "bank" and "shore" are different words) vs. ~0.85 (contextual — the model knows they mean the same thing in context).

## ELMo vs. BERT: Why BERT Won

| Aspect                | ELMo (2018)                     | BERT (2018)                       |
|-----------------------|---------------------------------|-----------------------------------|
| Architecture          | Bidirectional LSTM              | Bidirectional Transformer encoder |
| Context               | Sequential (LSTM hidden states) | Full bidirectional (self-attention) |
| Pretraining           | Language modeling (forward + backward) | Masked Language Modeling (MLM) |
| Quality on GLUE       | 70-75%                          | 80-85%                            |
| Training speed        | Slow (LSTM sequential)          | Fast (Transformer parallel)       |
| Scalability           | Limited (LSTM vanishing gradients) | Scales to billions of params   |

### Why Transformer beat LSTM
1. **Full bidirectional context**: BERT's self-attention lets every token attend to every other token in one pass. ELMo's bidirectional LSTM concatenates forward and backward, but each direction is still sequential.
2. **Parallelism**: Transformer layers are fully parallel — train 10× faster than LSTM on GPUs.
3. **Scalability**: Transformers scale to billions of parameters without vanishing gradients. LSTMs struggle past a few layers.
4. **MLM pretraining**: BERT's masked LM is harder than ELMo's forward/backward LM, forcing deeper representations.

## Worked Example: Comparing Static and Contextual Embeddings

```python
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

# Static: Word2Vec (simulated)
# In practice: from gensim.models import KeyedVectors
# word2vec["bank"] = same vector for all contexts

# Contextual: BERT
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

def get_contextual_embedding(sentence, target_word):
    """Get BERT's contextual embedding for target_word in sentence."""
    inputs = tokenizer(sentence, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    # Find the position of target_word
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    target_pos = tokens.index(target_word)
    # Return the contextual embedding (last hidden state)
    return outputs.last_hidden_state[0, target_pos].numpy()

# Same word, different contexts
v1 = get_contextual_embedding("I sat by the river bank", "bank")
v2 = get_contextual_embedding("I deposited money in the bank", "bank")
v3 = get_contextual_embedding("I sat by the river shore", "shore")

print(f"bank (river) vs. bank (money): {cosine_similarity([v1], [v2])[0][0]:.3f}")
print(f"bank (river) vs. shore (river): {cosine_similarity([v1], [v3])[0][0]:.3f}")

# Expected: bank-vs-bank ~0.7 (same word, different sense)
# bank (river) vs. shore (river) ~0.85 (different word, same meaning in context)
# This demonstrates contextual embeddings capture meaning, not just word type
```

## Modern Contextual Embedding Models (2024-2026)

The BERT lineage evolved into modern embedding models optimized for retrieval:

| Model                  | Year | Base Architecture | Training Signal                | Best For                |
|------------------------|------|-------------------|--------------------------------|-------------------------|
| BERT                   | 2018 | Encoder           | MLM + NSP                      | Classification, NER     |
| Sentence-BERT          | 2019 | Encoder           | Mean pooling + contrastive     | Sentence similarity     |
| SimCSE                 | 2021 | Encoder           | Contrastive (dropout)          | Sentence embeddings     |
| E5                     | 2022 | Encoder           | Text-text contrastive          | Retrieval               |
| BGE                    | 2023 | Encoder           | Multi-stage contrastive        | Retrieval, multilingual |
| GTE                    | 2023 | Decoder (Llama)   | Contrastive                    | Retrieval               |
| OpenAI text-embedding-3| 2024 | Unknown           | Contrastive                    | General-purpose         |

The key shift: from MLM pretraining (BERT) to **contrastive pretraining** (BGE, E5, GTE). Modern embedding models are trained directly for retrieval quality, not language modeling.

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| BERT embeddings not capturing domain semantics | BERT trained on general text | Fine-tune on domain data; use domain-specific model |
| Sentence embeddings poorly clustered | Mean pooling inadequate | Use CLS token; or use Sentence-BERT / BGE |
| Embeddings from different layers inconsistent | Wrong layer choice | Use last 4 layers averaged (BERTology finding); or last layer |
| Cross-model similarity meaningless | Different embedding spaces | Never compare embeddings from different models |
| BERT slow for retrieval | Encoder is heavy | Use Sentence-BERT (smaller); or BGE-small |

## Connection to Other Concepts

- [[05 - NLP Fundamentals/Embeddings/05 - Word2Vec GloVe FastText|Word2Vec/GloVe/FastText]] — static predecessors.
- [[05 - NLP Fundamentals/Tokenization/03 - WordPiece|WordPiece]] — BERT's tokenizer.
- [[07 - Transformers/Encoder Models/07 - BERT|BERT]] — detailed BERT note.
- [[09 - Foundation Models/Embedding Models/02 - Embedding Models for Retrieval|Embedding Models for Retrieval]] — modern retrieval embeddings.
- [[09 - Foundation Models/Embedding Models/06 - Embedding Model Training|Embedding Model Training]] — contrastive training.
- [[14 - Interpretability/Probing/05 - Probing|Probing]] — analyzing what BERT encodes.
- [[17 - RAG/Ingestion and Retrieval/01 - RAG Pipeline Overview|RAG Pipeline]] — embeddings for retrieval.
- [[02 - Mathematics/Linear Algebra/03 - Cosine Similarity|Cosine Similarity]] — comparing embeddings.

## Interview Questions

1. **Q: What's the key difference between static and contextual embeddings?**
   A: Static (Word2Vec, GloVe): one vector per word type — "bank" has the same vector regardless of context. Contextual (ELMo, BERT): one vector per word token — "bank" in "river bank" gets a different vector than "bank" in "bank account". Contextual embeddings are computed by the Transformer incorporating the full sentence context via self-attention.

2. **Q: Why did BERT replace ELMo?**
   A: Four reasons. (1) Full bidirectional context: BERT's self-attention lets every token attend to every other in one pass; ELMo's bidirectional LSTM concatenates forward/backward, each sequential. (2) Parallelism: Transformer layers train 10× faster than LSTM on GPUs. (3) Scalability: Transformers scale to billions without vanishing gradients; LSTMs struggle past a few layers. (4) MLM pretraining is harder than LM, forcing deeper representations. Result: BERT beat ELMo by 10-15% on GLUE.

3. **Q: How do contextual embeddings solve polysemy?**
   A: A word's meaning depends on context. Static embeddings assign one vector per word type — can't distinguish "bank" (river) from "bank" (money). Contextual embeddings assign one vector per word token — the vector is computed by the Transformer incorporating the full sentence. Self-attention lets "bank" attend to "river" (giving the water-bank vector) or "money" (giving the financial-bank vector). Empirically, the cosine similarity between "bank" in different contexts is ~0.7 (still "bank") but between "bank" and "shore" in the same context is ~0.85 (same meaning).

4. **Q: What is MLM, and why is it better than standard LM for pretraining?**
   A: MLM (Masked Language Modeling): mask 15% of tokens, predict them from the full bidirectional context. Standard LM: predict next token from left context only. MLM is better because (1) bidirectional — uses both left and right context; (2) harder — forces deeper representations; (3) more sample-efficient — every masked token is a training signal. BERT's MLM beat ELMo's forward/backward LM by 10-15% on GLUE.

5. **Q: How do modern embedding models (BGE, GTE) differ from BERT?**
   A: BERT is pretrained with MLM (language modeling). Modern embedding models (BGE, GTE, E5) are pretrained with **contrastive learning** — directly optimized for retrieval quality. They use positive pairs (query, relevant doc) and negative pairs (query, irrelevant doc), with InfoNCE loss. This produces embeddings better suited for retrieval than BERT's MLM embeddings. Modern embedding models also use larger context (512→8K), decoder architectures (GTE uses Llama), and multi-stage training (pretrain → fine-tune → distill).

6. **Q: When would you use BERT vs. a modern embedding model?**
   A: Use BERT for: classification, NER, token-level tasks (where MLM pretraining helps). Use modern embedding models (BGE, GTE) for: retrieval, semantic search, RAG (where contrastive pretraining helps). BERT's MLM embeddings are okay for retrieval but not optimal — they weren't trained for it. Modern embedding models are 5-20% better on retrieval benchmarks.

## See Also

- [[05 - Word2Vec GloVe FastText]]
- [[08 - Perplexity]]
- [[07 - Transformers/Encoder Models/BERT|BERT]] (planned full note)
- [[17 - RAG/Embeddings/Embedding Models|Embedding Models]] (planned)
- [[05 - NLP Fundamentals/MOC|NLP MOC]]