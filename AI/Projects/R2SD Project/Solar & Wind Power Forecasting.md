
# System 1: The Solar Hybrid Residual Corrector
**Focus:** Handling Intermittency and Uncertainty via Physics-Guided Residual Refinement.

### I. Dataset Composition & Spatio-Temporal Alignment
The Solar AI does not rely on a single data stream. It performs a **Multi-Source Fusion** to create a high-fidelity "Physical Context" for the model.

*   **The Generation Log (`Solar_Generation_sub.csv`):** 
    *   **Scope:** Historical power output for **Site 25**.
    *   **Granularity:** 15-minute intervals.
    *   **The Target:** This is the ground truth $y$ that the model is trained to minimize error against.
*   **The Weather Log (`Weather_data_sub.csv`):** 
    *   **Scope:** Meteorological data for **Campus 1 (Bundoora)**.
    *   **Variables:** Temperature ($^\circ\text{C}$), Humidity ($\%$), and Wind Speed ($\text{m/s}$).
    *   **Relevance:** High ambient temperatures reduce the efficiency of photovoltaic cells (the "Temperature Coefficient" effect).
*   **The Irradiance Log (`Solar_Irradiance.csv`):** 
    *   **Scope:** Raw solar fuel data.
    *   **Variables:** Global Horizontal Irradiance (GHI).
    *   **Alignment:** Data is merged using a `merge_asof` logic with a **15-minute tolerance**, ensuring that the weather at 12:00:05 is correctly mapped to the power output at 12:00:00.

---

### II. The Solar Physics Engine (`src/data/physics.py`)
The Physics Engine acts as a deterministic filter that overrides the AI when the laws of nature are absolute.

1.  **Ineichen Clear Sky Modeling:**
    The engine calculates the theoretical maximum GHI for the exact GPS coordinates of Site 25. This allows the model to calculate the **Clear Sky Index ($k_t$)**:
    $$k_t = \frac{GHI_{\text{observed}}}{GHI_{\text{theoretical}}}$$
    By focusing on $k_t$, the AI is stripped of the "easy" task of predicting the sun's position (which is a simple clock function) and is forced to solve the "hard" task: predicting cloud-induced shading.
2.  **The "Ghost Energy" Constraint:**
    A common failure in pure statistical models is predicting solar power at night due to mathematical averaging. 
    *   **Logic:** If $GHI_{\text{observed}} < 5 \text{ Watts/m}^2$, the engine declares "Night."
    *   **Action:** The model forcefully sets power output to **0.0**, providing a hard physical boundary that the neural network cannot violate.

---

### III. Dual-Stage Hybrid Architecture
The model is a **Sequential, Non-Differentiable Hybrid** consisting of two distinct mathematical phases.

#### Stage 1: XGBoost (The Tabular Workhorse)
*   **Role:** To map static, non-linear relationships between weather and power.
*   **Logic:** It uses Gradient Boosted Decision Trees to answer: *"Given this specific temperature and this specific sun intensity, what is the expected output?"*
*   **Output:** A base prediction ($\hat{y}_{xgb}$).

#### Stage 2: PyTorch LSTM (The Temporal Refiner)
*   **Role:** To capture the "Motion" of the weather.
*   **Input:** A **6-hour sliding window** of the errors (residuals) made by Stage 1.
*   **Architecture:** A 2-layer stacked LSTM (64 hidden units) with Dropout.
*   **Differential Correction:** The LSTM predicts a **Delta ($\Delta$)**. The final prediction is $\hat{y}_{final} = \hat{y}_{xgb} + \Delta$.

#### Stage 3: Heteroscedastic Uncertainty Layer
Instead of a point forecast, the LSTM uses a **Heteroscedastic Loss** function to predict the **Log-Variance ($s$)** of the error.
$$\text{Loss} = \frac{1}{2n} \sum \left( e^{-s} \|y - \hat{y}\|^2 + s \right)$$
When the sky is "patchy" or volatile, the model increases its **Uncertainty ($\sigma$)**, providing a confidence interval for the forecast.

### IV. Empirical Results (Solar)
*   **Dataset Size:** 10,000+ intervals (after cleaning and night-filling).
*   **Accuracy:** **$R^2 \approx 0.87$**.
*   **Performance:** The model successfully recovers ~18,000 missing rows of data through physics-based nighttime imputation.

---

