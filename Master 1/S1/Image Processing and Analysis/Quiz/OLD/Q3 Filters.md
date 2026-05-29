---
sources:
  - "[[2.2 Linear Spatial Filters (Mean, Gaussian).md]]"
  - "[[2.3 Non-Linear Spatial Filters (Median, Nagao).md]]"
  - "[[TP2 - Noise Generation and Filtering.md]]"
  - "[[TP3 - Nagao Filter and Performance.md]]"
  - "[[Gabor Filters.md]]"
  - "[[Convolution.md]]"
  - "[[The Fourier Transform in Imaging.md]]"
---

> [!question] The Mean (Averaging) filter is the most effective choice for removing Salt-and-Pepper (impulse) noise.
>> [!success]- Answer
>> False
>> **Explanation:** The Mean filter averages the noise with surrounding pixels, smudging the error. The **Median** filter is the correct choice for Salt-and-Pepper noise.

> [!question] A Gaussian filter uses a kernel where pixels closer to the center have higher weights than those at the periphery.
>> [!success]- Answer
>> True

> [!question] The Nagao filter is considered a "Linear" filter because it uses convolution to calculate the output.
>> [!success]- Answer
>> False
>> **Explanation:** The Nagao filter is **Non-Linear**. It uses logic (calculating variance of sub-regions) to select which pixels to average, rather than a fixed weighted sum.

> [!question] Increasing the `sigma` ($\sigma$) value in a Gaussian filter reduces the amount of blurring.
>> [!success]- Answer
>> False
>> **Explanation:** Increasing `sigma` widens the bell curve, considering a larger neighborhood, which results in **more** blurring.

> [!question] The Median filter preserves sharp edges better than the Mean filter.
>> [!success]- Answer
>> True

> [!question] To implement a spatial filter manually (without using `cv2.blur`), you must iterate over every pixel and apply the kernel to its neighborhood.
>> [!success]- Answer
>> True

> [!question] A Gabor filter is constructed by multiplying a Gaussian kernel with a sinusoidal wave.
>> [!success]- Answer
>> True

> [!question] If you apply a 3x3 Mean filter to an image, the resulting image will be sharper than the original.
>> [!success]- Answer
>> False
>> **Explanation:** Mean filters smooth (blur) the image, reducing sharpness.

> [!question] In the frequency domain, a Low-Pass filter attenuates high frequencies, resulting in a smoothing effect similar to a Mean filter.
>> [!success]- Answer
>> True

> [!question] The Nagao filter chooses the sub-region with the *maximum* variance to calculate the mean.
>> [!success]- Answer
>> False
>> **Explanation:** It chooses the sub-region with the **minimum** variance (the smoothest area) to avoid averaging across edges.

> [!question] Convolution in the spatial domain is computationally equivalent to element-wise multiplication in the frequency domain.
>> [!success]- Answer
>> True

> [!question] The Median filter is sensitive to outliers, meaning a single extreme white pixel will significantly skew the result.
>> [!success]- Answer
>> False
>> **Explanation:** The Median filter is **robust** to outliers. The extreme value is sorted to the end of the list and ignored. The *Mean* filter is sensitive to outliers.

> [!question] A "Separable" filter (like Gaussian) allows you to perform two 1D convolutions instead of one 2D convolution to save processing time.
>> [!success]- Answer
>> True

> [!question] Gabor filters are primarily used for noise reduction rather than feature extraction.
>> [!success]- Answer
>> False
>> **Explanation:** Gabor filters are primarily used for **texture analysis and feature extraction** (detecting specific orientations/frequencies).

> [!question] "Padding" with `cv2.copyMakeBorder` is used to discard the edges of an image before filtering.
>> [!success]- Answer
>> False
>> **Explanation:** Padding adds pixels *around* the image so the filter kernel can process the original border pixels without going out of bounds.

> [!question] Which filter is best suited for removing Gaussian noise (random variations in brightness)?
> a) Median Filter
> b) Mean (or Gaussian) Filter
> c) High-Pass Filter
> d) Laplacian Filter
>> [!success]- Answer
>> b) Mean (or Gaussian) Filter

