---
sources:
  - "[[06.1.1. Physical Image Formation, Radiometry, and Optical Sensing]]"
  - "[[06.1.2. Spatial Discretization, Dirac Comb Sampling, and Nyquist-Shannon Theorem]]"
  - "[[06.1.3. Amplitude Quantization, Dynamic Range, and Bit Depth]]"
  - "[[06.1.4. Image Representations - Raster Matrix vs Mathematical Vector Primitives]]"
  - "[[06.1.5. Color Models - Additive RGB, Subtractive CMYK, and Photometric Grayscale]]"
  - "[[06.1.6. Perceptual and Broadcast Spaces - YUV, YCbCr, HSV, and CIE Lab]]"
  - "[[06.1.7. Digital File Encapsulation, Compression Standards, and Medical DICOM]]"
  - "[[06.1.8. Discrete Spatial Topology, Neighborhoods (N4, N8), and Metric Spaces]]"
  - "[[06.1.9. Tonal Histograms, Probability Densities, and Cumulative Distribution Functions]]"
  - "[[06.1.10. Mathematical 2D Spatial Convolution, Cross-Correlation, and Boundary Padding]]"
  - "[[06.1.11. The Classical Vision Processing Hierarchy - Low, Mid, and High-Level Tasks]]"
---
> [!question] According to the Nyquist-Shannon sampling theorem, a continuous image can be reconstructed without distortion when the sampling frequency is exactly equal to twice the highest spatial frequency present in the scene.
>> [!success]- Answer
>> False

> [!question] In the illumination-reflectance decomposition of image formation, the illumination component behaves as a low-frequency signal varying smoothly across the scene, while the reflectance component behaves as a high-frequency signal changing abruptly at material boundaries.
>> [!success]- Answer
>> True

> [!question] False contouring is an aliasing artifact caused by sampling the scene below the Nyquist rate rather than an effect of amplitude quantization.
>> [!success]- Answer
>> False

> [!question] Upscaling a vector graphic produces blurry pixelation because vector files store a fixed grid of sampled pixels.
>> [!success]- Answer
>> False

> [!question] Vector representation offers compact storage for typography and line art but cannot efficiently model complex photographic scenes with millions of subtle color variations.
>> [!success]- Answer
>> True

> [!question] For any two pixels on a discrete grid, the Chebyshev distance never exceeds the Euclidean distance, and the Euclidean distance never exceeds the Manhattan distance.
>> [!success]- Answer
>> True

> [!question] Most modern deep learning frameworks and computer vision libraries implement cross-correlation internally while labeling the operation as convolution.
>> [!success]- Answer
>> True

> [!question] The cumulative distribution function of image intensities is a non-decreasing step function that reaches the value 1.0 at the maximum gray level.
>> [!success]- Answer
>> True

> [!question] PNG is the preferred file format for natural photographs because its DEFLATE compression produces the smallest files for continuous-tone scenes.
>> [!success]- Answer
>> False

> [!question] In the classical vision processing hierarchy, mid-level processing maps raw pixel matrices directly into semantic scene classifications and automated decisions.
>> [!success]- Answer
>> False

> [!question] Which discretization operation maps continuous spatial coordinates to discrete integer grid coordinates?
> a) Amplitude quantization
> b) Spatial sampling
> c) Histogram equalization
> d) Color demosaicing
>> [!success]- Answer
>> b) Spatial sampling

> [!question] A medical imaging sensor quantizes each pixel with a depth of 16 bits per pixel. How many discrete intensity states can a single pixel represent?
> a) 256
> b) 4,096
> c) 16,384
> d) 65,536
>> [!success]- Answer
>> d) 65,536

> [!question] Which formula gives the photometrically weighted ITU-R BT.601 conversion from RGB to grayscale luminance?
> a) $Y = \frac{R + G + B}{3}$
> b) $Y = 0.299 \cdot R + 0.587 \cdot G + 0.114 \cdot B$
> c) $Y = 0.114 \cdot R + 0.587 \cdot G + 0.299 \cdot B$
> d) $Y = \max(R, G, B)$
>> [!success]- Answer
>> b) $Y = 0.299 \cdot R + 0.587 \cdot G + 0.114 \cdot B$

> [!question] Which color space is perceptually uniform, so that the Euclidean distance between two color points corresponds to their perceived color difference?
> a) YCbCr
> b) HSV
> c) CIE $L^*a^*b^*$
> d) CMYK
>> [!success]- Answer
>> c) CIE $L^*a^*b^*$

