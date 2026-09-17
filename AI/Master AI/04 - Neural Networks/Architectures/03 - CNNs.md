---
tags: [neural-networks, cnn, convolution, vision]
iteration: 9
created: 2026-08-07
last_updated: 2026-08-08
aliases: [CNNs, Convolutional Neural Networks]
---

# 03 - CNNs (Convolutional Neural Networks)

> [!info] TL;DR
> CNNs use **convolution** — sliding a small filter across the input — to exploit spatial locality and translation invariance. Dominant for vision from 1998 (LeNet) to 2020 (Vision Transformer). Still important for efficient vision, video, and as the conceptual ancestor of "sliding window attention" in modern Transformers.

## The Core Idea: Convolution

A **convolutional layer** slides a small filter (kernel) across the input, computing dot products at each position:

```
Input (5x5):        Filter (3x3):      Output (3x3):
1 2 3 4 5           1 0 -1             (sum of element-wise products)
6 7 8 9 0           1 0 -1
1 2 3 4 5           1 0 -1
6 7 8 9 0
1 2 3 4 5
```

The same filter is shared across all positions. This is the key difference from a dense layer.

## Why Convolutions Work for Images

### 1. Spatial locality
Nearby pixels are correlated (an edge, a texture). A small filter (3×3, 5×5) captures local patterns efficiently. Dense layers would mix all pixels globally — wasteful and noisy.

### 2. Translation invariance
A cat is a cat whether it's in the top-left or bottom-right of the image. By sharing the filter across positions, the CNN recognizes the same pattern anywhere.

### 3. Parameter efficiency
A 3×3 conv on a 224×224 image has 9 parameters (per filter). A dense layer connecting all pixels would have $224 \times 224 \approx 50$k parameters. CNNs use far fewer parameters for the same input.

### 4. Hierarchical features
Stacking conv layers builds a feature hierarchy: edges → textures → parts → objects. Early layers learn simple patterns; later layers compose them into complex ones.

## The CNN Block

A typical CNN layer:
1. **Convolution**: apply the filter.
2. **Activation**: ReLU (or GELU).
3. **Pooling** (sometimes): downsample (max pool or average pool).
4. **BatchNorm** (sometimes): normalize activations.

Stack 5–50 of these, then a dense head for classification.

## Worked Example (LeNet-style)

```python
import torch.nn as nn

class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, padding=1)   # 1 channel in, 32 out, 3x3
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)                # halves spatial dims
        self.fc = nn.Linear(64 * 7 * 7, num_classes)
    
    def forward(self, x):                              # x: (B, 1, 28, 28)
        x = self.pool(F.relu(self.conv1(x)))           # (B, 32, 14, 14)
        x = self.pool(F.relu(self.conv2(x)))           # (B, 64, 7, 7)
        x = x.flatten(1)                                # (B, 64*7*7)
        return self.fc(x)
```

## The ResNet Revolution (2015)

Plain CNNs couldn't go deep — past ~20 layers, training degraded (vanishing gradients, see [[06 - Backpropagation]]). **ResNet** introduced **skip connections** (residuals):

$$
\mathbf{y} = \mathbf{x} + F(\mathbf{x})
$$

where $F$ is a stack of conv layers. This lets gradients flow directly through the network, enabling 100+ layer CNNs. See [[07 - Transformers/Architecture/Residual Connections|Residual Connections]].

ResNet-50 was SOTA on ImageNet in 2015 and is still widely used as a backbone for downstream vision tasks.

## Modern Variants

- **ResNet** (2015): residuals, the standard.
- **Inception / GoogLeNet** (2014): multi-scale parallel convs.
- **MobileNet** (2017): depthwise separable convs for mobile.
- **EfficientNet** (2019): compound scaling of width/depth/resolution.

All of these were SOTA before the Vision Transformer (2020). ViT now matches or beats CNNs on large datasets, but CNNs remain relevant for:
- **Smaller datasets** (ViT is data-hungry).
- **Mobile / edge** (CNNs are more efficient).
- **Dense prediction** (segmentation, detection — U-Net architectures).