> [!question] What is the primary advantage of the Nagao filter over the Mean filter?
> a) It is much faster to compute.
> b) It preserves edges while smoothing homogeneous regions.
> c) It removes Salt-and-Pepper noise better than the Median filter.
> d) It increases the resolution of the image.
>> [!success]- Answer
>> b) It preserves edges while smoothing homogeneous regions.

> [!question] In a custom implementation of a 3x3 Mean filter, what is the value of every element in the kernel?
> a) 1
> b) 0
> c) 1/9
> d) 1/3
>> [!success]- Answer
>> c) 1/9

> [!question] Which parameter of the Gabor filter controls the orientation of the features it detects (e.g., vertical vs. horizontal lines)?
> a) Sigma ($\sigma$)
> b) Lambda ($\lambda$)
> c) Theta ($\theta$)
> d) Gamma ($\gamma$)
>> [!success]- Answer
>> c) Theta ($\theta$)

> [!question] How does the Median filter calculate the new value for a pixel?
> a) It calculates the weighted average of the neighborhood.
> b) It sorts the neighborhood values and selects the middle value.
> c) It selects the maximum value in the neighborhood.
> d) It multiplies the pixels by a sine wave.
>> [!success]- Answer
>> b) It sorts the neighborhood values and selects the middle value.

> [!question] Which OpenCV function is used to apply a simple averaging (Mean) filter?
> a) `cv2.blur()`
> b) `cv2.medianBlur()`
> c) `cv2.gaussianBlur()`
> d) `cv2.filter2D()`
>> [!success]- Answer
>> a) `cv2.blur()`

> [!question] What happens if you use a High-Pass filter on an image?
> a) The image becomes blurry.
> b) The image brightness increases uniformly.
> c) Edges and fine details are enhanced (sharpened).
> d) Salt-and-Pepper noise is removed.
>> [!success]- Answer
>> c) Edges and fine details are enhanced (sharpened).

> [!question] In the context of the Nagao filter, why is the variance calculated for each sub-region?
> a) To find the brightest region.
> b) To find the darkest region.
> c) To determine which region is the most homogeneous (smoothest).
> d) To find the region with the most noise.
>> [!success]- Answer
>> c) To determine which region is the most homogeneous (smoothest).

> [!question] Why is the Gaussian filter preferred over the Box (Mean) filter for smoothing?
> a) It is faster.
> b) It produces a more natural blur with fewer artifacts (less "blocky").
> c) It removes edges completely.
> d) It requires no parameters.
>> [!success]- Answer
>> b) It produces a more natural blur with fewer artifacts (less "blocky").

> [!question] What is the "Kernel" in the context of spatial filtering?
> a) The central pixel of the image.
> b) A small matrix of weights that slides over the image.
> c) The frequency spectrum of the image.
> d) The border of the image.
>> [!success]- Answer
>> b) A small matrix of weights that slides over the image.

> [!question] Which distance metric is implicitly used by a standard $N \times N$ square neighborhood (like in the Mean filter)?
> a) Euclidean Distance
> b) Manhattan Distance
> c) Chebyshev (Chessboard) Distance
> d) Mahalanobis Distance
>> [!success]- Answer
>> c) Chebyshev (Chessboard) Distance

> [!question] If an image suffers from periodic noise (structured patterns), which filtering domain is most effective?
> a) Spatial Domain (using Median filter)
> b) Spatial Domain (using Mean filter)
> c) Frequency Domain (using Band-Reject filter)
> d) Morphological Domain
>> [!success]- Answer
>> c) Frequency Domain (using Band-Reject filter)

> [!question] What is the mathematical operation denoted by $f \otimes h$ in filtering?
> a) Multiplication
> b) Subtraction
> c) Convolution
> d) Division
>> [!success]- Answer
>> c) Convolution

