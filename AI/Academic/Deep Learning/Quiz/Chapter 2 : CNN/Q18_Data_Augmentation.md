---
sources:
  - "[[18. Data Augmentation]]"
---
> [!question] Data augmentation is the practice of artificially expanding a training dataset by applying transformations to existing training images.
>> [!success]- Answer
>> True

> [!question] A CNN has an innate understanding of the physical world and knows that a cat is still a cat when viewed from a different angle.
>> [!success]- Answer
>> False

> [!question] Data augmentation can provide gains comparable to collecting substantially more training data at essentially zero cost.
>> [!success]- Answer
>> True

> [!question] Horizontal flip augmentation teaches a CNN about translation invariance.
>> [!success]- Answer
>> False

> [!question] Color jitter augmentation teaches photometric invariance.
>> [!success]- Answer
>> True

> [!question] Collecting more data is generally cheaper and easier than implementing data augmentation.
>> [!success]- Answer
>> False

> [!question] Data augmentation is only necessary when the training dataset is extremely small.
>> [!success]- Answer
>> False

> [!question] Random crop augmentation teaches a CNN about horizontal invariance.
>> [!success]- Answer
>> False

> [!question] Modern convolutional architectures typically have fewer parameters than traditional neural networks.
>> [!success]- Answer
>> False

> [!question] Data augmentation requires substantial additional disk storage for the transformed images.
>> [!success]- Answer
>> False

> [!question] Which of the following is NOT a compelling reason why data augmentation is necessary in practice?
> a) CNNs are data-hungry
> b) Collecting more data is expensive
> c) Real-world data is diverse
> d) CNNs cannot learn without data augmentation
>> [!success]- Answer
>> d) CNNs cannot learn without data augmentation

> [!question] What does data augmentation teach a CNN?
> a) The physical properties of objects
> b) Invariance properties
> c) How to label new images
> d) How to reduce model size
>> [!success]- Answer
>> b) Invariance properties

> [!question] Which augmentation technique teaches horizontal invariance?
> a) Random crop
> b) Color jitter
> c) Horizontal flip
> d) Rotation
>> [!success]- Answer
>> c) Horizontal flip

> [!question] What does random crop augmentation teach a CNN?
> a) Photometric invariance
> b) Translation invariance
> c) Scale invariance
> d) Rotation invariance
>> [!success]- Answer
>> b) Translation invariance

> [!question] Compared to collecting and labeling new images, data augmentation is:
> a) More expensive
> b) About the same cost
> c) Essentially free
> d) More time-consuming
>> [!success]- Answer
>> c) Essentially free

> [!question] What is a major benefit of data augmentation mentioned in the text?
> a) It reduces model complexity
> b) It improves validation accuracy by 2-5 percentage points
> c) It eliminates the need for human annotators
> d) It reduces computational requirements
>> [!success]- Answer
>> b) It improves validation accuracy by 2-5 percentage points

> [!question] Which of the following is NOT a geometric transformation commonly used in data augmentation?
> a) Horizontal flip
> b) Color jitter
> c) Random crop
> d) Rotation
>> [!success]- Answer
>> b) Color jitter

> [!question] How do CNNs process images?
> a) As three-dimensional objects
> b) As arrays of pixel values
> c) With inherent understanding of physics
> d) With common sense about object behavior
>> [!success]- Answer
>> b) As arrays of pixel values

> [!question] What is the primary purpose of data augmentation?
> a) To reduce the size of the training dataset
> b) To teach the network specific invariance properties
> c) To replace the need for collecting real data
> d) To increase model complexity
>> [!success]- Answer
>> b) To teach the network specific invariance properties

> [!question] Match the augmentation technique with the type of invariance it teaches.
>> [!example] Group A
>> a) Horizontal flip
>> b) Random crop
>> c) Color jitter
>
>> [!example] Group B
>> n) Translation invariance
>> o) Photometric invariance
>> p) Horizontal invariance
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the statements with the corresponding concepts.
>> [!example] Group A
>> a) CNN has no concept of 3D space
>> b) Data augmentation is essentially free
>> c) CNNs are data-hungry
>
>> [!example] Group B
>> n) Requires millions of parameters
>> o) Processes images as pixel arrays
>> p) No additional disk storage needed
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the statements with the reasons for data augmentation necessity.
>> [!example] Group A
>> a) CNNs have millions of parameters
>> b) Real-world data is diverse
>> c) Collecting images requires expensive equipment
>
>> [!example] Group B
>> n) Models overfit with insufficient data
>> o) Simulates variations not in training set
>> p) High cost and effort of new data
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the statements with the corresponding properties of CNNs.
>> [!example] Group A
>> a) No notion of object permanence
>> b) No common sense about object behavior
>> c) No understanding of gravity
>
>> [!example] Group B
>> n) Cannot track objects across views
>> o) Cannot predict object interactions
>> p) Cannot interpret spatial relationships
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the statements with the implications of data augmentation.
>> [!example] Group A
>> a) Horizontal flip augmentation
>> b) Random crop augmentation
>> c) Color jitter augmentation
>
>> [!example] Group B
>> n) Object preserved under left-right reflection
>> o) Object preserved under brightness changes
>> p) Object preserved when not centered
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the statements with the corresponding aspects of data augmentation.
>> [!example] Group A
>> a) Geometric transformations
>> b) CNNs have no concept of physical reality
>> c) Data augmentation provides benefits without new data collection
>
>> [!example] Group B
>> n) Modifies spatial arrangement of pixels
>> o) Requires learning from data alone
>> p) Simulates real-world variations
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the statements with the corresponding characteristics of CNNs.
>> [!example] Group A
>> a) Upright cat and flipped cat are different patterns
>> b) CNN processes images as arrays
>> c) CNN must learn from data alone
>
>> [!example] Group B
>> n) No inherent understanding of transformations
>> o) No concept of semantic categories
>> p) Different from human vision
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the statements with the corresponding aspects of data augmentation philosophy.
>> [!example] Group A
>> a) Each transformation teaches a specific invariance
>> b) CNN has no lifetime of experience
>> c) Augmentation encodes prior knowledge
>
>> [!example] Group B
>> n) Different from human learning
>> o) About physical world properties
>> p) Not just adding variety
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the statements with the corresponding data augmentation benefits.
>> [!example] Group A
>> a) Improves validation accuracy
>> b) Requires few lines of code
>> c) No additional disk storage
>
>> [!example] Group B
>> n) On-the-fly transformations
>> o) 2-5 percentage points gain
>> p) Small computation increase
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)