## Relation to Transformer Attention

CNNs and self-attention are conceptually related:
- A **convolution** is a "local attention" with fixed weights.
- A **self-attention** layer is a "global convolution" with input-dependent weights.

Sliding-window attention (Mistral 7B, Longformer) is essentially a CNN-style local attention pattern applied to sequences. The attention mechanism generalizes convolution.

## Why This Matters for AI

- CNNs are the **historical foundation** of deep learning. The deep learning revolution started with AlexNet (2012) — a CNN.
- For vision tasks where data is limited or compute is constrained, CNNs are still the right choice.
- The convolution pattern (parameter sharing across positions) shows up in modern architectures in modified forms (sliding window attention, depthwise convs in Mamba).
- For multimodal AI, CNN backbones (ResNet, ViT) encode images that LLMs then attend to.

## Production Implications

- **Use pretrained CNN backbones** (ResNet-50, EfficientNet-B0) for vision tasks with limited data. HuggingFace `transformers` and `timm` libraries make this trivial.
- **For object detection / segmentation**: Faster R-CNN, YOLO, Mask R-CNN, DETR all use CNN backbones.
- **For mobile / edge**: MobileNetV3, EfficientNet-Lite.
- **For large-scale vision**: ViT usually wins, but requires more data and compute.

## Common Pitfalls

- **No padding** — output shrinks each layer. Use `padding='same'` or compute output dims explicitly.
- **Wrong stride** — `stride=2` downsamples (like pooling); `stride=1` keeps resolution.
- **Forgetting flatten before the FC head** — common shape bug.
- **Too many channels early** — wastes parameters; better to increase channels as resolution decreases.
- **Mixing up "channels first" vs "channels last"** — PyTorch uses (B, C, H, W); TensorFlow uses (B, H, W, C). Don't mix.

## Further Reading

- LeCun et al. (1998), *Gradient-Based Learning Applied to Document Recognition* (LeNet).
- Krizhevsky et al. (2012), *ImageNet Classification with Deep CNNs* (AlexNet).
- He et al. (2016), *Deep Residual Learning for Image Recognition* (ResNet).

## The Mathematics of Convolution (Detailed)

A 2D convolution with kernel $\mathbf{K} \in \mathbb{R}^{k \times k}$ on input $\mathbf{X} \in \mathbb{R}^{H \times W}$:

$$
(\mathbf{X} * \mathbf{K})_{ij} = \sum_{a=0}^{k-1} \sum_{b=0}^{k-1} X_{i+a, j+b} \cdot K_{a, b}
$$

(Technically this is **cross-correlation** — the "convolution" in deep learning flips neither input nor kernel. True convolution flips the kernel, but this distinction is irrelevant for learned kernels.)

### Output shape computation
For input $H \times W$, kernel $k \times k$, padding $p$, stride $s$:
$$
H_{\text{out}} = \left\lfloor \frac{H + 2p - k}{s} \right\rfloor + 1
$$
Same for $W_{\text{out}}$. With $p = (k-1)/2$ and $s = 1$, output has the same spatial size as input ("same" padding).

### Parameter count
A conv layer with $C_{\text{in}}$ input channels, $C_{\text{out}}$ output channels, kernel $k \times k$:
- Parameters: $C_{\text{out}} \times C_{\text{in}} \times k \times k + C_{\text{out}}$ (weights + biases).
- Example: 3 → 64 channels, 3×3 kernel = 1,792 parameters.
- Compare to a dense layer connecting every pixel of a 224×224×3 image to 64 outputs: $224 \times 224 \times 3 \times 64 = 9.6$M parameters.

The parameter efficiency comes from **weight sharing** — the same kernel is applied at every spatial position.

