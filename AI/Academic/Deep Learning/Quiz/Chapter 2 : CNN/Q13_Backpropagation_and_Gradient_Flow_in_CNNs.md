---
sources:
  - "[[13. Backpropagation and Gradient Flow in CNNs]]"
---
> [!question] The primary goal of training a neural network is to maximize the loss function.
>> [!success]- Answer
>> False

> [!question] The loss function quantifies how wrong a neural network's predictions are.
>> [!success]- Answer
>> True

> [!question] Backpropagation is a learning algorithm that directly updates the weights of a neural network.
>> [!success]- Answer
>> False

> [!question] Mean Squared Error (MSE) is commonly used as a loss function for classification tasks.
>> [!success]- Answer
>> False

> [!question] The chain rule of calculus is essential for computing gradients in deep neural networks.
>> [!success]- Answer
>> True

> [!question] A neural network can be considered as a composition of many individual operations.
>> [!success]- Answer
>> True

> [!question] Cross-Entropy Loss measures the divergence between predicted and true probability distributions.
>> [!success]- Answer
>> True

> [!question] In backpropagation, gradients are computed from the output layer backward to the input layer.
>> [!success]- Answer
>> True

> [!question] The derivative of a composition of functions can be computed by simply multiplying the derivatives of each function.
>> [!success]- Answer
>> False

> [!question] Pooling operations are differentiable and contribute to the gradient computation in backpropagation.
>> [!success]- Answer
>> False

> [!question] What is the primary purpose of the loss function in neural network training?
> a) To increase model complexity
> b) To quantify the error between predictions and targets
> c) To normalize input data
> d) To regularize the model
>> [!success]- Answer
>> b) To quantify the error between predictions and targets

> [!question] Which of the following is NOT a common loss function for classification tasks?
> a) Cross-Entropy Loss
> b) Mean Squared Error
> c) Hinge Loss
> d) Kullback-Leibler Divergence
>> [!success]- Answer
>> b) Mean Squared Error

> [!question] What mathematical principle is essential for backpropagation in deep neural networks?
> a) The product rule
> b) The chain rule
> c) The quotient rule
> d) The power rule
>> [!success]- Answer
>> b) The chain rule

> [!question] In the context of gradient flow, what does the gradient represent?
> a) The direction of steepest increase in the loss
> b) The direction of steepest decrease in the loss
> c) The magnitude of the loss
> d) The optimal learning rate
>> [!success]- Answer
>> a) The direction of steepest increase in the loss

> [!question] Which operation is typically NOT differentiable and requires special handling during backpropagation?
> a) ReLU activation
> b) Sigmoid activation
> c) Max pooling
> d) Convolution
>> [!success]- Answer
>> c) Max pooling

> [!question] What happens during the forward pass of a CNN?
> a) Gradients are computed and weights are updated
> b) Input data flows through the network producing predictions
> c) The loss function is minimized
> d) Network architecture is modified
>> [!success]- Answer
>> b) Input data flows through the network producing predictions

> [!question] Which statement best describes vanishing gradients?
> a) Gradients become too large, causing unstable training
> b) Gradients become too small, slowing down or stopping learning in early layers
> c) The loss function becomes undefined
> d) The network forgets previously learned features
>> [!success]- Answer
>> b) Gradients become too small, slowing down or stopping learning in early layers

> [!question] What is the purpose of batch normalization in CNNs?
> a) To reduce the number of parameters in the network
> b) To speed up the forward pass computation
> c) To stabilize and accelerate training by normalizing layer inputs
> d) To increase model capacity
>> [!success]- Answer
>> c) To stabilize and accelerate training by normalizing layer inputs

> [!question] Which activation function is commonly used in CNNs and helps mitigate the vanishing gradient problem?
> a) Sigmoid
> b) Tanh
> c) ReLU
> d) Softmax
>> [!success]- Answer
>> c) ReLU

