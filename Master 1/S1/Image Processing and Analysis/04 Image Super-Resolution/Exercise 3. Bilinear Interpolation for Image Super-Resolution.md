## Exercise 3: Bilinear Interpolation for Image Super-Resolution

### Problem Statement
An image is being upsampled by a factor of $2$. Calculate the intensity of the new upsampled pixel at coordinates $P(1.5, 1.5)$ using the intensities of its four nearest neighbors on the original pixel grid:
* $Q_{11}(1, 1) = 120$
* $Q_{21}(2, 1) = 140$
* $Q_{12}(1, 2) = 100$
* $Q_{22}(2, 2) = 180$

---

### Step-by-Step Derivation

We interpolate along the coordinate range $[x_1, x_2] = [1, 2]$ and $[y_1, y_2] = [1, 2]$. Since the grid spacing is $1$:

$$(x_2 - x_1) = 1, \quad (y_2 - y_1) = 1$$

Using the bilinear interpolation formula:

$$\begin{aligned}
f(x, y) = & f(Q_{11})(x_2 - x)(y_2 - y) + f(Q_{21})(x - x_1)(y_2 - y) \\
+ & f(Q_{12})(x_2 - x)(y - y_1) + f(Q_{22})(x - x_1)(y - y_1)
\end{aligned}$$

Substitute the coordinate values $x = 1.5$ and $y = 1.5$:
* $(x_2 - x) = (2 - 1.5) = 0.5$
* $(x - x_1) = (1.5 - 1) = 0.5$
* $(y_2 - y) = (2 - 1.5) = 0.5$
* $(y - y_1) = (1.5 - 1) = 0.5$

Substitute these weights into the interpolation equation:

$$\begin{aligned}
f(1.5, 1.5) = & 120 \times (0.5 \times 0.5) + 140 \times (0.5 \times 0.5) \\
+ & 100 \times (0.5 \times 0.5) + 180 \times (0.5 \times 0.5)
\end{aligned}$$

Factor out the common weight $(0.5 \times 0.5) = 0.25$:

$$f(1.5, 1.5) = 0.25 \times (120 + 140 + 100 + 180)$$

$$f(1.5, 1.5) = 0.25 \times 540 = 135$$

The interpolated intensity value at coordinate $P(1.5, 1.5)$ is **135**.
