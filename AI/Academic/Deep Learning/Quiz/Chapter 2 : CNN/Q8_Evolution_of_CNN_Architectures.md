---
sources:
  - "[[8. Evolution of CNN Architectures]]"
---
> [!question] LeNet-5 was the first convolutional neural network to demonstrate that learned features could outperform hand-crafted feature pipelines.
>> [!success]- Answer
>> True

> [!question] LeNet-5 used max pooling for its subsampling layers.
>> [!success]- Answer
>> False

> [!question] AlexNet achieved a top-5 error rate of approximately 15.3% on ImageNet, which was an improvement of about 10.8 percentage points over the runner-up.
>> [!success]- Answer
>> True

> [!question] LeNet-5 used ReLU activation functions, which helped solve the vanishing gradient problem.
>> [!success]- Answer
>> False

> [!question] Local Response Normalization (LRN) is still widely used in modern CNN architectures as an effective normalization technique.
>> [!success]- Answer
>> False

> [!question] AlexNet employed dropout with p=0.5 in its first two fully connected layers to prevent overfitting.
>> [!success]- Answer
>> True

> [!question] VGG-16 standardized on using only 3×3 convolutions, motivated by the receptive field argument where two 3×3 convolutions have a larger effective receptive field than a single 5×5 convolution.
>> [!success]- Answer
>> True

> [!question] The GoogLeNet (Inception) module used multiple filter sizes in parallel and concatenated their outputs, significantly increasing computational efficiency.
>> [!success]- Answer
>> True

> [!question] Batch Normalization normalizes across the channel dimension rather than the batch dimension, making it strictly superior to Local Response Normalization.
>> [!success]- Answer
>> False

> [!question] ResNet introduced skip connections to explicitly address the vanishing gradient problem in deep networks, allowing for the training of networks with hundreds of layers.
>> [!success]- Answer
>> True

> [!question] Which of the following CNN architectures was the first to demonstrate that deep learning could dominate large-scale visual recognition tasks?
> a) LeNet-5
> b) AlexNet
> c) VGG-16
> d) GoogLeNet
>> [!success]- Answer
>> b) AlexNet

> [!question] Which activation function did AlexNet introduce that helped solve the vanishing gradient problem for positive inputs?
> a) Sigmoid
> b) Tanh
> c) ReLU
> d) Leaky ReLU
>> [!success]- Answer
>> c) ReLU

> [!question] What was the primary limitation of LeNet-5 that made it inadequate for complex, high-resolution natural images?
> a) Use of average pooling instead of max pooling
> b) Small model size with only ~60K parameters
> c) Use of sigmoid/tanh activations
> d) Lack of data augmentation
>> [!success]- Answer
>> b) Small model size with only ~60K parameters

> [!question] Which regularization technique did AlexNet employ to combat overfitting given its large number of parameters (~61 million)?
> a) Weight decay
> b) Data augmentation
> c) Dropout
> d) Both b and c
>> [!success]- Answer
>> d) Both b and c

> [!question] What was the key design philosophy of VGG-16?
> a) Use large filter sizes to capture more features
> b) Use only 3×3 convolutions and stack them deeply
> c) Use skip connections to enable very deep networks
> d) Use multiple parallel filter sizes in each layer
>> [!success]- Answer
>> b) Use only 3×3 convolutions and stack them deeply

> [!question] Which of the following is NOT true about AlexNet's innovations?
> a) It used overlapping max pooling
> b) It introduced Local Response Normalization which is still widely used today
> c) It was trained on GPUs, reducing training time from weeks to days
> d) It used PCA-based color augmentation
>> [!success]- Answer
>> b) It introduced Local Response Normalization which is still widely used today

> [!question] What problem did ResNet's skip connections specifically address?
> a) Overfitting in very deep networks
> b) Computational inefficiency
> c) Network degradation problem where accuracy gets saturated or drops when increasing depth
> d) Vanishing activations in the early layers
>> [!success]- Answer
>> c) Network degradation problem where accuracy gets saturated or drops when increasing depth

> [!question] Which of the following architectures introduced the concept of "Inception modules" that use multiple filter sizes in parallel?
> a) VGG-16
> b) AlexNet
> c) GoogLeNet
> d) ResNet
>> [!success]- Answer
>> c) GoogLeNet

> [!question] What was the primary computational efficiency improvement of the Inception module compared to a standard convolutional layer?
> a) Using smaller filters
> b) Reducing the number of channels
> c) Using 1×1 convolutions to reduce dimensionality before applying larger filters
> d) Using batch normalization to speed up training
>> [!success]- Answer
>> c) Using 1×1 convolutions to reduce dimensionality before applying larger filters

> [!question] Which normalization technique was introduced after AlexNet and is considered strictly superior to Local Response Normalization?
> a) Weight Normalization
> b) Layer Normalization
> c) Batch Normalization
> d) Instance Normalization
>> [!success]- Answer
>> c) Batch Normalization

