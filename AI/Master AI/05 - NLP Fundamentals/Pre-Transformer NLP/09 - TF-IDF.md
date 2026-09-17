---
tags: [nlp, ir, tf-idf, vector-space-model, classical-ir]
iteration: 7
created: 2026-08-07
last_updated: 2026-08-08
aliases: [TF-IDF, Term Frequency Inverse Document Frequency, TFIDF]
---

# 09 - TF-IDF

> [!info] TL;DR
> TF-IDF (Term Frequency-Inverse Document Frequency) scores how important a word is to a document in a corpus. Common words get low scores; rare words get high scores. The foundation of classical information retrieval — and still the right baseline for keyword search. This note covers the formula, variants, why it works, use in IR, comparison to BM25 and embeddings, limitations, production patterns, and worked examples.

## The Formula

For term $t$ in document $d$ in corpus $D$:

$$
\text{tf-idf}(t, d, D) = \text{tf}(t, d) \cdot \text{idf}(t, D)
$$

The product of two factors: how often the term appears in this document (TF), and how rare the term is across the corpus (IDF).

### Term Frequency (TF)

How often $t$ appears in $d$. Several variants:

- **Raw count**: $\text{count}(t, d)$
- **Normalized**: $\text{count}(t, d) / |d|$ (term frequency divided by document length)
- **Log-scaled**: $1 + \log(\text{count}(t, d))$ (most common; dampens the effect of very frequent terms)
- **Augmented**: $0.5 + 0.5 \cdot \frac{\text{count}(t, d)}{\max_{t'} \text{count}(t', d)}$ (prevents bias toward longer documents)

The log-scaled variant is standard because it dampens the effect of terms that appear many times. A term appearing 100 times isn't 100× more important than one appearing once; it's about 7× more important ($1 + \log(100) \approx 5.6$).

### Inverse Document Frequency (IDF)

How rare $t$ is across the corpus:

$$
\text{idf}(t, D) = \log \frac{|D|}{|\{d \in D : t \in d\}|}
$$

- **Common words** ("the", "and"): appear in most documents → low IDF → low TF-IDF.
- **Rare words** ("quokka", "topotear"): appear in few documents → high IDF → high TF-IDF.
- **Constant smoothing**: $\text{idf}(t, D) = \log \frac{1 + |D|}{1 + |\{d : t \in d\}|} + 1$ (sklearn default) to avoid division by zero and overly harsh low IDF.

