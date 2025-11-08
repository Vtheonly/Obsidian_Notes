
This note explains the purpose and calculation of Mean Squared Error (MSE) and Peak Signal-to-Noise Ratio (PSNR), two common metrics used to objectively measure the quality of a processed or compressed image against an original, pristine reference image.

## Purpose of Quality Metrics

In image processing, filtering operations aim to improve an image (e.g., by removing noise), but they can also introduce artifacts (e.g., blurring). Visual inspection is subjective. Objective metrics provide a quantitative, reproducible way to measure the fidelity of a result and compare the performance of different algorithms.

## Mean Squared Error (MSE)

MSE measures the cumulative squared error between two images. It represents the average of the squares of the differences between the pixel intensity values of the original and processed images.

### Calculation
For two grayscale images, `Im` (original) and `Imf` (filtered), of size `H x W`:

```
          1      H-1  W-1
MSE = ------- *  Σ    Σ   (Im[i,j] - Imf[i,j])²
        H * W    i=0  j=0
```

### Interpretation
-   A lower MSE value indicates a smaller difference between the images, meaning higher fidelity.
-   An MSE of 0 means the images are identical.
-   **Insight:** The squaring of the difference term means that large errors are penalized much more heavily than small errors.

## Peak Signal-to-Noise Ratio (PSNR)

PSNR is a more common metric that builds upon MSE. It measures the ratio between the maximum possible power of a signal (the image) and the power of the corrupting noise that affects its fidelity.

### Calculation
PSNR is defined on a logarithmic scale (decibels, dB):

```
             R²
PSNR = 10 * log10(----)
             MSE
```

Where:
-   `R` is the maximum possible pixel value of the image. For an 8-bit grayscale image, `R = 255`.
-   `MSE` is the Mean Squared Error calculated previously.

### Interpretation
-   A **higher PSNR** value indicates a better quality reconstruction or a more effective filtering result.
-   Because of the logarithmic scale, PSNR aligns better with human perception of quality than MSE does.
-   Typical values for image processing range from 20 dB (poor) to over 40 dB (excellent). An infinite PSNR occurs only if the MSE is 0 (identical images).



