# 00 - Master Index

> **Vault:** AI-Course (revised)
> **Total:** ~230 notes across 10 chapters
> **Goal:** Deep understanding over coverage — every concept explained with intuition, connected to its neighbors, and motivated by the problems it solves.

This is the navigation hub. Use it to find any chapter, sub-folder, or note. The vault is organized as a **learning graph**, not just a linear sequence — each note has prerequisite and connection links, so you can follow your own path.

---

## How to Use This Vault

### Linear path (recommended for first-time learners)

01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 10

This gives you the full foundations-to-modern-AI trajectory: math and Python → classical ML → neural networks → CNNs → image processing → sequence models → attention/Transformers → generative models.

### Non-linear paths (for targeted learning)

- **Want to understand Transformers?** → [[08 - Attention and Transformers]] (but read [[07 - Sequence Models and RNNs]] first for the motivation)
- **Want to understand ViT?** → [[08.3 - Vision Transformers]] (read [[08.2 - The Transformer Architecture]] and [[01. Introduction and Foundations of CNNs]] first)
- **Want evaluation metrics?** → [[03.6 - Model Evaluation]] (classification, regression, clustering, and CV metrics)
- **Want generative models?** → [[10 - Generative Models]] (autoencoders, VAEs, GANs, diffusion)
- **Want the math behind loss functions?** → [[07. Probability and Statistics for ML]] (MLE → MSE/BCE, MAP → L2 regularization)
- **Want tree-based models for tabular data?** → [[03.7 - Tree-Based Models]] (Decision Trees, Random Forests, XGBoost)

### Reading conventions

- Every note starts with a **Prerequisites** and **Connections** block — follow these to navigate.
- Notes end with **"What you should walk away with"** — the key takeaways.
- `[!NOTE]`, `[!TIP]`, `[!DANGER]` callouts highlight important points.
- `[[wikilinks]]` connect to related notes — click them to follow connections.

---

## Chapter Map

