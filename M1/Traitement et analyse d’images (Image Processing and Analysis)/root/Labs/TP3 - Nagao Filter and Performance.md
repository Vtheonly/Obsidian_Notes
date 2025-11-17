# Lab 3: The Nagao Filter and Performance Analysis

**Objective:** To implement and understand the Nagao filter, an advanced non-linear spatial filter designed for edge-preserving smoothing, and to evaluate its performance against simpler filters.

## 1. The Concept of the Nagao Filter

The Nagao filter is an adaptive smoothing filter that aims to reduce noise without blurring important structural details like edges and corners. It achieves this by being selective about the neighborhood it uses for averaging.

### The Limitation of Simpler Filters
-   **Mean Filter:** Averages indiscriminately, blurring everything.
-   **Median Filter:** Preserves edges better but can still degrade fine textures and corners.

### The Nagao Mechanism
The filter operates on a local neighborhood (e.g., 5x5) around each pixel. Instead of using the entire neighborhood for calculation, it first divides the neighborhood into several smaller sub-regions.

1.  **Define Sub-Regions:** Within the 5x5 window, the algorithm defines a set of pre-determined sub-regions (typically 9 regions of 7 pixels each, including the center). These sub-regions are shaped to represent different orientations (lines, corners).
2.  **Calculate Variance:** For each of these sub-regions, it calculates the intensity variance.
    -   **Variance** is a measure of how spread out the pixel values are. A low variance indicates a smooth, homogeneous region, while a high variance indicates a region with edges or texture.
3.  **Identify the Smoothest Sub-Region:** The algorithm identifies the sub-region with the **minimum variance**. This is the most homogeneous (smoothest) sub-region in the neighborhood.
4.  **Calculate the Mean:** It then calculates the mean (average) intensity of the pixels *only within that winning sub-region*.
5.  **Assign New Value:** The central pixel of the 5x5 window is replaced with this calculated mean.

### The Core Insight
By selecting the sub-region with the lowest variance, the Nagao filter intelligently adapts to the local image structure.
-   **In a flat, uniform area:** All sub-regions will have low variance, and the result will be similar to a standard mean filter.
-   **Near an edge:** The sub-regions that lie *along* the edge will be relatively homogeneous and have low variance. The sub-regions that lie *across* the edge will contain a sharp transition and have high variance. The filter will choose a sub-region aligned with the edge, thus averaging pixels on the same side of the edge and preserving its sharpness.

## 2. Implementation and Performance

### Implementation Details
Implementing the Nagao filter requires a nested loop structure:
1.  Iterate through each pixel of the input image (excluding borders).
2.  For each pixel, extract the 5x5 neighborhood.
3.  Within the neighborhood, iterate through the 9 pre-defined sub-regions.
4.  For each sub-region, calculate its variance and mean.
5.  Keep track of the sub-region with the minimum variance found so far.
6.  After checking all sub-regions, assign the mean of the minimum-variance sub-region to the output pixel.

### Performance Evaluation
As with other filters, the performance is quantified using **PSNR** by comparing the filtered image to the original, noise-free ground truth.

-   **Expected Outcome:** The Nagao filter should yield a significantly higher PSNR than the mean filter when applied to noisy images containing sharp edges. It effectively smooths noise in uniform areas while protecting the high-frequency information that defines the edges.
-   **Computational Cost:** The Nagao filter is computationally more expensive than the mean or median filters because it requires calculating multiple variances and means for every single pixel in the image. This trade-off between performance and computational cost is a common theme in image processing.