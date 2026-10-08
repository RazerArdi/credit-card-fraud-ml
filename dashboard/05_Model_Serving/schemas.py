from pydantic import BaseModel, Field

class TransactionInput(BaseModel):
    # Fitur numerik utama yang diekstraksi
    amt: float = Field(..., description="Nominal transaksi dalam USD")
    distance_km: float = Field(..., description="Jarak antara pelanggan dan merchant (KM)")
    age: int = Field(..., description="Umur pelanggan")
    city_pop: int = Field(..., description="Populasi kota tempat tinggal pelanggan")
    
    # Fitur hasil Target Encoding (contoh)
    merchant_encoded: float = Field(..., description="Nilai risk smoothing dari merchant")
    job_encoded: float = Field(..., description="Nilai risk smoothing dari profesi")
    
    # Fitur Kategori Biner/One-Hot
    gender_M: int = Field(0, description="1 jika Laki-laki, 0 jika Perempuan")
    
    class Config:
        schema_extra = {
            "example": {
                "amt": 125.50,
                "distance_km": 15.2,
                "age": 34,
                "city_pop": 85000,
                "merchant_encoded": 0.005,
                "job_encoded": 0.001,
                "gender_M": 1
            }
        }