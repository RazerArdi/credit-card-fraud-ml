# User Manual & Operations Guide: Risk System

This guide explains how to configure, run, and use the **Risk Fraud Analytics System**. The system consists of a Machine Learning API microservice, an interactive business dashboard, a RAG-based AI Copilot, and Power BI data export.

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Environment Configuration](#2-environment-configuration)
3. [Building the Knowledge Base (ChromaDB)](#3-building-the-knowledge-base-chromadb)
4. [Execution Method A: Docker Compose](#4-execution-method-a-docker-compose)
5. [Execution Method B: Local Development](#5-execution-method-b-local-development)
6. [Exporting Data for Power BI](#6-exporting-data-for-power-bi)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Prerequisites

| Requirement | Details | Needed for |
| --- | --- | --- |
| **Python 3.10+** | Application runtime | Local development, knowledge base build |
| **Git** | Cloning the repository | All modes |
| **Docker & Docker Compose** | Containerized deployment | Docker mode only |

---

## 2. Environment Configuration

The system uses a `.env` file for secrets management, API authentication, and AI telemetry. Create it in the **root directory** (alongside `README.md`):

```env
# 1. AI Copilot (Groq API)
GROQ_API_KEY=your_groq_api_key_here

# 2. FastAPI Security (JWT authentication)
API_SECRET_KEY=your_secure_jwt_secret_key

# 3. Model Registry (MLOps)
MLFLOW_TRACKING_URI=http://localhost:5000

# 4. LangSmith Telemetry (RAG monitoring, optional)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=Risk_Production
```

> **Security:** Never commit `.env`. Make sure it is listed in `.gitignore`.

---

## 3. Building the Knowledge Base (ChromaDB)

The AI Copilot needs a local vector database to answer operational queries based on compliance documents. **Run this step once locally**, regardless of whether you later use Docker or manual execution.

1. Place your reference PDFs in the `knowledge_base/` folder.
2. Install the dashboard dependencies:

```bash
   pip install -r dashboard/06_Dashboard/requirements.txt
```

3. Run the vector database builder:

```bash
   cd dashboard/06_Dashboard/core/
   python build_vector_db.py
   cd ../../../
```

4. Verify that a `chroma_db/` directory now exists in the project root.

> Re-run this step whenever you add new documents to `knowledge_base/`.

---

## 4. Execution Method A: Docker Compose

Recommended for a clean, isolated, production-like deployment. It runs the backend API and the frontend dashboard together in containers.

### 4.1. Launch the System

From the root directory:

```bash
docker compose up -d --build
```

> On older Docker versions, use `docker-compose` instead of `docker compose`.

### 4.2. Access the Services

| Service | URL |
| --- | --- |
| **Operational Dashboard** | http://localhost:8050 |
| **Inference API (Swagger UI)** | http://localhost:8000/docs |

### 4.3. Manage the Containers

| Goal |  |
| --- | --- |
| View live logs | `docker compose logs -f` |
| Stop without removing containers | `docker compose stop` |
| Start again after stopping | `docker compose start` |
| Remove containers and networks | `docker compose down` |

---

## 5. Execution Method B: Local Development

Use this method when you are actively modifying the code and need hot-reloading. **Open three separate terminals** so the services run concurrently.

### 5.1. Install Dependencies

From the root directory:

```bash
pip install -r dashboard/05_Model_Serving/requirements.txt
pip install -r dashboard/06_Dashboard/requirements.txt
```

### 5.2. Terminal 1: MLflow Model Registry

Starts the tracking server so the system can fetch the latest model artifacts.

```bash
# Run from the root directory
mlflow server --host 127.0.0.1 --port 5000
```

### 5.3. Terminal 2: FastAPI Inference Engine

Starts the backend prediction microservice.

```bash
# Run from the root directory
uvicorn dashboard.05_Model_Serving.app:app --host 0.0.0.0 --port 8000 --reload
```

API documentation: http://localhost:8000/docs

### 5.4. Terminal 3: Dash Operational Dashboard

Starts the frontend. Run it from inside its own directory so static assets (CSS and images) load correctly.

```bash
cd dashboard/06_Dashboard/
python app.py
```

Dashboard: http://localhost:8050

---

## 6. Exporting Data for Power BI

To generate management reports, export the model predictions into a flat table (Data Mart).

1. Open a terminal in the project root.
2. Run the exporter:

```bash
   python report/export_powerbi.py
```

3. The script writes the output to `dataset/03_powerbi/powerbi_fraud_mart.csv`.
4. Open Power BI Desktop (or `report/Fraud_Analytics_Report.pbix`), load the CSV, and map it to your visuals.

---

## 7. Troubleshooting

| Issue | Resolution |
| --- | --- |
| **`ImportError: cannot import name 'TransactionInput'`** | Run the `uvicorn`  from the **root directory** as shown in Section 5.3, not from inside the `05_Model_Serving` folder. |
| **Error 400 (message length) on AI Copilot** | Make sure the Groq model set in `ai_assistant.py` supports a large context window (for example `llama-3.1-8b-instant`). Do not use prompt-guard models for RAG. |
| **Cannot fetch MLflow model metadata** | Verify that Terminal 1 (`mlflow server`) is running on port 5000. If it is unavailable, the dashboard falls back to default metrics. |
| **`401 Unauthorized` on the API** | The `/predict_risk` endpoint is secured by JWT. Make sure your API client (for example Postman) sends a Bearer token generated with your `API_SECRET_KEY`. |
| **ChromaDB SQLite3 error** | If you see an outdated `pysqlite3` version error, delete the `chroma_db/` folder, run `pip install --upgrade chromadb`, then rebuild the knowledge base (Section 3). |

---

<div align="center">

**Risk: Enterprise Fraud Analytics & Intelligence System**

© 2026 Bayu Ardiyansyah

</div>