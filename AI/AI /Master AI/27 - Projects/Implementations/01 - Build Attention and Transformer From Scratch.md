---
tags: [projects, implementations, attention-from-scratch, transformer-from-scratch]
iteration: 12
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Build Attention From Scratch, Build Transformer From Scratch]
---

# 01 - Build Attention and Transformer From Scratch

> [!info] TL;DR
> The single highest-leverage learning project: implement scaled dot-product attention, then a Transformer block, then a tiny GPT — in pure PyTorch. You'll understand Transformers more deeply in 1 weekend than in months of reading.

## Why Build From Scratch?

Reading papers and using HuggingFace gives a surface-level understanding. Building from scratch forces you to confront every detail:
- Why scale by $\sqrt{d_k}$?
- How does causal masking actually work?
- What's the shape of every intermediate tensor?
- Where does the KV cache plug in?

After this project, every architectural decision in modern LLMs becomes clear.

## Project 1: Scaled Dot-Product Attention

Implement [[06 - Attention Mechanisms/Self-Attention/04 - Self-Attention|Self-Attention]] from scratch:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class SelfAttention(nn.Module):
    def __init__(self, d_model, d_k=None):
        super().__init__()
        d_k = d_k or d_model
        self.W_q = nn.Linear(d_model, d_k, bias=False)
        self.W_k = nn.Linear(d_model, d_k, bias=False)
        self.W_v = nn.Linear(d_model, d_k, bias=False)
        self.scale = d_k ** -0.5
    
    def forward(self, x, mask=None):
        # x: (B, T, d_model)
        Q = self.W_q(x)  # (B, T, d_k)
        K = self.W_k(x)
        V = self.W_v(x)
        
        scores = Q @ K.transpose(-2, -1) * self.scale  # (B, T, T)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        attn = F.softmax(scores, dim=-1)
        out = attn @ V  # (B, T, d_k)
        return out

# Test
B, T, D = 2, 5, 16
x = torch.randn(B, T, D)
attn = SelfAttention(D)
out = attn(x)
print(out.shape)  # (2, 5, 16)
```

### Verify
- Without mask: each output token is a blend of all input tokens.
- With causal mask: token $i$'s output only depends on tokens $\leq i$.

## Project 2: Multi-Head Attention

Extend to multiple heads (see [[06 - Attention Mechanisms/Multi-Head Attention/05 - Multi-Head Attention|Multi-Head Attention]]):

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, n_heads):
        super().__init__()
        assert d_model % n_heads == 0
        self.d_k = d_model // n_heads
        self.n_heads = n_heads
        self.W_qkv = nn.Linear(d_model, 3 * d_model, bias=False)
        self.W_o = nn.Linear(d_model, d_model, bias=False)
    
    def forward(self, x, mask=None):
        B, T, D = x.shape
        qkv = self.W_qkv(x)  # (B, T, 3D)
        q, k, v = qkv.split(D, dim=-1)
        q = q.view(B, T, self.n_heads, self.d_k).transpose(1, 2)  # (B, h, T, d_k)
        k = k.view(B, T, self.n_heads, self.d_k).transpose(1, 2)
        v = v.view(B, T, self.n_heads, self.d_k).transpose(1, 2)
        
        scores = (q @ k.transpose(-2, -1)) * (self.d_k ** -0.5)  # (B, h, T, T)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        attn = F.softmax(scores, dim=-1)
        out = attn @ v  # (B, h, T, d_k)
        out = out.transpose(1, 2).contiguous().view(B, T, D)
        return self.W_o(out)
```

## Project 3: Transformer Block

```python
class TransformerBlock(nn.Module):
    def __init__(self, d_model, n_heads, d_ff, dropout=0.1):
        super().__init__()
        self.norm1 = nn.LayerNorm(d_model)
        self.attn = MultiHeadAttention(d_model, n_heads)
        self.norm2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Linear(d_ff, d_model),
        )
        self.drop = nn.Dropout(dropout)
    
    def forward(self, x, mask=None):
        # Pre-norm residual
        x = x + self.drop(self.attn(self.norm1(x), mask=mask))
        x = x + self.drop(self.ffn(self.norm2(x)))
        return x
```

