# Business Requirements Document (BRD)

**Project Name:** Enterprise Fraud Analytics & Intelligence System

**Document Version:** 2.0 (Updated Scope for E2E Deployment)
**Prepared By:** Bayu Ardiyansyah

**Date:** October 2026

---

## 1. Executive Summary

The organization requires an advanced, machine learning-driven fraud detection system to mitigate financial losses stemming from unauthorized credit card transactions. By leveraging historical transaction data, spatial-temporal analysis, and demographic profiling, this project will transition the existing risk mitigation strategy from a reactive, static rule-based engine to a proactive, predictive intelligence platform.

To bridge the gap between data science and business operations, the final system will not only provide automated risk scoring but also feature a real-time operational dashboard, a Retrieval-Augmented Generation (RAG) AI Copilot for compliance navigation, and a Power BI data mart for C-level financial reporting (ROI and Net Savings).

## 2. Problem Statement

Current static rule-based fraud detection systems face several critical limitations:

1. **Inability to Detect Emerging Threats:** Fixed rules fail to adapt to rapidly evolving, sophisticated fraud vectors.
2. **High Customer Friction:** Legitimate transactions are frequently flagged (High False Positive Rate), leading to customer dissatisfaction and card abandonment.
3. **Operational Bottlenecks:** A high volume of false alarms overwhelms the Risk Operations team, increasing manual review costs.
4. **Lack of Executive Visibility:** Disconnect between technical machine learning metrics and business KPIs (e.g., Net Savings, Operational Costs) prevents executives from evaluating the system's actual financial impact.
5. **Black-Box Decision Making:** Lack of algorithmic transparency makes it difficult to audit why specific transactions are blocked, complicating regulatory compliance.

## 3. Business Objectives

Aligned with the organization's strategic risk management goals, this project seeks to:

* **Maximize Net Business Value:** Reduce gross fraud losses while simultaneously minimizing the operational expenditure (OpEx) of manual reviews.
* **Enhance Operational Efficiency:** Provide real-time spatial and temporal alert monitoring for the Fraud Operations team via an interactive interface.
* **Ensure Regulatory Compliance:** Integrate an AI Copilot that can cross-reference internal SOPs and regulatory documents (e.g., POJK, Visa Rules) to guide operational responses.
* **Deliver Algorithmic Transparency:** Utilize Explainable AI (XAI) to break down transaction risk factors for internal auditing.

## 4. Scope of Work

### 4.1 In-Scope

* **Data Pipeline Construction:** Development of robust data ingestion pipelines, including spatial (Haversine distance) and temporal feature extraction.
* **Model Development:** Training and optimization of tree-based machine learning classifiers (LightGBM) calibrated for severe class imbalance.
* **MLOps Infrastructure:** Implementation of a Model Registry and tracking environment utilizing MLflow to ensure model reproducibility.
* **Enterprise Dashboard Application:** Development of a web-based dashboard (Python/Dash) utilizing an MVC architecture, featuring dedicated interfaces for Executive Summary, Operations Monitor, and Model Performance.
* **AI Copilot (RAG):** Integration of an LLM (Large Language Model) orchestrated via LangChain, utilizing a ChromaDB vector database to provide compliance and metric-based assistance.
* **BI Integration:** Development of an automated data mart exporter to feed flat-table predictions directly into Power BI.

### 4.2 Out-of-Scope

* Direct integration into the payment gateway's core authorization switch (the system will act as an asynchronous risk-scoring microservice and monitoring platform).
* Handling of physical credit card issuance or chargeback legal processing.

## 5. Key Performance Indicators (KPIs) & Success Metrics

The success of the project will be evaluated against three primary metric categories:

### 5.1 Business / Executive Metrics

* **Net Savings (ROI):** Total fraud losses prevented minus the estimated operational cost of manual reviews.
* **Customer Friction Rate (FPR):** Must remain below 0.5% to ensure minimal disruption to legitimate customer transactions.
* **System Approval Rate:** Percentage of total transactions passed without requiring manual operational intervention.

### 5.2 Operational Metrics

* **Alert Volume / Manual Review Queue:** Maintain the absolute number of low-confidence alerts forwarded to the manual review queue within the team's daily capacity.
* **Loss Escaped:** The financial value of actual fraud that bypassed the current decision threshold.

### 5.3 Technical / Data Science Metrics

* **Precision-Recall Area Under Curve (PR-AUC):** The primary metric for model evaluation, given the extreme minority class (0.58% fraud rate).
* **Inference Latency:** Ensure the model serving endpoint processes scoring requests efficiently for real-time monitoring.

## 6. Functional Requirements

* **FR-01 (Feature Engineering):** The system must dynamically calculate the geospatial distance between the cardholder's registered address and the merchant's coordinates.
* **FR-02 (Categorical Handling):** The system must utilize Target Encoding with robust smoothing to handle high-cardinality features without inducing data leakage.
* **FR-03 (Model Registry):** All trained models and evaluation metrics must be automatically logged into a centralized MLflow registry.
* **FR-04 (Dashboard Navigation):** The UI must separate executive financial views from granular operational geospatial maps and technical ML evaluation views.
* **FR-05 (AI Retrieval):** The AI Copilot must process natural language queries, retrieving exact clauses from uploaded PDF documents (SOPs, regulations) to generate grounded responses.
* **FR-06 (Explainability):** The system must generate and display SHAP (SHapley Additive exPlanations) values to justify individual prediction scores.

## 7. Non-Functional Requirements

* **NFR-01 (Architecture):** The application must strictly follow the Model-View-Controller (MVC) software engineering paradigm to separate data logic from UI rendering.
* **NFR-02 (Security):** Personally Identifiable Information (PII) such as exact credit card numbers must be excluded from the dashboard displays and AI prompts. API keys (e.g., Groq API) must be secured via environment variables (`.env`).
* **NFR-03 (Interoperability):** The system must automatically generate structured CSV/Parquet files formatted explicitly for seamless schema import into Power BI Desktop.

## 8. Target Audience & Stakeholders

* **C-Suite & Executives (CRO, CFO):** Primary consumers of the Executive Summary tab and Power BI reports to validate system ROI and TPV (Total Processed Value) impact.
* **Fraud Operations Team:** Primary users of the Operations Monitor and AI Copilot to review the investigation queue and consult compliance guidelines.
* **Data Science & Risk Analytics:** Owners of the Model Performance tab and MLflow registry to continuously monitor training drift, threshold tuning, and algorithmic bias.