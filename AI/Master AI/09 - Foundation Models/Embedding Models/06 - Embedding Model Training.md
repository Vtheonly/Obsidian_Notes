---
tags: [foundation-models, embeddings, training, contrastive, recipe]
iteration: 6
created: 2026-08-08
aliases: [Embedding Model Training, Contrastive Training, Embedding Training]
---

# 06 — Embedding Model Training

> [!info] TL;DR
> Embedding models (BGE, E5, GTE, OpenAI's `text-embedding-3-*`) are trained to map semantically similar inputs to nearby vectors in a high-dimensional space. The dominant training recipe is **contrastive learning**: positive pairs (query + relevant document) are pulled together; negative pairs (query + irrelevant document) are pushed apart. Modern recipes use **in-batch negatives** (other queries' positives become this query's negatives), **hard negative mining** (explicitly retrieved negatives that are similar but not relevant), and **multi-stage training** (pretrain on weak labels, then fine-tune on labeled data). Embedding model training is conceptually simpler than LLM training but has subtle failure modes — bad negatives can collapse the embedding space.

## Why Embedding Models Matter

Embedding models are the backbone of:

- **RAG**: retrieve relevant documents for a query.
- **Semantic search**: find similar items in a database.
- **Clustering**: group similar items.
- **Classification**: train a classifier on top of embeddings.
- **Recommendation**: find items similar to a user's history.

Without good embeddings, RAG retrieval fails — you retrieve irrelevant documents, and the LLM generates answers based on noise. Embedding quality is the #1 determinant of RAG performance.

## The Core Idea: Contrastive Learning

Given a query $q$ and a set of candidate documents $\{d_1, ..., d_N\}$ where $d_+$ is the relevant document, contrastive learning trains the model to assign high similarity to $(q, d_+)$ and low similarity to $(q, d_i)$ for $i \neq +$.

The standard loss is **InfoNCE** (Info Noise-Contrastive Estimation):

$$\mathcal{L} = -\log \frac{\exp(\text{sim}(q, d_+) / \tau)}{\sum_{i=1}^{N} \exp(\text{sim}(q, d_i) / \tau)}$$

where $\text{sim}$ is cosine similarity and $\tau$ is a temperature parameter.

This is just softmax cross-entropy where the "classes" are the candidate documents. The model learns to assign probability mass to the positive document and zero to negatives.

## The Training Pipeline

### Stage 1: Pretraining on Weak Supervision

The first stage uses large-scale weak supervision: pairs of (query, document) where the pairing comes from a heuristic, not human labels. Sources:

- **Web page titles + body**: the title is the query; the body is the document.
- **Reddit post titles + top comments**: titles are queries; comments are documents.
- **Wikipedia article titles + first paragraph**.
- **QA sites (StackOverflow, Quora)**: the question is the query; the answer is the document.
- **Scientific paper titles + abstracts**.

Datasets like MS-MARCO, Natural Questions, and proprietary web crawls provide millions of weak pairs. The model learns basic semantic matching from this data.

This stage uses a **dual-encoder** architecture: separate encoders (or a shared encoder) for queries and documents. Each input is encoded independently; similarity is computed at the end.

### Stage 2: Fine-Tuning on Labeled Data

The second stage uses high-quality labeled data: human-annotated (query, relevant document) pairs, plus hard negatives. Sources:

- **MS-MARCO** (human-annotated query-document pairs from Bing).
- **Natural Questions** (real Google queries + Wikipedia passages).
- **HotpotQA** (multi-hop reasoning queries).
- **Proprietary click data** (search result clicks as relevance signals).

The key innovation at this stage is **hard negative mining**: explicitly find documents that are similar to the query but not relevant, and include them as negatives. This forces the model to learn fine distinctions.

### Stage 3: (Optional) Distillation

Some models (Cohere Embed v3, OpenAI text-embedding-3-large) use a stronger model (e.g., a cross-encoder reranker or a large LLM) to score (query, document) pairs. The embedding model is trained to match the stronger model's scores. This transfers the reranker's precision to the embedding model's efficiency.

## Key Training Techniques

### In-Batch Negatives

For a batch of $B$ (query, positive) pairs, the negatives for query $i$ are the positives of all other queries in the batch. This gives $B-1$ negatives per query "for free" — no extra forward passes needed.

With batch size 1024, each query has 1023 negatives. This is much more efficient than computing dedicated negatives.

The downside: in-batch negatives are random. They may be too easy (clearly irrelevant) or too hard (actually relevant). Dedicated hard negatives (below) address this.

### Hard Negative Mining

Hard negatives are documents that are similar to the query (high lexical or embedding similarity) but not relevant. They force the model to learn fine distinctions.

Mining procedure:

1. For each query, retrieve top-K documents using BM25 or the current embedding model.
2. Filter out the known positives.
3. Manually label or use a reranker to identify which retrieved documents are NOT relevant.
4. Use these as hard negatives in training.

Hard negatives should be "hard but not too hard" — if they're actually relevant (false negatives in the labeling), training will be unstable. If they're too easy, they don't help.

Typical configuration: 1 positive + 7 hard negatives + ~1000 in-batch negatives per query.

### Asymmetric vs Symmetric Embeddings

- **Symmetric**: query and document use the same encoder and live in the same space. Used for clustering, similarity search. Example: sentence-transformers.
- **Asymmetric**: query and document use separate encoders (or separate prefixes). Used for search, where queries are short and documents are long. Example: BGE, E5, GTE.

Most modern embedding models support both modes via prefix tokens (`query: ...` vs `passage: ...`). The model learns different behavior for each prefix.

### Matryoshka Embeddings

A recent innovation (OpenAI text-embedding-3, Nomic Embed): the embedding is trained so that prefixes of it are also valid embeddings. A 1536-dimensional embedding can be truncated to 256 or 64 dimensions with graceful degradation.

This is achieved by training with multiple losses, each operating on a different prefix length. The result: you can trade off embedding size vs. quality at inference time, choosing smaller embeddings for lower-latency retrieval.

### Pooling Strategies

After the encoder produces per-token embeddings, they must be pooled into a single vector:

- **CLS pooling**: use the first token's embedding (BERT-style).
- **Mean pooling**: average all token embeddings. Most common for sentence embeddings.
- **Last-token pooling**: use the last token's embedding (good for causal LMs).
- **Attention pooling**: learn a weighted average. Best quality but most parameters.

Mean pooling is the production default — simple, effective, and works with any encoder.

## Architecture Choices

### Encoder

Most embedding models use a BERT-style encoder (110M-350M parameters). Larger encoders (1B+) give better embeddings but are slower. Modern models (BGE-large, E5-mistral) use LLM-scale encoders (3B-7B) for state-of-the-art quality.

The choice depends on the latency budget. For real-time retrieval (sub-100ms), use a small encoder. For batch indexing (offline), use a large encoder.

### Sequence Length

The encoder must handle the document length. For short documents (sentences, paragraphs), 512 tokens is enough. For long documents (full pages, chapters), use a long-context encoder (4K-8K tokens).

Late-interaction models like ColBERT handle long documents differently — they keep per-token embeddings and compute MaxSim at retrieval time. This is more accurate but more expensive.

### Dimensionality

Most embedding models produce 768-1536 dimensional vectors. Higher dimensions capture more information but cost more storage and compute. Matryoshka embeddings let you choose at inference time.

## Common Failure Modes

### Embedding Collapse

If all negatives are too easy, the model learns to map everything to the same point (the trivial solution to "make positives similar and negatives different"). Symptoms: all embeddings have high cosine similarity; retrieval returns near-random results.

Fix: add hard negatives. The model is forced to spread embeddings to distinguish them.

### False Negatives

If your "negatives" are actually relevant (because your labeling missed them), the model gets conflicting signal: "this similar thing is relevant, but also this similar thing is not relevant." Symptoms: training loss plateaus; embeddings cluster oddly.

Fix: use a reranker to verify negatives are truly irrelevant before training. Filter out borderline cases.

### Domain Mismatch

A model trained on web data (titles + bodies) may perform poorly on domain-specific queries (medical, legal, technical). Symptoms: good performance on general benchmarks, poor performance on your domain.

Fix: include domain-specific data in stage 2 fine-tuning. Even a few thousand domain-specific (query, positive, hard negatives) triples significantly improve domain performance.

### Catastrophic Forgetting

If stage 2 fine-tuning uses only narrow domain data, the model forgets general knowledge. Symptoms: improved domain performance, degraded general performance.

Fix: mix general and domain data in stage 2. Use replay (include stage 1 data in stage 2 batches).

## Production Considerations

### Choosing an Embedding Model

For most use cases in 2026:

- **General-purpose English**: `BAAI/bge-large-en-v1.5` or `intfloat/e5-large-v2` (open) or `text-embedding-3-large` (OpenAI).
- **Multilingual**: `BAAI/bge-m3` or `intfloat/multilingual-e5-large`.
- **Code**: `intfloat/e5-code` or specialized code embedding models.
- **Long documents**: `nomic-ai/nomic-embed-text-v1` (8K context) or late-interaction models like ColBERT.
- **Domain-specific (medical, legal)**: fine-tune a general model on domain data.

### Indexing and Serving

Embeddings are typically indexed in a vector database (pgvector, Qdrant, Milvus, Weaviate). See [[04 - Vector Memory Backends]] for the database side.

For serving:

- Batch encoding (for initial indexing): use vLLM or TGI with the embedding model.
- Real-time encoding (for queries): use a small dedicated model server. Latency matters; queries must return in <100ms.
- Cache embeddings aggressively. Document embeddings don't change; query embeddings can be cached for repeated queries.

### Re-Embedding Strategy

When you upgrade your embedding model, you must re-embed all documents (embeddings from different models are incompatible). This is expensive for large corpora. Plan for it:

- Version your embeddings (store the model name + version with each embedding).
- Have a re-embedding pipeline ready.
- Consider backward-compatible upgrades (Matryoshka embeddings let you truncate to a smaller size without re-embedding).

## Evaluation

Embedding models are evaluated on retrieval benchmarks:

- **MTEB** (Massive Text Embedding Benchmark): 56 tasks across 9 categories (retrieval, classification, clustering, etc.). The standard benchmark for embedding models.
- **BEIR**: a zero-shot retrieval benchmark (no fine-tuning on the target task).
- **MS-MARCO retrieval**: the standard IR benchmark.
- **Custom domain eval**: build a small (100-1000 query, positive, negatives) eval set for your domain. This is the most reliable signal for production fitness.

For production, the most important evaluation is **retrieval recall@K on your own data**: of the top-K retrieved documents, what fraction contains the gold answer? Optimize this metric, not MTEB scores.

## See Also

- [[02 - Embedding Models for Retrieval]] — overview of embedding models
- [[01 - RAG Pipeline Overview]] — where embeddings fit
- [[02 - Chunking Hybrid Search Reranking]] — how embeddings are used in retrieval
- [[04 - Vector Memory Backends]] — where embeddings are stored
- [[01 - Vision Foundation Models]] — sister domain (vision encoders also produce embeddings)
- [[05 - Multimodal Foundation Models]] — multimodal embeddings (CLIP)
- [[09 - Foundation Models/MOC|09 Foundation Models MOC]]
