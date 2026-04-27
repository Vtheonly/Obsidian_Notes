---
sources:
  - "[[6. Loss Functions and Cost Optimization]]"
---
> [!question] MSE stands for Mean Squared Error and is used for regression problems.
>> [!success]- Answer
>> True

> [!question] MAE is more sensitive to outliers than MSE.
>> [!success]- Answer
>> False

> [!question] Huber Loss behaves like MSE for small errors and like MAE for large errors.
>> [!success]- Answer
>> True

> [!question] Binary Cross-Entropy is used for multi-class classification with 5+ classes.
>> [!success]- Answer
>> False

> [!question] Using MSE for classification results in a non-convex loss landscape.
>> [!success]- Answer
>> True

> [!question] Categorical Cross-Entropy uses one-hot encoded labels.
>> [!success]- Answer
>> True

> [!question] Hinge Loss is primarily used for Support Vector Machines.
>> [!success]- Answer
>> True

> [!question] The logarithm in classification loss punishes confident wrong predictions exponentially.
>> [!success]- Answer
>> True

> [!question] MAE has a gradient that naturally decreases as the error approaches zero.
>> [!success]- Answer
>> False

> [!question] Categorical Cross-Entropy is always paired with the Softmax activation.
>> [!success]- Answer
>> True

> [!question] Which loss function is most appropriate for a regression problem with severe outliers?
> a) MSE
> b) MAE
> c) Binary Cross-Entropy
> d) Hinge Loss
>> [!success]- Answer
>> b) MAE

> [!question] What is the formula for MSE?
> a) Average of absolute differences
> b) Average of squared differences between predicted and actual values
> c) Sum of logarithms
> d) Max of differences
>> [!success]- Answer
>> b) Average of squared differences between predicted and actual values

> [!question] Why is MSE sensitive to outliers?
> a) It uses absolute values
> b) Errors are squared, so an outlier with error 10 contributes 100 to the loss
> c) It ignores outliers completely
> d) It uses logarithms
>> [!success]- Answer
>> b) Errors are squared, so an outlier with error 10 contributes 100 to the loss

> [!question] What does Huber Loss do when the error is below the threshold delta?
> a) It acts like MAE
> b) It acts like MSE (quadratic)
> c) It acts like Cross-Entropy
> d) It becomes zero
>> [!success]- Answer
>> b) It acts like MSE (quadratic)

> [!question] Which loss function is used for binary classification?
> a) MSE
> b) MAE
> c) Binary Cross-Entropy (Log Loss)
> d) Huber Loss
>> [!success]- Answer
>> c) Binary Cross-Entropy (Log Loss)

> [!question] Why should you never use MSE for classification?
> a) It is too fast
> b) It produces a non-convex landscape with many local minima
> c) It only works with images
> d) It requires too much memory
>> [!success]- Answer
>> b) It produces a non-convex landscape with many local minima

> [!question] What happens to the penalty in Log Loss when the model predicts 0.001 for a true label of 1?
> a) The penalty is 0.001
> b) The penalty is approximately 0.99
> c) The penalty is very large (approximately 6.9)
> d) There is no penalty
>> [!success]- Answer
>> c) The penalty is very large (approximately 6.9)

> [!question] What is the key property of Hinge Loss?
> a) It always produces zero loss
> b) It forces predictions to be correct by a margin, not just correct
> c) It uses logarithms
> d) It only works for regression
>> [!success]- Answer
>> b) It forces predictions to be correct by a margin, not just correct

> [!question] In Categorical Cross-Entropy, which terms contribute to the loss?
> a) All class terms equally
> b) Only the term for the true class (because other y_ij are 0)
> c) Only the predicted class
> d) No terms contribute
>> [!success]- Answer
>> b) Only the term for the true class (because other y_ij are 0)

> [!question] Why does the 1/2m trick in MSE exist?
> a) To make MSE larger
> b) To make the derivative cleaner by canceling the exponent 2
> c) To change the optimization result
> d) To handle outliers
>> [!success]- Answer
>> b) To make the derivative cleaner by canceling the exponent 2

> [!question] Match the loss function with its use case.
>> [!example] Group A
>> a) MSE
>> b) Binary Cross-Entropy
>> c) Categorical Cross-Entropy
>> d) Huber Loss
>
>> [!example] Group B
>> n) Multi-class classification
>> o) Regression with occasional outliers
>> p) Binary classification
>> q) Standard regression without severe outliers
>
>> [!success]- Answer
>> a) -> q)
>> b) -> p)
>> c) -> n)
>> d) -> o)

> [!question] Match the loss function with its sensitivity to outliers.
>> [!example] Group A
>> a) MSE
>> b) MAE
>> c) Huber Loss
>
>> [!example] Group B
>> n) Moderate — switches behavior at threshold delta
>> o) Low — each outlier contributes linearly
>> p) High — errors are squared
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the classification loss with the number of classes it handles.
>> [!example] Group A
>> a) Binary Cross-Entropy
>> b) Categorical Cross-Entropy
>
>> [!example] Group B
>> n) 3+ classes (multi-class)
>> o) 2 classes (binary)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the loss behavior with the scenario.
>> [!example] Group A
>> a) Log Loss when y=1 and prediction=0.99
>> b) Log Loss when y=1 and prediction=0.01
>
>> [!example] Group B
>> n) Huge penalty (confidently wrong)
>> o) Minimal penalty (correct and confident)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the loss function with its gradient behavior near zero.
>> [!example] Group A
>> a) MSE
>> b) MAE
>
>> [!example] Group B
>> n) Constant gradient (oscillates around minimum)
>> o) Gradient naturally decreases (smooth convergence)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the Huber Loss region with its behavior.
>> [!example] Group A
>> a) Error <= delta
>> b) Error > delta
>
>> [!example] Group B
>> n) Linear (MAE-like, robust to outliers)
>> o) Quadratic (MSE-like, smooth convergence)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the loss function with its mathematical operation.
>> [!example] Group A
>> a) MSE
>> b) MAE
>> c) Log Loss
>
>> [!example] Group B
>> n) Negative logarithm of predicted probability
>> o) Average of absolute differences
>> p) Average of squared differences
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the Hinge Loss condition with the outcome.
>> [!example] Group A
>> a) y * y_hat >= 1
>> b) 0 < y * y_hat < 1
>> c) y * y_hat < 0
>
>> [!example] Group B
>> n) Loss = 0 (correct with margin)
>> o) Loss > 1 (wrong prediction)
>> p) Loss > 0 (correct but too close to boundary)
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the loss function with the paired activation.
>> [!example] Group A
>> a) BCE
>> b) CCE
>
>> [!example] Group B
>> n) Softmax
>> o) Sigmoid
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the property with the loss function.
>> [!example] Group A
>> a) Quadratic penalty on errors
>> b) Linear penalty on errors
>> c) Exponentially increasing penalty for confident wrong predictions
>
>> [!example] Group B
>> n) MAE
>> o) Log Loss / Cross-Entropy
>> p) MSE
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)
