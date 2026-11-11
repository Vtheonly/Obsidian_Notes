---
tags: [nlp, tokenization, sentencepiece]
iteration: 11
created: 2026-08-07
last_updated: 2026-08-08
aliases: [SentencePiece]
---

# SentencePiece

> [!info] TL;DR
> SentencePiece is a tokenizer library (not an algorithm) that implements BPE and Unigram LM tokenizers. Its key innovation: **treats whitespace as a regular character**, making it language-agnostic and fully reversible. Used by T5, ALBERT, XLNet, Llama (BPE mode), and many multilingual models.

## What SentencePiece Is

SentencePiece (Kudo & Richardson, 2018) is a tokenizer library that:

1. Implements two subword algorithms: **BPE** and **Unigram Language Model**.
2. Treats text as a raw byte sequence — whitespace is just another character (encoded as `▁`, the meta-symbol "space").
3. Is **language-agnostic** — no language-specific pre-tokenization.
4. Is **lossless** — you can always reconstruct the original text from tokens.

The whitespace-as-character design is the key innovation. Other tokenizers (BPE in GPT-2, WordPiece in BERT) pre-tokenize by splitting on whitespace first, which assumes words are separated by spaces. This breaks for Chinese, Japanese, Thai, and other languages without explicit word boundaries.

## The `▁` Meta-Symbol

SentencePiece replaces the space character with a special Unicode codepoint `▁` (U+2581, "LOWER ONE EIGHTH BLOCK"). This:

- Makes spaces visible in the token stream.
- Allows tokens to encode whether they follow a space: `▁Hello` (after space) vs `Hello` (no preceding space).
- Lets the model learn that `▁the` and `the` are different tokens — useful for distinguishing word-initial vs word-internal occurrences.

## Algorithms in SentencePiece

### BPE mode

Same as [[BPE]] but applied to the `▁`-substituted byte sequence without pre-tokenization. Llama, Llama 2, Llama 3, and Mistral all use SentencePiece-BPE.

### Unigram LM mode

A **top-down** algorithm:

1. Start with a large vocabulary of candidate subwords (e.g., all substrings up to length N in the corpus, plus characters).
2. Compute the likelihood of the corpus under a Unigram LM that picks subwords probabilistically.
3. Iteratively **prune** the subwords whose removal least decreases the likelihood.
4. Stop when the vocabulary reaches the target size.

The Unigram LM produces **multiple valid segmentations** per word. At encode time, the best segmentation is found via Viterbi (the most probable one) or sampled (for data augmentation).

T5, mT5, ALBERT, and XLNet use SentencePiece-Unigram.

## Key Features

- **Reversibility**: `decode(encode(text)) == text` — always.
- **No `[UNK]`** (with byte-fallback): falls back to UTF-8 bytes for unknown characters.
- **Multilingual** by design — works equally well for English, Chinese, Japanese, Korean, Arabic, etc.
- **Streaming-friendly**: encoders/decoders can be used in incremental mode.
- **Vocab export**: vocabulary is a plain text file, easy to inspect and version.

## Worked Example

```python
import sentencepiece as spm

# Train (typically done once per model)
spm.SentencePieceTrainer.train(
    input='corpus.txt',
    model_prefix='sp_model',
    vocab_size=32000,
    model_type='bpe',  # or 'unigram'
    character_coverage=0.9995,
    normalizer_spec_name='nmt_nfkc',
)

# Use
sp = spm.SentencePieceProcessor()
sp.load('sp_model.model')

tokens = sp.encode('Hello world')  # [1234, 5678]
text = sp.decode(tokens)           # 'Hello world'
```

In HuggingFace:

```python
from transformers import LlamaTokenizer
tok = LlamaTokenizer.from_pretrained('meta-llama/Llama-2-7b')
tok.encode('Hello world')  # uses SentencePiece under the hood
```

## The `normalizer_spec_name` Option

SentencePiece supports several normalization rules:

- `nmt_nfkc` (default) — NFKC normalization + some NMT-specific tweaks (e.g., strip accents in some cases).
- `identity` — no normalization.
- Custom rules — you can specify your own.

Normalization affects what counts as "the same character" — important for multilingual corpora where the same letter can be encoded multiple ways in Unicode.

## Why This Matters for AI

