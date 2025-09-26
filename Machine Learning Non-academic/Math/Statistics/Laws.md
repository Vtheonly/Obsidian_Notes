# Summary of Key Laws, Distributions, and Formulas in Probability

This summary organizes essential laws, distributions, and formulas discussed, categorized for clarity. Each concept includes practical context on when and where to use it, along with concrete examples to illustrate application.

---

## **I. General Laws and Concepts Related to Random Variables**

### **1. Random Variable**

* A random variable \(X\) on a sample space \(S\) maps each outcome in \(S\) to a real number.
* Condition: The inverse image of any real interval must be an event in \(S\).

**Context and Usage:**
- **Discrete Random Variables:** Used for countable outcomes (e.g., number of heads in coin flips, dice rolls, number of customers arriving)
- **Continuous Random Variables:** Used for measurements that can take any value in an interval (e.g., height, weight, time, temperature)

**Example:**
- **Dice Roll:** Let \(X\) be the number shown on a fair six-sided die. Sample space \(S = \{1,2,3,4,5,6\}\), \(X(s) = s\) for each outcome $s$.
- **Height Measurement:** Let $Y$ be the height of a randomly selected person. $Y$ can take any value between, say, 140cm and 220cm.

### **2. Probability Distribution**

* **Discrete Random Variable:** For values $x_1, x_2, \ldots, x_n$, the probability distribution $f$ is defined as:

  $
  f(x_i) = P(X = x_i)
  $
* **Conditions for Validity:**

  $
  f(x_i) \geq 0 \quad \forall i,
  \qquad \sum_i f(x_i) = 1
  $

**Context and Usage:**
- **Probability Mass Function (PMF):** Used for discrete random variables to show the probability of each possible outcome
- **Probability Density Function (PDF):** Used for continuous random variables to show the relative likelihood of values in a continuous range
- **Purpose:** Provides the foundation for calculating probabilities, expected values, and other statistical measures

**Example:**
- **PMF Example:** For a fair six-sided die, $f(x) = 1/6$ for $x = 1,2,3,4,5,6$
- **PDF Example:** For a continuous uniform distribution between 0 and 1, $f(x) = 1$ for $0 \leq x \leq 1$

### **3. Expected Value (Mean)**

* **Discrete Case:**

  $
  \mathbb{E}[X] = \mu = \sum_i x_i f(x_i)
  $
* **Continuous Case:**

  $
  \mathbb{E}[X] = \int_{-\infty}^{\infty} x f(x)\, dx
  $

**Context and Usage:**
- **Long-term Average:** Represents the average value you expect to observe over many trials
- **Decision Making:** Used in economics, finance, and gambling to evaluate expected returns
- **Quality Control:** Used to predict average measurements in manufacturing processes
- **Insurance:** Used to calculate expected claims and set premiums

**Example:**
- **Dice Game:** Fair six-sided die has expected value $\mathbb{E}[X] = (1+2+3+4+5+6)/6 = 3.5$
- **Insurance Premium:** If an insurance policy pays $10,000 with probability 0.01 and $0 otherwise, expected payout is $10,000 \times 0.01 = $100, so premium should be >$100 to be profitable

### **4. Properties of Expected Value**

* Linearity:

  $
  \mathbb{E}[kX] = k\mathbb{E}[X]
  $

  $
  \mathbb{E}[X + k] = \mathbb{E}[X] + k
  $

  $
  \mathbb{E}[X + Y] = \mathbb{E}[X] + \mathbb{E}[Y]
  $

  $
  \mathbb{E}\!\left[\sum_{i=1}^n X_i\right] = \sum_{i=1}^n \mathbb{E}[X_i]
  $
* For a transformation $Y = \Phi(X)$:

  $
  \mathbb{E}[Y] = \mathbb{E}[\Phi(X)]
  $

### **5. Variance**

* Definition:

  $
  \mathrm{Var}(X) = \mathbb{E}[(X - \mu)^2]
  $
* **Discrete Case:**

  $
  \mathrm{Var}(X) = \sum_i (x_i - \mu)^2 f(x_i)
  $
* **Continuous Case:**

  $  \mathrm{Var}(X) = \int_{-\infty}^\infty (x - \mu)^2 f(x)\, dx
  $
