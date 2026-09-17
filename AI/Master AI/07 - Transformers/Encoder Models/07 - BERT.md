---
tags: [transformer, encoder, bert, mlm]
iteration: 2
created: 2026-08-07
aliases: [BERT]
---

# 07 - BERT

> [!info] TL;DR
> BERT (Devlin et al. 2018) is a bidirectional encoder-only Transformer pretrained with Masked Language Modeling. Kicked off the modern NLP era. Still widely used for classification, NER, embeddings, and as the backbone of modern embedding models (BGE, E5).

## Architecture

BERT is a Transformer **encoder**:
- Bidirectional attention (no causal mask).
- 12 layers (Base) or 24 layers (Large).
- Hidden dim 768 (Base) or 1024 (Large).
- 12 heads (Base) or 16 heads (Large).
- 110M (Base) or 340M (Large) parameters.

No decoder, no generation. BERT produces contextual embeddings, not text.

## Pretraining Objectives

### Masked Language Model (MLM)
Randomly mask 15% of tokens; predict them from the rest.

Of the 15% selected:
- 80% replaced with `[MASK]`.
- 10% replaced with a random token.
- 10% left unchanged.

The mix forces the model to learn contextual representations, not just memorize the `[MASK]` token. The 10% random + 10% unchanged prevent the model from learning that masked positions are always `[MASK]`.

### Next Sentence Prediction (NSP)
Given sentence pairs, predict whether they're adjacent in the original text. Uses a `[CLS]` token at the start.

**RoBERTa (Liu et al. 2019)** showed NSP doesn't help and removed it. Modern BERT-family models skip NSP.

## Input Format

```
[CLS] sentence A [SEP] sentence B [SEP]
```

- `[CLS]`: classification token; its final-layer representation is used for sequence classification.
- `[SEP]`: separates segments.
- Segment embeddings: separate learned embeddings for sentence A vs B.

## Fine-Tuning BERT

The pretrain-then-fine-tune paradigm:

1. **Pretrain** BERT once on a large corpus (Wikipedia + BookCorpus).
2. **Fine-tune** for downstream tasks with a small task-specific head:
   - Classification: `[CLS]` + linear head.
   - NER: per-token linear head.
   - Q&A: predict start and end positions.
   - Sentence pair: `[CLS]` + binary head.

Fine-tuning is fast (an hour on a single GPU) and gives SOTA on many tasks with very little labeled data.

## BERT Family

| Model      | Change vs BERT                                  |
|------------|-------------------------------------------------|
| RoBERTa    | More data, bigger batches, no NSP, dynamic MLM  |
| ALBERT     | Factorized embeddings, parameter sharing        |
| DeBERTa    | Disentangled attention, enhanced mask decoder   |
| ELECTRA    | Replaced token detection (more efficient)       |
| DistilBERT | Distilled (6 layers, 60% params, 95% quality)   |
| Sentence-BERT | Pooled sentence embeddings for semantic search |

## BERT as Embedding Backbone

Many modern embedding models are BERT-family models fine-tuned with contrastive loss:
- **BGE** (BAAI): BERT-like, fine-tuned for retrieval.
- **E5** (Microsoft): similar.
- **GTE** (Alibaba): similar.
- **sentence-transformers** (SBERT): the original.

These produce sentence/document embeddings for RAG, search, clustering. They're still BERT-family under the hood.

## Worked Example

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

inputs = tokenizer("This movie was great!", return_tensors="pt", truncation=True, max_length=512)
outputs = model(**inputs)
logits = outputs.logits  # (1, 2)
predicted_class = logits.argmax(-1)
```

For fine-tuning: standard supervised training, lr=2e-5, 3–5 epochs, batch size 16–32.

## Why This Matters for AI

- BERT was the model that **made Transformers dominant** in NLP. The pretrain-then-fine-tune paradigm originated here.
- BERT-family models are still **the right choice** for classification, NER, extraction, and embedding — cheaper and often more accurate than LLMs for these tasks.
- For RAG, BERT-family embedding models (BGE, E5) are the standard. Every RAG system uses one.
- Understanding BERT helps you read older NLP papers (2018–2021) and use embedding models correctly.

## Production Implications

- For **classification / NER / extraction** with limited data, fine-tune a BERT-family model. Faster, cheaper, often more accurate than an LLM.
- For **embeddings in RAG**, use a modern BERT-family embedder (BGE-large, E5-large, GTE-large). Don't use raw BERT embeddings — fine-tuned for retrieval is much better.
- **Max sequence length** is 512 (or 1024 for some variants). For longer documents, use sliding window or Longformer.
- **Quantization**: BERT quantizes well to INT8. Most serving frameworks support it out of the box.
- **DistilBERT** for low-latency / edge deployments: 60% smaller, 60% faster, 95% of quality.

## Common Pitfalls

- **Wrong tokenizer for the model** — `bert-base-uncased` requires lowercased input; `bert-base-cased` requires original case.
- **Forgetting `[CLS]` and `[SEP]`** — most HuggingFace tokenizers add these, but raw `encode` may not.
- **Using BERT for generation** — it can't generate; it's bidirectional.
- **Passing > 512 tokens** — silent truncation or error. Always truncate explicitly.
- **Comparing BERT embeddings across models** — different BERT variants have different embedding spaces. Don't mix.

## Further Reading

- Devlin et al. (2019), *BERT: Pre-training of Deep Bidirectional Transformers*.
- Liu et al. (2019), *RoBERTa: A Robustly Optimized BERT Pretraining Approach*.
- Reimers & Gurevych (2019), *Sentence-BERT*.

## See Also

- [[05 - NLP Fundamentals/Embeddings/06 - Contextual Embeddings ELMo to BERT|Contextual Embeddings]]
- [[09 - GPT Family Evolution]]
- [[12 - T5 and BART]]
- [[01 - Transformer Block]]
- [[07 - Transformers/MOC|Transformers MOC]]
