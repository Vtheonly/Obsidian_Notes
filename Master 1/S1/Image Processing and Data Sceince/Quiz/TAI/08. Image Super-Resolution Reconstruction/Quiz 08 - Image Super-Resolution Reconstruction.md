---
sources:
  - "[[08.1. Continuous Image Reconstruction (Nearest, Bilinear, and Keys' Bicubic Spline)]]"
  - "[[08.2. Edge-Adaptive Interpolation (Contour Stencils and Total Variation Minimization)]]"
  - "[[08.3. Deep Super-Resolution Frameworks (SRCNN, Perceptual SRGAN, and ESRGAN)]]"
  - "[[08.4. Document Image Super-Resolution (Bi-ESRGAN Dual Path Architecture)]]"
---
> [!question] Nearest-neighbor interpolation assigns each target point the intensity of the nearest known pixel and is highly computationally efficient.
>> [!success]- Answer
>> True

> [!question] Standard bilinear and bicubic interpolation blur edges because they average pixel values isotropically across boundaries.
>> [!success]- Answer
>> True

> [!question] Bilinear interpolation preserves sharp edges and fine details better than Keys' bicubic spline because it averages fewer neighboring pixels.
>> [!success]- Answer
>> False

> [!question] SRGAN introduced generative adversarial networks and perceptual loss to generate realistic high-frequency textures in super-resolution.
>> [!success]- Answer
>> True

> [!question] The contour stencil method selects the directional stencil with the maximum total variation as the optimal orientation $S^*$.
>> [!success]- Answer
>> False

> [!question] SRCNN relies on an adversarial discriminator network to produce realistic high-frequency textures.
>> [!success]- Answer
>> False

> [!question] In Keys' cubic convolution kernel, the parameter value $a = -0.5$ is chosen so that the kernel matches the Taylor expansion of the continuous function.
>> [!success]- Answer
>> True

> [!question] Bi-ESRGAN restores degraded documents with a single network path that processes text and background jointly.
>> [!success]- Answer
>> False

> [!question] Which artifact is characteristic of nearest-neighbor (zero-order hold) interpolation?
> a) Blurring of high-frequency details and sharp edges
> b) Ringing oscillations along strong edges
> c) Severe blockiness and jagged edges
> d) Overly smooth textures caused by averaging many neighbors
>> [!success]- Answer
>> c) Severe blockiness and jagged edges

> [!question] In the bilinear weighted-average formula, which product forms the weight of pixel $Q_{21}$?
> a) $(x_2 - x)(y_2 - y)$
> b) $(x_2 - x)(y - y_1)$
> c) $(x - x_1)(y - y_1)$
> d) $(x - x_1)(y_2 - y)$
>> [!success]- Answer
>> d) $(x - x_1)(y_2 - y)$

> [!question] How does bilinear interpolation compare with nearest-neighbor interpolation in output quality?
> a) It produces smoother results but blurs high-frequency details and sharp edges
> b) It produces sharper edges but suffers from more blockiness
> c) It is computationally cheaper but introduces more aliasing
> d) It produces identical results with a simpler formula
>> [!success]- Answer
>> a) It produces smoother results but blurs high-frequency details and sharp edges

> [!question] How many distinct stencil angles does the contour stencil method evaluate when choosing the optimal orientation?
> a) 4
> b) 8
> c) 12
> d) 16
>> [!success]- Answer
>> c) 12

> [!question] What is the correct order of the three processing stages in SRCNN?
> a) Patch extraction, then non-linear mapping, then reconstruction
> b) Non-linear mapping, then patch extraction, then reconstruction
> c) Patch extraction, then reconstruction, then non-linear mapping
> d) Reconstruction, then patch extraction, then non-linear mapping
>> [!success]- Answer
>> a) Patch extraction, then non-linear mapping, then reconstruction

> [!question] In SRGAN's perceptual objective, how is the adversarial loss term weighted relative to the VGG content loss?
> a) It is added with equal weight
> b) It is weighted by a factor of $10^{-3}$
> c) It is weighted by a factor of $10^{3}$
> d) It is omitted from the final objective
>> [!success]- Answer
>> b) It is weighted by a factor of $10^{-3}$

