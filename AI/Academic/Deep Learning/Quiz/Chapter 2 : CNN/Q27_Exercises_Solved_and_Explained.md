---
sources:
  - "[[27. Exercises Solved and Explained]]"
---
> [!question] A convolutional layer with 64 filters of size 3x3, stride 1, and padding 1 will maintain the spatial dimensions of a 128x128 input image.
>> [!success]- Answer
>> True

> [!question] In a CNN, the output channels are determined by the number of filters in the convolutional layer.
>> [!success]- Answer
>> True

> [!question] A max pooling layer with 2x2 window size and stride 2 will reduce the spatial dimensions of a 128x128 feature map to 64x64.
>> [!success]- Answer
>> True

> [!question] The floor function in the CNN output dimension formula is necessary because edge pixels that cannot be fully covered by the filter are discarded.
>> [!success]- Answer
>> True

> [!question] Adding padding to a convolutional layer increases the spatial dimensions of the output.
>> [!success]- Answer
>> False

> [!question] Batch normalization is typically applied before the activation function in a convolutional layer.
>> [!success]- Answer
>> True

> [!question] Dropout is applied during training but not during inference in deep learning models.
>> [!success]- Answer
>> True

> [!question] Transfer learning involves using a pre-trained model and fine-tuning it on a new task.
>> [!success]- Answer
>> True

> [!question] In a CNN, the number of parameters in a convolutional layer is determined by the kernel size, input channels, and output channels.
>> [!success]- Answer
>> True

> [!question] When using a stride greater than 1 in a convolutional layer, the output spatial dimensions will increase.
>> [!success]- Answer
>> False

> [!question] What is the output spatial dimension of a convolutional layer with input size 128x128, kernel size 5x5, stride 2, and padding 1?
> a) 64x64
> b) 65x65
> c) 63x63
> d) 62x62
>> [!success]- Answer
>> c) 63x63

> [!question] How many parameters are in a convolutional layer with 32 filters of size 3x3, given 3 input channels?
> a) 288
> b) 96
> c) 864
> d) 32
>> [!success]- Answer
>> b) 96

> [!question] Which pooling operation is most commonly used to reduce spatial dimensions while preserving important features?
> a) Average pooling
> b) Max pooling
> c) Min pooling
> d) Global pooling
>> [!success]- Answer
>> b) Max pooling

> [!question] What is the primary purpose of batch normalization in deep learning?
> a) To reduce overfitting
> b) To normalize the input data
> c) To stabilize and accelerate training
> d) To increase model capacity
>> [!success]- Answer
>> c) To stabilize and accelerate training

> [!question] What is the output shape after applying a 2x2 max pooling with stride 2 to a feature map of size 56x56x64?
> a) 28x28x64
> b) 28x28x32
> c) 56x56x32
> d) 14x14x64
>> [!success]- Answer
>> a) 28x28x64

> [!question] What dropout rate would typically result in removing approximately 50% of neurons during training?
> a) 0.1
> b) 0.3
> c) 0.5
> d) 0.7
>> [!success]- Answer
>> c) 0.5

> [!question] In transfer learning, which part of a pre-trained model is typically fine-tuned?
> a) Only the final classification layer
> b) The entire model
> c) Only the convolutional base
> d) Only the early layers
>> [!success]- Answer
>> a) Only the final classification layer

> [!question] What is the most common mistake when implementing CNNs that leads to dimension mismatches?
> a) Incorrect padding calculation
> b) Forgetting to flatten before fully connected layers
> c) Incorrect stride settings
> d) All of the above
>> [!success]- Answer
>> d) All of the above

> [!question] Which activation function is commonly used in the output layer of a binary classification CNN?
> a) ReLU
> b) Sigmoid
> c) Tanh
> d) Softmax
>> [!success]- Answer
>> b) Sigmoid

> [!question] Match the regularization techniques with their primary purpose.
>> [!example] Regularization Techniques
>> a) Dropout
>> b) Batch Normalization
>> c) Data Augmentation
>
>> [!example] Primary Purpose
>> n) Reduces overfitting by randomly dropping neurons during training
>> o) Normalizes layer inputs to stabilize training
>> p) Increases effective training data through transformations
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the CNN components with their typical order in a layer.
>> [!example] Layer Components
>> a) Convolution
>> b) Activation
>> c) Pooling
>
>> [!example] Typical Order
>> n) Applied first in the sequence
>> o) Applied after convolution
>> p) Applied after activation (when used)
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the pooling types with their characteristics.
>> [!example] Pooling Types
>> a) Max Pooling
>> b) Average Pooling
>> c) Global Pooling
>
>> [!example] Characteristics
>> n) Takes the maximum value in each window
>> o) Takes the average value in each window
>> p) Reduces each feature map to a single value
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the common CNN architectures with their key innovation.
>> [!example] Architectures
>> a) LeNet-5
>> b) AlexNet
>> c) VGGNet
>
>> [!example] Key Innovations
>> n) Pioneered deep CNNs with ReLU and dropout
>> o) Introduced smaller 3x3 filters in deeper networks
>> p) One of the first CNNs for digit recognition
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the optimization algorithms with their key characteristics.
>> [!example] Optimizers
>> a) SGD
>> b) Adam
>> c) RMSprop
>
>> [!example] Characteristics
>> n) Simple but effective with proper learning rate tuning
>> o) Combines momentum and adaptive learning rates
>> p) Adapts learning rates based on moving averages of squared gradients
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the common CNN problems with their solutions.
>> [!example] Problems
>> a) Vanishing gradients
>> b) Exploding gradients
>> c) Overfitting
>
>> [!example] Solutions
>> n) Use ReLU or similar activation functions
>> o) Apply gradient clipping
>> p) Use regularization techniques
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the dimension calculation components with their roles.
>> [!example] Components
>> a) Kernel size (F)
>> b) Padding (P)
>> c) Stride (S)
>
>> [!example] Roles
>> n) Size of the convolutional filter
>> o) Zero-padded pixels around input
>> p) Number of pixels filter moves per step
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the CNN layer types with their functions.
>> [!example] Layer Types
>> a) Convolutional
>> b) Fully Connected
>> c) Flatten
>
>> [!example] Functions
>> n) Extracts features through learned filters
>> o) Converts feature maps to a vector
>> p) Performs final classification/regression
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the transfer learning strategies with their use cases.
>> [!example] Strategies
>> a) Feature Extraction
>> b) Fine-tuning
>> c) Transfer Learning from Scratch
>
>> [!example] Use Cases
>> n) When dataset is very small and similar to pre-trained data
>> o) When dataset is large and different from pre-trained data
>> p) When dataset is large and similar to pre-trained data
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the common activation functions with their properties.
>> [!example] Activation Functions
>> a) ReLU
>> b) Sigmoid
>> c) Tanh
>
>> [!example] Properties
>> n) Outputs between 0 and 1, good for binary classification
>> o) Outputs between -1 and 1, zero-centered
>> p) Simple, efficient, avoids vanishing gradient for positive inputs
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)
