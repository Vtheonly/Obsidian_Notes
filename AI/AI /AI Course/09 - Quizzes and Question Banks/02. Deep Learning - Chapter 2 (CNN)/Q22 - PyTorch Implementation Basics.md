---
sources:
  - "[[22. PyTorch Implementation Basics]]"
---
> [!question] PyTorch provides tensor data structures similar to NumPy arrays but with GPU support.
>> [!success]- Answer
>> True

> [!question] The torch.nn module contains all standard layer types like Conv2d, Linear, and MaxPool2d.
>> [!success]- Answer
>> True

> [!question] DataLoader is used directly for iterating over datasets without any additional functionality.
>> [!success]- Answer
>> False

> [!question] The torchvision.datasets module contains pre-built dataset classes for common benchmarks like MNIST and CIFAR-10.
>> [!success]- Answer
>> True

> [!question] PyTorch separates model definition from optimization strategy to enforce a clean separation of concerns.
>> [!success]- Answer
>> True

> [!question] MNIST consists of color images of handwritten digits.
>> [!success]- Answer
>> False

> [!question] The torch.optim module contains optimizer classes like SGD, Adam, and RMSprop.
>> [!success]- Answer
>> True

> [!question] Transforms are applied to each sample as it is loaded, enabling on-the-fly data augmentation.
>> [!success]- Answer
>> True

> [!question] DataLoader wraps a Dataset and provides automatic batching, shuffling, and parallel loading.
>> [!success]- Answer
>> True

> [!question] PyTorch tensors do not support GPU acceleration.
>> [!success]- Answer
>> False

> [!question] What is the primary purpose of the torch.nn module?
> a) GPU acceleration
> b) Neural network layers and base classes
> c) Optimization algorithms
> d) Data loading and preprocessing
>> [!success]- Answer
>> b) Neural network layers and base classes

> [!question] Which of the following is NOT a benefit of using DataLoader?
> a) Automatic batching
> b) Direct dataset iteration without any wrapper
> c) Shuffling
> d) Parallel loading
>> [!success]- Answer
>> b) Direct dataset iteration without any wrapper

> [!question] What does the torchvision.datasets module primarily provide?
> a) Image transformation pipelines
> b) Pre-built dataset classes for common benchmarks
> c) Optimizer implementations
> d) Neural network layer definitions
>> [!success]- Answer
>> b) Pre-built dataset classes for common benchmarks

> [!question] Which optimizer uses adaptive learning rates?
> a) SGD
> b) RMSprop
> c) Adam
> d) Both b and c
>> [!success]- Answer
>> d) Both b and c

> [!question] What is the purpose of transforms in PyTorch?
> a) To optimize model parameters
> b) To define neural network architectures
> c) To apply image transformations as data is loaded
> d) To compute gradients
>> [!success]- Answer
>> c) To apply image transformations as data is loaded

> [!question] Why does PyTorch separate nn and optim modules?
> a) To reduce memory usage
> b) To enforce separation of concerns and allow swapping components
> c) To improve training speed
> d) To simplify the API
>> [!success]- Answer
>> b) To enforce separation of concerns and allow swapping components

> [!question] What does the torch.utils.data.DataLoader provide?
> a) Only automatic batching
> b) Wraps a Dataset and provides batching, shuffling, and parallel loading
> c) Only shuffling functionality
> d) Direct access to individual samples
>> [!success]- Answer
>> b) Wraps a Dataset and provides batching, shuffling, and parallel loading

> [!question] Which of the following is NOT a common dataset available in torchvision?
> a) MNIST
> b) CIFAR-10
> c) ImageNet
> d) Handwritten Digits
>> [!success]- Answer
>> d) Handwritten Digits

> [!question] What is the primary function of torch.autograd?
> a) To define neural network architectures
> b) To compute gradients automatically
> c) To load datasets
> d) To optimize model parameters
>> [!success]- Answer
>> b) To compute gradients automatically

