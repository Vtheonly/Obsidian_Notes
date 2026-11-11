---
tags: [interview, coding, reasoning, vlm, mcp, grpo, moe]
iteration: 10
created: 2026-08-08
aliases: [Coding Interview Questions 2, Advanced Coding Interview, Coding Interview 2]
---

# 04 — Coding Interview Questions (Part 2)

> [!info] TL;DR
> Coding interview questions for advanced AI engineering topics that the original [[03 - Coding Interview Questions|Coding Interview Questions]] note didn't cover: reasoning models (GRPO loss), Vision-Language Models (image patch embedding), MCP (tool server), Mixture-of-Experts (routing), KV cache (PagedAttention), and quantization (INT4). These are the questions that distinguish a senior AI engineer from a junior one — they test depth, not breadth. Each question includes the problem, the approach, key implementation details, and common pitfalls.

## How to Use This Note

Each question is structured as:

1. **Problem statement** — what you're asked to implement.
2. **Approach** — the high-level strategy.
3. **Key implementation details** — the things that separate a working solution from a broken one.
4. **Common pitfalls** — what interviewers look for you to avoid.
5. **Follow-up questions** — what the interviewer might ask next.

Aim to write the code in 20–30 minutes for a senior role; 40–60 minutes for a mid-level role. Always explain your reasoning as you code — the interviewer cares about your thought process, not just the final code.

---

## Question 1: Implement GRPO Loss for Reasoning Model Training

### Problem

Implement the GRPO (Group Relative Policy Optimization) loss function used to train reasoning models like DeepSeek-R1. GRPO is a variant of PPO that eliminates the value function by using group-relative advantages.

### Background

GRPO generates $G$ completions per prompt, computes rewards for each, and uses the group-relative advantage $A_i = (r_i - \text{mean}(r)) / \text{std}(r)$ instead of PPO's value-function-based advantage. This is simpler (no value network to train) and works well for verifiable-reward tasks (math, code).

### Approach

1. Sample $G$ completions per prompt from the current policy.
2. Compute rewards $r_1, \ldots, r_G$ (using a verifier or reward model).
3. Compute group-relative advantages: $A_i = (r_i - \bar{r}) / \sigma_r$.
4. Compute the policy gradient loss with clipping (like PPO) and KL penalty to a reference policy.

### Implementation

```python
import torch
import torch.nn.functional as F

def grpo_loss(
    policy_log_probs: torch.Tensor,    # (G,) log p(completion_i | prompt) under current policy
    old_log_probs: torch.Tensor,       # (G,) log p under the policy that generated the completions
    ref_log_probs: torch.Tensor,       # (G,) log p under the reference (frozen) policy
    rewards: torch.Tensor,             # (G,) reward for each completion
    beta: float = 0.04,                # KL penalty coefficient
    clip_epsilon: float = 0.2,         # PPO clip range
) -> torch.Tensor:
    """
    Compute GRPO loss for a single prompt's group of G completions.

    Returns: scalar loss (to be minimized).
    """
    G = rewards.shape[0]

    # 1. Group-relative advantage
    mean_r = rewards.mean()
    std_r = rewards.std() + 1e-8  # avoid div by zero
    advantages = (rewards - mean_r) / std_r  # (G,)

    # 2. Importance sampling ratio (PPO-style)
    log_ratio = policy_log_probs - old_log_probs  # (G,)
    ratio = torch.exp(log_ratio)

    # 3. Clipped surrogate objective
    surr1 = ratio * advantages
    surr2 = torch.clamp(ratio, 1.0 - clip_epsilon, 1.0 + clip_epsilon) * advantages
    policy_loss = -torch.min(surr1, surr2).mean()  # negate because we minimize

    # 4. KL penalty to reference policy
    # KL(policy || ref) ≈ exp(ref_log - policy_log) - (ref_log - policy_log) - 1
    # This is the unbiased k3 estimator from John Schulman's blog
    log_diff = ref_log_probs - policy_log_probs
    kl = (torch.exp(log_diff) - log_diff - 1).mean()

    # 5. Total loss
    loss = policy_loss + beta * kl

    return loss

# Test
if __name__ == "__main__":
    G = 8
    policy_log_probs = torch.randn(G)
    old_log_probs = policy_log_probs.clone()  # On-policy: ratio = 1
    ref_log_probs = torch.randn(G)
    rewards = torch.tensor([1.0, 0.0, 1.0, 0.5, 0.0, 1.0, 0.0, 0.5])

    loss = grpo_loss(policy_log_probs, old_log_probs, ref_log_probs, rewards)
    print(f"GRPO loss: {loss.item():.4f}")  # Should be a reasonable scalar
```