## Project 4: Tiny GPT

Put it all together:

```python
class TinyGPT(nn.Module):
    def __init__(self, vocab_size, d_model=128, n_heads=4, d_ff=512, n_layers=4, max_len=256):
        super().__init__()
        self.tok_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(max_len, d_model)
        self.blocks = nn.ModuleList([
            TransformerBlock(d_model, n_heads, d_ff) for _ in range(n_layers)
        ])
        self.norm = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, vocab_size, bias=False)
    
    def forward(self, tokens):
        B, T = tokens.shape
        pos = torch.arange(T, device=tokens.device).unsqueeze(0)
        x = self.tok_emb(tokens) + self.pos_emb(pos)
        
        # Causal mask
        mask = torch.tril(torch.ones(T, T, device=tokens.device))
        mask = mask.unsqueeze(0).unsqueeze(0)  # (1, 1, T, T)
        
        for block in self.blocks:
            x = block(x, mask=mask)
        x = self.norm(x)
        return self.head(x)

# Train on a small text corpus
model = TinyGPT(vocab_size=1000)
optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)

for step in range(10000):
    tokens = sample_batch()  # (B, T) ints
    logits = model(tokens)
    
    # Next-token prediction loss
    shift_logits = logits[..., :-1, :].contiguous()
    shift_labels = tokens[..., 1:].contiguous()
    loss = F.cross_entropy(shift_logits.view(-1, 1000), shift_labels.view(-1))
    
    optimizer.zero_grad()
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    optimizer.step()
    
    if step % 100 == 0:
        print(f"step {step}, loss {loss.item():.3f}")
```

## Project 5: Add Modern Features

Once basic GPT works:
1. Replace LayerNorm with RMSNorm.
2. Replace GELU FFN with SwiGLU.
3. Replace learned positional embeddings with RoPE.
4. Add GQA (grouped-query attention).
5. Add KV cache for inference.
6. Train on a real dataset (TinyStories, OpenWebText subset).

Each step teaches you a key architectural decision.

## Project 6: Add BERT

Encoder-only variant:
- Remove causal mask (bidirectional).
- Add `[CLS]` and `[SEP]` tokens.
- Train with MLM (mask 15% of tokens, predict them).

## Reference Implementations

- **nanoGPT** (Karpathy): https://github.com/karpathy/nanoGPT — minimal clean GPT in ~300 LOC.
- **minGPT**: predecessor to nanoGPT, even simpler.
- **llm.c** (Karpathy): GPT in C/CUDA.
- **tinygrad**: minimal framework, easy to read.

These are the gold standard. Read them line-by-line after you've built your own.

## Why This Matters for AI

- This single project transforms your understanding of LLMs. You'll never look at a model config the same way.
- It's the basis for everything else: BERT, GPT, ViT, MoE, FlashAttention all build on this foundation.
- For interviews, "I built GPT from scratch" is a strong signal of depth.

## Production Implications

- Don't ship your from-scratch implementation. Use HuggingFace / vLLM for production.
- But the understanding you gain will help you debug, optimize, and choose models correctly.
- Many production bugs (wrong mask, wrong shape, wrong scaling) are easy to spot once you've built these from scratch.

## Common Pitfalls

- **Forgetting the causal mask** — model "cheats" by looking ahead; training looks great but model is useless.
- **Wrong shift in loss** — predict current from current; loss is artificially low.
- **Wrong scaling** — without $\sqrt{d_k}$, training is unstable for larger $d_k$.
- **Forgetting `model.eval()`** — dropout is active during inference.
- **No gradient clipping** — training diverges around step 1000 without it.

## Further Reading

- Karpathy's "Let's build GPT from scratch" video (YouTube).
- Vaswani et al. (2017), *Attention Is All You Need*.
- The Annotated Transformer (Harvard NLP).

## See Also

- [[06 - Attention Mechanisms/Self-Attention/04 - Self-Attention|Self-Attention]]
- [[06 - Attention Mechanisms/Multi-Head Attention/05 - Multi-Head Attention|Multi-Head Attention]]
- [[07 - Transformers/Architecture/01 - Transformer Block|Transformer Block]]
- [[08 - LLMs/Architecture/01 - Decoder-Only Architecture|Decoder-Only Architecture]]
- [[27 - Projects/MOC|Projects MOC]]

