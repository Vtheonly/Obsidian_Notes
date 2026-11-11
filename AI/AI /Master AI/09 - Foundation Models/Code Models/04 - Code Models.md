---
tags: [foundation-models, code-models, codex, starcoder, deepseek-coder]
iteration: 6
created: 2026-08-08
aliases: [Code Models, Codex, StarCoder, Code Llama, DeepSeek-Coder]
---

# 04 — Code Models

> [!info] TL;DR
> Code models are LLMs specialized for software engineering tasks: code generation, code completion, code review, bug fixing, and code translation. They are pretrained on massive corpora of source code (GitHub, GitLab, public repositories) and often further trained on code-related instruction data. The major families are **Codex** (OpenAI, closed), **StarCoder** (BigCode, open), **Code Llama** (Meta, open), **DeepSeek-Coder** (DeepSeek, open), and **Qwen-Coder** (Alibaba, open). Code models introduce domain-specific design choices — fill-in-the-middle (FIM) objectives, byte-level tokenizers, large context windows for repositories — that distinguish them from general LLMs.

## Why Code Models Are Different

Code is structurally different from natural language in ways that matter for model design:

- **Formal syntax**: code must parse. A missing bracket or wrong indentation breaks execution. Models trained on natural language tolerate minor grammar errors; code models must respect syntax.
- **Long-range dependencies**: a function defined in one file may be called in another. Repository-level understanding requires long context (32K-128K tokens).
- **Bidirectional context**: code completion often requires filling in the middle of a function — the model sees both the prefix (function signature) and the suffix (closing brace). This is the **fill-in-the-middle (FIM)** objective, distinct from standard left-to-right language modeling.
- **Sparse, repetitive patterns**: code has more repeated patterns (boilerplate, common idioms) than natural language. Byte-level tokenizers help capture these without fragmentation.

A general LLM fine-tuned on code works okay, but a model designed from scratch for code works much better.

## The Major Code Model Families

### Codex (OpenAI, closed)

Codex (2021) was the first major code model, described in the paper "Evaluating Large Language Models Trained on Code" (Chen et al., 2021). It powered the original GitHub Copilot. **Status:** Not publicly released. The model is accessible only via OpenAI's API (as the `code-*` models) and via Copilot. Architecture: GPT-3 derivative, trained on 159GB of code from GitHub. **Status as of 2026:** Codex as a distinct model name is deprecated; OpenAI's current code-capable models (GPT-4o, o1, o3) inherit Codex's code training but are general-purpose.

### StarCoder / StarCoder 2 (BigCode, open)

StarCoder (2023) was the first major open-weights code model with permissive licensing. BigCode is a collaboration between HuggingFace and ServiceNow. **Architecture:** 15.5B parameters, 8K context (StarCoder 1); 3B/7B/15B, 16K context with Fill-in-the-Middle (StarCoder 2). Trained on 80+ programming languages from The Stack (a curated GitHub dump with per-file license attribution). **Strengths:** transparent data provenance, opt-out for repository authors, strong on less-common languages. The Stack v2 used for StarCoder 2 contains 4x more data than v1.

### Code Llama (Meta, open)

Code Llama (2023) is a Llama 2 derivative fine-tuned on code. **Architecture:** 7B/13B/34B/70B parameters; 16K context (extendable to 100K with RoPE scaling). Trained on 500B tokens of code. **Strengths:** inherits Llama's strong language understanding, available in three flavors: base, Python-specialized, and Instruct. The 70B version is competitive with GPT-4 on HumanEval at release. **Licensing:** Llama 2 community license (with usage caps for very large commercial deployments).

### DeepSeek-Coder (DeepSeek, open)

DeepSeek-Coder (2024) is a code-focused model from DeepSeek. **Architecture:** 1.3B/6.7B/33B parameters; 16K context. Trained on 2T tokens (87% code, 13% natural language). **Strengths:** strong performance on math+code benchmarks, particularly the 33B version. Released under a permissive license (MIT for code, DeepSeek license for weights). DeepSeek-Coder-V2 (2024) adds MoE architecture and supports 33K+ languages.

### Qwen-Coder (Alibaba, open)

Qwen-Coder (2024) is a code-specialized variant of the Qwen model family. **Architecture:** 1.5B/7B/32B parameters; 32K+ context. Trained on a curated code corpus with emphasis on practical software engineering (not just algorithmic problems). **Strengths:** strong on real-world coding tasks (debugging, refactoring) rather than just competitive programming. Permissive Apache 2.0 license for the smaller models.

## Key Design Choices

### Fill-in-the-Middle (FIM)

Standard LMs are left-to-right: given the prefix, predict the next token. But code completion often requires filling in the middle: given the function signature and the code after the cursor, predict what's in between.

FIM reformulates training to support this. The training example `(prefix, middle, suffix)` is transformed into one of two formats:

- **PSM** (Prefix-Suffix-Middle): `<fim_prefix>prefix<fim_suffix>suffix<fim_middle>middle`
- **SPM** (Suffix-Prefix-Middle): `<fim_suffix>suffix<fim_prefix>prefix<fim_middle>middle`

The model is trained on both formats with equal probability. At inference, the IDE provides the prefix and suffix; the model generates the middle.

Without FIM, code completion is limited to "predict the next token given what's before the cursor." With FIM, the model uses both before-cursor and after-cursor context, dramatically improving completion quality.

