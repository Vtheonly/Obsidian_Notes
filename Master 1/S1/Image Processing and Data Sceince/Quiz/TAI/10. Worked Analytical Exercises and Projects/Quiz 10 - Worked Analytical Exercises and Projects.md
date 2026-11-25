---
sources:
  - "[[10.1. Exercise 1 - Complete Calculation of 2D Convolution and Boundary Padding Modes]]"
  - "[[10.2. Exercise 2 - Exhaustive Step-by-Step Optimization of Otsu's Inter-Class Variance]]"
  - "[[10.3. Exercise 3 - Analytical Sub-Pixel Reconstruction via Bilinear Interpolation]]"
  - "[[10.4. Project - End-to-End Historical Document Restoration and Extraction Pipeline]]"
---
> [!question] Because the $3 \times 3$ high-pass kernel is symmetric along both the horizontal and vertical axes ($h(i, j) = h(-i, -j)$), 2D convolution and 2D cross-correlation yield identical numerical expressions for this kernel.
>> [!success]- Answer
>> True

> [!question] Zero padding preserves the local intensity continuity at the image border, so the high-pass filter response at the corner pixel stays close to zero.
>> [!success]- Answer
>> False

> [!question] Because the kernel weights sum to zero ($-1 \times 8 + 8 = 0$), the high-pass filter outputs exactly 0 in completely flat, uniform areas.
>> [!success]- Answer
>> True

> [!question] Otsu's between-class variance is computed as $\omega_1(t) \cdot \omega_2(t) \cdot (\mu_1(t) + \mu_2(t))^2$, using the sum of the two class means.
>> [!success]- Answer
>> False

> [!question] At every candidate threshold, the class weights and class means satisfy $\omega_1 + \omega_2 = 1$ and $\omega_1\mu_1 + \omega_2\mu_2 = \mu_T$.
>> [!success]- Answer
>> True

> [!question] In the sequential three-step solution of the bilinear reconstruction of $P(1.5, 1.5)$, the vertical interpolation along the column at $x = 1.5$ is carried out before the two horizontal row interpolations.
>> [!success]- Answer
>> False

> [!question] In the direct 2D formulation, the reconstructed intensity is a linear convex combination of the four neighboring intensities, with weights given by normalized quadrant areas.
>> [!success]- Answer
>> True

> [!question] In the Sauvola binarization stage, pixels brighter than the local threshold surface are set to 255 as foreground text.
>> [!success]- Answer
>> False

> [!question] A $3 \times 3$ high-pass kernel with center weight 8 and $-1$ everywhere else is centered on the corner pixel $f(0, 0) = 100$; the only in-bounds neighbors are 130, 110, and 90, and every out-of-bounds position is filled with 0. What is the raw filter output?
> a) $-40$
> b) $470$
> c) $800$
> d) $330$
>> [!success]- Answer
>> b) $470$

> [!question] Which value does mirror (reflection) padding substitute for the out-of-bounds coordinate $f(0, -1)$ when a $3 \times 3$ kernel is centered on the corner pixel $f(0, 0)$?
> a) $0$, since every out-of-bounds position is assigned zero
> b) $f(0, 0) = 100$, since the border pixel is repeated outward
> c) $f(0, 1) = 130$, since the border pixel is reflected across the boundary
> d) $f(0, 4) = 110$, since the index wraps around to the opposite edge
>> [!success]- Answer
>> c) $f(0, 1) = 130$, since the border pixel is reflected across the boundary

> [!question] A $6 \times 6$ image contains intensity levels 0, 1, and 2 with pixel counts $n_0 = 12$, $n_1 = 16$, and $n_2 = 8$. What global mean $\mu_T$ does the Otsu derivation compute?
> a) $\frac{8}{9}$
> b) $1.0$
> c) $\frac{4}{9}$
> d) $\frac{4}{3}$
>> [!success]- Answer
>> a) $\frac{8}{9}$

> [!question] For the candidate threshold $t = 0$, the foreground class contains the 16 pixels of level 1 and the 8 pixels of level 2. What is the foreground class mean $\mu_2(0)$?
> a) $2.0$
> b) $\frac{4}{7}$
> c) $\frac{8}{9}$
> d) $\frac{4}{3}$
>> [!success]- Answer
>> d) $\frac{4}{3}$

