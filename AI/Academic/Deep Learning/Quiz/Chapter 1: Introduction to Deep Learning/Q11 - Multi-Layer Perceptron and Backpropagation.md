---
sources:
  - "[[11. Multi-Layer Perceptron and Backpropagation]]"
---
> [!question] An MLP with at least one hidden layer can approximate any continuous function, including XOR.
>> [!success]- Answer
>> True

> [!question] The input layer in an MLP performs computation on the data.
>> [!success]- Answer
>> False

> [!question] In a Dense/Fully Connected layer, every neuron connects to every neuron in the next layer.
>> [!success]- Answer
>> True

> [!question] Backpropagation specifically refers to the efficient computation of gradients using the chain rule.
>> [!success]- Answer
>> True

> [!question] The number of layers and neurons in an MLP are learned from data during training.
>> [!success]- Answer
>> False

> [!question] Backpropagation reuses intermediate results, making gradient computation roughly the same cost as the forward pass.
>> [!success]- Answer
>> True

> [!question] The vanishing gradient problem occurs because Sigmoid derivatives are smaller than 0.25, causing gradients to shrink across layers.
>> [!success]- Answer
>> True

> [!question] In a 10-layer Sigmoid network, the gradient reaching Layer 1 is about one-millionth of the original signal.
>> [!success]- Answer
>> True

> [!question] The output layer of an MLP for binary classification should have N neurons.
>> [!success]- Answer
>> False

> [!question] In MLP notation, w_{1,2}^{(h)} represents the weight connecting hidden neuron 1 to input 2.
>> [!success]- Answer
>> True

> [!question] What is an MLP (Multi-Layer Perceptron)?
> a) A single-layer neural network
> b) A feedforward neural network with multiple dense layers capable of solving non-linearly separable problems
> c) A decision tree
> d) An SVM variant
>> [!success]- Answer
>> b) A feedforward neural network with multiple dense layers capable of solving non-linearly separable problems

> [!question] What are the 4 steps of training in backpropagation?
> a) Load, Train, Test, Deploy
> b) Forward Pass, Calculate Loss, Backward Pass, Update Weights
> c) Init, Forward, Predict, Save
> d) Read, Process, Output, Close
>> [!success]- Answer
>> b) Forward Pass, Calculate Loss, Backward Pass, Update Weights

> [!question] What happens during the Forward Pass?
> a) Gradients are calculated
> b) Weights are updated
> c) Data flows from input to output to generate a prediction
> d) The loss is minimized
>> [!success]- Answer
>> c) Data flows from input to output to generate a prediction

> [!question] What are hyperparameters in an MLP?
> a) Weights learned during training
> b) Settings chosen before training such as number of layers and neurons
> c) The loss function output
> d) The training data labels
>> [!success]- Answer
>> b) Settings chosen before training such as number of layers and neurons

> [!question] How many weight connections exist between a layer with 100 neurons and a layer with 50 neurons?
> a) 150
> b) 5,000
> c) 50
> d) 100
>> [!success]- Answer
>> b) 5,000

> [!question] What does the weight notation w_{dest,source}^{(layer)} mean?
> a) Weight at layer (layer) connecting source to destination neuron
> b) The bias term
> c) The activation function
> d) The learning rate
>> [!success]- Answer
>> a) Weight at layer (layer) connecting source to destination neuron

> [!question] Why does backpropagation reuse intermediate results?
> a) To save memory only
> b) To make the gradient computation roughly the same cost as the forward pass
> c) To increase accuracy
> d) To add more layers
>> [!success]- Answer
>> b) To make the gradient computation roughly the same cost as the forward pass

> [!question] In a 10-layer network using Sigmoid, approximately what fraction of the gradient reaches Layer 1?
> a) 0.25
> b) 0.5
> c) Approximately 0.00000095 (one-millionth)
> d) 1.0
>> [!success]- Answer
>> c) Approximately 0.00000095 (one-millionth)

> [!question] What is the output layer size for a multi-class classification problem with 5 classes?
> a) 1 neuron
> b) 5 neurons
> c) 10 neurons
> d) 0 neurons
>> [!success]- Answer
>> b) 5 neurons

> [!question] What does 'Dense/Fully Connected' mean in an MLP?
> a) Only some neurons connect to the next layer
> b) Every neuron in one layer connects to every neuron in the next layer
> c) No connections between layers
> d) Only the bias connects
>> [!success]- Answer
>> b) Every neuron in one layer connects to every neuron in the next layer

> [!question] Match the MLP layer with its function.
>> [!example] Group A
>> a) Input Layer
>> b) Hidden Layer
>> c) Output Layer
>
>> [!example] Group B
>> n) Produces the final prediction
>> o) Receives raw data, no computation
>> p) Applies weights, biases, and activations to learn patterns
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the training step with its description.
>> [!example] Group A
>> a) Forward Pass
>> b) Calculate Loss
>> c) Backward Pass
>> d) Update Weights
>
>> [!example] Group B
>> n) Optimizer adjusts weights using gradients to reduce error
>> o) Compare prediction to true target using a loss function
>> p) Compute gradients for every weight using the chain rule
>> q) Data flows through network to generate prediction
>
>> [!success]- Answer
>> a) -> q)
>> b) -> o)
>> c) -> p)
>> d) -> n)

> [!question] Match the notation component with its meaning.
>> [!example] Group A
>> a) a_1^{(h)}
>> b) w_{1,2}^{(h)}
>> c) a_1^{(out)}
>
>> [!example] Group B
>> n) Output layer activation of neuron 1
>> o) Hidden layer activation of neuron 1
>> p) Weight connecting input x_2 to hidden neuron 1
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the problem with the cause.
>> [!example] Group A
>> a) Vanishing Gradient
>> b) XOR not solvable by single Perceptron
>
>> [!example] Group B
>> n) Data is not linearly separable
>> o) Sigmoid derivatives < 0.25 shrink gradients across deep layers
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the layer count with the gradient behavior (using Sigmoid).
>> [!example] Group A
>> a) 1 layer
>> b) 10 layers
>
>> [!example] Group B
>> n) Gradient reduced to ~0.00000095 of original
>> o) Gradient passes through at full strength
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the MLP component with its type.
>> [!example] Group A
>> a) Number of hidden layers
>> b) Weight values
>> c) Biases
>
>> [!example] Group B
>> n) Learned parameter
>> o) Hyperparameter (chosen before training)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> n)

> [!question] Match the output layer configuration with the task.
>> [!example] Group A
>> a) 1 neuron with Sigmoid
>> b) N neurons with Softmax
>> c) 1 neuron with Linear activation
>
>> [!example] Group B
>> n) Multi-class classification
>> o) Regression
>> p) Binary classification
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the backpropagation advantage with the explanation.
>> [!example] Group A
>> a) Reuses intermediate results
>> b) Chain Rule
>
>> [!example] Group B
>> n) Computes gradient of composite functions by multiplying individual derivatives
>> o) Makes gradient computation roughly same cost as forward pass
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the network characteristic with its value.
>> [!example] Group A
>> a) 100 neurons -> 50 neurons (dense)
>> b) Input layer computation
>
>> [!example] Group B
>> n) None — just passes values forward
>> o) 5,000 weight connections + 50 biases
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)

> [!question] Match the gradient problem with the solution.
>> [!example] Group A
>> a) Vanishing Gradient (Sigmoid)
>> b) XOR not solvable by Perceptron
>
>> [!example] Group B
>> n) Use MLP with at least one hidden layer
>> o) Use ReLU activation instead of Sigmoid
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
