---
tags: [glossary, terms, reference]
iteration: 4
created: 2026-08-08
aliases: [A-Z Terms, Glossary Terms]
---

# A-Z Glossary Terms

> [!info] Alphabetical glossary of AI engineering terms, with concise definitions and links to concept notes. For acronyms, see [[Acronyms Index]].

## A

- **Activation function** — a nonlinear function applied to a neuron's output. Common: ReLU, GELU, SwiGLU. See [[02 - Activation Functions]]
- **Activation patching** — intervention technique for establishing causality in interpretability. See [[04 - Activation Patching and Causal Tracing]]
- **Adapter** — a small trainable module inserted into a frozen pretrained model for efficient fine-tuning. See [[01 - LoRA]]
- **Additive attention** — Bahdanau's scoring function using a feed-forward network. See [[01 - Bahdanau Attention 2014]]
- **Agent** — an LLM that reasons and takes actions via tools. See [[01 - Agent vs Workflow vs LLM Application]]
- **Agentic RAG** — RAG where the LLM decides when to retrieve and what to query. See [[03 - Advanced RAG Patterns]]
- **Alignment** — adjusting model behavior to be helpful, harmless, and honest. See [[07 - InstructGPT 2022]]
- **ALiBi** — positional encoding using attention biases. See [[09 - ALiBi]]
- **Anchor box** — predefined bounding box in object detection.
- **Approximate Nearest Neighbor (ANN)** — algorithms for fast vector similarity search. See [[04 - Vector Memory Backends]]
- **Attention** — mechanism for weighting different parts of the input. See [[04 - Self-Attention]]
- **Attention head** — a single attention sublayer in multi-head attention. See [[05 - Multi-Head Attention]]
- **Attention weight** — the softmax-normalized similarity between a query and a key.
- **Autonomous agent** — an agent that operates without human intervention for extended periods.
- **Autoregressive** — generating one token at a time, conditioning on previous outputs. See [[01 - Decoder-Only Architecture]]

## B

- **Backpropagation** — algorithm for computing gradients in neural networks. See [[06 - Backpropagation]]
- **Bahdanau attention** — additive attention; the original attention mechanism. See [[01 - Bahdanau Attention 2014]]
- **Batch size** — number of examples processed in one forward/backward pass.
- **Beam search** — decoding that maintains top-K candidate sequences. See [[03 - Sampling Strategies]]
- **BERT** — bidirectional encoder Transformer. See [[03 - BERT 2018]]
- **Bias** — systematic deviation from the true value; can refer to model bias (demographic) or statistical bias (estimator).
- **Block table** — PagedAttention's mapping from logical to physical KV cache blocks. See [[10 - PagedAttention vLLM 2023]]
- **BPE** — Byte-Pair Encoding; tokenization by merging frequent character pairs. See [[02 - BPE]]
- **Broadcasting** — NumPy/tensor operation for combining arrays of different shapes. See [[06 - Tensors and Broadcasting]]
- **Byte-level BPE** — BPE operating on bytes, avoiding out-of-vocabulary tokens. Used in GPT-2.

## C

- **Causal masking** — preventing attention to future tokens; used in decoders. See [[01 - Decoder-Only Architecture]]
- **Causal tracing** — a specific activation patching technique for localizing information. See [[04 - Activation Patching and Causal Tracing]]
- **Chain-of-Thought (CoT)** — prompting the model to reason step by step. See [[02 - Chain-of-Thought]]
- **Chat template** — format for wrapping user/assistant messages. See [[03 - Instruction Tuning and Chat Templates]]
- **Checkpoint** — saved model state during training, used for resumption or evaluation.
- **Chunking** — splitting documents into passages for RAG. See [[02 - Chunking Hybrid Search Reranking]]
- **Circuit** — a subnetwork of attention heads/MLPs performing a specific function. See [[01 - Mechanistic Interpretability]]
- **Classifier** — a model that predicts discrete labels.
- **CLIP** — contrastive vision-language model. See [[02 - CLIP]]
- **Compute-optimal** — training at the optimal ratio of parameters to data. See [[01 - Pretraining Objectives and Scaling Laws]]
- **Concat attention** — Bahdanau-style additive attention.
- **Conditioning** — providing context to a generative model to guide output.
- **Constitutional AI** — alignment via AI feedback on the model's own outputs.
- **Context window** — the maximum sequence length an LLM can process.
- **Continuous batching** — iteration-level batching for LLM serving. See [[04 - vLLM and Continuous Batching]]
- **Contrastive learning** — training to pull similar examples together, push dissimilar apart. See [[02 - CLIP]]
- **Control task** — a baseline for probing experiments. See [[05 - Probing]]
- **Convolution** — sliding-window operation over an input. See [[03 - CNNs]]
- **Cross-attention** — attention between two sequences (e.g., encoder-decoder). See [[06 - Cross-Modal Attention]]
- **Cross-encoder** — a model that takes (query, document) pairs and outputs a relevance score. Used for reranking.
- **Cross-entropy** — loss function for classification. See [[15 - Entropy Cross-Entropy KL]]
- **Curriculum learning** — training on increasingly difficult examples.