> [!question] Otsu's exhaustive sweep over the three-level histogram gives $\sigma_B^2(0) \approx 0.39506$ and $\sigma_B^2(1) \approx 0.35273$. Which candidate is selected as the optimal threshold $T^*$?
> a) $t = 0$, because it yields the larger between-class variance
> b) $t = 1$, because it yields the larger between-class variance
> c) $t = 1$, because it yields the smaller between-class variance
> d) Neither candidate, because Otsu's method requires both classes to hold equal pixel counts
>> [!success]- Answer
>> a) $t = 0$, because it yields the larger between-class variance

> [!question] The four neighbors surrounding the sub-pixel point $P(1.5, 1.5)$ have intensities 120, 140, 100, and 180, and $P$ sits exactly at the center of the unit cell. What intensity does direct 2D bilinear interpolation reconstruct at $P$?
> a) $130$
> b) $135.0$
> c) $140$
> d) $540$
>> [!success]- Answer
>> b) $135.0$

> [!question] Which formula defines the pixel-wise threshold surface of the Sauvola binarization stage, with $m(x, y)$ the local mean, $s(x, y)$ the local standard deviation, and $R$ the dynamic range?
> a) $T(x, y) = m(x, y) + k \cdot s(x, y)$
> b) $T(x, y) = R \cdot [1 + k \cdot (m(x, y) / s(x, y) - 1)]$
> c) $T(x, y) = m(x, y) \cdot [1 + k \cdot (s(x, y) / R - 1)]$
> d) $T(x, y) = m(x, y) \cdot k \cdot s(x, y) / R$
>> [!success]- Answer
>> c) $T(x, y) = m(x, y) \cdot [1 + k \cdot (s(x, y) / R - 1)]$

> [!question] In what order does the document restoration pipeline apply its processing stages?
> a) Grayscale ingestion, Retinex illumination flattening, bilateral edge-preserving smoothing, Sauvola binarization, morphological refinement, connected-component extraction
> b) Grayscale ingestion, Sauvola binarization, Retinex illumination flattening, bilateral edge-preserving smoothing, morphological refinement, connected-component extraction
> c) Grayscale ingestion, bilateral edge-preserving smoothing, Sauvola binarization, Retinex illumination flattening, morphological refinement, connected-component extraction
> d) Grayscale ingestion, Retinex illumination flattening, Sauvola binarization, bilateral edge-preserving smoothing, morphological refinement, connected-component extraction
>> [!success]- Answer
>> a) Grayscale ingestion, Retinex illumination flattening, bilateral edge-preserving smoothing, Sauvola binarization, morphological refinement, connected-component extraction

> [!question] Match each quantity from the $3 \times 3$ high-pass filtering of the corner pixel $f(0, 0) = 100$ with its value.
>> [!example] Group A
>> a) The center term $100 \times 8$ of the kernel sum
>> b) The total of the eight negative neighbor products under mirror padding
>> c) The raw mirror-padded output before clamping
>> d) The 8-bit stored value of the zero-padded corner response
>> e) The 8-bit stored value of the mirror-padded corner response
>
>> [!example] Group B
>> n) The value $-40$.
>> o) The value $800$.
>> p) The value $0$.
>> q) The value $-840$.
>> r) The value $255$.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> r)
>> e) -> p)

> [!question] In the Otsu example with level counts $n_0 = 12$, $n_1 = 16$, and $n_2 = 8$ over 36 pixels, match each statistic at the candidate threshold $t = 1$ with its computed value.
>> [!example] Group A
>> a) Background class weight $\omega_1(1)$
>> b) Foreground class weight $\omega_2(1)$
>> c) Background class mean $\mu_1(1)$
>> d) Foreground class mean $\mu_2(1)$
>
>> [!example] Group B
>> n) The number $\frac{4}{7}$.
>> o) The number $2.0$.
>> p) The number $\frac{7}{9}$.
>> q) The number $\frac{2}{9}$.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] Match each Otsu class at each candidate threshold with the set of intensity levels it contains.
>> [!example] Group A
>> a) Background $C_1$ at $t = 0$
>> b) Foreground $C_2$ at $t = 0$
>> c) Background $C_1$ at $t = 1$
>> d) Foreground $C_2$ at $t = 1$
>
>> [!example] Group B
>> n) The level set $\{2\}$.
>> o) The level set $\{0, 1\}$.
>> p) The level set $\{1, 2\}$.
>> q) The level set $\{0\}$.
>
>> [!success]- Answer
>> a) -> q)
>> b) -> p)
>> c) -> o)
>> d) -> n)

