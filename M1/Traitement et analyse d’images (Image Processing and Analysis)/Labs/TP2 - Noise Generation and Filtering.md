
## 1. Simulating Image Noise (Exercise 1)

Noise is any unwanted random variation in image brightness or color information. This exercise simulates two of the most common types.

### Additive Noise (Gaussian)
-   **Concept:** Gaussian noise is characterized by adding a random value from a Gaussian (normal) distribution to each pixel's intensity.
-   **Characteristics:**
    -   It affects *every pixel* in the image.
    -   It is described by its mean (μ) and variance (σ²). A higher variance results in more intense noise.
    -   It is a good model for sensor noise caused by poor lighting or high temperature.
-   **Simulation:** To add Gaussian noise, one generates a matrix of random numbers with a Gaussian distribution (mean 0, specified variance) and adds it to the original image matrix.

### Impulse Noise (Salt & Pepper)
-   **Concept:** Impulse noise is characterized by randomly replacing a fraction of image pixels with either a maximum value (salt/white) or a minimum value (pepper/black).
-   **Characteristics:**
    -   It affects only a *subset* of pixels.
    -   It is described by the *density* or percentage (`p`) of corrupted pixels.
    -   It is a good model for errors in data transmission or faulty memory locations in hardware.
-   **Simulation:** To add salt & pepper noise, one randomly selects a percentage of pixel locations. For each selected location, it is randomly assigned a value of either 0 or 255.

## 2. Applying Spatial Filters (Exercise 2)

Spatial filtering involves applying an operation (via a kernel or neighborhood rule) to a group of pixels to calculate a new value for the central pixel.

### The Mean Filter (Linear)
-   **Mechanism:** This is a linear filter that replaces the value of each pixel with the average (mean) of the intensity values in its neighborhood. This is achieved through convolution with a kernel where all elements are equal (e.g., `1/9` for a 3x3 kernel).
-   **Effectiveness:**
    -   **Good for Gaussian Noise:** Since Gaussian noise is a zero-mean random process, averaging tends to cancel it out, resulting in a smoother image.
    -   **Poor for Impulse Noise:** An extreme outlier (like a white pixel in a dark area) will significantly skew the average, leaving a visible smudge instead of removing the noise.
-   **Drawback:** It blurs the entire image, softening edges and fine details, which is often an undesirable side effect.

### The Median Filter (Non-Linear)
-   **Mechanism:** This is a non-linear filter. For each pixel, it considers the intensity values in its neighborhood, sorts them in ascending order, and replaces the central pixel's value with the **median** of that list.
-   **Effectiveness:**
    -   **Excellent for Impulse Noise:** Extreme outliers (salt or pepper pixels) are moved to the beginning or end of the sorted list and are thus ignored by the median calculation. The filter effectively removes the noise without being influenced by the corrupted values.
    -   **Good for Edge Preservation:** Compared to the mean filter, the median filter is much better at preserving sharp edges, as the median is more robust to the variations that define an edge.
-   **Insight:** The choice of filter is highly dependent on the type of noise. The Median filter is specifically designed to combat impulse noise, while the Mean filter is a general-purpose smoother best suited for additive, random noise like Gaussian.

## 3. Evaluating Filter Performance

To objectively measure how well a filter works, we compare the filtered image to the original, noise-free image.
-   **Mean Squared Error (MSE):** Calculates the average squared difference between the pixel values of two images. A lower MSE indicates a better result.
-   **Peak Signal-to-Noise Ratio (PSNR):** A logarithmic metric based on the MSE and the maximum possible pixel value (255).
    -   **Insight:** PSNR is measured in decibels (dB). A **higher PSNR value indicates a better quality** reconstruction, meaning the filtered image is closer to the original, noise-free image. It is the standard way to quantify the performance of noise reduction algorithms. You can learn more in the [[In-Depth/Image Quality Metrics (PSNR, MSE)]] note.