### Byte-Level Tokenizers

Code contains many out-of-vocabulary tokens for natural-language tokenizers: variable names, camelCase/snake_case identifiers, special symbols. Byte-level tokenizers (like GPT-2's BPE on UTF-8 bytes) handle any character without an `<unk>` token.

StarCoder uses a byte-level BPE with 49K tokens. This handles all programming languages uniformly, including those with non-ASCII identifiers (Chinese variable names, emoji in comments).

### Long Context for Repository Understanding

Modern code models support 16K-128K context. This enables repository-level tasks: "given this entire codebase, refactor the auth module." The model sees the imports, the type definitions, and the call sites — not just the file being edited.

Techniques for long context:

- **RoPE scaling** (Code Llama): extend the RoPE base frequency to attend over longer distances.
- **YaRN** (some Qwen-Coder variants): a more sophisticated RoPE extension.
- **Training on long sequences**: StarCoder 2 explicitly trains on long-context examples.

### Repository-Level Training Data

Beyond single files, modern code models train on repository-level context: multiple files from the same repo, so the model learns how files relate. DeepSeek-Coder and StarCoder 2 both use repository-aware data sampling.

## Evaluation

Code models are evaluated on:

- **HumanEval** (OpenAI, 2021): 164 hand-written Python problems. Each problem has a function signature and docstring; the model must implement the function. Pass@1 is the standard metric. **Limitation:** small, easy, Python-only.
- **HumanEval+ / MBPP+**: expanded versions with more test cases (catches more bugs).
- **MBPP** (Google, 2021): 974 Python problems, mostly beginner-level.
- **MultiPL-E**: HumanEval translated into 18 languages. Tests multilingual code capability.
- **LiveCodeBench**: problems scraped from LeetCode/AtCoder with timestamps, so you can test on problems released after the model's training cutoff. Prevents contamination.
- **BigCodeBench**: harder, practical tasks requiring library usage.
- **SWE-bench**: real GitHub issues with the corresponding PRs. The model must produce a patch that resolves the issue. Tests repository-level understanding.

Pass@1 on HumanEval is the most commonly reported number, but it's saturated (models achieve 90%+) and contaminated (many models saw HumanEval during training). LiveCodeBench and SWE-bench are more reliable for comparing 2026-era models.

## How Code Models Are Used in Production

### IDE Integration (Copilot, Cursor, Continue)

The dominant production use case is inline completion in the IDE. The user types; the model suggests the rest of the line or the next few lines. FIM is essential here — the model uses both before-cursor and after-cursor context.

Latency matters: suggestions must appear in <300ms or users disable them. This drives serving optimizations (small models, prefix caching, speculative decoding).

### Chat-Based Coding (ChatGPT, Claude, Cursor Chat)

For complex tasks ("refactor this module", "debug this error"), users interact conversationally. The model sees the code, the error, the conversation history. This is closer to general LLM use but with code-specialized models.

### Agentic Coding (Devin, SWE-Agent, OpenDevin)

The frontier use case: agents that autonomously navigate a codebase, make changes, run tests, and iterate. This requires:

- Long context (to hold the repo structure).
- Tool use (file operations, shell commands, test runners).
- Planning (decompose "implement feature X" into steps).
- Self-correction (when tests fail, diagnose and fix).

Code models that perform well on HumanEval often struggle with agentic tasks, which require multi-step reasoning and tool use. SWE-bench is the relevant benchmark.

## Strengths and Limitations of Current Code Models

### Strengths

- **Algorithmic problem-solving**: top models solve 90%+ of HumanEval.
- **Multi-language support**: top models handle 80+ languages.
- **Repository-level context**: 128K+ context windows.
- **Tool integration**: production models support function calling for IDE integration.

### Limitations

- **Hallucinated APIs**: models suggest APIs that don't exist or have wrong signatures.
- **Outdated library knowledge**: libraries evolve; models trained a year ago may not know current APIs.
- **Weak on niche languages**: strong on Python/JavaScript/Java; weaker on Rust, Zig, niche DSLs.
- **Limited debugging ability**: models can write code but struggle to systematically diagnose bugs in unfamiliar codebases.
- **Security vulnerabilities**: models produce code with common vulnerabilities (SQL injection, XSS) unless explicitly trained not to.

## Future Directions

- **Repository-aware models**: models that maintain a persistent representation of the codebase across queries.
- **Execution-aware training**: models trained not just on code text but on execution traces (what does this code do when run?).
- **Test-time compute for code**: applying reasoning-model techniques (chain-of-thought, self-reflection) to code generation.
- **Multimodal code models**: models that understand code + screenshots + diagrams (for UI work, data science).
- **Better agentic evaluation**: SWE-bench is improving, but we need benchmarks for long-horizon coding tasks (multi-day projects).

## See Also

- [[01 - Vision Foundation Models]] — sister domain
- [[02 - Embedding Models for Retrieval]] — sister domain
- [[03 - Reasoning Models]] — sister domain
- [[05 - Multimodal Foundation Models]] — sister domain
- [[07 - Transformers/MOC|07 Transformers]] — the underlying architecture
- [[08 - LLMs/MOC|08 LLMs]] — general LLM background
- [[09 - Foundation Models/MOC|09 Foundation Models MOC]]
