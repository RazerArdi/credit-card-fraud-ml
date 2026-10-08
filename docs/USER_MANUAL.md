# Fraud Analytics System: User Manual & Operations Guide

This guide provides comprehensive instructions for configuring, running, and utilizing the **Fraud Analytics System**. This system includes a Machine Learning API, an interactive Business Dashboard, a RAG-based AI Copilot, and Power BI Data Export capabilities.

---

## 1. Environment Setup (Prerequisites)

Before running any components, ensure you have set up your virtual environment and environment variables.

### 1.1 Install Global Dependencies

Ensure you are in the project's root directory (`credit-card-fraud-ml/`) and run:

```bash
pip install -r dashboard/06_Dashboard/requirements.txt
```

> **Note:** You can also install dependencies per module inside their respective folders.

### 1.2 Configure API Keys & Environment Variables

Create a file named `.env` in the root directory (alongside the `README.md` file). Add the following credentials:

```env
# LLM Access for the AI Copilot (Required)
GROQ_API_KEY=your_groq_api_key_here

# MLflow Tracking URI (Optional, only needed if fetching live training metrics)
MLFLOW_TRACKING_URI=http://localhost:5000
```

---

## 2. Building the Knowledge Base for AI Copilot (RAG)

The AI Copilot requires a local Vector Database (ChromaDB) to answer questions based on internal SOPs and banking regulations. This setup only needs to be executed **once** (or whenever new PDF documents are added).

### 2.1 Place Reference Documents

Place your reference documents (e.g., Compliance Regulations, Investigation SOPs, Dispute Guidelines) into the `knowledge_base/` folder.

### 2.2 Run the Vector Database Builder

Run the following commands:

```bash
cd dashboard/06_Dashboard/core/
python build_vector_db.py
```

### 2.3 Wait for the Embedding Process

Wait for the embedding process to complete. A new folder named `chroma_db` will be generated in the root repository.

---

## 3. Running the Fraud Analytics Dashboard

The dashboard serves as the primary interface for analysts and executives. It is built with Dash (Python) using a standard MVC (Model-View-Controller) architecture.

### 3.1 Navigate to the Dashboard Directory

Open your terminal and navigate to the dashboard directory:

```bash
cd dashboard/06_Dashboard/
```

### 3.2 Launch the Application

Run:

```bash
python app.py
```

### 3.3 Access the Dashboard

Open your web browser and navigate to:

**`http://localhost:8050`**

### Dashboard Navigation Guide

* **Executive Summary:** Displays C-level metrics such as Total Processed Value (TPV), Net Savings (ROI), Customer Friction Rate, and monthly financial impact. Designed for management reporting.
* **Operations Monitor:** Displays a geospatial anomaly map (Haversine distance), temporal trends, and a real-time **Investigation Queue**. Designed for daily fraud operations monitoring.
* **Model Performance:** Displays MLOps technical metrics, the Confusion Matrix, and Explainable AI (SHAP) feature importance for algorithmic transparency audits.
* **AI Copilot:** An intelligent assistant that answers questions regarding live operational metrics and fraud handling procedures based on the documents stored in the `knowledge_base/` folder.

---

## 4. Exporting Data for Power BI (Data Mart)

To create advanced reports using Power BI, you need to export the processed model predictions (flat table format).

### 4.1 Run the Export Script

Open your terminal in the root project directory.

Run the export script:

```bash
python report/export_powerbi.py
```

### 4.2 Output

The system will process the operational data, append Confusion Matrix labels (TP, FP, FN, TN), and save it to:

`dataset/03_powerbi/powerbi_fraud_mart.csv`

### 4.3 Load Data into Power BI

Open **Power BI Desktop**, select *Get Data -> Text/CSV*, and load the generated file. You can save your final `.pbix` file inside the `report/` folder.

---

## 5. Running the Model Serving API (Optional)

If you need to test the REST API endpoint for real-time predictions (typically connected to a Payment Gateway):

### 5.1 Navigate to the Model Serving Folder

```bash
cd dashboard/05_Model_Serving/
```

### 5.2 Run the FastAPI Server

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 5.3 Access Swagger UI

Access the interactive Swagger UI documentation at:

**`http://localhost:8000/docs`**

---

## Troubleshooting

| Error / Issue                                  | Solution                                                                                                                                                             |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Error 400 (Length Messages) on AI Copilot**  | Ensure you are using an LLM with a large context window (e.g., `llama-3.1-8b-instant` or `mixtral-8x7b-32768`) in `ai_assistant.py`, **not** a `prompt-guard` model. |
| **Cannot fetch MLflow model metadata**         | Ensure your local MLflow server is running (`mlflow ui`) on port 5000. Otherwise, the dashboard will gracefully fallback to default metrics.                         |
| **ModuleNotFoundError during Power BI export** | Ensure you are running `python report/export_powerbi.py` directly from the project root directory, not from inside the `report/` folder.                             |
| **ChromaDB Error (sqlite3)**                   | This occurs if the system `pysqlite3` version is outdated. Delete the `chroma_db/` folder and reinstall dependencies using `pip install --upgrade chromadb`.         |