### FLOP count
For input $C_{\text{in}} \times H \times W$, kernel $k \times k$, $C_{\text{out}}$ output channels:
- FLOPs = $2 \cdot C_{\text{out}} \cdot C_{\text{in}} \cdot k^2 \cdot H_{\text{out}} \cdot W_{\text{out}}$.
- Example: 3×224×224 → 64 channels, 3×3, stride 1, same padding: $2 \cdot 64 \cdot 3 \cdot 9 \cdot 224 \cdot 224 \approx 173$M FLOPs.

## The Evolution of CNN Architectures

| Model            | Year | Innovation                                          | Top-5 ImageNet Acc |
|------------------|------|-----------------------------------------------------|--------------------|
| LeNet            | 1998 | First successful CNN (digit recognition)            | N/A (MNIST)        |
| AlexNet          | 2012 | GPU training, ReLU, dropout (deep learning revolution) | 84.7%              |
| VGG              | 2014 | Deeper (16-19 layers), small 3×3 kernels            | 92.0%              |
| GoogLeNet/Inception | 2014 | Multi-scale parallel convs, 1×1 convs              | 93.3%              |
| ResNet           | 2015 | Residual connections (skip connections)             | 96.4%              |
| DenseNet         | 2017 | Dense connections (every layer connects to every other) | 96.4%              |
| MobileNet        | 2017 | Depthwise separable convs (mobile)                  | 90.6%              |
| EfficientNet     | 2019 | Compound scaling (width/depth/resolution)           | 97.1%              |
| ConvNeXt         | 2022 | Modernized ResNet (rivals ViT)                      | 97.8%              |

### Why ResNet was the breakthrough
Before ResNet, deeper networks performed **worse** (degradation problem) — not overfitting, but optimization difficulty. ResNet's identity shortcut $\mathbf{y} = \mathbf{x} + F(\mathbf{x})$ lets gradients flow directly through the network. If $F(\mathbf{x}) = 0$ is optimal, the layer becomes identity — the network can learn to "skip" layers. This enabled 100+ layer networks.

The same principle — residual connections — is used in every modern Transformer. See [[07 - Transformers/Architecture/03 - Residual Connections|Residual Connections]].

### ConvNeXt: CNNs strike back
ConvNeXt (Liu et al. 2022) modernized the ResNet architecture with insights from ViT:
- Larger kernels (7×7 instead of 3×3).
- LayerNorm instead of BatchNorm.
- GELU instead of ReLU.
- Fewer activation functions (only one per block).
- Inverted bottleneck (wide → narrow → wide).

Result: ConvNeXt matches or beats ViT on ImageNet, proving CNNs are still competitive when modernized. This challenges the "ViT replaced CNNs" narrative.

## Depthwise Separable Convolutions (MobileNet)

Standard conv: $C_{\text{out}} \times C_{\text{in}} \times k^2$ parameters. Depthwise separable conv decomposes this into:
1. **Depthwise conv**: one filter per input channel. $C_{\text{in}} \times k^2$ parameters.
2. **Pointwise conv** (1×1): mix channels. $C_{\text{out}} \times C_{\text{in}}$ parameters.

Total: $C_{\text{in}} \times k^2 + C_{\text{out}} \times C_{\text{in}}$ vs. $C_{\text{out}} \times C_{\text{in}} \times k^2$. For $k = 3$, $C_{\text{out}} = C_{\text{in}} = 64$: 832 vs. 36,864 — 44× fewer parameters.

This is the foundation of MobileNet, EfficientNet, and most mobile/edge vision models. The cost: slight quality reduction (~1-2% ImageNet accuracy).

## CNNs vs. ViT: When to Use Each (2026)

