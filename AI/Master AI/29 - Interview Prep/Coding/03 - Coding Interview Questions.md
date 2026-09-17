---
tags: [interview, coding, implementation, pytorch]
iteration: 3
created: 2026-08-07
aliases: [Coding Interview, LLM Coding Interview, Implement Attention]
---

# 03 — Coding Interview Questions

> [!info] TL;DR
> LLM coding interviews test your ability to implement core components from scratch: attention, multi-head attention, RoPE, KV cache, sampling, and small training loops. The four most common questions are: implement scaled dot-product attention, implement multi-head attention, implement top-k/top-p sampling, and implement a KV cache. Each can be done in 20–50 lines of PyTorch and tests a specific conceptual understanding.

## How to Approach LLM Coding Interviews

Unlike algorithmic coding interviews (where the bottleneck is finding the right trick), LLM coding interviews test whether you can translate mathematical formulas into correct PyTorch code. The structure:

1. **Clarify the spec**: inputs, outputs, shapes, edge cases.
2. **Write the math**: state the formula you're implementing.
3. **Write the code**: clean, vectorized PyTorch.
4. **Test with a small example**: verify shapes and values.
5. **Discuss extensions**: causal masking, batched inputs, optimization.

Common mistakes:
- Forgetting the `1/sqrt(d_k)` scaling.
- Mixing up `Q @ K^T` (correct) with `Q^T @ K` (wrong).
- Wrong dimension for softmax (should be over the last dim, the key dimension).
- Forgetting causal masking for decoder attention.
- Inefficient implementations (Python loops instead of vectorized ops).

## Question 1: Implement Scaled Dot-Product Attention

### Spec
Implement `scaled_dot_product_attention(Q, K, V, mask=None)` where:
- `Q`: shape `(batch, ..., seq_q, d_k)`
- `K`: shape `(batch, ..., seq_k, d_k)`
- `V`: shape `(batch, ..., seq_k, d_v)`
- `mask`: optional, shape broadcastable to `(batch, ..., seq_q, seq_k)`
- Returns: shape `(batch, ..., seq_q, d_v)`

### Math
```
Attention(Q, K, V) = softmax(Q K^T / sqrt(d_k)) V
```

### Solution

```python
import torch
import torch.nn.functional as F
import math

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Scaled dot-product attention.
    
    Args:
        Q: (batch, ..., seq_q, d_k)
        K: (batch, ..., seq_k, d_k)
        V: (batch, ..., seq_k, d_v)
        mask: optional, broadcastable to (batch, ..., seq_q, seq_k)
            True or 1 = attend, False or 0 = masked out
    
    Returns:
        output: (batch, ..., seq_q, d_v)
        attention_weights: (batch, ..., seq_q, seq_k)
    """
    d_k = Q.shape[-1]
    
    # Compute attention scores
    # (batch, ..., seq_q, d_k) @ (batch, ..., d_k, seq_k) = (batch, ..., seq_q, seq_k)
    scores = Q @ K.transpose(-2, -1) / math.sqrt(d_k)
    
    # Apply mask (if provided)
    if mask is not None:
        # mask: True/1 = attend, False/0 = mask out
        # We set masked positions to -inf so softmax gives them 0
        scores = scores.masked_fill(~mask.bool() if mask.dtype == torch.bool else mask == 0, float('-inf'))
    
    # Softmax over the last dimension (keys)
    attention_weights = F.softmax(scores, dim=-1)
    
    # Weighted sum of values
    # (batch, ..., seq_q, seq_k) @ (batch, ..., seq_k, d_v) = (batch, ..., seq_q, d_v)
    output = attention_weights @ V
    
    return output, attention_weights
```

### Test

```python
# Test basic functionality
torch.manual_seed(42)
Q = torch.randn(1, 4, 8)  # batch=1, seq=4, d_k=8
K = torch.randn(1, 6, 8)  # seq_k=6
V = torch.randn(1, 6, 5)  # d_v=5

output, weights = scaled_dot_product_attention(Q, K, V)
assert output.shape == (1, 4, 5)
assert weights.shape == (1, 4, 6)
assert torch.allclose(weights.sum(dim=-1), torch.ones(1, 4))  # rows sum to 1

# Test with causal mask
seq_len = 4
causal_mask = torch.tril(torch.ones(seq_len, seq_len)).bool()
output_causal, weights_causal = scaled_dot_product_attention(Q[:, :4], K[:, :4], V[:, :4], mask=causal_mask)
# Upper triangle should be 0
assert torch.all(weights_causal[0, 0, 1, 0] == 0)  # position 1 cannot attend to position 0... wait, that's wrong
# Actually: position i can attend to positions 0..i (lower triangular)
# So weights[0, 1, 0] should be non-zero (position 1 attends to position 0)
# And weights[0, 0, 1] should be zero (position 0 cannot attend to position 1)
assert weights_causal[0, 0, 1] == 0  # position 0 cannot see position 1
print("All tests passed!")
```

