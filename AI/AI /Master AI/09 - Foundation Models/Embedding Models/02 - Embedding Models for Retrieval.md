---
tags: [foundation-models, embedding-models, bge, e5, gte, contrastive]
iteration: 13
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Embedding Models for Retrieval, BGE, E5, GTE]
---

# 02 - Embedding Models (BGE, E5, GTE, SigLIP-2)

> [!info] TL;DR
> Modern embedding models (BGE, E5, GTE, OpenAI text-embedding-3, SigLIP-2) are BERT-family encoders (or decoder-based for the larger variants) fine-tuned with contrastive loss to produce sentence/document embeddings for retrieval. The backbone of every RAG system. Iteration 13 expanded this note to cover the 2024–2026 landscape: BGE-M3 (multilingual + multi-granularity), SigLIP-2 (image-text), and the late-interaction (ColBERT/ColPali) alternative to single-vector embeddings.

## What Makes a "Retrieval Embedding Model"?

A standard BERT model produces contextual token embeddings, but no single "sentence embedding." To get a sentence embedding, you can:
- Pool token embeddings (mean, max, or `[CLS]`).
- Fine-tune with a contrastive objective that pushes similar sentences together and dissimilar ones apart in embedding space.

Modern retrieval embedding models use the second approach — contrastive fine-tuning on millions of (query, relevant_doc, irrelevant_doc) triplets. The contrastive loss (InfoNCE for CLIP-style, sigmoid for SigLIP-style) trains the model to score the correct (query, doc) pair higher than incorrect pairs. This produces embeddings where semantic similarity = cosine similarity.

The key property: embeddings live in a vector space where **semantic similarity = geometric proximity**. This allows vector search: given a query, find the documents whose embeddings are closest. Without contrastive training, BERT embeddings don't have this property — semantically similar sentences can be far apart in embedding space.

## The Major Embedding Models

### BGE (BAAI General Embedding, 2022–2024)
- Open-source, BERT-family.
- Variants: BGE-small (33M), BGE-base (110M), BGE-large (335M), BGE-M3 (multilingual + multi-granularity).
- Strong performance on retrieval benchmarks (MTEB).
- Used by: most open-source RAG systems.
- BGE-M3 (2024) is the flagship: supports 100+ languages, dense + sparse + multi-vector retrieval, up to 8K context.

### E5 (Microsoft, 2022–2024)
- BERT-family, contrastive training on web text + labeled data.
- Variants: E5-base, E5-large, multilingual-E5, E5-Mistral (decoder-based, 7B parameters).
- Strong on multilingual retrieval.
- E5-Mistral uses a Mistral-7B backbone — much larger than BERT-family but better quality on long documents.

### GTE (Alibaba, 2023–2024)
- BERT-family, trained on large-scale weakly-supervised data.
- Variants: GTE-base, GTE-large, multilingual GTE, GTE-Qwen2 (decoder-based).
- Competitive with BGE and E5.
- GTE-Qwen2 uses a Qwen-2 backbone — the decoder-based approach gives state-of-the-art retrieval quality at high cost.

### OpenAI text-embedding-3 (2024)
- Closed-source, accessible via API.
- text-embedding-3-small (1536 dim) and text-embedding-3-large (3072 dim).
- Strong on MTEB; supports shortening (reduce dim with minimal quality loss).
- Shortening: project the 3072-dim embedding to 256/512/1024 dim via Matryoshka representation learning. Trade-off: lower dim = faster search but lower quality.

### Cohere Embed v3
- Commercial, strong on multilingual.
- Supports int8/binary quantization for fast search.
- Embed v3 introduced input_type parameter ("search_document", "search_query", "classification", "clustering") — model produces different embeddings for different use cases.

### Voyage AI
- Commercial, optimized for retrieval.
- Often SOTA on MTEB.
- voyage-3 (1024 dim), voyage-3-large (3072 dim), voyage-multilingual-2.

### SigLIP-2 (Google, 2025)
- **Multimodal**: produces embeddings for both images and text in a shared space.
- Used for image-text retrieval (find images matching a text query, or vice versa).
- Replaces CLIP for 2026 multimodal RAG systems.
- See [[26 - Papers/Multimodal/55 - SigLIP-2 2025]].

