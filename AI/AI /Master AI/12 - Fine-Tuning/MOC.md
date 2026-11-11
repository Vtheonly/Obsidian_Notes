---
tags: [fine-tuning, moc]
iteration: 2
created: 2026-08-07
---

# 12 — Fine-Tuning MOC

> [!info] How to adapt a pretrained LLM to your task.

## Reading Order

| #   | Note                                              | Sub-domain          | Purpose                                            |
|-----|---------------------------------------------------|---------------------|----------------------------------------------------|
| 01  | [[01 - LoRA]]                                     | PEFT                | The dominant PEFT method.                          |
| 02  | [[02 - QLoRA]]                                    | PEFT                | 4-bit quantized LoRA; fine-tune on consumer GPUs.  |
| 03  | [[03 - Instruction Tuning and Chat Templates]]    | Instruction Tuning  | SFT; chat templates.                               |
| 04  | [[04 - DPO Derivation]]                           | DPO                 | The simpler alternative to PPO.                    |
| 05  | [[05 - RLHF with PPO]]                            | RLHF                | PPO-based alignment; what DPO replaces.            |

## Sub-Domains

- [[12 - Fine-Tuning/PEFT/01 - LoRA|PEFT]] — notes 01–02
- [[12 - Fine-Tuning/Instruction Tuning/03 - Instruction Tuning and Chat Templates|Instruction Tuning]] — note 03
- [[12 - Fine-Tuning/DPO/04 - DPO Derivation|DPO]] — note 04
- [[12 - Fine-Tuning/RLHF/05 - RLHF with PPO|RLHF]] — note 05
- [[12 - Fine-Tuning/MOC|Distillation]] — (planned)

## The Standard Pipeline

```mermaid
graph LR
  Base[Base Model] --> SFT[SFT 03]
  SFT --> PrefOpt[Preference Optimization: DPO 04 or RLHF 05]
  PrefOpt --> Merge[Merge LoRA]
  Merge --> Quantize[Quantize for Inference]
  Quantize --> Serve[Serve with vLLM]
```

## See Also

- [[11 - Training/MOC|11 Training]] — pretraining (what fine-tuning builds on)
- [[13 - Inference/MOC|13 Inference]] — running the fine-tuned model
- [[08 - LLMs/MOC|08 LLMs]]