- SentencePiece is the foundation of most **multilingual LLMs** — Llama, Qwen, mT5, etc.
- It's the de-facto standard for **open-source tokenizers**. If you train a new model from scratch, you probably use SentencePiece.
- The `▁`-as-space convention is ubiquitous in modern tokenizer outputs. Recognizing `▁Hello` as "space + Hello" is essential for debugging.
- SentencePiece's Unigram mode is the **only mainstream probabilistic tokenizer**. Its sampling feature is used for tokenizer-based data augmentation.

## Production Implications

- **Use the official SentencePiece model file** for each model. Never retrain.
- **`character_coverage`** matters for non-English: 1.0 covers all characters (good for very multilingual corpora) but uses more vocab budget on rare characters. 0.9995 is the typical default.
- **Vocab size considerations** — SentencePiece can handle very large vocabularies (200k+). Larger vocabs → shorter sequences but bigger embeddings.
- **Inference performance** — SentencePiece's pure-Python implementation is slow. Use the C++ extension (default in modern versions) or pre-tokenize in batch.
- **Streaming decoding** — when generating tokens one at a time, you must handle the `▁` correctly. Most serving frameworks handle this, but custom implementations may not.

## Common Pitfalls

- **Treating `▁` as part of the word** — `▁Hello` is two characters of metadata (`▁`) + the word. When decoding, replace `▁` with a space.
- **Forgetting to use the model's normalization** — different SentencePiece models have different normalization rules; using one model's normalizer on another's tokens corrupts the text.
- **Mixing SentencePiece with BPE/WordPiece** — they have different vocabularies and conventions. Don't mix.
- **Truncating mid-token** — when streaming, never split a token across chunks. Decode at token boundaries.

## SentencePiece vs BPE vs WordPiece — Quick Reference

| Feature                     | SentencePiece-BPE | SentencePiece-Unigram | tiktoken BPE | WordPiece |
|-----------------------------|-------------------|-----------------------|--------------|-----------|
| Whitespace handling         | `▁` as char       | `▁` as char           | Pre-tokenize | Pre-tokenize |
| Algorithm                   | Bottom-up merges  | Top-down pruning      | Bottom-up merges | Bottom-up merges |
| Probabilistic segmentation  | No                | Yes                   | No           | No        |
| Language-agnostic           | Yes               | Yes                   | Yes (byte-level) | No (assumes word boundaries) |
| Used by                     | Llama, Mistral    | T5, ALBERT            | GPT-2/3/4    | BERT      |

## Further Reading

- Kudo (2018), *SentencePiece: A simple and language independent subword tokenizer and detokenizer for neural text processing*.
- Kudo & Richardson (2018), *SentencePiece: A simple and language independent subword tokenizer* (EMNLP demo).
- Repo: https://github.com/google/sentencepiece

## See Also

- [[Tokenization Overview]]
- [[BPE]]
- [[WordPiece]]
- [[05 - NLP Fundamentals/MOC|NLP Fundamentals MOC]]

## The `▁` Symbol — Implementation Details

SentencePiece replaces the space character with `▁` (U+2581, "LOWER ONE EIGHTH BLOCK"). This is a visible Unicode character that doesn't appear in normal text, making it safe to use as a marker. Key implementation details:

- **Encoding**: text `"Hello world"` becomes `"▁Hello▁world"` (spaces replaced with `▁`).
- **Tokenization**: BPE/Unigram operates on this `▁`-substituted text. Tokens like `▁Hello`, `▁world` encode the leading space.
- **Decoding**: replace `▁` with space: `▁Hello▁world` → `Hello world`. Lossless.
- **Edge cases**: leading spaces, multiple spaces, trailing spaces are all preserved. `"  Hello  "` becomes `"▁▁Hello▁▁"` — both leading spaces are captured.

This is different from BPE's approach (GPT-2), which keeps spaces as actual space characters and attaches them to the following token (`' Hello'`). Both approaches work; SentencePiece's `▁` is more visible and explicit, while BPE's space-attachment is more compact.

## Unigram LM Segmentation — Viterbi Decoding

Unigram LM produces multiple valid segmentations per word. At encode time, the best segmentation is found via **Viterbi** — dynamic programming over the token sequence.

For a word `"lowest"` with possible segmentations:
- `[low, est]` — probabilities $P(\text{low}) \times P(\text{est}) = 0.001 \times 0.002 = 2 \times 10^{-6}$
- `[low, e, s, t]` — $0.001 \times 0.01 \times 0.01 \times 0.01 = 10^{-9}$
- `[l, o, w, e, s, t]` — $10^{-12}$

