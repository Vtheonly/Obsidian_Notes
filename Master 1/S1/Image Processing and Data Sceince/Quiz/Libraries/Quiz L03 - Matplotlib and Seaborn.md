---
sources:
  - "[[03. Matplotlib Core Architecture - Figure, Axes, and Canvas Visualization Mechanics]]"
  - "[[10. Matplotlib and Seaborn Statistical Plotting for Tabular Data]]"
---
> [!question] In Matplotlib's rendering architecture, the Axes object is the top-level window that manages figure dimensions, DPI, and subplots.
>> [!success]- Answer
>> False

> [!question] The pyplot functional interface draws on the most recently active Axes using implicit global state.
>> [!success]- Answer
>> True

> [!question] When `vmin` and `vmax` are left as `None` in `imshow`, Matplotlib anchors the display to the fixed 0 to 255 range.
>> [!success]- Answer
>> False

> [!question] A violin plot combines a box plot with a rotated kernel density curve.
>> [!success]- Answer
>> True

> [!question] `plt.tight_layout()` enlarges the figure window until every subplot fits.
>> [!success]- Answer
>> False

> [!question] Seaborn is built on top of Matplotlib and integrates directly with Pandas DataFrames, handling aggregations automatically.
>> [!success]- Answer
>> True

> [!question] Which Matplotlib object contains an individual coordinate system and exposes plotting methods such as `plot`, `scatter`, and `hist`?
> a) Figure
> b) Axis
> c) Axes
> d) Artist
>> [!success]- Answer
>> c) Axes

> [!question] Why should `imshow` be called with `vmin=0, vmax=255` when rendering 8-bit images?
> a) To speed up rendering of large matrices
> b) To prevent automatic scaling from exaggerating background noise in dark images
> c) To convert the image to grayscale automatically
> d) To center the color map at the mid-gray level
>> [!success]- Answer
>> b) To prevent automatic scaling from exaggerating background noise in dark images

> [!question] Which `imshow` array shape is interpreted as RGB plus an alpha channel?
> a) $(M, N)$
> b) $(N, M, 2)$
> c) $(M, N, 3)$
> d) $(M, N, 4)$
>> [!success]- Answer
>> d) $(M, N, 4)$

> [!question] For an 8-bit tonal histogram, which `Axes.hist` settings give each gray level its own bar?
> a) `bins=20, range=(0, 1)`
> b) `bins=256, range=(0, 256)`
> c) `bins=128, range=(0, 128)`
> d) `bins=10, range=None`
>> [!success]- Answer
>> b) `bins=256, range=(0, 256)`

> [!question] What does `density=True` do in `Axes.hist`?
> a) Normalizes bar heights so the total area equals 1, yielding an empirical probability density function
> b) Replaces the bars with the cumulative distribution curve
> c) Smooths the bars into a kernel density estimate line
> d) Scales each bar height by the number of bins
>> [!success]- Answer
>> a) Normalizes bar heights so the total area equals 1, yielding an empirical probability density function

> [!question] Which pattern renders a 3D intensity topography of a surface $Z$?
> a) `ax.imshow(Z, cmap='viridis')`
> b) `sns.heatmap(Z, annot=True)`
> c) `fig.add_subplot(111, projection='3d')` followed by `plot_surface`
> d) `sns.histplot(Z, kde=True)`
>> [!success]- Answer
>> c) `fig.add_subplot(111, projection='3d')` followed by `plot_surface`

> [!question] Match each Matplotlib architecture object with its role.
>> [!example] Group A
>> a) Figure
>> b) Axes
>> c) Axis
>> d) Artists
>
>> [!example] Group B
>> n) The top-level window or canvas that manages figure dimensions, DPI, and subplots.
>> o) An individual coordinate area that exposes plotting methods such as `plot`, `scatter`, and `hist`.
>> p) Handles scale limits, tick marks, and tick labels.
>> q) The rendered primitives of a plot, such as lines, markers, and legend boxes.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match each Matplotlib interface or layout call with its behavior.
>> [!example] Group A
>> a) Pyplot functional interface
>> b) Object-oriented interface
>> c) `plt.subplots(nrows, ncols)`
>> d) `plt.tight_layout()`
>
>> [!example] Group B
>> n) Adjusts subplot spacing automatically to prevent overlapping labels.
>> o) Relies on implicit global state and styles the most recently active Axes.
>> p) Explicitly instantiates Figure and Axes objects for finer control in production code.
>> q) Creates a grid of plots and returns the Axes objects as an array.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> q)
>> d) -> n)

> [!question] Match each color map choice with its rendering behavior.
>> [!example] Group A
>> a) 'gray'
>> b) 'viridis'
>> c) 'jet' and 'hsv'
>
>> [!example] Group B
>> n) Perceptually uniform modern default colormap.
>> o) Linear grayscale mapping where 0 renders black and 255 renders white.
>> p) High-contrast rainbow spectra that can introduce visual artifacts.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match each statistical plot type with what it displays.
>> [!example] Group A
>> a) Histogram
>> b) Box plot
>> c) Violin plot
>> d) Correlation heatmap
>
>> [!example] Group B
>> n) Visualizes relationships across a matrix using an annotated color scale.
>> o) Shows quartiles and highlights outliers beyond $1.5 \times \text{IQR}$.
>> p) Displays the distribution of a continuous feature grouped into bins.
>> q) Combines a box plot with a rotated kernel density curve to reveal where data concentrates.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> q)
>> d) -> n)

> [!question] Match each rendering or histogram parameter with its meaning.
>> [!example] Group A
>> a) `cmap`
>> b) `vmin` and `vmax`
>> c) `bins`
>> d) `density`
>
>> [!example] Group B
>> n) Normalizes histogram heights so the total area equals 1.
>> o) Selects the palette used to render a 2D scalar matrix.
>> p) Sets the number or explicit edges of the histogram bars.
>> q) Anchors the display scaling bounds of a rendered matrix.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> p)
>> d) -> n)

> [!question] Match each Seaborn or Matplotlib call with its purpose.
>> [!example] Group A
>> a) `sns.load_dataset`
>> b) `sns.set_theme`
>> c) `sns.histplot` with `kde=True`
>> d) `ax.axis('off')`
>
>> [!example] Group B
>> n) Fetches a standard practice dataset as a DataFrame.
>> o) Overlays an estimated probability density curve on the binned counts.
>> p) Suppresses axis ticks and labels on a panel.
>> q) Applies a global visual style such as whitegrid to all plots.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> q)
>> c) -> o)
>> d) -> p)
