---
sources:
  - "[[20. Loss Functions and Optimizers Deep Dive]]"
---
> [!question] The loss function is used to evaluate the final performance of a trained model.
>> [!success]- Answer
>> False

> [!question] A loss function must always be differentiable to be used in training neural networks.
>> [!success]- Answer
>> True

> [!question] The Softmax function ensures that the outputs sum to 1 and are in the range (0, 1).
>> [!success]- Answer
>> True

> [!question] Cross-Entropy Loss is the most commonly used loss function for regression problems.
>> [!success]- Answer
>> False

> [!question] The LogSumExp trick is used to prevent numerical overflow in the computation of Cross-Entropy Loss.
>> [!success]- Answer
>> True

> [!question] Accuracy is a differentiable metric that can be directly used as a loss function for neural networks.
>> [!success]- Answer
>> False

> [!question] Negative Log-Likelihood Loss is the same as Cross-Entropy Loss when used with Softmax outputs.
>> [!success]- Answer
>> True

> [!question] A decreasing training loss always indicates that the model is performing better on unseen data.
>> [!success]- Answer
>> False

> [!question] The gradient of the loss function tells each weight which direction and how much to change.
>> [!success]- Answer
>> True

> [!question] For binary classification problems, Binary Cross-Entropy is typically preferred over Mean Squared Error.
>> [!success]- Answer
>> True

> [!question] What is the primary purpose of a loss function in deep learning?
> a) To visualize the model's architecture
> b) To quantify how wrong the model's predictions are
> c) To increase the model's complexity
> d) To reduce the amount of training data needed
>> [!success]- Answer
>> b) To quantify how wrong the model's predictions are

> [!question] Which of the following is NOT a property of the Softmax function?
> a) Outputs are in the range (0, 1)
> b) Outputs sum to 1
> c) Outputs are monotonic in the logits
> d) Outputs can be negative
>> [!success]- Answer
>> d) Outputs can be negative

> [!question] What is the main difference between a loss function and an evaluation metric?
> a) Loss functions are used for testing, metrics for training
> b) Loss functions must be differentiable, metrics may not be
> c) Loss functions are always linear, metrics can be non-linear
> d) There is no difference between them
>> [!success]- Answer
>> b) Loss functions must be differentiable, metrics may not be

> [!question] Which loss function is most appropriate for multi-class classification problems?
> a) Mean Squared Error
> b) Mean Absolute Error
> c) Cross-Entropy Loss
> d) Hinge Loss
>> [!success]- Answer
>> c) Cross-Entropy Loss

> [!question] What does the LogSumExp trick help prevent in the computation of Cross-Entropy Loss?
> a) Computational complexity
> b) Overfitting
> c) Numerical overflow or underflow
> d) Vanishing gradients
>> [!success]- Answer
>> c) Numerical overflow or underflow

> [!question] Which of the following statements about Cross-Entropy Loss is true?
> a) It's only used for binary classification
> b) It combines Softmax and Negative Log-Likelihood
> c) It's not suitable for neural networks
> d) It's the same as Mean Squared Error for classification
>> [!success]- Answer
>> b) It combines Softmax and Negative Log-Likelihood

> [!question] What happens to the Cross-Entropy Loss when the model is very confident about the correct class?
> a) The loss becomes very large
> b) The loss approaches zero
> c) The loss becomes undefined
> d) The loss remains constant
>> [!success]- Answer
>> b) The loss approaches zero

> [!question] Which of the following is NOT a role of the loss function in training?
> a) Providing gradient signals for parameter updates
> b) Defining what "good" means for the problem
> c) Monitoring training progress
> d) Selecting the model architecture
>> [!success]- Answer
>> d) Selecting the model architecture

> [!question] What is the formula for Cross-Entropy Loss when expanded?
> a) -z_c + log(sum(e^z_j))
> b) z_c * log(sum(e^z_j))
> c) -sum(z_c * log(p_c))
> d) sum((p_c - z_c)^2)
>> [!success]- Answer
>> a) -z_c + log(sum(e^z_j))

> [!question] Match the loss functions to their most appropriate use cases.
>> [!example] Loss Functions
>> a) Cross-Entropy Loss
>> b) Mean Squared Error
>> c) Hinge Loss
>
>> [!example] Use Cases
>> n) Multi-class classification
>> o) Regression problems
>> p) Support Vector Machines
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the components to their descriptions.
>> [!example] Components
>> a) Softmax
>> b) Negative Log-Likelihood
>> c) LogSumExp
>
>> [!example] Descriptions
>> n) Converts logits to probabilities
>> o) Computes negative log of correct class probability
>> p) Prevents numerical overflow in log-sum-exp calculation
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the properties to their corresponding functions.
>> [!example] Properties
>> a) Outputs sum to 1
>> b) Differentiable everywhere
>> c) Measures classification error
>
>> [!example] Functions
>> n) Softmax
>> o) Cross-Entropy
>> p) Mean Squared Error
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the optimization challenges to their potential solutions.
>> [!example] Challenges
>> a) Vanishing gradients
>> b) Exploding gradients
>> c) Overfitting
>
>> [!example] Solutions
>> n) Gradient clipping
>> o) Regularization techniques
>> p) Activation functions like ReLU
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the loss functions to their mathematical formulations.
>> [!example] Loss Functions
>> a) Binary Cross-Entropy
>> b) Categorical Cross-Entropy
>> c) Hinge Loss
>
>> [!example] Formulations
>> n) -∑(y_i * log(p_i) + (1-y_i) * log(1-p_i))
>> o) -∑(y_i * log(p_i))
>> p) max(0, 1 - y_i * p_i)
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the concepts to their definitions.
>> [!example] Concepts
>> a) Loss function
>> b) Metric
>> c) Optimizer
>
>> [!example] Definitions
>> n) Measures model performance for evaluation
>> o) Algorithm that updates model parameters based on loss
>> p) Function that quantifies model error
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the regularization techniques to their purposes.
>> [!example] Techniques
>> a) L1 regularization
>> b) L2 regularization
>> c) Dropout
>
>> [!example] Purposes
>> n) Encourages sparse weights
>> o) Prevents co-adaptation of neurons
>> p) Penalizes large weights
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the gradient descent variants to their characteristics.
>> [!example] Variants
>> a) Batch Gradient Descent
>> b) Stochastic Gradient Descent
>> c) Adam Optimizer
>
>> [!example] Characteristics
>> n) Uses entire dataset for each update
>> o) Uses single sample for each update
>> p) Adaptive learning rate methods
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the activation functions to their common use cases.
>> [!example] Activation Functions
>> a) Sigmoid
>> b) Tanh
>> c) ReLU
>
>> [!example] Use Cases
>> n) Binary classification output
>> o) Hidden layers with zero-centered outputs
>> p) Hidden layers with non-linearity
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
