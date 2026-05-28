## Exercise 2: Implementing Otsu's Global Thresholding

### Problem Statement
Given a $6 \times 6$ image with three gray levels ($0, 1,$ and $2$), find the optimal binarization threshold $T^*$ using Otsu's method.

The pixel count for each gray level is:
* Intensity **0:** $12$ pixels
* Intensity **1:** $16$ pixels
* Intensity **2:** $8$ pixels

Total number of pixels $N = 6 \times 6 = 36$ pixels.

---

### Step-by-Step Derivation

#### Step 1: Calculate the Class Probabilities $p_i$

$$p_0 = \frac{12}{36} \approx 0.3333$$

$$p_1 = \frac{16}{36} \approx 0.4444$$

$$p_2 = \frac{8}{36} \approx 0.2222$$

#### Step 2: Compute the Global Mean $\mu_G$

$$\mu_G = \sum_{i=0}^{2} i \cdot p_i = (0 \times 0.3333) + (1 \times 0.4444) + (2 \times 0.2222)$$

$$\mu_G = 0 + 0.4444 + 0.4444 = 0.8888$$

---

#### Step 3: Evaluate Candidate Threshold $t = 0$

At $t = 0$, the image is partitioned into two classes:
* $C_1 = \{0\}$
* $C_2 = \{1, 2\}$

##### 1. Class Weights ($\omega_1, \omega_2$)

$$\omega_1(0) = p_0 = 0.3333$$

$$\omega_2(0) = p_1 + p_2 = 0.4444 + 0.2222 = 0.6667$$

##### 2. Class Means ($\mu_1, \mu_2$)

$$\mu_1(0) = \frac{1}{\omega_1(0)} \sum_{i=0}^{0} i \cdot p_i = \frac{0 \times 0.3333}{0.3333} = 0$$

$$\mu_2(0) = \frac{1}{\omega_2(0)} \sum_{i=1}^{2} i \cdot p_i = \frac{(1 \times 0.4444) + (2 \times 0.2222)}{0.6667} = \frac{0.8888}{0.6667} \approx 1.3331$$

##### 3. Inter-Class Variance ($\sigma_B^2(0)$)

$$\sigma_B^2(0) = \omega_1(0) \omega_2(0) \big(\mu_1(0) - \mu_2(0)\big)^2$$

$$\sigma_B^2(0) = (0.3333) \times (0.6667) \times (0 - 1.3331)^2$$

$$\sigma_B^2(0) \approx 0.2222 \times 1.7772 \approx 0.3949$$

---

#### Step 4: Evaluate Candidate Threshold $t = 1$

At $t = 1$, the classes are:
* $C_1 = \{0, 1\}$
* $C_2 = \{2\}$

##### 1. Class Weights ($\omega_1, \omega_2$)

$$\omega_1(1) = p_0 + p_1 = 0.3333 + 0.4444 = 0.7777$$

$$\omega_2(1) = p_2 = 0.2222$$

##### 2. Class Means ($\mu_1, \mu_2$)

$$\mu_1(1) = \frac{1}{\omega_1(1)} \sum_{i=0}^{1} i \cdot p_i = \frac{(0 \times 0.3333) + (1 \times 0.4444)}{0.7777} = \frac{0.4444}{0.7777} \approx 0.5714$$

$$\mu_2(1) = \frac{2 \times 0.2222}{0.2222} = 2.0$$

##### 3. Inter-Class Variance ($\sigma_B^2(1)$)

$$\sigma_B^2(1) = \omega_1(1) \omega_2(1) \big(\mu_1(1) - \mu_2(1)\big)^2$$

$$\sigma_B^2(1) = (0.7777) \times (0.2222) \times (0.5714 - 2.0)^2$$

$$\sigma_B^2(1) = 0.1728 \times (-1.4286)^2 \approx 0.1728 \times 2.0409 \approx 0.3527$$

---

#### Conclusion and Selection
* **Variance for $t = 0$:** $\sigma_B^2(0) = 0.3949$
* **Variance for $t = 1$:** $\sigma_B^2(1) = 0.3527$

Otsu's method selects the threshold that maximizes inter-class variance. Since $\sigma_B^2(0) > \sigma_B^2(1)$, the optimal threshold is:

$$T^* = 0$$

Pixels with intensity values $> 0$ are classified as foreground, and pixels with intensity $0$ are classified as background.
