# dashboard/06_Dashboard/Dockerfile

# Gunakan base image Python yang ringan
FROM python:3.10-slim

# Set working directory di dalam kontainer
WORKDIR /app

# Salin file requirements terlebih dahulu untuk caching layer Docker
COPY requirements.txt .

# Instal dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode aplikasi dasbor ke dalam kontainer
COPY . .

# Ekspos port yang digunakan oleh Dash (default: 8050)
EXPOSE 8050

# Jalankan aplikasi server
CMD ["python", "app.py"]