## D

- **Decoder** — the generation part of a Transformer. See [[01 - Decoder-Only Architecture]]
- **Deduplication** — removing duplicate data in pretraining. See [[01 - Pretraining Objectives and Scaling Laws]]
- **Deep learning** — neural networks with many layers.
- **Dense model** — non-MoE model; all parameters active per token.
- **Diffusion** — generative process that iteratively denoises. See [[05 - DiT and FLUX]]
- **Distillation** — training a smaller model to mimic a larger one.
- **Distributed training** — training across multiple GPUs/nodes. See [[02 - Distributed Training]]
- **Dot product** — sum of element-wise products; a similarity measure. See [[02 - Dot Product]]
- **DPO** — Direct Preference Optimization. See [[09 - DPO 2023]]
- **Dropout** — regularization that randomly zeros activations during training.

## E

- **Early stopping** — stopping training when validation performance stops improving.
- **Edge device** — resource-constrained device (phone, IoT). See [[08 - Ollama and llama.cpp]]
- **Embedding** — vector representation of a token or document.
- **Encoder** — the understanding part of a Transformer. See [[03 - BERT 2018]]
- **Entropy** — measure of uncertainty or information content. See [[15 - Entropy Cross-Entropy KL]]
- **Episodic memory** — memory of specific past events. See [[01 - Memory Types]]
- **Eval set** — held-out data for evaluating model performance.
- **Expert** — a subnetwork in a Mixture-of-Experts model. See [[15 - Mixture of Experts Transformer]]

## F

- **Feature** — an individual measurable property or learned representation.
- **Few-shot** — providing a few examples in the prompt. See [[04 - In-Context Learning]]
- **FFN** — Feed-Forward Network; the MLP sublayer in a Transformer. See [[05 - Feed-Forward Network Deep]]
- **Fine-tuning** — adapting a pretrained model to a specific task. See [[01 - LoRA]]
- **FlashAttention** — IO-aware exact attention. See [[08 - FlashAttention 2022]]
- **Float16 (FP16)** — 16-bit floating point; standard for LLM training.
- **Format validation** — checking that model output matches expected schema.
- **Foundation model** — a large pretrained model adapted to many tasks. See [[09 - Foundation Models/MOC]]

## G

- **Gate** — a multiplicative scaling factor (e.g., in LSTM, SwiGLU).
- **Gated attention** — attention combined with a gating mechanism.
- **GELU** — Gaussian Error Linear Unit; common activation function. See [[02 - Activation Functions]]
- **Generalization** — performing well on unseen data.
- **Generative model** — a model that produces new data (text, images).
- **Global attention** — tokens that attend to everything (Longformer). See [[18 - Longformer 2020]]
- **GPU** — Graphics Processing Unit; the workhorse of deep learning.
- **Gradient** — vector of partial derivatives; direction of steepest increase. See [[10 - Gradient and Chain Rule]]
- **Gradient checkpointing** — trading compute for memory by recomputing activations during backprop.
- **Gradient clipping** — limiting gradient magnitude to prevent instability. See [[14 - Learning Rate Schedules]]
- **GraphRAG** — RAG over a knowledge graph. See [[03 - Advanced RAG Patterns]]
- **Greedy decoding** — always picking the highest-probability token. See [[03 - Sampling Strategies]]
- **GRPO** — Group Relative Policy Optimization (DeepSeek). See [[12 - DeepSeek-R1 2025]]
- **GQA** — Grouped-Query Attention. See [[14 - GQA MQA MLA]]
- **Guardrail** — input/output filter for safety and policy. See [[04 - Guardrails]]

## H

