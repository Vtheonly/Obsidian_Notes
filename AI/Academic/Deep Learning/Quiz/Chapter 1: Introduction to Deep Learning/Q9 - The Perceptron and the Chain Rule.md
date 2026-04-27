---
sources:
  - "[[9. The Perceptron and the Chain Rule]]"
---
> [!question] The Perceptron is the simplest neural network — a single layer with a single neuron.
>> [!success]- Answer
>> True

> [!question] The Perceptron can solve non-linearly separable problems like XOR.
>> [!success]- Answer
>> False

> [!question] The Chain Rule of Calculus is used to compute gradients in backpropagation.
>> [!success]- Answer
>> True

> [!question] The Perceptron uses a step (Heaviside) activation function for classification.
>> [!success]- Answer
>> True

> [!question] The Perceptron weight update rule uses the error between the predicted and true output.
>> [!success]- Answer
>> True

> [!question] A single Perceptron can solve the AND and OR logic gates.
>> [!success]- Answer
>> True

> [!question] The Perceptron learning rule guarantees convergence for non-linearly separable data.
>> [!success]- Answer
>> False

> [!question] The Chain Rule states that the derivative of a composite function is the product of individual derivatives.
>> [!success]- Answer
>> True

> [!question] In the Perceptron, the bias term shifts the decision boundary away from the origin.
>> [!success]- Answer
>> True

> [!question] The Perceptron update rule increases weights when the prediction is correct.
>> [!success]- Answer
>> False

> [!question] What is the Perceptron's fundamental limitation?
> a) It requires too much data
> b) It can only solve linearly separable problems
> c) It is too slow
> d) It cannot use a bias term
>> [!success]- Answer
>> b) It can only solve linearly separable problems

> [!question] What does the Chain Rule allow us to compute?
> a) The dataset size
> b) The gradient of a composite function by multiplying individual derivatives
> c) The learning rate
> d) The number of layers
>> [!success]- Answer
>> b) The gradient of a composite function by multiplying individual derivatives

> [!question] What happens when the Perceptron's prediction matches the true label?
> a) Weights are increased
> b) Weights are decreased
> c) No update is needed — the weights are already correct for this example
> d) The bias is removed
>> [!success]- Answer
>> c) No update is needed — the weights are already correct for this example

> [!question] What activation function does the classic Perceptron use?
> a) Sigmoid
> b) ReLU
> c) Step (Heaviside) function
> d) Softmax
>> [!success]- Answer
>> c) Step (Heaviside) function

> [!question] Why was the XOR problem significant in the history of neural networks?
> a) It proved neural networks could solve any problem
> b) It showed that a single Perceptron cannot solve non-linearly separable problems, causing the first AI Winter
> c) It demonstrated the power of deep learning
> d) It proved GPUs are necessary
>> [!success]- Answer
>> b) It showed that a single Perceptron cannot solve non-linearly separable problems, causing the first AI Winter

> [!question] What is the Perceptron weight update formula?
> a) w = w + alpha * (y - y_hat) * x
> b) w = w - alpha * gradient
> c) w = w * alpha
> d) w = alpha * x
>> [!success]- Answer
>> a) w = w + alpha * (y - y_hat) * x

> [!question] What does the bias term do in a Perceptron?
> a) It speeds up computation
> b) It shifts the decision boundary away from the origin
> c) It adds more layers
> d) It removes the need for weights
>> [!success]- Answer
>> b) It shifts the decision boundary away from the origin

> [!question] Which logic gate CAN a single Perceptron solve?
> a) XOR
> b) AND
> c) XNOR
> d) None of the above
>> [!success]- Answer
>> b) AND

> [!question] In the Chain Rule, if z = f(g(x)), what is dz/dx?
> a) f(x) * g(x)
> b) f'(g(x)) * g'(x)
> c) f(x) + g(x)
> d) f(g(x))
>> [!success]- Answer
>> b) f'(g(x)) * g'(x)

> [!question] What did Minsky and Papert prove in 1969?
> a) That neural networks can solve all problems
> b) That a single-layer Perceptron is fundamentally incapable of solving XOR
> c) That GPUs are needed for training
> d) That backpropagation works
>> [!success]- Answer
>> b) That a single-layer Perceptron is fundamentally incapable of solving XOR

> [!question] Match the Perceptron component with its role.
>> [!example] Group A
>> a) Weights
>> b) Bias
>> c) Activation function
>> d) Input
>
>> [!example] Group B
>> n) Shifts the decision boundary
>> o) Raw data fed to the neuron
>> p) Determines the strength of each input connection
>> q) Produces the final binary output
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)

> [!question] Match the logic gate with whether a single Perceptron can solve it.
>> [!example] Group A
>> a) AND
>> b) OR
>> c) XOR
>
>> [!example] Group B
>> n) Cannot be solved (non-linearly separable)
>> o) Can be solved (linearly separable)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> o)
>> c) -> n)

> [!question] Match the Chain Rule step with the operation.
>> [!example] Group A
>> a) f(g(x))
>> b) f'(g(x))
>> c) g'(x)
>
>> [!example] Group B
>> n) Derivative of inner function
>> o) Derivative of outer function evaluated at inner function
>> p) Composite function itself
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the update scenario with the weight change.
>> [!example] Group A
>> a) y = 1, y_hat = 0
>> b) y = 0, y_hat = 1
>> c) y = y_hat
>
>> [!example] Group B
>> n) No change needed
>> o) Increase weights (positive error)
>> p) Decrease weights (negative error)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the Perceptron part with its biological analogy.
>> [!example] Group A
>> a) Weights
>> b) Summation
>> c) Activation
>> d) Input
>
>> [!example] Group B
>> n) Dendrite receiving signals
>> o) Synaptic strength
>> p) Axon firing
>> q) Cell body processing
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> p)
>> d) -> n)

> [!question] Match the concept with its mathematical expression.
>> [!example] Group A
>> a) Perceptron output
>> b) Chain Rule
>> c) Weight update
>
>> [!example] Group B
>> n) f'(g(x)) * g'(x)
>> o) activation(w^T * x + b)
>> p) w = w + alpha * (y - y_hat) * x
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the term with its definition.
>> [!example] Group A
>> a) Linearly separable
>> b) Non-linearly separable
>> c) Decision boundary
>
>> [!example] Group B
>> n) Data that cannot be separated by a single straight line/hyperplane
>> o) The line/hyperplane that separates two classes
>> p) Data that can be separated by a single straight line/hyperplane
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the activation function with its output type.
>> [!example] Group A
>> a) Step (Heaviside)
>> b) Sigmoid
>> c) ReLU
>
>> [!example] Group B
>> n) Continuous value in (0, 1)
>> o) 0 or 1 (binary)
>> p) Continuous value in [0, +inf)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the historical event with its year.
>> [!example] Group A
>> a) Perceptron invented
>> b) Minsky & Papert prove XOR limitation
>
>> [!example] Group B
>> n) 1969
>> o) 1958
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the gradient computation with the method.
>> [!example] Group A
>> a) Single Perceptron
>> b) Multi-layer network
>
>> [!example] Group B
>> n) Chain Rule extended backward across multiple layers (backpropagation)
>> o) Direct derivative of loss with respect to weights
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