| Criterion                    | CNN (ResNet, ConvNeXt)    | ViT (ViT, DeiT, Swin)      |
|------------------------------|---------------------------|----------------------------|
| Small datasets (<100K images) | ✅ Better (inductive bias) | ❌ Data-hungry              |
| Large datasets (>10M images)  | ✅ Good                    | ✅ Better (scales)          |
| Mobile / edge                | ✅ More efficient          | ❌ Heavier                  |
| Dense prediction (detection)  | ✅ Better (hierarchical)   | 🟡 ViTDet closes the gap    |
| Long-range dependencies       | ❌ Limited receptive field | ✅ Global attention         |
| Transfer learning            | ✅ Strong                  | ✅ Strong (often better)    |
| Interpretability             | 🟡 Feature visualization   | 🟡 Attention visualization  |

**2026 recommendation**: start with a pretrained ViT (DINOv2, SigLIP) for most vision tasks. Use CNN (ConvNeXt, EfficientNet) when (1) data is limited, (2) mobile/edge deployment, (3) dense prediction with strict latency. The gap has narrowed — both are viable for most tasks.

## Worked Example: Modern CNN (ConvNeXt-style block)

```python
import torch
import torch.nn as nn

class ConvNeXtBlock(nn.Module):
    """ConvNeXt-style block: depthwise conv → LN → pointwise → GELU → pointwise."""
    def __init__(self, dim, layer_scale=1e-6):
        super().__init__()
        self.dw_conv = nn.Conv2d(dim, dim, kernel_size=7, padding=3, groups=dim)
        self.norm = nn.LayerNorm(dim)
        self.pw1 = nn.Linear(dim, dim * 4)  # expand
        self.act = nn.GELU()
        self.pw2 = nn.Linear(dim * 4, dim)  # contract
        self.gamma = nn.Parameter(layer_scale * torch.ones(dim)) if layer_scale else 1.0

    def forward(self, x):
        residual = x
        x = self.dw_conv(x)                   # depthwise: local spatial
        x = x.permute(0, 2, 3, 1)             # (B, H, W, C) for LayerNorm
        x = self.norm(x)
        x = self.pw1(x)                        # expand
        x = self.act(x)
        x = self.pw2(x)                        # contract
        x = self.gamma * x
        x = x.permute(0, 3, 1, 2)             # back to (B, C, H, W)
        return residual + x                    # residual

# A ConvNeXt stage: stem + N blocks + downsample
class ConvNeXtStage(nn.Module):
    def __init__(self, in_dim, out_dim, n_blocks, stride=2):
        super().__init__()
        self.downsample = nn.Conv2d(in_dim, out_dim, kernel_size=stride, stride=stride)
        self.blocks = nn.Sequential(*[ConvNeXtBlock(out_dim) for _ in range(n_blocks)])

    def forward(self, x):
        return self.blocks(self.downsample(x))
```

This modernized CNN block (7×7 depthwise conv, LayerNorm, GELU, inverted bottleneck, layer scale) rivals ViT blocks on ImageNet — proving CNNs can be modernized to match Transformers.

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Output shrinks each layer | No padding | Use `padding='same'` or compute output dims |
| Memory explosion | Too many channels early | Increase channels as resolution decreases |
| Slow training | Small batch size; conv-bound | Increase batch; use mixed precision |
| Wrong channel format | Mixing NHWC and NCHW | PyTorch = NCHW; TF = NHWC; don't mix |
| Poor accuracy on small dataset | CNN overfitting; ViT too data-hungry | Use pretrained CNN; strong augmentation |
| Detection model misses small objects | Receptive field too large | Use FPN (Feature Pyramid Network); multi-scale |

## Connection to Other Concepts

- [[04 - Neural Networks/Foundations/01 - Perceptrons and MLPs|Perceptrons and MLPs]] — CNNs are MLPs with weight sharing.
- [[04 - Neural Networks/Training/06 - Backpropagation|Backpropagation]] — gradients through conv layers.
- [[04 - Neural Networks/Training/07 - Initialization Schemes|Initialization Schemes]] — He init for ReLU convs.
- [[07 - Transformers/Architecture/03 - Residual Connections|Residual Connections]] — ResNet's innovation.
- [[07 - Transformers/Variants/13 - Vision Transformer ViT|Vision Transformer]] — the architecture that displaced CNNs at scale.
- [[06 - Attention Mechanisms/Modern Attention/15 - Sliding Window Attention|Sliding Window Attention]] — CNN-style local attention.
- [[06 - Attention Mechanisms/Efficient Attention/12 - Sparse Attention|Sparse Attention]] — local patterns inspired by CNNs.
- [[09 - Foundation Models/Vision/01 - Vision Foundation Models|Vision Foundation Models]] — modern vision encoders.
- [[23 - Multimodal AI/MOC|Multimodal AI]] — CNN backbones for VLMs.