> [!question] Why can the chrominance channels be downsampled in YCbCr compression, as in 4:2:0 chroma subsampling, without noticeable loss of visual quality?
> a) The human visual system is far more sensitive to spatial variations in brightness than in color.
> b) The Cb and Cr channels contain only zero values for natural images.
> c) The luminance channel holds all image structure, so chrominance detail is mathematically redundant.
> d) Subsampling is restricted to regions where the image is already flat and untextured.
>> [!success]- Answer
>> a) The human visual system is far more sensitive to spatial variations in brightness than in color.

> [!question] Which distance metric is also known as the chessboard distance because it matches the movement of a king?
> a) Manhattan distance ($d_1$)
> b) Euclidean distance ($d_2$)
> c) Chebyshev distance ($d_\infty$)
> d) Mahalanobis distance
>> [!success]- Answer
>> c) Chebyshev distance ($d_\infty$)

> [!question] What is the essential mathematical difference between 2D discrete convolution and 2D cross-correlation?
> a) Cross-correlation normalizes its output by the kernel energy, while convolution does not.
> b) Convolution operates over a larger spatial support than cross-correlation.
> c) Convolution requires periodic boundary padding, while cross-correlation requires zero padding.
> d) Convolution flips the kernel by 180 degrees before the sum of products, while cross-correlation uses the kernel as is.
>> [!success]- Answer
>> d) Convolution flips the kernel by 180 degrees before the sum of products, while cross-correlation uses the kernel as is.

> [!question] A separable $15 \times 15$ kernel is applied as two consecutive 1D passes instead of one direct 2D pass. How many multiplications per pixel does the separated implementation require?
> a) 15
> b) 30
> c) 60
> d) 225
>> [!success]- Answer
>> b) 30

> [!question] A binary image analysis defines the foreground objects with 8-connectivity. Which connectivity definition must be applied to the background to avoid the connectivity paradox?
> a) 4-connectivity
> b) 8-connectivity
> c) Diagonal connectivity
> d) Any definition, since foreground and background connectivity do not interact
>> [!success]- Answer
>> a) 4-connectivity

> [!question] In a CT scan stored as a DICOM file, what do the rescale slope and intercept attributes accomplish?
> a) They compress the pixel data stream using quantization tables.
> b) They anonymize the patient identity and clinical history.
> c) They record the radiation dose and slice thickness of the acquisition.
> d) They convert raw integer pixel values into calibrated Hounsfield Units.
>> [!success]- Answer
>> d) They convert raw integer pixel values into calibrated Hounsfield Units.

> [!question] Match each discrete spatial concept with the geometric shape or pixel set it defines.
>> [!example] Group A
>> a) Manhattan distance
>> b) Euclidean distance
>> c) Chebyshev distance
>> d) 4-neighborhood
>> e) 8-neighborhood
>
>> [!example] Group B
>> n) All pixels within a given radius form a diamond.
>> o) All pixels within a given radius form a circle.
>> p) All pixels within a given radius form a square.
>> q) The pixels adjacent to a central pixel through a shared horizontal or vertical edge.
>> r) The pixels adjacent to a central pixel through a shared edge or a shared corner.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
>> e) -> r)

> [!question] Match the image file format with its compression behavior and typical use.
>> [!example] Group A
>> a) PNG
>> b) JPEG
>> c) DICOM
>> d) RAW
>
>> [!example] Group B
>> n) Lossy compression via the Discrete Cosine Transform that can introduce visible $8 \times 8$ blocking artifacts at high compression ratios.
>> o) Lossless compression using DEFLATE, with support for 16-bit channels and alpha transparency.
>> p) A clinical record that bundles pixel data with embedded patient and acquisition metadata.
>> q) Unprocessed direct sensor data captured before demosaicing, with no compression applied.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)
>> d) -> q)

> [!question] Match the boundary padding strategy with its behavior for out-of-bounds pixels.
>> [!example] Group A
>> a) Zero padding
>> b) Replication padding
>> c) Mirror padding
>> d) Periodic padding
>
>> [!example] Group B
>> n) Clamps out-of-bounds coordinates to the nearest edge pixel, preserving border intensity levels.
>> o) Wraps coordinates around to the opposite edge, as required for convolution via the Discrete Fourier Transform.
>> p) Treats out-of-bounds locations as a fixed dark value, which can create an artificial border that distorts edge detectors.
>> q) Reflects pixel values back into the image across the boundary, maintaining local intensity gradients.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)

