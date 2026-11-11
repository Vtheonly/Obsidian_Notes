---
sources:
  - "[[06.3.1. 2D Discrete Fourier Transform (DFT), FFT Shift, and Convolution Theorem]]"
  - "[[06.3.2. Frequency Filters (Low-Pass, High-Pass, and Band-Reject Notch Filtering)]]"
---
> [!question] Convolving an image $f(x, y)$ with a spatial kernel $h(x, y)$ produces exactly the same result as multiplying $F(u, v)$ by $H(u, v)$ element-wise in the frequency domain.
>> [!success]- Answer
>> True

> [!question] Attenuating the high frequencies of an image with a low-pass filter sharpens edges and enhances fine detail.
>> [!success]- Answer
>> False

> [!question] In a notch reject filter, each factor $H_k(u, v)$ is a low-pass filter centered on the noise frequency $(u_k, v_k)$.
>> [!success]- Answer
>> False

> [!question] The inverse 2D DFT uses the same negative-sign complex exponential as the forward transform and applies no normalization factor.
>> [!success]- Answer
>> False

> [!question] Applying `np.fft.fftshift()` to a computed 2D DFT moves the zero-frequency DC component from the array corner to the visual center of the spectrum.
>> [!success]- Answer
>> True

> [!question] Because the DC coefficient $F(0, 0)$ is orders of magnitude larger than the high-frequency coefficients, spectra are displayed through the logarithmic map $D(u, v) = \log(1 + |F(u, v)|)$ to compress the dynamic range.
>> [!success]- Answer
>> True

> [!question] What does the 2D Discrete Fourier Transform produce when applied to an $M \times N$ image?
> a) A real-valued edge map of gradient magnitudes
> b) A complex-valued spectrum expressing the image as a weighted sum of sinusoidal basis functions
> c) A histogram of the pixel intensity occurrences
> d) A compressed copy of the image at reduced resolution
>> [!success]- Answer
>> b) A complex-valued spectrum expressing the image as a weighted sum of sinusoidal basis functions

> [!question] In a centered 2D Fourier spectrum, what does the coefficient at the visual center represent?
> a) The highest spatial frequency present in the image
> b) The dominant edge orientation of the scene
> c) The variance of the high-frequency noise
> d) The zero-frequency DC term $F(0, 0)$, proportional to the average brightness of the whole image
>> [!success]- Answer
>> d) The zero-frequency DC term $F(0, 0)$, proportional to the average brightness of the whole image

> [!question] What is the main computational motivation for filtering images in the frequency domain?
> a) The FFT computes the transform in $O(N \log N)$ operations, making element-wise spectral multiplication an efficient alternative to direct convolution with large kernels
> b) Frequency-domain filters never introduce blurring around edges
> c) The Fourier transform itself removes sensor noise from the image
> d) Spectra are real-valued and cheaper to store than spatial images
>> [!success]- Answer
>> a) The FFT computes the transform in $O(N \log N)$ operations, making element-wise spectral multiplication an efficient alternative to direct convolution with large kernels

> [!question] Periodic electrical interference appears in the Fourier spectrum as bright symmetric spikes at specific frequencies. Which filter removes it most selectively?
> a) A low-pass filter with a very large cutoff radius
> b) A high-pass filter that discards all frequencies near the center
> c) A band-reject notch filter tuned to the interference frequencies
> d) A spatial averaging filter applied repeatedly until the stripes disappear
>> [!success]- Answer
>> c) A band-reject notch filter tuned to the interference frequencies

> [!question] What is the effect of applying a high-pass frequency filter to an image?
> a) It enhances sharp edges while removing smooth background tones
> b) It smooths noise while blurring edges
> c) It brightens the image by amplifying the DC term
> d) It removes periodic stripes without affecting anything else
>> [!success]- Answer
>> a) It enhances sharp edges while removing smooth background tones

