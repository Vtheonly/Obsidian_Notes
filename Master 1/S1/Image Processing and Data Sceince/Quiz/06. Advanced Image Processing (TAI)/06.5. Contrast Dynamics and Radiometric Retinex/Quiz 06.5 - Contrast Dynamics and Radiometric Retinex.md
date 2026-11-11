---
sources:
  - "[[06.5.1. Dynamic Range Expansion and Noise-Tolerant Contrast Stretching]]"
  - "[[06.5.2. Advanced Contrast Models (Histogram Specification and Land's Retinex Theory)]]"
---
> [!question] Linear contrast stretching can correct an image that suffers from both harsh shadows and bright highlights at the same time.
>> [!success]- Answer
>> False

> [!question] Global histogram equalization can over-amplify background noise in near-constant regions because its mapping function is global.
>> [!success]- Answer
>> True

> [!question] In CLAHE, the pixels clipped from bins that exceed the clip limit are redistributed evenly across all histogram bins rather than discarded.
>> [!success]- Answer
>> True

> [!question] In Land's Retinex theory, the illumination component carries the sharp details, edges, and textures of the observed scene.
>> [!success]- Answer
>> False

> [!question] The Retinex framework uses logarithms to turn the multiplicative illumination-reflectance relationship into an additive one.
>> [!success]- Answer
>> True

> [!question] The Thang and Zhuang S-curve increases contrast in mid-tones while stretching shadows and highlights to the extremes of the intensity range.
>> [!success]- Answer
>> False

> [!question] An underexposed image spans the narrow intensity range $[60, 120]$. Using full-range linear contrast stretching to $[0, 255]$, what is the slope of the mapping?
> a) 0.235
> b) 2.0
> c) 4.25
> d) 255.0
>> [!success]- Answer
>> c) 4.25

> [!question] In the CLAHE pipeline, what happens immediately after the total excess $E_{\text{total}}$ is computed from clipped bins?
> a) The excess pixels are discarded and each clipped bin is left at the clip limit
> b) The tile is merged with its four adjacent tiles
> c) The clip limit is automatically raised until no bin exceeds it
> d) The excess is redistributed evenly across all histogram bins before computing the CDF
>> [!success]- Answer
>> d) The excess is redistributed evenly across all histogram bins before computing the CDF

> [!question] Why does CLAHE finish with bilinear interpolation across tile centers?
> a) To remove visible seams between adjacent tiles
> b) To increase the clip limit of each tile
> c) To convert the image into a decoupled color space
> d) To sharpen the edges attenuated by clipping
>> [!success]- Answer
>> a) To remove visible seams between adjacent tiles

> [!question] In histogram specification, which composition expresses the final mapping applied to the input intensities?
> a) $s = T(G(r))$
> b) $z = G^{-1}(T(r))$
> c) $z = T^{-1}(G(s))$
> d) $z = T(r) \cdot G(z)$
>> [!success]- Answer
>> b) $z = G^{-1}(T(r))$

> [!question] In Single-Scale Retinex, how is the illumination component $L(x, y)$ estimated?
> a) By convolving the image with a wide Gaussian low-pass filter
> b) By thresholding the image at its mean intensity
> c) By equalizing the image histogram globally
> d) By taking the pixel-wise maximum of the image and its inverse
>> [!success]- Answer
>> a) By convolving the image with a wide Gaussian low-pass filter

> [!question] How does Multi-Scale Retinex combine the outputs of several Single-Scale Retinex runs?
> a) By selecting the output of the largest scale only
> b) By multiplying the outputs element-wise
> c) By taking a weighted average whose weights sum to 1
> d) By cascading the outputs one after another
>> [!success]- Answer
>> c) By taking a weighted average whose weights sum to 1

> [!question] Match each contrast enhancement method with its primary mechanism.
>> [!example] Group A
>> a) Global histogram equalization
>> b) Linear contrast stretching
>> c) Histogram specification
>> d) CLAHE
>
>> [!example] Group B
>> n) Rescales a narrow observed intensity range onto the full dynamic range with a linear mapping.
>> o) Uses the image CDF as a non-linear transfer function to flatten the histogram.
>> p) Transforms the histogram to match a target reference distribution.
>> q) Equalizes clipped local tile histograms to limit contrast amplification.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)
>> d) -> q)

> [!question] Match each CLAHE pipeline stage with its purpose.
>> [!example] Group A
>> a) Tile division
>> b) Histogram clipping
>> c) Redistribution
>> d) Bilinear interpolation
>
>> [!example] Group B
>> n) Splits the image into small non-overlapping contextual regions such as 8x8 blocks.
>> o) Caps every bin that exceeds the clip limit and collects the surplus.
>> p) Spreads the collected surplus evenly across all bins of the tile histogram.
>> q) Blends the mappings of the four nearest tiles to hide boundaries.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match each Retinex model component with its spatial property.
>> [!example] Group A
>> a) Illumination
>> b) Reflectance
>> c) Observed image
>
>> [!example] Group B
>> n) Modeled as the product of the two other components.
>> o) Varies smoothly across the scene and lives at low spatial frequencies.
>> p) Carries sharp details, edges, and textures at high spatial frequencies.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match each step of the safe CLAHE procedure for color images with its role.
>> [!example] Group A
>> a) Convert to CIE Lab or HSV
>> b) Equalize only the luminance channel
>> c) Merge channels and convert back to RGB
>
>> [!example] Group B
>> n) Restores the enhanced picture in its original color representation.
>> o) Moves brightness into a channel decoupled from chrominance.
>> p) Improves contrast without disturbing the relative ratios between colors.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match each formula with the technique it defines.
>> [!example] Group A
>> a) $Y = \frac{Y_{max} - Y_{min}}{X_{max} - X_{min}} (X - X_{min}) + Y_{min}$
>> b) $s_k = \text{round}((L - 1) \cdot P_c(r_k))$
>> c) $F(x) = 0.5 + \frac{\arctan(\delta (x - m))}{\pi}$
>> d) $R_{SSR}(x, y) = \log I(x, y) - \log(I(x, y) * G_\sigma(x, y))$
>
>> [!example] Group B
>> n) Single-Scale Retinex reflectance estimation.
>> o) Full dynamic range linear stretching.
>> p) Equalized output level computation from the CDF.
>> q) Thang and Zhuang S-curve tone mapping.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> q)
>> d) -> n)

> [!question] Match each Retinex concept with its role.
>> [!example] Group A
>> a) Single-Scale Retinex
>> b) Multi-Scale Retinex
>> c) Color constancy
>> d) Gaussian low-pass filter
>
>> [!example] Group B
>> n) The perceptual ability the theory explains, namely stable object colors under varying illumination.
>> o) Blends several single-scale outputs with weights that sum to 1.
>> p) The smoothing operator used to estimate the illumination component.
>> q) Computes reflectance from one illumination estimate at a single chosen scale.
>
>> [!success]- Answer
>> a) -> q)
>> b) -> o)
>> c) -> n)
>> d) -> p)