* Alternative Formula:

  $
  \mathrm{Var}(X) = \mathbb{E}[X^2] - \mu^2
  $

**Context and Usage:**
- **Risk Assessment:** Measures how spread out values are from the mean - higher variance means more uncertainty
- **Quality Control:** Used to assess consistency in manufacturing (lower variance = more consistent products)
- **Finance:** Portfolio variance measures investment risk
- **Statistics:** Foundation for confidence intervals and hypothesis testing

**Example:**
- **Manufacturing:** Machine producing bolts with mean length 10cm. If variance is 0.01, most bolts are within ~10±0.3cm. If variance is 1.0, bolts vary by ~10±3cm.
- **Investment:** Two stocks both with expected return 8%. Stock A with variance 16 (σ=4%) is less risky than Stock B with variance 64 (σ=8%).

### **6. Standard Deviation**

$\sigma_X = \sqrt{\mathrm{Var}(X)}$

**Context and Usage:**
- **Same units as data:** Unlike variance, standard deviation is in the same units as the original measurements
- **Rule of Thumb:** About 68% of data falls within ±1σ, 95% within ±2σ, 99.7% within ±3σ (for normal distributions)
- **Comparative Analysis:** Used to compare variability between different datasets

**Example:**
- **Test Scores:** Class A has mean 75, σ=5. Class B has mean 75, σ=15. Class A is more consistent.
- **Blood Pressure:** Normal range is about 120±20 mmHg (σ≈6.7 mmHg), indicating typical variation in healthy population.

### **7. Covariance**

$\mathrm{Cov}(X, Y) = \mathbb{E}[(X - \mu_X)(Y - \mu_Y)]$

Alternative form:

$\mathrm{Cov}(X, Y) = \mathbb{E}[XY] - \mu_X \mu_Y$

**Context and Usage:**
- **Direction of Relationship:** Positive covariance indicates variables tend to move together, negative means they move oppositely
- **Linear Dependence:** Measures linear relationship strength, but scale-dependent
- **Portfolio Theory:** Used in finance to understand how assets move together
- **Multivariate Analysis:** Foundation for principal component analysis and factor analysis

**Example:**
- **Height and Weight:** Covariance between height (inches) and weight (pounds) is typically positive - taller people tend to weigh more
- **Stock Portfolio:** If Stock A and Stock B both tend to increase together, they have positive covariance

### **8. Correlation**

$\rho(X, Y) = \frac{\mathrm{Cov}(X, Y)}{\sigma_X \sigma_Y}$

**Context and Usage:**
- **Standardized Measure:** Always between -1 and +1, allowing comparison across different scales
- **Strength Assessment:** |ρ| = 1 indicates perfect linear relationship, |ρ| = 0 indicates no linear relationship
- **Regression Analysis:** Used to quantify relationship strength in linear regression
- **Feature Selection:** Helps identify redundant variables in machine learning

**Example:**
- **Perfect Correlation:** Height in inches and height in centimeters have ρ = 1 (perfect positive correlation)
- **Study Time and Grades:** If ρ = 0.7, there's a strong positive relationship - more study time tends to result in better grades
- **Random Walk:** Stock price changes and lottery numbers have ρ ≈ 0 (no meaningful relationship)

### **9. Independent Random Variables**

* Independence:

  $P(X = x_i, Y = y_j) = P(X = x_i) \cdot P(Y = y_j)$

* Properties for independent $X$ and $Y$:

  $\mathbb{E}[XY] = \mathbb{E}[X] \cdot \mathbb{E}[Y]$

  $\mathrm{Var}(X + Y) = \mathrm{Var}(X) + \mathrm{Var}(Y)$

  $\mathrm{Cov}(X, Y) = 0$

**Context and Usage:**
- **No Influence:** Independent variables don't affect each other's outcomes
- **Simplification:** Makes probability calculations much easier when dealing with multiple variables
- **Experimental Design:** Important in statistics to ensure treatments don't interfere with each other
- **Risk Assessment:** Independent risks can be added directly, dependent risks require more complex analysis

**Example:**
- **Coin Flips:** Tossing two fair coins - the outcome of first coin doesn't affect the second coin
- **Manufacturing Lines:** Quality defects on two independent production lines can be analyzed separately
- **Weather and Stock Market:** Generally independent - rain in New York doesn't systematically affect stock prices

