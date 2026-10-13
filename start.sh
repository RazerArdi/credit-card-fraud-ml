#!/bin/bash
# Jalankan FastAPI (Backend) di background (&)
uvicorn dashboard.Model_Serving.app:app --host 127.0.0.1 --port 8000 &

sleep 3

# Jalankan Dash (Frontend) di foreground (Port 7860)
python dashboard/Dashboard/app.py