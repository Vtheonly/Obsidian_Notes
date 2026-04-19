## 1. Cross-Entropy and Label Smoothing

### Deriving Cross-Entropy from Maximum Likelihood

The model outputs logits $z \in \mathbb{R}^V$ (one scalar per vocabulary token). Convert to probabilities:

$$p_j = \frac{e^{z_j}}{\sum_{k=1}^{V} e^{z_k}} \quad \text{(Softmax)}$$

The probability of the correct target token $y^*$ is $p_{y^*}$.

Maximum Likelihood Estimation (MLE) says: find model parameters $\theta$ that maximize $P(Y \mid X)$. Since the factorization gives us a product of step-wise probabilities, and products of small numbers are numerically unstable, we instead maximize the log-likelihood:

$$\mathcal{L}_{MLE} = \sum_{t=1}^{T} \log P(y_t \mid y_{<t}, X)$$

Minimizing the negative log-likelihood is equivalent to minimizing Cross-Entropy:

$$\mathcal{L}_{CE} = -\sum_{t=1}^{T} \log p_{y_t^*}$$

For a one-hot target distribution $q$ (1 at the correct class, 0 elsewhere), this is equivalent to the standard cross-entropy formula:

$$H(q, p) = -\sum_{j=1}^{V} q_j \log p_j = -\log p_{y^*}$$

---

### Label Smoothing: Regularizing Overconfidence

**The problem with hard one-hot targets:**
Standard cross-entropy sets $q_{y^*} = 1.0$ and $q_j = 0$ for all $j \neq y^*$. The loss gradient drives the model to push $p_{y^*} \to 1$ and $p_j \to 0$ for all others. There is no minimum-loss point before the logit $z_{y^*} \to +\infty$ and all other logits $\to -\infty$.

This leads to:
1. **Overconfident predictions**: The model assigns near-zero probability to any alternative, even reasonable alternatives. For a handwritten `1` that might look like `l`, the model becomes 99.99% sure it is `1`.
2. **Poor calibration**: The model's probability scores no longer reflect true uncertainty. A score of 0.95 does not mean "95% chance of being correct".
3. **Overfitting**: The model memorizes idiosyncrasies of the training data to achieve extreme confidence.

**Label Smoothing fix:**
Redistributes a small $\epsilon$ fraction of probability mass from the correct class to all classes uniformly:

$$q_{smooth}(y^*) = 1 - \epsilon$$
$$q_{smooth}(j \neq y^*) = \frac{\epsilon}{V - 1}$$

With $\epsilon = 0.1$ and $V = 512$:

$$q_{smooth}(y^*) = 0.9$$
$$q_{smooth}(j \neq y^*) = \frac{0.1}{511} \approx 0.000196$$

The loss function now has a finite minimum when $p_{y^*} = 0.9$, not at $p_{y^*} = 1.0$. The model is explicitly trained to be slightly uncertain.

The new smoothed cross-entropy loss:

$$\mathcal{L}_{LS} = -q_{smooth}(y^*) \log p_{y^*} - \sum_{j \neq y^*} \frac{\epsilon}{V-1} \log p_j$$

> **Important reminder:** Label Smoothing also prevents the logit values from exploding. If $z_{y^*} = 1000$ and all others are $-1000$, the Softmax numerically saturates (gradient vanishes). With label smoothing, the model has incentive to keep logit values moderate because assigning all probability to one class is penalized. This is especially important in early training when random initialization produces garbage predictions.

---