Viterbi finds the segmentation with the highest probability. This is $O(L^2)$ per word where $L$ is word length — fast enough for production.

### Sampling for data augmentation

Unigram LM can also **sample** segmentations (instead of always taking the best). This produces different token sequences for the same text on different training epochs, acting as a form of data augmentation. This is why T5 and ALBERT (which use Unigram) are slightly more robust to tokenization variation than BPE-trained models.

## Byte-Fallback — Handling Any Character

SentencePiece's **byte-fallback** mode handles unknown characters by falling back to UTF-8 bytes:

- If a character isn't in the vocab, decompose it into UTF-8 bytes.
- Each byte is a token (e.g., `<0xE4>`, `<0xB8>`, `<0xAD>` for the Chinese character `中`).
- This guarantees no `[UNK]` tokens ever — any Unicode string is representable.

Byte-fallback is enabled by default in modern SentencePiece models (Llama 2/3, Mistral). Without it, a single unknown character would produce an `[UNK]` token, breaking the model's output.

## Production Performance Considerations

- **Pure-Python SentencePiece is slow** — ~50K tokens/sec on a single core. Too slow for high-throughput production.
- **C++ extension** (default in modern `pip install sentencepiece`) is ~10× faster — ~500K tokens/sec.
- **Batch encoding**: `sp.encode_batch(texts)` parallelizes across texts.
- **Caching**: encode prompts once and cache the token IDs. Decoding is cheap; encoding is moderately expensive.
- **Streaming**: when generating tokens one at a time, you must handle the `▁` correctly. Most serving frameworks (vLLM, TGI) handle this automatically.

## Worked Example: SentencePiece BPE vs Unigram

```python
import sentencepiece as spm

# Train BPE model
spm.SentencePieceTrainer.train(
    input='corpus.txt',
    model_prefix='bpe_model',
    vocab_size=32000,
    model_type='bpe',
    character_coverage=0.9995,
)

# Train Unigram model
spm.SentencePieceTrainer.train(
    input='corpus.txt',
    model_prefix='unigram_model',
    vocab_size=32000,
    model_type='unigram',
    character_coverage=0.9995,
)

# Compare
bpe_sp = spm.SentencePieceProcessor(); bpe_sp.load('bpe_model.model')
uni_sp = spm.SentencePieceProcessor(); uni_sp.load('unigram_model.model')

text = "Hello world"
print(f"BPE:     {bpe_sp.encode(text)} -> {bpe_sp.encode_as_pieces(text)}")
print(f"Unigram: {uni_sp.encode(text)} -> {uni_sp.encode_as_pieces(text)}")

# Sample from Unigram (data augmentation)
print(f"Unigram sampled: {uni_sp.encode(text, enable_sampling=True, alpha=0.1)}")

# Round-trip (lossless)
assert bpe_sp.decode(bpe_sp.encode(text)) == text
assert uni_sp.decode(uni_sp.encode(text)) == text
```

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Treating `▁` as part of the word | Misunderstanding the convention | Replace `▁` with space when decoding; never display raw `▁` to users |
| Mixing SentencePiece with other tokenizers | Different vocabularies and conventions | Don't mix; pick one tokenizer per model |
| Wrong normalization rule | Different SentencePiece models have different normalizers | Use the model's specified normalizer; don't apply external normalization |
| Slow encoding | Pure-Python SentencePiece | Install the C++ extension (`pip install sentencepiece` includes it by default) |
| `[UNK]` tokens appearing | Byte-fallback not enabled | Re-train with `byte_fallback=true` |

## Connection to Other Concepts

- [[05 - NLP Fundamentals/Tokenization/01 - Tokenization Overview|Tokenization Overview]] — the broader context.
- [[05 - NLP Fundamentals/Tokenization/02 - BPE|BPE]] — the algorithm SentencePiece implements.
- [[05 - NLP Fundamentals/Tokenization/03 - WordPiece|WordPiece]] — BERT's algorithm (not SentencePiece).
- [[10 - Model Architecture Research/Open Source/03 - Llama Family Architecture|Llama Family Architecture]] — uses SentencePiece-BPE.
- [[10 - Model Architecture Research/Open Source/04 - Mistral and Mixtral Architecture|Mistral and Mixtral Architecture]] — same.
- [[26 - Papers/Transformers/05 - T5 2019|T5 2019]] — uses SentencePiece-Unigram.
- [[08 - LLMs/MOC|LLMs MOC]] — where SentencePiece is used.
- [[12 - Fine-Tuning/Instruction Tuning/03 - Instruction Tuning and Chat Templates|Instruction Tuning and Chat Templates]] — chat templates with SentencePiece tokens.

