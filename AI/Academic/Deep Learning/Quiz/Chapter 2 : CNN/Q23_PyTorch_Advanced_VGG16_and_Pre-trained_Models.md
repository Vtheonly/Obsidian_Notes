---
sources:
  - "[[23. PyTorch Advanced - VGG16 and Pre-trained Models]]"
---
> [!question] Pre-trained models in PyTorch can be loaded using the torchvision.models module.
>> [!success]- Answer
>> True

> [!question] The weights='DEFAULT' parameter loads random weights instead of pre-trained ones.
>> [!success]- Answer
>> False

> [!question] Batch Normalization layers in VGG16-BN help stabilize and accelerate training.
>> [!success]- Answer
>> True

> [!question] PyTorch caches pre-trained weights in a system-dependent directory, which can be changed using the TORCH_HOME environment variable.
>> [!success]- Answer
>> True

> [!question] When using model.eval(), all layers in the neural network behave exactly the same as during training.
>> [!success]- Answer
>> False

> [!question] The VGG16 architecture was one of the most influential CNN architectures.
>> [!success]- Answer
>> True

> [!question] Using pretrained=True is still the recommended way to load pre-trained weights in PyTorch 2.0+.
>> [!success]- Answer
>> False

> [!question] The ImageNet dataset contains 1.2 million images across 1000 classes.
>> [!success]- Answer
>> True

> [!question] The VGG16-BN weights file is approximately 558 MB in size.
>> [!success]- Answer
>> True

> [!question] When using model.eval(), Dropout layers remain active and continue to randomly drop neurons.
>> [!success]- Answer
>> False

> [!question] What is the recommended way to load pre-trained weights in PyTorch 2.0+?
> a) pretrained=True
> b) weights='DEFAULT'
> c) weights='IMAGENET'
> d) load_weights=True
>> [!success]- Answer
>> b) weights='DEFAULT'

> [!question] What does the Batch Normalization layer in VGG16-BN do?
> a) Reduces the number of parameters in the model
> b) Normalizes the activations after each convolution to stabilize and accelerate training
> c) Prevents overfitting by randomly dropping neurons
> d) Compresses the model size for faster inference
>> [!success]- Answer
>> b) Normalizes the activations after each convolution to stabilize and accelerate training

> [!question] Where are pre-trained weights cached on a Linux system?
> a) /usr/local/lib/python3.x/site-packages/torch/weights
> b) ~/.cache/torch/hub/checkpoints/
> c) /tmp/pytorch_weights
> d) /var/lib/torch/weights
>> [!success]- Answer
>> b) ~/.cache/torch/hub/checkpoints/

> [!question] What happens when you set weights=None when loading a VGG16-BN model?
> a) It loads the best available pre-trained weights
> b) It loads weights trained on a different dataset
> c) It loads the architecture with random weights
> d) It raises an error
>> [!success]- Answer
>> c) It loads the architecture with random weights

> [!question] Why is model.eval() important when using a pre-trained model for inference?
> a) It enables gradient computation for fine-tuning
> b) It ensures consistent behavior by turning off layers like Dropout and BatchNorm
> c) It increases the model's accuracy
> d) It reduces the model's memory footprint
>> [!success]- Answer
>> b) It ensures consistent behavior by turning off layers like Dropout and BatchNorm

> [!question] What does the VGG16_BN_Weights.IMAGENET1K_V1 specify?
> a) The model should be trained on ImageNet with 1K classes, version 1 weights
> b) The model should use 1K batch normalization layers
> c) The model is designed for images of size 1K x 1K pixels
> d) The model uses version 1 of the VGG architecture
>> [!success]- Answer
>> a) The model should be trained on ImageNet with 1K classes, version 1 weights

> [!question] Which of the following is NOT a benefit of using pre-trained models?
> a) Saves training time and computational resources
> b) Provides better performance with limited data
> c) Guarantees optimal performance for any task
> d) Leverages features learned from large datasets
>> [!success]- Answer
>> c) Guarantees optimal performance for any task

