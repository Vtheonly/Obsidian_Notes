---
sources:
  - "[[06.6.1. Feature Space Clustering (Mean-Shift and 2SP-DBSCAN by UMBB iVision)]]"
  - "[[06.6.2. Deep Learning Denoising (Patch MLPs, Residual DnCNN, and Uformer)]]"
---
> [!question] In feature-space clustering, each pixel is treated as a point whose coordinates combine its position and its color, for example $(x, y, R, G, B)$ or $(x, y, L^*, a^*, b^*)$.
>> [!success]- Answer
>> True

> [!question] Mean-Shift requires the number of clusters to be fixed in advance, which is why it is classified as a parametric method.
>> [!success]- Answer
>> False

> [!question] Mean-Shift filtering groups pixels into flat regions of constant color separated by sharp boundaries, giving the image a posterized appearance.
>> [!success]- Answer
>> True

> [!question] DnCNN is trained to reconstruct the clean image $X$ directly from the noisy input $Y = X + V$.
>> [!success]- Answer
>> False

> [!question] Deep learning denoisers learn complex noise models directly from training pairs consisting of corrupted inputs and clean ground-truth targets.
>> [!success]- Answer
>> True

> [!question] In each Mean-Shift iteration, the shift vector $m(x)$ moves the current point toward which target?
> a) The centroid of the largest cluster discovered so far.
> b) The kernel-weighted mean of the feature points inside the current search window.
> c) The median intensity of the pixels inside the current search window.
> d) A fixed cluster center chosen when the algorithm is initialized.
>> [!success]- Answer
>> b) The kernel-weighted mean of the feature points inside the current search window.

> [!question] Given the noisy input $Y$ and the noise prediction $\mathcal{R}(Y)$ produced by DnCNN, how is the restored image $X^*$ computed?
> a) $X^* = \mathcal{R}(Y) - Y$
> b) $X^* = \mathcal{R}(Y)$
> c) $X^* = Y - \mathcal{R}(Y)$
> d) $X^* = Y + \mathcal{R}(Y)$
>> [!success]- Answer
>> c) $X^* = Y - \mathcal{R}(Y)$

> [!question] Why does residual learning make DnCNN easier to train than predicting the clean image directly?
> a) The noise residual is simpler and more uniform, while the clean image contains complex semantic textures and edges that are hard to reconstruct from scratch.
> b) The noise residual spans a much wider dynamic range, which keeps the gradients large.
> c) Predicting the clean image directly would make the loss function non-differentiable.
> d) The noise residual can be computed exactly by a single fully connected layer.
>> [!success]- Answer
>> a) The noise residual is simpler and more uniform, while the clean image contains complex semantic textures and edges that are hard to reconstruct from scratch.

> [!question] Which statement correctly describes the architecture of Uformer?
> a) A stack of fully connected layers applied to flattened image patches.
> b) An encoder-decoder hourglass that predicts the noise residual for subtraction.
> c) A clustering pipeline that splits the feature space into separate spatial and color domains.
> d) A U-shaped hierarchical design built from Transformer blocks rather than standard convolutions.
>> [!success]- Answer
>> d) A U-shaped hierarchical design built from Transformer blocks rather than standard convolutions.

> [!question] Why is standard DBSCAN computationally slow on high-resolution document images?
> a) It computes multi-dimensional distances between all pairs of pixels, which scales as $\mathcal{O}(N^2)$.
> b) It must first train on thousands of labeled document images.
> c) It runs a separate mean-shift ascent for every pixel of the page.
> d) It stores a complete color histogram in memory for every cluster it forms.
>> [!success]- Answer
>> a) It computes multi-dimensional distances between all pairs of pixels, which scales as $\mathcal{O}(N^2)$.

> [!question] Match each Mean-Shift ingredient with its role.
>> [!example] Group A
>> a) Local mode
>> b) Bandwidth $h$
>> c) Kernel profile derivative $g$
>> d) Search window $S_h$
>
>> [!example] Group B
>> n) The scale parameter that sets how wide the averaging neighborhood in feature space reaches.
>> o) The multi-dimensional neighborhood centered on the current point, gathering the points whose mean is computed.
>> p) The peak of the estimated probability density function that a point climbs toward and eventually settles on.
>> q) Defined as $-k'(s)$, it weights the points that enter each iterative average.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)

> [!question] Match each step of the Mean-Shift procedure with its action.
>> [!example] Group A
>> a) Initialization
>> b) Averaging
>> c) Center shift
>> d) Convergence test
>> e) Result assignment
>
>> [!example] Group B
>> n) Move the middle of the window onto the newly computed mean.
>> o) Place the search window on the pixel being processed before any iteration begins.
>> p) Stop repeating once the displacement vector becomes negligibly small, approaching zero.
>> q) Compute the mean of the feature vectors of every point inside the current window.
>> r) Give the original pixel the color at which its window settled.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)
>> e) -> r)

> [!question] Match each aspect of 2SP-DBSCAN with its description.
>> [!example] Group A
>> a) Space splitting
>> b) Integral volume table
>> c) Artifact removal
>> d) Stroke preservation
>
>> [!example] Group B
>> n) A precomputed structure that returns neighbor density counts in $O(1)$ constant time.
>> o) Keeping the thin lines of characters intact throughout the restoration.
>> p) Treats the 2D coordinates and the 1D or 3D color or intensity values as two separate, independent domains.
>> q) Clearing scanned historical manuscripts of ink bleed-through, stains, and paper aging effects.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)

> [!question] Match each deep denoising architecture with its defining mechanism.
>> [!example] Group A
>> a) Patch-based MLP
>> b) Convolutional auto-encoder
>> c) DnCNN
>> d) Uformer
>
>> [!example] Group B
>> n) An hourglass-shaped design whose skip connections follow the U-Net pattern.
>> o) Flattens small windows such as $17 \times 17$ pixels into 1D vectors for a stack of fully connected layers.
>> p) Relies on self-attention so distant clean structures can guide the reconstruction of repetitive textures and patterns.
>> q) Introduced in 2017, pairing residual learning with batch normalization in a convolutional denoiser.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> q)
>> d) -> p)

> [!question] Match each denoising concept with its description.
>> [!example] Group A
>> a) Hand-crafted model
>> b) Flattening penalty
>> c) Small receptive field
>> d) Parameter bloat
>
>> [!example] Group B
>> n) Fully connected layers need so many weights that processing entire high-resolution images becomes slow.
>> o) Turning a 2D patch into a 1D vector throws away the spatial relationships between pixels.
>> p) Traditional restoration filters are built from explicitly designed mathematical formulations instead of relationships learned from examples.
>> q) The limited local view of convolutional networks that makes global image context hard to capture.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> q)
>> d) -> n)
