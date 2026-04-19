# Chapter 2: Data Representation and Caching Physics

---

## Chapter Introduction

Before any neural network can learn, the raw data must be transformed into a format suitable for GPU computation. This chapter addresses the practical engineering challenges of preparing mathematical formula images for training, with particular emphasis on the memory constraints that dominate real-world deep learning workflows.

The first major problem is **batching**: PyTorch requires all images in a batch to have identical dimensions, but mathematical formulas come in wildly different aspect ratios. A short fraction like $\frac{1}{2}$ produces a roughly square image, while a long polynomial can produce an image 20 times wider than it is tall. Naive resizing destroys the stroke geometry that the model needs to recognize individual symbols. TAMER's solution is **aspect-ratio-preserving resize with white padding**: scale uniformly to fit within a target bounding box (256 x 1024), then center the result with white fill.

The second major problem is **memory management**. In Jupyter/Kaggle notebook environments, Python's reference counting garbage collector can fail to free large objects that remain in the global namespace. Storing 50,000 PIL images in a list consumes ~150 GB of RAM, and rerunning the cell creates a second list before the first is freed, causing immediate OOM crashes. TAMER solves this with a **disk-backed streaming architecture** using JSONL format — images are processed one at a time, saved to disk immediately, and only their file paths (strings consuming ~200 bytes each) are kept in memory. This reduces RAM usage by a factor of ~30,000x.

The chapter also covers the **path resolution bug** that causes re-sanitization when relative paths resolve differently across kernel restarts, and the critical importance of using `os.path.abspath()` throughout the codebase.

Finally, we examine **data augmentation theory**: why augmentation prevents overfitting by expanding the effective training distribution, and how TAMER's specific augmentation pipeline (CoarseDropout, ShiftScaleRotate, GaussianNoise, GridDistortion) simulates real-world image degradation to build model robustness.

### Sections in this Chapter

| Section | Title | Key Topics |
|---------|-------|------------|
| 1 | Image Processing for OCR Constraints | Aspect-ratio-preserving resize, padding strategy, worked examples for tall/wide/extreme images |
| 2 | Python Memory Leaks and The OOM Caching Bug | Reference counting GC, JSONL streaming architecture, path resolution bugs, string path pattern |
| 3 | Data Augmentation Theory | Overfitting prevention, CoarseDropout/Cutout, ShiftScaleRotate, GaussianNoise, GridDistortion, train-only augmentation |

---