## Interview Questions

1. **Q: Why do CNNs use weight sharing, and what does it buy?**
   A: Weight sharing means the same kernel is applied at every spatial position. This buys: (1) parameter efficiency — a 3×3 conv has 9 parameters regardless of image size; a dense layer has $H \times W$ parameters; (2) translation invariance — a cat is a cat anywhere in the image; (3) locality — nearby pixels are correlated, so small kernels capture relevant patterns. The cost: less flexibility than a dense layer, but this is a feature (inductive bias) for vision.

2. **Q: What is depthwise separable convolution, and why is it efficient?**
   A: Decompose a standard conv ($C_{\text{out}} \times C_{\text{in}} \times k^2$ params) into depthwise ($C_{\text{in}} \times k^2$, one filter per channel) + pointwise ($C_{\text{out}} \times C_{\text{in}}$, 1×1 conv). For $k=3$, $C_{\text{out}} = C_{\text{in}} = 64$: 832 vs. 36,864 — 44× fewer parameters. The cost: ~1-2% accuracy reduction. Foundation of MobileNet, EfficientNet, and mobile vision.

3. **Q: Why did ResNet enable deeper networks?**
   A: Before ResNet, deeper networks performed worse (degradation problem) — gradients vanished through many layers. ResNet's identity shortcut $\mathbf{y} = \mathbf{x} + F(\mathbf{x})$ provides a direct path for gradients. If $F(\mathbf{x}) = 0$ is optimal, the layer becomes identity — the network can "skip" layers. This enabled 100+ layer networks. The same principle (residual connections) is used in every modern Transformer.

4. **Q: When would you choose a CNN over a ViT?**
   A: Choose CNN when: (1) small datasets (<100K images) — CNN's inductive bias (locality, translation invariance) helps with limited data; (2) mobile/edge — CNNs are more efficient; (3) dense prediction (detection, segmentation) — hierarchical features work well. Choose ViT when: (1) large datasets — ViT scales better; (2) long-range dependencies matter; (3) transfer learning — ViT often transfers better. The gap has narrowed; both are viable for most tasks in 2026.

5. **Q: How does ConvNeXt modernize CNNs to rival ViT?**
   A: ConvNeXt applies ViT-inspired changes to ResNet: (1) larger kernels (7×7 vs. 3×3) for wider receptive field; (2) LayerNorm instead of BatchNorm; (3) GELU instead of ReLU; (4) fewer activations (one per block, not per layer); (5) inverted bottleneck (wide→narrow→wide, like ViT's FFN). Result: ConvNeXt matches or beats ViT on ImageNet, proving CNNs are still competitive when modernized.

6. **Q: How does sliding window attention relate to convolution?**
   A: Sliding window attention (Mistral 7B, Longformer) applies attention only within a local window of size $w$ — exactly like a CNN with kernel size $w$. The difference: attention weights are input-dependent (learned per position), while conv weights are fixed (learned once). Attention generalizes convolution — a conv is "local attention with fixed weights". This is why CNN-inspired patterns appear in efficient attention.

## See Also

- [[01 - Perceptrons and MLPs]]
- [[06 - Backpropagation]]
- [[07 - Transformers/Architecture/Residual Connections|Residual Connections]]
- [[07 - Transformers/Encoder Models/Vision Transformer ViT|Vision Transformer]] (planned)
- [[04 - Neural Networks/MOC|Neural Networks MOC]]