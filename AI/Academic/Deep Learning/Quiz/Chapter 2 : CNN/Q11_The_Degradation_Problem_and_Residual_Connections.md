---
sources:
  - "[[11. The Degradation Problem and Residual Connections]]"
---
> [!question] According to the identity mapping argument, deeper networks should perform at least as well as shallower networks because the extra layers can learn to pass their input through unchanged.
>> [!success]- Answer
>> True

> [!question] The degradation problem refers to the observation that deeper networks converge to solutions with higher test error than their shallower counterparts, while having lower training error.
>> [!success]- Answer
>> False

> [!question] When comparing a 20-layer network to a 56-layer network on CIFAR-10, the 56-layer network had higher training error than the 20-layer network.
>> [!success]- Answer
>> True

> [!question] The degradation problem is fundamentally the same as the vanishing gradient problem, which occurs when gradients diminish as they propagate backwards through many layers.
>> [!success]- Answer
>> False

> [!question] The identity mapping argument states that a deeper network with L+K layers should perform at least as well as a shallower network with L layers because the extra K layers can learn to do nothing.
>> [!success]- Answer
>> True

> [!question] In the context of the degradation problem, if a deeper network has higher training error than a shallower network, this is evidence of overfitting.
>> [!success]- Answer
>> False

> [!question] Batch normalization effectively solves the degradation problem by ensuring that activations have roughly unit variance throughout the network.
>> [!success]- Answer
>> False

> [!question] The ReLU activation function makes it difficult for layers to learn identity mappings because it zeroes out all negative values.
>> [!success]- Answer
>> True

> [!question] According to the text, the degradation problem occurs because it is fundamentally difficult for standard optimization algorithms to learn identity mappings through many stacked nonlinear layers.
>> [!success]- Answer
>> True

> [!question] The ResNet solution reformulates the learning problem to have layers learn the desired mapping H(x) directly rather than learning the residual F(x) = H(x) - x.
>> [!success]- Answer
>> False

> [!question] What is the primary theoretical argument that deeper networks should perform at least as well as shallower networks?
> a) Deeper networks have more parameters and can represent more complex functions
> b) The extra layers in deeper networks can learn the identity mapping
> c) Deeper networks benefit from batch normalization
> d) Deeper networks are less prone to vanishing gradients
>> [!success]- Answer
>> b) The extra layers in deeper networks can learn the identity mapping

> [!question] What surprising observation did He et al. make when comparing 20-layer and 56-layer networks on CIFAR-10?
> a) The 56-layer network had lower training error but higher test error
> b) The 56-layer network had higher training error than the 20-layer network
> c) The 56-layer network failed to converge entirely
> d) The 56-layer network showed signs of severe overfitting
>> [!success]- Answer
>> b) The 56-layer network had higher training error than the 20-layer network

> [!question] Why is the degradation problem NOT the same as overfitting?
> a) Because overfitting only occurs in shallow networks
> b) Because overfitting is characterized by low training error and high test error
> c) Because overfitting only happens when batch normalization is not used
> d) Because overfitting is solved by adding more layers to the network
>> [!success]- Answer
>> b) Because overfitting is characterized by low training error and high test error

> [!question] Why does the degradation problem persist even when batch normalization is used?
> a) Batch normalization actually makes the optimization landscape more difficult
> b) Batch normalization only solves vanishing gradients but not the fundamental optimization difficulty
> c) Batch normalization introduces new types of numerical instabilities
> d) Batch normalization is incompatible with deep networks
>> [!success]- Answer
>> b) Batch normalization only solves vanishing gradients but not the fundamental optimization difficulty

> [!question] What makes it difficult for standard optimization algorithms to learn identity mappings through many stacked nonlinear layers?
> a) The gradients become too large and cause exploding gradients
> b) The narrow region in parameter space where identity mappings are representable is hard to find
> c) The ReLU activation function prevents any form of identity mapping
> d) The batch normalization destroys information necessary for identity mappings
>> [!success]- Answer
>> b) The narrow region in parameter space where identity mappings are representable is hard to find

> [!question] What is the core insight behind the ResNet solution to the degradation problem?
> a) Removing batch normalization from deep networks
> b) Reformulating the learning problem to have layers learn residuals rather than direct mappings
> c) Using different activation functions that can represent identity mappings more easily
> d) Limiting the depth of networks to prevent degradation
>> [!success]- Answer
>> b) Reformulating the learning problem to have layers learn residuals rather than direct mappings

> [!question] According to the intuitive analogy provided, why is passing a message through 36 people difficult without degradation?
> a) Each person intentionally modifies the message
> b) Small distortions accumulate across many transformations
> c) The message gets shorter with each person
> d) The people cannot understand the original message
>> [!success]- Answer
>> b) Small distortions accumulate across many transformations

> [!question] What would be the output of a residual block if the layers learn the zero mapping (F(x) = 0)?
> a) The output would be undefined
> b) The output would be x, the original input
> c) The output would be 0
> d) The output would be F(x)
>> [!success]- Answer
>> b) The output would be x, the original input