### Extensions to Discuss

- **FlashAttention**: explain that this implementation materializes the `seq_q × seq_k` matrix, which is `O(N²)` memory. FlashAttention avoids this with tiling. See [[08 - FlashAttention 2022]].
- **Memory layout**: for efficiency, queries and keys should be in row-major order for the matmul. PyTorch handles this, but it matters for custom CUDA kernels.
- **Mask types**: boolean mask (most common), additive mask (for ALiBi), or float mask.

## Question 2: Implement Multi-Head Attention

### Spec
Implement `MultiHeadAttention` as a PyTorch module:
- Input: `x` of shape `(batch, seq_len, d_model)`
- Output: same shape
- Parameters: `W_Q`, `W_K`, `W_V`, `W_O` (all `d_model × d_model`)
- Number of heads: `h`

### Solution

```python
import torch
import torch.nn as nn

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model: int, num_heads: int):
        super().__init__()
        assert d_model % num_heads == 0, "d_model must be divisible by num_heads"
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads  # dimension per head
        
        # Combined QKV projection for efficiency
        self.qkv = nn.Linear(d_model, 3 * d_model, bias=False)
        # Output projection
        self.o = nn.Linear(d_model, d_model, bias=False)
    
    def forward(self, x, mask=None):
        """
        Args:
            x: (batch, seq_len, d_model)
            mask: optional, (batch, seq_len, seq_len) or broadcastable
        
        Returns:
            (batch, seq_len, d_model)
        """
        batch_size, seq_len, _ = x.shape
        
        # Project to Q, K, V in one matmul
        # (batch, seq_len, d_model) -> (batch, seq_len, 3*d_model)
        qkv = self.qkv(x)
        # Split into Q, K, V
        # Each: (batch, seq_len, d_model)
        Q, K, V = qkv.chunk(3, dim=-1)
        
        # Reshape for multi-head: (batch, seq_len, d_model) -> (batch, num_heads, seq_len, d_k)
        Q = Q.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        
        # Expand mask for heads if needed
        if mask is not None:
            # mask: (batch, seq_len, seq_len) -> (batch, 1, seq_len, seq_len) for broadcasting
            if mask.dim() == 3:
                mask = mask.unsqueeze(1)
        
        # Apply attention
        # output: (batch, num_heads, seq_len, d_k)
        output, _ = scaled_dot_product_attention(Q, K, V, mask=mask)
        
        # Concatenate heads: (batch, num_heads, seq_len, d_k) -> (batch, seq_len, d_model)
        output = output.transpose(1, 2).contiguous().view(batch_size, seq_len, self.d_model)
        
        # Output projection
        return self.o(output)
```

### Test

```python
# Test
torch.manual_seed(42)
mha = MultiHeadAttention(d_model=512, num_heads=8)
x = torch.randn(2, 10, 512)  # batch=2, seq=10, d_model=512
output = mha(x)
assert output.shape == (2, 10, 512)

# Test with causal mask
seq_len = 10
causal_mask = torch.tril(torch.ones(seq_len, seq_len)).bool()
output_causal = mha(x, mask=causal_mask)
assert output_causal.shape == (2, 10, 512)

# Count parameters
n_params = sum(p.numel() for p in mha.parameters())
assert n_params == 4 * 512 * 512  # 4 projections of d_model x d_model
print(f"Parameters: {n_params}")
print("All tests passed!")
```

### Extensions to Discuss

- **Combined QKV**: the `qkv` projection computes Q, K, V in one matmul, which is more efficient than three separate projections. This is the standard optimization.
- **GQA / MQA**: for Grouped-Query Attention, K and V have fewer heads than Q. Modify the reshape to share K, V across multiple Q heads. See [[14 - GQA MQA MLA]].
- **No bias**: modern LLMs typically omit bias in attention projections. The original Transformer used bias; Llama does not.
- **RoPE**: applied to Q and K after the projection, before the reshape. See Question 4.

## Question 3: Implement Top-k and Top-p (Nucleus) Sampling

### Spec
Implement `sample(logits, temperature=1.0, top_k=None, top_p=None)` that returns a sampled token index.

### Solution

