---
sources:
  - "[[06.2.1. Physical Noise Models (PSF, Gaussian, Impulse Salt-and-Pepper, Speckle)]]"
  - "[[06.2.2. Quantitative Quality Benchmarks (MSE, PSNR, and SSIM)]]"
  - "[[06.2.3. Linear Spatial Smoothing (Mean Box Filter, Gaussian Bell, and 1D Separability)]]"
  - "[[06.2.4. Spatial High-Pass Filtering, Sobel Gradients, and Laplacian Sharpening]]"
  - "[[06.2.5. Order-Statistic Non-Linear Filtering (Median, Min, Max, Min-Max Operators)]]"
  - "[[06.2.6. Structural Edge-Preserving Smoothing (Nagao 9-Sector Multi-Directional Filter)]]"
  - "[[06.2.7. Non-Linear Boundary-Preserving Filtering (Bilateral Joint Spatial-Radiometric Filter)]]"
  - "[[06.2.8. Partial Differential Equations in Restoration (Perona-Malik Anisotropic Diffusion)]]"
---
> [!question] Thermal Johnson-Nyquist sensor noise is most accurately modeled as impulsive salt-and-pepper noise.
>> [!success]- Answer
>> False

> [!question] In multiplicative speckle noise, brighter regions of the image exhibit larger noise variations while dark regions exhibit little noise.
>> [!success]- Answer
>> True

> [!question] A higher Peak Signal-to-Noise Ratio value indicates a larger reconstruction error and lower fidelity to the reference image.
>> [!success]- Answer
>> False

> [!question] Decomposing a $W \times W$ separable 2D convolution into two 1D passes reduces the computational cost from $W^2$ to $2W$ operations per pixel.
>> [!success]- Answer
>> True

> [!question] Because second derivatives are highly sensitive to rapid fluctuations, Laplacian sharpening amplifies noise and should not be applied to noisy images without prior smoothing.
>> [!success]- Answer
>> True

> [!question] The median filter is a linear filter because its output is computed as a convolution sum with a fixed weight matrix.
>> [!success]- Answer
>> False

> [!question] The Nagao filter replaces the central pixel with the mean of the sub-region that exhibits the maximum intensity variance.
>> [!success]- Answer
>> False

> [!question] Increasing the range parameter $\sigma_r$ of the bilateral filter toward infinity makes it preserve edges more sharply.
>> [!success]- Answer
>> False

> [!question] In Perona-Malik anisotropic diffusion, the diffusion rate approaches zero in regions where the gradient magnitude is much larger than the sensitivity threshold $K$.
>> [!success]- Answer
>> True

> [!question] The gradient of an image is a vector that points in the direction of maximum intensity change.
>> [!success]- Answer
>> True

> [!question] Which noise model is described by the equation $G(x, y) = F(x, y) \cdot \eta(x, y)$?
> a) Additive thermal Gaussian noise
> b) Multiplicative speckle noise
> c) Impulsive salt-and-pepper noise
> d) Uniform quantization noise
>> [!success]- Answer
>> b) Multiplicative speckle noise

> [!question] In the salt-and-pepper noise model with corruption probability $p$, what happens to an individual pixel?
> a) It is replaced by 255 with probability $p$ and left unchanged with probability $1 - p$
> b) It receives an additive zero-mean fluctuation drawn from a Gaussian distribution
> c) It is set to 0 with probability $p/2$, set to 255 with probability $p/2$, and left unchanged with probability $1 - p$
> d) It is multiplied by a random factor proportional to its intensity
>> [!success]- Answer
>> c) It is set to 0 with probability $p/2$, set to 255 with probability $p/2$, and left unchanged with probability $1 - p$

> [!question] In the PSNR formula $\text{PSNR} = 10 \cdot \log_{10}(R^2/\text{MSE})$, what is the value of $R$ for a standard 8-bit unsigned image?
> a) 128
> b) 1.0
> c) 256
> d) 255
>> [!success]- Answer
>> d) 255

> [!question] Which expression is mathematically equivalent to $20 \cdot \log_{10}(R/\sqrt{\text{MSE}})$?
> a) $10 \cdot \log_{10}(R^2/\text{MSE})$
> b) $10 \cdot \log_{10}(R/\text{MSE})$
> c) $20 \cdot \log_{10}(R^2 \cdot \text{MSE})$
> d) $2 \cdot \log_{10}(R/\text{MSE})$
>> [!success]- Answer
>> a) $10 \cdot \log_{10}(R^2/\text{MSE})$