### Late-Interaction Models (ColBERT, ColPali)
- **Different paradigm**: instead of one embedding per document, produce one embedding per token (ColBERT) or per image patch (ColPali).
- Retrieval: max-sim over token/patch embeddings (late interaction).
- Higher quality than single-vector embeddings, but more expensive (multiple vectors per doc).
- See [[26 - Papers/Multimodal/48 - ColPali 2024]] for the vision variant.

## Evaluation: MTEB

**MTEB (Massive Text Embedding Benchmark)** is the standard eval. Covers:
- Retrieval (BEIR, MS MARCO).
- Classification.
- Clustering.
- STS (semantic textual similarity).
- Reranking.
- Summarization.

Check the MTEB leaderboard (https://huggingface.co/spaces/mteb/leaderboard) for current SOTA. As of 2026, the leaderboard is dominated by:
- **Top open-source**: BGE-M3, GTE-Qwen2, E5-Mistral.
- **Top commercial**: Voyage-3, OpenAI text-embedding-3-large, Cohere Embed v3.

Different models win different subtasks. For pure retrieval, GTE-Qwen2 and Voyage-3 are SOTA. For multilingual, BGE-M3. For image-text, SigLIP-2. Always check the specific subtask relevant to your use case, not the aggregate score.

## Worked Example (BGE)

```python
from FlagEmbedding import FlagModel

model = FlagModel('BAAI/bge-large-en-v1.5', 
                  query_instruction_for_retrieval="Represent this sentence for searching relevant passages: ")

docs = ["The cat sat on the mat.", "Paris is the capital of France.", "Dogs love to play fetch."]
query = "Where is Paris?"

doc_embeddings = model.encode(docs)
query_embedding = model.encode_queries([query])

scores = query_embedding @ doc_embeddings.T
# Should rank "Paris is the capital of France" highest.
```

## Worked Example (BGE-M3 — multilingual + multi-granularity)

```python
from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)

docs = [
    "Paris is the capital of France.",  # English
    "巴黎是法国的首都。",  # Chinese
    "Tokyo is the capital of Japan.",  # English
]
query = "What is the capital of France?"  # English query

# BGE-M3 produces dense, sparse, and multi-vector embeddings simultaneously
output = model.encode(docs, return_dense=True, return_sparse=True, return_colbert_vecs=True)
query_output = model.encode_queries([query], return_dense=True, return_sparse=True, return_colbert_vecs=True)

# Compute scores three ways
dense_scores = model.compute_dense_score(query_output, output)
sparse_scores = model.compute_sparse_score(query_output, output)
colbert_scores = model.compute_colbert_score(query_output, output)

print("Dense scores:", dense_scores)  # for fast retrieval
print("Sparse scores:", sparse_scores)  # like BM25, good for keyword matches
print("ColBERT scores:", colbert_scores)  # late-interaction, highest quality

# Production: often combine all three (hybrid fusion)
```

## Choosing an Embedding Model

| Consideration             | Recommendation                              |
|---------------------------|---------------------------------------------|
| Open source / self-hosted | BGE, E5, GTE                                |
| Best quality (text)        | Check MTEB leaderboard; Voyage-3, GTE-Qwen2 |
| Multilingual              | BGE-M3, multilingual-E5, Cohere Embed       |
| Low cost / fast           | BGE-small, E5-small                         |
| Long context              | BGE-M3 (up to 8k tokens), Jina embeddings   |
| API / managed             | OpenAI, Cohere, Voyage                      |
| Image-text                | SigLIP-2 (replaces CLIP for 2026)           |
| Document retrieval        | ColPali (vision-native, no OCR)             |
| Highest retrieval quality | ColBERT v2, ColPali (late interaction)      |

## Production Implications

- **Start with BGE-large-en-v1.5** for English retrieval — strong, open-source, well-supported.
- **For multilingual**, use BGE-M3 or multilingual-E5.
- **For multimodal** (image + text), use SigLIP-2 — the 2026 default. CLIP is legacy.
- **For documents** (PDFs, screenshots), consider ColPali — eliminates OCR entirely.
- **Embedding dimension** matters: larger = more expressive but slower search. 768–1024 is the sweet spot for single-vector; multi-vector (ColBERT) is higher quality but slower.
- **Quantize embeddings** to int8 for 4x memory reduction with minimal quality loss. Most vector DBs support this.
- **Cache embeddings** — re-embedding the same document is wasteful. Hash and cache.
- **Re-embed when you change models** — embeddings are model-specific; can't mix.
- **Query prefix matters** — many models (BGE, E5) require different prefixes for queries vs documents. Match the model's convention.
- **Matryoshka embeddings** (OpenAI text-embedding-3, Voyage-3) support dimension shortening. Use this to trade off quality vs latency.

## Common Pitfalls

- **Using a non-retrieval embedding model** — base BERT embeddings are much worse than fine-tuned BGE/E5.
- **Forgetting the query prefix** — many models (BGE, E5) require different prefixes for queries vs documents. Match the model's convention.
- **Wrong max sequence length** — BGE is 512; longer documents need chunking. BGE-M3 supports 8K but is slower.
- **Mixing embedding models** — different models produce different spaces; similarities across are meaningless.
- **Not normalizing** — some models output normalized vectors, others don't. Match the search metric (cosine vs L2).
- **Using CLIP for 2026 multimodal RAG** — SigLIP-2 is the modern default; CLIP is legacy.
- **OCR + text embedding for documents** — ColPali (vision-native) is often better and skips OCR.
- **Treating embedding dimension as the only quality metric** — a 1024-dim BGE-M3 may beat a 3072-dim OpenAI embedding on specific tasks. Always check MTEB for your use case.

## Modern Developments (2024–2026)

### Decoder-Based Embedding Models
2024 saw the emergence of decoder-based embedding models (E5-Mistral, GTE-Qwen2). These use a Mistral-7B or Qwen-2-7B backbone with the last hidden state as the embedding. Much larger than BERT-family (7B vs 110M), but better quality on long documents and complex queries. Trade-off: 10× slower and 10× more memory.

### BGE-M3: Multi-Vector + Multi-Lingual
BGE-M3 (2024) produces dense, sparse (BM25-like), and multi-vector (ColBERT-style) embeddings simultaneously. This enables hybrid retrieval (combine dense + sparse) without separate models. Supports 100+ languages and up to 8K context.

### Matryoshka Representation Learning
OpenAI text-embedding-3 and Voyage-3 use Matryoshka embeddings — train at multiple dimensions simultaneously (3072, 1024, 256). At inference, you can truncate to any dimension with minimal quality loss. Trade-off: lower dim = faster search but lower quality. Allows runtime trade-off without retraining.

### SigLIP-2: Multilingual Image-Text
SigLIP-2 (Google, 2025) is the default 2026 vision encoder for VLMs. It produces embeddings for both images and text in a shared space. Used for image-text retrieval, multimodal RAG, and as the vision encoder in PaliGemma 2, InternVL 2.5, LLaVA-NeXT. See [[26 - Papers/Multimodal/55 - SigLIP-2 2025]].

### ColPali: Vision-Native Document Retrieval
ColPali (2024) eliminates OCR entirely — embeds document pages as images and retrieves via late interaction over patches. Faster than OCR + text retrieval, and handles visual content (charts, tables, diagrams) better. See [[26 - Papers/Multimodal/48 - ColPali 2024]].

### Instruction-Tuned Embeddings
Models like E5-Mistral accept instructions ("find a passage that answers this question" vs "find a passage with similar topic"). The instruction shapes the embedding space, improving task-specific retrieval. The future of embedding models is instruction-aware.

## Common Failure Modes — Diagnostic Table

| Symptom                                  | Likely Cause                                        | Fix                                                              |
|------------------------------------------|------------------------------------------------------|------------------------------------------------------------------|
| Low retrieval recall                     | Wrong model; or no query prefix                      | Use BGE-M3; ensure query prefix matches model convention         |
| Multilingual queries return wrong docs   | Model not multilingual                               | Switch to BGE-M3 or multilingual-E5                              |
| Long documents truncated                | Max sequence length too short                         | Use BGE-M3 (8K); or chunk long documents                          |
| Search latency too high                  | Embedding dim too large; or no quantization           | Matryoshka-shorten to 1024 dim; or quantize to int8               |
| Image-text retrieval fails              | Using text-only model for images                      | Switch to SigLIP-2 for image-text                                |
| Document retrieval quality low          | OCR errors corrupting text                            | Use ColPali (vision-native, no OCR)                              |
| Embeddings take too much memory          | Storing full precision (FP32) embeddings              | Quantize to int8; or use Matryoshka-shortened embeddings         |
| Different model embeddings mixed         | Migration bug                                         | Re-embed all documents with the new model; never mix            |
| Cosine similarity doesn't match expectation | Embeddings not normalized                          | Normalize before cosine; or use L2 distance                      |

## Interview Questions

1. **Q: Why are contrastive-trained embeddings better for retrieval than base BERT embeddings?**
   A: Base BERT is trained on masked language modeling — it learns contextual token representations but no single sentence embedding. Mean-pooling BERT's token embeddings gives a sentence embedding, but the embedding space isn't optimized for semantic similarity (similar sentences can be far apart). Contrastive training (InfoNCE for CLIP, sigmoid for SigLIP) explicitly shapes the embedding space: similar (query, doc) pairs are pulled together, dissimilar pairs pushed apart. The result: cosine similarity = semantic similarity. Without contrastive training, the embedding space is "random" w.r.t. semantic similarity.

2. **Q: When would you use ColBERT/ColPali (late interaction) over BGE (single vector)?**
   A: When retrieval quality matters more than latency/memory. Late-interaction models produce one vector per token (ColBERT) or per patch (ColPali); retrieval scores the query against each token/patch and takes the max (max-sim). This is higher quality because it preserves token-level matching (vs single-vector which collapses all tokens into one vector). Trade-off: storage is N× larger (one vector per token vs one per doc) and search is slower (N dot products per doc vs one). Use single-vector (BGE) for high-volume retrieval; late-interaction (ColBERT/ColPali) when quality is critical and volume is moderate.

3. **Q: How does BGE-M3's multi-vector output work?**
   A: BGE-M3 produces three outputs simultaneously: (1) **dense embeddings** (single 1024-dim vector per doc — standard retrieval), (2) **sparse embeddings** (BM25-like token weights — keyword matching), (3) **ColBERT-style multi-vector** (one vector per token — late interaction). At retrieval, compute all three scores and combine via weighted fusion. This gives the best of dense (semantic), sparse (keyword), and late-interaction (high quality) retrieval without needing three separate models. Production: BGE-M3 is the default for 2026 multilingual RAG.

## Connection to Other Concepts

- [[05 - NLP Fundamentals/Embeddings/06 - Contextual Embeddings ELMo to BERT|Contextual Embeddings]] — pre-BERT history.
- [[05 - NLP Fundamentals/Embeddings/05 - Word2Vec GloVe FastText|Word2Vec / GloVe / FastText]] — static embeddings.
- [[17 - RAG/MOC|RAG MOC]] — parent context.
- [[17 - RAG/Ingestion and Retrieval/02 - Chunking Hybrid Search Reranking|Chunking, Hybrid Search, Reranking]] — production RAG.
- [[20 - AI Infrastructure/Storage/02 - Vector Storage with pgvector|Vector Databases]] — storage layer.
- [[09 - Foundation Models/Embedding Models/06 - Embedding Model Training|Embedding Model Training]] — how to train.
- [[26 - Papers/Multimodal/55 - SigLIP-2 2025]] — multimodal embeddings.
- [[26 - Papers/Multimodal/48 - ColPali 2024]] — vision-native document retrieval.
- [[09 - Foundation Models/MOC|Foundation Models MOC]] — parent chapter.

## Further Reading

- MTEB leaderboard: https://huggingface.co/spaces/mteb/leaderboard
- BGE paper: Xiao et al. (2023), *C-Pack: Packaged Resources To Advance General Chinese Embedding*.
- E5 paper: Wang et al. (2022), *Text Embeddings by Weakly-Supervised Contrastive Pre-training*.
- BGE-M3 paper: Chen et al. (2024), *M3-Embedding: Multi-Lingual, Multi-Functionality, Multi-Granularity Text Embeddings*.
- SigLIP-2 paper: Tschannen et al. (2025). See [[26 - Papers/Multimodal/55 - SigLIP-2 2025]].
- ColPali paper: Faysse et al. (2024). See [[26 - Papers/Multimodal/48 - ColPali 2024]].

## See Also

- [[05 - NLP Fundamentals/Embeddings/06 - Contextual Embeddings ELMo to BERT|Contextual Embeddings]]
- [[17 - RAG/MOC|RAG MOC]]
- [[09 - Foundation Models/MOC|Foundation Models MOC]]
- [[20 - AI Infrastructure/Storage/02 - Vector Storage with pgvector|Vector Databases]]
