import os
import jwt
import pandas as pd
import mlflow.lightgbm
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .schemas import TransactionInput
import uvicorn
import warnings

warnings.filterwarnings("ignore")

# 1. Inisialisasi FastAPI
app = FastAPI(
    title="Risk API",
    description="Microservice untuk deteksi anomali kartu kredit dengan otentikasi JWT",
    version="1.0.0",
)

# 2. Konfigurasi Keamanan (JWT)
security = HTTPBearer()
API_SECRET_KEY = os.getenv("API_SECRET_KEY", "super-secret-key-for-jwt")


def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Fungsi dependensi untuk memvalidasi Bearer Token JWT pada request header."""
    try:
        payload = jwt.decode(
            credentials.credentials, API_SECRET_KEY, algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token telah kedaluwarsa"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token otentikasi tidak valid",
        )


# 3. Konfigurasi MLflow Server & Pemuatan Model
mlflow.set_tracking_uri("http://localhost:5000")

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

# 4. Endpoints


@app.get("/")
def root():
    """Health check endpoint (Dibiarkan publik tanpa otentikasi)."""
    return {"message": "Risk API is running securely."}


@app.post("/predict_risk")
def predict_fraud_risk(
    transaction: TransactionInput, token_payload: dict = Depends(verify_jwt)
):
    """Endpoint inferensi ML (Dilindungi oleh JWT)."""
    if model is None:
        raise HTTPException(
            status_code=500, detail="Model ML tidak tersedia di server."
        )

    try:
        # Konversi input Pydantic menjadi DataFrame
        input_data = pd.DataFrame([transaction.dict()])

        # Prediksi probabilitas (mengambil probabilitas kelas 1 / Fraud)
        fraud_probability = model.predict_proba(input_data)[0][1]

        # Menggunakan Threshold Optimal Anda (0.9741)
        optimal_threshold = 0.9741
        is_fraud = bool(fraud_probability >= optimal_threshold)

        return {
            "status": "success",
            "authorized_client": token_payload.get("sub", "Unknown Client"),
            "risk_score": round(float(fraud_probability), 4),
            "is_fraud": is_fraud,
            "threshold_used": optimal_threshold,
            "action": "BLOCK" if is_fraud else "APPROVE",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
