FROM python:3.10-slim

WORKDIR /app

# Salin seluruh file proyek ke dalam container
COPY . /app

# Install library untuk FastAPI (Backend) dan Dash (Frontend)
RUN pip install --no-cache-dir -r dashboard/Model_Serving/requirements.txt
RUN pip install --no-cache-dir -r dashboard/Dashboard/requirements.txt

# Beri izin eksekusi untuk bash script
RUN chmod +x start.sh

# Beritahu platform port mana yang terbuka
EXPOSE 7860

# Jalankan script
CMD ["./start.sh"]