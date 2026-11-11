---
sources:
  - "[[15. OpenCV Core Architecture - Matrix Representation, Channels, and Color Constellations]]"
  - "[[16. Image Spatial Transformations - Interpolation, Scaling, Cropping, and Affine Warping]]"
  - "[[17. SciPy Signal and Spatial Operations - 2D Filtering and Morphology]]"
  - "[[18. Visual Frequency and Radiometry - Histograms, Equalization, AHE, and CLAHE]]"
  - "[[19. Spatial Image Restoration - Noise Models, Linear Convolution, and Fast Integral Filters]]"
  - "[[20. Non-Linear and Edge-Preserving Filtering - Median, Bilateral, and Nagao Filters]]"
  - "[[21. Mathematical Morphology - Set Theory, Structuring Elements, and Thinning]]"
  - "[[22. Objective Image Quality Assessment - MSE, PSNR, and SSIM Metrics]]"
  - "[[24. Super-Resolution and Edge-Adaptive Interpolation - Pascal Getreuer Contour Stencils]]"
  - "[[25. Bilateral Filtering - Complete Mathematical Theory, Implementation, and Practice]]"
  - "[[26. Nagao Filtering - Multi-Implementation Reference with Hardcoded Kernels, Vectorized, and Convolution Approaches]]"
---
> [!question] In an image loaded with `cv2.imread` using `cv2.IMREAD_COLOR`, the pixel tuple `img[y, x]` stores the red component at index 0 because OpenCV follows the RGB display convention.
>> [!success]- Answer
>> False

> [!question] Computing `cv2.add` on the uint8 values 250 and 20 yields 255, whereas adding the same values with plain NumPy operators wraps around to 14.
>> [!success]- Answer
>> True

> [!question] A region of interest extracted with plain NumPy slicing such as `img[y1:y2, x1:x2]` is a memory view, so modifying its pixels also changes the source image unless `.copy()` is used.
>> [!success]- Answer
>> True

> [!question] `scipy.signal.convolve2d` flips the kernel before sliding it over the image, so for asymmetric kernels such as Sobel it differs from plain cross-correlation.
>> [!success]- Answer
>> True

> [!question] `cv2.equalizeHist` can be called directly on a 3-channel BGR image and equalizes all three color channels in one call.
>> [!success]- Answer
>> False

> [!question] Once the integral image has been built, the sum of any rectangular window is obtained from four corner lookups and additions, in constant time regardless of kernel size.
>> [!success]- Answer
>> True

> [!question] On an image corrupted by salt-and-pepper noise, a mean filter is pulled toward the extreme 0 or 255 values, while a median filter discards such outliers through rank sorting.
>> [!success]- Answer
>> True

> [!question] `cv2.connectedComponentsWithStats` returns a label count that already excludes the background, so `num_labels` equals the number of foreground objects.
>> [!success]- Answer
>> False

> [!question] The bilateral filter is the appropriate first choice for removing salt-and-pepper impulse noise, because its range kernel rejects intensities far from the center pixel.
>> [!success]- Answer
>> False

> [!question] OpenCV's `cv2.BORDER_REFLECT` flag and NumPy's `np.pad` reflect mode implement the same boundary behavior, so filter outputs compared across the two libraries match pixel-for-pixel.
>> [!success]- Answer
>> False

> [!question] In `cv2.bilateralFilter`, what happens when the diameter parameter `d` is passed a value of `-1`?
> a) The filter raises an error because the diameter must be a positive odd number.
> b) The filter falls back to a fixed default diameter of 5 pixels.
> c) OpenCV derives the window diameter from `sigmaSpace`, rounded to an odd value.
> d) The spatial term is disabled and only the range kernel is applied.
>> [!success]- Answer
>> c) OpenCV derives the window diameter from `sigmaSpace`, rounded to an odd value.

> [!question] How does `cv2.resize` interpret the `dsize` tuple that specifies the target resolution?
> a) As a (height, width) pair, matching the NumPy shape convention.
> b) As a (width, height) pair, the opposite of the NumPy shape convention.
> c) As relative scale factors along each axis.
> d) As the center point coordinates of the output raster.
>> [!success]- Answer
>> b) As a (width, height) pair, the opposite of the NumPy shape convention.

> [!question] For an input of shape $(M_1, N_1)$ convolved with a kernel of shape $(M_2, N_2)$, what output shape does `scipy.signal.convolve2d` return with `mode='full'`?
> a) $(M_1 + M_2 - 1, N_1 + N_2 - 1)$
> b) $(M_1, N_1)$
> c) $(M_1 - M_2 + 1, N_1 - N_2 + 1)$
> d) $(M_1 + M_2, N_1 + N_2)$
>> [!success]- Answer
>> a) $(M_1 + M_2 - 1, N_1 + N_2 - 1)$

