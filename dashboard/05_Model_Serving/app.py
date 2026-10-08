import pandas as pd
import mlflow.lightgbm
from fastapi import FastAPI, HTTPException
from .schemas import TransactionInput
import uvicorn
import warnings

warnings.filterwarnings('ignore')

from fastapi import FastAPI
app = FastAPI()

app = FastAPI(
    title="Risk API",
    description="Microservice untuk deteksi anomali kartu kredit",
    version="1.0.0"
)

# 1. Konfigurasi MLflow Server Local
mlflow.set_tracking_uri("http://localhost:5000")

# 2. Mengambil Model dari Registry (Ganti '1' dengan versi model Anda)
MODEL_NAME = "Risk_LGBM_Production"
MODEL_VERSION = 1
MODEL_URI = f"models:/{MODEL_NAME}/{MODEL_VERSION}"

print(f"Memuat model dari {MODEL_URI}...")
try:
    # Memuat sebagai model LightGBM asli agar bisa menggunakan predict_proba
    model = mlflow.lightgbm.load_model(MODEL_URI)
    print("Model berhasil dimuat.")
except Exception as e:
    model = None
    print(f"Gagal memuat model: {e}")

@app.post("/predict_risk")
def predict_fraud_risk(transaction: TransactionInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model ML tidak tersedia.")
    
    try:
        # Konversi input Pydantic menjadi DataFrame
        input_data = pd.DataFrame([transaction.dict()])
        
        # Prediksi probabilitas (mengambil probabilitas kelas 1 / Fraud)
        fraud_probability = model.predict_proba(input_data)[0][1]
        
        # Menggunakan Threshold Optimal Anda (0.9741 dari Notebook 03)
        optimal_threshold = 0.9741
        is_fraud = bool(fraud_probability >= optimal_threshold)
        
        return {
            "status": "success",
            "risk_score": round(float(fraud_probability), 4),
            "is_fraud": is_fraud,
            "threshold_used": optimal_threshold,
            "action": "BLOCK" if is_fraud else "APPROVE"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/")
def root():
    return {"message": "Risk API is running"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)