```python
import torch
import torch.nn.functional as F

def sample(logits, temperature=1.0, top_k=None, top_p=None):
    """
    Sample a token from logits with temperature, top-k, and top-p.
    
    Args:
        logits: (vocab_size,) or (batch, vocab_size)
        temperature: scaling factor; higher = more random
        top_k: if set, only consider top-k tokens
        top_p: if set, only consider tokens in the nucleus (cumulative prob <= top_p)
    
    Returns:
        sampled token index (int or tensor)
    """
    if logits.dim() == 1:
        logits = logits.unsqueeze(0)
    
    # Apply temperature
    if temperature != 1.0:
        logits = logits / temperature
    
    # Apply top-k: keep only top-k tokens, set rest to -inf
    if top_k is not None and top_k > 0:
        top_k = min(top_k, logits.size(-1))
        # Get the k-th largest value
        kth_value = torch.topk(logits, top_k, dim=-1).values[:, -1:]
        # Set everything below k-th value to -inf
        logits = logits.masked_fill(logits < kth_value, float('-inf'))
    
    # Apply top-p (nucleus): keep the smallest set of tokens whose cumulative prob >= top_p
    if top_p is not None and 0 < top_p < 1:
        # Sort logits in descending order
        sorted_logits, sorted_indices = torch.sort(logits, descending=True, dim=-1)
        sorted_probs = F.softmax(sorted_logits, dim=-1)
        cumulative_probs = torch.cumsum(sorted_probs, dim=-1)
        
        # Find tokens to remove: those whose cumulative prob exceeds top_p
        # (but keep at least one token)
        sorted_indices_to_remove = cumulative_probs > top_p
        # Shift right: always keep the first token (highest prob)
        sorted_indices_to_remove[:, 1:] = sorted_indices_to_remove[:, :-1].clone()
        sorted_indices_to_remove[:, 0] = False
        
        # Scatter back to original indices
        indices_to_remove = sorted_indices_to_remove.scatter(
            -1, sorted_indices, sorted_indices_to_remove
        )
        logits = logits.masked_fill(indices_to_remove, float('-inf'))
    
    # Convert to probabilities
    probs = F.softmax(logits, dim=-1)
    
    # Sample
    if logits.size(0) == 1:
        return torch.multinomial(probs, num_samples=1).squeeze(0).item()
    else:
        return torch.multinomial(probs, num_samples=1).squeeze(-1)
```

### Test

```python
# Test
torch.manual_seed(42)

# Test temperature
logits = torch.tensor([1.0, 2.0, 3.0, 4.0])
# Without temperature, the highest logit dominates
samples = [sample(logits, temperature=0.1) for _ in range(10)]
assert all(s == 3 for s in samples)  # always picks index 3 (highest logit)

# With high temperature, distribution is more uniform
samples = [sample(logits, temperature=10.0) for _ in range(100)]
# Some samples should be different from 3
assert any(s != 3 for s in samples)

# Test top_k
logits = torch.tensor([1.0, 2.0, 3.0, 4.0, 5.0])
samples = [sample(logits, top_k=2) for _ in range(100)]
# Only indices 3 and 4 should be sampled
assert all(s in [3, 4] for s in samples)

# Test top_p
logits = torch.tensor([1.0, 1.0, 1.0, 1.0, 10.0])
samples = [sample(logits, top_p=0.9) for _ in range(100)]
# With top_p=0.9, the high logit (index 4) should dominate
assert sum(s == 4 for s in samples) > 90

print("All tests passed!")
```

### Extensions to Discuss

- **Greedy decoding**: temperature → 0 (or use `argmax`).
- **Beam search**: maintain top-B sequences, expand each, keep best. Not sampling but related.
- **Repetition penalty**: subtract a penalty from previously-seen tokens. The exact formula varies; the common one is `logits[t] = logits[t] / penalty if t in seen else logits[t]`.
- **Constrained decoding**: use a finite state machine or grammar to constrain valid next tokens. Useful for structured outputs (JSON, regex). See Outlines and Guidance libraries.

## Question 4: Implement RoPE (Rotary Position Embedding)

### Spec
Implement RoPE: rotate the Q and K vectors based on their position.

### Math
For position `m` and dimension pair `(2i, 2i+1)`:
```
q'_2i   = q_2i * cos(m * θ_i) - q_2i+1 * sin(m * θ_i)
q'_2i+1 = q_2i * sin(m * θ_i) + q_2i+1 * cos(m * θ_i)
```
where `θ_i = 10000^(-2i/d)`.

### Solution