## Production Hardening Checklist

1. **Use BF16 over FP16**: BF16 has FP32-equivalent dynamic range — no loss scaling needed. Mandatory for >1M param training.
2. **FlashAttention**: replace the naive `softmax(QK^T/sqrt(d))V` with `flash_attn_func` from `flash_attn` package — 2–4x speedup, 5–20x memory reduction. The math is identical; only the kernel changes.
3. **Pre-norm over post-norm**: modern Transformers (Llama, GPT-NeoX) use pre-norm (LayerNorm/RMSNorm before attention) — more stable training at depth.
4. **RMSNorm over LayerNorm**: no mean subtraction; no bias; ~10–20% faster; identical quality. Used by Llama, Mistral, Gemma.
5. **RoPE over sinusoidal**: rotary positional embeddings generalize better to longer contexts and support YaRN/NTK scaling.
6. **SwiGLU/GEGLU FFN**: replace ReLU/GELU FFN with SwiGLU (used by Llama, Mistral) — better quality at same param count.
7. **Gradient clipping at 1.0**: prevents loss spikes from destabilizing training.
8. **AdamW with cosine schedule + warmup**: 2000-step warmup → cosine decay to 10% of peak LR.
9. **Initialization**: GPT-2 style init for stability: `nn.init.normal_(module.weight, mean=0, std=0.02)`; scale residuals by `1/sqrt(2*N_layers)`.
10. **Causal mask**: don't forget the triangular mask in self-attention — without it, the model "cheats" by attending to future tokens.
11. **KV cache for inference**: cache K and V across generation steps to avoid recomputing them; essential for >32 token generation.
12. **Tied embeddings**: tie input and output embeddings (share weights) — saves parameters and improves quality for small models.
13. **Dropout**: 0.1 on residuals and attention weights during training; disable at inference.
14. **Checkpointing**: save every 500–1000 steps; keep last 3 + best by val loss.

## Common Failure Modes — Diagnostic Table

| Symptom                                | Likely Cause                                  | Fix                                                          |
|----------------------------------------|-----------------------------------------------|--------------------------------------------------------------|
| Loss plateaus immediately              | LR too high; or initialization wrong          | Lower LR 10x; check init std=0.02                            |
| Loss spikes to NaN                     | FP16 overflow; or attention not scaled        | Switch to BF16; verify `1/sqrt(d_k)` scaling                 |
| Loss decreases then explodes           | Gradient explosion                            | Add gradient clipping at 1.0                                 |
| Model produces garbage text            | Wrong tokenizer; or causal mask missing       | Verify tokenizer matches training; check mask in attention   |
| Training loss decreases but val rises  | Overfitting                                   | Add dropout; reduce model size; more data                    |
| Generation repeats same token          | Temperature too low; or no repetition penalty | Increase temperature to 0.7+; add repetition penalty 1.1     |
| Training 10x slower than expected      | Not using FlashAttention                      | Install `flash_attn`; replace attention call                 |
| OOM at seq_len=2048                    | Naive attention is O(N²) memory               | Use FlashAttention; or reduce seq_len; or use gradient checkpointing |
| Model can't generalize to longer ctx   | Sinusoidal pos encoding doesn't extrapolate   | Switch to RoPE; or apply YaRN/NTK scaling at inference       |
| Loss diverges after N steps            | LR schedule wrong (warmup too short)          | Increase warmup to 2000 steps                                |

## Modern Developments (2024–2026)

### FlashAttention-3 (2024)
FlashAttention-3 (Tri Dao, 2024) is the 2024 state-of-the-art attention kernel for Hopper (H100) GPUs. Key improvements over FA2: (1) async warp-specialization (overlap matmul and softmax), (2) FP8 support (2x throughput on H100), (3) better occupancy via two-stage softmax. FA3 is ~1.5–2x faster than FA2 on H100 and is the default in PyTorch 2.5+ and vLLM 0.6+. If you're implementing attention from scratch today, use FA3 (or FA2 on Ampere and older).

