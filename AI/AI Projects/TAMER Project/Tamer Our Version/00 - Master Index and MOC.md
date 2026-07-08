# Master Index and Map of Content

> This is the **Map of Content (MOC)** for the TAMER Master Vault. Every chapter and
> every file is listed here, in the recommended reading order, with a one-line
> description of what each file covers.

## Chapter Map (Recommended Reading Order)

### `10_Prerequisites/` — Prerequisites — LaTeX, OCR Problem, Python Project Structure

- [[10_Prerequisites/00_Chapter_Intro_DL_OCR_Foundations.md|00_Chapter_Intro_DL_OCR_Foundations.md]] — T3 chapter intro for the DL+OCR foundations chapter. Standalone preface, placed at end of Prerequisites chapter as it bridges into Ch 1.
- [[10_Prerequisites/01_LaTeX_Syntax_Primer.md|01_LaTeX_Syntax_Primer.md]] — Direct rename from T2 Ch 0. No other source covers LaTeX syntax as a primer.
- [[10_Prerequisites/02_OCR_Problem_and_Why_Math_Is_Hard.md|02_OCR_Problem_and_Why_Math_Is_Hard.md]] — Direct rename from T2 Ch 0. T1 1.1 HMER Overview is a related but distinct angle (about TAMER's tree-aware philosophy) -> routed to 70_The_TAMER_Model_Architecture as supplement.
- [[10_Prerequisites/03_Python_and_Project_Structure.md|03_Python_and_Project_Structure.md]] — Direct rename from T2 Ch 0. Unique to T2.
- [[10_Prerequisites/04_Introduction_to_Image_to_Sequence_Models.md|04_Introduction_to_Image_to_Sequence_Models.md]] — T3 unique. Intro to image-to-sequence models — natural fit in Prerequisites.
- [[10_Prerequisites/05_The_Physics_of_Mathematical_Typography.md|05_The_Physics_of_Mathematical_Typography.md]] — T3 unique. About the physics of math typography — natural fit in Prerequisites.

### `20_ML_and_DL_Foundations/` — ML and DL Foundations — Machine Learning to Regularization

- [[20_ML_and_DL_Foundations/01_What_is_Machine_Learning.md|01_What_is_Machine_Learning.md]] — Direct rename from T2 Ch 1. Unique foundational intro.
- [[20_ML_and_DL_Foundations/02_Deep_Learning_Fundamentals.md|02_Deep_Learning_Fundamentals.md]] — Canonical = T2. Supplement = Academic Project Report 1.1 (different voice).
- [[20_ML_and_DL_Foundations/03_Tensors_and_PyTorch_Basics.md|03_Tensors_and_PyTorch_Basics.md]] — Direct rename. Unique to T2.
- [[20_ML_and_DL_Foundations/04_Gradient_Descent_and_Optimizers.md|04_Gradient_Descent_and_Optimizers.md]] — Canonical = T2. Supplements: Top Ch 1 sec 1 (AdamW / OneCycleLR / differential LR student tip) and Academic Report 1.1 (update rule pseudo-code).
- [[20_ML_and_DL_Foundations/05_Sequence_Modeling_and_Autoregressive_Generation.md|05_Sequence_Modeling_and_Autoregressive_Generation.md]] — Direct rename. Unique to T2.
- [[20_ML_and_DL_Foundations/06_Linear_Algebra_for_Deep_Learning.md|06_Linear_Algebra_for_Deep_Learning.md]] — Direct rename. Unique to T2.
- [[20_ML_and_DL_Foundations/07_Probability_and_Information_Theory_for_ML.md|07_Probability_and_Information_Theory_for_ML.md]] — Direct rename. Unique to T2.
- [[20_ML_and_DL_Foundations/08_Regularization_Techniques.md|08_Regularization_Techniques.md]] — Direct rename. Unique to T2.

### `30_Computer_Vision_and_Image_Processing/` — Computer Vision and Image Processing

- [[30_Computer_Vision_and_Image_Processing/01_Digital_Images_and_Representation.md|01_Digital_Images_and_Representation.md]] — Direct rename. Unique to T2.
- [[30_Computer_Vision_and_Image_Processing/02_Image_Preprocessing_and_Normalization.md|02_Image_Preprocessing_and_Normalization.md]] — Canonical = T2. Related: T3 02_Data_Representation Ch 2 sec 1 (Image Processing for OCR Constraints) -> supplement.
- [[30_Computer_Vision_and_Image_Processing/03_Data_Augmentation_for_OCR.md|03_Data_Augmentation_for_OCR.md]] — Canonical = T2. Supplements: T1 4.2 Synthetic Data and Augmentation (different scope, also covers training augmentation) and T3 02_Data_Representation Ch 2 sec 3 (Data Augmentation Theory).

### `40_The_Transformer_Architecture/` — The Transformer Architecture — Attention to Layer Norm

- [[40_The_Transformer_Architecture/01_Attention_Mechanism.md|01_Attention_Mechanism.md]] — Canonical = T2. Supplements: Top Ch 1 sec 2 (Q/K/V intuitive explanation) and Academic Report 1.2 (attention narrative).
- [[40_The_Transformer_Architecture/02_Positional_Encoding_and_Embeddings.md|02_Positional_Encoding_and_Embeddings.md]] — Direct rename. Related 1D/2D positional encoding content in T3 Ch 3.7 and T1 Ch 2.4 stays as supplements.
- [[40_The_Transformer_Architecture/03_The_Transformer_Block.md|03_The_Transformer_Block.md]] — Direct rename. Unique to T2.
- [[40_The_Transformer_Architecture/04_Encoder_Decoder_Architecture.md|04_Encoder_Decoder_Architecture.md]] — Direct rename. Unique to T2.
- [[40_The_Transformer_Architecture/05_Mathematics_of_Attention_in_Detail.md|05_Mathematics_of_Attention_in_Detail.md]] — Direct rename. Unique to T2.
- [[40_The_Transformer_Architecture/06_Layer_Normalization_and_Residual_Connections.md|06_Layer_Normalization_and_Residual_Connections.md]] — Direct rename. Related: T3 9.4 Why norm-first Matters at Scale is a deeper-dive supplement but routed to 150_Architecture_Blueprint (its own chapter).
- [[40_The_Transformer_Architecture/07_What_Is_Positional_Encoding_1D_vs_2D.md|07_What_Is_Positional_Encoding_1D_vs_2D.md]] — T3 unique. Comparative 1D vs 2D positional encoding overview — fits in the Transformer Architecture chapter next to Positional Encoding.

### `50_Swin_Transformer_v2/` — Swin Transformer v2 — Vision Encoder

- [[50_Swin_Transformer_v2/00_Chapter_Intro.md|00_Chapter_Intro.md]] — T3 chapter intro for Vision Encoders chapter. Standalone preface.
- [[50_Swin_Transformer_v2/00b_Chapter_Intro_Sequence_Gen.md|00b_Chapter_Intro_Sequence_Gen.md]] — T3 chapter intro for Sequence Generation chapter. Standalone preface.
- [[50_Swin_Transformer_v2/01_Vision_Transformers_and_Patch_Approach.md|01_Vision_Transformers_and_Patch_Approach.md]] — [merged 2 sources: TAMER 2, TAMER 3] Direct rename. Related: T3 04_Sequence_Generation sec 1 (Conv vs Transformer Vision Models) -> supplement.
- [[50_Swin_Transformer_v2/02_Swin_Transformer_Architecture.md|02_Swin_Transformer_Architecture.md]] — [merged 3 sources: TAMER 1, TAMER 2, TAMER 3] Canonical = T2. Supplements: T1 2.2 Swin Transformer V2 and T3 04_Sequence_Generation sec 2 (Swin Transformer v2 Architecture).
- [[50_Swin_Transformer_v2/03_Swin_Transformer_v2_Improvements.md|03_Swin_Transformer_v2_Improvements.md]] — Direct rename. Unique to T2.
- [[50_Swin_Transformer_v2/04_Patch_Merging_and_Spatial_Resolution.md|04_Patch_Merging_and_Spatial_Resolution.md]] — Direct rename. Unique to T2.
- [[50_Swin_Transformer_v2/05_Relative_Position_Bias_and_Window_Attention.md|05_Relative_Position_Bias_and_Window_Attention.md]] — Direct rename. Unique to T2.
- [[50_Swin_Transformer_v2/06_CNNs_and_Spatial_Precision.md|06_CNNs_and_Spatial_Precision.md]] — T1 unique. About CNNs as alternative vision encoder — natural fit in the vision encoders chapter.
- [[50_Swin_Transformer_v2/07_Feature_Pyramid_Networks_and_Fusion.md|07_Feature_Pyramid_Networks_and_Fusion.md]] — T1 unique. About FPN multi-scale fusion — natural fit in vision encoders chapter.
- [[50_Swin_Transformer_v2/08_2D_Positional_Encodings.md|08_2D_Positional_Encodings.md]] — [merged 2 sources: TAMER 1, TAMER 3] T1 unique. About 2D positional encoding for vision. Related: T3 04 sec 3 (2D PE and Spatial Awareness) -> supplement to this file.

### `60_Transformer_Decoder_and_Sequence_Generation/` — Transformer Decoder and Sequence Generation

- [[60_Transformer_Decoder_and_Sequence_Generation/00_Chapter_Intro.md|00_Chapter_Intro.md]] — T3 chapter intro. Standalone (preserved whole as a chapter preface).
- [[60_Transformer_Decoder_and_Sequence_Generation/01_Transformer_Decoder_in_Detail.md|01_Transformer_Decoder_in_Detail.md]] — [merged 3 sources: TAMER 1, TAMER 2, TAMER 3] Canonical = T2. Supplements: T1 3.1 Transformer Decoder Fundamentals and T3 05_Chapter_Intro + 05 sec 1 Transformer Decoder Architecture.
- [[60_Transformer_Decoder_and_Sequence_Generation/02_Causal_Masking_and_Autoregressive_Decoding.md|02_Causal_Masking_and_Autoregressive_Decoding.md]] — Direct rename. Unique to T2.
- [[60_Transformer_Decoder_and_Sequence_Generation/03_Teacher_Forcing_and_Training_vs_Inference.md|03_Teacher_Forcing_and_Training_vs_Inference.md]] — [merged 2 sources: TAMER 2, TAMER 3] Canonical = T2. Supplement: T3 05 sec 3 Autoregressive Teacher Forcing.
- [[60_Transformer_Decoder_and_Sequence_Generation/04_Output_Projection_and_Softmax.md|04_Output_Projection_and_Softmax.md]] — Direct rename. Unique to T2.
- [[60_Transformer_Decoder_and_Sequence_Generation/05_Handling_Variable_Length_Sequences.md|05_Handling_Variable_Length_Sequences.md]] — Direct rename. Unique to T2.
- [[60_Transformer_Decoder_and_Sequence_Generation/06_1D_Sinusoidal_Positional_Encoding.md|06_1D_Sinusoidal_Positional_Encoding.md]] — T3 unique. About 1D sinusoidal PE for the decoder — natural fit in decoder chapter.
- [[60_Transformer_Decoder_and_Sequence_Generation/06_Cross_Attention_and_Coverage.md|06_Cross_Attention_and_Coverage.md]] — T1 unique. About cross-attention + coverage in the decoder — natural fit in decoder chapter. Disambiguated from T1 4.1 Joint Loss Functions.

### `70_The_TAMER_Model_Architecture/` — The TAMER Model Architecture — End-to-End Model

- [[70_The_TAMER_Model_Architecture/00_Course_Overview.md|00_Course_Overview.md]] — T3 course-level intro. Standalone (preserved whole as a course preface in the architecture chapter).
- [[70_The_TAMER_Model_Architecture/01_TAMER_Model_Overview.md|01_TAMER_Model_Overview.md]] — [merged 2 sources: TAMER 1, TAMER 2] Canonical = T2. Supplement: T1 1.1 HMER Overview and Challenges (philosophy of TAMER, tree-awareness).
- [[70_The_TAMER_Model_Architecture/02_From_Image_to_LaTeX_Data_Flow.md|02_From_Image_to_LaTeX_Data_Flow.md]] — Direct rename. Unique to T2.
- [[70_The_TAMER_Model_Architecture/03_Model_Configuration_and_Hyperparameters.md|03_Model_Configuration_and_Hyperparameters.md]] — Direct rename. Unique to T2.
- [[70_The_TAMER_Model_Architecture/04_Model_Submodules_Attention_Encoder_Decoder.md|04_Model_Submodules_Attention_Encoder_Decoder.md]] — Direct rename. Unique to T2.
- [[70_The_TAMER_Model_Architecture/05_The_No_Tree_Trade_off_Relying_on_Attention.md|05_The_No_Tree_Trade_off_Relying_on_Attention.md]] — T3 unique. Discusses the design trade-off of dropping tree-awareness. Natural fit in TAMER Architecture chapter.

### `80_Data_Pipeline_and_Preprocessing/` — Data Pipeline and Preprocessing — Datasets to DataLoader

- [[80_Data_Pipeline_and_Preprocessing/00_Chapter_Intro.md|00_Chapter_Intro.md]] — T3 chapter intro for Data Representation chapter. Standalone preface.
- [[80_Data_Pipeline_and_Preprocessing/01_The_Four_Datasets.md|01_The_Four_Datasets.md]] — Direct rename. Unique to T2.
- [[80_Data_Pipeline_and_Preprocessing/02_Image_Preprocessing_and_Normalization.md|02_Image_Preprocessing_and_Normalization.md]] — T3 supplement to T2 Ch 2.2 canonical for image preprocessing topic.
- [[80_Data_Pipeline_and_Preprocessing/02_LaTeX_Tokenization.md|02_LaTeX_Tokenization.md]] — [merged 4 sources: TAMER 1, TAMER 2, TAMER 3] Canonical = T2. Supplements: T1 1.3 Tokenization and Mathematical Grammar and T3 03_Vision_Encoders sec 1 Lexical Analysis of LaTeX and sec 2 Vocabulary and Special Tokens.
- [[80_Data_Pipeline_and_Preprocessing/03_Data_Sanitization_and_Filtering.md|03_Data_Sanitization_and_Filtering.md]] — [merged 2 sources: TAMER 1, TAMER 2] Direct rename. Unique to T2.
- [[80_Data_Pipeline_and_Preprocessing/04_Curriculum_Learning.md|04_Curriculum_Learning.md]] — [merged 2 sources: TAMER 2, TAMER 3] Canonical = T2. Supplements: T1 4.3 Two-Stage Pretraining and Curriculum Learning (different angle: combines pretraining + curriculum) and T3 07_Hardware_Optimization sec 4 (Section 7.3 Two-Stage Pretraining and Curriculum Learning).
- [[80_Data_Pipeline_and_Preprocessing/05_The_MathDataset_and_DataLoader.md|05_The_MathDataset_and_DataLoader.md]] — [merged 2 sources: TAMER 2, TAMER 3] Canonical = T2. Supplement: T3 08_Evaluation_and_MLOps sec 2 PyTorch DataLoaders and RAM Saturation.
- [[80_Data_Pipeline_and_Preprocessing/06_LaTeX_Normalization.md|06_LaTeX_Normalization.md]] — Direct rename. Unique to T2.
- [[80_Data_Pipeline_and_Preprocessing/07_Data_Validation_and_Integrity.md|07_Data_Validation_and_Integrity.md]] — Direct rename. Unique to T2.
- [[80_Data_Pipeline_and_Preprocessing/08_The_Downloader_and_Dataset_Registry.md|08_The_Downloader_and_Dataset_Registry.md]] — Direct rename. Unique to T2.
- [[80_Data_Pipeline_and_Preprocessing/09_Python_Memory_Leaks_and_OOM_Caching_Bug.md|09_Python_Memory_Leaks_and_OOM_Caching_Bug.md]] — T3 unique. About Python memory leaks / OOM caching bug — natural fit in data pipeline chapter.
- [[80_Data_Pipeline_and_Preprocessing/10_Data_Augmentation_Theory.md|10_Data_Augmentation_Theory.md]] — T3 unique. Theoretical treatment of data augmentation — fits in data pipeline.

### `90_Loss_Functions_and_Optimization/` — Loss Functions and Optimization

- [[90_Loss_Functions_and_Optimization/00_Chapter_Intro.md|00_Chapter_Intro.md]] — T3 chapter intro. Standalone preface.
- [[90_Loss_Functions_and_Optimization/01_Cross_Entropy_Loss_for_Sequence_Models.md|01_Cross_Entropy_Loss_for_Sequence_Models.md]] — [merged 2 sources: TAMER 2, TAMER 3] Canonical = T2. Supplement: T3 06_Objective_Functions sec 1 (Cross-Entropy and Label Smoothing).
- [[90_Loss_Functions_and_Optimization/02_Label_Smoothing.md|02_Label_Smoothing.md]] — Canonical = T2. Supplement: T3 06 sec 1 also covers label smoothing — appended here.
- [[90_Loss_Functions_and_Optimization/03_Structure_Aware_Loss.md|03_Structure_Aware_Loss.md]] — [merged 2 sources: TAMER 2, TAMER 3] Canonical = T2. Supplement: T3 06 sec 2 Structure-Aware Loss Functions.

### `100_Training_Infrastructure_and_Techniques/` — Training Infrastructure and Techniques

- [[100_Training_Infrastructure_and_Techniques/00_Chapter_Intro.md|00_Chapter_Intro.md]] — T3 chapter intro for Evaluation_and_MLOps. Standalone preface.
- [[100_Training_Infrastructure_and_Techniques/01_Mixed_Precision_Training_BFloat16.md|01_Mixed_Precision_Training_BFloat16.md]] — [merged 2 sources: TAMER 2, TAMER 3] Canonical = T2. Supplement: T3 08_Evaluation_and_MLOps sec 1 (Mixed Precision BFloat16 vs FP16).
- [[100_Training_Infrastructure_and_Techniques/02_Multi_GPU_Training_DataParallel.md|02_Multi_GPU_Training_DataParallel.md]] — [merged 2 sources: TAMER 2, TAMER 3] Canonical = T2. Supplement: T3 08 sec 3 (Multi-GPU Training DataParallel).
- [[100_Training_Infrastructure_and_Techniques/03_Training_Loop_and_Engine_Functions.md|03_Training_Loop_and_Engine_Functions.md]] — Direct rename. Unique to T2.
- [[100_Training_Infrastructure_and_Techniques/04_Encoder_Freeze_and_Differential_Learning_Rates.md|04_Encoder_Freeze_and_Differential_Learning_Rates.md]] — Direct rename. Unique to T2.
- [[100_Training_Infrastructure_and_Techniques/05_Checkpointing_and_Model_Persistence.md|05_Checkpointing_and_Model_Persistence.md]] — Direct rename. Unique to T2. Related engineering content in Top Ch 9 sec 1 (Atomic Checkpoint Writes) is in 180_Data_Engineering_and_Reliability chapter.
- [[100_Training_Infrastructure_and_Techniques/06_torch_compile_Deep_Dive.md|06_torch_compile_Deep_Dive.md]] — Direct rename. Unique to T2.
- [[100_Training_Infrastructure_and_Techniques/07_Hardware_Optimization_and_GPU_Utilization.md|07_Hardware_Optimization_and_GPU_Utilization.md]] — Direct rename. Unique to T2.
- [[100_Training_Infrastructure_and_Techniques/08_Debugging_Training_Issues.md|08_Debugging_Training_Issues.md]] — Direct rename. Unique to T2.

### `110_Inference_and_Decoding/` — Inference and Decoding — Greedy, Beam Search, Constraints

- [[110_Inference_and_Decoding/00_Chapter_Intro.md|00_Chapter_Intro.md]] — T3 chapter intro for Hardware Optimization and Training Dynamics. Standalone preface.
- [[110_Inference_and_Decoding/01_Greedy_Decoding.md|01_Greedy_Decoding.md]] — [merged 2 sources: TAMER 2, TAMER 3] Canonical = T2. Supplement: T3 07_Hardware_Optimization sec 1 (Batched Greedy Decoding).
- [[110_Inference_and_Decoding/02_Beam_Search.md|02_Beam_Search.md]] — [merged 3 sources: TAMER 1, TAMER 2, TAMER 3] Canonical = T2. Supplements: T1 5.1 Beam Search and Greedy Decoding and T3 07 sec 2 (Beam Search Decoding).
- [[110_Inference_and_Decoding/03_Tree_Based_Structural_Scoring.md|03_Tree_Based_Structural_Scoring.md]] — T1 unique. About tree-based structural scoring during inference — natural fit in inference chapter.
- [[110_Inference_and_Decoding/04_Grammar_Constrained_Decoding.md|04_Grammar_Constrained_Decoding.md]] — T1 unique. About grammar-constrained decoding — natural fit in inference chapter.

### `120_Evaluation_Metrics_for_OCR/` — Evaluation Metrics for OCR

- [[120_Evaluation_Metrics_for_OCR/01_Exact_Match_Rate_and_Edit_Distance.md|01_Exact_Match_Rate_and_Edit_Distance.md]] — Direct rename. Unique to T2.
- [[120_Evaluation_Metrics_for_OCR/02_Structural_Accuracy_and_Token_Level_Metrics.md|02_Structural_Accuracy_and_Token_Level_Metrics.md]] — Direct rename. Unique to T2.

### `130_The_Complete_Training_Pipeline/` — The Complete Training Pipeline — End-to-End Walkthrough

- [[130_The_Complete_Training_Pipeline/01_End_to_End_Pipeline_Walkthrough.md|01_End_to_End_Pipeline_Walkthrough.md]] — Direct rename. Unique to T2.
- [[130_The_Complete_Training_Pipeline/02_Kaggle_Notebook_Cells_Explained.md|02_Kaggle_Notebook_Cells_Explained.md]] — Direct rename. Unique to T2.
- [[130_The_Complete_Training_Pipeline/03_The_train_py_Entry_Point.md|03_The_train_py_Entry_Point.md]] — Direct rename. Unique to T2.
- [[130_The_Complete_Training_Pipeline/04_The_OCR_Landscape_How_TAMER_Compares.md|04_The_OCR_Landscape_How_TAMER_Compares.md]] — Direct rename. Related SOTA content in Top Ch 7 -> routed to 170_Context_SOTA chapter.

### `140_Tree_Aware_TAMER_Extensions/` — Tree-Aware TAMER Extensions — Niche: Tree Decoding, Covering Attention, Grammar

- [[140_Tree_Aware_TAMER_Extensions/01_Sequence_vs_Tree_Decoding.md|01_Sequence_vs_Tree_Decoding.md]] — T1 unique. Core tree-aware TAMER concept — niche topic gets own chapter.
- [[140_Tree_Aware_TAMER_Extensions/02_Tree_Representation_and_Annotation.md|02_Tree_Representation_and_Annotation.md]] — T1 unique. About how math is represented as trees.
- [[140_Tree_Aware_TAMER_Extensions/03_Covering_Attention_Mechanism.md|03_Covering_Attention_Mechanism.md]] — T1 unique. About covering attention — TAMER-specific.
- [[140_Tree_Aware_TAMER_Extensions/04_Tree_Aware_Module_Implementation.md|04_Tree_Aware_Module_Implementation.md]] — T1 unique. Implementation of the Tree-Aware Module (TAM).
- [[140_Tree_Aware_TAMER_Extensions/05_Joint_Loss_Functions.md|05_Joint_Loss_Functions.md]] — T1 unique. Joint loss combining sequence + tree objectives. Disambiguated from T1 4.1 Cross-Attention (same number, different topic).
- [[140_Tree_Aware_TAMER_Extensions/06_LaTeX_Grammar_Constraints.md|06_LaTeX_Grammar_Constraints.md]] — T1 unique. About LaTeX grammar constraints during decoding. Disambiguated from T1 4.2 Synthetic Data (same number, different topic).
- [[140_Tree_Aware_TAMER_Extensions/07_Constrained_Beam_Search.md|07_Constrained_Beam_Search.md]] — T1 unique. Beam search with grammar + tree constraints. Disambiguated from T1 4.3 Two-Stage Pretraining (same number, different topic).
- [[140_Tree_Aware_TAMER_Extensions/08_Two_Stage_Pretraining_and_Curriculum_Learning.md|08_Two_Stage_Pretraining_and_Curriculum_Learning.md]] — T1 supplement. Disambiguated from T1 4.3 Constrained Beam Search. Appended to T2 Ch 7.4 canonical for curriculum learning topic.

### `150_The_Complete_Architecture_Blueprint/` — The Complete Architecture Blueprint — Niche: Master Diagram, Tensor Flow, Grammar State Machine

- [[150_The_Complete_Architecture_Blueprint/00_Chapter_Intro.md|00_Chapter_Intro.md]] — T3 chapter intro. Standalone preface.
- [[150_The_Complete_Architecture_Blueprint/01_The_Master_TAMER_Architecture_Diagram.md|01_The_Master_TAMER_Architecture_Diagram.md]] — T3 unique. Master TAMER architecture diagram.
- [[150_The_Complete_Architecture_Blueprint/02_Layer_by_Layer_Tensor_Flow_and_Mathematics.md|02_Layer_by_Layer_Tensor_Flow_and_Mathematics.md]] — T3 unique. Layer-by-layer tensor flow + math.
- [[150_The_Complete_Architecture_Blueprint/03_The_Row_Boundary_Marker_Deep_Dive.md|03_The_Row_Boundary_Marker_Deep_Dive.md]] — T3 unique. Row boundary marker deep dive.
- [[150_The_Complete_Architecture_Blueprint/04_Why_norm_first_Matters_at_Scale.md|04_Why_norm_first_Matters_at_Scale.md]] — T3 unique. Why norm-first matters at scale.
- [[150_The_Complete_Architecture_Blueprint/05_The_Complete_Forward_Pass_Every_Tensor_Every_Shape.md|05_The_Complete_Forward_Pass_Every_Tensor_Every_Shape.md]] — T3 unique. Complete forward pass with every tensor and shape.
- [[150_The_Complete_Architecture_Blueprint/06_The_Training_Loop_vs_Inference_Loop_Side_by_Side.md|06_The_Training_Loop_vs_Inference_Loop_Side_by_Side.md]] — T3 unique. Training loop vs inference loop side-by-side.
- [[150_The_Complete_Architecture_Blueprint/07_The_Grammar_State_Machine_Full_Specification.md|07_The_Grammar_State_Machine_Full_Specification.md]] — T3 unique. Grammar state machine full specification.

### `160_Scheduling_and_Exposure_Bias/` — Scheduling and Exposure Bias — Niche: Teacher Forcing, Scheduled Sampling, Full Decoder Loop

- [[160_Scheduling_and_Exposure_Bias/01_Teacher_Forcing_and_Exposure_Bias.md|01_Teacher_Forcing_and_Exposure_Bias.md]] — T3 unique. Teacher forcing + exposure bias analysis.
- [[160_Scheduling_and_Exposure_Bias/02_Scheduled_Sampling_Bridging_the_Training_Inference_Gap.md|02_Scheduled_Sampling_Bridging_the_Training_Inference_Gap.md]] — T3 unique. Scheduled sampling technique.
- [[160_Scheduling_and_Exposure_Bias/03_The_Full_Decoder_Training_Loop_End_to_End.md|03_The_Full_Decoder_Training_Loop_End_to_End.md]] — T3 unique. Full decoder training loop end-to-end.

### `170_Context_SOTA_and_Benchmarks/` — Context, SOTA Models and Benchmarks

- [[170_Context_SOTA_and_Benchmarks/01_SOTA_Models_and_Benchmarks.md|01_SOTA_Models_and_Benchmarks.md]] — Top Ch 7 P1. Condensed SOTA models + benchmarks lecture note. Kept whole.
- [[170_Context_SOTA_and_Benchmarks/02_Context_and_Deployment_Comparison.md|02_Context_and_Deployment_Comparison.md]] — Top Ch 7 P2. Condensed context + deployment lecture note. Kept whole.

### `180_Data_Engineering_and_Reliability/` — Data Engineering and System Reliability — Niche: POSIX Atomicity, NFS Bypass, Flight Recorder

- [[180_Data_Engineering_and_Reliability/01_Data_Engineering_and_Distributed_Systems.md|01_Data_Engineering_and_Distributed_Systems.md]] — Top Ch 8 P1. Condensed data engineering lecture note (HTTP Range, chunked streaming, NFS bypass). Kept whole.
- [[180_Data_Engineering_and_Reliability/02_System_Reliability_and_Checkpointing.md|02_System_Reliability_and_Checkpointing.md]] — Top Ch 9 P1. Condensed system reliability lecture note (atomic checkpoints, fsync, flight recorder, /dev/shm). Kept whole.

### `190_Experiments_and_Results/` — Experiments, Results and MLOps

- [[190_Experiments_and_Results/01_Datasets_and_Evaluation_Metrics.md|01_Datasets_and_Evaluation_Metrics.md]] — [merged 2 sources: TAMER 1, TAMER 3] T1 canonical for the experiments chapter. Supplements: T3 08 sec 5 Datasets and Evaluation Metrics.
- [[190_Experiments_and_Results/02_Performance_and_Complexity_Analysis.md|02_Performance_and_Complexity_Analysis.md]] — [merged 2 sources: TAMER 1, TAMER 3] T1 canonical. Disambiguated from T1 6.2 Analysis and Future Directions (same number, different topic). Supplement: T3 08 sec 6 Performance and Complexity Analysis.
- [[190_Experiments_and_Results/03_Ablation_Study_and_Inference_Speed.md|03_Ablation_Study_and_Inference_Speed.md]] — T1 unique. Ablation study.
- [[190_Experiments_and_Results/04_Analysis_and_Future_Directions.md|04_Analysis_and_Future_Directions.md]] — T1 unique. Disambiguated from T1 6.2 Performance and Complexity Analysis (same number, different topic).
- [[190_Experiments_and_Results/05_Cloud_Integration_and_Hardware_Limits.md|05_Cloud_Integration_and_Hardware_Limits.md]] — [merged 2 sources: TAMER 1, TAMER 3] T1 canonical. Supplements: T3 08 sec 7 Cloud Integration and Persistence.
- [[190_Experiments_and_Results/06_Environment_Configuration_for_CV_Tools.md|06_Environment_Configuration_for_CV_Tools.md]] — T1 unique. About env configuration for CV tools — natural fit in experiments / MLOps chapter.

### `200_Lecture_Summaries/` — Lecture Summaries — Condensed Multi-Topic Study Notes (Top Chapters)

- [[200_Lecture_Summaries/01_DL_and_Attention_Summary.md|01_DL_and_Attention_Summary.md]] — Top Ch 1. Condensed multi-topic summary (NN, attention, encoder-decoder, transformers). Kept whole as a study companion to the deep chapters.
- [[200_Lecture_Summaries/02a_Computer_Vision_Summary.md|02a_Computer_Vision_Summary.md]] — Top Ch 2 P1. Kept whole.
- [[200_Lecture_Summaries/02b_Computer_Vision_Summary.md|02b_Computer_Vision_Summary.md]] — Top Ch 2 P2. Kept whole.
- [[200_Lecture_Summaries/02c_Computer_Vision_Summary.md|02c_Computer_Vision_Summary.md]] — Top Ch 2 P3. Kept whole.
- [[200_Lecture_Summaries/02d_Computer_Vision_Summary.md|02d_Computer_Vision_Summary.md]] — Top Ch 2 P4. Kept whole.
- [[200_Lecture_Summaries/02e_Computer_Vision_Summary.md|02e_Computer_Vision_Summary.md]] — Top Ch 2 P5. Kept whole.
- [[200_Lecture_Summaries/03a_Sequence_Modeling_Summary.md|03a_Sequence_Modeling_Summary.md]] — Top Ch 3 P1. Kept whole.
- [[200_Lecture_Summaries/03b_Sequence_Modeling_Summary.md|03b_Sequence_Modeling_Summary.md]] — Top Ch 3 P2. Kept whole.
- [[200_Lecture_Summaries/03c_Sequence_Modeling_Summary.md|03c_Sequence_Modeling_Summary.md]] — Top Ch 3 P3. Kept whole.
- [[200_Lecture_Summaries/03d_Sequence_Modeling_Summary.md|03d_Sequence_Modeling_Summary.md]] — Top Ch 3 P4. Kept whole.
- [[200_Lecture_Summaries/03e_Sequence_Modeling_Summary.md|03e_Sequence_Modeling_Summary.md]] — Top Ch 3 P5. Kept whole.
- [[200_Lecture_Summaries/04a_Text_Processing_Summary.md|04a_Text_Processing_Summary.md]] — Top Ch 4 P1. Kept whole.
- [[200_Lecture_Summaries/04b_Text_Processing_Summary.md|04b_Text_Processing_Summary.md]] — Top Ch 4 P2. Kept whole.
- [[200_Lecture_Summaries/05a_Advanced_Training_Summary.md|05a_Advanced_Training_Summary.md]] — Top Ch 5 P1. Kept whole.
- [[200_Lecture_Summaries/05b_Advanced_Training_Summary.md|05b_Advanced_Training_Summary.md]] — Top Ch 5 P2. Kept whole.
- [[200_Lecture_Summaries/05c_Advanced_Training_Summary.md|05c_Advanced_Training_Summary.md]] — Top Ch 5 P3. Kept whole.
- [[200_Lecture_Summaries/06a_Inference_and_Evaluation_Summary.md|06a_Inference_and_Evaluation_Summary.md]] — Top Ch 6 P1. Kept whole.
- [[200_Lecture_Summaries/06b_Inference_and_Evaluation_Summary.md|06b_Inference_and_Evaluation_Summary.md]] — Top Ch 6 P2. Kept whole.

### `300_Academic_Project_Report/` — Academic Project Report — Standalone Narrative Document

- [[300_Academic_Project_Report/Academic_Project_Report.md|Academic_Project_Report.md]] — Standalone narrative academic report (~92K chars, different voice/genre). Kept whole as its own top-level document.

### `900_Source_READMEs/` — Source Collection READMEs — Historical Context

- [[900_Source_READMEs/TAMER_1_README.md|TAMER_1_README.md]] — TAMER 1 collection README. Preserved whole for historical context.
- [[900_Source_READMEs/TAMER_2_README.md|TAMER_2_README.md]] — TAMER 2 collection README. Preserved whole for historical context.

---

## Auxiliary Files

- [[Shared/AI/AI Projects/TAMER Project/Tamer Our Version/README]] — Vault overview, design principles, statistics
- [[01_Transformation_Log]] — Per-source-file routing log
- [[999_Source_Archive_Index]] — Reverse index: every source file → its master destination
- [[_merge_groups.tsv]] — Machine-readable per-master-file merge report
- [[_transformation_log.tsv]] — Machine-readable per-source-file transformation report

---

## Cross-Chapter Topic Map

Some topics span multiple chapters. Use this map to find every file that touches a
given topic:

| Topic | Files |
|---|---|
| Curriculum | `140_Tree_Aware_TAMER_Extensions/08_Two_Stage_Pretraining_and_Curriculum_Learning.md`, `80_Data_Pipeline_and_Preprocessing/04_Curriculum_Learning.md` |
| Image Preprocessing | `30_Computer_Vision_and_Image_Processing/02_Image_Preprocessing_and_Normalization.md`, `80_Data_Pipeline_and_Preprocessing/02_Image_Preprocessing_and_Normalization.md` |