> [!question] Match each step of the bilinear reconstruction of $P(1.5, 1.5)$ with the values it blends.
>> [!example] Group A
>> a) Horizontal interpolation along row $y = 1$
>> b) Horizontal interpolation along row $y = 2$
>> c) Vertical interpolation along the column at $x = 1.5$
>> d) The direct 2D formulation
>
>> [!example] Group B
>> n) Blends 120 and 140, each with weight 0.5, producing 130.
>> o) Blends 100 and 180, each with weight 0.5, producing 140.
>> p) Multiplies all four corner intensities by 0.25 and sums them in a single pass.
>> q) Blends the two intermediate row results, each with weight 0.5.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> q)
>> d) -> p)

> [!question] Match each interpolation weight expression with the term it multiplies.
>> [!example] Group A
>> a) $\frac{x_2 - x}{x_2 - x_1}$
>> b) $\frac{x - x_1}{x_2 - x_1}$
>> c) $(x_2 - x)(y_2 - y)$
>> d) $(x - x_1)(y - y_1)$
>
>> [!example] Group B
>> n) Weight of the right endpoint in a 1D interpolation along a row.
>> o) Area factor multiplying $f(Q_{22})$ in the direct 2D sum.
>> p) Weight of the left endpoint in a 1D interpolation along a row.
>> q) Area factor multiplying $f(Q_{11})$ in the direct 2D sum.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)

> [!question] Match each stage of the document restoration pipeline with its purpose.
>> [!example] Group A
>> a) Stage 1, ingestion
>> b) Stage 2, restoration
>> c) Stage 3, adaptive binarization
>> d) Stage 4, morphological refinement
>> e) Stage 5, region extraction
>
>> [!example] Group B
>> n) Local window Sauvola thresholding with dynamic range constraints, segmenting strokes under varying contrast.
>> o) Reading the scan with OpenCV and converting BGR to grayscale luminance.
>> p) Connected component labeling, bounding-box filtering, and automated character counting.
>> q) Bilateral edge-preserving smoothing combined with Single-Scale Retinex background flattening.
>> r) Opening for noise removal followed by closing for stroke consolidation.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> r)
>> e) -> p)

> [!question] Match each implementation detail of the document restoration pipeline with its role.
>> [!example] Group A
>> a) The wide Gaussian blur inside the Retinex step
>> b) The `+1.0` offset added to the float image
>> c) The `cv2.normalize` call applied to the log reflectance
>> d) The `BORDER_REFLECT` argument of the box filters
>> e) Skipping label 0 in the component loop
>
>> [!example] Group B
>> n) Prevents taking the logarithm of zero.
>> o) Leaves the page background out of the character tally.
>> p) Estimates the smoothly varying illumination field.
>> q) Rescales values to the standard 8-bit range from 0 to 255.
>> r) Provides substitute values when the local window overhangs the image edges.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> r)
>> e) -> o)

> [!question] Match each element of the binarization and refinement stages with its computational role.
>> [!example] Group A
>> a) Morphological opening with the $2 \times 2$ kernel
>> b) Morphological closing with the $2 \times 1$ kernel
>> c) The local mean $m(x, y)$ of the Sauvola formula
>> d) The local standard deviation $s(x, y)$ of the Sauvola formula
>> e) The character acceptance criterion
>
>> [!example] Group B
>> n) Bridges small gaps in broken text strokes.
>> o) Removes isolated salt-noise specks from the binary mask.
>> p) Square root of $E[X^2] - (E[X])^2$ computed over each local window.
>> q) Averaging box filter over a $25 \times 25$ neighborhood.
>> r) Keeps only regions with pixel area between 20 and 5000 and height above 8.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> q)
>> d) -> p)
>> e) -> r)