> [!question] What is a Gabor filter?
> a) A low-pass mask that keeps only the components clustered around the spectral center
> b) A high-pass mask that removes the DC term and all smooth background tones
> c) A Gaussian envelope modulated by a sinusoidal plane wave, optimal for joint spatial and frequency localization
> d) A pair of narrow zeros placed over two symmetric noise spikes
>> [!success]- Answer
>> c) A Gaussian envelope modulated by a sinusoidal plane wave, optimal for joint spatial and frequency localization

> [!question] Match each filter with the way it treats the frequency spectrum.
>> [!example] Group A
>> a) Low-pass filter
>> b) High-pass filter
>> c) Band-reject notch filter
>> d) Gabor filter
>
>> [!example] Group B
>> n) Attenuates the components clustered near the spectral center and keeps the ones far from it.
>> o) Responds selectively to one narrow frequency range at a chosen orientation to extract directional textures.
>> p) Keeps the components clustered near the spectral center and attenuates the ones far from it.
>> q) Places narrow attenuation zeros over specific noise coordinates while preserving every other frequency.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)

> [!question] Match each symbol of the 2D DFT formula with its meaning.
>> [!example] Group A
>> a) $f(x, y)$
>> b) $(u, v)$
>> c) $e^{-j2\pi(ux/M + vy/N)}$
>> d) $M \times N$
>
>> [!example] Group B
>> n) The complex exponential weight applied to each pixel for a given frequency pair.
>> o) The intensity of one input pixel of the image being transformed.
>> p) The image dimensions, which set the limits of the double summation.
>> q) The frequency coordinates that index one coefficient of the output spectrum.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match each Fourier spectral concept with what it reveals about the image.
>> [!example] Group A
>> a) Magnitude spectrum
>> b) Phase spectrum
>> c) Low frequencies
>> d) High frequencies
>
>> [!example] Group B
>> n) Where the structural edges and spatial geometry of the scene are located.
>> o) The smooth regions and slow intensity gradients of the picture.
>> p) How strongly each sinusoidal component contributes to the image.
>> q) The sharp transitions, edges, and fine detail of the picture.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)
>> d) -> q)

> [!question] Match each stage of frequency-domain filtering with its operation.
>> [!example] Group A
>> a) Forward 2D FFT
>> b) Transfer function
>> c) Element-wise product
>> d) Inverse 2D FFT
>
>> [!example] Group B
>> n) Multiplies $F(u, v)$ and $H(u, v)$ point by point to yield the filtered spectrum $G(u, v)$.
>> o) Turns the spatial image $f(x, y)$ into its spectrum $F(u, v)$.
>> p) Brings the filtered spectrum $G(u, v)$ back to the spatial domain as $g(x, y)$.
>> q) The spectrum $H(u, v)$ of the spatial mask, obtained by transforming the kernel $h(x, y)$.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match each parameter of the Gabor filter with its role.
>> [!example] Group A
>> a) Orientation $\theta$
>> b) Wavelength $\lambda$
>> c) Phase offset $\psi$
>> d) Gaussian spread $\sigma$
>> e) Aspect ratio $\gamma$
>
>> [!example] Group B
>> n) Sets the spatial size of the receptive field.
>> o) The filter angle, where 0 degrees responds to vertical edges and 90 degrees to horizontal edges.
>> p) Defines the ellipticity of the envelope.
>> q) Controls the symmetry of the wave, where a value of zero gives the symmetric real form.
>> r) Controls the frequency and thickness of the stripes the filter reacts to.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> r)
>> c) -> q)
>> d) -> n)
>> e) -> p)

> [!question] Match each concept from Gabor filtering with its description.
>> [!example] Group A
>> a) Filter bank
>> b) Visual cortex model
>> c) Feature vector
>> d) Biometric applications
>
>> [!example] Group B
>> n) Practical uses such as fingerprint recognition and iris segmentation.
>> o) The biological parallel, since these kernels mirror how the mammalian brain processes directional textures.
>> p) The rich per-pixel descriptor produced by convolving the image with the full set of kernels.
>> q) A collection of kernels spanning orientations such as 0, 45, 90, and 135 degrees together with several wavelengths.
>
>> [!success]- Answer
>> a) -> q)
>> b) -> o)
>> c) -> p)
>> d) -> n)
