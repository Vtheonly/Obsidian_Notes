---
tags: [fine-tuning, instruction-tuning, sft, chat-templates]
iteration: 12
created: 2026-08-07
last_updated: 2026-08-08
aliases: [Instruction Tuning, SFT, Chat Templates]
---

# 03 - Instruction Tuning and Chat Templates

> [!info] TL;DR
> SFT (supervised fine-tuning) on instruction-response pairs turns a base LLM (which only predicts next tokens) into a chat model (which follows instructions). Chat templates format conversations consistently. The bridge between pretraining and aligned chat models.

## What Instruction Tuning Does

A pretrained base LLM continues text: prompt "The capital of France is" → completion " Paris, which is known for..."

An instruction-tuned model responds to instructions: prompt "What is the capital of France?" → response "The capital of France is Paris."

The transformation: supervised fine-tuning on (instruction, response) pairs. The model learns to treat the input as an instruction to follow, not text to continue.

## The SFT Training Loop

1. Collect (instruction, response) pairs — usually 10k–1M examples.
2. Format each as a single sequence using a chat template.
3. Train with standard CLM loss, but **only compute loss on the response tokens** (mask the instruction).

```python
def format_and_mask(example, tokenizer):
    text = tokenizer.apply_chat_template(
        [{"role": "user", "content": example["instruction"]},
         {"role": "assistant", "content": example["response"]}],
        tokenize=False,
    )
    full_ids = tokenizer(text, return_tensors="pt").input_ids[0]
    
    # Find where the assistant response starts; mask everything before
    prompt_text = tokenizer.apply_chat_template(
        [{"role": "user", "content": example["instruction"]}],
        tokenize=False, add_generation_prompt=True,
    )
    prompt_ids = tokenizer(prompt_text, return_tensors="pt").input_ids[0]
    
    labels = full_ids.clone()
    labels[:len(prompt_ids)] = -100  # ignore in loss
    return {"input_ids": full_ids, "labels": labels}
```

## Chat Templates

Each model has its own chat template — a way to format conversations into a single string the model was trained on. Examples:

### ChatML (used by many models, including Qwen, some Mistral)
```
<|im_start|>user
Hello!<|im_end|>
<|im_start|>assistant
Hi there!<|im_end|>
```

### Llama 3
```
<|begin_of_text|><|start_header_id|>user<|end_header_id|>

Hello!<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Hi there!<|eot_id|>
```

### Mistral
```
[INST] Hello! [/INST] Hi there!</s>
```

**Critical**: each model expects its own template. Using the wrong template causes silent quality degradation — the model produces reasonable-sounding but suboptimal responses.

Use `tokenizer.apply_chat_template(messages)` to apply the correct template automatically.

## Instruction Datasets

### Open-source datasets
- **OpenAssistant**: ~150k human-written conversations.
- **Alpaca / Vicuna**: GPT-3.5-generated instructions (52k).
- **Dolly**: Databricks human-written (15k).
- **OpenHermes**: large synthetic (1M).
- **UltraChat**: large synthetic (1.5M).
- **FLAN**: Google's instruction tuning collection.

### Commercial / private
- **InstructGPT / GPT-4**: human labelers + RLHF.
- **Anthropic HH-RLHF**: helpfulness + harmlessness.
- Most frontier models use large proprietary SFT datasets.

## Quality Considerations

- **Diversity matters**: vary instructions, response lengths, topics.
- **No contradictions**: don't include conflicting instructions ("be brief" + "explain in detail").
- **No harmful content** (if you want a safe model): filter or label carefully.
- **Format consistency**: responses should follow a consistent style.
- **Synthetic data can work** — many top open models are trained mostly on synthetic data (GPT-4-generated).

## Why This Matters for AI

- Instruction tuning is **the** step that turns a pretrained model into a useful chatbot. Without it, LLMs are just text completers.
- The shift from "few examples in prompt" (ICL) to "fine-tuned on instructions" was the second big LLM shift (after pretraining).
- For most production use cases, you start with an instruction-tuned model (e.g., Llama-3-8B-Instruct, not Llama-3-8B).
- For custom fine-tuning, instruction tuning is the foundation — DPO/RLHF build on top.

## Production Implications

