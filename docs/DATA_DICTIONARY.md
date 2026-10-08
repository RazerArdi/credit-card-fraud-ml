# Data Dictionary: Credit Card Transactions Fraud Detection

## Dataset Overview
This dataset contains simulated credit card transactions, comprising both legitimate and fraudulent activities occurring between January 1, 2019, and December 31, 2020. It encompasses transaction records from 1,000 customers interacting with a pool of 800 merchants.

**Source of Simulation:** 
The data was generated using the [Sparkov Data Generation](https://github.com/name/Sparkov) tool created by Brandon Harris. The simulation relies on the Python `faker` library and predefined user profiles (e.g., demographic segments, regional distribution, transaction frequencies, and expenditure parameters) to create a realistic representation of credit card usage and fraud patterns.

---

## File Structure
*   **`dataset/01_raw/fraudTrain.csv`**: The training dataset utilized for exploratory data analysis (EDA) and model development.
*   **`dataset/01_raw/fraudTest.csv`**: The testing dataset allocated for out-of-time/out-of-sample model evaluation and performance validation.

---

## Data Schema (Raw Features)

The following table details the raw columns present in both `fraudTrain.csv` and `fraudTest.csv`:

| Column Name | Data Type | Example Value | Description |
| :--- | :--- | :--- | :--- |
| `Unnamed: 0` / `index` | Integer | `0`, `1` | Unique row identifier (typically dropped during preprocessing). |
| `trans_date_trans_time` | Datetime | `2020-06-21 12:14:25` | Date and time the transaction occurred. |
| `cc_num` | Integer | `2291163933867244` | Customer's credit card number (high cardinality categorical identifier). |
| `merchant` | String | `fraud_Kirlin and Sons` | Name of the merchant where the transaction took place. |
| `category` | String | `personal_care` | Merchant category or industry type. |
| `amt` | Float | `2.86` | Transaction amount in USD. |
| `first` | String | `Jeff` | Credit card holder's first name. |
| `last` | String | `Elliott` | Credit card holder's last name. |
| `gender` | String | `M`, `F` | Credit card holder's gender (`M` = Male, `F` = Female). |
| `street` | String | `351 Darlene Green` | Credit card holder's street address. |
| `city` | String | `Columbia` | Credit card holder's city of residence. |
| `state` | String | `SC` | Credit card holder's state of residence. |
| `zip` | Integer / String | `29209` | Credit card holder's postal zip code. |
| `lat` | Float | `33.9659` | Latitude coordinate of the credit card holder's residence. |
| `long` | Float | `-80.9355` | Longitude coordinate of the credit card holder's residence. |
| `city_pop` | Integer | `333497` | Total population of the credit card holder's city. |
| `job` | String | `Mechanical engineer` | Credit card holder's profession or job title. |
| `dob` | Date | `1968-03-19` | Credit card holder's date of birth. |
| `trans_num` | String | `2da90c...` | Unique transaction identifier (hash string format). |
| `unix_time` | Integer | `1371816865` | Transaction timestamp in UNIX epoch format. |
| `merch_lat` | Float | `33.986391` | Latitude coordinate of the merchant's location. |
| `merch_long` | Float | `-81.200714` | Longitude coordinate of the merchant's location. |
| **`is_fraud`** | **Integer** | `0`, `1` | **[TARGET]** Class label indicating a fraudulent transaction (`0` = Legitimate, `1` = Fraudulent). |

---

## Engineered Features (Derived Variables)

During the Data Preprocessing and Feature Engineering phase, the raw geospatial and temporal columns are transformed to generate high-value predictive features for the machine learning models and rules engine.

| New Feature Name | Source Column(s) | Description / Logic |
| :--- | :--- | :--- |
| `distance_km` | `lat`, `long`, `merch_lat`, `merch_long` | The physical distance between the customer's residence and the merchant's location (calculated using the Haversine formula). Used to identify spatial anomalies. |
| `age` | `dob`, `trans_date_trans_time` | The customer's age at the time of the transaction. Derived by subtracting the date of birth from the transaction date. |
| `transaction_hour` | `trans_date_trans_time` | The hour of the transaction (0-23). Extracted to identify unusual temporal patterns (e.g., abnormal late-night activity). |
| `day_of_week` | `trans_date_trans_time` | The day of the week the transaction occurred. Utilized to analyze weekday versus weekend fraud distributions. |

---

## Data Notes

*   **Class Imbalance:** The target variable (`is_fraud`) is inherently highly imbalanced, reflecting real-world financial data. Standard accuracy metrics are unreliable for model assessment. Evaluation methodologies must prioritize metrics such as **AUC-ROC, Precision, Recall, and the F1-Score**.
*   **Data Artifacts:** Due to the naming convention in the Sparkov simulator, the `merchant` string often includes a "fraud_" prefix by default, even for legitimate transactions. This string must be processed or encoded appropriately during preprocessing to prevent data leakage and ensure model robustness.