---
sources:
  - "[[24. The Full Training Pipeline End-to-End Checklist]]"
---
> [!question] Data inspection should be performed before writing any model code.
>> [!success]- Answer
>> True

> [!question] In the provided code, class imbalance is detected when the imbalance ratio exceeds:
>> [!success]- Answer
>> 3

> [!question] The code uses Path from pathlib instead of os.path because:
>> a) It provides more functionality
>> b) It's more cross-platform compatible
>> c) It's faster for file operations
>> d) It automatically handles image files
>> [!success]- Answer
>> b) It's more cross-platform compatible

> [!question] Match items.
>> [!example] Phase 1 Components
>> a) Data Preparation
>> b) Model Construction
>> c) Training Configuration
>
>> [!example] Key Activities
>> n) Define or Load Architecture
>> o) Gather & Inspect Dataset
>> p) Loss Function Selection
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] The training pipeline consists of exactly 5 phases.
>> [!success]- Answer
>> True

> [!question] In the provided code, how does the code check for corrupted files?
>> a) By checking file extensions
>> b) By using try/except blocks
>> c) By verifying file size
>> d) By checking image metadata
>> [!success]- Answer
>> b) By using try/except blocks

> [!question] Class imbalance warnings are triggered when the max/min ratio exceeds 3.
>> [!success]- Answer
>> True

> [!question] Match items.
>> [!example] Pipeline Phase 2
>> a) Define or Load Architecture
>> b) Verify with Dummy Input
>> c) Count Parameters
>
>> [!example] Purpose
>> n) Ensure model can process input
>> o) Track model complexity
>> p) Select appropriate model structure
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] The code uses PIL to:
>> a) Perform image transformations
>> b) Check for corrupted files
>> c) Calculate class distributions
>> d) Create data loaders
>> [!success]- Answer
>> b) Check for corrupted files

> [!question] ImageFolder convention assumes that class labels are:
>> [!success]- Answer
>> Directory names

> [!question] The training pipeline should always be followed in the exact order presented.
>> [!success]- Answer
>> True

> [!question] In Phase 3, which component is responsible for adjusting learning rates during training?
>> a) Loss Function
>> b) Optimizer
>> c) LR Scheduler
>> d) Model Architecture
>> [!success]- Answer
>> c) LR Scheduler

> [!question] Match items.
>> [!example] Phase 4 Components
>> a) Train Phase
>> b) Validation Phase
>> c) Checkpointing
>
>> [!example] Purpose
>> n) Save model state
>> o) Evaluate model performance
>> p) Update model parameters
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] The code uses Counter from collections to:
>> a) Count class occurrences
>> b) Count total images
>> c) Count corrupted files
>> d) Count parameters
>> [!success]- Answer
>> a) Count class occurrences

> [!question] For a production-ready pipeline, checkpointing should be implemented in the training phase.
>> [!success]- Answer
>> True

> [!question] Which of the following is NOT a component of Phase 5 (Final Evaluation & Analysis)?
>> a) Load Best Checkpoint
>> b) Test Set Evaluation
>> c) Class Distribution Analysis
>> d) Classification Report
>> [!success]- Answer
>> c) Class Distribution Analysis

> [!question] Match items.
>> [!example] Data Inspection Areas
>> a) Class distribution
>> b) Image size consistency
>> c) Corrupted files
>
>> [!example] Potential Issues
>> n) Training failures
>> o) Memory problems
>> p) Model bias
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] The code uses glob('*.*') to:
>> a) Find all directories
>> b) Find all files in a directory
>> c) Find specific file extensions
>> d) Find image files only
>> [!success]- Answer
>> b) Find all files in a directory

> [!question] The validation phase should only be performed after the training phase is complete.
>> [!success]- Answer
>> False

> [!question] Which of the following is the primary purpose of verifying with dummy input?
>> a) To test the loss function
>> b) To ensure the model can process input
>> c) To count model parameters
>> d) To select the optimizer
>> [!success]- Answer
>> b) To ensure the model can process input

> [!question] Match items.
>> [!example] Phase 1 Steps
>> a) Gather & Inspect
>> b) Define Transforms
>> c) Create Datasets & Loaders
>
>> [!example] Key Components
>> n) Data augmentation
>> o) Class imbalance detection
>> p) Batch processing
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] The imbalance ratio is calculated as max_count divided by min_count.
>> [!success]- Answer
>> True

> [!question] Which component is responsible for updating model parameters during training?
>> a) Loss Function
>> b) Optimizer
>> c) LR Scheduler
>> d) Model Architecture
>> [!success]- Answer
>> b) Optimizer

> [!question] Match items.
>> [!example] Phase 3 Components
>> a) Loss Function
>> b) Optimizer
>> c) LR Scheduler
>
>> [!example] Purpose
>> n) Adjust learning rates
>> o) Calculate prediction error
>> p) Update model weights
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] The code uses Path objects instead of string paths for better performance.
>> [!success]- Answer
>> False

> [!question] Which of the following is NOT a recommended activity in the "Gather & Inspect" phase?
>> a) Visual inspection of sample images
>> b) Checking for corrupted files
>> c) Optimizing model architecture
>> d) Analyzing class distribution
>> [!success]- Answer
>> c) Optimizing model architecture

> [!question] The final evaluation phase should use the same validation set used during training.
>> [!success]- Answer
>> False

> [!question] Match items.
>> [!example] Pipeline Phases
>> a) Phase 1
>> b) Phase 2
>> c) Phase 3
>
>> [!example] Main Focus
>> n) Model definition
>> o) Data preparation
>> p) Training setup
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] In the provided code, the training directory is defined as:
>> [!success]- Answer
>> data_dir / 'train'

> [!question] Counting parameters is important for:
>> a) Debugging model issues
>> b) Tracking model complexity
>> c) Selecting appropriate batch size
>> d) All of the above
>> [!success]- Answer
>> d) All of the above

> [!question] The training pipeline should be followed rigidly without any modifications for different projects.
>> [!success]- Answer
>> False

> [!question] Match items.
>> [!example] Phase 4 Components
>> a) Train Phase
>> b) Validation Phase
>> c) Checkpointing
>
>> [!example] Key Activities
>> n) Save model state
>> o) Calculate gradients
>> p) Evaluate performance
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] The code uses len(list(class_dir.glob('*.*'))) to count:
>> [!success]- Answer
>> Files in a directory

> [!question] Which component is responsible for calculating the difference between predictions and true labels?
>> a) Loss Function
>> b) Optimizer
>> c) LR Scheduler
>> d) Model Architecture
>> [!success]- Answer
>> a) Loss Function
