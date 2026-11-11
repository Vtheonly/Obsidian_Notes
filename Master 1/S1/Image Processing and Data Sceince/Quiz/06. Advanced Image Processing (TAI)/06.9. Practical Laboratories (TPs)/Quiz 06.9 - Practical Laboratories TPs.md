---
sources:
  - "[[06.9.1. TP1 - Digital Image Acquisition, Matrix Topologies, and Fixed Thresholding]]"
  - "[[06.9.2. TP1 - Spatial Transformations, ROI Extraction, and Multi-Channel Histograms]]"
  - "[[06.9.3. TP2 Part 1 - Discrete Noise Models and Spatial Convolution Smoothing]]"
  - "[[06.9.4. TP2 Part 1 Homework - Fast Integral Filtering and Adaptive Smoothing]]"
  - "[[06.9.5. TP2 Part 2 - Edge-Preserving Non-Linear Smoothing with Nagao Filter]]"
  - "[[06.9.6. TP2 Part 3 - Mathematical Morphology, Cell Counting, and Skeletonization]]"
  - "[[06.9.7. TP2 Part 4 - Contrast Dynamics, Histogram Equalization, and CLAHE]]"
  - "[[06.9.8. TP2 Part 5 - Single-Frame Super-Resolution and Contour Stencils]]"
---
> [!question] In an image loaded by `cv2.imread` in default color mode, the unpacking `b_val, g_val, r_val = img[100, 150]` places the Blue intensity in `b_val` because OpenCV stores color channels in BGR order.
>> [!success]- Answer
>> True

> [!question] In the lab's `manual_threshold` implementation, a pixel whose gray intensity is exactly equal to the threshold value is assigned 255.
>> [!success]- Answer
>> False

> [!question] In `cv2.rectangle(im4, (200, 30), (400, 150), (255, 0, 0), thickness=2)`, the color tuple `(255, 0, 0)` draws a red outline because OpenCV lists the red component first.
>> [!success]- Answer
>> False

> [!question] `cv2.calcHist` returns a column-shaped array that the lab flattens with `.ravel()` before comparing it element-wise against the `np.bincount` histogram.
>> [!success]- Answer
>> True

> [!question] In the lab's `calculate_psnr`, comparing two identical images returns a PSNR of 0 dB because the squared error is zero.
>> [!success]- Answer
>> False

> [!question] In `fast_box_filter_integral`, once the summed-area table is built, every window sum costs four array lookups regardless of the kernel size.
>> [!success]- Answer
>> True

> [!question] The Nagao lab pads the input with `np.pad(im, 2, mode='reflect')` because a 5x5 neighborhood reaches two pixels beyond the central pixel.
>> [!success]- Answer
>> True

> [!question] Zhang-Suen thinning via `cv2.ximgproc.thinning` runs with any plain `import cv2` installation because it lives in the core module.
>> [!success]- Answer
>> False

> [!question] The `expansionHisto` function remaps intensities linearly so the darkest valid pixel maps to 0 and the brightest valid pixel maps to 255.
>> [!success]- Answer
>> True

> [!question] In `contour_stencil_2x`, the shared edge midpoints are interpolated before the low-resolution pixels are copied onto the even coordinates.
>> [!success]- Answer
>> False

> [!question] What does `cv2.imread()` do when the image file cannot be found or read?
> a) It raises a FileNotFoundError exception automatically.
> b) It returns None, which the lab detects with `if img is None` before raising its own error.
> c) It returns an empty array of shape (0, 0, 3).
> d) It prints a warning and loads a black placeholder image.
>> [!success]- Answer
>> b) It returns None, which the lab detects with `if img is None` before raising its own error.

> [!question] In the lab, `im3 = img[30:150, 200:400].copy()` extracts which region?
> a) x from 30 to 150 and y from 200 to 400, because slicing follows the column, row convention.
> b) Rows 30 through 150 and columns 200 through 400, with both endpoints included.
> c) Rows 30 through 149 and columns 200 through 399, because slicing follows the row, column convention and excludes the stop index.
> d) A centered square patch of 120 by 120 pixels.
>> [!success]- Answer
>> c) Rows 30 through 149 and columns 200 through 399, because slicing follows the row, column convention and excludes the stop index.

> [!question] The lab computes `sigma = np.sqrt(var)` before generating Gaussian noise of variance 100 because the second argument of `np.random.normal` is which quantity?
> a) The variance of the distribution.
> b) The squared mean of the samples.
> c) A seed value that makes the draws reproducible.
> d) The standard deviation of the distribution.
>> [!success]- Answer
>> d) The standard deviation of the distribution.

> [!question] In the lab's `sp_noise` salt-and-pepper generator, pixels whose random draw falls in the range `[prob / 2, prob)` are assigned which value?
> a) 255, the salt value.
> b) 128, a mid-gray impulse.
> c) 0, the pepper value.
> d) The original intensity, left unchanged.
>> [!success]- Answer
>> c) 0, the pepper value.