> [!question] What is the effect of increasing the standard deviation $\sigma$ when designing a spatial Gaussian smoothing filter?
> a) The filter kernel automatically shrinks to fewer taps
> b) The bell curve widens, smoothing across a larger neighborhood and increasing blur
> c) High-frequency details and sharp edges are accentuated
> d) The kernel values become negative at the periphery
>> [!success]- Answer
>> b) The bell curve widens, smoothing across a larger neighborhood and increasing blur

> [!question] Why does the $3 \times 3$ box mean filter blur sharp edges?
> a) It sorts the pixel values and discards the extreme ones
> b) It amplifies high-frequency components near boundaries
> c) It weights all pixels in the neighborhood equally, regardless of their position
> d) It applies distance-dependent weights that favor distant pixels
>> [!success]- Answer
>> c) It weights all pixels in the neighborhood equally, regardless of their position

> [!question] Laplacian sharpening is performed with the standard kernel whose center coefficient is $-4$. Which equation applies?
> a) $g(x, y) = f(x, y) + \nabla^2 f(x, y)$
> b) $g(x, y) = \nabla^2 f(x, y) - f(x, y)$
> c) $g(x, y) = f(x, y) \cdot \nabla^2 f(x, y)$
> d) $g(x, y) = f(x, y) - \nabla^2 f(x, y)$
>> [!success]- Answer
>> d) $g(x, y) = f(x, y) - \nabla^2 f(x, y)$

> [!question] A $3 \times 3$ neighborhood contains the values 105, 108, 102, 106, 255, 107, 103, 104, and 108, where 255 is a salt outlier. What do the mean filter and the median filter respectively output at the center?
> a) 122 and 106
> b) 106 and 122
> c) 122 and 255
> d) 106 and 106
>> [!success]- Answer
>> a) 122 and 106

> [!question] How many pixels are contained in each of the nine sub-regions of the standard $5 \times 5$ Nagao filter?
> a) 5
> b) 7
> c) 8
> d) 9
>> [!success]- Answer
>> b) 7

> [!question] In the bilateral filter, which two weights are multiplied together to determine the contribution of a neighbor pixel $q$ to the filtered value at pixel $p$?
> a) The Fourier magnitude and the phase angle of the local spectrum
> b) The local variance and the gradient orientation of the neighborhood
> c) The spatial kernel $G_{\sigma_s}$ based on geometric distance and the range kernel $G_{\sigma_r}$ based on intensity difference
> d) The structuring element size and the dynamic range clip limit
>> [!success]- Answer
>> c) The spatial kernel $G_{\sigma_s}$ based on geometric distance and the range kernel $G_{\sigma_r}$ based on intensity difference

> [!question] Match each degradation or noise phenomenon with its defining behavior.
>> [!example] Group A
>> a) Additive Gaussian noise
>> b) Impulsive salt-and-pepper noise
>> c) Multiplicative speckle noise
>> d) Point spread function
>
>> [!example] Group B
>> n) Arises in coherent imaging systems such as SAR, sonar, and medical ultrasound through interference of reflected waves.
>> o) Corrupts every pixel of the image with a small random intensity fluctuation.
>> p) Degradation operator of a linear space-invariant system, expressible as a spatial convolution as in motion blur or out-of-focus optics.
>> q) Randomly replaces a small fraction of pixels with the extreme values 0 or 255 while the remaining pixels stay clean.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match each PSNR range with its standard interpretation.
>> [!example] Group A
>> a) PSNR above 35 dB
>> b) PSNR between 30 and 35 dB
>> c) PSNR between 20 and 30 dB
>> d) PSNR below 20 dB
>
>> [!example] Group B
>> n) Good restoration with minor artifacts visible upon close inspection.
>> o) Severe degradation with significant distortion of image details.
>> p) High visual quality with artifacts nearly imperceptible.
>> q) Poor restoration with visible blurring or lingering noise.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)

> [!question] Match each linear smoothing concept with its characteristic property.
>> [!example] Group A
>> a) Box mean filter
>> b) Gaussian kernel shape
>> c) Kernel normalization
>> d) Gaussian behavior at edges
>
>> [!example] Group B
>> n) Rotationally symmetric bell weighting in which pixels closer to the center receive larger coefficients.
>> o) Dividing the sampled entries by their total sum makes the weights sum to 1 and preserves overall image brightness.
>> p) Produces less distortion at object boundaries than equal-weight averaging over the same neighborhood.
>> q) Assigns identical weights, such as $1/9$ in each cell of a $3 \times 3$ window, to every neighbor.
>
>> [!success]- Answer
>> a) -> q)
>> b) -> n)
>> c) -> o)
>> d) -> p)