### RoPE with NTK-aware Scaling and YaRN
Modern long-context models extend RoPE via: (1) **NTK-aware scaling** — adjust the rotation base (default 10000) to a higher value (e.g., 1.5M for 1M-token context); (2) **YaRN** —分段 scaling that treats different frequency bands differently. Both let a model trained on 4k context work at 32k–1M context without retraining. Implementation: 3 lines of code change in the RoPE function. See [[06 - Attention Mechanisms/Positional Information/10 - YaRN and NTK-aware Scaling]].

### Grouped-Query Attention (GQA) and Multi-Head Latent Attention (MLA)
Modern LLMs (Llama 3, Mistral, Gemma) use GQA instead of MHA: K heads share V heads (e.g., 32 Q heads, 8 KV heads). Reduces KV cache size 4x with negligible quality loss. DeepSeek-V3 introduced MLA — compresses KV cache 4x further via low-rank projection. For from-scratch implementations, MHA is fine for learning; switch to GQA for production.

### Mixture-of-Experts Transformers
For models >10B params, sparse MoE (e.g., 8 experts, top-2 routing) achieves better quality-per-FLOP than dense. The transformer block changes: FFN is replaced with N parallel FFNs + a router. See [[27 - Projects/Implementations/04 - Build a Mini MoE]].

### torch.compile for Training
PyTorch 2.0+ `torch.compile()` fuses kernels and applies automatic optimizations. Wrap your model: `model = torch.compile(model)`. Typical speedup: 1.5–2x for training, 2–3x for inference. No code changes needed beyond the wrap.

## Worked Example — Generate Text with the Trained Model

```python
def generate(model, tokenizer, prompt: str, max_new_tokens: int = 100,
             temperature: float = 0.7, top_k: int = 50) -> str:
    """Autoregressive generation with top-k sampling."""
    model.eval()
    input_ids = tokenizer.encode(prompt, return_tensors='pt').to(model.device)
    
    with torch.no_grad():
        for _ in range(max_new_tokens):
            # Crop context to max_seq_len
            context = input_ids[:, -model.max_seq_len:]
            
            # Forward pass
            logits = model(context)  # (1, T, V)
            next_logits = logits[0, -1, :] / temperature  # (V,)
            
            # Top-k filtering
            if top_k > 0:
                top_k_logits, top_k_indices = torch.topk(next_logits, top_k)
                probs = F.softmax(top_k_logits, dim=-1)
                next_idx = top_k_indices[torch.multinomial(probs, num_samples=1)]
            else:
                probs = F.softmax(next_logits, dim=-1)
                next_idx = torch.multinomial(probs, num_samples=1)
            
            # Append and stop on EOS
            input_ids = torch.cat([input_ids, next_idx.unsqueeze(0)], dim=1)
            if next_idx.item() == tokenizer.eos_token_id:
                break
    
    return tokenizer.decode(input_ids[0])

# KV-cache version — 5-10x faster for long generations
def generate_with_kv_cache(model, tokenizer, prompt: str, max_new_tokens: int = 100) -> str:
    """Generation with KV cache — only computes the new token's K, V."""
    model.eval()
    input_ids = tokenizer.encode(prompt, return_tensors='pt').to(model.device)
    
    # Initial forward — populate KV cache
    with torch.no_grad():
        logits, kv_cache = model(input_ids, use_cache=True)
        next_idx = torch.argmax(logits[0, -1, :]).unsqueeze(0).unsqueeze(0)
        generated = [next_idx.item()]
        
        for _ in range(max_new_tokens - 1):
            # Forward only the new token — passes kv_cache
            logits, kv_cache = model(next_idx, use_cache=True, past_kv=kv_cache)
            next_idx = torch.argmax(logits[0, -1, :]).unsqueeze(0).unsqueeze(0)
            generated.append(next_idx.item())
            if next_idx.item() == tokenizer.eos_token_id:
                break
    
    return tokenizer.decode(generated)
```

## Interview Questions

1. **Q: Walk through the math of scaled dot-product attention. Why divide by √d_k?**
   A: Attention is `softmax(QK^T / √d_k) V`. Q and K are projected to dimension d_k. The dot product Q·K has variance proportional to d_k (sum of d_k independent products). For large d_k (e.g., 64), the raw dot product can reach magnitudes where softmax saturates (outputs ~0 or ~1, killing gradients). Dividing by √d_k normalizes the variance to 1, keeping softmax in its linear regime. Without it, training is unstable for d_k > 16.

