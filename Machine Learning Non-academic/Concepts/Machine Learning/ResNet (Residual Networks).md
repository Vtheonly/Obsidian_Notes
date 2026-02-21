# ResNet (Residual Networks)

## What is ResNet?

**ResNet** (Residual Network) is a family of deep convolutional neural network architectures introduced to make very deep networks trainable by using **skip connections** (also called shortcut connections). It solved the problem that simply stacking more layers often made training **worse** (not better) due to vanishing/exploding gradients and optimization difficulties.

---

## The Problem: Why Do We Need ResNet?

```mermaid
flowchart TB
    subgraph Problem["The Problem with Deep Networks"]
        D20["20 Layers<br/>✓ Works well"]
        D50["50 Layers<br/>✗ Worse performance!"]
        D100["100+ Layers<br/>✗ Training fails!"]
    end
    
    D20 --> D50 --> D100
    
    style D20 fill:#90EE90
    style D50 fill:#FFA07A
    style D100 fill:#FF6347
```

**Paradox:** Deeper networks should perform better, but they often perform **worse** due to:
- **Vanishing gradients** - early layers don't learn
- **Degradation problem** - even with good initialization, deeper = harder to optimize

---

## Intuition / Motivation

When you stack many layers, it becomes hard for SGD to update weights so deeper layers improve performance. ResNet puts **identity shortcuts** that let gradients and signals flow directly through the network.

### Key Insight
Instead of forcing a block to learn a full mapping **H(x)**, you ask it to learn the **residual**:

$$F(x) = H(x) - x$$

Then the block output is:

$$\text{output} = F(x) + x$$

**If the block cannot improve on identity**, it can learn F(x) ≈ 0 so the block behaves like an identity — this stabilizes very deep nets.

---

## The Solution: Skip Connections

```mermaid
flowchart TB
    subgraph ResBlock["Residual Block"]
        X["Input x"]
        F1["Weight Layer 1<br/>+ ReLU"]
        F2["Weight Layer 2"]
        Add["+ Add"]
        ReLU["ReLU"]
        Out["Output: F(x) + x"]
        
        X --> F1
        F1 --> F2
        F2 --> Add
        Add --> ReLU
        ReLU --> Out
        
        X -.->|"Skip Connection<br/>(Identity)"| Add
    end
    
    style X fill:#87CEEB
    style Add fill:#90EE90
    style Out fill:#98FB98
```

---

## Plain Network vs ResNet

```mermaid
flowchart TB
    subgraph Plain["Plain Network (No Skip)"]
        P1["Input x"]
        P2["Conv + ReLU"]
        P3["Conv"]
        P4["Output H(x)"]
        
        P1 --> P2 --> P3 --> P4
    end
    
    subgraph ResNet["ResNet (With Skip)"]
        R1["Input x"]
        R2["Conv + ReLU"]
        R3["Conv: F(x)"]
        R4["+ Add"]
        R5["Output: F(x) + x"]
        
        R1 --> R2 --> R3 --> R4 --> R5
        R1 -.->|Skip| R4
    end
    
    style P4 fill:#FFA07A
    style R5 fill:#90EE90
```

---

## The Residual Block (Two Variants)

### Basic Block (ResNet-18 / ResNet-34)

```mermaid
flowchart TB
    subgraph Basic["Basic Block"]
        IN["Input"]
        C1["3×3 Conv<br/>+ BN + ReLU"]
        C2["3×3 Conv<br/>+ BN"]
        ADD["+ Add Input"]
        OUT["ReLU<br/>Output"]
        
        IN --> C1 --> C2 --> ADD --> OUT
        IN -.->|Identity| ADD
    end
    
    style ADD fill:#90EE90
```

- Two 3×3 convolutions (Conv-BN-ReLU), then add the input (x)
- If spatial or channel dimensions change (stride >1 or different channels), a **projection** (1×1 conv) is applied to x to match shapes

### Bottleneck Block (ResNet-50/101/152)

```mermaid
flowchart TB
    subgraph Bottleneck["Bottleneck Block (1×1, 3×3, 1×1 convs)"]
        IN["Input: 256 channels"]
        C1["1×1 Conv<br/>Reduce to 64"]
        C2["3×3 Conv<br/>Process (64)"]
        C3["1×1 Conv<br/>Expand to 256"]
        ADD["+ Add"]
        OUT["Output: 256 channels"]
        
        IN --> C1 --> C2 --> C3 --> ADD --> OUT
        IN -.->|Skip| ADD
    end
    
    style C1 fill:#87CEEB
    style C2 fill:#98FB98
    style C3 fill:#87CEEB
```

- 1×1 conv reduces channels → 3×3 conv processes → 1×1 conv expands channels
- Reduces computation while allowing deeper models

---

## Why Skip Connections Help (Gradient View)

```mermaid
flowchart LR
    subgraph Gradient["Gradient Flow Benefits"]
        GC["Gradient can flow<br/>directly through skip"]
        GM["Derivative of addition = 1<br/>for shortcut path"]
        GL["Deeper layers receive<br/>stronger learning signal"]
    end
    
    GC --> GM --> GL
    
    style GL fill:#90EE90
```

### 1. **Gradient Highway**
- Skip connection acts as a "gradient superhighway"
- Gradients flow backward without being multiplied by small numbers
- Derivative of addition is 1 for the shortcut path

