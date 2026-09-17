---
tags: [datasets, sim-to-real]
---

# Sim-to-Real

> **Definition.** Transfer models trained on synthetic data to real-world applications.

## Pipeline

1. Generate synthetic data with rendering / procedural generation.
2. Apply domain randomization.
3. Train model on synthetic.
4. (Optional) Fine-tune on small real dataset.
5. Deploy on real.

## Why It's Hard

- **Domain gap**: synthetic looks different from real.
- **Noise**: real sensors are noisy.
- **Distribution shift**: real data may have variations not in synthetic.

## Strategies

- **Photorealistic rendering**: minimize domain gap.
- **Domain randomization**: cover real variations.
- **Domain adaptation**: align synthetic and real distributions.
- **Fine-tuning**: small real data to bridge the gap.

## In Buildings

- Train BIM generator on synthetic buildings, deploy on real.
- Train perception model on synthetic RGB-D, deploy on real scans.

See [[Domain Randomization]], [[Synthetic Generators]].

## Related Concepts

- [[Domain Randomization]]
- [[Synthetic Generators]]
- [[Real Datasets]]
