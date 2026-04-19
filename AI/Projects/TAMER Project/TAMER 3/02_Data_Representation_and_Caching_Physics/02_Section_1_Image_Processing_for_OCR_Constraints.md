## 1. Image Processing for OCR Constraints

### The Batching Problem

PyTorch requires all images in a batch to have identical dimensions. This is because the GPU processes data as a single rectangular tensor of shape:

$$\text{Batch} \times \text{Channels} \times \text{Height} \times \text{Width}$$

Mathematical formulas come in wildly different aspect ratios:
- $\frac{1}{2}$ might produce an image of 80×40 pixels (roughly square).
- A long polynomial like $a_n x^n + a_{n-1} x^{n-1} + \cdots + a_0$ might produce an image of 40×800 pixels (very wide).
- A system of equations might produce an image of 200×400 pixels (tall).

You cannot put a 80×40 image in the same batch as a 40×800 image without modification.

---

### Naive Resizing and Why It Fails

The most obvious solution is to simply resize every image to the target dimensions (e.g., 256×1024). This is called **unconstrained resizing** and it causes a critical failure mode for OCR:

When you resize 80×40 to 256×1024, the horizontal scale factor is $1024/40 = 25.6$x and the vertical scale factor is $256/80 = 3.2$x. These are completely different, so the image is stretched 8 times more horizontally than vertically. A perfectly circular symbol like `○` becomes a wide ellipse. A fraction bar that was 2px thin becomes 16px wide and blurry. The stroke geometry the model needs to recognize individual symbols is destroyed.

---

### Aspect-Ratio-Preserving Resizing: Full Mathematical Derivation

TAMER's preprocessor preserves the aspect ratio of all images. Let's define the variables:

- $H, W$: Original image height and width in pixels.
- $T_H = 256$: Target height.
- $T_W = 1024$: Target width.
- $S$: The scalar scale factor to apply uniformly to both dimensions.

The rule is: choose $S$ such that the scaled image fits inside the target bounding box without cropping, and without distortion.

$$S = \min\left(\frac{T_H}{H}, \frac{T_W}{W}\right)$$

Taking the minimum ensures neither dimension exceeds the target. After scaling:

$$H_{\text{new}} = \lfloor H \times S \rfloor, \quad W_{\text{new}} = \lfloor W \times S \rfloor$$

The remaining space is filled with white padding (pixel value 255 for grayscale), applied symmetrically to center the formula in the canvas.

**Worked Example: Tall Image**

Given: $H = 300$, $W = 200$.

$$S_H = 256 / 300 = 0.853$$
$$S_W = 1024 / 200 = 5.12$$
$$S = \min(0.853, 5.12) = 0.853$$
$$H_{\text{new}} = 300 \times 0.853 = 256, \quad W_{\text{new}} = 200 \times 0.853 = 171$$

The image is placed centered in a 256×1024 canvas. Left padding = $(1024 - 171) / 2 = 427$ pixels. Right padding = 427 pixels.

**Worked Example: Wide Image**

Given: $H = 60$, $W = 900$.

$$S_H = 256 / 60 = 4.267$$
$$S_W = 1024 / 900 = 1.138$$
$$S = \min(4.267, 1.138) = 1.138$$
$$H_{\text{new}} = 60 \times 1.138 = 68, \quad W_{\text{new}} = 900 \times 1.138 = 1024$$

The image fills the full width. Top padding = $(256 - 68) / 2 = 94$ pixels. Bottom padding = 94 pixels.

**Worked Example: Extremely Wide Image (Overflow Case)**

Given: $H = 30$, $W = 2000$.

$$S_H = 256 / 30 = 8.533$$
$$S_W = 1024 / 2000 = 0.512$$
$$S = \min(8.533, 0.512) = 0.512$$
$$H_{\text{new}} = 30 \times 0.512 = 15, \quad W_{\text{new}} = 2000 \times 0.512 = 1024$$

The formula is tiny vertically. Top padding = $(256 - 15) / 2 = 120$ pixels. This is a legitimate case where the formula is genuinely very long. The model handles it, but very long formulas are hard. This motivates the dataset filtering step that removes excessively long LaTeX strings.

> **Important reminder:** The padding value is always 255 (white), not 0 (black). This is because the model is trained on white-background math typeset by LaTeX renderers. If you pad with black, the model sees a large black rectangle as part of the formula. Always match the padding color to the background color of your data source.

---