### 2. **Easy Identity Learning**
- If the best solution is to pass input unchanged, network can learn F(x) = 0
- Then H(x) = 0 + x = x (identity mapping)

### 3. **Solves Degradation Problem**
- Adding more layers doesn't hurt performance
- Network can always learn to ignore extra layers if needed

---

## ResNet Versions and Differences

```mermaid
graph LR
    subgraph Variants["ResNet Variants"]
        R18["ResNet-18<br/>Basic Block"]
        R34["ResNet-34<br/>Basic Block"]
        R50["ResNet-50<br/>Bottleneck ★"]
        R101["ResNet-101<br/>Bottleneck"]
        R152["ResNet-152<br/>Bottleneck"]
    end
    
    R18 --> R34 --> R50 --> R101 --> R152
    
    style R50 fill:#90EE90
```

| Model | Layers | Block Type | Use Case |
|-------|--------|------------|----------|
| ResNet-18 | 18 | Basic | Small datasets, fast training |
| ResNet-34 | 34 | Basic | Medium complexity tasks |
| **ResNet-50** | 50 | Bottleneck | **Most popular, good balance** |
| ResNet-101 | 101 | Bottleneck | Complex tasks, more compute |
| ResNet-152 | 152 | Bottleneck | Research, maximum accuracy |

### ResNet-v2 (Pre-activation)
- Reorders block as **BN → ReLU → Conv**
- Helps optimization and generalization in very deep models

---

## ResNet vs Previous Architectures

```mermaid
flowchart TB
    subgraph Comparison["Evolution of Deep Networks"]
        VGG["VGG (2014)<br/>Very deep but slow<br/>No skip connections"]
        ResNet["ResNet (2015)<br/>Deeper AND faster<br/>Skip connections ✓"]
        DenseNet["DenseNet (2017)<br/>Dense connections<br/>Even better gradient flow"]
    end
    
    VGG --> ResNet --> DenseNet
    
    style ResNet fill:#90EE90
```

---

## Practical Details / Training Tips

```mermaid
mindmap
    root((ResNet Training))
        Normalization
            BatchNorm after Conv
            Essential for ResNets
        Initialization
            He/Kaiming init
            Standard for ReLU nets
        Learning Rate
            Step decay
            Cosine annealing
            Warmup
        Skip Connection
            Identity if same shape
            Projection 1×1 if changed
        Transfer Learning
            Remove final FC
            Attach your head
```

| Tip | Details |
|-----|---------|
| **BatchNorm** | Use after convolutions (ResNets rely on it) |
| **Initialization** | He initialization (Kaiming) is standard |
| **Learning Rate** | Typical schedules: step decay, cosine, warmup |
| **Projection** | If channels/stride change, use 1×1 conv in shortcut |
| **Transfer Learning** | Remove final FC layer and attach your custom head |

---

## Common Uses

```mermaid
flowchart TB
    subgraph Uses["ResNet Applications"]
        IC["Image Classification<br/>(ImageNet)"]
        DET["Detection Backbones<br/>(Faster R-CNN, Mask R-CNN)"]
        SEG["Segmentation<br/>(FCN, DeepLab)"]
        TL["Transfer Learning<br/>(Vision & Multi-modal)"]
        NV["Non-Vision Domains<br/>(Deep feedforward nets)"]
    end
    
    style IC fill:#90EE90
    style TL fill:#98FB98
```

- **Image classification** (ImageNet)
- **Detection and segmentation backbones** (Faster R-CNN, Mask R-CNN)
- **Transfer learning backbone** in many vision and multi-modal architectures
- **Non-vision domains** where very deep feedforward nets are helpful

---

## Strengths and Limitations

### Strengths ✓

| Strength | Explanation |
|----------|-------------|
| **Elegant Design** | Simple trick with outsized impact — fundamentally changed deep learning |
| **Robust Backbone** | Very reliable for transfer learning |
| **Scalable** | Scales to deep models (100+ layers) while remaining trainable |
| **Must-Know Baseline** | Understanding residual connections is essential for modern architectures |

### Limitations ✗

| Limitation | Explanation |
|------------|-------------|
| **Compute Heavy** | Still heavy compute for large models |
| **Newer Architectures** | Swin, ConvNeXt, Vision Transformers can outperform ResNets on some tasks |
| **May Need Modifications** | Pre-activation, layer scaling, improved normalization can provide better performance |

---

## Key Takeaways

```mermaid
mindmap
    root((ResNet))
        Core Idea
            Skip Connections
            Learn Residual F(x)
            Output = F(x) + x
        Benefits
            Train Very Deep Networks
            Solve Vanishing Gradients
            Easy Identity Learning
        Variants
            ResNet-18 to ResNet-152
            Basic vs Bottleneck Blocks
            Pre-activation ResNet v2
        Impact
            Won ImageNet 2015
            152 layers trained
            Foundation for many architectures
```

---

## Quick Memory Aid

| Term | Meaning |
|------|---------|
| **ResNet** | Residual Network with skip connections |
| **Skip Connection** | Direct path that adds input to output |
| **Residual** | What the network learns (F(x) = H(x) - x) |
| **Bottleneck** | 1×1 → 3×3 → 1×1 conv block for efficiency |
| **Basic Block** | Two 3×3 convs (ResNet-18/34) |
| **Projection** | 1×1 conv to match dimensions when needed |

**ResNet = Skip connections let gradients flow → Train 100+ layers successfully!**