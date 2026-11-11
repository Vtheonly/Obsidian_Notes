---
tags: [training, moc]
iteration: 6
created: 2026-08-07
---

# 11 — Training MOC

> [!info] How foundation models are pretrained. Most AI engineers will fine-tune, not pretrain, but understanding pretraining is essential for understanding the models you fine-tune. Iteration 6 added three new notes: Data Pipelines and Deduplication, Mixed Precision Training (FP16/BF16/FP8), and Loss Spikes and Stability.

## Reading Order

| #   | Note                                              | Sub-domain          | Purpose                                            |
|-----|---------------------------------------------------|---------------------|----------------------------------------------------|
| 01  | [[01 - Pretraining Objectives and Scaling Laws]]  | Pretraining         | CLM/MLM/span corruption; Chinchilla.               |
| 02  | [[02 - Distributed Training]]                     | Distributed         | DP, TP, PP, ZeRO, FSDP; 3D parallelism.            |
| 03  | [[03 - Data Pipelines and Deduplication]]         | Data                | Collection, extraction, filtering, dedup.          |
| 04  | [[04 - Mixed Precision Training]]                 | Optimization        | FP16, BF16, FP8; master weights.                   |
| 05  | [[05 - Loss Spikes and Stability]]                | Optimization        | Spike causes, prevention, recovery.                |

## Sub-Domains

- [[11 - Training/Pretraining/01 - Pretraining Objectives and Scaling Laws|Pretraining]] — note 01
- [[12 - Fine-Tuning/MOC|Alignment]] — SFT, RLHF, RLAIF (chapter 12 covers fine-tuning)
- [[11 - Training/Data/03 - Data Pipelines and Deduplication|Data]] — note 03
- [[11 - Training/Distributed Training/02 - Distributed Training|Distributed Training]] — note 02
- [[11 - Training/Optimization/04 - Mixed Precision Training|Optimization]] — notes 04, 05

## The Big Picture

Training a foundation model involves five interlocking concerns:

1. **Data**: what you train on (note 03). Quality determines model quality.
2. **Objective**: what the model learns to predict (note 01). CLM, MLM, span corruption.
3. **Optimization**: how you update weights (notes 04, 05; see also chapter 02 for math).
4. **Distribution**: how you parallelize across GPUs (note 02).
5. **Alignment**: how you make the model useful and safe (see chapter 12 for fine-tuning).

Each concern is a deep topic. Production training teams have specialists for each.

## Why This Matters for AI Engineers

Even if you never pretrain a model from scratch:

- **Fine-tuning** uses the same optimization, distribution, and stability techniques at smaller scale.
- **Choosing a model** requires understanding how it was trained (data, objective, scale).
- **Debugging fine-tuning** failures often requires understanding pretraining stability.
- **Estimating training cost** for a custom model requires understanding distributed training and mixed precision.

## Cross-Domain Connections

- [[02 - Mathematics/Optimization/13 - Adam Derivation|Adam Derivation]] — the optimizer used in most pretraining.
- [[02 - Mathematics/Optimization/14 - Learning Rate Schedules|LR Schedules]] — the schedule used in pretraining.
- [[12 - Fine-Tuning/MOC|12 Fine-Tuning]] — adapting pretrained models (uses same techniques at smaller scale).
- [[10 - Model Architecture Research/MOC|10 Model Architecture Research]] — the models being trained.
- [[13 - Inference/MOC|13 Inference]] — what comes after training.

## Future Expansion (Iteration 7+)

- Alignment sub-domain: SFT, RLHF, RLAIF, Constitutional AI.
- Curriculum learning and data mixing.
- Synthetic data generation.
- Tokenizer training.
- Evaluation during pretraining.

## See Also

- [[12 - Fine-Tuning/MOC|12 Fine-Tuning]] — adapting pretrained models
- [[02 - Mathematics/Optimization/13 - Adam Derivation|Adam Derivation]]
- [[02 - Mathematics/Optimization/14 - Learning Rate Schedules|LR Schedules]]
- [[10 - Model Architecture Research/MOC|10 Model Architecture Research]]