- **Hallucination** — model produces fabricated information. See [[05 - Hallucination]]
- **HNSW** — Hierarchical Navigable Small World; popular vector index. See [[04 - Vector Memory Backends]]
- **Human-in-the-loop (HiTL)** — requiring human approval at certain agent steps. See [[03 - LangGraph]]
- **Hybrid search** — combining vector and keyword search. See [[02 - Chunking Hybrid Search Reranking]]
- **HyDE** — Hypothetical Document Embeddings; RAG query rewriting technique.

## I

- **In-context learning (ICL)** — learning from examples in the prompt. See [[04 - In-Context Learning]]
- **Induction head** — attention head that performs pattern completion. See [[01 - Mechanistic Interpretability]]
- **Inference** — running a trained model on inputs.
- **Instruction tuning** — fine-tuning on instruction-response pairs. See [[03 - Instruction Tuning and Chat Templates]]
- **IO-aware** — algorithm optimized for memory access patterns. See [[08 - FlashAttention 2022]]

## J-K

- **Jacobian** — matrix of all first-order partial derivatives. See [[11 - Jacobians and Hessians]]
- **KL divergence** — Kullback-Leibler divergence; measure of distribution difference. See [[15 - Entropy Cross-Entropy KL]]
- **Knowledge distillation** — training a smaller model to mimic a larger one.
- **Knowledge graph** — structured representation of entities and relationships.
- **KV cache** — cached keys/values for efficient autoregressive generation. See [[02 - KV Cache Mechanics]]

## L

- **Latent space** — the learned representation space.
- **LayerNorm** — layer normalization. See [[04 - Normalization Layers]]
- **Learning rate** — step size for gradient descent. See [[14 - Learning Rate Schedules]]
- **Linear attention** — attention approximated to be O(N). See [[13 - Linear Attention]]
- **Logit** — raw output of a model before softmax.
- **Logit lens** — applying the unembedding to intermediate activations. See [[02 - Logit Lens and Tuned Lens]]
- **Long context** — sequence lengths >8K tokens. See [[18 - Longformer 2020]]
- **LoRA** — Low-Rank Adaptation. See [[01 - LoRA]]
- **Loss function** — measure of prediction error. See [[15 - Entropy Cross-Entropy KL]]
- **Luong attention** — multiplicative (dot-product) attention. See [[13 - Luong Attention 2015]]

## M

- **Mamba** — selective state-space model. See [[11 - Mamba 2023]]
- **Masked Language Modeling (MLM)** — pretraining objective: predict masked tokens. See [[03 - BERT 2018]]
- **Matrix multiplication** — fundamental linear algebra operation. See [[04 - Matrix Multiplication]]
- **Maxout** — activation function taking the max over linear projections.
- **MCP** — Model Context Protocol. See [[01 - MCP Overview]]
- **MemGPT** — OS-inspired memory hierarchy for agents. See [[02 - MemGPT and Letta]]
- **Memory** — persistent state for agents. See [[01 - Memory Types]]
- **Mixture of Experts (MoE)** — conditional computation with expert subnetworks. See [[15 - Mixture of Experts Transformer]]
- **MLA** — Multi-head Latent Attention (DeepSeek). See [[14 - GQA MQA MLA]]
- **Model card** — documentation describing a model's capabilities, limitations, and intended use.
- **Model editing** — surgically modifying specific knowledge in a model. See [[04 - Activation Patching and Causal Tracing]]
- **Model registry** — versioned store for model artifacts. See [[03 - Model Registry and Versioning]]
- **Monosemantic** — a feature that represents a single concept. See [[03 - Sparse Autoencoders Deep Dive]]
- **MQA** — Multi-Query Attention. See [[14 - GQA MQA MLA]]
- **Multi-agent system** — multiple agents coordinating. See [[01 - Multi-Agent Architectures]]
- **Multi-head attention** — parallel attention heads. See [[05 - Multi-Head Attention]]
- **Multi-hop retrieval** — iterative retrieval for complex queries. See [[03 - Advanced RAG Patterns]]
- **Multimodal** — processing multiple modalities (text, image, audio). See [[01 - Multimodal AI Overview]]

## N

- **N-gram** — sequence of N consecutive tokens. See [[07 - N-gram Language Models]]
- **Neural network** — a model composed of layers of neurons.
- **Neuron** — a single unit in a neural network.
- **Next-token prediction** — pretraining objective: predict the next token. See [[01 - Decoder-Only Architecture]]
- **Normalization** — standardizing activations. See [[04 - Normalization Layers]]
- **NSP** — Next Sentence Prediction; BERT's auxiliary objective. See [[03 - BERT 2018]]