| # | Chapter | Sub-folders | Purpose |
| :--- | :--- | :---: | :--- |
| 01 | [[#01 - Foundations and Overview\|Foundations and Overview]] | 3 | AI/ML/DL hierarchy, math foundations, data science |
| 02 | [[#02 - Python and Data Tooling\|Python and Data Tooling]] | 4 | Python environment, programming, libraries, data cleaning |
| 03 | [[#03 - Machine Learning\|Machine Learning]] | 8 | Classical ML: regression, optimization, KNN, SVM, clustering, trees, dim reduction, evaluation |
| 04 | [[#04 - Neural Networks and Deep Learning Foundations\|Neural Networks and DL Foundations]] | 4 | Neuron basics, backprop deep dive, training dynamics, labs |
| 05 | [[#05 - Convolutional Neural Networks (CNN)\|Convolutional Neural Networks (CNN)]] | 8 | The deep-learning workhorse for images + advanced operators + modern CV tasks |
| 06 | [[#06 - Image Processing\|Image Processing]] | 6 | Classical digital image processing + bridge to CNNs |
| 07 | [[#07 - Sequence Models and RNNs\|Sequence Models and RNNs]] | 4 | RNNs, LSTMs, GRUs, Seq2Seq, Encoder-Decoder — **the bridge to Attention** |
| 08 | [[#08 - Attention and Transformers\|Attention and Transformers]] | 4 | The mechanism, the architecture, Vision Transformers, the encoder-decoder design space |
| 10 | [[#10 - Generative Models\|Generative Models]] | 4 | Autoencoders, VAEs, GANs, Diffusion — the generative AI foundation |
| 09 | [[#09 - Quizzes and Question Banks\|Quizzes and Question Banks]] | 3 | All quiz material for review |

---

## 01 - Foundations and Overview

### 01.1 - AI, ML, and DL Hierarchy
- [[01. Introduction to Machine Learning]]
- [[02. Types of Learning]]
- [[03. Deep Learning Definition and Context]]
- [[04. Machine Learning vs Deep Learning]]
- [[05. Evolution and History of Deep Learning]]
- [[06. Applications of Deep Learning]]
- [[07. Comparing Data Science, AI, ML, and BI]]
- [[08. Foundations of Machine Learning (Summary)]]

### 01.2 - Mathematical Foundations
- [[00. Linear Algebra Fundamentals]] — **NEW**: vectors, matrices, SVD, eigenvalues
- [[01. Mathematical Notation (ML Course)]]
- [[02. Mathematical Notation and Symbols]]
- [[03. Understanding the Math Notation - Chain Rule and wrt]]
- [[04. Partial vs. Ordinary Derivatives]]
- [[05. Derivatives, Power Rule, and the Chain Rule]]
- [[06. Gradients and Gradient Descent]]
- [[07. Probability and Statistics for ML]] — **NEW**: MLE, MAP, distributions, KL divergence
- [[08. Multivariate Calculus - Jacobians and Hessians]] — **NEW**: Jacobians, Hessians, second-order optimization

### 01.3 - Data Science Foundations
- [[01. Data Science Definition and Philosophy]]
- [[02. The Importance of Data-Driven Decision Making]]
- [[03. The Four Pillars of Data Science]]
- [[04. The Complete Data Science Workflow]]
- [[05. Careers and Roles in the Data Ecosystem]]
- [[06. Essential Technical and Soft Skills]]
- [[07. Exercise 1 - Identifying Applications and Roles]]

---

## 02 - Python and Data Tooling

### 02.1 - Python Environment Setup
- [[01. Python Language Overview]] → [[02. Installation and Distributions]] → [[03. IDEs and Development Environments]] → [[04. Virtual Environments and Package Management]] → [[05. Version Control with Git and GitHub]] → [[06. Project Structure and Best Practices]] → [[07. Exercise 2 - Hospital Data Project Setup]]

### 02.2 - Python Programming Essentials
- [[01. Variables, Operators, and Type Casting]] → [[02. Advanced Control Flow and Loops]] → [[03. Data Structures - Lists, Tuples, and Sets]] → [[04. Dictionaries and Key Value Management]] → [[05. Functions and Lambda Expressions]] → [[06. Object Oriented Programming (OOP) in Data Science]] → [[07. Iterators, Generators, and Memory Efficiency]] → [[08. Error Handling and Exception Management]] → [[09. Exercise 3 - Sales Project Logic and OOP]]

### 02.3 - Essential Python Libraries
- [[01. NumPy - Numerical Computation and Arrays]] → [[02. Pandas - Data Manipulation and Series]] → [[03. DataFrames - Deep Dive and Operations]] → [[04. Matplotlib - Static Data Visualization]] → [[05. Seaborn - Statistical Data Visualization]] → [[06. Interactive Plotting with Plotly]] → [[07. Exercise 4 - Temperature and Grade Analysis]]

### 02.4 - Data Cleaning and Preprocessing
- [[01. Handling Missing Data and Imputation Strategies]] → [[02. Duplicate Detection and Record Linkage]] → [[03. Outlier Detection and Treatment Methods]] → [[04. Feature Scaling and Normalization]] *(expanded)* → [[05. Categorical Encoding and Text Normalization]] *(expanded)* → [[06. Exercise 5 - Medical Dataset Pipeline]]

---

## 03 - Machine Learning

### 03.1 - Regression
- [[01. Introduction to Regression]] → [[02. Linear Regression from Scratch]] → [[03. Linear Regression (DL Perspective)]] → [[04. Logistic Regression]] → [[05. Regression Fundamentals (In Depth)]] → [[07. Lab - Guide Complet Régression Linéaire et Deep Learning (MNIST)]]

### 03.2 - Optimization Algorithms
- [[01. Gradient Descent Optimization (DL Course)]] → [[02. Loss Functions and Cost Optimization]] → [[06. Loss Functions and Error Calculation]] → [[07. Gradient Descent - The Update Rule and Convergence]] → [[08. Loss Functions and Optimizers Deep Dive]]

### 03.3 - K-Nearest Neighbors (KNN)
- [[01. K-Nearest Neighbors (KNN) - Comprehensive]]

### 03.4 - Support Vector Machines (SVM)
- [[01. SVM - Course Overview]] → [[02. Introduction and The Widest Street]] → [[03. The Mathematics of Separation]] → [[04. The Lagrangian Optimization]] → [[05. The Dual Representation and Dot Products]] → [[06. The Kernel Trick]]

### 03.5 - K-Means Clustering
- [[01. K-Means Clustering]]

### 03.6 - Model Evaluation
- [[01. Model Evaluation and Metrics]] — classification basics, confusion matrix
- [[02. Model Evaluation Metrics Beyond Accuracy]] — deep classification (precision, recall, F1, ROC-AUC)
- [[03. Regression Metrics - MAE, MSE, RMSE, R2, MAPE]] — **NEW**
- [[04. Clustering Metrics - Silhouette, Davies-Bouldin, ARI, NMI]] — **NEW**
- [[05. Computer Vision Metrics - IoU, mAP, Dice]] — **NEW**

### 03.7 - Tree-Based Models — **NEW FOLDER**
- [[01. Decision Trees - Splitting Criteria and Tree Construction]]
- [[02. Random Forests and Bagging]]
- [[03. Gradient Boosting and XGBoost]]

### 03.8 - Dimensionality Reduction — **NEW FOLDER**
- [[01. Principal Component Analysis (PCA)]]
- [[02. t-SNE and UMAP]]

---

## 04 - Neural Networks and Deep Learning Foundations

### 04.1 - Neural Network Basics
- [[01. Fundamentals of Neural Networks]] → [[02. Neural Network Architecture and Notation]] → [[03. Artificial Neural Networks (ANN) - Comprehensive]] → [[04. The Perceptron and the Chain Rule]] → [[05. Forward Propagation and Activation Functions]] → [[06. Activation Functions in Deep Learning]] → [[07. Multi-Layer Perceptron and Backpropagation]] → [[08. Data Preparation and MLP Implementation]]

### 04.2 - Backpropagation Deep Dive
- [[00. README - Backpropagation Module]] → [[01. Backpropagating to the Output Layer]] → [[02. Backpropagating to the Hidden Layer]] → [[03. Matrix Implementation and the Delta Weight Formula]] → [[04. Backpropagation and Gradient Flow in CNNs]]

### 04.3 - Training Dynamics and Stability
- [[01. Weight Initialization]] → [[02. Weight Initialization Techniques]] → [[03. The Vanishing and Exploding Gradient Problems]] → [[04. Hyperparameters and Network Configuration]] → [[05. Batch Normalization]] → [[06. Dropout and Regularization]] → [[07. Data Augmentation]]

### 04.4 - Labs
- [[01. TP2]] → [[02. TP3 - Data Cleaning, Normalization, and Encoding - Solution Guide]]

---

## 05 - Convolutional Neural Networks (CNN)

### Top-level
- [[00. CNN Mastery Roadmap]] → [[00. Course Overview]]

### 05.1 - Foundations and Philosophy
- [[01. Introduction and Foundations of CNNs]] → [[02. Core Architecture and Philosophy]] → [[03. The Bridge - From Basic Convolution to Learned Weights]] → [[04. Demystifying Tensors - Volumes, Depth, and Data Formats]] → [[05. Processing 3D Volumes, Depth Summation, and Biases]]

### 05.2 - Core Operators and Geometry *(consolidated from 12 → 7 files)*
- [[01. The Convolution Operation Deep Dive]] → [[02. The Mathematics of Receptive Fields and 1x1 Convolutions]] → [[03. Activation and Pooling Layers]] → [[04. Advanced Pooling Mechanisms and Global Average Pooling]] → [[05. The Output Spatial Dimension Formula]] → [[06. Padding - Mathematics, Edge Effects, and Valid vs Same]] → [[07. Strides - Skipping Pixels and Downsampling]]

### 05.3 - Architecture and Connectivity
- [[01. Local Connectivity and Parameter Sharing]] → [[02. Hierarchical Feature Extraction]] → [[04. The Fully Connected Layer and Flattening]] → [[05. Evolution of CNN Architectures]] → [[06. VGG16 Architecture Deep Dive]] → [[07. Inception Architecture Deep Dive]] → [[08. The Degradation Problem and Residual Connections]] → [[09. ResNet Bottleneck Blocks and Architectural Variants]]

### 05.4 - Training, Transfer Learning, and PyTorch
- [[01. Transfer Learning and Fine-Tuning]] → [[02. PyTorch Implementation Basics]] → [[03. PyTorch Advanced - VGG16 and Pre-trained Models]]

### 05.5 - Pipeline, Evaluation, and Interpretability
- [[01. The Full Training Pipeline End-to-End Checklist]] → [[02. Common Mistakes and How to Fix Them]] → [[03. Demystifying the Black Box - CNN Interpretability]] → [[04. Exercises Solved and Explained]]

### 05.6 - Chapter Summaries (Aggregated)
- Long-form reference notes on foundations, operators, architectures, normalization, transfer learning, and scaling.

### 05.7 - Advanced Operators — **NEW FOLDER**
- [[01. Advanced Convolutional Operators - Depthwise, Dilated, Transposed, Grouped]]

### 05.8 - Modern Computer Vision Tasks — **NEW FOLDER**
- [[01. Modern Computer Vision Tasks - Detection and Segmentation]]

---

## 06 - Image Processing

### 06.1 - Fundamentals of Digital Images
- [[1.1 What is a Digital Image]] *(expanded)* → [[1.2 Image Representation Types]] → [[1.3 Resolution and Bit Depth]] → [[1.4 Color Spaces and Models]] *(expanded)* → [[1.5 Image File Formats]] → [[1.6 Pixel Relationships and Distance Metrics]] → [[1.7 The Color Image Processing Pipeline]] *(NEW — Bayer, white balance, gamma)*

### 06.2 - Intensity Transformations and Histograms
- [[2.1 The Image Histogram]] → [[2.2 Point Processing Operations]] → [[2.3 Contrast Stretching]] → [[2.4 Histogram Equalization (HE)]] → [[2.5 Advanced Histogram Techniques]]

### 06.3 - Spatial Filtering and Neighborhood Processing
- [[3.1 The Mechanics of Spatial Filtering]] → [[3.2 Linear Smoothing Filters]] → [[3.3 Non-Linear Smoothing Filters]] → [[3.4 Edge Preserving Filters]] → [[3.5 Sharpening and Edge Detection]] *(expanded)* → [[3.6 Canny and LoG - Advanced Edge Detection]] *(NEW)* → [[3.7 Geometric Transformations and Interpolation]] *(NEW)* → [[3.8 Feature Descriptors - SIFT, SURF, ORB, HOG]] *(NEW)* → [[3.9 Image Pyramids and Multi-Scale Representation]] *(NEW)* → [[3.10 The Hough Transform]] *(NEW)*

### 06.4 - Frequency Domain and Restoration
- [[4.1 Introduction to the Frequency Domain]] *(expanded)* → [[4.2 The Fourier Transform]] *(expanded)* → [[4.3 Frequency Domain Filtering]] *(expanded)* → [[4.4 Image Degradation and Noise Models]] *(expanded)* → [[4.5 Image Quality Metrics]] *(expanded — SSIM, LPIPS)*

### 06.5 - Morphological Processing and Segmentation
- [[5.1 Mathematical Morphology Basics]] → [[5.2 Erosion and Dilation]] → [[5.3 Opening and Closing]] → [[5.4 Morphological Algorithms]] *(expanded — Zhang-Suen, Hit-or-Miss, grayscale morphology)* → [[5.5 Deep Learning for Imaging]] → [[5.6 The Classical-to-Deep Bridge]] → [[5.7 Thresholding and Otsu's Method]] *(NEW)* → [[5.8 Watershed Segmentation]] *(NEW)* → [[5.9 Connected Components and Region Properties]] *(NEW)*

### 06.6 - Concepts (ML Perspective)
- [[01. Convolution]] → [[02. Gabor Filters]] → [[05. The Fourier Transform in Imaging]]

### 06.7 - Quiz
- [[Q1]] / [[Q2]] / [[Q3]] / [[Q4]] / [[Q5]] / [[Q6]]

---

## 07 - Sequence Models and RNNs — **NEW CHAPTER**

### 07.1 - Motivation and Recurrence
- [[01. Why Sequence Models - The Limits of Feedforward Networks]] → [[02. The Recurrent Neuron - Unrolling Through Time]] → [[03. Backpropagation Through Time (BPTT)]] → [[04. The Vanishing and Exploding Gradient Problem in RNNs]]

### 07.2 - LSTM and GRU
- [[01. LSTM - Gates as Learned Traffic Controllers]] → [[02. GRU - Simplifying the LSTM]] → [[03. LSTM vs GRU - When to Use Which]]

### 07.3 - Sequence to Sequence and Encoder-Decoder
- [[01. The Encoder-Decoder Pattern - Conditional Generation]] → [[02. Teacher Forcing and Exposure Bias]] → [[03. Beam Search and Decoding Strategies]]

### 07.4 - Sequence Modeling Pitfalls and Limits
- [[01. The Bottleneck Problem - Why One Vector Is Not Enough]] → [[02. Long-Range Dependencies and Why RNNs Struggle]] → [[03. From RNNs to Attention - The Historical Bridge]]

---

## 08 - Attention and Transformers — **NEW CHAPTER**

### 08.1 - The Attention Mechanism
- [[01. Attention as Soft Lookup - From Bahdanau to Dot-Product]] → [[02. Queries Keys and Values - The Database Analogy]] → [[03. Scaled Dot-Product Attention - Why the Square Root]] → [[04. Multi-Head Attention - Parallel Relationship Patterns]]

### 08.2 - The Transformer Architecture
- [[01. Self-Attention - When the Sequence Attends to Itself]] → [[02. Positional Encoding - Injecting Order Into a Set]] → [[03. The Transformer Encoder Block]] → [[04. The Transformer Decoder Block - Masking and Cross-Attention]] → [[05. The Full Transformer - Assembling the Pieces]]

### 08.3 - Vision Transformers
- [[01. From Words to Patches - How ViT Tokenizes an Image]] → [[02. The CLS Token and Why It Works]] → [[03. Inductive Bias - CNNs vs ViTs and Why ViTs Need More Data]] → [[04. ViT Architecture and Design Decisions]]

### 08.4 - Encoder, Decoder, and the Design Space
- [[01. The Encoder-Decoder Design Space - BERT vs GPT vs T5]] → [[02. The Information Bottleneck and Latent Space]] → [[03. Autoregressive vs Parallel Encoding]] → [[04. Choosing the Right Architecture for the Task]]

---

## 10 - Generative Models — **NEW CHAPTER**

### 10.1 - Autoencoders
- [[01. The Autoencoder - Compression as Learning]] → [[02. Denoising Autoencoders and Sparse Autoencoders]]

### 10.2 - Variational Autoencoders
- [[01. From Autoencoder to VAE - Learning a Distribution]] → [[02. The Reparameterization Trick]] → [[03. The KL Divergence Loss]]

### 10.3 - GANs
- [[01. The Adversarial Game - Generator vs Discriminator]] → [[02. Training Dynamics and Mode Collapse]] → [[03. Wasserstein GANs and Modern Variants]]

### 10.4 - Diffusion Models
- [[01. The Forward Process - Adding Noise]] → [[02. The Reverse Process - Learning to Denoise]] → [[03. Score-Based and Latent Diffusion]]

---

## 09 - Quizzes and Question Banks

### 09.1 - Deep Learning - Chapter 1 (Introduction to DL)
- Q1–Q12 covering DL definitions, ML vs DL, history, applications, GD, loss functions, linear/logistic regression, perceptron, activation functions, MLP, data preparation

### 09.2 - Deep Learning - Chapter 2 (CNN)
- Q1–Q27 covering CNN foundations, convolution, receptive fields, pooling, architectures (VGG, Inception, ResNet), backprop in CNNs, weight init, vanishing gradients, BatchNorm, dropout, augmentation, transfer learning, PyTorch, pipeline, mistakes, interpretability, exercises

### 09.3 - Question Series
- [[Qs1]] / [[Qs3]] / [[Qs4]]

---

## Cross-Reference Map (Topic → Where to Find It)

| Topic | Primary location | Also see |
| :--- | :--- | :--- |
| AI / ML / DL definitions | 01.1 | 01.3 |
| Math notation | 01.2/01–06 | 03.2 (applied) |
| Linear algebra | **01.2/00** | 03.8 (PCA uses SVD) |
| Probability, MLE, MAP | **01.2/07** | 03.2 (loss functions), 10.2 (VAE KL) |
| Jacobians, Hessians | **01.2/08** | 07.1 (BPTT), 04.2 (backprop) |
| Gradient descent | 03.2 | 04.2, 07.1 |
| Backpropagation | 04.2 | 03.2, 07.1 (BPTT) |
| Activation functions | 04.1/06 | 08.2 (GELU in Transformers) |
| Weight initialization | 04.3/01–02 | |
| Vanishing gradients | 04.3/03 | **07.1/04** (RNN version) |
| BatchNorm / LayerNorm | 04.3/05 | 08.2 (LayerNorm in Transformers) |
| Dropout / regularization | 04.3/06 | |
| CNN foundations | 05.1 | 05.6 (synthesized) |
| CNN convolution | 05.2 | 06.6 (ML angle), **06.5/5.6** (bridge) |
| CNN architectures | 05.3 | 05.6 |
| **Advanced CNN operators** | **05.7** | 05.3 (MobileNet, DeepLab mentions) |
| **Object detection / segmentation** | **05.8** | 06.5/5.5 (U-Net) |
| PyTorch implementation | 05.4 | |
| CNN training pipeline | 05.5 | |
| Model evaluation (classification) | 03.6/01–02 | |
| **Regression metrics** | **03.6/03** | |
| **Clustering metrics** | **03.6/04** | |
| **CV metrics (IoU, mAP, Dice)** | **03.6/05** | 05.8 |
| Image processing fundamentals | 06.1 | 06.6 |
| Image filtering | 06.3 | 06.4 |
| Classical ↔ deep bridge | **06.5/5.6** | 05.1/03 |
| **RNNs, LSTMs, GRUs** | **07** | 04.3/03 (vanishing gradients) |
| **Encoder-Decoder (RNN)** | **07.3** | 08.4 (Transformer version) |
| **Attention mechanism** | **08.1** | 07.4 (the motivation) |
| **Transformer architecture** | **08.2** | |
| **Vision Transformers (ViT)** | **08.3** | 05.1/01 (CNN comparison) |
| **BERT vs GPT vs T5** | **08.4** | |
| **Autoencoders, VAEs** | **10.1–10.2** | 08.4/02 (latent space) |
| **GANs** | **10.3** | |
| **Diffusion models** | **10.4** | |
| **Tree-based models** | **03.7** | |
| **PCA, t-SNE, UMAP** | **03.8** | 01.2/00 (linear algebra) |
| Quizzes | 09 | 06.7 (image processing) |

---

## The Learning Trajectory

This vault tells a story: **from classical ML to modern AI, each architecture a response to the limitations of the previous one.**

```
Linear/Logistic Regression → MLPs → CNNs (images)
                                   → RNNs (sequences) → Encoder-Decoder → Bottleneck
                                                                          ↓
                                                                    Attention → Transformer
                                                                          ↓
                                                                    ViT (vision) → ConvNeXt
                                                                          ↓
                                                                    BERT / GPT / T5
                                                                          ↓
                                                                    Generative models: VAE → GAN → Diffusion
```

Every node in this graph is a response to a limitation of the previous node. Understanding the limitations — not just the architectures — is what this vault optimizes for.

---

*For the full merge report and structural history, see [[README]].*
