---
tags: [nlp, moc]
iteration: 2
created: 2026-08-07
---

# 05 — NLP Fundamentals MOC

> [!info] The pre-Transformer NLP background you need to understand what Transformers replaced and why. Read the notes in numbered order.

## Reading Order

| #   | Note                                              | Sub-domain        | Purpose                                            |
|-----|---------------------------------------------------|-------------------|----------------------------------------------------|
| 01  | [[01 - Tokenization Overview]]                    | Tokenization      | The bridge between text and model IDs.             |
| 02  | [[02 - BPE]]                                      | Tokenization      | The dominant subword algorithm.                    |
| 03  | [[03 - WordPiece]]                                | Tokenization      | BERT's tokenizer.                                  |
| 04  | [[04 - SentencePiece]]                            | Tokenization      | Multilingual / language-agnostic library.          |
| 05  | [[05 - Word2Vec GloVe FastText]]                  | Embeddings        | Static word embeddings.                            |
| 06  | [[06 - Contextual Embeddings ELMo to BERT]]       | Embeddings        | The shift to contextual embeddings.                |
| 07  | [[07 - N-gram Language Models]]                   | Language Modeling | Pre-neural LMs; baseline.                          |
| 08  | [[08 - Perplexity]]                               | Language Modeling | The intrinsic LM metric.                           |
| 09  | [[09 - TF-IDF]]                                   | Pre-Transformer   | Classical IR scoring.                              |
| 10  | [[10 - BM25]]                                     | Pre-Transformer   | **SOTA for keyword search; hybrid RAG component.** |

## Sub-Domains

- [[05 - NLP Fundamentals/Tokenization/01 - Tokenization Overview|Tokenization]] — notes 01–04
- [[05 - NLP Fundamentals/Embeddings/05 - Word2Vec GloVe FastText|Embeddings]] — notes 05–06
- [[05 - NLP Fundamentals/Language Modeling/07 - N-gram Language Models|Language Modeling]] — notes 07–08
- [[05 - NLP Fundamentals/Pre-Transformer NLP/09 - TF-IDF|Pre-Transformer NLP]] — notes 09–10
- [[04 - Neural Networks/Architectures/04 - RNN LSTM GRU|Sequence Models]] — covered in [[04 - Neural Networks/MOC|04 Neural Networks]]

## Why This Chapter Matters

Transformers operate on **tokens** and produce **embeddings**. To understand the input pipeline of any LLM, you need to understand tokenization. To understand why attention was invented, you need to understand the limitations of RNN-based Seq2Seq. To understand modern hybrid RAG, you need BM25.

## See Also

- [[04 - Neural Networks/MOC|04 Neural Networks]] — the underlying NN machinery
- [[06 - Attention Mechanisms/MOC|06 Attention Mechanisms]] — what replaced RNNs
- [[08 - LLMs/MOC|08 LLMs]] — modern LMs
- [[17 - RAG/MOC|17 RAG]] — BM25 still matters here
