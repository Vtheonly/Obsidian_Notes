---
sources:
  - "[[7. Linear Regression]]"
---
> [!question] Linear regression predicts a continuous output Y based on input X.
>> [!success]- Answer
>> True

> [!question] In simple linear regression, the hypothesis function is Y = wX + b.
>> [!success]- Answer
>> True

> [!question] The bias term (theta_0) represents the slope of the regression line.
>> [!success]- Answer
>> False

> [!question] The cost function for linear regression is the Mean Squared Error (MSE).
>> [!success]- Answer
>> True

> [!question] In gradient descent for linear regression, theta_0 and theta_1 must be updated simultaneously.
>> [!success]- Answer
>> True

> [!question] Vectorization replaces slow for-loops with fast matrix operations.
>> [!success]- Answer
>> True

> [!question] The Normal Equation gives an approximate solution that requires iteration.
>> [!success]- Answer
>> False

> [!question] Feature scaling helps gradient descent converge faster by making the loss landscape more circular.
>> [!success]- Answer
>> True

> [!question] Min-Max Normalization is more robust to outliers than Z-score Standardization.
>> [!success]- Answer
>> False

> [!question] OLS (Ordinary Least Squares) is the analytical solution for linear regression.
>> [!success]- Answer
>> True

> [!question] What is the vectorized form of the hypothesis function?
> a) h(x) = theta_0 + theta_1 * x
> b) h(x) = theta^T * x
> c) h(x) = sigmoid(theta^T * x)
> d) h(x) = max(0, theta^T * x)
>> [!success]- Answer
>> b) h(x) = theta^T * x

> [!question] Why must theta_0 and theta_1 be updated simultaneously?
> a) It is faster computationally
> b) Sequential updates use a different point on the loss surface, leading to incorrect gradient
> c) It reduces the learning rate
> d) It makes the loss function convex
>> [!success]- Answer
>> b) Sequential updates use a different point on the loss surface, leading to incorrect gradient

> [!question] What does the 1/2m trick in the MSE cost function accomplish?
> a) It makes the loss larger
> b) It simplifies the derivative by canceling the exponent 2
> c) It handles outliers
> d) It changes the minimum
>> [!success]- Answer
>> b) It simplifies the derivative by canceling the exponent 2

> [!question] What is the Normal Equation?
> a) W = X^T Y
> b) W = (X^T X)^{-1} X^T Y
> c) W = X Y^{-1}
> d) W = gradient * alpha
>> [!success]- Answer
>> b) W = (X^T X)^{-1} X^T Y

> [!question] When should you use Gradient Descent instead of OLS?
> a) When the dataset is small
> b) When you need the exact solution
> c) When the dataset is large or the model is non-linear
> d) When features are few
>> [!success]- Answer
>> c) When the dataset is large or the model is non-linear

> [!question] What is the complexity of computing the Normal Equation inverse?
> a) O(n)
> b) O(m^3) where m is the number of features
> c) O(1)
> d) O(log n)
>> [!success]- Answer
>> b) O(m^3) where m is the number of features

> [!question] What does Z-score standardization do?
> a) Scales data to [0, 1]
> b) Centers data to mean 0 and standard deviation 1
> c) Removes all outliers
> d) Converts data to integers
>> [!success]- Answer
>> b) Centers data to mean 0 and standard deviation 1

> [!question] Why is Min-Max Normalization vulnerable to outliers?
> a) It uses the mean
> b) A single extreme outlier compresses all other values into a tiny range
> c) It removes outliers
> d) It squares the values
>> [!success]- Answer
>> b) A single extreme outlier compresses all other values into a tiny range

> [!question] What is the matrix formulation for batch predictions in linear regression?
> a) Y_hat = X + W + b
> b) Y_hat = XW + b
> c) Y_hat = X * W * b
> d) Y_hat = X / W
>> [!success]- Answer
>> b) Y_hat = XW + b

> [!question] What is the endogenous variable in linear regression?
> a) The independent variable X
> b) The dependent variable Y being predicted
> c) The weight theta_1
> d) The bias theta_0
>> [!success]- Answer
>> b) The dependent variable Y being predicted

> [!question] Match the term with its meaning in linear regression.
>> [!example] Group A
>> a) theta_0 (bias)
>> b) theta_1 (weight)
>> c) Endogenous variable
>> d) Exogenous variable
>
>> [!example] Group B
>> n) Independent variable X
>> o) Dependent variable Y
>> p) Slope — how much Y changes per unit of X
>> q) Y-intercept — prediction when all inputs are zero
>
>> [!success]- Answer
>> a) -> q)
>> b) -> p)
>> c) -> o)
>> d) -> n)

> [!question] Match the scaling method with its formula.
>> [!example] Group A
>> a) Min-Max Normalization
>> b) Z-score Standardization
>
>> [!example] Group B
>> n) (x - mu) / sigma
>> o) (x - x_min) / (x_max - x_min)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the solution method with its characteristic.
>> [!example] Group A
>> a) OLS (Normal Equation)
>> b) Gradient Descent
>
>> [!example] Group B
>> n) Iterative approximation, scales to large datasets
>> o) Exact analytical solution, O(m^3) complexity
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the scaling method with its outlier robustness.
>> [!example] Group A
>> a) Min-Max Normalization
>> b) Z-score Standardization
>
>> [!example] Group B
>> n) More robust — does not compress range
>> o) Vulnerable — extreme outlier compresses all values
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the update approach with its correctness.
>> [!example] Group A
>> a) Simultaneous update
>> b) Sequential update
>
>> [!example] Group B
>> n) Incorrect — uses different point on loss surface
>> o) Correct — all gradients computed at the same point
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the partial derivative with the parameter it updates.
>> [!example] Group A
>> a) Average error (no x weighting)
>> b) Error weighted by x_i
>
>> [!example] Group B
>> n) Derivative for theta_1 (weight)
>> o) Derivative for theta_0 (bias)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the concept with its benefit.
>> [!example] Group A
>> a) Vectorization
>> b) Feature Scaling
>
>> [!example] Group B
>> n) Makes the loss landscape more circular for faster convergence
>> o) Replaces for-loops with fast matrix operations
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the approach with when to use it.
>> [!example] Group A
>> a) OLS / Normal Equation
>> b) Gradient Descent
>
>> [!example] Group B
>> n) Large dataset or many features or non-linear model
>> o) Small dataset with few features
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the matrix dimension with the variable.
>> [!example] Group A
>> a) n x m matrix
>> b) m x 1 vector
>> c) n x 1 vector
>
>> [!example] Group B
>> n) Y_hat (predictions)
>> o) X (feature matrix)
>> p) W (weights)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the scaling method with its output range.
>> [!example] Group A
>> a) Min-Max Normalization
>> b) Z-score Standardization
>
>> [!example] Group B
>> n) Mean 0, standard deviation 1
>> o) Strictly [0, 1]
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
