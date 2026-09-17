---
tags: [nlp, tokenization, bpe, wordpiece, sentencepiece]
iteration: 11
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Tokenization Overview]
---

# Tokenization Overview

> [!info] TL;DR
> Tokenization is the bridge between raw text and the integer IDs a language model consumes. Modern LLMs use **subword tokenization** (BPE, WordPiece, Unigram, SentencePiece) — a sweet spot between character-level (too fine) and word-level (too sparse). This note gives the overview; deep dives live in [[BPE]], [[WordPiece]], [[SentencePiece]].

## Why Tokenization Matters

A language model can't read text — it can only read integer IDs into an embedding table. **Tokenization** is the function:

$$
\text{tokenize}: \text{string} \rightarrow \text{list of integers}
$$

Every choice in the tokenizer affects the model:

- **Vocabulary size** — bigger vocab → fewer tokens per sentence (shorter sequences, faster) but bigger embedding matrix (more params, more memory) and slower softmax.
- **Token granularity** — finer (character-level) → small vocab but very long sequences; coarser (word-level) → short sequences but huge vocab and out-of-vocabulary (OOV) problem.
- **Multilingual coverage** — does the tokenizer handle Chinese, Arabic, code, emoji well?
- **Special tokens** — `[BOS]`, `[EOS]`, `[PAD]`, `[SEP]`, `[CLS]`, chat templates, tool-calling markers.

The tokenizer is **frozen after pretraining** — you cannot change it without retraining the model. So getting it right is high-stakes.

## The Three Granularities

### Character-level

- Vocabulary = ASCII (or Unicode).
- Each character is a token.
- **Pros**: tiny vocabulary, no OOV.
- **Cons**: very long sequences (a sentence = dozens of tokens), model must learn word structure from scratch.

### Word-level

- Vocabulary = all words in the training corpus (or top-N most frequent).
- Each word is a token.
- **Pros**: short sequences, words are meaningful units.
- **Cons**: huge vocabulary, OOV problem (rare words → `[UNK]`), morphology (run/running/runs are unrelated tokens).

### Subword-level (the modern default)

- Vocabulary = commonly-occurring substrings (a few thousand to ~200k).
- Common words are single tokens; rare words are split into subwords.
- **Pros**: small-ish vocabulary, no OOV (any word can be represented), shorter sequences than character-level.
- **Cons**: tokenizer must be trained on the corpus; subwords can be linguistically unintuitive.

## The Three Main Subword Algorithms

| Algorithm     | Used by                              | Mechanism                                | Notes                                    |
|---------------|--------------------------------------|------------------------------------------|------------------------------------------|
| [[BPE]]       | GPT-2/3/4, Llama, Mistral, Tiktoken  | Merge most frequent pair, repeat         | Bottom-up; deterministic                 |
| [[WordPiece]] | BERT, DistilBERT, Electra            | Like BPE but maximizes likelihood        | Bottom-up; uses likelihood not frequency |
| Unigram LM    | T5, mT5, ALBERT (via SentencePiece)  | Start big, prune tokens that hurt loss   | Top-down; probabilistic                  |

[[SentencePiece]] is not an algorithm — it's a tokenizer library that implements BPE and Unigram, plus treats whitespace as a regular character (so it's language-agnostic and reversible).

## The Tokenization Pipeline

A modern LLM tokenizer does several steps:

1. **Normalization** — lowercase (sometimes), strip accents (sometimes), normalize unicode.
2. **Pre-tokenization** — split on whitespace and punctuation, but keep certain patterns together (e.g., numbers, URLs).
3. **Subword segmentation** — apply BPE / WordPiece / Unigram merges.
4. **Post-processing** — add special tokens (`[BOS]`, `[EOS]`), convert to IDs.

For example, GPT-4's `tiktoken` tokenizer:
- Pre-tokenization uses a regex that splits text into chunks like "word", "  ", "123", "!", etc.
- Each chunk is then BPE-tokenized independently.

## Vocabulary Size — Tradeoffs

