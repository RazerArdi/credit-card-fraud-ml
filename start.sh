#!/bin/bash
# 1. Jalankan FastAPI (Backend) di background (&)
uvicorn dashboard.Model_Serving.app:app --host 127.0.0.1 --port 8000 &

# 2. Tunggu sebentar agar API siap
sleep 3

# 3. Jalankan Dash (Frontend) di foreground (Port 7860)
python dashboard/Dashboard/app.py