2. **Q: Why multi-head attention instead of single-head with the same total dimension?**
   A: Multi-head attention lets the model attend to different things simultaneously — one head can track syntax, another coreference, another long-range dependencies. Empirically, head specialization emerges in trained models (see mechanistic interp papers). With same total compute (d_model=512 split into 8 heads of 64 vs 1 head of 512), MHA is strictly more expressive. Ablations show ~2–4% quality drop from removing multi-head structure.

3. **Q: Why pre-norm instead of post-norm?**
   A: Post-norm (original Transformer): `x = LayerNorm(x + Sublayer(x))`. Pre-norm (GPT-2, Llama): `x = x + Sublayer(LayerNorm(x))`. Pre-norm is more stable because the residual path is unmodified — gradients flow directly through the residual connections. Post-norm's LayerNorm on the residual can saturate at depth >20 layers. Pre-norm enables training 100+ layer Transformers; post-norm typically diverges beyond 20 layers without careful init.

4. **Q: Why is the FFN expansion ratio typically 4x?**
   A: The FFN `Linear(d_model, 4*d_model) → GELU → Linear(4*d_model, d_model)` expands then contracts. The 4x ratio is empirical — original Transformer paper used 4x, and most models follow. Larger ratios (8x, 16x) give slightly better quality but more parameters; SwiGLU models (Llama) often use ~2.67x to compensate for the extra gate projection. The FFN is where most of the model's parameters live (~2/3 of total), so the ratio matters for parameter efficiency.

5. **Q: How does RoPE work, and why is it better than sinusoidal?**
   A: RoPE rotates Q and K vectors in 2D subspaces by an angle θ_i that depends on position i. The dot product Q_i · K_j becomes a function of (i-j), giving relative position for free. Advantages over sinusoidal: (1) relative position is what matters for language; (2) extrapolates to longer contexts (with NTK/YaRN scaling); (3) no extra parameters. Sinusoidal adds position info to embeddings but the attention dot product doesn't naturally extract relative position.

6. **Q: Why tie input and output embeddings?**
   A: The input embedding (token → vector) and output projection (vector → logits) are dual operations. Tying them (sharing the weight matrix) saves V * d_model parameters (e.g., 50k * 4096 = 200M for Llama 7B, ~3% of total). Empirically, tying gives equal or slightly better quality — the model learns a single token representation. Untied embeddings sometimes help for very large models (>30B) but the benefit is marginal. Most production models tie.

## Connection to Other Concepts

- [[06 - Attention Mechanisms/Self-Attention/04 - Self-Attention]] — the core attention operation implemented here.
- [[06 - Attention Mechanisms/Multi-Head Attention/05 - Multi-Head Attention]] — the multi-head extension.
- [[06 - Attention Mechanisms/Positional Information/08 - RoPE]] — modern positional encoding.
- [[07 - Transformers/Architecture/01 - Transformer Block]] — the block structure implemented here.
- [[07 - Transformers/Architecture/02 - Pre-Norm vs Post-Norm]] — pre-norm choice.
- [[07 - Transformers/Architecture/03 - Residual Connections]] — why residuals enable depth.
- [[07 - Transformers/Components/04 - Normalization Layers]] — LayerNorm vs RMSNorm.
- [[07 - Transformers/Components/05 - Feed-Forward Network Deep]] — FFN design.
- [[08 - LLMs/Architecture/01 - Decoder-Only Architecture]] — the architecture this implements.
- [[08 - LLMs/Context and KV Cache/02 - KV Cache Mechanics]] — KV cache for inference.
- [[26 - Papers/Transformers/02 - Vaswani Attention Is All You Need 2017]] — the original paper.
- [[26 - Papers/Efficient Attention/08 - FlashAttention 2022]] — modern attention kernel.
- [[27 - Projects/Implementations/05 - Build a Tiny LLM Trainer]] — full training pipeline using this architecture.
- [[27 - Projects/Implementations/04 - Build a Mini MoE]] — MoE variant of this architecture.