> [!question] What is the main advantage of using two 3×3 convolutions instead of one 5×5 convolution as done in VGG?
> a) Two 3×3 convolutions have a larger effective receptive field than one 5×5 convolution
> b) Two 3×3 convolutions have fewer parameters than one 5×5 convolution
> c) Two 3×3 convolutions introduce more non-linearity
> d) Two 3×3 convolutions reduce computational cost
>> [!success]- Answer
>> c) Two 3×3 convolutions introduce more non-linearity

> [!question] Match the CNN architecture with its key innovation or characteristic.
>> [!example] Group A
>> a) LeNet-5
>> b) AlexNet
>> c) VGG-16
>> d) GoogLeNet
>> e) ResNet
>
>> [!example] Group B
>> n) First to use ReLU activation and dropout for regularization
>> o) Standardized on 3×3 convolutions and demonstrated that depth matters
>> p) Introduced skip connections to address network degradation
>> q) Proved that learned features could outperform hand-crafted features
>> r) Used Inception modules with multiple parallel filter sizes
>
>> [!success]- Answer
>> a) -> q)
>> b) -> n)
>> c) -> o)
>> d) -> r)
>> e) -> p)

> [!question] Match the architectural component with its primary function.
>> [!example] Group A
>> a) Convolutional layers
>> b) Pooling layers
>> c) Fully connected layers
>> d) Dropout
>> e) Batch Normalization
>
>> [!example] Group B
>> n) Reduces spatial dimensions to decrease computational cost
>> o) Normalizes activations to stabilize and accelerate training
>> p) Extracts features through learned filters
>> q) Prevents overfitting by randomly setting neurons to zero during training
>> r) Maps features to class scores for classification
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> r)
>> d) -> q)
>> e) -> o)

> [!question] Match the architectural challenge with its corresponding solution.
>> [!example] Group A
>> a) Vanishing gradients
>> b) Overfitting
>> c) Network degradation
>> d) Computational efficiency
>> e) Slow training
>
>> [!example] Group B
>> n) Skip connections
>> o) ReLU activation
>> p) Data augmentation
>> q) Inception modules
>> r) GPU acceleration
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
>> d) -> q)
>> e) -> r)

> [!question] Match the historical CNN with its contribution to the field.
>> [!example] Group A
>> a) LeNet-5
>> b) AlexNet
>> c) VGG-16
>> d) GoogLeNet
>> e) ResNet
>
>> [!example] Group B
>> n) Established the fundamental CNN template with alternating convolution and pooling
>> o) Demonstrated deep learning could dominate visual recognition at scale
>> p) Showed that depth alone could improve performance
>> q) Introduced the concept of network-in-network
>> s) Enabled training of very deep networks through skip connections
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
>> e) -> s)

> [!question] Match the pooling type with its characteristic.
>> [!example] Group A
>> a) Max pooling
>> b) Average pooling
>> c) Overlapping pooling
>> d) Global average pooling
>> e) Strided convolution
>
>> [!example] Group B
>> n) Takes the maximum value in each region
>> o) Computes the average of all values in each region
>> p) Uses regions that overlap with adjacent regions
>> q) Computes the average across the entire spatial dimensions
>> r) Reduces spatial dimensions through convolution with stride > 1
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
>> e) -> r)

> [!question] Match the CNN architecture with its approximate number of parameters.
>> [!example] Group A
>> a) LeNet-5
>> b) AlexNet
>> c) VGG-16
>> d) GoogLeNet
>> e) ResNet-50
>
>> [!example] Group B
>> n) ~60,000
>> o) ~61 million
>> p) ~138 million
>> q) ~6.8 million
>> r) ~25.6 million
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
>> e) -> r)

> [!question] Match the normalization technique with its dimension of normalization.
>> [!example] Group A
>> a) Batch Normalization
>> b) Layer Normalization
>> c) Instance Normalization
>> d) Local Response Normalization
>> e) Group Normalization
>
>> [!example] Group B
>> n) Normalizes across the batch dimension
>> o) Normalizes across the feature dimension for each sample
>> p) Normalizes each channel independently
>> q) Normalizes across channels for each sample and position
>> r) Normalizes across a subset of channels for each sample
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
>> e) -> r)

> [!question] Match the CNN component with its effect on network properties.
>> [!example] Group A
>> a) Depth
>> b) Width (number of filters)
>> c) Kernel size
>> d) Stride
>> e) Padding
>
>> [!example] Group B
>> n) Increases receptive field without adding parameters
>> o) Controls the level of spatial downsampling
>> p) Affects the number of learnable features
>> q) Determines how spatial information is preserved
>> r) Impacts the computational cost and receptive field size
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> r)
>> d) -> o)
>> e) -> q)

> [!question] Match the architectural concept with its purpose in CNN design.
>> [!example] Group A
>> a) Receptive field
>> b) Skip connection
>> c) 1×1 convolution
>> d) Bottleneck layer
>> e) Depthwise separable convolution
>
>> [!example] Group B
>> n) Reduces parameters by separating spatial and channel-wise operations
>> o) Captures the region of input that influences a particular feature
>> p) Lowers dimensionality before expensive operations
>> q) Connects non-adjacent layers to preserve gradient flow
>> r) Changes channel dimensions without affecting spatial dimensions
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> r)
>> d) -> p)
>> e) -> n)