> [!question] Which NumPy expression builds the integral image (summed-area table) inside `fast_box_filter_integral`?
> a) `np.sum(padded, axis=(0, 1))`
> b) `np.add.reduce(padded, axis=1)`
> c) `np.gradient(padded, axis=0)`
> d) `np.cumsum(np.cumsum(padded, axis=0), axis=1)`
>> [!success]- Answer
>> d) `np.cumsum(np.cumsum(padded, axis=0), axis=1)`

> [!question] The 5x5 Nagao filter evaluates how many overlapping sub-regions around each pixel?
> a) 4
> b) 5
> c) 8
> d) 9
>> [!success]- Answer
>> d) 9

> [!question] In the erythrocyte pipeline, why is 0 passed as the threshold argument in `cv2.threshold(im1, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)`?
> a) The passed value is ignored because the Otsu flag makes OpenCV compute the optimal cutoff automatically.
> b) Zero is the hand-tuned cutoff that was experimentally best for red blood cells.
> c) A cutoff of zero marks every pixel as foreground before the morphological step.
> d) Zero activates the inverted flag instead of supplying a cutoff.
>> [!success]- Answer
>> a) The passed value is ignored because the Otsu flag makes OpenCV compute the optimal cutoff automatically.

> [!question] Right after `num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(opened_cells)`, why does the lab compute `total_cells = num_labels - 1`?
> a) The function always over-counts by one because of border padding.
> b) Label 0 is the background component, which does not correspond to a cell.
> c) The largest component must be discarded as an outlier.
> d) One label is reserved for the structuring element footprint.
>> [!success]- Answer
>> b) Label 0 is the background component, which does not correspond to a cell.

> [!question] To apply CLAHE to the color glaucoma image, the lab converts BGR to LAB, splits the channels, and applies `clahe.apply()` to which channel?
> a) The L luminance channel only, leaving a and b untouched.
> b) All three LAB channels simultaneously.
> c) The a color channel only.
> d) The blue channel of the original BGR image.
>> [!success]- Answer
>> a) The L luminance channel only, leaving a and b untouched.

> [!question] For a 256x256 low-resolution input, `contour_stencil_2x` returns an image of what size?
> a) 512x512, exactly doubled in each dimension.
> b) 511x511, following the 2h-1 by 2w-1 output formula.
> c) 255x255, one pixel short in each dimension.
> d) 1024x1024, doubled twice.
>> [!success]- Answer
>> b) 511x511, following the 2h-1 by 2w-1 output formula.

> [!question] Match each element of the TP1 thresholding lab with its role.
>> [!example] Group A
>> a) `cv2.imread(path, cv2.IMREAD_GRAYSCALE)`
>> b) `cv2.threshold(img, 80, 255, cv2.THRESH_BINARY)`
>> c) The underscore in `_, imgb1 = cv2.threshold(...)`
>> d) `np.zeros_like(gray_img)`
>> e) `np.array_equal(imgb1, imgb2)`
>> f) `cv2.imwrite(path, img)`
>
>> [!example] Group B
>> n) Binarizes against a global cutoff into a 0/255 mask.
>> o) Verifies element-wise that both binarizations agree.
>> p) Serializes the result matrix back to disk.
>> q) Loads the raster into RAM as a single-channel uint8 matrix.
>> r) Pre-allocates an output buffer matching the input's shape and dtype.
>> s) Discards the first returned value and keeps the binarized image.
>
>> [!success]- Answer
>> a) -> q)
>> b) -> n)
>> c) -> s)
>> d) -> r)
>> e) -> o)
>> f) -> p)

> [!question] Match the spatial transformation call from TP1 Exercise 4 with its effect.
>> [!example] Group A
>> a) `cv2.resize(img, (w // 2, h // 2), interpolation=cv2.INTER_LINEAR)`
>> b) `img[30:150, 200:400].copy()`
>> c) `cv2.putText(im4, "My rectangle", (200, 20), ...)`
>> d) `cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)`
>> e) `cv2.GaussianBlur(img, ksize=(5, 5), sigmaX=1.5)`
>
>> [!example] Group B
>> n) Turns the frame a quarter turn to the right.
>> o) Halves the frame dimensions with weighted neighborhood averaging.
>> p) Applies isotropic low-pass smoothing that softens detail.
>> q) Crops the bounded region of interest out of the frame.
>> r) Renders a text caption onto the annotated copy.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> r)
>> d) -> n)
>> e) -> p)