### Key Implementation Details

- **Group-relative advantage**: $A_i = (r_i - \bar{r}) / \sigma_r$. This replaces PPO's value-function-based advantage. The normalization (subtract mean, divide by std) is critical — without it, all-positive rewards would push the policy to increase all completion probabilities, which is wrong.
- **Importance sampling ratio**: $\rho = \pi_\theta / \pi_{\text{old}}$. Even in on-policy training, $\pi_\theta$ drifts from $\pi_{\text{old}}$ between updates, so the ratio matters.
- **Clipping**: prevents destructive large updates. Same as PPO.
- **KL penalty**: keeps the policy close to the reference (frozen) policy. Without this, the policy can drift into degenerate behavior (e.g., always producing the same completion regardless of prompt).
- **k3 KL estimator**: $\text{KL} \approx \exp(\log p_{\text{ref}} - \log p_\theta) - (\log p_{\text{ref}} - \log p_\theta) - 1$. This is unbiased and more numerically stable than the naive $\exp$ estimator.

### Common Pitfalls

- **Forgetting to normalize advantages** — without normalization, all-positive rewards push all probabilities up, which is wrong.
- **Using PPO's value function** — GRPO eliminates the value function. Don't add it back.
- **Wrong KL estimator** — the naive $\exp(\log p_{\text{ref}} - \log p_\theta)$ estimator is biased; use k3.
- **Forgetting to detach `old_log_probs`** — these are constants (from the generation step), not differentiable.
- **Per-prompt vs. batch** — GRPO computes advantages per-prompt (within the group), not across the batch. Different prompts have different reward distributions.

### Follow-Up Questions

- **Why does GRPO eliminate the value function?** — because the group-relative advantage is a sufficient signal for verifiable-reward tasks. The value function is needed in PPO because rewards are sparse and noisy; in GRPO, the group provides a natural baseline.
- **How would you handle variable-length completions?** — pad to the max length in the group, mask padding in the log-prob computation (sum over actual tokens only).
- **What's the difference between GRPO and RLOO (Reinforce Leave-One-Out)?** — RLOO uses leave-one-out means as baselines; GRPO uses the group mean and std for normalization. They're similar but GRPO's normalization makes it more robust to reward scale.

---

## Question 2: Implement Image Patch Embedding for a VLM

### Problem

Implement the patch embedding layer that converts an image into a sequence of token embeddings for a Vision-Language Model (VLM). This is the first layer of ViT, CLIP, and LLaVA.

### Background

A VLM needs to convert a 2D image into a 1D sequence of token embeddings that the Transformer can process. The standard approach: split the image into non-overlapping patches (e.g., 16×16), flatten each patch, and project to the embedding dimension.

### Approach

1. Input: image tensor of shape `(B, C, H, W)`.
2. Split into patches of size `P × P`, giving `(B, C, H/P, W/P, P, P)`.
3. Flatten patches to `(B, num_patches, C × P × P)`.
4. Linear project to `(B, num_patches, embed_dim)`.
5. Add positional embeddings.
6. Prepend a `[CLS]` token (optional).

### Implementation

```python
import torch
import torch.nn as nn

class PatchEmbedding(nn.Module):
    """Convert image to patch embeddings (ViT-style)."""

    def __init__(
        self,
        patch_size: int = 16,
        in_channels: int = 3,
        embed_dim: int = 768,
        image_size: int = 224,
    ):
        super().__init__()
        self.patch_size = patch_size
        self.embed_dim = embed_dim
        self.num_patches = (image_size // patch_size) ** 2

        # Conv2d is an efficient way to do patch extraction + projection
        # kernel_size=patch_size, stride=patch_size => non-overlapping patches
        self.proj = nn.Conv2d(
            in_channels, embed_dim,
            kernel_size=patch_size, stride=patch_size
        )

        # Positional embeddings (learned)
        self.pos_embed = nn.Parameter(
            torch.randn(1, self.num_patches + 1, embed_dim) * 0.02
        )

        # CLS token (optional)
        self.cls_token = nn.Parameter(torch.randn(1, 1, embed_dim) * 0.02)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        x: (B, C, H, W) — image tensor
        returns: (B, num_patches + 1, embed_dim) — patch embeddings + CLS
        """
        B = x.shape[0]

        # 1. Patch extraction + projection: (B, C, H, W) -> (B, embed_dim, H/P, W/P)
        x = self.proj(x)

        # 2. Flatten spatial dims: (B, embed_dim, H/P, W/P) -> (B, embed_dim, num_patches)
        x = x.flatten(2)

        # 3. Transpose: (B, embed_dim, num_patches) -> (B, num_patches, embed_dim)
        x = x.transpose(1, 2)

        # 4. Prepend CLS token
        cls = self.cls_token.expand(B, -1, -1)  # (B, 1, embed_dim)
        x = torch.cat([cls, x], dim=1)  # (B, num_patches + 1, embed_dim)

        # 5. Add positional embeddings
        x = x + self.pos_embed

        return x

# Test
if __name__ == "__main__":
    patch_embed = PatchEmbedding(patch_size=16, embed_dim=768, image_size=224)
    image = torch.randn(2, 3, 224, 224)  # Batch of 2 RGB images
    embeddings = patch_embed(image)
    print(f"Input shape: {image.shape}")
    print(f"Output shape: {embeddings.shape}")  # Should be (2, 197, 768) — 196 patches + 1 CLS
```