> [!question] How should CLAHE be applied to a color image so that the colors are preserved?
> a) Apply the CLAHE object directly to the 3-channel BGR tensor.
> b) Apply CLAHE independently to the blue, green, and red planes, then merge them.
> c) Convert to grayscale, apply CLAHE, and stack the result back into three channels.
> d) Convert to LAB, apply CLAHE to the lightness channel only, merge, and convert back to BGR.
>> [!success]- Answer
>> d) Convert to LAB, apply CLAHE to the lightness channel only, merge, and convert back to BGR.

> [!question] In `cv2.GaussianBlur(src, ksize, sigmaX)`, what does passing `sigmaX=0` do?
> a) It disables smoothing and returns a copy of the source image.
> b) It makes OpenCV derive the Gaussian sigma from the kernel size.
> c) It derives the kernel size from the sigma argument.
> d) It applies a box filter instead of a Gaussian kernel.
>> [!success]- Answer
>> b) It makes OpenCV derive the Gaussian sigma from the kernel size.

> [!question] In the Nagao filter, after the variance of each of the nine sub-regions has been computed, what value is written to the center pixel?
> a) The minimum variance value itself, rescaled to the 0 to 255 intensity range.
> b) The median of the nine sub-region means.
> c) The mean of the sub-region with the smallest variance.
> d) The average of the means of all nine sub-regions.
>> [!success]- Answer
>> c) The mean of the sub-region with the smallest variance.

> [!question] Which flag passed to `cv2.getStructuringElement` produces a cross-shaped structuring element aligned with the cardinal axes?
> a) `cv2.MORPH_RECT`
> b) `cv2.MORPH_CROSS`
> c) `cv2.MORPH_ELLIPSE`
> d) `cv2.MORPH_OPEN`
>> [!success]- Answer
>> b) `cv2.MORPH_CROSS`

> [!question] In the PSNR implementation, what is returned when the two compared images are identical?
> a) The value 0, indicating zero error.
> b) The value 255, the maximum 8-bit intensity.
> c) A division-by-zero exception.
> d) Infinity, since the mean squared error is zero.
>> [!success]- Answer
>> d) Infinity, since the mean squared error is zero.

> [!question] In the contour stencil factor-2 upscaling implementation, when the total variation of one diagonal is strictly smaller than that of the other, how is the cell center point X computed?
> a) As the average of the two corner pixels along the smaller-variation diagonal.
> b) As the average of the two corner pixels along the larger-variation diagonal.
> c) As the average of all four corner pixels of the cell.
> d) As a copy of the top-left corner pixel value.
>> [!success]- Answer
>> a) As the average of the two corner pixels along the smaller-variation diagonal.

> [!question] In the convolution-based Nagao implementation, why must the image be cast to `float64` before evaluating `f * f`?
> a) Because `cv2.filter2D` rejects uint8 inputs entirely.
> b) Because floating-point convolution runs faster than integer convolution.
> c) Because squared pixel values reach $255^2 = 65025$, far past the uint8 maximum, so uint8 arithmetic would overflow.
> d) Because the mean kernels contain fractional weights that uint8 arrays cannot store.
>> [!success]- Answer
>> c) Because squared pixel values reach $255^2 = 65025$, far past the uint8 maximum, so uint8 arithmetic would overflow.

> [!question] Match the OpenCV core function with its documented behavior.
>> [!example] Group A
>> a) `cv2.imread`
>> b) `cv2.split`
>> c) `cv2.merge`
>> d) `cv2.cvtColor`
>
>> [!example] Group B
>> n) Decomposes a multi-channel tensor into separate single-channel planes.
>> o) Reassembles single-channel planes back into one multi-channel tensor.
>> p) Loads a raster into RAM and returns None when the path is invalid or decoding fails.
>> q) Converts between color spaces, for example swapping the outer channels of a BGR array.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)
>> d) -> q)

> [!question] Match the `cv2.resize` interpolation flag with its sampling behavior.
>> [!example] Group A
>> a) `cv2.INTER_NEAREST`
>> b) `cv2.INTER_LINEAR`
>> c) `cv2.INTER_CUBIC`
>> d) `cv2.INTER_AREA`
>
>> [!example] Group B
>> n) Bicubic spline sampling over a $4 \times 4$ neighborhood, producing sharper edges with fewer artifacts.
>> o) Pixel-area resampling preferred for downsampling without aliasing.
>> p) The fastest method, but it produces visible pixelation and jagged staircase edges.
>> q) Bilinear sampling over a $2 \times 2$ neighborhood, the standard choice for general upsampling.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] Match the `scipy.signal.convolve2d` argument value with its effect on the computation.
>> [!example] Group A
>> a) `'same'`
>> b) `'valid'`
>> c) `'fill'`
>> d) `'symm'`
>> e) `'wrap'`
>
>> [!example] Group B
>> n) Computes output only where the kernel overlaps the input completely.
>> o) Mirrors pixel values across the image boundary, preserving border brightness.
>> p) Pads the border with a constant value, which darkens border regions when that constant is zero.
>> q) Treats the image as periodic, reading values from the opposite edge.
>> r) Returns the central portion of the convolution, matching the shape of the first input.
>
>> [!success]- Answer
>> a) -> r)
>> b) -> n)
>> c) -> p)
>> d) -> o)
>> e) -> q)