## O

- **Observability** — monitoring, logging, and tracing for production systems. See [[05 - Observability Stack]]
- **One-shot** — providing a single example in the prompt. See [[04 - In-Context Learning]]
- **Optimization** — finding model parameters that minimize loss. See [[12 - Optimization Essentials]]
- **Overfitting** — model learns training data too well, generalizes poorly.

## P

- **PagedAttention** — block-level KV cache management. See [[10 - PagedAttention vLLM 2023]]
- **Parameter** — a learnable weight in a model.
- **Perceptron** — the simplest neural network unit. See [[01 - Perceptrons and MLPs]]
- **Perplexity** — exponentiated cross-entropy; a language modeling metric. See [[08 - Perplexity]]
- **PGvector** — Postgres extension for vector storage. See [[02 - Vector Storage with pgvector]]
- **Positional encoding** — encoding token positions. See [[06 - Positional Encoding Overview]]
- **PPO** — Proximal Policy Optimization. See [[10 - PPO Deep Treatment]]
- **Pre-norm** — normalization before the sublayer (more stable than post-norm). See [[02 - Pre-Norm vs Post-Norm]]
- **Pretraining** — initial training on large unlabeled data. See [[01 - Pretraining Objectives and Scaling Laws]]
- **Prompt** — input to an LLM.
- **Prompt engineering** — crafting prompts for desired outputs. See [[02 - Prompt Management]]
- **Prompt injection** — adversarial input that overrides system instructions. See [[01 - LLM Security and Prompt Injection]]
- **Probing** — training a classifier on activations to test what they encode. See [[05 - Probing]]
- **PyTorch** — popular deep learning framework.

## Q

- **Q-K-V** — Query, Key, Value in attention. See [[04 - Self-Attention]]
- **QLoRA** — Quantized LoRA. See [[02 - QLoRA]]
- **Quantization** — reducing precision (e.g., FP16 → INT4) for efficiency. See [[03 - Quantization]]
- **Query rewriting** — transforming a user query for better retrieval.

## R

- **RAG** — Retrieval-Augmented Generation. See [[01 - RAG Pipeline Overview]]
- **Reasoning model** — model trained for multi-step reasoning (o1, R1). See [[09 - Foundation Models/Reasoning Models/03 - Reasoning Models]]
- **ReAct** — Reasoning + Acting pattern. See [[03 - ReAct Pattern]]
- **Recall** — fraction of relevant items retrieved.
- **Recurrent** — processing sequences step by step. See [[04 - RNN LSTM GRU]]
- **Reflexion** — agent pattern with self-critique. See [[05 - Reflection]]
- **Refusal** — model declines to answer.
- **Reinforcement Learning (RL)** — learning from reward signals. See [[07 - MDPs and Bellman Equations]]
- **Reranking** — re-scoring retrieved documents with a more expensive model. See [[02 - Chunking Hybrid Search Reranking]]
- **Residual connection** — skip connection that adds input to output. See [[03 - Residual Connections]]
- **Retrieval** — finding relevant documents for a query. See [[01 - RAG Pipeline Overview]]
- **Reward hacking** — model exploiting reward function flaws. See [[05 - RLHF with PPO]]
- **Reward model (RM)** — model that scores response quality. See [[07 - InstructGPT 2022]]
- **RLHF** — Reinforcement Learning from Human Feedback. See [[07 - InstructGPT 2022]]
- **RMSNorm** — Root Mean Square Normalization. See [[04 - Normalization Layers]]
- **RNN** — Recurrent Neural Network. See [[04 - RNN LSTM GRU]]
- **RoPE** — Rotary Position Embedding. See [[08 - RoPE]]
- **Router** — component that routes requests to appropriate models. See [[03 - Gateway and Router Patterns]]

## S