> [!question] Match each noise-filtering scenario from the TP2 Part 1 benchmark with its observed outcome.
>> [!example] Group A
>> a) `np.clip(noisy, 0, 255)` in the Gaussian generator
>> b) Median filtering of Gaussian noise
>> c) Median filtering of salt-and-pepper noise
>> d) Mean filtering of salt-and-pepper noise
>
>> [!example] Group B
>> n) Completely eliminates the impulse corruption.
>> o) Smears impulse pixels into visible dark and bright smudges.
>> p) Clamps float sums back into the 8-bit range before the uint8 cast.
>> q) Leaves residual variance in the restored image.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] Match the NumPy utility with the role it plays in the TP2 labs.
>> [!example] Group A
>> a) `np.pad`
>> b) `np.random.rand`
>> c) `np.median`
>> d) `np.log10`
>
>> [!example] Group B
>> n) Draws uniform samples whose two thresholds pick which pixels get corrupted.
>> o) Converts the squared-error ratio into decibels.
>> p) Mirror-extends the border so every filter window overlaps real pixels.
>> q) Computes the order statistic behind the non-linear smoothing response.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)

> [!question] Match the integral-filtering or adaptive-smoothing mechanism with its purpose.
>> [!example] Group A
>> a) The extra leading row and column of zeros in the integral array
>> b) `np.var(patch)` computed on each local window
>> c) A flat region where local variance is close to the noise variance
>> d) An edge region where local variance far exceeds the noise variance
>
>> [!example] Group B
>> n) Keeps the output close to the original pixel, preserving edge sharpness.
>> o) Lets the four-corner lookup formula read row 0 and column 0 without special cases.
>> p) Scales how strongly each pixel gets smoothed.
>> q) Reduces the output toward the local mean, wiping out noise.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> q)
>> d) -> n)

> [!question] Match the Nagao filter mechanism or benchmark result with its description.
>> [!example] Group A
>> a) Sub-region selection rule
>> b) Center pixel replacement
>> c) 5x5 mean filter benchmark
>> d) 5x5 Nagao filter benchmark
>
>> [!example] Group B
>> n) Significantly blurs edge transitions.
>> o) Replaces the pixel with the mean of the most homogeneous sector.
>> p) Produces sharp, clean edge boundaries.
>> q) Selects the sector with the lowest spread.
>
>> [!success]- Answer
>> a) -> q)
>> b) -> o)
>> c) -> n)
>> d) -> p)

> [!question] Match the erythrocyte pipeline call with its role.
>> [!example] Group A
>> a) `cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))`
>> b) `cv2.morphologyEx(imb1, cv2.MORPH_OPEN, se_5)`
>> c) `cv2.connectedComponentsWithStats(opened_cells)`
>> d) `cv2.ximgproc.thinning(opened_cells)`
>
>> [!example] Group B
>> n) Labels each blob in two passes and reports its area and bounding box.
>> o) Breaks the thin bridges connecting neighboring cells.
>> p) Shrinks every blob to its centerline skeleton.
>> q) Builds the flat probe swept over the binary mask.
>
>> [!success]- Answer
>> a) -> q)
>> b) -> o)
>> c) -> n)
>> d) -> p)

> [!question] Match the contrast-enhancement call or parameter with its effect.
>> [!example] Group A
>> a) The `seuil` argument of `expansionHisto`
>> b) `cv2.normalize(im1, None, 0, 255, cv2.NORM_MINMAX)`
>> c) `clipLimit=2.0` in `cv2.createCLAHE`
>> d) `tileGridSize=(8, 8)` in `cv2.createCLAHE`
>
>> [!example] Group B
>> n) Caps how much any histogram bin may be amplified.
>> o) Divides the image into a grid of blocks, each equalized separately.
>> p) Excludes low-count bins when locating the min and max stretch bounds.
>> q) Performs the library's one-call linear contrast stretch.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] Match the step of `contour_stencil_2x` with what it does.
>> [!example] Group A
>> a) `out[2 * y, 2 * x] = im[y, x]`
>> b) The cell-center value when one variation is strictly smaller
>> c) The cell-center value when both variations are equal
>> d) The shared edge midpoint updates
>
>> [!example] Group B
>> n) Takes one quarter of the sum of the four surrounding corners.
>> o) Averages the two pixels at the ends of the favored diagonal.
>> p) Averages the values directly above and below, or left and right.
>> q) Seats each original sample on every other row and column of the output.
>
>> [!success]- Answer
>> a) -> q)
>> b) -> o)
>> c) -> n)
>> d) -> p)

> [!question] Match the 2x upsampling method from the super-resolution benchmark with its observed behavior.
>> [!example] Group A
>> a) Nearest neighbor
>> b) Bilinear
>> c) Bicubic
>> d) Contour Stencils
>
>> [!example] Group B
>> n) Produces soft, blurred edge boundaries.
>> o) Introduces severe pixelation and block artifacts despite being fastest.
>> p) Balances sharpness and smoothness with competitive PSNR scores.
>> q) Delivers superior subjective edge sharpness on directional strokes like historic typography.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)
>> d) -> q)
