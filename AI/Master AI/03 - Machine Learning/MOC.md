---
tags: [moc, machine-learning]
iteration: 2
created: 2026-08-07
---

# 03 — Machine Learning MOC

> [!info] Classical ML + reinforcement learning. Reinforcement learning matters more than you might think — PPO is the foundation of RLHF, which aligned every modern chatbot.

## Reading Order

| #   | Note                                              | Sub-domain              | Purpose                                            |
|-----|---------------------------------------------------|-------------------------|----------------------------------------------------|
| 01  | [[01 - Bias Variance Tradeoff]]                   | Generalization          | Why models under/overfit; the fundamental tension. |
| 02  | [[02 - Linear and Logistic Regression]]           | Supervised              | The simplest models; the foundation.               |
| 03  | [[03 - Decision Trees and Gradient Boosting]]     | Supervised              | Still SOTA for tabular data.                       |
| 04  | [[04 - Clustering and Dimensionality Reduction]]  | Unsupervised            | K-means, PCA, t-SNE, UMAP.                         |
| 05  | [[05 - ML Evaluation Metrics]]                    | Evaluation              | Accuracy, F1, ROC, calibration.                    |
| 06  | [[06 - Regularization Techniques]]                | Generalization          | L1/L2, dropout, early stopping.                    |
| 07  | [[07 - MDPs and Bellman Equations]]               | Reinforcement Learning  | The RL formalism.                                  |
| 08  | [[08 - Q-Learning and DQN]]                       | Reinforcement Learning  | Value-based RL.                                    |
| 09  | [[09 - Policy Gradients and Actor Critic]]        | Reinforcement Learning  | Policy-based RL.                                   |
| 10  | [[10 - PPO Deep Treatment]]                       | Reinforcement Learning  | **Required reading before RLHF.**                  |

## Sub-Domains

- [[03 - Machine Learning/Supervised Learning/02 - Linear and Logistic Regression|Supervised Learning]] — notes 02–03
- [[03 - Machine Learning/Unsupervised Learning/04 - Clustering and Dimensionality Reduction|Unsupervised Learning]] — note 04
- [[03 - Machine Learning/Evaluation/05 - ML Evaluation Metrics|Evaluation]] — note 05
- [[03 - Machine Learning/Generalization/01 - Bias Variance Tradeoff|Generalization]] — notes 01, 06
- [[03 - Machine Learning/Reinforcement Learning/07 - MDPs and Bellman Equations|Reinforcement Learning]] — notes 07–10

## Why This Chapter Matters

- **Classical ML is still the right tool for many problems.** Tabular data, small datasets, interpretable models — gradient boosting beats deep learning here.
- **RL is the foundation of RLHF.** Without understanding PPO, you can't understand how ChatGPT was aligned.
- **Evaluation is its own skill.** Most ML failures are evaluation failures: wrong metric, leaked test set, uncalibrated probabilities.

## Reading Order Recommendation

### If you're new to ML
Read all 10 notes in order. ~4–6 weeks of part-time study.

### If you already know classical ML
Skip to note 07 (MDPs) and read 07–10 for the RL foundation you need for RLHF.

### If you only have time for one note
Read [[10 - PPO Deep Treatment]] — it's the prerequisite for understanding RLHF (chapter 12).

## See Also

- [[02 - Mathematics/MOC|02 Mathematics]] — the math behind ML
- [[04 - Neural Networks/MOC|04 Neural Networks]] — deep learning
- [[12 - Fine-Tuning/MOC|12 Fine-Tuning]] — where PPO is used (RLHF)
- [[11 - Training/MOC|11 Training]] — pretraining at scale