> [!question] Match each level of the classical vision processing hierarchy with its input-to-output transformation.
>> [!example] Group A
>> a) Low-level processing
>> b) Mid-level processing
>> c) High-level processing
>
>> [!example] Group B
>> n) Consumes raw pixel matrices and outputs processed pixel matrices through operations such as noise removal and contrast enhancement.
>> o) Consumes structural features and geometric attributes to produce semantic interpretations and automated decisions.
>> p) Consumes processed pixel matrices to produce symbolic descriptors such as segmented regions and bounding boxes.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the color space with the property for which it was designed.
>> [!example] Group A
>> a) YUV
>> b) YCbCr
>> c) HSV
>> d) CIE $L^*a^*b^*$
>
>> [!example] Group B
>> n) A cylindrical model whose hue channel can be thresholded while ignoring brightness fluctuations caused by shadows.
>> o) A space with a green-to-red axis and a blue-to-yellow axis supplementing a lightness dimension.
>> p) The European broadcast luminance-chrominance encoding used in MPEG video compression.
>> q) The digital luminance-chrominance encoding used in the JPEG image compression standard.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] Match the histogram shape with the tonal condition it reveals about the image.
>> [!example] Group A
>> a) Underexposed image
>> b) Overexposed image
>> c) Low-contrast image
>> d) Bimodal histogram
>
>> [!example] Group B
>> n) The counts are compressed into a narrow band in the middle of the intensity range, leaving the scene flat and washed out.
>> o) The counts cluster heavily near intensity 0 at the far left of the range.
>> p) Two distinct peaks separated by a deep valley, indicating suitability for segmentation by global thresholding.
>> q) The counts cluster heavily near intensity 255 at the far right of the range.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match the component of physical image formation with its property.
>> [!example] Group A
>> a) Illumination component $i(x, y)$
>> b) Reflectance component $r(x, y)$
>> c) Collected charge $Q$
>> d) Anti-aliasing filter
>
>> [!example] Group B
>> n) The fraction of incident light that physical surfaces return into the optical aperture, bounded between 0 and 1.
>> o) The amount of incident light energy reaching the scene from environmental sources, ranging from just above 0 to infinity.
>> p) An optical low-pass element placed in front of the sensor to remove frequencies above the Nyquist limit before sampling.
>> q) Built up at a photo-site by absorbing photon flux over the exposure duration and the sensor area.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> q)
>> d) -> p)

> [!question] Match the spatial sampling concept with its definition.
>> [!example] Group A
>> a) Dirac comb function
>> b) Nyquist rate
>> c) Moiré patterns
>> d) Jagged contours
>
>> [!example] Group B
>> n) The critical threshold equal to twice the highest spatial frequency present in the scene.
>> o) An ideal two-dimensional impulse train multiplied with the continuous image to model sampling.
>> p) False ripple textures that appear when fine repetitive structures such as fabric weaves are sampled.
>> q) Stair-stepped diagonal boundaries that replace smooth edges when the sampling rate is too low.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)
>> d) -> q)

> [!question] Match the quantization bit depth with its typical application.
>> [!example] Group A
>> a) 1-bit
>> b) 8-bit
>> c) 12 to 14-bit
>> d) 16-bit
>
>> [!example] Group B
>> n) The display standard in which value 0 is absolute black and value 255 is peak white.
>> o) Two-state binary masks, document binarization, and structural silhouettes.
>> p) DICOM radiography, CT, and MRI recordings of subtle tissue density differences.
>> q) Professional camera capture that preserves highlight and shadow detail before tone-mapping.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> q)
>> d) -> p)

> [!question] Match the color model with its defining property.
>> [!example] Group A
>> a) Additive RGB model
>> b) Subtractive CMYK model
>> c) Key component
>> d) Photometric grayscale conversion
>
>> [!example] Group B
>> n) A weighted combination of the red, green, and blue values that mirrors the retina's greater sensitivity to green light.
>> o) A pigment system whose inks absorb selected wavelengths, with cyan, magenta, and yellow as complements of the display primaries.
>> p) A fourth pigment computed as the minimum of the cyan, magenta, and yellow amounts, used to save inks and deepen dark tones.
>> q) A cubic domain whose origin is total absence of light and whose opposite corner is all primaries at full intensity.
>
>> [!success]- Answer
>> a) -> q)
>> b) -> o)
>> c) -> p)
>> d) -> n)