The smoothing prevents two issues:
1. **Division by zero**: if a term appears in no documents (shouldn't happen for query terms, but can for unknown terms).
2. **IDF = 0 for universal terms**: without the +1, terms appearing in all documents get IDF = 0, removing them entirely from scoring.

### Why Log?

The logarithm dampens the effect of extreme values. Without log:
- A term in 1 document out of 1M has IDF = 1,000,000.
- A term in 100 documents has IDF = 10,000.
- The rare term dominates retrieval, even if it's not very relevant.

With log:
- The rare term has IDF = $\log(1M) = 13.8$.
- The common term has IDF = $\log(10K) = 9.2$.
- The ratio is more reasonable (1.5×, not 100×).

## Why It Works

A word that appears in many documents isn't useful for distinguishing them. A word that appears in only a few documents is highly informative for those documents.

TF-IDF combines:
- **TF**: how central the term is to this document.
- **IDF**: how distinctive the term is across the corpus.

The product gives a score that's high for terms that are both frequent in this document and rare across the corpus — exactly the terms that best characterize this document.

### Intuition

Consider a document about "quokkas" (a small marsupial). The word "the" appears 50 times; the word "quokka" appears 10 times. Without IDF, "the" would score higher. But "the" appears in almost every document, so it has low IDF. "Quokka" appears in few documents, so it has high IDF. The product makes "quokka" the dominant term — which is correct.

## Use in Information Retrieval

To rank documents for a query $q$:

1. Compute the TF-IDF vector for $q$.
2. Compute TF-IDF vectors for all documents (precomputed).
3. Rank by cosine similarity to $q$.

This is **vector space model retrieval** — classical IR (Salton et al. 1975). Before BERT, this was how search engines worked.

### The Vector Space Model

Each document is represented as a vector in $\mathbb{R}^V$ where $V$ is the vocabulary size. Entry $i$ is the TF-IDF score of term $i$ in the document. Most entries are 0 (sparse vector).

Queries are also represented as TF-IDF vectors. Retrieval is cosine similarity between query and document vectors.

$$
\text{sim}(q, d) = \cos(\mathbf{q}, \mathbf{d}) = \frac{\mathbf{q} \cdot \mathbf{d}}{\|\mathbf{q}\| \|\mathbf{d}\|}
$$

Cosine similarity normalizes for document length — a long document with many terms doesn't get an unfair advantage.

### Why Cosine Similarity?

- **Length invariance**: a 1000-word document and a 100-word document with the same term proportions get the same similarity.
- **Range [-1, 1]**: bounded, easy to interpret (though TF-IDF vectors are non-negative, so range is [0, 1]).
- **Efficient**: can be computed via dot product if vectors are normalized.

### Inverted Index

For large corpora, computing cosine similarity against every document is too slow. The **inverted index** is the data structure that makes TF-IDF retrieval fast.

An inverted index maps each term to the list of documents containing it:

```
"quokka" → [doc_42, doc_178, doc_902]
"marsupial" → [doc_42, doc_55, doc_178, doc_902, ...]
```

For a query, we only need to look at documents containing at least one query term — much faster than scanning all documents. Elasticsearch, OpenSearch, and Lucene are built on inverted indexes.

## Worked Example

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

docs = [
    "the cat sat on the mat",
    "the dog ran in the park",
    "cats and dogs are common pets",
]
query = "cat on mat"

vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
doc_vectors = vectorizer.fit_transform(docs)
query_vector = vectorizer.transform([query])

sims = cosine_similarity(query_vector, doc_vectors).flatten()
print(sims)  # highest for docs[0]

# Inspect the vocabulary
print(vectorizer.vocabulary_)  # {'cat': ..., 'sat': ..., 'mat': ..., ...}

# Inspect the IDF values
print(vectorizer.idf_)  # [1.69, 1.69, 1.69, ...]
```

### Manual Computation

For the corpus above (3 documents):

Term "cat":
- TF in doc_0: $\log(1) + 1 = 1$ (appears once).
- TF in doc_2: $\log(1) + 1 = 1$ (appears once, as "cats" — but if we stem, it's the same).
- IDF: $\log(3/2) \approx 0.41$ (appears in 2 of 3 docs).
- TF-IDF in doc_0: $1 \times 0.41 = 0.41$.

Term "mat":
- TF in doc_0: 1.
- IDF: $\log(3/1) \approx 1.10$ (appears in 1 of 3 docs).
- TF-IDF in doc_0: $1 \times 1.10 = 1.10$.

So "mat" contributes more to doc_0's score than "cat" — because "mat" is rarer across the corpus.

## Comparison to BM25

BM25 (see [[10 - BM25]]) is the successor to TF-IDF, with two improvements:

1. **Term saturation**: TF-IDF's TF grows linearly (or log-linearly) with count. BM25's TF saturates — beyond a point, more occurrences don't help. This matches the intuition that a term appearing 100 times isn't 100× more relevant than one appearing once.

2. **Length normalization**: TF-IDF doesn't explicitly normalize for document length (only via cosine similarity). BM25 has a length normalization parameter that penalizes long documents.

BM25 formula:
$$
\text{BM25}(t, d, D) = \text{idf}(t, D) \cdot \frac{\text{tf}(t, d) \cdot (k_1 + 1)}{\text{tf}(t, d) + k_1 \cdot (1 - b + b \cdot |d| / \text{avgdl})}
$$

where $k_1$ (typically 1.2) controls saturation and $b$ (typically 0.75) controls length normalization.

**When to use which**:
- BM25 for production search (better quality).
- TF-IDF for teaching/understanding (simpler).
- Both are "classical IR" — neither has semantic understanding.

## Comparison to Embeddings

| Aspect | TF-IDF | Embeddings (BGE, E5, OpenAI) |
|--------|--------|------------------------------|
| Semantic understanding | None | Yes |
| Word order | Ignored | Captured (for contextual embeddings) |
| Vocabulary | Fixed at training | Subword/byte-level |
| Sparse vs. dense | Sparse (100K+ dim) | Dense (768-1536 dim) |
| Compute | Cheap (lookups) | Expensive (model forward pass) |
| Interpretable | Yes (which terms matched) | No (black box) |
| Best for | Keyword queries | Semantic queries |
| Hybrid | Combine with vector | Combine with BM25 |

### When TF-IDF/BM25 Beats Embeddings

- **Keyword queries**: "error code ERR_4093" — exact match matters; embeddings may miss it.
- **Rare terms**: "quokka" — embeddings may not have seen it; TF-IDF handles it naturally.
- **Code search**: variable names, function names — exact match is critical.
- **Legal/medical**: precise terminology where synonyms are dangerous.
- **Cheap baseline**: when you can't afford embedding model inference.

### When Embeddings Beat TF-IDF

- **Semantic queries**: "how do I configure auth?" — no exact keywords, but conceptual match.
- **Paraphrased queries**: "user login" vs. "user sign in" — embeddings capture the equivalence.
- **Cross-lingual**: query in English, documents in Chinese — multilingual embeddings handle this.
- **Conceptual search**: "things related to machine learning" — embeddings capture concepts.

### Hybrid Search

The best of both worlds: combine BM25 (keyword) and vector (semantic) search. Use **reciprocal rank fusion** (RRF) to merge:

$$
\text{RRF score}(d) = \sum_{r \in \text{rankings}} \frac{1}{k + \text{rank}_r(d)}
$$

where $k$ is typically 60.

Hybrid search is the production standard for RAG. See [[02 - Chunking Hybrid Search Reranking]].

## Limitations

- **No semantic understanding**: "cat" and "feline" are completely unrelated. A query for "feline" won't match documents about "cats".
- **No word order**: "dog bites man" and "man bites dog" are identical. The vector ignores syntax.
- **Sparse, high-dimensional**: vocabulary can be 100K+; vectors are sparse. Memory-intensive for large vocabularies.
- **No contextualization**: the same word has the same TF-IDF regardless of context. "Bank" (river) and "bank" (financial) are treated identically.
- **Vocabulary mismatch**: synonyms and related terms don't match. The model only knows exact terms.
- **Stemming/lemmatization required**: "running", "runs", "ran" are different terms without preprocessing.

These limitations are exactly what embedding-based retrieval (BGE, E5, OpenAI embeddings) addresses. But TF-IDF + BM25 are still widely used because:

- **Cheap**: no model to run, just lookups.
- **Interpretable**: you can see exactly which terms contributed.
- **Strong baseline**: for keyword-heavy queries, BM25 often beats vector search.
- **Hybrid**: combine with vector search for best of both worlds.

## Why This Matters for AI

- TF-IDF is the **ancestor of vector-based retrieval**. Understanding it makes the motivation for embeddings clear.
- For **hybrid RAG**, BM25 (TF-IDF-derived) is still essential. Pure vector search misses exact-match queries.
- The TF-IDF **vector** is a simple embedding — pre-Word2Vec, this was how documents were embedded.
- For **text classification** with limited data, TF-IDF + logistic regression is a strong baseline.
- Understanding TF-IDF is essential for understanding search engines (Elasticsearch, Lucene) and classical IR.

## Production Implications

- For **keyword search**, use BM25 ([[10 - BM25]]) — it's TF-IDF with better saturation and length normalization.
- For **hybrid search** (BM25 + vector), weight BM25 higher for keyword-heavy queries, vector higher for semantic queries.
- **TF-IDF + Logistic Regression** is a great baseline for text classification — beat it before reaching for deep learning.
- For **real-time search**, use an inverted index (Elasticsearch, OpenSearch) rather than computing TF-IDF on the fly.
- For **multi-lingual**, TF-IDF works per-language. Don't mix languages in one index.
- For **streaming data**, update IDF incrementally as new documents arrive.
- **Vocabulary size**: control via min_df (minimum document frequency) and max_df (maximum document frequency) to filter rare and common terms.
- **Stop words**: remove common words ("the", "and", "is") to focus on content terms.
- **Stemming/lemmatization**: apply to normalize word forms ("running" → "run").
- **N-grams**: include bigrams ("machine learning") to capture multi-word terms.

## Common Pitfalls

- **Forgetting to lowercase** — "The" and "the" become different tokens. Always lowercase.
- **Not removing stop words** — common words dominate without stop-word removal.
- **Using raw counts instead of log-scaled TF** — long documents get unfairly high scores.
- **Comparing TF-IDF across different corpora** — IDF depends on the corpus; values change.
- **Not stemming** — "running" and "runs" are different terms without stemming.
- **Vocabulary too large** — 1M terms means 1M-dimensional vectors. Use min_df/max_df to control.
- **Vocabulary too small** — filtering too aggressively loses important terms.
- **Forgetting to handle out-of-vocabulary terms** — query terms not in the vocabulary get zero score.
- **Not using an inverted index for large corpora** — naive cosine similarity is $O(N)$ per query; inverted index is $O(\log N)$.

## Worked Example: TF-IDF for Classification

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

# Load data
texts, labels = load_dataset()

# Build pipeline: TF-IDF + Logistic Regression
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        max_features=50000,
        ngram_range=(1, 2),  # unigrams + bigrams
        stop_words='english',
        sublinear_tf=True,  # log-scaled TF
    )),
    ('clf', LogisticRegression(C=1.0, max_iter=1000)),
])

# Train
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2)
pipeline.fit(X_train, y_train)

# Evaluate
accuracy = pipeline.score(X_test, y_test)
print(f"Accuracy: {accuracy:.3f}")

# Inspect top features per class
feature_names = pipeline.named_steps['tfidf'].get_feature_names_out()
coefs = pipeline.named_steps['clf'].coef_
for i, class_label in enumerate(pipeline.named_steps['clf'].classes_):
    top_features = sorted(zip(feature_names, coefs[i]), key=lambda x: x[1], reverse=True)[:10]
    print(f"\nTop features for class '{class_label}':")
    for name, coef in top_features:
        print(f"  {name}: {coef:.3f}")
```

This baseline often achieves 80-90% of deep learning performance at 1% of the compute. Beat it before reaching for BERT.

## Interview Questions

- **Q: What does TF-IDF measure?**  
  A: How important a term is to a document in a corpus. TF (term frequency) measures how often the term appears in this document; IDF (inverse document frequency) measures how rare the term is across the corpus. The product gives high scores to terms that are both frequent in this document and rare overall.

- **Q: Why use log for IDF?**  
  A: To dampen the effect of extreme values. Without log, a term in 1 document out of 1M would have IDF 1M, dominating retrieval. With log, the IDF is ~14, a more reasonable ratio to common terms.

- **Q: How does TF-IDF differ from BM25?**  
  A: BM25 adds term saturation (TF doesn't grow linearly forever) and length normalization (penalizes long documents). Both are classical IR; BM25 is the production standard.

- **Q: When would you use TF-IDF instead of embeddings?**  
  A: For keyword queries (exact match matters), rare terms (embeddings may not have seen them), code search (variable names), and as a cheap baseline. For hybrid RAG, combine BM25 (TF-IDF-derived) with vector search.

- **Q: What are the limitations of TF-IDF?**  
  A: No semantic understanding (synonyms don't match), no word order, sparse high-dimensional vectors, no contextualization (same word has same score regardless of context). Embeddings address these but at higher compute cost.

## Further Reading

- Salton et al. (1975), *A Vector Space Model for Automatic Indexing*.
- Manning, Raghavan, Schütze, *Introduction to Information Retrieval*, Chapter 6.
- Robertson & Zaragoza (2009), *The Probabilistic Relevance Framework: BM25 and Beyond*.
- sklearn TF-IDF docs: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html

## See Also

- [[10 - BM25]] — the production-standard successor
- [[07 - N-gram Language Models]] — pre-neural language modeling
- [[05 - Word2Vec GloVe FastText]] — neural embeddings (the successor)
- [[06 - Contextual Embeddings ELMo to BERT]] — contextual embeddings
- [[02 - Embedding Models for Retrieval]] — modern retrieval
- [[17 - RAG/MOC|RAG MOC]] — where retrieval matters
- [[02 - Chunking Hybrid Search Reranking]] — hybrid search with TF-IDF/BM25
- [[05 - NLP Fundamentals/MOC|NLP MOC]]
