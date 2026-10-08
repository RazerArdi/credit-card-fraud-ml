import os
import importlib.util
import pandas as pd

# 1. Konfigurasi Path Absolut
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIPELINE_PATH = os.path.join(BASE_DIR, 'dashboard', '06_Dashboard', 'core', 'data_pipeline.py')
OUTPUT_DIR = os.path.join(BASE_DIR, 'dataset', '03_powerbi')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'powerbi_fraud_mart.csv')

# 2. Impor dinamis dari folder 06_Dashboard/core/data_pipeline.py
print(f"Mengimpor logika pipeline dari: {PIPELINE_PATH}")
spec = importlib.util.spec_from_file_location("data_pipeline", PIPELINE_PATH)
data_pipeline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(data_pipeline)

def generate_powerbi_dataset():
    print("Memproses dataset dengan prediksi model...")
    # Menarik data yang sama persis dengan yang ada di web dashboard
    df = data_pipeline.load_and_prep_data()
    
    # 3. Rekayasa Kolom Khusus Power BI (Confusion Matrix Labels)
    def get_confusion_label(row):
        if row['is_fraud'] == 1 and row['predicted_fraud'] == 1: 
            return 'Caught Fraud (TP)'
        if row['is_fraud'] == 0 and row['predicted_fraud'] == 1: 
            return 'False Alarm (FP)'
        if row['is_fraud'] == 1 and row['predicted_fraud'] == 0: 
            return 'Escaped Fraud (FN)'
        return 'Legitimate (TN)'
        
    df['classification_status'] = df.apply(get_confusion_label, axis=1)
    
    # 4. Simpan ke folder dataset/03_powerbi/
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Datasetdisimpan di:\n   -> {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_powerbi_dataset()