### Key Implementation Details

- **Conv2d trick**: using a Conv2d with `kernel_size=patch_size, stride=patch_size` is equivalent to patch extraction + linear projection, but much faster (fused into one operation). This is what production ViTs use.
- **Patch count**: for 224×224 image with 16×16 patches, num_patches = (224/16)² = 196. Plus 1 for CLS = 197 tokens.
- **Positional embeddings**: learned, shape `(1, num_patches + 1, embed_dim)`. Initialized with small std (0.02). Added (not concatenated) to patch embeddings.
- **CLS token**: a learnable token prepended to the sequence. Its final state is used as the image representation (for classification) or fed to the LLM (in CLIP/LLaVA).
- **Initialization**: pos_embed and cls_token are typically initialized with std=0.02 (matching Transformer init convention).

### Common Pitfalls

- **Wrong patch count** — off-by-one if image_size isn't divisible by patch_size. Add an assertion.
- **Wrong transpose** — `(B, embed_dim, num_patches)` vs `(B, num_patches, embed_dim)`. The Transformer expects sequence-first.
- **Forgetting positional embeddings** — without them, the model can't distinguish patch positions (Transformer is permutation-invariant).
- **Wrong CLS expansion** — `cls_token` has shape `(1, 1, embed_dim)`, needs `.expand(B, -1, -1)` to match batch size.
- **Conv2d vs. unfold** — using `unfold` is slower and uses more memory. Stick with Conv2d.

### Follow-Up Questions

- **How would you handle variable image sizes?** — interpolate the positional embeddings to the new size (bicubic). The patch count changes, but the embed_dim stays the same.
- **Why use Conv2d instead of explicit patch extraction?** — it's a fused operation (extract + project in one CUDA kernel), much faster than separate extraction + linear.
- **What's the difference between ViT and CLIP's image encoder?** — CLIP uses a ViT architecture but with a different training objective (contrastive) and typically larger embed_dim. The patch embedding is the same.

---

## Question 3: Implement an MCP Tool Server

### Problem

Implement a minimal MCP (Model Context Protocol) server that exposes a single tool (e.g., "search the web") and handles JSON-RPC requests from an MCP client.

### Background

MCP is a protocol for LLMs to call external tools. An MCP server exposes resources, prompts, and tools via JSON-RPC. Clients (like Claude Desktop, Cursor) connect to servers and call their tools.

### Approach

1. Define the tool's schema (name, description, input schema).
2. Implement the JSON-RPC `initialize`, `tools/list`, and `tools/call` methods.
3. Run the server over stdio (the simplest transport).

### Implementation

```python
import json
import sys
from typing import Any

def search_web(query: str, max_results: int = 5) -> list[dict]:
    """Mock web search — replace with a real search API."""
    return [
        {"title": f"Result {i+1} for '{query}'", "url": f"https://example.com/{i+1}"}
        for i in range(max_results)
    ]

# Tool definitions
TOOLS = [
    {
        "name": "search_web",
        "description": "Search the web and return top results.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "max_results": {"type": "integer", "description": "Max results (default 5)", "default": 5},
            },
            "required": ["query"],
        },
    }
]

def handle_request(request: dict) -> dict | None:
    """Handle a single JSON-RPC request."""
    method = request.get("method")
    req_id = request.get("id")
    params = request.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "web-search-server", "version": "1.0.0"},
            },
        }

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": TOOLS},
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})

        if tool_name == "search_web":
            result = search_web(**tool_args)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {"type": "text", "text": json.dumps(result, indent=2)}
                    ]
                },
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
            }

    # Notification (no id) — no response needed
    if req_id is None:
        return None

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Unknown method: {method}"},
    }

def main():
    """Read JSON-RPC requests from stdin, write responses to stdout."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = handle_request(request)
            if response is not None:
                print(json.dumps(response), flush=True)
        except json.JSONDecodeError:
            error = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"},
            }
            print(json.dumps(error), flush=True)

if __name__ == "__main__":
    main()
```