> [!question] Match the histogram or contrast routine with its role in radiometric processing.
>> [!example] Group A
>> a) `cv2.calcHist`
>> b) `cv2.normalize`
>> c) `cv2.createCLAHE`
>> d) `np.bincount`
>
>> [!example] Group B
>> n) Constructs the clipped, tile-based adaptive equalization operator configured by `clipLimit` and `tileGridSize`.
>> o) Counts pixels per intensity bin, with parameters for channels, mask, bin count, and range.
>> p) Maps the array minimum onto `alpha` and the maximum onto `beta` under the `NORM_MINMAX` type.
>> q) NumPy counting routine used inside the custom contrast-stretching code to obtain the 256-bin histogram.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
>> d) -> q)

> [!question] Match the noise-synthesis or padding routine with its documented use.
>> [!example] Group A
>> a) `np.random.normal`
>> b) `np.random.rand`
>> c) `np.random.seed`
>> d) `np.pad`
>> e) `cv2.copyMakeBorder`
>
>> [!example] Group B
>> n) Draws uniform samples that, after thresholding, decide which pixels become salt or pepper.
>> o) Enlarges the raster by half the kernel width on every side so that windows always overlap real data.
>> p) Draws per-pixel Gaussian-distributed samples for additive white noise synthesis.
>> q) Fixes the generator state so that synthetic noise is reproducible from run to run.
>> r) Produces an explicitly padded copy of the image under a chosen border type.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)
>> e) -> r)

> [!question] Match the morphology or component-analysis routine with its role.
>> [!example] Group A
>> a) `cv2.getStructuringElement`
>> b) `cv2.morphologyEx`
>> c) `cv2.connectedComponentsWithStats`
>> d) `cv2.ximgproc.thinning`
>> e) `cv2.distanceTransform`
>
>> [!example] Group B
>> n) Applies a compound operation such as opening or closing in a single call.
>> o) Builds a probe kernel of a chosen shape, such as a full rectangle, a cross, or a discretized disk.
>> p) Computes the Euclidean distance from each foreground pixel to the nearest background boundary.
>> q) Reduces a binary shape to a one-pixel-wide skeleton and requires the contrib modules.
>> r) Labels connected pixel groups and returns per-component bounding boxes, areas, and centroids.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> r)
>> d) -> q)
>> e) -> p)

> [!question] Match the quality metric or constant with its meaning.
>> [!example] Group A
>> a) MSE
>> b) PSNR
>> c) SSIM
>> d) $C_1$ and $C_2$
>
>> [!example] Group B
>> n) Logarithmic decibel ratio of peak signal power to noise power, using 255 as the peak for 8-bit data.
>> o) Regularization constants built from $K_1 = 0.01$ and $K_2 = 0.03$ that prevent division by zero.
>> p) Average of the squared per-pixel differences between the reference and the degraded image.
>> q) Product of luminance, contrast, and structural-correlation comparisons between local statistics.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)

> [!question] Match the contour stencil concept with its role in factor-2 upscaling.
>> [!example] Group A
>> a) Total variation of a curve
>> b) Stencil set
>> c) Edge midpoints
>> d) Output grid
>
>> [!example] Group B
>> n) Family of twelve candidate geometric configurations encoding eight discretized contour orientations.
>> o) Sub-pixel points shared between adjacent cells, each obtained by averaging the two bordering values.
>> p) Quantity that approaches zero when a candidate path runs along a nearly constant image contour.
>> q) Lattice of size $2H - 1$ by $2W - 1$ that receives the known samples at even coordinates.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)
>> d) -> q)

> [!question] Match the bilateral filter parameter or optimization with its effect.
>> [!example] Group A
>> a) `sigmaColor`
>> b) `sigmaSpace`
>> c) `d`
>> d) Range LUT
>
>> [!example] Group B
>> n) Diameter of the spatial support; larger values average more neighbor candidates at higher computational cost.
>> o) Spread of the Gaussian applied to intensity differences; small values give strong edge preservation but weak smoothing.
>> p) Precomputed table of 256 range weights that replaces a transcendental call per neighbor.
>> q) Spread of the Gaussian applied to geometric distance, expressed in pixel units.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match the Nagao implementation strategy with its measured characteristics.
>> [!example] Group A
>> a) Pure-loop variant
>> b) Fancy-indexing variant
>> c) Hardcoded-kernel variant
>> d) Sliding-window variant
>
>> [!example] Group B
>> n) Eighteen SIMD correlations with normalized mean masks through the OpenCV engine; about 0.009 seconds, 763 times faster than the reference.
>> o) Nested interpreter traversal of every pixel and sector; about 6.8 seconds, the auditable ground truth for testing.
>> p) Batched gathering of each sector's values with the $E[X^2] - E[X]^2$ identity; about 0.088 seconds.
>> q) Zero-copy neighborhood views fed to `einsum`; the squared term still materializes a large 4-D float copy.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
>> d) -> q)
