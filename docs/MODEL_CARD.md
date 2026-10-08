# Model Card: Risk Fraud Detection Engine

## 1. Model Details
* **Model Name:** Risk LightGBM Classifier
* **Version:** 1.0 (Production Candidate)
* **Date:** October 2026
* **Developer:** Bayu Ardiyansyah
* **Model Type:** Gradient Boosting Decision Tree (LightGBM) for Binary Classification.
* **Architecture / Framework:** LightGBM via Scikit-Learn API.
* **License:** Proprietary / Internal Enterprise Use.

## 2. Intended Use
* **Primary Use Case:** To asynchronously score credit card transactions and output a fraud probability score (0.0 - 1.0) to assist the Risk Operations team in identifying unauthorized transactions.
* **Primary Users:** Fraud Operations Analysts (via the Risk Dashboard) and Automated Escalation Rules Engines.
* **Out-of-Scope Uses:** 
  * This model is **not** intended for real-time synchronous blocking at the payment gateway switch level (latency requirements for that layer are stricter).
  * This model is **not** intended for credit risk scoring (loan approval).

## 3. Factors & Feature Overview
The model predictions are driven by spatial, temporal, and categorical features engineered from raw transaction logs.
* **Temporal Features:** `hour` (extracted from transaction timestamp to detect abnormal late-night activity).
* **Geospatial Features:** `distance_km` (Haversine distance calculated between the cardholder's registered address and the merchant's location).
* **Categorical Features:** `merchant`, `category` (Target Encoded with smoothing to prevent data leakage).
* **Demographic Features:** `age` (Derived from DOB).

## 4. Metrics
Given the extreme class imbalance (Fraud rate ≈ 0.58%), standard accuracy is misleading. The model is evaluated using the following metrics:
* **Primary Metric:** Precision-Recall Area Under Curve (PR-AUC).
* **Operational Metrics (at decision threshold 0.9741):**
  * **Recall (Sensitivity):** ~77.0% (Percentage of actual fraud caught).
  * **Precision:** ~91.0% (Percentage of flagged transactions that are truly fraud).
  * **False Positive Rate (FPR):** ~0.03% (Customer friction rate).

## 5. Evaluation Data
* **Dataset:** `fraudTest.csv` (Simulated credit card transaction data).
* **Size:** ~555,719 rows.
* **Class Distribution:** 99.42% Legitimate (Class 0) | 0.58% Fraud (Class 1).
* **Preprocessing:** Standard scaling applied to continuous variables; PII (Names, exact credit card numbers) removed entirely.

## 6. Training Data
* **Dataset:** `fraudTrain.csv`
* **Handling Imbalance:** The model utilizes class weighting (via LightGBM's `scale_pos_weight` or `is_unbalance=True`) rather than synthetic oversampling (SMOTE) to preserve the natural distribution of the feature space and maintain inference speed.

## 7. Ethical Considerations & Fairness
* **Personally Identifiable Information (PII):** To protect user privacy, direct identifiers (Names, Credit Card Numbers, exact street addresses) were excluded from the training and inference pipelines.
* **Algorithmic Bias:** Demographic features such as `gender` and `age` were evaluated using SHAP (SHapley Additive exPlanations). While `age` provides some predictive power (e.g., seniors being targeted by specific scams), the model's global feature importance relies predominantly on behavioral metrics (`distance_km`, `transaction_amount`) rather than demographic profiling, minimizing the risk of discriminatory flagging.

## 8. Caveats and Recommendations
* **Threshold Tuning:** The current threshold (0.9741) is heavily optimized for Precision to reduce manual review costs (OpEx). If the business strategy shifts towards zero-tolerance for fraud losses, this threshold must be lowered to increase Recall, at the expense of higher operational review queues.
* **Concept Drift:** Fraud patterns evolve rapidly. It is recommended that this model be retrained every 30-45 days with the latest confirmed chargeback data, monitored continuously via MLflow.
* **Cold Start Problem:** New merchants without historical transaction data may suffer from inaccurate Target Encoding averages. A fallback global average is used, but predictions for brand-new merchants should be treated with lower confidence.