- **Use Instruct versions of models** for chat / agentic use cases. Base models are for research or continued pretraining.
- **Always apply the correct chat template**. HuggingFace tokenizers do this automatically via `apply_chat_template`.
- **For custom SFT**, use a framework like TRL (HuggingFace), Axolotl, or Unsloth. They handle the formatting and loss masking correctly.
- **Don't over-train**. SFT typically needs only 1–3 epochs on 10k–100k examples. More = overfitting.
- **Use LoRA** for SFT — full fine-tuning is rarely needed and expensive.

## Common Pitfalls

- **Using a base model for chat** — produces completions, not responses. Use Instruct versions.
- **Wrong chat template** — silent quality loss. Always use `apply_chat_template`.
- **Forgetting to mask instruction tokens in loss** — model learns to "predict" the instruction, which is wasteful and can hurt quality.
- **Bad SFT data** — contradictions, low quality, harmful content all leak into the model.
- **Too many epochs** — overfits; the model produces templated, repetitive responses.
- **Wrong LR for SFT** — typically 1e-5 to 5e-5 for full FT, 1e-4 to 5e-4 for LoRA. Higher than pretraining LR.

## Further Reading

- Ouyang et al. (2022), *Training language models to follow instructions with human feedback* (InstructGPT).
- Wang et al. (2022), *Self-Instruct: Aligning Language Models with Self-Generated Instructions*.
- Taori et al. (2023), *Stanford Alpaca*.

## See Also

- [[01 - LoRA]]
- [[02 - QLoRA]]
- [[04 - DPO Derivation]]
- [[08 - LLMs/MOC|LLMs MOC]]
- [[12 - Fine-Tuning/MOC|Fine-Tuning MOC]]


## Interview Questions

1. **Q: What is the difference between a base model and an instruction-tuned model?**
   A: A base model continues text: "The capital of France is" → " Paris, which is known for...". An instruction-tuned model responds to instructions: "What is the capital of France?" → "The capital of France is Paris." The transformation is SFT on (instruction, response) pairs. Always use Instruct versions for chat/agentic use cases.

2. **Q: Why do you mask the instruction tokens in the loss?**
   A: You only want the model to learn to *generate* responses, not to *predict* instructions. If you compute loss on instruction tokens, the model wastes capacity learning to generate the user's input. Mask instruction tokens with -100 (PyTorch's ignore_index) so only response tokens contribute to the loss.

3. **Q: What is a chat template and why does using the wrong one cause silent quality loss?**
   A: Each model has its own format for conversations (ChatML, Llama-3 format, Mistral [INST] format). The model was trained on its specific template. Using the wrong template means the model sees input in a format it wasn't trained on — it still produces reasonable-sounding output but at lower quality. Always use `tokenizer.apply_chat_template(messages)`.

4. **Q: How many examples do you need for SFT?**
   A: Typically 10K-100K high-quality examples for 1-3 epochs. More isn't better — over-training causes the model to produce templated, repetitive responses. Quality matters more than quantity: 10K diverse, well-formatted examples beat 100K mediocre ones.

5. **Q: What LR should you use for SFT?**
   A: Full fine-tuning: 1e-5 to 5e-5 (lower than pretraining because the model is already good). LoRA: 1e-4 to 5e-4 (higher because LoRA params start from zero). DPO: 5e-7 to 5e-6 (much lower — preference loss is sharp). Always sweep on a short run.

6. **Q: Can you do SFT with synthetic data (GPT-4-generated)?**
   A: Yes — many top open models (OpenHermes, Tulu) are trained mostly on synthetic data. Key considerations: (1) diversity — vary instructions, response lengths, topics; (2) no contradictions; (3) format consistency; (4) filter for quality (some synthetic data is bad). Synthetic data is scalable and cheap; quality control is the bottleneck.

## Connection to Other Concepts

- [[12 - Fine-Tuning/PEFT/01 - LoRA|LoRA]] — usually combined with SFT.
- [[12 - Fine-Tuning/PEFT/02 - QLoRA|QLoRA]] — memory-efficient SFT.
- [[12 - Fine-Tuning/DPO/04 - DPO Derivation|DPO]] — builds on top of SFT.
- [[12 - Fine-Tuning/RLHF/05 - RLHF with PPO|RLHF]] — alternative alignment.
- [[08 - LLMs/Capabilities/04 - In-Context Learning|In-Context Learning]] — SFT turns ICL into consistent behavior.
- [[05 - NLP Fundamentals/Tokenization/01 - Tokenization Overview|Tokenization Overview]] — chat templates are tokenization-level.
