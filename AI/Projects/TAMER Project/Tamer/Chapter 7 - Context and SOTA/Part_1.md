# Chapter 7: Context and State-of-the-Art (SOTA)

## 1. SOTA Models and Benchmarks in Mathematical OCR

To understand why this codebase is structured this way, we must look at the giants in the field.

**The Benchmarks:**
Model performance is judged against standardized public datasets:
1.  **CROHME (Competition on Recognition of Online Handwritten Mathematical Expressions):** The gold standard. Extremely difficult, messy, real-world handwriting from students. 
2.  **HME100K:** A massive dataset of 100,000 messy handwritten equations collected from real educational settings in China.
3.  **Im2LaTeX-100K:** Clean, rendered, printed LaTeX. Considered an "easy" benchmark today.

**Current State-of-the-Art Approaches:**
1.  **Mathpix (Commercial/Proprietary):** The undisputed industry leader. It operates behind an API, utilizing massive, undisclosed proprietary datasets and likely heavy ensemble models.
2.  **Nougat (Meta):** Based on the Donut architecture (Transformer-based, completely OCR-free). Nougat parses entire scientific PDFs into markdown/LaTeX. It is brilliant for printed text but struggles with highly distorted, isolated handwriting.
3.  **Original TAMER (Tencent):** The paper your architecture is based on. They achieved SOTA on CROHME and HME100K by treating math recognition strictly as a visual-linguistic translation task, proving that CNNs were obsolete for this task.

**How Your Project Competes:**
Your implementation simplifies the original TAMER paper by removing the Training-Aware Module, but bolsters it with superior image processing (Top-Left Anchoring), strict dataset separation (`MultiDatasetBatchSampler`), and hardware-optimized BF16 training. By achieving exact spatial-token alignment and using a structural-aware loss function, your model is designed to reach near-SOTA accuracy on the hardest handwritten datasets (CROHME) using a fraction of the computational complexity required by massive multimodal models like Nougat.