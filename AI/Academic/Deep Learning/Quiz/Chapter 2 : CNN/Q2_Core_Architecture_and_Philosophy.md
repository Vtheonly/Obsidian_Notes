---
sources:
  - "[[2. Core Architecture and Philosophy]]"
---
> [!question] Every Convolutional Neural Network is organized into two fundamentally distinct functional parts: the Front-End and the Back-End.
>> [!success]- Answer
>> True

> [!question] The front-end of a CNN is responsible for performing the actual classification in the learned representation space.
>> [!success]- Answer
>> False

> [!question] The hierarchy of features in CNNs emerges automatically from the training process and architectural constraints.
>> [!success]- Answer
>> True

> [!question] Low-level features in CNNs are highly specific to the training dataset and vary significantly across different models.
>> [!success]- Answer
>> False

> [!question] ReLU introduces non-linearity to the network and sparsifies the feature map by setting negative values to zero.
>> [!success]- Answer
>> True

> [!question] The order of operations in CNN blocks is always Pool → Conv → ReLU to ensure optimal feature extraction.
>> [!success]- Answer
>> False

> [!question] High-level features in CNNs are the most task-specific and are heavily influenced by the training dataset.
>> [!success]- Answer
>> True

> [!question] Mid-level features in CNNs combine low-level edges and textures into larger patterns that represent object parts and simple shapes.
>> [!success]- Answer
>> True

> [!question] Pooling operations reduce spatial dimensions but increase the computational cost for subsequent layers.
>> [!success]- Answer
>> False

> [!question] The fundamental insight behind the two-part CNN design is that visual recognition cannot be meaningfully decomposed into sub-problems.
>> [!success]- Answer
>> False

> [!question] What is the primary function of the front-end in a CNN?
> a) Classifying input images into categories
> b) Extracting progressively more abstract features from raw pixels
> c) Reducing the spatial dimensions of input images
> d) Initializing the weights of the network
>> [!success]- Answer
>> b) Extracting progressively more abstract features from raw pixels

> [!question] Which of the following is NOT a typical characteristic of low-level features in CNNs?
> a) They detect simple, local features like edges and color gradients
> b) They are highly generic and useful for virtually any visual task
> c) They represent entire object categories and semantic attributes
> d) They are nearly identical across CNNs trained on different datasets
>> [!success]- Answer
>> c) They represent entire object categories and semantic attributes

> [!question] What is the main purpose of the ReLU activation function in a CNN?
> a) To reduce spatial dimensions of feature maps
> b) To introduce non-linearity and sparsify feature maps
> c) To combine multiple feature maps into one
> d) To normalize the input data
>> [!success]- Answer
>> b) To introduce non-linearity and sparsify feature maps

> [!question] Which of the following best describes the relationship between low-level, mid-level, and high-level features in CNNs?
> a) They are independent of each other and serve different purposes
> b) Mid-level features are more universal than low-level features
> c) High-level features are built upon mid-level features, which are built upon low-level features
> d) All feature levels are learned simultaneously during training
>> [!success]- Answer
>> c) High-level features are built upon mid-level features, which are built upon low-level features

> [!question] What is the primary purpose of pooling operations in CNNs?
> a) To increase the spatial resolution of feature maps
> b) To introduce non-linearity into the network
> c) To reduce computational cost and provide translation invariance
> d) To initialize the weights of the network
>> [!success]- Answer
>> c) To reduce computational cost and provide translation invariance

> [!question] Why is the order of operations in CNN blocks typically Conv → ReLU → Pool?
> a) This order minimizes computational complexity
> b) This order ensures that pooling selects from non-negative activations meaningful for feature detection
> c) This order is arbitrary and any sequence would produce similar results
> d) This order maximizes the number of parameters in the network
>> [!success]- Answer
>> b) This order ensures that pooling selects from non-negative activations meaningful for feature detection

> [!question] Which of the following statements about the back-end of a CNN is most accurate?
> a) It consists of convolutional layers that detect features in the input
> b) It maps high-level features extracted by the front-end to output categories
> c) It is responsible for reducing the spatial dimensions of the input
> d) It uses pooling operations to introduce non-linearity
>> [!success]- Answer
>> b) It maps high-level features extracted by the front-end to output categories

> [!question] What makes transfer learning effective in CNNs?
> a) The high-level features learned on one dataset are universally applicable to all tasks
> b) The low-level features learned on one dataset are just as useful for different domains
> c) The entire network architecture needs to be redesigned for each new task
> d) The pooling operations are task-specific and must be retrained
>> [!success]- Answer
>> b) The low-level features learned on one dataset are just as useful for different domains

