## 9.5 The Complete Forward Pass: Every Tensor, Every Shape

This is the tensor-level specification of a single forward pass through TAMER. Every intermediate tensor shape is tracked explicitly.

### Encoder Forward Pass

```
Input:
  images:  [B, 3, 256, 1024]  (float32, normalized)

Step 1: Swin Backbone
  backbone(images) → raw_features
  raw_features:  [B, 1024, 8, 32]  (float32)

Step 2: Permute to channels-last
  raw_features.permute(0, 2, 3, 1) → x
  x:  [B, 8, 32, 1024]

Step 3: Linear Projection (1024 → 768)
  self.proj(x) → x
  x:  [B, 8, 32, 768]

Step 4: Layer Normalization
  self.norm(x) → x
  x:  [B, 8, 32, 768]  (same shape, normalized values)

Step 5: 2D Positional Encoding
  row_indices: [0, 1, 2, 3, 4, 5, 6, 7]
  col_indices: [0, 1, 2, ..., 31]
  row_embed: self.row_embed(row_indices) → [8, 384]
  col_embed: self.col_embed(col_indices) → [32, 384]
  
  # Broadcast to full grid
  row_pe: [8, 384] → unsqueeze(1) → [8, 1, 384] → expand → [8, 32, 384]
  col_pe: [32, 384] → unsqueeze(0) → [1, 32, 384] → expand → [8, 32, 384]
  
  pe_2d = concat(row_pe, col_pe, dim=-1) → [8, 32, 768]
  x = x + pe_2d → [B, 8, 32, 768]

Step 6: Row Boundary Computation
  row_means = x.mean(dim=2) → [B, 8, 768]
  boundary = self.row_boundary_proj(row_means) → [B, 8, 768]
  boundary = boundary + self.row_boundary_base → [B, 8, 768]
  
  # self.row_boundary_base: [768] (single learnable vector)

Step 7: Interleaving
  # For each row r in range(8):
  #   Take visual patches: x[:, r, :, :] → [B, 32, 768]
  #   Take boundary token: boundary[:, r:r+1, :] → [B, 1, 768]
  #   Concatenate: [B, 33, 768] per row
  
  memory = cat(all_segments, dim=1) → [B, 264, 768]

Output:
  memory:  [B, 264, 768]  (the Encoder Memory Matrix)
```

### Decoder Forward Pass (Training with Teacher Forcing)

```
Input:
  tgt_ids:  [B, T]        (int64, token indices, SOS prepended)
  memory:   [B, 264, 768] (from encoder)
  tgt_mask: [T, T]        (float, causal mask, -inf above diagonal)
  tgt_key_padding_mask: [B, T]  (bool, True for pad positions)

Step 1: Token Embedding
  self.embedding(tgt_ids) → x
  x:  [B, T, 768]

Step 2: 1D Sinusoidal Positional Encoding
  pe_1d: [T, 768]  (precomputed, not learned)
  x = x + pe_1d → [B, T, 768]

Step 3: Dropout (training only)
  x = self.dropout(x) → [B, T, 768]

Step 4: 10 Stacked Decoder Layers
  For each layer in range(10):
  
    # Pre-Norm Self-Attention
    x_norm = layer.norm1(x) → [B, T, 768]
    q = k = v = x_norm
    attn_out = MultiHeadAttention(
        q, k, v,
        attn_mask=tgt_mask,        # [T, T] causal
        key_padding_mask=tgt_key_padding_mask  # [B, T] padding
    ) → [B, T, 768]
    x = x + attn_out  # Residual connection
    
    # Pre-Norm Cross-Attention
    x_norm = layer.norm2(x) → [B, T, 768]
    cross_out = MultiHeadAttention(
        query=x_norm,              # [B, T, 768] from decoder
        key=memory,                # [B, 264, 768] from encoder
        value=memory,              # [B, 264, 768] from encoder
        key_padding_mask=None      # memory has no padding
    ) → [B, T, 768]
    x = x + cross_out  # Residual connection
    
    # Pre-Norm Feed-Forward
    x_norm = layer.norm3(x) → [B, T, 768]
    ff_out = layer.linear2(F.gelu(layer.linear1(x_norm)))
    # linear1: [B, T, 768] → [B, T, 3072]
    # gelu:    [B, T, 3072] → [B, T, 3072]
    # linear2: [B, T, 3072] → [B, T, 768]
    x = x + ff_out  # Residual connection

  # Final normalization after all layers
  x = self.final_norm(x) → [B, T, 768]

Step 5: Output Projection
  self.output_proj(x) → logits
  logits:  [B, T, 522]  (522 = vocab_size)

Output:
  logits:  [B, T, 522]
```

---