## Interview Questions

1. **Q: What is SentencePiece's `▁` symbol and why is it used?**
   A: SentencePiece replaces the space character with `▁` (U+2581, "LOWER ONE EIGHTH BLOCK"). This is a visible Unicode character that doesn't appear in normal text, making it safe as a marker. The benefit: spaces are treated as regular characters, so the tokenizer is language-agnostic (works for Chinese, Japanese, Thai — languages without explicit word boundaries) and lossless (`decode(encode(text)) == text` always). Tokens like `▁Hello` encode the leading space, distinguishing mid-sentence from after-space. This is different from GPT-2's approach of keeping spaces as actual characters and attaching them to the following token.

2. **Q: Compare SentencePiece-BPE and SentencePiece-Unigram.**
   A: **BPE** (bottom-up): start with characters/bytes, repeatedly merge the most frequent pair. Deterministic output — one segmentation per text. **Unigram** (top-down): start with a large vocab, iteratively prune tokens whose removal least decreases likelihood. Produces multiple valid segmentations; uses Viterbi at encode time to find the best. Unigram also supports sampling (for data augmentation). BPE is simpler and faster; Unigram is more principled (likelihood-based) and offers augmentation. Llama/Mistral use BPE; T5/ALBERT use Unigram. Both produce similar quality.

3. **Q: How does byte-fallback work and why is it important?**
   A: Byte-fallback handles unknown characters by decomposing them into UTF-8 bytes. If a character isn't in the vocab, it's split into 1-4 byte tokens (e.g., `<0xE4>`, `<0xB8>`, `<0xAD>` for the Chinese character `中`). This guarantees no `[UNK]` tokens ever — any Unicode string is representable. Without byte-fallback, a single unknown character (e.g., a rare emoji or an unusual script) would produce an `[UNK]` token, breaking the model's output. Byte-fallback is enabled by default in modern SentencePiece models (Llama 2/3, Mistral).

4. **Q: Why is SentencePiece better than GPT-2's BPE for multilingual text?**
   A: Two reasons. (1) **No language-specific pre-tokenization** — GPT-2's BPE splits on whitespace (which assumes word boundaries), while SentencePiece treats the entire text as a byte sequence (no assumptions about word boundaries). This works for Chinese, Japanese, Thai, and other languages without explicit word boundaries. (2) **Lossless round-trip** — `decode(encode(text)) == text` always, because spaces are preserved as `▁`. GPT-2's BPE is also lossless in practice but the convention is less explicit. The cost: SentencePiece's `▁` convention is visually uglier and requires care when displaying tokens.

5. **Q: How does Unigram LM's sampling work as data augmentation?**
   A: Unigram LM produces multiple valid segmentations per word, each with a probability. At encode time, Viterbi normally picks the highest-probability segmentation. But Unigram can also **sample** from the distribution over segmentations (with temperature `alpha`). This produces different token sequences for the same text on different training epochs. The model sees slightly different inputs each epoch, which acts as regularization — the model becomes more robust to tokenization variation. This is why T5 and ALBERT (Unigram-based) are slightly more robust than BPE-trained models.

6. **Q: When would you choose SentencePiece over Tiktoken?**
   A: Choose SentencePiece when: (1) you're training a new multilingual model from scratch (SentencePiece's language-agnostic design handles non-English better); (2) you need lossless round-trip with explicit space handling; (3) you want Unigram's sampling for data augmentation; (4) you're working with Llama/Mistral/T5 (which use SentencePiece). Choose Tiktoken when: (1) you're using OpenAI models (GPT-2/3/4) — Tiktoken is the official tokenizer; (2) you need maximum encoding speed (Tiktoken is slightly faster); (3) you're building an English-focused application where the `▁` convention is unnecessary overhead. Both are excellent; the choice is mostly about ecosystem compatibility.

## See Also

- [[Tokenization Overview]]
- [[BPE]]
- [[WordPiece]]
- [[05 - NLP Fundamentals/MOC|NLP Fundamentals MOC]]