### Key Implementation Details

- **JSON-RPC 2.0**: every request has `jsonrpc: "2.0"`, an `id`, and a `method`. Responses echo the `id`. Notifications (no `id`) don't get responses.
- **Protocol version**: MCP uses dated protocol versions (e.g., `2024-11-05`). The client and server negotiate during `initialize`.
- **Tools vs. resources vs. prompts**: tools are functions the LLM can call; resources are data the LLM can read; prompts are templates the LLM can use. This example only implements tools.
- **Content format**: tool results are returned as a list of content blocks (`{"type": "text", "text": "..."}`). Other types: `image`, `resource`.
- **Stdio transport**: the simplest MCP transport. The server reads JSON-RPC from stdin, writes to stdout. Other transports: HTTP, SSE.

### Common Pitfalls

- **Forgetting `flush=True`** — without flushing, the client doesn't receive the response until the buffer fills.
- **Not handling notifications** — notifications (no `id`) don't get responses. Returning a response for a notification is a protocol error.
- **Wrong error codes** — JSON-RPC defines specific error codes (-32700 parse error, -32601 method not found, etc.). Use them correctly.
- **Not validating input schema** — the tool's `inputSchema` should be validated against the actual arguments. Use Pydantic or jsonschema.
- **Blocking I/O** — the stdio loop blocks on `sys.stdin`. For concurrent tool execution, use async I/O.

### Follow-Up Questions

- **How would you add authentication?** — for stdio transport, the client and server are on the same machine (no auth needed). For HTTP transport, use OAuth or API keys in the Authorization header.
- **How would you handle long-running tools?** — return a "progress" notification immediately, then send the final result when ready. The client can display progress to the user.
- **What's the difference between MCP and OpenAI function calling?** — MCP is a protocol (transport + schema), function calling is an API feature. MCP servers can be used by any client (Claude, Cursor, custom); function calling is OpenAI-specific. MCP is more general; function calling is simpler.

---

## Question 4: Implement Mixture-of-Experts Routing

### Problem

Implement the routing mechanism for a Mixture-of-Experts (MoE) layer. Given an input token, the router selects the top-K experts and combines their outputs.

### Background

MoE layers have $N$ expert feed-forward networks. For each token, a router network computes logits over experts, picks the top-K, and combines their outputs weighted by the softmax of the logits. This gives sparse activation: only K experts are active per token, even though all N experts' parameters are stored.

### Approach

1. Router: linear layer from `embed_dim` to `num_experts`.
2. Top-K selection: pick the K experts with highest logits.
3. Softmax over the selected K logits (not all N).
4. Dispatch tokens to selected experts.
5. Combine outputs weighted by the softmax scores.