> [!question] What input does SRCNN's three-layer convolutional network directly process?
> a) The raw low-resolution image at its original scale
> b) Random noise vectors sampled from a prior distribution
> c) Feature maps extracted by a pre-trained VGG network
> d) A bicubic-upsampled version of the low-resolution image
>> [!success]- Answer
>> d) A bicubic-upsampled version of the low-resolution image

> [!question] Bi-ESRGAN is a specialized deep learning architecture designed for which task?
> a) General natural-scene super-resolution benchmarks
> b) Document image restoration and super-resolution
> c) Real-time video frame interpolation
> d) Handwritten text recognition
>> [!success]- Answer
>> b) Document image restoration and super-resolution

> [!question] Match each interpolation method with the samples it uses to compute a target pixel value.
>> [!example] Group A
>> a) Nearest-neighbor interpolation
>> b) Bilinear interpolation
>> c) Keys' bicubic spline interpolation
>
>> [!example] Group B
>> n) Draws on exactly one source sample, the value of the pixel closest to the target point.
>> o) Blends the four pixels immediately surrounding the target point in a 2x2 arrangement.
>> p) Weights 16 surrounding samples arranged on a 4x4 grid.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match each region of the distance argument $d$ in Keys' cubic convolution kernel $W(d)$ with the expression that applies.
>> [!example] Group A
>> a) Central region $0 \le |d| \le 1$
>> b) Outer region $1 < |d| \le 2$
>> c) Beyond the support, where $|d|$ is greater than 2
>
>> [!example] Group B
>> n) The kernel equals $(a+2)|d|^3 - (a+3)|d|^2 + 1$.
>> o) The kernel equals $a|d|^3 - 5a|d|^2 + 8a|d| - 4a$.
>> p) The kernel equals zero.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match each concept from edge-adaptive interpolation with its description.
>> [!example] Group A
>> a) Contour stencils
>> b) Total variation $\text{TV}(S)$
>> c) Directional interpolation
>
>> [!example] Group B
>> n) Filling in missing pixels along the selected orientation instead of across it.
>> o) The averaged sum of weighted absolute intensity differences along a candidate's edges.
>> p) The framework by Getreuer that estimates local edge orientation before upsampling.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match each SRCNN processing stage with the convolution that implements it.
>> [!example] Group A
>> a) Patch extraction
>> b) Non-linear mapping
>> c) Reconstruction
>
>> [!example] Group B
>> n) A 9x9 convolution applied to the input that pulls out feature representations.
>> o) A 1x1 or 5x5 convolution that transforms each low-resolution feature into a high-resolution counterpart.
>> p) A 5x5 convolution that assembles the transformed features into the final high-resolution image.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match each training objective from deep super-resolution with its mechanism or effect.
>> [!example] Group A
>> a) VGG content loss
>> b) Adversarial loss
>> c) Pixel-wise MSE loss
>
>> [!example] Group B
>> n) Computes the Euclidean distance between feature representations extracted from a pre-trained network.
>> o) Averages possible high-frequency patterns and therefore yields overly smooth textures.
>> p) Pushes the generator to produce high-frequency details that fool a discriminator.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match each ESRGAN improvement with its effect.
>> [!example] Group A
>> a) RRDB
>> b) Removal of Batch Normalization
>> c) Relativistic average discriminator
>
>> [!example] Group B
>> n) Replaces basic residual blocks with multi-level residual connections, increasing capacity and training stability.
>> o) Eliminates layers that introduced visual artifacts while reducing computational overhead.
>> p) Estimates the probability that the real image is relatively more realistic than the generated one.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match each Bi-ESRGAN component with the restoration role it performs.
>> [!example] Group A
>> a) Text foreground path
>> b) Background denoising path
>> c) Channel fusion network
>
>> [!example] Group B
>> n) Sharpens character strokes while preserving their legibility and connectivity.
>> o) Removes stains, ink bleed-through, paper grain, and non-uniform illumination.
>> p) Merges the outputs of the two processing streams into a single restored image.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match each Bi-ESRGAN processing strategy with the outcome it delivers.
>> [!example] Group A
>> a) High-frequency edge optimization
>> b) Smooth background inpainting
>> c) Channel fusion
>
>> [!example] Group B
>> n) Reconstruction of sharp character strokes.
>> o) Removal of stains and artifacts from the page.
>> p) Production of the final high-resolution restored document.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