> [!question] What is the purpose of the torchvision.models module?
> a) To visualize neural network architectures
> b) To provide pre-built implementations of famous architectures with pre-trained weights
> c) To optimize neural network models for deployment
> d) To create custom neural network layers
>> [!success]- Answer
>> b) To provide pre-built implementations of famous architectures with pre-trained weights

> [!question] Match the weight loading methods with their descriptions.
>> [!example] Methods
>> a) weights='DEFAULT'
>> b) weights=None
>> c) weights=VGG16_BN_Weights.IMAGENET1K_V1
>
>> [!example] Descriptions
>> n) Loads the architecture with random weights
>> o) Loads the best available pre-trained weights
>> p) Specifies the exact weight version for reproducibility
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the layers with their behavior during model.eval().
>> [!example] Layers
>> a) Dropout
>> b) BatchNorm
>> c) Conv2d
>
>> [!example] Behavior
>> n) Uses running statistics instead of batch statistics
>> o) Always active and computes the same output for the same input
>> p) Randomly drops neurons during training but is disabled during eval
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the components of the VGG16 architecture with their descriptions.
>> [!example] Components
>> a) Convolutional layers
>> b) Fully connected layers
>> c) Max pooling layers
>
>> [!example] Descriptions
>> n) Reduce spatial dimensions of feature maps
>> o) Extract features from input images
>> p) Perform final classification based on extracted features
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the PyTorch model loading methods with their appropriate use cases.
>> [!example] Methods
>> a) weights='DEFAULT'
>> b) weights=None
>> c) weights=VGG16_BN_Weights.IMAGENET1K_V1
>
>> [!example] Use Cases
>> n) When you need to reproduce a specific version of a pre-trained model
>> o) When you want to transfer learning to a new but related task
>> p) When you want to train a model from scratch on a completely different dataset
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the terms with their definitions in the context of pre-trained models.
>> [!example] Terms
>> a) Transfer learning
>> b) Fine-tuning
>> c) Feature extraction
>
>> [!example] Definitions
>> n) Using a pre-trained model as a fixed feature extractor and only training the classifier
>> o) Adapting a pre-trained model to a new task by training both the feature extractor and classifier
>> p) Leveraging knowledge gained from solving one problem to solve a different but related problem
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the model evaluation scenarios with the appropriate model state.
>> [!example] Scenarios
>> a) Training a model from scratch
>> b) Performing inference on a pre-trained model
>> c) Fine-tuning a pre-trained model on a new dataset
>
>> [!example] Model States
>> n) model.train()
>> o) model.eval()
>> p) Depends on the specific part of the code
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the PyTorch model attributes with their purposes.
>> [!example] Attributes
>> a) model.features
>> b) model.avgpool
>> c) model.classifier
>
>> [!example] Purposes
>> n) Contains the final classification layers
>> o) Contains the convolutional and pooling layers
>> p) Contains the average pooling layer that reduces spatial dimensions
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the weight specification methods with their characteristics.
>> [!example] Methods
>> a) weights='DEFAULT'
>> b) weights=None
>> c) Using explicit weight enums
>
>> [!example] Characteristics
>> n) Loads random initialization for training from scratch
>> o) Provides reproducibility by specifying exact weight versions
>> p) Uses the best available weights without specifying exact version
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the layers with their impact on model behavior during inference.
>> [!example] Layers
>> a) Dropout
>> b) BatchNorm
>> c) ReLU
>
>> [!example] Impact
>> n) Behaves consistently during inference without randomness
>> o) Can produce different outputs for the same input if not handled properly
>> p) Always applies the same non-linear transformation
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the model loading options with their memory requirements.
>> [!example] Options
>> a) VGG16 without BatchNorm
>> b) VGG16 with BatchNorm
>> c) VGG19 with BatchNorm
>
>> [!example] Memory Requirements
>> n) Largest file size due to more parameters and additional BatchNorm parameters
>> o) Smaller file size compared to VGG19-BN
>> p) Larger file size compared to VGG16 without BatchNorm due to additional BatchNorm parameters
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