### Implementation

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class MoELayer(nn.Module):
    def __init__(
        self,
        embed_dim: int = 768,
        num_experts: int = 8,
        top_k: int = 2,
        expert_hidden_dim: int = 3072,
    ):
        super().__init__()
        self.num_experts = num_experts
        self.top_k = top_k

        # Router: embed_dim -> num_experts logits
        self.router = nn.Linear(embed_dim, num_experts, bias=False)

        # Experts: each is a standard FFN (Linear -> SwiGLU -> Linear)
        self.experts = nn.ModuleList([
            self._make_expert(embed_dim, expert_hidden_dim)
            for _ in range(num_experts)
        ])

    def _make_expert(self, embed_dim, hidden_dim):
        return nn.Sequential(
            nn.Linear(embed_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, embed_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        x: (B, N, D) — batch of sequences
        returns: (B, N, D) — same shape, but each token processed by top-K experts
        """
        B, N, D = x.shape
        x_flat = x.view(B * N, D)  # (B*N, D)

        # 1. Router logits
        router_logits = self.router(x_flat)  # (B*N, num_experts)

        # 2. Top-K selection
        top_k_logits, top_k_indices = torch.topk(router_logits, self.top_k, dim=-1)
        # top_k_logits: (B*N, K), top_k_indices: (B*N, K)

        # 3. Softmax over the selected K (not all N)
        router_weights = F.softmax(top_k_logits, dim=-1)  # (B*N, K)

        # 4. Dispatch to experts and combine
        output = torch.zeros_like(x_flat)
        for k in range(self.top_k):
            expert_indices = top_k_indices[:, k]  # (B*N,) — which expert for each token at slot k
            weights = router_weights[:, k]  # (B*N,) — weight for each token at slot k

            # Group tokens by expert
            for e in range(self.num_experts):
                mask = expert_indices == e
                if not mask.any():
                    continue
                expert_input = x_flat[mask]  # (num_tokens_for_expert_e, D)
                expert_output = self.experts[e](expert_input)  # (num_tokens, D)
                output[mask] += weights[mask].unsqueeze(-1) * expert_output

        return output.view(B, N, D)

# Test
if __name__ == "__main__":
    moe = MoELayer(embed_dim=768, num_experts=8, top_k=2)
    x = torch.randn(2, 10, 768)  # Batch of 2, seq_len 10
    out = moe(x)
    print(f"Input: {x.shape}, Output: {out.shape}")  # Both (2, 10, 768)
```

### Key Implementation Details

- **Top-K, not top-1**: top-2 or top-8 is standard. Top-1 is too sparse (loses quality); top-K with large K approaches dense (loses efficiency).
- **Softmax over selected K, not all N**: this is critical. If you softmax over all N, the unselected experts get non-zero weight, breaking sparsity.
- **Grouping by expert**: the inner loop groups tokens by expert, allowing batched computation per expert. This is much faster than calling each expert per-token.
- **Auxiliary loss**: production MoE adds a load-balancing loss to encourage experts to be used evenly. The naive implementation above doesn't include this.
- **No bias in router**: the router typically has no bias (just a linear projection). Bias can cause degenerate solutions where one expert always wins.

### Common Pitfalls

- **Softmax over all N instead of selected K** — breaks sparsity. The unselected experts get non-zero weight, defeating the purpose.
- **Not grouping by expert** — calling each expert per-token is O(B×N×K) expert calls. Grouping by expert is O(N_experts) expert calls (each with a batch). 10–100× faster.
- **Forgetting the auxiliary loss** — without load balancing, one expert can dominate (router collapse), wasting the other experts' parameters.
- **Wrong gradient flow** — the top-K selection is non-differentiable (argmax). Gradients flow through the softmax weights, not the selection. This is correct but easy to get wrong in custom implementations.
- **Capacity factor** — production MoE has a "capacity" per expert (max tokens it can process). Tokens beyond capacity are dropped. This implementation doesn't have capacity — fine for learning, not for production.

### Follow-Up Questions

- **How would you add load balancing?** — add an auxiliary loss that penalizes imbalanced expert usage. The standard formulation: $L_{\text{aux}} = N \cdot \sum_i f_i \cdot P_i$, where $f_i$ is the fraction of tokens routed to expert $i$ and $P_i$ is the average router probability for expert $i$. This encourages uniform usage.
- **What's the difference between this and DeepSeek-V3's auxiliary-loss-free routing?** — DeepSeek-V3 uses a bias term per expert that's adjusted based on usage (increased for underused experts, decreased for overused). This achieves load balancing without the gradient interference of the auxiliary loss.
- **How would you parallelize this across GPUs?** — expert parallelism: each GPU holds a subset of experts. Tokens are dispatched to the GPU that holds their assigned expert. This requires all-to-all communication.

---

## Question 5: Implement PagedAttention (Simplified)

### Problem

Implement a simplified version of PagedAttention, the KV cache management strategy used by vLLM. The key idea: partition the KV cache into fixed-size blocks (pages), allowing non-contiguous storage and efficient memory usage.

### Background

Standard KV cache stores each sequence's K and V as a contiguous tensor. This wastes memory (fragmentation) and limits batching. PagedAttention partitions the cache into blocks (e.g., 16 tokens each), stores each sequence as a list of block pointers, and attention computes over the blocks.

### Approach

1. Maintain a global pool of KV blocks (each holding K and V for `block_size` tokens).
2. Each sequence has a list of block IDs (its "page table").
3. During attention, gather blocks for the sequence and compute attention.
4. When a sequence grows, allocate a new block; when it ends, free its blocks.

### Implementation (Conceptual)

```python
import torch
import torch.nn.functional as F

class PagedKVCache:
    """Simplified PagedAttention KV cache."""

    def __init__(
        self,
        num_blocks: int,
        block_size: int,
        num_heads: int,
        head_dim: int,
        dtype=torch.bfloat16,
    ):
        self.block_size = block_size
        self.num_heads = num_heads
        self.head_dim = head_dim

        # Global pool of KV blocks
        # Shape: (num_blocks, 2, block_size, num_heads, head_dim)
        # The 2 is for K and V
        self.kv_pool = torch.zeros(
            num_blocks, 2, block_size, num_heads, head_dim, dtype=dtype
        )
        self.free_blocks = list(range(num_blocks))  # Stack of free block IDs
        self.sequence_blocks: dict[int, list[int]] = {}  # seq_id -> block IDs

    def allocate_sequence(self, seq_id: int):
        """Start a new sequence (no blocks yet)."""
        self.sequence_blocks[seq_id] = []

    def append_kv(self, seq_id: int, new_k: torch.Tensor, new_v: torch.Tensor):
        """
        Append new K, V for a sequence.
        new_k, new_v: (new_tokens, num_heads, head_dim)
        """
        num_new = new_k.shape[0]
        for i in range(num_new):
            # If current block is full, allocate a new one
            seq_blocks = self.sequence_blocks[seq_id]
            current_pos = len(seq_blocks) * self.block_size + i  # approx

            if not seq_blocks or current_pos % self.block_size == 0:
                # Need a new block
                if not self.free_blocks:
                    raise RuntimeError("KV cache full — increase num_blocks")
                block_id = self.free_blocks.pop()
                seq_blocks.append(block_id)

            # Write K, V to the current block
            block_id = seq_blocks[-1]
            offset = (len(seq_blocks) * self.block_size - 1) % self.block_size
            self.kv_pool[block_id, 0, offset] = new_k[i]  # K
            self.kv_pool[block_id, 1, offset] = new_v[i]  # V

    def get_kv(self, seq_id: int) -> tuple[torch.Tensor, torch.Tensor]:
        """Get the full K, V for a sequence (gathered from blocks)."""
        block_ids = self.sequence_blocks[seq_id]
        if not block_ids:
            return torch.empty(0), torch.empty(0)

        # Gather blocks
        blocks = self.kv_pool[block_ids]  # (num_blocks, 2, block_size, num_heads, head_dim)
        # Flatten block + token dims
        k = blocks[:, 0].reshape(-1, self.num_heads, self.head_dim)  # (seq_len, num_heads, head_dim)
        v = blocks[:, 1].reshape(-1, self.num_heads, self.head_dim)
        return k, v

    def free_sequence(self, seq_id: int):
        """Free all blocks for a finished sequence."""
        for block_id in self.sequence_blocks[seq_id]:
            self.free_blocks.append(block_id)
        del self.sequence_blocks[seq_id]


def paged_attention(
    query: torch.Tensor,  # (num_heads, head_dim)
    cache: PagedKVCache,
    seq_id: int,
) -> torch.Tensor:
    """Compute attention for a single query against the paged KV cache."""
    k, v = cache.get_kv(seq_id)  # (seq_len, num_heads, head_dim)

    # Per-head attention (simplified — no batching)
    head_dim = query.shape[-1]
    scores = torch.einsum('hd,thd->th', query, k) / (head_dim ** 0.5)  # (seq_len,)
    weights = F.softmax(scores, dim=0)
    output = torch.einsum('t,thd->hd', weights, v)  # (num_heads, head_dim)
    return output
```

### Key Implementation Details

- **Block pool**: a single large tensor for all KV storage, partitioned into blocks. Avoids per-sequence allocation overhead.
- **Page table**: each sequence has a list of block IDs. This indirection allows non-contiguous storage (no external fragmentation).
- **Block size**: typically 16 tokens. Smaller blocks → less internal fragmentation but more metadata overhead. vLLM uses 16.
- **Free list**: a stack of free block IDs. Allocating is `pop()`; freeing is `append()`. O(1) operations.
- **Gather operation**: to compute attention, gather the sequence's blocks and flatten. In production, this is done with custom CUDA kernels (vLLM's PagedAttention kernel).

### Common Pitfalls

- **External fragmentation** — without paging, allocating and freeing variable-length sequences fragments memory. Paging eliminates this.
- **Internal fragmentation** — the last block of each sequence may be partially full. With block_size=16, average waste is 8 tokens per sequence. Acceptable.
- **Wrong block indexing** — the offset calculation (which slot in the block to write to) is easy to get wrong. Test carefully.
- **Not freeing blocks** — if sequences don't free their blocks, the cache fills up. Always free on sequence end (or preemption).
- **Capacity management** — when the cache is full, you must preempt sequences (free their blocks to make room for new ones). vLLM uses LRU preemption.

### Follow-Up Questions

- **How does PagedAttention enable continuous batching?** — without paging, you can't add new sequences to a batch mid-generation (the contiguous KV caches don't have room). With paging, you just allocate new blocks for the new sequence. This lets vLLM process sequences of different lengths and arrival times in the same batch.
- **What's the block size tradeoff?** — smaller blocks (e.g., 4) reduce internal fragmentation but increase metadata overhead (more block pointers per sequence). Larger blocks (e.g., 64) reduce overhead but increase fragmentation. vLLM found 16 to be the sweet spot empirically.
- **How would you implement preemption?** — when the cache is full, pick a sequence to evict (LRU is common). Free its blocks and either recompute it on next request (longer latency) or swap its blocks to CPU (faster resume).

---

## Question 6: Implement INT4 Quantization

### Problem

Implement INT4 weight-only quantization for a Linear layer. Convert fp16/bf16 weights to 4-bit integers and implement the dequantization + matmul at inference time.

### Background

INT4 quantization reduces model memory by 4× (vs fp16) and can speed up inference (memory bandwidth is the bottleneck for LLM inference). The simplest form is weight-only quantization: weights are stored as INT4, activations stay in fp16/bf16, and dequantization happens on the fly during the matmul.

### Approach

1. **Quantization**: for each weight, find the min/max, compute scale = (max - min) / 15, quantize to [0, 15].
2. **Storage**: pack two INT4 values into one byte (since 4+4=8 bits).
3. **Dequantization**: at inference, unpack and dequantize: `w = (q * scale) + zero_point`.
4. **Matmul**: dequantize weights on the fly and multiply with fp16 activations.

### Implementation

```python
import torch
import torch.nn as nn

def quantize_int4(weight: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Quantize a weight tensor to INT4 (per-row asymmetric quantization).

    weight: (out_features, in_features)
    returns:
        packed: (out_features, in_features // 2) — two INT4 values packed per byte
        scales: (out_features,) — per-row scale
        zero_points: (out_features,) — per-row zero point
    """
    out_features, in_features = weight.shape

    # Per-row min/max
    w_min = weight.min(dim=1, keepdim=True).values  # (out_features, 1)
    w_max = weight.max(dim=1, keepdim=True).values

    # Scale and zero point
    scales = (w_max - w_min) / 15  # (out_features, 1)
    zero_points = -w_min / scales  # (out_features, 1)

    # Quantize: clamp to [0, 15] and round
    q = torch.clamp(torch.round(weight / scales + zero_points), 0, 15).to(torch.uint8)
    # q is (out_features, in_features) with values in [0, 15]

    # Pack two values per byte
    assert in_features % 2 == 0
    q_left = q[:, ::2]   # (out_features, in_features // 2)
    q_right = q[:, 1::2]
    packed = (q_left << 4) | q_right  # (out_features, in_features // 2)

    return packed, scales.squeeze(1), zero_points.squeeze(1)


def dequantize_int4(
    packed: torch.Tensor,
    scales: torch.Tensor,
    zero_points: torch.Tensor,
) -> torch.Tensor:
    """Dequantize INT4 packed weights back to fp16."""
    out_features, half_in = packed.shape
    in_features = half_in * 2

    # Unpack
    q_left = (packed >> 4) & 0x0F  # (out_features, half_in)
    q_right = packed & 0x0F

    # Interleave back
    q = torch.zeros(out_features, in_features, dtype=torch.uint8, device=packed.device)
    q[:, ::2] = q_left
    q[:, 1::2] = q_right

    # Dequantize: w = (q - zero_point) * scale
    weight = (q.float() - zero_points.unsqueeze(1)) * scales.unsqueeze(1)
    return weight.to(torch.float16)


class INT4Linear(nn.Module):
    """Linear layer with INT4 quantized weights."""

    def __init__(self, in_features: int, out_features: int, bias: bool = True):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features

        # Quantized weights (set during quantize())
        self.register_buffer("packed_weight", torch.zeros(out_features, in_features // 2, dtype=torch.uint8))
        self.register_buffer("weight_scales", torch.zeros(out_features))
        self.register_buffer("weight_zero_points", torch.zeros(out_features))

        if bias:
            self.register_buffer("bias", torch.zeros(out_features))
        else:
            self.bias = None

    def quantize_(self, weight: torch.Tensor):
        """Quantize an fp16/bf16 weight tensor in place."""
        packed, scales, zps = quantize_int4(weight.float())
        self.packed_weight.copy_(packed)
        self.weight_scales.copy_(scales)
        self.weight_zero_points.copy_(zps)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (..., in_features) -> (..., out_features)"""
        # Dequantize on the fly
        weight = dequantize_int4(self.packed_weight, self.weight_scales, self.weight_zero_points)

        # Standard matmul
        out = x @ weight.T

        if self.bias is not None:
            out = out + self.bias

        return out

# Test
if __name__ == "__main__":
    # Create a fp16 linear layer
    fp16_linear = nn.Linear(768, 768, bias=True).to(torch.float16)

    # Quantize it
    int4_linear = INT4Linear(768, 768, bias=True)
    int4_linear.quantize_(fp16_linear.weight.data)
    int4_linear.bias.copy_(fp16_linear.bias.data)

    # Compare outputs
    x = torch.randn(1, 10, 768, dtype=torch.float16)
    with torch.no_grad():
        y_fp16 = fp16_linear(x)
        y_int4 = int4_linear(x)

    # Check they're close (INT4 has quantization error)
    error = (y_fp16 - y_int4).abs().mean()
    print(f"Mean absolute error: {error.item():.4f}")
    print(f"Relative error: {(error / y_fp16.abs().mean()).item():.2%}")

    # Check memory savings
    fp16_bytes = fp16_linear.weight.nelement() * 2  # 2 bytes per fp16
    int4_bytes = int4_linear.packed_weight.nelement() * 1  # 1 byte per 2 INT4 values
    print(f"fp16 weight: {fp16_bytes} bytes")
    print(f"INT4 weight: {int4_bytes} bytes ({fp16_bytes / int4_bytes:.1f}x smaller)")
```

### Key Implementation Details

- **Per-row quantization**: each output row has its own scale and zero point. This is critical because different rows can have very different value ranges. Per-tensor quantization (one scale for the whole weight) is much worse.
- **Asymmetric quantization**: scale and zero point allow the quantized range to start at any value. Symmetric quantization (only scale, zero point = 0) is simpler but worse for weights with non-zero mean.
- **Packing**: two INT4 values per byte. This halves the storage cost vs. storing each INT4 in a byte (with the high nibble wasted).
- **Dequantization on the fly**: the matmul reads INT4, dequantizes, and multiplies with fp16 activations. In production, this is done with custom CUDA kernels that fuse dequantize + matmul.
- **Bias in fp16**: the bias is typically kept in fp16 (small enough to not matter).

### Common Pitfalls

- **Per-tensor instead of per-row quantization** — much worse quality. Always quantize per-row (or per-channel) for weights.
- **Symmetric instead of asymmetric** — symmetric is simpler but worse for weights with non-zero mean. Use asymmetric.
- **Wrong packing order** — `q_left << 4 | q_right` puts `q_left` in the high nibble. Be consistent when unpacking.
- **Forgetting to handle odd in_features** — packing requires `in_features % 2 == 0`. For odd sizes, pad with a zero.
- **No group quantization** — for better quality, quantize in groups of 32 or 64 (group quantization). This implementation is per-row; group quantization is finer-grained.
- **Not fusing dequantize + matmul** — dequantizing to fp16 and then calling `torch.matmul` is slow. Production kernels (GPTQ, AWQ, Marlin) fuse these operations.

### Follow-Up Questions

- **What's the difference between weight-only and weight+activation quantization?** — weight-only keeps activations in fp16/bf16, so dequantization happens per-weight. Weight+activation quantizes both, requiring dequantization of both before matmul. Weight-only is simpler and works well for memory-bound inference; weight+activation is needed for compute-bound scenarios.
- **What are GPTQ and AWQ?** — GPTQ (Generalized Post-Training Quantization) uses second-order information (Hessian) to minimize quantization error per layer. AWQ (Activation-aware Weight Quantization) scales weights based on activation magnitudes. Both achieve better quality than naive per-row quantization.
- **How would you quantize the KV cache?** — similar approach: per-channel (per-head) INT8 or INT4 quantization. The challenge is that KV values change during generation, so quantization must be online. vLLM supports KV cache quantization.

---

## See Also

- [[29 - Interview Prep/MOC|Interview Prep MOC]]
- [[29 - Interview Prep/Coding/03 - Coding Interview Questions|Coding Interview Questions]] — the original, with attention/MHA/sampling/RoPE/KV cache.
- [[29 - Interview Prep/System Design/02 - System Design Interview Questions|System Design Interview Questions]]
- [[29 - Interview Prep/System Design/05 - System Design Interview Questions 2|System Design Interview Questions 2]]
- [[27 - Projects/Implementations/01 - Build Attention and Transformer From Scratch|Build Attention and Transformer From Scratch]]
- [[12 - Fine-Tuning/RLHF/05 - RLHF with PPO|RLHF with PPO]] — PPO is the foundation for GRPO.
- [[23 - Multimodal AI/Vision-Language/03 - LLaVA|LLaVA]] — uses patch embeddings.
- [[19 - MCP/Architecture/01 - MCP Overview|MCP Overview]] — the protocol this server implements.
- [[07 - Transformers/Variants/15 - Mixture of Experts Transformer|Mixture of Experts Transformer]]
- [[13 - Inference/KV Cache/02 - PagedAttention|PagedAttention]]
- [[13 - Inference/Quantization/03 - Quantization|Quantization]]
