## 2. Vocabulary and Special Tokens

### Special Control Tokens

The tokenizer's vocabulary is built from the training set using the lexical rules above. Additionally, four special tokens are hardcoded at fixed indices:

**Index 0: `<pad>` (Padding Token)**

Sequences in a batch must all be the same length to form a rectangular tensor. If batch sequences have lengths [12, 47, 83, 31], they must all be padded to length 83. The padding token fills the gaps.

The loss function masks `<pad>` positions by setting their contribution to zero. The model is not penalized for any prediction at a `<pad>` position.

> **Critical reminder:** The model does see `<pad>` tokens during the decoder's masked self-attention. They are not invisible to the attention mechanism by default. You must explicitly mask them out in the attention computation to prevent the model from attending to meaningless padding and learning spurious patterns. This is done via the `src_key_padding_mask` and `tgt_key_padding_mask` arguments in PyTorch's `nn.TransformerDecoder`.

**Index 1: `<sos>` (Start of Sequence Token)**

The decoder is autoregressive: it predicts one token at a time, each conditioned on previous predictions. But at step $t=0$, there are no previous predictions. The `<sos>` token is the seed. It is always the first input to the decoder at $t=0$, and the decoder is trained to predict the first real token of the sequence as its response to `<sos>`.

**Index 2: `<eos>` (End of Sequence Token)**

The model needs to know when to stop generating. Mathematical formulas have variable lengths. If the generation loop runs forever, it produces infinite garbage tokens.

During training, `<eos>` is appended to the end of every target sequence. The model is trained to predict `<eos>` after the last real token. During inference, the generation loop terminates when `<eos>` is produced.

**Index 3: `<unk>` (Unknown Token)**

If a symbol appears in the validation set that was not in the training vocabulary, the tokenizer cannot represent it. It is mapped to `<unk>`. A model that frequently produces `<unk>` is encountering symbols outside its vocabulary, which indicates either:
1. The training set does not cover the full distribution of mathematical notation.
2. The formula contains symbols from a different LaTeX package not used during training.

A high `<unk>` rate is a data distribution mismatch signal, not a model architecture problem.

---

### Vocabulary Size Considerations

The TAMER vocabulary typically contains 300-600 tokens depending on the dataset. This is tiny compared to NLP models (GPT-4 has 100,000 tokens).

This small vocabulary is a significant advantage:
- The final linear projection layer (mapping decoder hidden states to token logits) is only `D × V` (e.g., 768 × 512 = 393,216 parameters) instead of billions.
- Softmax over 512 tokens is computationally trivial.
- The model can realistically learn good probability estimates for all 512 token types because they all appear frequently.

---