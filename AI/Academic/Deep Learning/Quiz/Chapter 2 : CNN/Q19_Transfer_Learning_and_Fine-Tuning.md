---
sources:
  - "[[19. Transfer Learning and Fine-Tuning]]"
---
> [!question] Transfer Learning is the process of training a deep learning model from scratch on a large dataset.
>> [!success]- Answer
>> False

> [!question] Training a ResNet-50 model on ImageNet typically requires about 8-10 days of continuous training on a modern GPU.
>> [!success]- Answer
>> True

> [!question] Transfer Learning requires more labeled data than training a model from scratch.
>> [!success]- Answer
>> False

> [!question] Transfer Learning leverages pre-trained knowledge to achieve strong performance with less data and compute.
>> [!success]- Answer
>> True

> [!question] Fine-tuning a ResNet-50 on a small dataset typically takes about 30 minutes on a V100 GPU.
>> [!success]- Answer
>> True

> [!question] Training from scratch always results in better performance than Transfer Learning.
>> [!success]- Answer
>> False

> [!question] Transfer Learning works best when the source and target domains are very different.
>> [!success]- Answer
>> False

> [!question] Transfer Learning typically requires more extensive hyperparameter tuning than training from scratch.
>> [!success]- Answer
>> False

> [!question] One of the main advantages of Transfer Learning is that it's accessible to practitioners with limited computational resources.
>> [!success]- Answer
>> True

> [!question] Even when the target domain is radically different from the source domain, Transfer Learning is never beneficial.
>> [!success]- Answer
>> False

> [!question] What is the primary motivation behind using Transfer Learning?
> a) To reduce the computational cost of training
> b) To leverage pre-trained knowledge for new tasks
> c) To increase model complexity
> d) To avoid using labeled data
>> [!success]- Answer
>> b) To leverage pre-trained knowledge for new tasks

> [!question] How does Transfer Learning compare to training from scratch in terms of data requirements?
> a) Transfer Learning requires more data
> b) Training from scratch requires less data
> c) Transfer Learning requires significantly less data
> d) Both approaches require the same amount of data
>> [!success]- Answer
>> c) Transfer Learning requires significantly less data

> [!question] According to the text, what might happen if you unfreeze too many layers with too little data in Transfer Learning?
> a) The model will train faster
> b) The risk of overfitting increases
> c) The model will perform better on the training set
> d) The computational cost will decrease
>> [!success]- Answer
>> b) The risk of overfitting increases

> [!question] Which of the following is NOT a dimension where Transfer Learning and training from scratch differ significantly?
> a) Data required
> b) Model architecture
> c) Training time
> d) Hyperparameter tuning requirements
>> [!success]- Answer
>> b) Model architecture

> [!question] What is the driving analogy used in the text to explain Transfer Learning?
> a) Learning to drive a truck if you already know how to drive a car
> b) Learning to swim after knowing how to run
> c) Learning to speak a new language after learning one
> d) Learning to cook after knowing how to bake
>> [!success]- Answer
>> a) Learning to drive a truck if you already know how to drive a car

> [!question] When might Transfer Learning fail to provide good results?
> a) When the target domain is similar to the source domain
> b) When using a GPU for training
> c) When the source and target domains are radically different
> d) When using a pre-trained model
>> [!success]- Answer
>> c) When the source and target domains are radically different

> [!question] What is typically the main hyperparameter that needs tuning in Transfer Learning?
> a) Batch size
> b) Learning rate
> c) Number of layers
> d) Activation function
>> [!success]- Answer
>> b) Learning rate

> [!question] According to the text, what knowledge does a pre-trained model already possess?
> a) Task-specific knowledge only
> b) Only knowledge about the original training dataset
> c) Knowledge about edges, textures, shapes, and complex object parts
> d) No useful knowledge
>> [!success]- Answer
>> c) Knowledge about edges, textures, shapes, and complex object parts