> [!question] When implementing a custom filter in Python, why are nested loops (for i, for j) generally discouraged for large images?
> a) They are inaccurate.
> b) They are computationally slow compared to optimized NumPy/OpenCV functions.
> c) They cannot handle color images.
> d) They consume too much memory.
>> [!success]- Answer
>> b) They are computationally slow compared to optimized NumPy/OpenCV functions.

> [!question] Which filter would you use to extract texture features for a machine learning classifier?
> a) Mean Filter
> b) Filter Bank of Gabor Filters
> c) Median Filter
> d) High-Pass Filter
>> [!success]- Answer
>> b) Filter Bank of Gabor Filters

> [!question] Match the Filter with its primary use case.
>> [!example] Group A
>> a) Median Filter
>> b) Gaussian Filter
>> c) Gabor Filter
>> d) High-Pass Filter
>
>> [!example] Group B
>> n) Removing Salt-and-Pepper noise.
>> o) Smoothing/Blurring natural images.
>> p) Analyzing texture orientation.
>> q) Sharpening / Edge Detection.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the kernel property to the filter type.
>> [!example] Group A
>> a) All weights are equal (e.g., 1/9).
>> b) Weights follow a bell curve shape.
>> c) Weights sum to 0 (typically).
>
>> [!example] Group B
>> n) Gaussian Filter.
>> o) Mean Filter.
>> p) Edge Detection / High-Pass Filter.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the Nagao filter step to its purpose.
>> [!example] Group A
>> a) Divide neighborhood into sub-regions
>> b) Calculate Variance of sub-regions
>> c) Select Minimum Variance region
>
>> [!example] Group B
>> n) To evaluate the "smoothness" of each area.
>> o) To define possible directions (lines, corners).
>> p) To avoid averaging across an edge.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the Frequency Domain term with its definition.
>> [!example] Group A
>> a) FFT (Fast Fourier Transform)
>> b) Low Frequencies
>> c) High Frequencies
>
>> [!example] Group B
>> n) Detailed parts of the image (edges, noise).
>> o) Algorithm to convert Spatial to Frequency domain.
>> p) Smooth parts of the image (sky, walls).
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the OpenCV function to the filter it implements.
>> [!example] Group A
>> a) `cv2.medianBlur`
>> b) `cv2.GaussianBlur`
>> c) `cv2.blur`
>
>> [!example] Group B
>> n) Linear Averaging Filter.
>> o) Non-linear Order-Statistic Filter.
>> p) Linear Weighted Filter (Bell curve).
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the Gabor parameter to what it controls.
>> [!example] Group A
>> a) $\theta$ (Theta)
>> b) $\lambda$ (Lambda)
>> c) $\sigma$ (Sigma)
>
>> [!example] Group B
>> n) The size of the receptive field (Gaussian envelope).
>> o) The orientation of the strips.
>> p) The frequency (thickness) of the strips.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the Filter Category to the specific filter.
>> [!example] Group A
>> a) Linear Filter
>> b) Non-Linear Filter
>> c) Frequency Domain Filter
>
>> [!example] Group B
>> n) Nagao Filter.
>> o) Band-Reject Filter.
>> p) Mean Filter.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the border handling method with its description.
>> [!example] Group A
>> a) Zero Padding
>> b) Mirror/Reflection Padding
>> c) Replication Padding
>
>> [!example] Group B
>> n) Fills border with black pixels (0).
>> o) Replicates the last pixel value at the edge.
>> p) Mirrors the pixels inside the image across the border.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the noise type to the reason why specific filters fail/succeed.
>> [!example] Group A
>> a) Gaussian Noise
>> b) Salt-and-Pepper Noise
>
>> [!example] Group B
>> n) Fails with Mean filter because extreme values skew the average.
>> o) Succeeds with Mean filter because average of random errors approaches zero.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the Filter size to its expected outcome (assuming Mean filter).
>> [!example] Group A
>> a) 3x3 Kernel
>> b) 15x15 Kernel
>
>> [!example] Group B
>> n) Strong blurring, loss of object definition.
>> o) Slight smoothing, most details preserved.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)