| Vocab size | Pros                                       | Cons                                              |
|------------|--------------------------------------------|---------------------------------------------------|
| 32k        | Small embedding matrix, fast softmax       | Longer sequences, more "splits" of rare words     |
| 64k–128k   | Sweet spot for English + code              | Bigger embedding matrix                           |
| 200k+      | Good multilingual coverage, short seqs     | Very big embedding matrix; GPT-4 uses ~100k       |

The embedding matrix is `vocab_size × hidden_dim`. For a 4096-dim model with 128k vocab, that's 524M parameters just for embeddings — comparable to a small model on its own. This is why some models use **tied embeddings** (input and output share the matrix) or **factorized embeddings** (e.g., ALBERT).

## Special Tokens

Every tokenizer has special tokens:

| Token          | Purpose                                                    |
|----------------|------------------------------------------------------------|
| `[PAD]`        | Padding to fixed batch length.                             |
| `[BOS]` / `[CLS]` | Beginning of sequence / classification head.            |
| `[EOS]`        | End of sequence — model emits this to stop.               |
| `[SEP]`        | Separator between segments (BERT).                        |
| `[UNK]`        | Out-of-vocabulary fallback (subword tokenizers don't need this in practice). |
| `<\|im_start\|>`, `<\|im_end\|>` | Chat template markers (ChatML, etc.).      |
| `<\|tool_call\|>`, `<\|tool_response\|>` | Tool-calling markers.                  |

The choice of chat template and special tokens is a major part of **instruction tuning** and is what makes a base model into a chat model. See [[12 - Fine-Tuning/Instruction Tuning/03 - Instruction Tuning and Chat Templates|Instruction Tuning]] (planned).

## Why This Matters for AI

- **Tokenization affects every aspect of the model**: training cost (sequence length), inference latency (tokens generated), embedding matrix size, multilingual fairness, code understanding, math understanding.
- **Tokenizer bugs are silent** — if your chat template is wrong, the model will still produce reasonable-sounding output but be subtly worse. Many "my model is dumb" issues trace to tokenization.
- **Tokenizer choice affects evaluation** — different tokenizers make the same model benchmark differently because of sequence length effects.
- **Multilingual fairness** — tokenizers trained mostly on English make non-English text require 2–5x more tokens (the "tax" on non-English users). This is a real fairness issue in production.

## Production Implications

- **Tokenizer versioning** is critical. The model and tokenizer are a pair; mismatched versions produce garbage. Pin both in your model registry.
- **Token counting** is the basis of cost. APIs charge per token; budget per request by counting tokens before sending. Use `len(tokenizer.encode(text))`, not `len(text.split())`.
- **Context window math** — context length is measured in tokens, not characters. A 128k-token context holds roughly 100k English words or 50k Chinese characters (depending on tokenizer).
- **Streaming output** — generate tokens one at a time and decode incrementally. Be aware that BPE/WordPiece can produce partial multi-byte characters mid-stream; use `skip_special_tokens=True` and incremental decode.

## Common Pitfalls

- **Wrong tokenizer for the model** — using the GPT-2 tokenizer for a Llama model will silently produce nonsense.
- **Forgetting to add special tokens** — base models often need `[BOS]` prepended; chat models need their template applied.
- **Counting characters instead of tokens** — leads to wrong context-window and cost estimates.
- **Adding tokens without resizing embeddings** — when you add special tokens for fine-tuning, you must resize the embedding matrix and initialize the new rows. Forgetting this causes index-out-of-bounds or garbage.
- **Decoding partial tokens** — BPE merges can span multi-byte UTF-8 boundaries. Decode only complete tokens.

## Further Reading

- Sennrich, Haddow, Birch (2016), *Neural Machine Translation of Rare Words with Subword Units* — original BPE for NMT.
- Wu et al. (2016), *Google's Neural Machine Translation System* — WordPiece.
- Kudo (2018), *SentencePiece: A simple and language independent subword tokenizer*.
- HuggingFace tokenizers docs: https://huggingface.co/docs/tokenizers

## See Also

- [[BPE]]
- [[WordPiece]]
- [[SentencePiece]]
- [[Word2Vec GloVe FastText]]
- [[08 - LLMs/MOC|LLMs MOC]]
- [[05 - NLP Fundamentals/MOC|NLP Fundamentals MOC]]

## The Token Economy — Why Tokenization Drives Cost

LLM APIs are priced per token, not per character or word. This makes tokenization a direct cost driver. Empirical ratios (English text, GPT-4 tokenizer):

- 1 token ≈ 4 characters (English)
- 1 token ≈ 0.75 words (English)
- 1 token ≈ 1.5 characters (Chinese) — non-English text is "taxed" 2-3×
- 1 token ≈ 2-3 characters (code, especially with whitespace)

This means:
- 1M English words ≈ 1.3M tokens ≈ $0.13 (GPT-4o-mini input)
- 1M Chinese characters ≈ 670K tokens ≈ $0.07
- 1M lines of Python code ≈ 10-20M tokens ≈ $1-2

For production systems, **token counting is the basis of cost**. Always count tokens before sending a request (`len(tokenizer.encode(text))`), not characters. Token-aware chunking, caching, and routing all rely on accurate counts.

### The non-English tax

Tokenizers trained mostly on English assign multi-byte UTF-8 sequences to individual byte tokens, which means non-English text requires 2-5× more tokens per character. A Chinese sentence that's 50 characters might be 100+ tokens, while the equivalent English translation is 30 tokens. This is a real fairness issue: non-English users pay more for the same capability. Modern tokenizers (Qwen, DeepSeek) are trained with more multilingual data to reduce this tax.

## Tokenizer Versions and Compatibility

Tokenizers are versioned. Mixing versions produces silently wrong outputs:

| Model             | Tokenizer          | Vocab size | Notes                                  |
|-------------------|--------------------|------------|----------------------------------------|
| GPT-2            | `r50k_base`        | 50,257     | Original byte-level BPE                |
| GPT-3 / Codex    | `r50k_base` / `p50k_base` | 50,257 / 50,281 | Slight additions for code        |
| GPT-3.5 / GPT-4  | `cl100k_base`      | 100,357    | Major revision; better multilingual    |
| GPT-4o           | `o200k_base`       | 200,019    | Larger vocab; better non-English       |
| Llama 1/2        | SentencePiece BPE  | 32,000     | `▁` space convention                   |
| Llama 3          | Tiktoken-style BPE | 128,256    | Larger vocab; better multilingual      |
| Mistral 7B       | SentencePiece BPE  | 32,000     | Similar to Llama 2                     |
| Qwen 2/2.5       | Tiktoken-style BPE | 151,665+   | Strong Chinese / code coverage         |
| Gemma            | SentencePiece      | 256,000    | Very large vocab for multilingual      |
| DeepSeek-V3      | BPE                | 129,280    | Similar to Llama 3                     |

**Pin the tokenizer version in your model registry.** GPT-3 used `r50k_base`; GPT-3.5/4 use `cl100k_base`; GPT-4o uses `o200k_base`. The encodings are NOT interchangeable — a model trained with one will produce garbage with another.

## Vocabulary Size Tradeoffs — Detailed

The embedding matrix is `vocab_size × hidden_dim`. For Llama 3 8B (hidden_dim = 4096, vocab = 128K): embedding matrix = 128K × 4096 × 2 bytes (bf16) = 1 GB. That's 12% of the 8B total parameters, just for embeddings.

| Vocab size | Embedding params (4096-dim) | Pros                                       | Cons                                              |
|------------|------------------------------|--------------------------------------------|---------------------------------------------------|
| 32K        | 131M                         | Small embedding matrix, fast softmax       | Longer sequences, more splits of rare words       |
| 64K        | 262M                         | Balanced                                   | Balanced                                          |
| 128K       | 524M                         | Shorter sequences, better multilingual     | Bigger embedding matrix, slower softmax           |
| 256K       | 1.05B                        | Excellent multilingual, very short seqs    | Embedding matrix dominates; softmax is slow       |

**Tied embeddings**: input and output share the embedding matrix. Saves `vocab_size × hidden_dim` parameters. Used by Llama, Mistral, most modern LLMs. The tradeoff: the input embedding (good for token representation) and output projection (good for predicting next token) may have different optimal geometries. Untied (GPT-2, T5) gives slightly better quality but doubles the embedding parameter count.

**Factorized embeddings** (ALBERT): instead of `vocab × hidden`, use `vocab × factorized_dim + factorized_dim × hidden` where `factorized_dim << hidden`. Drastically reduces parameters for large vocabs. Rarely used in modern LLMs because the quality loss outweighs the parameter savings.

## Worked Example: Token Counting and Cost Estimation

```python
import tiktoken

class TokenCostEstimator:
    def __init__(self, model='gpt-4o', encoding='o200k_base'):
        self.encoding = tiktoken.get_encoding(encoding)
        # Pricing as of 2026 (illustrative)
        self.prices = {
            'gpt-4o': {'input': 2.50 / 1e6, 'output': 10.00 / 1e6},
            'gpt-4o-mini': {'input': 0.15 / 1e6, 'output': 0.60 / 1e6},
            'gpt-4': {'input': 30.00 / 1e6, 'output': 60.00 / 1e6},
        }

    def count_tokens(self, text: str) -> int:
        return len(self.encoding.encode(text))

    def estimate_cost(self, prompt: str, expected_output_tokens: int = 500) -> dict:
        input_tokens = self.count_tokens(prompt)
        output_tokens = expected_output_tokens
        price = self.prices[self.model]
        input_cost = input_tokens * price['input']
        output_cost = output_tokens * price['output']
        return {
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': input_tokens + output_tokens,
            'input_cost_usd': input_cost,
            'output_cost_usd': output_cost,
            'total_cost_usd': input_cost + output_cost,
        }

estimator = TokenCostEstimator(model='gpt-4o')
text = """Large language models are neural networks trained on vast amounts of text data.
They can generate human-like text, answer questions, and perform various language tasks."""
print(estimator.estimate_cost(text, expected_output_tokens=200))
```

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Garbage output from a model | Wrong tokenizer version | Pin tokenizer in model registry; verify with `tokenizer.encode` test |
| Cost is 5× expected | Counting characters, not tokens | Use `len(tokenizer.encode(text))` for cost estimation |
| Model can't do arithmetic | Numbers are split into single digits | Use a tokenizer that keeps multi-digit numbers together (Llama 3, Qwen) |
| Non-English text is expensive | Tokenizer trained mostly on English | Use a multilingual tokenizer (Qwen, Gemma, GPT-4o) |
| Adding special tokens breaks the model | Embedding matrix not resized | Call `model.resize_token_embeddings(len(tokenizer))` after adding |
| Streaming produces partial UTF-8 | BPE merges span multi-byte boundaries | Use incremental decode; accumulate bytes until a complete codepoint |
| Chat template not applied | Base model used without chat template | Apply the model's chat template (ChatML, Llama-3 format, etc.) |

## Connection to Other Concepts

- [[05 - NLP Fundamentals/Tokenization/02 - BPE|BPE]] — the dominant algorithm.
- [[05 - NLP Fundamentals/Tokenization/03 - WordPiece|WordPiece]] — BERT's algorithm.
- [[05 - NLP Fundamentals/Tokenization/04 - SentencePiece|SentencePiece]] — the library.
- [[05 - NLP Fundamentals/Embeddings/05 - Word2Vec GloVe FastText|Word2Vec GloVe FastText]] — pre-tokenization embeddings.
- [[05 - NLP Fundamentals/Tokenization/01 - Tokenization Overview|Tokenization Overview]] — this note.
- [[08 - LLMs/MOC|LLMs MOC]] — where tokenizers are used.
- [[12 - Fine-Tuning/Instruction Tuning/03 - Instruction Tuning and Chat Templates|Instruction Tuning and Chat Templates]] — chat templates and special tokens.
- [[13 - Inference/Decoding/07 - Constrained Decoding and CFG|Constrained Decoding and CFG]] — token-level constraints.
- [[17 - RAG/Ingestion and Retrieval/02 - Chunking Hybrid Search Reranking|Chunking Hybrid Search Reranking]] — token-aware chunking.
- [[22 - Production AI/Security/05 - PII and Data Leakage|PII and Data Leakage]] — tokenization and PII redaction.
- [[21 - LLMOps and MLOps/Pipelines/02 - Prompt Management|Prompt Management]] — token budgeting.
- [[21 - LLMOps and MLOps/Cost/06 - Cost Optimization|Cost Optimization]] — token cost is the main cost driver.

## Interview Questions

1. **Q: Why do modern LLMs use subword tokenization instead of word-level or character-level?**
   A: Subword tokenization hits the sweet spot between word-level (too sparse, huge vocab, OOV problem) and character-level (too fine, very long sequences). Common words become single tokens (efficient); rare words are split into subwords (no OOV); sequences are short (faster training/inference); vocabulary is bounded (~32K-256K). This is why every modern LLM uses BPE, WordPiece, or Unigram — they're all subword algorithms.

2. **Q: What's the difference between BPE, WordPiece, and Unigram?**
   A: **BPE** (bottom-up): start with characters, repeatedly merge the most frequent pair. Used by GPT-2/3/4, Llama, Mistral. **WordPiece** (bottom-up): like BPE but selects merges that maximize the likelihood of the training data (not just frequency). Used by BERT. **Unigram** (top-down): start with a large vocab, iteratively prune tokens whose removal least decreases likelihood. Produces multiple valid segmentations; uses Viterbi at encode time. Used by T5, ALBERT. SentencePiece is a library that implements both BPE and Unigram. All three produce similar quality; BPE is the most common due to simplicity and Tiktoken's speed.

3. **Q: How does the choice of tokenizer affect non-English users?**
   A: Tokenizers trained mostly on English assign multi-byte UTF-8 sequences to individual byte tokens. Non-English text requires 2-5× more tokens per character than English. A Chinese sentence that's 50 characters might be 100+ tokens, while the equivalent English translation is 30 tokens. This is the "non-English tax" — non-English users pay more for the same capability. Modern tokenizers (Qwen, Gemma, GPT-4o) are trained with more multilingual data to reduce this tax. GPT-4o's `o200k_base` is significantly better for non-English than GPT-3.5's `cl100k_base`.

4. **Q: What happens if you add a special token during fine-tuning without resizing the embedding matrix?**
   A: The model produces garbage or crashes. The tokenizer returns an index beyond the embedding matrix's range, causing an index-out-of-bounds error. Or, if the index happens to be within range, the model uses an existing token's embedding for the new special token, producing semantically wrong outputs. The fix: always call `model.resize_token_embeddings(len(tokenizer))` after adding special tokens. The new rows are initialized with random values, so you also need to fine-tune to teach the model what the new tokens mean.

5. **Q: Why is the embedding matrix so large, and how do tied embeddings help?**
   A: The embedding matrix is `vocab_size × hidden_dim`. For Llama 3 8B (vocab = 128K, hidden = 4096): 524M parameters, just for embeddings — 6.6% of the 8B total. Tied embeddings share the matrix between input (token → vector) and output (vector → token probabilities), saving `vocab_size × hidden_dim` parameters. Used by Llama, Mistral, most modern LLMs. The tradeoff: input embedding and output projection may have different optimal geometries; untied (GPT-2, T5) gives slightly better quality but doubles the parameter count.

6. **Q: How would you handle streaming token decoding where BPE merges span multi-byte UTF-8 boundaries?**
   A: BPE merges can produce byte sequences that are partial UTF-8 codepoints mid-stream. Naive decoding produces errors. Three approaches: (1) **Accumulate bytes** until you have a complete UTF-8 codepoint, then decode. Track the expected byte count from the leading byte (1-4 bytes for UTF-8). (2) **Use `errors='replace'`** in decode to substitute replacement characters for partial sequences. Visually ugly but won't crash. (3) **Use the tokenizer's streaming API** (HuggingFace's `decode_incremental` or `convert_tokens_to_string`). Production serving frameworks (vLLM, TGI) handle this automatically.

## See Also

- [[BPE]]
- [[WordPiece]]
- [[SentencePiece]]
- [[Word2Vec GloVe FastText]]
- [[08 - LLMs/MOC|LLMs MOC]]
- [[05 - NLP Fundamentals/MOC|NLP Fundamentals MOC]]
