---
tags: [transformers, moc]
iteration: 2
created: 2026-08-07
---

# 07 — Transformers MOC

> [!info] The Transformer architecture — the single most important idea in modern AI. Read in numbered order.

## Reading Order

| #   | Note                                              | Sub-domain        | Purpose                                            |
|-----|---------------------------------------------------|-------------------|----------------------------------------------------|
| 01  | [[01 - Transformer Block]]                        | Architecture      | The repeatable unit; the whole picture.            |
| 02  | [[02 - Pre-Norm vs Post-Norm]]                    | Architecture      | Critical stability decision.                       |
| 03  | [[03 - Residual Connections]]                     | Architecture      | Why deep Transformers train.                       |
| 04  | [[04 - Normalization Layers]]                     | Components        | LayerNorm, RMSNorm.                                |
| 05  | [[05 - Feed-Forward Network Deep]]                | Components        | FFN, SwiGLU, GEGLU; where params live.             |
| 06  | [[06 - Embedding Layer]]                          | Components        | Token ID → vector; tied vs untied.                 |
| 07  | [[07 - BERT]]                                     | Encoder Models    | Bidirectional encoder; still useful.               |
| 09  | [[09 - GPT Family Evolution]]                     | Decoder Models    | Modern LLM architecture recipe.                    |
| 12  | [[12 - T5 and BART]]                              | Encoder-Decoder   | Text-to-text; denoising autoencoder.               |
| 13  | [[13 - Vision Transformer ViT]]                   | Variants          | Transformers for images.                           |
| 15  | [[15 - Mixture of Experts Transformer]]           | Variants          | MoE; scale params without scaling compute.         |

## Sub-Domains

- [[07 - Transformers/Architecture/01 - Transformer Block|Architecture]] — notes 01–03
- [[07 - Transformers/Components/04 - Normalization Layers|Components]] — notes 04–06
- [[07 - Transformers/Encoder Models/07 - BERT|Encoder Models]] — notes 07–08
- [[07 - Transformers/Decoder Models/09 - GPT Family Evolution|Decoder Models]] — notes 09–11
- [[07 - Transformers/Encoder-Decoder Models/12 - T5 and BART|Encoder-Decoder Models]] — note 12
- [[07 - Transformers/Variants/15 - Mixture of Experts Transformer|Variants]] — notes 13–16

## See Also

- [[06 - Attention Mechanisms/MOC|06 Attention Mechanisms]] — the core operation
- [[08 - LLMs/MOC|08 LLMs]] — modern decoder-only Transformers
- [[10 - Model Architecture Research/MOC|10 Model Architecture Research]] — per-model deep dives
- [[13 - Inference/MOC|13 Inference]] — running Transformers efficiently