### **10. Cumulative Distribution Function (CDF)**

* Definition:

  $F(x) = P(X \leq x)$

* **Discrete Case:**

  $F(x) = \sum_{x_i \leq x} f(x_i)$

* **Continuous Case:**

  $F(x) = \int_{-\infty}^x f(t)\, dt$

**Context and Usage:**
- **Probability Calculation:** Gives probability that random variable is less than or equal to a specific value
- **Percentile Determination:** F(x) tells you what percentage of data falls below x
- **Hypothesis Testing:** Used in statistical tests to determine p-values
- **Risk Analysis:** Helps calculate probabilities of extreme events

**Example:**
- **Dice CDF:** For a fair six-sided die, F(3) = P(X ≤ 3) = (1+2+3)/6 = 0.5, meaning 50% of rolls are 3 or less
- **Test Scores:** If F(85) = 0.7, then 70% of students scored 85 or below
- **Height Distribution:** F(170) = 0.5 means 50% of people are 170cm or shorter (median height)

---

## **II. Specific Probability Distributions**

### **1. Bernoulli Distribution**

* **PMF:**

  $
  P(X = 1) = p,
  \quad
  P(X = 0) = 1 - p
  $
* Mean and variance:

  $
  \mathbb{E}[X] = p,
  \qquad
  \mathrm{Var}(X) = p(1 - p)
  $

**Context and Usage:**
- **Single Trial:** Models a single yes/no, success/failure experiment
- **Building Block:** Foundation for binomial distribution (multiple Bernoulli trials)
- **Quality Control:** Pass/fail inspection of individual items
- **Clinical Trials:** Success/failure of a treatment on a single patient

**Example:**
- **Coin Flip:** X = 1 if heads (success), X = 0 if tails. If fair coin, p = 0.5
- **Quality Control:** X = 1 if a light bulb works, X = 0 if defective. If p = 0.95, 95% of bulbs work
- **Email Campaign:** X = 1 if customer clicks link, X = 0 otherwise. If p = 0.02, expect 2% click rate

### **2. Binomial Distribution**

* **PMF:**

  $
  P(X = x) = \binom{n}{x} p^x (1 - p)^{n - x},
  \quad x = 0,1,\dots,n
  $
* Mean and variance:

  $
  \mathbb{E}[X] = np,
  \qquad
  \mathrm{Var}(X) = np(1 - p)
  $

**Context and Usage:**
- **Multiple Trials:** Models number of successes in n independent Bernoulli trials
- **Count Data:** Used when counting occurrences of events in fixed number of opportunities
- **Quality Control:** Number of defective items in a batch of fixed size
- **Survey Analysis:** Number of people with a certain characteristic in a sample

**Example:**
- **Coin Flips:** Number of heads in 10 flips of fair coin (p=0.5, n=10). Expected value = 5 heads
- **Quality Control:** Number of defective products in a batch of 100 items, if defect rate is 3% (p=0.03, n=100)
- **Multiple Choice Test:** Number of correct answers out of 20 questions, if probability of guessing correctly is 0.25 (p=0.25, n=20)

### **3. Poisson Distribution**

* **PMF:**

  $
  P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!},
  \quad k = 0,1,2,\dots
  $
* Mean and variance:

  $
  \mathbb{E}[X] = \lambda,
  \qquad
  \mathrm{Var}(X) = \lambda
  $

**Context and Usage:**
- **Rare Events:** Models count of rare events occurring in fixed time/space intervals
- **Rate-Based:** Used when events happen independently at a constant average rate
- **Queueing Theory:** Number of customers arriving, calls received, accidents occurring
- **Natural Phenomena:** Radioactive decay, mutations, meteor showers

**Example:**
- **Call Center:** Number of calls received per hour if average is 5 calls/hour (λ=5)
- **Traffic Accidents:** Number of accidents at an intersection per day if average is 0.3/day (λ=0.3)
- **Website Visitors:** Number of visitors to a rarely-visited page per day if average is 2/day (λ=2)

### **4. Uniform Distribution (Continuous)**

* **PDF:**

  $
  f(x) = \frac{1}{b - a}, \quad a \leq x \leq b
  $
