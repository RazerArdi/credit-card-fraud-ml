FROM python:3.10-slim

WORKDIR /app

# Salin seluruh file proyek ke dalam container
COPY . /app

# Install semua library yang dibutuhkan
RUN pip install --no-cache-dir -r requirements.txt

# Beri izin eksekusi untuk bash script
RUN chmod +x start.sh

# Beritahu HF Spaces port mana yang terbuka
EXPOSE 7860

# Jalankan script
CMD ["./start.sh"]