> [!question] What is one strategy mentioned for when Transfer Learning doesn't work well with radically different domains?
> a) Use a different optimizer
> b) Unfreeze more layers
> c) Reduce the learning rate
> d) Increase the batch size
>> [!success]- Answer
>> b) Unfreeze more layers

> [!question] According to the text, what is almost always worth trying first even when domains are radically different?
> a) Training from scratch
> b) Using a different architecture
> c) Transfer Learning with random initialization
> d) Increasing the dataset size
>> [!success]- Answer
>> c) Transfer Learning with random initialization

> [!question] Match the Transfer Learning strategy with its description.
>> [!example] Strategy 1
>> a) Freezing all pre-trained layers
>> b) Fine-tuning with a few layers unfrozen
>> c) Training from scratch
>
>> [!example] Descriptions
>> n) Used when source and target domains are very different
>> o) Most common approach, preserves pre-trained features while learning task-specific ones
>> p) Used when computational resources are unlimited and data is massive
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the aspect with its characteristic in Transfer Learning.
>> [!example] Aspect
>> a) Data required
>> b) Compute required
>> c) Training time
>
>> [!example] Characteristic
>> n) Hours to a day on a single GPU
>> o) Hundreds to tens of thousands of images
>> p) Days to weeks on multi-GPU setups
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the hierarchical feature learning concept with its description.
>> [!example] Concept
>> a) Low-level features
>> b) Mid-level features
>> c) High-level features
>
>> [!example] Description
>> n) Edges and basic textures
>> o) Complex object parts and configurations
>> p) Shapes and patterns
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the Transfer Learning advantage with its explanation.
>> [!example] Advantage
>> a) Reduced computational cost
>> b) Less data requirement
>> c) Faster development
>
>> [!example] Explanation
>> n) Often under $10 in cloud compute
>> o) Sometimes as few as 100 images per class
>> p) Minutes to hours instead of days to weeks
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the Transfer Learning consideration with its impact.
>> [!example] Consideration
>> a) Domain overlap
>> b) Number of unfrozen layers
>> c) Learning rate
>
>> [!example] Impact
>> n) Higher risk of overfitting if too many layers are unfrozen with little data
>> o) Performance degrades if domains are radically different
>> p) Critical for fine-tuning the new head and optionally for fine-tuned layers
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the Transfer Learning scenario with its recommended approach.
>> [!example] Scenario
>> a) Small dataset, similar domain
>> b) Limited data, different domain
>> c) Massive dataset, specific domain
>
>> [!example] Approach
>> n) Freeze most layers, fine-tune only the final layers
>> o) Train from scratch
>> p) Unfreeze more layers, use aggressive data augmentation
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the model characteristic with its typical value in Transfer Learning.
>> [!example] Characteristic
>> a) Final performance with limited data
>> b) Risk of overfitting
>> c) Hyperparameter tuning requirements
>
>> [!example] Value
>> n) Often matches or exceeds from-scratch training
>> o) Higher if too many layers are unfrozen with little data
>> p) Minimal, usually just learning rate for the new head
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the Transfer Learning element with its role.
>> [!example] Element
>> a) Pre-trained model
>> b) New classification head
>> c) Fine-tuning process
>
>> [!example] Role
>> n) Adapts learned representations to the specific task
>> o) Provides already learned useful representations
>> p) Adjusts model parameters while preserving useful features
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the Transfer Learning challenge with its solution.
>> [!example] Challenge
>> a) Radically different domains
>> b) Limited computational resources
>> c) Small target dataset
>
>> [!example] Solution
>> n) Start with Transfer Learning, unfreeze more layers if needed
>> o) Use freezing strategies and minimal fine-tuning
>> p) Leverage pre-trained features, use data augmentation
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the Transfer Learning concept with its analogy.
>> [!example] Concept
>> a) Feature reuse
>> b) Knowledge transfer
>> c) Domain adaptation
>
>> [!example] Analogy
>> n) Learning to drive a truck after knowing how to drive a car
>> o) Using existing building blocks for new construction
>> p) Adapting communication style for different audiences
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)