> [!question] Which of the following is NOT a typical characteristic of high-level features in CNNs?
> a) They are highly abstract and semantically meaningful
> b) They encode entire object parts and object categories
> c) They are the most universal across different training datasets
> d) They are heavily influenced by the specific classes the model was trained to recognize
>> [!success]- Answer
>> c) They are the most universal across different training datasets

> [!question] Match the item with its description.
>> [!example] Group A
>> a) Low-level features
>> b) Mid-level features
>> c) High-level features
>> d) Convolution operation
>
>> [!example] Group B
>> n) Combines edges and textures into object parts and simple shapes
>> o) Detects simple, local features like edges and color gradients
>> p) Maps high-level features to output categories
>> q) Learns highly abstract and semantically meaningful representations
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> q)
>> d) -> p)

> [!question] Match the item with its description.
>> [!example] Group A
>> a) ReLU activation
>> b) Pooling operation
>> c) Convolution operation
>> d) Fully connected layer
>
>> [!example] Group B
>> n) Reduces spatial dimensions and provides translation invariance
>> o) Extracts local patterns from input feature maps
>> p) Maps features to output categories in the back-end
>> q) Introduces non-linearity and sparsifies feature maps
>
>> [!success]- Answer
>> a) -> q)
>> b) -> n)
>> c) -> o)
>> d) -> p)

> [!question] Match the item with its description.
>> [!example] Group A
>> a) Front-end
>> b) Back-end
>> c) Transfer learning
>> d) Feature hierarchy
>
>> [!example] Group B
>> n) Decomposes visual recognition into feature extraction and classification
>> o) Builds more abstract representations from simpler ones across layers
>> p) Uses knowledge from one task to improve performance on another
>> q) Maps high-level features to output categories
>
>> [!success]- Answer
>> a) -> n)
>> b) -> q)
>> c) -> p)
>> d) -> o)

> [!question] Match the item with its description.
>> [!example] Group A
>> a) Gabor-like filters
>> b) Object parts
>> c) Semantic attributes
>> d) Simple shapes
>
>> [!example] Group B
>> n) Complex features like a dog's snout or car wheel assembly
>> o) Basic geometric forms like circles, rectangles, triangles
>> p) Filters that detect edges at various orientations
>> q) Properties like "furry" or "metallic"
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)

> [!question] Match the item with its description.
>> [!example] Group A
>> a) Translation invariance
>> b) Weight sharing
>> c) Sparse coding
>> d) Feature sparsity
>
>> [!example] Group B
>> n) Same filter applied at every location in the input
>> o) Setting negative values to zero in feature maps
>> p) Algorithm that learns filters similar to CNNs
>> q) Robustness to small spatial shifts in input
>
>> [!success]- Answer
>> a) -> q)
>> b) -> n)
>> c) -> p)
>> d) -> o)

> [!question] Match the item with its description.
>> [!example] Group A
>> a) Early layers
>> b) Middle layers
>> c) Late layers
>> d) Output layer
>
>> [!example] Group B
>> n) Learn features that are highly abstract and semantically meaningful
>> o) Detect simple, local features like edges and color gradients
>> p) Combine mid-level patterns into representations encoding object categories
>> q) Use softmax to produce class probabilities
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
>> d) -> q)

> [!question] Match the item with its description.
>> [!example] Group A
>> a) Max pooling
>> b) Average pooling
>> c) Strided convolution
>> d) Dilated convolution
>
>> [!example] Group B
>> n) Reduces spatial dimensions by taking maximum values in regions
>> o) Expands receptive field without increasing parameters
>> p) Reduces spatial dimensions by averaging values in regions
>> q) Moves filter by multiple pixels at each step
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> q)
>> d) -> o)

> [!question] Match the item with its description.
>> [!example] Group A
>> a) Hubel and Wiesel cells
>> b) CNN front-end
>> c) CNN back-end
>> d) Visual cortex
>
>> [!example] Group B
>> n) Analogous to how humans process visual information
>> o) Detects simple features like oriented edges
>> p) Transforms pixels into abstract feature representations
>> q) Maps features to desired output categories
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> q)
>> d) -> n)

> [!question] Match the item with its description.
>> [!example] Group A
>> a) Receptive field
>> b) Activation map
>> c) Feature map
>> d) Pooling stride
>
>> [!example] Group B
>> n) Indicates where a pattern was detected in the input
>> o) The area of the input that a neuron "sees"
>> p) The distance between pooling operations
>> q) Output after applying non-linear activation to feature map
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)