> [!question] Match each high-pass operator concept with its mathematical description.
>> [!example] Group A
>> a) Gradient magnitude
>> b) Sobel operator
>> c) Laplacian operator
>> d) Diagonal-inclusive Laplacian kernel
>
>> [!example] Group B
>> n) Weights all eight neighbors by 1 and places $-8$ at the center.
>> o) Equals $\sqrt{G_x^2 + G_y^2}$ and is often approximated by $|G_x| + |G_y|$.
>> p) Isotropic second-order derivative obtained by summing the two spatial second partial derivatives.
>> q) 3 by 3 finite-difference kernels with coefficients 1 and 2 that estimate directional first derivatives.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> p)
>> d) -> n)

> [!question] Match each order-statistic filter with its filtering effect.
>> [!example] Group A
>> a) Median filter
>> b) Max filter
>> c) Min filter
>> d) Data-dependent min-max filter
>
>> [!example] Group B
>> n) Always picks the largest value in the window, brightening the image, removing black pepper noise, and corresponding to grayscale dilation.
>> o) Leaves the center pixel unchanged when it lies within the range spanned by its neighbors, and clamps it to the nearest bound when it falls outside that range.
>> p) Ranks the window values and outputs the middle one, eliminating impulse outliers while preserving sharp edges.
>> q) Always picks the smallest value in the window, darkening the image, removing white salt noise, and corresponding to grayscale erosion.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)

> [!question] Match each element of the Nagao algorithm with its role.
>> [!example] Group A
>> a) Sub-region layout
>> b) Sector variance
>> c) Variance computation
>> d) Output value
>
>> [!example] Group B
>> n) The mean intensity of the winning sub-region is assigned to the center pixel.
>> o) Evaluated per sector as the average of the squared intensities minus the squared mean.
>> p) Measures local intensity dispersion, and is large when a sub-region straddles an edge.
>> q) Nine overlapping sectors inside a $5 \times 5$ window: one central cross, four cardinal directions, and four diagonal corners.
>
>> [!success]- Answer
>> a) -> q)
>> b) -> p)
>> c) -> o)
>> d) -> n)

> [!question] Match each bilateral filter component with its function.
>> [!example] Group A
>> a) Spatial kernel $G_{\sigma_s}$
>> b) Range kernel $G_{\sigma_r}$
>> c) Normalization factor $W_p$
>> d) Very small $\sigma_r$
>
>> [!example] Group B
>> n) Ensures that all the filter weights sum to 1.
>> o) Weights each neighbor by the absolute difference between its intensity and that of the center pixel.
>> p) Weights each neighbor by its geometric distance from the center pixel.
>> q) Restricts averaging to pixels of nearly identical intensity, so sharp edges are preserved.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)
>> d) -> q)

> [!question] Match each Perona-Malik diffusion element with its behavior.
>> [!example] Group A
>> a) Standard heat diffusion equation
>> b) Conductance at low gradients
>> c) Exponential conductance function
>> d) Rational conductance function
>> e) Excessive iteration count
>
>> [!example] Group B
>> n) Produces staircasing artifacts in which smooth gradients turn into piecewise flat steps.
>> o) Favors high-contrast edges over low-contrast ones.
>> p) Equivalent to isotropic Gaussian blurring of the image.
>> q) The conductance coefficient approaches 1, giving standard isotropic smoothing in homogeneous areas.
>> r) Favors wider, smoother regions over sharp boundaries.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> o)
>> d) -> r)
>> e) -> n)

> [!question] Match each quality measurement concept with its meaning.
>> [!example] Group A
>> a) Mean Squared Error
>> b) MSE value of zero
>> c) Squared error term
>> d) PSNR in decibels
>
>> [!example] Group B
>> n) Signals a perfect reconstruction in which the restored image equals the reference.
>> o) The average of the squared pixel-wise differences between the restored and reference images.
>> p) Expresses the ratio of maximum possible signal power to corrupting noise power on a logarithmic scale.
>> q) Penalizes large localized deviations far more heavily than small widespread differences.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> q)
>> d) -> p)

> [!question] Match each parameter or formula quantity with its role in the corresponding method.
>> [!example] Group A
>> a) Spatial parameter $\sigma_s$ of the bilateral filter
>> b) Sensitivity threshold $K$ of Perona-Malik diffusion
>> c) Stability parameter $\lambda$ of the explicit diffusion scheme
>> d) Median position in a sorted window of $N$ values
>
>> [!example] Group B
>> n) Must remain at or below 0.25 on 2D grids to prevent numerical divergence.
>> o) Sets the gradient scale below which smoothing proceeds and above which diffusion halts.
>> p) Larger values allow pixels farther away to contribute to the output, producing stronger smoothing.
>> q) The middle rank $\frac{N+1}{2}$ of the ascending sequence.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)
>> d) -> q)