> [!question] What is the main challenge in computing gradients for deep neural networks?
> a) The computational complexity is too high
> b) The loss function is not convex
> c) The chain rule must be applied through many layers
> d) The input data is too large
>> [!success]- Answer
>> c) The chain rule must be applied through many layers

> [!question] Match the optimization concepts with their descriptions.
>> [!example] Group A
>> a) Gradient Descent
>> b) Learning Rate
>> c) Backpropagation
>
>> [!example] Group B
>> n) The algorithm for computing gradients efficiently in neural networks
>> o) The step size taken during weight updates
>> p) The optimization algorithm that follows the negative gradient direction
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the CNN components with their gradient flow characteristics.
>> [!example] Group A
>> a) Convolution Layer
>> b) ReLU Activation
>> c) Pooling Layer
>
>> [!example] Group B
>> n) Typically has a gradient that is either 0 or the input value
>> o) Computes gradients based on the kernel parameters and input feature maps
>> p) Often causes gradient reduction, potentially leading to vanishing gradients
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the loss functions with their typical applications.
>> [!example] Group A
>> a) Mean Squared Error
>> b) Cross-Entropy Loss
>> c) Hinge Loss
>
>> [!example] Group B
>> n) Used for ordinal regression or SVM-like classification
>> o) Commonly used for regression problems
>> p) Standard for multi-class classification problems
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the gradient issues with their descriptions.
>> [!example] Group A
>> a) Vanishing Gradients
>> b) Exploding Gradients
>> c) Gradient Clipping
>
>> [!example] Group B
>> n) Technique to prevent large gradients from destabilizing training
>> o) Problem where gradients become too small for effective learning
>> p) Problem where gradients become too large, causing numerical instability
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the optimization algorithms with their characteristics.
>> [!example] Group A
>> a) SGD
>> b) Adam
>> c) RMSprop
>
>> [!example] Group B
>> n) Uses adaptive learning rates and momentum
>> o) Simple but effective method that updates weights based on the gradient
>> p) Adapts learning rates based on moving averages of squared gradients
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the CNN operations with their gradient computation methods.
>> [!example] Group A
>> a) Convolution
>> b) Max Pooling
>> c) Average Pooling
>
>> [!example] Group B
>> n) Propagates gradients by distributing the incoming gradient equally to all positions
>> o) Propagates gradients only to the position that had the maximum value during forward pass
>> p) Computes gradients with respect to kernel weights and input feature maps
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the derivative concepts with their mathematical expressions.
>> [!example] Group A
>> a) Chain Rule
>> b) Partial Derivative
>> c) Total Derivative
>
>> [!example] Group B
>> n) Measures how a function changes with respect to one variable while holding others constant
>> o) Describes the rate of change of a function with respect to its input
>> p) Allows computation of derivatives of composed functions by multiplying derivatives
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the regularization techniques with their gradient flow effects.
>> [!example] Group A
>> a) L1 Regularization
>> b) L2 Regularization
>> c) Dropout
>
>> [!example] Group B
>> n) Adds penalty proportional to the square of weights, encouraging smaller weights
>> o) Randomly sets activations to zero during training, creating redundant pathways
>> p) Adds penalty proportional to absolute value of weights, promoting sparsity
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the gradient-based optimization concepts with their purposes.
>> [!example] Group A
>> a) Momentum
>> b) Learning Rate Scheduling
>> c) Batch Normalization
>
>> [!example] Group B
>> n) Adjusts learning rate during training to improve convergence
>> o) Accumulates past gradient directions to accelerate learning in consistent directions
>> p) Normalizes layer inputs to reduce internal covariate shift
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the CNN architectural components with their gradient flow characteristics.
>> [!example] Group A
>> a) Skip Connections
>> b) Batch Normalization
>> c) Depthwise Separable Convolution
>
>> [!example] Group B
>> n) Reduces computational cost and may help with gradient flow
>> o) Creates shortcuts for gradients to flow through deeper networks
>> p) Normalizes activations to maintain stable gradient distributions
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
