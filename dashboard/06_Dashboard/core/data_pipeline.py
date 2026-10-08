import os
import pandas as pd
import numpy as np
import mlflow

# Konfigurasi Path (Mundur 4 tingkat dari /core/data_pipeline.py ke root project)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_PATH = os.path.join(BASE_DIR, 'dataset', '01_raw', 'fraudTest.csv')

def fetch_system_metadata() -> dict:
    """Mengambil metadata model secara dinamis dari MLflow."""
    metadata = {
        "model_name": "LightGBM",
        "version": "Offline",
        "threshold": 0.9741, 
        "distance_engine": "Haversine (KM)",
        "pr_auc": "N/A"
    }
    try:
        mlflow.set_tracking_uri("http://localhost:5000")
        client = mlflow.tracking.MlflowClient()
        versions = client.get_latest_versions("RiskCommand_LGBM_Production", stages=["None", "Production"])
        if versions:
            latest = versions[-1]
            metadata["version"] = f"v{latest.version}"
            run = client.get_run(latest.run_id)
            metadata["pr_auc"] = f"{run.data.metrics.get('pr_auc', 0.0):.4f}"
    except Exception:
        pass
    return metadata

def load_and_prep_data() -> pd.DataFrame:
    """Memuat dan menyimulasikan hasil klasifikasi untuk kebutuhan visualisasi."""
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame(columns=['is_fraud', 'amt', 'lat', 'long', 'hour', 'month', 'merchant', 'category', 'predicted_fraud'])
    
    df = pd.read_csv(DATA_PATH)
    df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
    df['hour'] = df['trans_date_trans_time'].dt.hour
    df['month'] = df['trans_date_trans_time'].dt.strftime('%Y-%m')
    
    # Simulasi prediksi berdasarkan matriks performa asli (Recall 77%, Precision 91%)
    np.random.seed(42)
    df['predicted_fraud'] = 0
    
    actual_fraud_idx = df[df['is_fraud'] == 1].index
    caught_fraud_idx = np.random.choice(actual_fraud_idx, size=int(len(actual_fraud_idx) * 0.77), replace=False)
    df.loc[caught_fraud_idx, 'predicted_fraud'] = 1
    
    tp_count = len(caught_fraud_idx)
    fp_count = int((tp_count / 0.91) - tp_count)
    actual_normal_idx = df[df['is_fraud'] == 0].index
    false_alarm_idx = np.random.choice(actual_normal_idx, size=fp_count, replace=False)
    df.loc[false_alarm_idx, 'predicted_fraud'] = 1
    
    return df

def get_kpis(df: pd.DataFrame) -> dict:
    """Menghitung metrik finansial dan operasional."""
    tp_df = df[(df['is_fraud'] == 1) & (df['predicted_fraud'] == 1)]
    fp_df = df[(df['is_fraud'] == 0) & (df['predicted_fraud'] == 1)]
    fn_df = df[(df['is_fraud'] == 1) & (df['predicted_fraud'] == 0)]
    
    total_value = float(df['amt'].sum())
    loss_prevented = float(tp_df['amt'].sum())
    loss_escaped = float(fn_df['amt'].sum())
    
    # Asumsi biaya operasional review manual = $15 per False Positive
    review_cost = len(fp_df) * 15 
    net_savings = loss_prevented - review_cost
    
    # Metrik Efisiensi
    friction_rate = (len(fp_df) / (len(df) - df['is_fraud'].sum())) * 100 if len(df) > 0 else 0
    approval_rate = ((len(df) - df['predicted_fraud'].sum()) / len(df)) * 100 if len(df) > 0 else 0
    
    return {
        "total_trx": len(df),
        "total_value": total_value,
        "loss_prevented": loss_prevented,
        "loss_escaped": loss_escaped,
        "net_savings": net_savings,
        "friction_rate": friction_rate,
        "approval_rate": approval_rate,
        "fp_volume": len(fp_df),
        "review_cost": review_cost,
        "tp_volume": len(tp_df),
        "fn_volume": len(fn_df)
    }