* Mean and variance:

  $
  \mathbb{E}[X] = \frac{a + b}{2},
  \qquad
  \mathrm{Var}(X) = \frac{(b - a)^2}{12}
  $

**Context and Usage:**
- **Equal Likelihood:** All values in an interval are equally likely to occur
- **Random Selection:** Models truly random selection from a continuous range
- **Simulation:** Used in Monte Carlo methods and random number generation
- **Physical Measurements:** When no value is more likely than another within bounds

**Example:**
- **Random Number Generator:** Numbers between 0 and 1 are equally likely (a=0, b=1)
- **Bus Arrival:** If buses come exactly every 10 minutes, time until next bus is uniform between 0 and 10 minutes
- **Manufacturing Tolerance:** Diameter of shafts within tolerance limits [9.95mm, 10.05mm] with no preferred value

### **5. Exponential Distribution**

* **PDF:**

  $
  f(x) = \lambda e^{-\lambda x}, \quad x \geq 0
  $
* Mean and variance:

  $
  \mathbb{E}[X] = \frac{1}{\lambda},
  \qquad
  \mathrm{Var}(X) = \frac{1}{\lambda^2}
  $

**Context and Usage:**
- **Waiting Times:** Models time between events in a Poisson process
- **Survival Analysis:** Time until failure, death, or other terminating event
- **Reliability Engineering:** Time until system failure or component breakdown
- **Queueing Theory:** Time between customer arrivals or service times

**Example:**
- **Radioactive Decay:** Time until a radioactive atom decays (λ = decay rate)
- **Customer Service:** Time between customer arrivals at a bank if average is 2 minutes (λ = 0.5 per minute)
- **Equipment Failure:** Time until a light bulb burns out if average lifetime is 1000 hours (λ = 0.001 per hour)

### **6. Normal Distribution**

* **PDF:**

  $
  f(x) = \frac{1}{\sigma \sqrt{2\pi}}
  \exp\!\left(-\frac{(x - \mu)^2}{2\sigma^2}\right)
  $
* Mean and variance:

  $
  \mathbb{E}[X] = \mu,
  \qquad
  \mathrm{Var}(X) = \sigma^2
  $

**Context and Usage:**
- **Natural Phenomena:** Height, weight, IQ scores, measurement errors
- **Central Limit Theorem:** Many real-world variables become normally distributed with large samples
- **Statistical Inference:** Foundation for hypothesis testing, confidence intervals
- **Quality Control:** Process capability analysis, Six Sigma methodology

**Example:**
- **Human Height:** Adult male heights in US ~ Normal(μ=70 inches, σ=3 inches)
- **Test Scores:** Standardized test scores often designed to be normal (μ=100, σ=15)
- **Manufacturing:** Diameter measurements of precision parts with small variations around target

---

## **III. Application in Games of Chance**

* **Expected Gain:**

  $
  \mathbb{E} > 0 \quad \text{Favorable Game}
  $

  $
  \mathbb{E} < 0 \quad \text{Unfavorable Game}
  $

  $
  \mathbb{E} = 0 \quad \text{Fair Game}
  $

**Context and Usage:**
- **Decision Making:** Expected value determines if a game favors the player, casino, or is fair
- **Risk Assessment:** Helps players understand long-term outcomes vs. short-term variance
- **Game Design:** Casinos use house edge (negative expected value for players) to ensure profitability
- **Strategy Development:** Players can identify games with positive expected value

**Example:**
- **Fair Coin Flip:** Bet $1 on heads. Win $1 if correct, lose $1 if wrong. $\mathbb{E} = (0.5)(1) + (0.5)(-1) = 0$ (fair game)
- **Roulette (Single Zero):** Bet $1 on red. Win $1 with p=18/37, lose $1 with p=19/37. $\mathbb{E} = (18/37)(1) + (19/37)(-1) = -1/37 \approx -$0.027 (unfavorable)
- **Slot Machine:** Bet $1, win $10 with p=0.01, win $0 otherwise. $\mathbb{E} = (0.01)(10) + (0.99)(0) = $0.10 (favorable, but rare!)
- **Casino Blackjack:** With perfect basic strategy, house edge ≈ 0.5%, so $\mathbb{E} ≈ -$0.005 per $1 bet (slightly unfavorable)