# System 2: The Wind Differential CNN-BiLSTM
**Focus:** Lag Prevention and Fluid Dynamics modeling for Long-Horizon Forecasting.

### I. Dataset Strategy (The SCADA Mega-Log)
The Wind AI utilizes the **KDD Cup 2022 SDWPF Dataset**, one of the largest public wind datasets in existence.
*   **Scale:** **4,727,520 rows** of data.
*   **Scope:** **134 individual wind turbines**.
*   **Granularity:** 10-minute intervals over 245 days.
*   **Complexity:** Includes pitch angles ($Pab1, 2, 3$), Nacelle direction ($Ndir$), and internal temperatures ($Etmp, Itmp$).

---

### II. The Wind Physics Engine (`wpf_engine/data/physics_engine.py`)
Wind is a vector-based fluid dynamics problem. Raw sensor data is transformed into continuous physical states:

1.  **Vector Decomposition ($U, V$):**
    The engine solves the **"360-degree boundary problem."** Without this, an AI thinks $359^\circ$ and $1^\circ$ are far apart, even though they are physically identical.
    *   $U = \text{WindSpeed} \cdot \cos(\text{WindDirection})$
    *   $V = \text{WindSpeed} \cdot \sin(\text{WindDirection})$
2.  **Cubic Energy Flux ($V^3$):**
    Wind power is proportional to the **cube of wind speed**. The engine provides this feature ($V^3$) directly, ensuring the AI respects the Betz Limit and kinetic energy laws without having to "re-learn" physics from scratch.
3.  **Momentum & Gust Detection:**
    The engine calculates the **temporal derivative** of wind speed. This allows the AI to "feel" acceleration, which is a precursor to a weather front or a high-velocity gust.

---

### III. CNN-BiLSTM Differential Architecture
Built in **TensorFlow/Keras**, this model utilizes a high-throughput vectorized sequence generator.

#### Part A: The Spatio-Temporal Feature Extractor
1.  **CNN Layer (`Conv1D`):** Slides over the last **24 hours** of history. It acts as an "Edge Detector" for wind gusts and turbulence patterns.
2.  **Bi-LSTM Layer:** A Bidirectional LSTM reads the timeline in both directions. It understands how the current wind state evolved from the past, capturing the "Momentum" of the atmosphere.

#### Part B: The "Anchor" Logic (Lag Prevention)
Standard models suffer from "Forecasting Lag" where the prediction is just a shifted version of the past.
*   **The Anchor:** The model takes the **exact power output right now** as a separate input.
*   **Differential Head:** The AI does not predict power; it predicts the **Change ($\Delta$)** relative to the anchor.
*   **The Reconstruction:** Final Output = $\text{Anchor} + \text{Predicted Delta}$. This ensures the forecast is always grounded in the current physical reality.

#### Part C: The ReLU Physical Constraint
The model terminates in a **ReLU (Rectified Linear Unit)** layer.
*   **The Reason:** Physics dictates that a wind turbine cannot have negative power (it cannot consume energy to create wind). The ReLU layer "clips" any impossible mathematical artifacts to zero.

---

### IV. Empirical Results (Wind)
The model was stress-tested on the full 4.7M row dataset with a **48-Hour Forecast Horizon** (288 steps).

*   **Final $R^2$ Score:** **0.8130**.
*   **RMSE (Root Mean Square Error):** **183.17 kW**.
*   **MAE (Mean Absolute Error):** **115.96 kW**.
*   **Efficiency:** The Vectorized Generator achieved these results by processing batches of **4,096 sequences** simultaneously on the GPU.

---

# Final System Comparison

| Feature | Solar AI (Residual Hybrid) | Wind AI (Differential Transformer) |
| :--- | :--- | :--- |
| **Dataset Scale** | ~10k Intervals (Site 25) | 4.7M Rows (134 Turbines) |
| **Physics Rule** | Sun Elevation & Irradiance | Vector Decomp & Cubic Law ($V^3$) |
| **Logic** | Fixes errors made by XGBoost | Predicts change from "Anchor" power |
| **Architecture** | XGBoost + PyTorch LSTM | CNN + Bi-LSTM (TensorFlow) |
| **Result ($R^2$)** | **0.87** | **0.813** |
| **Output Type** | Point Forecast + Confidence ($\sigma$) | 48-Hour Continuous Multi-Step |
| **Framework** | PyTorch / Scikit-Learn | TensorFlow / Keras 3 |