```python
import torch
import torch.nn as nn
import math

def precompute_rope_frequencies(d_k: int, max_seq_len: int, base: float = 10000.0):
    """
    Precompute the rotation frequencies for RoPE.
    
    Returns:
        cos, sin: (max_seq_len, d_k / 2) each
    """
    # d_k must be even
    assert d_k % 2 == 0
    half_d = d_k // 2
    
    # Compute frequencies: theta_i = base^(-2i/d) for i in 0..d/2
    positions = torch.arange(max_seq_len).float()  # (max_seq_len,)
    frequencies = 1.0 / (base ** (torch.arange(0, d_k, 2).float() / d_k))  # (d_k / 2,)
    
    # Outer product: (max_seq_len, d_k / 2)
    angles = positions.unsqueeze(1) * frequencies.unsqueeze(0)
    
    return angles.cos(), angles.sin()


def apply_rope(x, cos, sin):
    """
    Apply RoPE to x.
    
    Args:
        x: (batch, num_heads, seq_len, d_k)
        cos, sin: (seq_len, d_k / 2)
    
    Returns:
        (batch, num_heads, seq_len, d_k)
    """
    seq_len = x.shape[-2]
    cos = cos[:seq_len].unsqueeze(0).unsqueeze(0)  # (1, 1, seq_len, d_k / 2)
    sin = sin[:seq_len].unsqueeze(0).unsqueeze(0)
    
    # Split x into even and odd indices
    x1 = x[..., 0::2]  # (batch, num_heads, seq_len, d_k / 2)
    x2 = x[..., 1::2]
    
    # Apply rotation
    rotated = torch.stack([
        x1 * cos - x2 * sin,
        x1 * sin + x2 * cos,
    ], dim=-1)
    
    # Interleave back
    return rotated.flatten(-2)


class RoPEAttention(nn.Module):
    def __init__(self, d_model: int, num_heads: int, max_seq_len: int = 4096):
        super().__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.qkv = nn.Linear(d_model, 3 * d_model, bias=False)
        self.o = nn.Linear(d_model, d_model, bias=False)
        
        # Precompute RoPE frequencies
        cos, sin = precompute_rope_frequencies(self.d_k, max_seq_len)
        self.register_buffer('rope_cos', cos, persistent=False)
        self.register_buffer('rope_sin', sin, persistent=False)
    
    def forward(self, x, mask=None):
        batch_size, seq_len, _ = x.shape
        
        qkv = self.qkv(x)
        Q, K, V = qkv.chunk(3, dim=-1)
        
        Q = Q.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        
        # Apply RoPE to Q and K (not V!)
        Q = apply_rope(Q, self.rope_cos, self.rope_sin)
        K = apply_rope(K, self.rope_cos, self.rope_sin)
        
        if mask is not None:
            if mask.dim() == 3:
                mask = mask.unsqueeze(1)
        
        output, _ = scaled_dot_product_attention(Q, K, V, mask=mask)
        output = output.transpose(1, 2).contiguous().view(batch_size, seq_len, self.d_model)
        return self.o(output)
```

### Test

```python
# Test
torch.manual_seed(42)
attn = RoPEAttention(d_model=64, num_heads=8, max_seq_len=128)
x = torch.randn(2, 10, 64)
output = attn(x)
assert output.shape == (2, 10, 64)

# Verify RoPE is applied (compare with and without)
# RoPE should change the attention pattern based on relative position
print("All tests passed!")
```

### Extensions to Discuss

- **Length extrapolation**: RoPE does not extrapolate well beyond the training length. Techniques like NTK-aware scaling and YaRN extend it. See [[10 - YaRN and NTK-aware Scaling]].
- **Implementation efficiency**: the interleaved version above is clear but slow. The "half-rotation" version (rotate the first and second halves of the vector) is mathematically equivalent and faster on GPU. See the Llama implementation.
- **V is not rotated**: only Q and K are rotated, because the rotation is about encoding *relative* position in the dot product `Q · K`. V is the output, not a position-encoded representation.

## General Tips

### Know the Shapes
For every line of code, know the shape of every tensor. Most bugs in attention implementations are shape errors. Write the shapes as comments.

### Vectorize
Avoid Python loops over sequence positions or heads. Use `torch.bmm`, `torch.matmul`, einsum, or reshape + broadcast. Loops are 10–100× slower.

### Use `math.sqrt`, Not `** 0.5`
For scalar square roots, `math.sqrt` is clearer. For tensor square roots, use `torch.sqrt(x)` or `x.sqrt()`.

### Test with Small Examples
Always write a test that verifies the output shape and a simple property (e.g., attention weights sum to 1).

### Discuss the Math
Interviewers want to see you understand the formula, not just memorize the code. Write the formula in a comment before implementing.

## See Also

- [[01 - Conceptual Interview Questions]]
- [[02 - System Design Interview Questions]]
- [[29 - Interview Prep/MOC|29 Interview Prep MOC]]
- [[04 - Self-Attention]]
- [[05 - Multi-Head Attention]]
- [[08 - RoPE]]
- [[01 - Build Attention and Transformer From Scratch]]
