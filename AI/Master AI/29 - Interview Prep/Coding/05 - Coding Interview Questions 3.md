---
tags: [interview, coding, attention, rope, gqa, kv-cache, spec-decoding, quantization]
iteration: 13
created: 2026-08-08
last_updated: 2026-08-08
aliases: [Coding Interview Questions 3, Advanced Coding Q&A, YaRN GQA RoPE Coding]
---

# 07 - Coding Interview Questions (Part 3)

> [!info] TL;DR
> Companion to [[29 - Interview Prep/Coding/03 - Coding Interview Questions]] and [[29 - Interview Prep/Coding/04 - Coding Interview Questions 2]] — covers coding questions for new topics introduced in iterations 10–13: YaRN, GQA, RoPE scaling, KV cache compression, EAGLE-2 spec decoding, GPTQ quantization. Each question is a "implement from scratch" exercise that tests deep understanding.

## YaRN (Yet another RoPE extensioN)

### Q: Implement YaRN position interpolation for extending RoPE to longer contexts.

```python
import torch

def yarn_rope(
    position_ids: torch.Tensor,  # (batch, seq_len)
    dim: int,  # head dim, must be even
    base: float = 10000.0,
    original_max_position: int = 4096,
    target_max_position: int = 131072,  # 32x extension
    beta_fast: float = 32.0,
    beta_slow: float = 1.0,
    scale: float = 1.0,
):
    """YaRN: non-uniform RoPE interpolation.

    High-frequency components are interpolated more aggressively;
    low-frequency components are interpolated less.
    """
    # Compute frequencies
    inv_freq = 1.0 / (base ** (torch.arange(0, dim, 2).float() / dim))

    # Find the wavelength of each frequency
    # High frequency = low wavelength = "local" position info
    # Low frequency = high wavelength = "global" position info
    def find_correction_dim(num_rotations: float, dim: int, base: float, max_position: int) -> float:
        return (dim * torch.log(base / (num_rotations * 2 * torch.pi))) / (2 * torch.log(base))

    # Dimensions where each frequency transitions from "local" to "global"
    low_freq_cutoff = find_correction_dim(beta_fast, dim, base, original_max_position)
    high_freq_cutoff = find_correction_dim(beta_slow, dim, base, original_max_position)
    low_freq_cutoff = max(low_freq_cutoff, 0)
    high_freq_cutoff = min(high_freq_cutoff, dim - 1)

    # Compute the interpolation factor for each frequency
    # High frequencies (above low_freq_cutoff): interpolate aggressively
    # Low frequencies (below high_freq_cutoff): interpolate less
    # Middle: smooth transition
    extension_ratio = target_max_position / original_max_position

    def get_interpolation_factor(freq_idx: int) -> float:
        if freq_idx < low_freq_cutoff:
            # High frequency: aggressive interpolation
            return 1.0 / extension_ratio
        elif freq_idx > high_freq_cutoff:
            # Low frequency: no interpolation (keep original)
            return 1.0
        else:
            # Smooth transition
            return 1.0 - (1.0 / extension_ratio) * (freq_idx - low_freq_cutoff) / (high_freq_cutoff - low_freq_cutoff)

    # Apply per-frequency interpolation
    interpolation_factors = torch.tensor([get_interpolation_factor(i) for i in range(dim // 2)])

    # Compute rotated frequencies
    position_ids = position_ids.float()
    freqs = position_ids.unsqueeze(-1) * inv_freq  # (batch, seq, dim//2)
    # Apply interpolation: scale position by interpolation factor for each frequency
    freqs = freqs * interpolation_factors  # (batch, seq, dim//2)

    # Compute cos and sin
    emb = torch.cat([freqs, freqs], dim=-1)  # (batch, seq, dim)
    cos = emb.cos() * scale
    sin = emb.sin() * scale
    return cos, sin


# Test
position_ids = torch.arange(0, 8192).unsqueeze(0)  # batch=1, seq=8192
cos, sin = yarn_rope(position_ids, dim=128, original_max_position=4096, target_max_position=131072)
print(f"cos shape: {cos.shape}")  # (1, 8192, 128)
```

**Key points**: YaRN's insight is that high-frequency RoPE components encode local position (less affected by length extension) while low-frequency components encode global position (more affected). Non-uniform interpolation gives better extrapolation than uniform NTK scaling. Used by Llama 3.1 to extend from 8K to 128K. See [[06 - Attention Mechanisms/Positional Information/10 - YaRN and NTK-aware Scaling]].