> [!question] What is the key diagnostic to distinguish the degradation problem from vanishing gradients or overfitting?
> a) The presence of batch normalization in the network
> b) The relationship between training error and test error
> c) The depth of the network relative to the dataset size
> d) The optimizer being used (SGD vs. Adam)
>> [!success]- Answer
>> b) The relationship between training error and test error

> [!question] Match the item with its description.
>> [!example] Group A
>> a) Identity mapping argument
>> b) Degradation problem
>> c) Residual learning
>> d) Vanishing gradients
>
>> [!example] Group B
>> n) The observation that deeper networks converge to solutions with higher training error than shallower networks
>> o) The reformulation where layers learn F(x) = H(x) - x rather than H(x) directly
>> p) The argument that deeper networks should perform at least as well as shallower networks because extra layers can learn to do nothing
>> q) The problem where gradients diminish as they propagate backwards through many layers
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)
>> d) -> q)

> [!question] Match the item with its description.
>> [!example] Group A
>> a) Overfitting
>> b) Batch normalization
>> c) ResNet solution
>> d) ReLU activation
>
>> [!example] Group B
>> n) An activation function that zeroes out negative values, making identity mappings difficult
>> o) The solution to degradation problem that reformulates learning to compute residuals
>> p) A regularization technique characterized by low training error and high test error
>> q) A technique that ensures activations have roughly unit variance to mitigate internal covariate shift
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> o)
>> d) -> n)

> [!question] Match the item with its description.
>> [!example] Group A
>> a) Hypothesis space
>> b) Local minimum
>> c) Parameter space
>> d) Computational graph
>
>> [!example] Group B
>> n) The set of all possible functions a network can represent
>> o) The multidimensional space of all possible parameter values
>> p) A graphical representation of the sequence of operations and computations in a network
>> q) A suboptimal solution in the optimization landscape that the optimizer converges to
>
>> [!success]- Answer
>> a) -> n)
>> b) -> q)
>> c) -> o)
>> d) -> p)

> [!question] Match the item with its description.
>> [!example] Group A
>> a) Internal covariate shift
>> b) SGD optimizer
>> c) CIFAR-10 dataset
>> d) ImageNet dataset
>
>> [!example] Group B
>> n) A popular benchmark dataset for deep learning with 60,000 32x32 color images in 10 classes
>> o) A stochastic optimization algorithm commonly used for training neural networks
>> p) A large-scale visual recognition dataset with over 14 million labeled images
>> q) The phenomenon where the distribution of activations changes during training, affecting gradient flow
>
>> [!success]- Answer
>> a) -> q)
>> b) -> o)
>> c) -> n)
>> d) -> p)

> [!question] Match the item with its description.
>> [!example] Group A
>> a) Residual block
>> b) Main path
>> c) Skip connection
>> d) Residual path
>
>> [!example] Group B
>> n) The connection that passes the input directly to the output of the block
>> o) The sequence of layers that computes F(x) in a residual block
>> p) A building block in ResNet that implements residual learning
>> q) Another name for the residual path in a residual block
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)
>> d) -> q)

> [!question] Match the item with its description.
>> [!example] Group A
>> a) Backpropagation
>> b) Gradient descent
>> c) Learning rate
>> d) Convolution layer
>
>> [!example] Group B
>> n) A hyperparameter that controls the step size during parameter updates
>> o) The algorithm used to compute gradients efficiently in neural networks
>> p) A layer that applies convolution operations to extract features from input
>> q) An optimization algorithm that iteratively moves parameters in the direction of steepest descent
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match the item with its description.
>> [!example] Group A
>> a) Nonlinear transformation
>> b) Information preservation
>> c) Local minimum
>> d) Hypothesis space
>
>> [!example] Group B
>> n) The set of all functions a model can represent
>> o) A transformation that changes the input in a non-linear way
>> p) The maintenance of information through computational steps
>> q) A suboptimal solution in the optimization landscape
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> q)
>> d) -> n)

> [!question] Match the item with its description.
>> [!example] Group A
>> a) AlexNet
>> b) VGG
>> c) Inception
>> d) ResNet
>
>> [!example] Group B
>> n) A network known for its use of residual connections to enable very deep architectures
>> o) A network that introduced the use of small 3x3 filters throughout the architecture
>> p) A network that popularized deep CNNs and used ReLU activations
>> q) A network that uses multi-scale processing with parallel convolutions of different sizes
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> q)
>> d) -> n)

> [!question] Match the item with its description.
>> [!example] Group A
>> a) Training error
>> b) Test error
>> c) Convergence
>> d) Optimization landscape
>
>> [!example] Group B
>> n) The error measured on a held-out dataset not used for training
>> o) The process by which an optimization algorithm approaches a minimum
>> p) The multidimensional surface representing all possible parameter values and their associated loss
>> q) The error measured on the training data during or after training
>
>> [!success]- Answer
>> a) -> q)
>> b) -> n)
>> c) -> o)
>> d) -> p)