- **SAE** — Sparse Autoencoder. See [[03 - Sparse Autoencoders Deep Dive]]
- **Sampling** — selecting tokens from the probability distribution. See [[03 - Sampling Strategies]]
- **ScaleNorm** — normalization variant.
- **Scheduler** — component that manages request queueing and batching. See [[10 - PagedAttention vLLM 2023]]
- **Self-attention** — attention within a single sequence. See [[04 - Self-Attention]]
- **Semantic caching** — caching responses for semantically similar queries.
- **Semantic search** — search based on meaning, not keywords. See [[04 - Vector Memory Backends]]
- **Sentiment analysis** — classifying text by emotional tone.
- **Seq2Seq** — sequence-to-sequence model. See [[05 - Seq2Seq and the Information Bottleneck]]
- **Shadow deployment** — running new model in parallel without serving traffic. See [[07 - A-B Testing and Shadow Deployment]]
- **SFT** — Supervised Fine-Tuning. See [[03 - Instruction Tuning and Chat Templates]]
- **Sliding window attention** — local attention within a window. See [[15 - Sliding Window Attention]]
- **Softmax** — converts logits to probabilities. See [[04 - Self-Attention]]
- **Sparse attention** — attention restricted to a subset of tokens. See [[12 - Sparse Attention]]
- **Speculative decoding** — using a draft model to accelerate generation. See [[05 - Speculative Decoding]]
- **State Space Model (SSM)** — linear-time sequence model. See [[01 - SSMs Mamba and Frontiers]]
- **Steering** — modifying activations to control model behavior. See [[03 - Sparse Autoencoders Deep Dive]]
- **Stop sequence** — token that terminates generation.
- **Streaming** — returning output incrementally as it's generated.
- **Superposition** — model representing more features than dimensions. See [[03 - Sparse Autoencoders Deep Dive]]
- **Supervised learning** — learning from labeled data.
- **SwiGLU** — Swish-Gated Linear Unit; common FFN activation. See [[05 - Feed-Forward Network Deep]]
- **System prompt** — initial instructions defining the model's role.

## T

- **Temperature** — controls sampling randomness. See [[03 - Sampling Strategies]]
- **Tensor** — multi-dimensional array. See [[06 - Tensors and Broadcasting]]
- **Tensor parallelism** — splitting model layers across GPUs. See [[02 - Distributed Training]]
- **Test set** — held-out data for final evaluation.
- **TF-IDF** — Term Frequency-Inverse Document Frequency. See [[09 - TF-IDF]]
- **Token** — a unit of text (word, subword, or character).
- **Tokenization** — splitting text into tokens. See [[01 - Tokenization Overview]]
- **Top-k** — sampling from the top K tokens. See [[03 - Sampling Strategies]]
- **Top-p (nucleus)** — sampling from the smallest set of tokens with cumulative probability ≥ p. See [[03 - Sampling Strategies]]
- **Tool calling** — LLM invoking external tools. See [[04 - Function Calling]]
- **Trace** — distributed tracing for observability. See [[05 - Observability Stack]]
- **Training** — optimizing model parameters on data.
- **Transfer learning** — applying knowledge from one task to another.
- **Transformer** — the dominant neural architecture. See [[01 - Transformer Block]]
- **Trusted execution environment (TEE)** — secure area for running code.

## U

- **Underfitting** — model is too simple to capture the data.
- **Universal approximation** — neural networks can approximate any function. See [[01 - Perceptrons and MLPs]]
- **Unsupervised learning** — learning from unlabeled data.

## V

- **Value** — the output vector in attention. See [[04 - Self-Attention]]
- **Vanishing gradient** — gradients become too small to learn. See [[08 - Vanishing and Exploding Gradients]]
- **Vector** — a 1D tensor. See [[01 - Vectors]]
- **Vector database** — database for storing and searching vectors. See [[04 - Vector Memory Backends]]
- **Verifiable reward** — reward based on objective correctness (math, code). See [[12 - DeepSeek-R1 2025]]
- **ViT** — Vision Transformer. See [[21 - Vision Transformer ViT 2020]]
- **vLLM** — popular LLM serving engine. See [[07 - vLLM]]

## W

- **Warmup** — gradually increasing learning rate at training start. See [[14 - Learning Rate Schedules]]
- **Weight** — a learnable parameter in a model.
- **Weight decay** — L2 regularization on weights.
- **Word2Vec** — word embedding method. See [[05 - Word2Vec GloVe FastText]]
- **WordPiece** — tokenization method used by BERT. See [[03 - WordPiece]]

## X-Y-Z

- **XLNet** — generalized autoregressive pretraining.
- **YaRN** — Yet another RoPE extensioN. See [[10 - YaRN and NTK-aware Scaling]]
- **Zero-shot** — performing a task with no examples in the prompt. See [[04 - In-Context Learning]]
- **ZeRO** — Zero Redundancy Optimizer for distributed training. See [[02 - Distributed Training]]

## See Also

- [[28 - Glossary/MOC|Glossary MOC]]
- [[Acronyms Index]]
- [[MOC|Master Map of Content]]
