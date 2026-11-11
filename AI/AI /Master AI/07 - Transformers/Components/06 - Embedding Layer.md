---
tags: [transformer, components, embeddings, token-embeddings]
iteration: 2
created: 2026-08-07
aliases: [Embedding Layer, Token Embeddings]
---

# 06 - Embedding Layer

> [!info] TL;DR
> The embedding layer maps token IDs (integers) to dense vectors. It's a simple lookup table — but a huge one. For Llama 3 (128k vocab, 4096 dim), the embedding matrix is ~1B parameters, ~14% of the model. Important for parameter efficiency, tied-weights decisions, and quantization.

## The Mechanism

An embedding layer is a learned lookup table:

$$
\mathbf{e}_i = \mathbf{E}[i]
$$

where $\mathbf{E} \in \mathbb{R}^{|V| \times d}$ is the embedding matrix, $|V|$ is vocabulary size, $d$ is model dimension. The $i$-th row is the embedding for token $i$.

Equivalent to a one-hot multiplication:

$$
\mathbf{e}_i = \text{onehot}(i) \cdot \mathbf{E}
$$

In practice, it's a gather operation, not a matmul.

## Worked Implementation

```python
import torch.nn as nn

class TokenEmbedding(nn.Module):
    def __init__(self, vocab_size, d_model):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
    
    def forward(self, token_ids):
        # token_ids: (B, T) ints
        return self.embedding(token_ids)  # (B, T, d_model)
```

That's it. The "embedding layer" is one of the simplest neural network components.

## Embedding Size Considerations

For Llama 3 8B: vocab = 128k, $d = 4096$ → embedding matrix is $128k \times 4096 = 524M$ params. With fp16, that's ~1 GB of weights — about 14% of the model.

Design tradeoffs:
- **Bigger vocab**: shorter sequences (fewer tokens per sentence), better multilingual coverage, but bigger embedding matrix.
- **Smaller vocab**: longer sequences, smaller embeddings, but worse multilingual coverage and worse rare-word handling.

Modern LLMs have converged on 32k–128k vocab as the sweet spot.

## Tied vs Untied Embeddings

The output layer (un-embedding) is also a $\mathbb{R}^{d \times |V|}$ matrix. Should input and output share weights?

### Tied (shared) embeddings
$\mathbf{E}_{\text{out}} = \mathbf{E}_{\text{in}}^T$

- Saves $|V| \cdot d$ parameters (significant — can be 10–30% of model).
- Theoretically motivated: similar tokens should have similar input and output representations.
- Used by: GPT-2, early Llama, many small models.

### Untied embeddings
- Separate input and output matrices.
- More parameters but slightly better quality (some studies).
- Used by: Llama 2/3, Mistral, many modern models.

The trend has been toward **untied** — the extra parameters are worth the quality gain, and modern models can afford them.

## Positional Embeddings (Already Covered)

Positional information can be added via:
- **Additive**: $\mathbf{x} = \mathbf{E}_{\text{token}}[i] + \mathbf{E}_{\text{pos}}[i]$ (learned or sinusoidal). See [[06 - Attention Mechanisms/Positional Information/07 - Sinusoidal and Learned Positional|Sinusoidal and Learned]].
- **Rotary (RoPE)**: applied to Q and K, not to embeddings. See [[06 - Attention Mechanisms/Positional Information/08 - RoPE|RoPE]].

Modern LLMs (Llama, Mistral) use RoPE — there's no positional embedding in the input layer.

## Embedding Scaling

Some models scale the token embeddings by $\sqrt{d_{model}}$:

$$
\mathbf{x} = \sqrt{d_{model}} \cdot \mathbf{E}_{\text{token}}[i] + \mathbf{E}_{\text{pos}}[i]
$$

This compensates for the relatively small magnitude of learned embeddings compared to positional encodings. Used in the original Transformer; less common in modern LLMs.

## Quantization Challenges

Embedding matrices are tricky to quantize:
- **Low-frequency tokens** have few training examples → their embeddings are noisy. Quantization noise compounds this.
- **INT4 embedding quantization** typically loses more quality than INT4 weight quantization on other layers.
- Many INT4 inference setups keep embeddings in FP16.

## Worked Example (Forward)

```python
# Batching
token_ids = torch.tensor([[1, 2, 3], [4, 5, 0]])  # batch of 2, seq_len 3, 0 is padding
embeddings = embedding_layer(token_ids)
# Shape: (2, 3, d_model)

# Add positional encoding (if not using RoPE)
x = embeddings + positional_encoding[:3]
```

## Why This Matters for AI

- Embedding layers are the **interface between discrete tokens and continuous vectors**. Every model has one.
- Embedding size is a major architectural decision affecting parameter count, multilingual ability, and sequence length economics.
- For **fine-tuning**, the embedding layer often needs resizing (when you add special tokens). Forgetting this causes index-out-of-bounds.
- For **RAG / retrieval**, embedding models (BGE, E5) are essentially embedding layers trained with contrastive loss — conceptually similar but for sentences/documents, not tokens.

## Production Implications

- **Vocabulary is frozen** after pretraining. You can't add tokens without retraining (or at least fine-tuning the embedding layer).
- **Adding special tokens** for fine-tuning: call `model.resize_token_embeddings(len(tokenizer))` after adding tokens. New rows are randomly initialized — fine-tune to learn them.
- **For multi-tenant serving**, embeddings are shared across all requests — no per-tenant customization without fine-tuning.
- **For multilingual**: check the tokenizer's coverage of your target language. A 32k English-focused tokenizer may use 3x more tokens for Chinese text — affects cost and context.

## Common Pitfalls

- **Forgetting to resize embeddings when adding tokens** — index-out-of-bounds crash or garbage output.
- **Random-init new tokens without fine-tuning** — the new tokens produce garbage. Always fine-tune.
- **Mixing tied/untied when loading a model** — mismatched state dict errors. Match the model's original design.
- **Treating embedding lookup as a matmul** — semantically equivalent but 100x slower. Use `nn.Embedding` (gather), not `onehot @ E`.
- **Padding token's embedding** — should be zeros or otherwise not affect downstream computation. Mask properly.

## Further Reading

- Vaswani et al. (2017), *Attention Is All You Need* — original embedding + sinusoidal.
- Press & Wolf (2017), *Using the Output Embedding to Improve Language Models* (tied embeddings).
- Chung et al. (2020), *Extending Multilingual BERT to Low-Resource Languages* (vocabulary considerations).

## See Also

- [[01 - Transformer Block]]
- [[05 - Feed-Forward Network Deep]]
- [[06 - Attention Mechanisms/Positional Information/06 - Positional Encoding Overview|Positional Encoding Overview]]
- [[05 - NLP Fundamentals/Tokenization/01 - Tokenization Overview|Tokenization Overview]]
- [[05 - NLP Fundamentals/Embeddings/05 - Word2Vec GloVe FastText|Word2Vec GloVe FastText]]
- [[07 - Transformers/MOC|Transformers MOC]]