## GQA (Grouped-Query Attention)

### Q: Implement GQA and explain the trade-off vs MHA and MQA.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class GQA(nn.Module):
    """Grouped-Query Attention.

    - MHA: num_kv_heads = num_heads (1:1)
    - MQA: num_kv_heads = 1 (all heads share KV)
    - GQA: num_kv_heads = num_heads // group_size (groups of heads share KV)

    GQA is the default for modern LLMs (Llama 3, Mistral, Qwen).
    """

    def __init__(self, hidden_dim: int, num_heads: int, num_kv_heads: int):
        super().__init__()
        assert num_heads % num_kv_heads == 0, "num_heads must be divisible by num_kv_heads"
        self.hidden_dim = hidden_dim
        self.num_heads = num_heads
        self.num_kv_heads = num_kv_heads
        self.head_dim = hidden_dim // num_heads
        self.group_size = num_heads // num_kv_heads  # how many query heads share each KV head

        # Q has full heads; K/V have num_kv_heads
        self.q_proj = nn.Linear(hidden_dim, num_heads * self.head_dim, bias=False)
        self.k_proj = nn.Linear(hidden_dim, num_kv_heads * self.head_dim, bias=False)
        self.v_proj = nn.Linear(hidden_dim, num_kv_heads * self.head_dim, bias=False)
        self.o_proj = nn.Linear(num_heads * self.head_dim, hidden_dim, bias=False)

    def forward(self, x: torch.Tensor, causal: bool = True) -> torch.Tensor:
        # x: (batch, seq_len, hidden_dim)
        batch, seq_len, _ = x.shape

        # Project
        q = self.q_proj(x).view(batch, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(x).view(batch, seq_len, self.num_kv_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(x).view(batch, seq_len, self.num_kv_heads, self.head_dim).transpose(1, 2)

        # Repeat KV heads to match Q heads
        # Each KV head is shared by self.group_size Q heads
        k = k.repeat_interleave(self.group_size, dim=1)  # (batch, num_heads, seq_len, head_dim)
        v = v.repeat_interleave(self.group_size, dim=1)

        # Scaled dot-product attention
        scores = q @ k.transpose(-2, -1) / math.sqrt(self.head_dim)  # (batch, num_heads, seq_len, seq_len)

        if causal:
            # Causal mask
            mask = torch.triu(torch.ones(seq_len, seq_len, dtype=torch.bool, device=x.device), diagonal=1)
            scores = scores.masked_fill(mask, float("-inf"))

        attn = F.softmax(scores, dim=-1)
        out = attn @ v  # (batch, num_heads, seq_len, head_dim)

        # Reshape and project
        out = out.transpose(1, 2).contiguous().view(batch, seq_len, self.num_heads * self.head_dim)
        return self.o_proj(out)


# Compare KV cache sizes
def kv_cache_size(num_layers: int, seq_len: int, num_kv_heads: int, head_dim: int, batch_size: int = 1, dtype_bytes: int = 2) -> int:
    """Compute KV cache size in bytes."""
    return num_layers * batch_size * seq_len * num_kv_heads * head_dim * 2 * dtype_bytes  # 2 for K and V

# Llama 3 8B: MHA vs GQA
# MHA (32 heads): 32 * 128 * 8192 * 2 * 2 = 67MB
# GQA (8 kv heads): 8 * 128 * 8192 * 2 * 2 = 17MB
# 4x reduction in KV cache

print("MHA KV cache at 8K context:", kv_cache_size(32, 8192, 32, 128), "bytes")
print("GQA KV cache at 8K context:", kv_cache_size(32, 8192, 8, 128), "bytes")
print("Ratio: 4x reduction")
```

**Key points**: GQA reduces KV cache by group_size× (typically 4–8×). Trade-off: slight quality loss (~0.5–1% on MMLU). Modern LLMs use 4–8 KV heads for 7–70B models. MQA (1 KV head) is too aggressive; quality drops noticeably. See [[06 - Attention Mechanisms/Modern Attention/14 - GQA MQA MLA]].

## RoPE Scaling for Long Context

### Q: Implement RoPE with NTK-aware scaling for length extrapolation.

```python
import torch

def ntk_aware_rope(
    position_ids: torch.Tensor,
    dim: int,
    base: float = 10000.0,
    scaling_factor: float = 4.0,  # extend to 4x training length
):
    """NTK-aware RoPE scaling.

    Instead of interpolating positions (YaRN), NTK-aware scaling adjusts the base frequency.
    Higher base = lower frequencies = better long-context extrapolation.

    NTK formula: new_base = base * scaling_factor ** (dim / (dim - 2))
    """
    # Compute new base
    new_base = base * (scaling_factor ** (dim / (dim - 2)))

    # Compute frequencies with new base
    inv_freq = 1.0 / (new_base ** (torch.arange(0, dim, 2).float() / dim))

    # Compute angles
    position_ids = position_ids.float()
    freqs = position_ids.unsqueeze(-1) * inv_freq  # (batch, seq, dim//2)

    # Compute cos and sin
    emb = torch.cat([freqs, freqs], dim=-1)
    cos = emb.cos()
    sin = emb.sin()
    return cos, sin


# Apply RoPE to Q and K
def apply_rope(q: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
    """Apply RoPE rotation to queries or keys.

    q: (batch, num_heads, seq_len, head_dim)
    cos, sin: (batch, seq_len, head_dim)
    """
    # Split q into two halves
    q1 = q[..., : q.shape[-1] // 2]
    q2 = q[..., q.shape[-1] // 2 :]

    # Reshape cos/sin for broadcasting
    cos = cos.unsqueeze(1)  # (batch, 1, seq_len, head_dim // 2)
    sin = sin.unsqueeze(1)

    # Rotation: rotate (q1, q2) by angle theta
    rotated_q1 = q1 * cos - q2 * sin
    rotated_q2 = q1 * sin + q2 * cos

    return torch.cat([rotated_q1, rotated_q2], dim=-1)
```

**Key points**: NTK-aware scaling is simpler than YaRN (just changes base frequency) and works well for moderate extensions (4–8×). YaRN is better for larger extensions (32×+). Both are used in production: Llama 3.1 405B uses YaRN; smaller models often use NTK. See [[06 - Attention Mechanisms/Positional Information/10 - YaRN and NTK-aware Scaling]].

## KV Cache Compression

### Q: Implement a simple KV cache eviction policy for long-context inference.

```python
import torch
from collections import deque
from typing import Optional

class EvictionKVCache:
    """KV cache with eviction policy for long-context inference.

    Eviction strategies:
    - 'fifo': evict oldest tokens (simplest)
    - 'least_attention': evict tokens with lowest cumulative attention
    - 'recent_window': keep last N tokens, evict older

    Trade-off: smaller cache = less memory but lower quality on long-context retrieval.
    """

    def __init__(
        self,
        max_cache_size: int,  # max number of tokens to cache
        head_dim: int,
        num_kv_heads: int,
        num_layers: int,
        eviction_strategy: str = "recent_window",
        recent_window: int = 1024,  # for 'recent_window' strategy
    ):
        self.max_cache_size = max_cache_size
        self.head_dim = head_dim
        self.num_kv_heads = num_kv_heads
        self.num_layers = num_layers
        self.eviction_strategy = eviction_strategy
        self.recent_window = recent_window

        # Initialize cache
        self.keys = [None] * num_layers  # list of (batch, num_kv_heads, seq, head_dim)
        self.values = [None] * num_layers
        self.attention_scores = [None] * num_layers  # cumulative attention for 'least_attention'
        self.token_positions = deque()  # FIFO of token positions

    def update(
        self,
        new_keys: list,  # list of (batch, num_kv_heads, new_seq, head_dim) per layer
        new_values: list,
    ):
        """Add new K/V to cache; evict if necessary."""
        for layer_idx in range(self.num_layers):
            if self.keys[layer_idx] is None:
                self.keys[layer_idx] = new_keys[layer_idx]
                self.values[layer_idx] = new_values[layer_idx]
            else:
                self.keys[layer_idx] = torch.cat([self.keys[layer_idx], new_keys[layer_idx]], dim=2)
                self.values[layer_idx] = torch.cat([self.values[layer_idx], new_values[layer_idx]], dim=2)

        # Track positions
        new_tokens = new_keys[0].shape[2]
        for i in range(new_tokens):
            self.token_positions.append(len(self.token_positions))

        # Evict if over capacity
        current_size = self.keys[0].shape[2]
        if current_size > self.max_cache_size:
            self._evict(current_size - self.max_cache_size)

    def _evict(self, n_to_evict: int):
        """Evict n_to_evict tokens from cache."""
        if self.eviction_strategy == "fifo":
            # Evict oldest
            for layer_idx in range(self.num_layers):
                self.keys[layer_idx] = self.keys[layer_idx][:, :, n_to_evict:, :]
                self.values[layer_idx] = self.values[layer_idx][:, :, n_to_evict:, :]
            for _ in range(n_to_evict):
                self.token_positions.popleft()

        elif self.eviction_strategy == "recent_window":
            # Keep last recent_window tokens + most-attended older tokens
            # Simplest version: just keep last recent_window tokens
            for layer_idx in range(self.num_layers):
                self.keys[layer_idx] = self.keys[layer_idx][:, :, -self.recent_window:, :]
                self.values[layer_idx] = self.values[layer_idx][:, :, -self.recent_window:, :]
            # Update positions
            while len(self.token_positions) > self.recent_window:
                self.token_positions.popleft()

        elif self.eviction_strategy == "least_attention":
            # Evict tokens with lowest cumulative attention
            # Requires tracking attention scores (complex; omitted for brevity)
            raise NotImplementedError("See H2O: Heavy-Hitter Oracle paper")

    def get(self) -> tuple:
        return self.keys, self.values


# Test
cache = EvictionKVCache(
    max_cache_size=4096,  # cache up to 4096 tokens
    head_dim=128, num_kv_heads=8, num_layers=32,
    eviction_strategy="recent_window", recent_window=2048,
)
# Simulate adding tokens
batch_size = 1
for step in range(100):
    new_k = [torch.randn(batch_size, 8, 100, 128) for _ in range(32)]
    new_v = [torch.randn(batch_size, 8, 100, 128) for _ in range(32)]
    cache.update(new_k, new_v)

keys, values = cache.get()
print(f"Final cache size: {keys[0].shape[2]} tokens (target: 4096)")
# With recent_window=2048, cache stays at 2048 once exceeded
```

**Key points**: KV cache compression is essential for long-context serving. Common strategies: (1) recent window (keep last N tokens), (2) attention-based eviction (H2O — keep tokens with high cumulative attention), (3) token merging (combine similar tokens), (4) low-rank compression (MLA in DeepSeek-V3). Trade-off: smaller cache = lower quality on retrieval. See [[08 - LLMs/Context and KV Cache/02 - KV Cache Mechanics]].

## EAGLE-2 Speculative Decoding

### Q: Implement a simple EAGLE-2-style speculative decoding loop.

```python
import torch
import torch.nn.functional as F

def eagle2_speculative_decode(
    target_model,
    draft_model,
    input_ids: torch.Tensor,  # (batch, seq_len)
    max_new_tokens: int = 100,
    K: int = 4,  # speculation depth
    top_k_tree: int = 8,  # tree width per step
    temperature: float = 0.0,
):
    """EAGLE-2 spec decoding: draft model proposes K tokens, target model verifies in one forward pass.

    Key insight: predict HIDDEN STATES (not tokens), use target model's vocab head to decode.
    Tree-structured speculation: propose multiple candidate continuations, verify all in one pass.
    """
    batch_size = input_ids.shape[0]
    generated = input_ids.clone()

    while generated.shape[1] - input_ids.shape[1] < max_new_tokens:
        # === Step 1: Draft model proposes K tokens ===
        # Get hidden state from target model (one forward pass)
        with torch.no_grad():
            target_outputs = target_model(generated, output_hidden_states=True)
            target_hidden = target_outputs.hidden_states[-1][:, -1:, :]  # (batch, 1, hidden_dim)

        # Draft model predicts next K hidden states (chained)
        draft_hidden = target_hidden
        draft_tokens = []
        draft_probs = []
        for k in range(K):
            # Draft model: takes hidden state, predicts next hidden state + token
            draft_out = draft_model(draft_hidden)
            next_hidden = draft_out.hidden_states  # predicted next hidden state
            next_logits = target_model.lm_head(next_hidden)  # use target's vocab head
            next_probs = F.softmax(next_logits, dim=-1)

            # Sample top-k candidate tokens for tree
            topk_probs, topk_tokens = torch.topk(next_probs, top_k_tree, dim=-1)
            # For simplicity, take argmax (in production, build full tree)
            next_token = topk_tokens[:, :, 0]  # (batch, 1)
            draft_tokens.append(next_token)
            draft_probs.append(topk_probs[:, :, 0])

            draft_hidden = next_hidden  # chain

        # === Step 2: Target model verifies all K drafted tokens in ONE forward pass ===
        # Construct verification input: original + drafted tokens
        drafted_seq = torch.cat([generated] + draft_tokens, dim=1)  # (batch, seq + K)

        with torch.no_grad():
            verify_outputs = target_model(drafted_seq)
            verify_logits = verify_outputs.logits  # (batch, seq + K, vocab)

        # === Step 3: Accept longest matching prefix ===
        # For each drafted position, check if target model would have produced the same token
        n_accepted = 0
        for k in range(K):
            # Target model's prediction at position (seq + k - 1) is for token at position (seq + k)
            target_pos = generated.shape[1] + k - 1
            target_probs = F.softmax(verify_logits[:, target_pos, :], dim=-1)

            drafted_token = draft_tokens[k]
            target_prob_of_drafted = target_probs[:, drafted_token[:, 0]].squeeze(-1)

            # Rejection sampling: accept with probability min(1, P_target / P_draft)
            # If temperature=0 (greedy), accept if drafted == argmax(target)
            if temperature == 0:
                target_argmax = target_probs.argmax(dim=-1)
                if target_argmax.item() == drafted_token.item():
                    n_accepted += 1
                else:
                    break
            else:
                # Stochastic acceptance
                P_draft = draft_probs[k].squeeze(-1)
                accept_prob = torch.min(torch.ones_like(target_prob_of_drafted), target_prob_of_drafted / P_draft)
                if torch.rand(1).item() < accept_prob.item():
                    n_accepted += 1
                else:
                    # Resample from corrected distribution
                    corrected_probs = torch.clamp(target_probs - P_draft, min=0)
                    corrected_probs = corrected_probs / corrected_probs.sum(dim=-1, keepdim=True)
                    resampled = torch.multinomial(corrected_probs, 1)
                    generated = torch.cat([generated, resampled], dim=1)
                    break

        # Append accepted tokens
        accepted_tokens = torch.cat(draft_tokens[:n_accepted], dim=1) if n_accepted > 0 else None
        if accepted_tokens is not None:
            generated = torch.cat([generated, accepted_tokens], dim=1)

        # If we rejected everything, append target's next token (standard autoregressive step)
        if n_accepted == 0 and temperature == 0:
            target_pos = generated.shape[1] - 1
            target_next = verify_logits[:, target_pos, :].argmax(dim=-1, keepdim=True)
            generated = torch.cat([generated, target_next], dim=1)

    return generated


# Performance analysis
"""
EAGLE-2 vs vanilla:
- Vanilla: 1 forward pass per token. For 100 tokens, 100 forward passes.
- EAGLE-2 (K=4, 90% acceptance): ~25 forward passes (each accepts ~4 tokens).
- Speedup: 4x.

EAGLE-2's key insight: predict HIDDEN STATES (smoother, more predictable than tokens),
use target model's vocab head to decode. This ensures distribution alignment.
"""
```

**Key points**: EAGLE-2's two innovations: (1) predict hidden states (not tokens) — smoother, more predictable; (2) dynamic trees — multiple candidate continuations verified in one pass. Combined: 85–95% acceptance rate, 3.5–4.5× speedup. EAGLE-3 adds confidence-aware scheduling (4–6× speedup). See [[26 - Papers/Efficient Attention/49 - Medusa and EAGLE 2024]] and [[26 - Papers/Efficient Attention/51 - EAGLE-3 2025]].

## GPTQ Quantization

### Q: Implement a simplified GPTQ-style INT4 quantization.

```python
import torch
import torch.nn as nn

def gptq_quantize(
    weight: torch.Tensor,  # (out_features, in_features)
    calibration_data: torch.Tensor,  # (n_samples, in_features) - sample inputs
    bits: int = 4,
    group_size: int = 128,  # group quantization
):
    """Simplified GPTQ: post-training INT4 quantization using Hessian information.

    Full GPTQ: quantizes weights column-by-column, updating remaining weights
    to compensate for quantization error. Uses Hessian (X^T X) as importance.

    This simplified version: just group-wise symmetric quantization with Hessian-based scaling.
    """
    out_features, in_features = weight.shape

    # Compute Hessian: H = X^T X (averaged over samples)
    # This is the "importance" of each input feature
    hessian = (calibration_data.T @ calibration_data) / calibration_data.shape[0]  # (in_features, in_features)
    hessian_diag = torch.diag(hessian)  # importance per input feature

    # Group-wise quantization
    n_groups = in_features // group_size
    quantized_weight = torch.zeros_like(weight)
    scales = torch.zeros(n_groups, out_features)
    zeros = torch.zeros(n_groups, out_features)

    for g in range(n_groups):
        start = g * group_size
        end = (g + 1) * group_size

        # Get weight slice for this group
        w_slice = weight[:, start:end]  # (out_features, group_size)

        # Compute scale and zero per output channel within group
        # Scale: max absolute value / (2^(bits-1) - 1)
        max_abs = w_slice.abs().amax(dim=-1, keepdim=True)  # (out_features, 1)
        scale = max_abs / (2 ** (bits - 1) - 1)
        zero = 2 ** (bits - 1) - 1  # symmetric

        # Quantize: round to nearest integer
        q = torch.round(w_slice / scale).clamp(-2 ** (bits - 1), 2 ** (bits - 1) - 1)
        # Dequantize (for error compensation)
        w_dequant = q * scale

        # Error compensation: GPTQ updates remaining weights to compensate
        # Simplified version: just use the quantized weight directly
        # Full GPTQ: uses Hessian to update weights to the right of current column
        # (omitted here for brevity)

        quantized_weight[:, start:end] = q  # store INT4 values (will pack in production)
        scales[g] = scale.squeeze(-1)
        zeros[g] = zero

    return quantized_weight, scales, zeros


# Test: quantize a linear layer
linear = nn.Linear(4096, 4096, bias=False)
# Generate calibration data
cal_data = torch.randn(128, 4096)

quantized_weight, scales, zeros = gptq_quantize(
    linear.weight.data, cal_data, bits=4, group_size=128
)

# Verify size reduction
print(f"Original weight: {linear.weight.element_size() * linear.weight.numel() / 1e6:.1f} MB (FP32)")
print(f"Quantized weight: {quantized_weight.element_size() * quantized_weight.numel() / 1e6:.1f} MB (simulated)")
print(f"In production (packed INT4): {0.5 * 4096 * 4096 / 1e6:.1f} MB")
print(f"Scales overhead: {scales.element_size() * scales.numel() / 1e6:.1f} MB")


# Quality test: compare output
test_input = torch.randn(1, 4096)
original_output = linear(test_input)

# Simulate dequantized forward pass
dequant_weight = quantized_weight * scales.repeat_interleave(128, dim=0).T
quantized_output = test_input @ dequant_weight.T

mse = F.mse_loss(original_output, quantized_output)
print(f"MSE between original and quantized: {mse.item():.6f}")
print(f"Relative error: {(mse / original_output.var()).item() * 100:.2f}%")
```

**Key points**: GPTQ uses Hessian information to quantize weights intelligently. The full algorithm quantizes column-by-column, updating remaining weights to compensate for each column's quantization error. The simplified version above shows the basic idea; production GPTQ adds the error compensation step. Quality: ~1–2% loss on MMLU for INT4. AWQ is a similar approach (activation-aware). See [[13 - Inference/Quantization/03 - Quantization]].

## How to Use This Note

For each question:
1. Try to implement without looking at the solution.
2. Compare your implementation to the solution above.
3. Run the test code; verify it works.
4. Read the linked concept note for the underlying theory.
5. Practice explaining your implementation out loud — interview coding is about communication as much as correctness.

## See Also

- [[29 - Interview Prep/MOC|Interview Prep MOC]]
- [[29 - Interview Prep/Coding/03 - Coding Interview Questions]] — part 1.
- [[29 - Interview Prep/Coding/04 - Coding Interview Questions 2]] — part 2.
- [[29 - Interview Prep/Conceptual/01 - Conceptual Interview Questions]] — conceptual questions.
- [[29 - Interview Prep/Conceptual/06 - Conceptual Interview Questions 2]] — conceptual questions part 2.
- [[28 - Glossary/MOC|Glossary MOC]]
